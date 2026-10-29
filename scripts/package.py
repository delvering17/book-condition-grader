#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "book-condition-grader"
SKILL_DIR = Path("skills") / SKILL_NAME
REFERENCES = ("aladin-grading-rules.md", "inspection-guide.md")
GRADES = {"최상", "상", "중", "매입불가", "판정 보류"}
README_START = "<!-- BEGIN GENERATED GRADING -->"
README_END = "<!-- END GENERATED GRADING -->"


def read_json(root, relative):
    return json.loads((root / relative).read_text(encoding="utf-8"))


def frontmatter(content):
    match = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
    if not match:
        raise ValueError("SKILL.md의 YAML 헤더가 없습니다")
    fields = {}
    for line in match[1].splitlines():
        key, sep, value = line.partition(":")
        if not sep or key in fields:
            raise ValueError("이 패키저는 중복 없는 단일행 헤더를 사용합니다")
        fields[key] = value.strip().strip('"')
    if set(fields) != {"name", "description"}:
        raise ValueError("이 프로젝트의 Skill 헤더는 name·description을 사용합니다")
    if fields["name"] != SKILL_NAME or not fields["description"]:
        raise ValueError("Skill 이름 또는 설명이 잘못되었습니다")
    return fields, content[match.end():]


def local_file(root, relative):
    candidate = root / relative
    if candidate.is_symlink() or not candidate.is_file():
        raise ValueError(f"배포 파일 누락 또는 심볼릭 링크: {relative}")
    if not candidate.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"패키지 밖의 경로: {relative}")
    return candidate


def plugin_files(root):
    manifest = read_json(root, "plugin.json")
    interface = manifest["extensions"]["com.openai"]["interface"]
    result = {Path("plugin.json"), Path("README.md"), Path("GRADING.md"), Path("LICENSE")}
    result.update(Path("docs") / name for name in (
        "privacy.md", "terms.md", "installation-and-release.md", "compatibility.md", "grading-example.md"
    ))
    result.update(Path("evals") / name for name in (
        "evaluation-guide.md", "test-cases.json", "results.json", "validation-report.md", "field-test-report.md"
    ))
    result.add(SKILL_DIR / "SKILL.md")
    result.add(SKILL_DIR / "agents/openai.yaml")
    result.update(SKILL_DIR / "references" / name for name in REFERENCES)
    result.update(Path(interface[key]) for key in ("composerIcon", "logo"))
    return sorted(result)


def validate(root=ROOT):
    manifest = read_json(root, "plugin.json")
    if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        raise ValueError("portable Agent Plugins 스키마를 사용해야 합니다")
    if manifest.get("name") != SKILL_NAME:
        raise ValueError("manifest의 이름이 다릅니다")
    if not re.fullmatch(r"\d+\.\d+\.\d+", manifest.get("version", "")):
        raise ValueError("배포 버전은 major.minor.patch 형식이어야 합니다")
    if any(key in manifest for key in ("skills", "apps", "hooks", "mcpServers")):
        raise ValueError("이 portable Skill 전용 manifest에 불필요한 컴포넌트가 있습니다")
    settings = manifest["extensions"]["com.openai"]
    if any(key in settings for key in ("apps", "hooks", "requires_local_executor")):
        raise ValueError("Skill 전용 패키지의 실행 범위가 변경되었습니다")
    interface = settings["interface"]
    for key, maximum in (("displayName", 30), ("shortDescription", 30),
                         ("longDescription", 4000), ("developerName", 80)):
        if not isinstance(interface.get(key), str) or not 0 < len(interface[key]) <= maximum:
            raise ValueError(f"표시 메타데이터 길이 오류: {key}")
    prompts = interface["defaultPrompt"]
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        raise ValueError("시작 프롬프트는 1~3개여야 합니다")
    if any(not isinstance(p, str) or not 0 < len(p) <= 128 for p in prompts):
        raise ValueError("시작 프롬프트 길이 오류")
    for key in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        if not interface[key].startswith("https://"):
            raise ValueError(f"HTTPS URL이 필요합니다: {key}")
    for key in ("composerIcon", "logo"):
        if not interface[key].startswith("./"):
            raise ValueError(f"루트 상대 경로가 필요합니다: {key}")
        asset = local_file(root, interface[key])
        svg = ET.parse(asset).getroot()
        bounds = [float(n) for n in svg.attrib["viewBox"].split()]
        if bounds[2] != bounds[3] or bounds[2] < 48 or asset.stat().st_size > 5 * 1024 * 1024:
            raise ValueError("아이콘은 48 이상 정사각형, 5MiB 이하여야 합니다")
    skill = local_file(root, SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    frontmatter(skill)
    for ref in REFERENCES:
        if f"references/{ref}" not in skill:
            raise ValueError(f"Skill의 참조 링크가 없습니다: {ref}")
        local_file(root, SKILL_DIR / "references" / ref)
    for relative in plugin_files(root):
        local_file(root, relative)
    if (root / "GRADING.md").read_text(encoding="utf-8") != grading_guide(root):
        raise ValueError("GRADING.md가 원본과 다릅니다. python3 scripts/package.py guide로 갱신하세요")
    readme = (root / "README.md").read_text(encoding="utf-8")
    if readme != updated_readme(root, readme):
        raise ValueError("README의 판독 지침이 원본과 다릅니다. python3 scripts/package.py guide로 갱신하세요")
    cases = read_json(root, "evals/test-cases.json")["cases"]
    ids = [case["id"] for case in cases]
    if len(cases) < 15 or len(set(ids)) != len(ids):
        raise ValueError("평가 사례는 고유 ID를 가진 15개 이상이어야 합니다")
    for case in cases:
        expected = case["expected"]
        if expected["grade"] not in GRADES or not expected["reasoning"]:
            raise ValueError(f"기대 판정 또는 근거 오류: {case['id']}")
        for key in ("unknowns", "follow_up", "rule_ids"):
            if not isinstance(expected[key], list):
                raise ValueError(f"평가 필드 오류: {case['id']}/{key}")
    result_log = read_json(root, "evals/results.json")
    results = result_log["cases"]
    if sorted(item["id"] for item in results) != sorted(ids):
        raise ValueError("평가 결과와 사례의 ID가 일치하지 않습니다")
    for result in results:
        if result["status"] not in {"not_run", "passed", "failed", "blocked"}:
            raise ValueError(f"평가 상태 오류: {result['id']}")
        if result["status"] in {"passed", "failed"}:
            if not result.get("actual_output") or not result.get("evidence"):
                raise ValueError(f"실행 출력·증거 없는 평가 결과: {result['id']}")
            local_file(root, result["actual_output"])
            for evidence in result["evidence"]:
                local_file(root, evidence)
    field_tests = result_log.get("field_tests", [])
    for field_test in field_tests:
        if field_test["status"] not in {"passed", "failed", "blocked"}:
            raise ValueError("실사용 테스트 상태가 잘못되었습니다")
        local_file(root, field_test["report"])
    catalog = read_json(root, ".agents/plugins/marketplace.json")
    entries = catalog["plugins"]
    if len(entries) != 1 or entries[0]["name"] != manifest["name"]:
        raise ValueError("로컬 카탈로그의 플러그인이 일치하지 않습니다")
    if entries[0]["source"] != {"source": "local", "path": "./"}:
        raise ValueError("로컬 카탈로그는 marketplace 루트의 플러그인을 가리켜야 합니다")
    if any((root / name).exists() for name in ("mcp.json", ".mcp.json", ".app.json")):
        raise ValueError("이 MVP에는 MCP·앱 설정을 포함하지 않습니다")
    return {"version": manifest["version"], "scenario_count": len(cases),
            "evaluated_count": sum(r["status"] in {"passed", "failed"} for r in results),
            "field_failures": sum(t["status"] == "failed" for t in field_tests)}


def standalone(root):
    _, body = frontmatter((root / SKILL_DIR / "SKILL.md").read_text(encoding="utf-8"))
    for ref in REFERENCES:
        body = re.sub(r"\[([^\]]+)\]\(references/" + re.escape(ref) + r"\)",
                      lambda match: f"{match[1]} (아래 첨부 참조 문서: {ref})", body)
    parts = ["이 파일은 중고책 판독용 지침과 참조 문서입니다. 책 사진 또는 열람 가능한 영상과 함께 제공하고 판독을 요청하세요.\n"
             "두 참조 문서가 아래에 포함되어 있습니다. 별도 파일을 찾는 대신 이 파일의 해당 첨부 참조 문서를 읽어 적용하세요.\n", body]
    for ref in REFERENCES:
        parts.extend((f"\n---\n첨부 참조 문서: {ref}\n", (root / SKILL_DIR / "references" / ref).read_text(encoding="utf-8")))
    return "\n".join(parts)


def grading_guide(root):
    version = read_json(root, "plugin.json")["version"]
    return (
        "# 책 사진 품질 판독 지침\n\n"
        f"지침 패키지 버전: {version}\n\n"
        "<!-- Skill과 참조 문서에서 자동 생성. python3 scripts/package.py guide로 갱신합니다. -->\n\n"
        "책 사진 또는 영상을 첨부하고 아래 저장소 링크만 ChatGPT에 보내세요. 영상은 실제 장면을 읽을 수 있는 환경에서 사용합니다.\n\n"
        "```text\n"
        "https://github.com/delvering17/book-condition-grader\n"
        "```\n\n"
        "이 문서를 읽는 AI는 첨부한 책 사진 또는 실제로 열람 가능한 영상 장면을 아래 지침으로 검사한다. "
        "검사 절차와 참조 내용은 이 문서에 함께 수록되어 있으므로 사용자에게 다른 파일을 읽으라고 지시할 필요가 없다. "
        "첨부가 없으면 사진 또는 장면마다 최소 2초씩 멈춰 찍는 영상의 촬영 방법을 안내한다. "
        "영상 장면을 읽을 수 없으면 캡처 사진을 요청한다. 링크나 첨부 내용을 읽지 못한 상태에서 판독한 척하지 않는다.\n\n"
        + standalone(root)
    )


def updated_readme(root, content):
    instructions = standalone(root)
    instructions = re.sub(
        r"```markdown\n.*?\n```",
        "결과에는 적용 지침, 예상등급, 판정 근거 표(검사 항목·관찰·규칙 ID·부분등급), 추가 확인, 종합 의견, 매입 확인, 비공식 주의사항을 포함한다.",
        instructions, flags=re.S,
    )
    version = read_json(root, "plugin.json")["version"]
    block = f"{README_START}\n\n## 판독 지침과 기준\n\n지침 패키지 버전: {version}\n\n{instructions}\n\n{README_END}"
    if README_START not in content and README_END not in content:
        return content.rstrip() + "\n\n" + block + "\n"
    if content.count(README_START) != 1 or content.count(README_END) != 1:
        raise ValueError("README의 자동 생성 구간 표시가 잘못되었습니다")
    before, remainder = content.split(README_START)
    _, after = remainder.split(README_END)
    return before + block + after


def write_guide(root=ROOT):
    readme = (root / "README.md").read_text(encoding="utf-8")
    new_readme = updated_readme(root, readme)
    (root / "GRADING.md").write_text(grading_guide(root), encoding="utf-8")
    (root / "README.md").write_text(new_readme, encoding="utf-8")


def write_zip(destination, files):
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)


def build(root=ROOT, output=None):
    summary = validate(root)
    output = output or root / "dist"
    output.mkdir(parents=True, exist_ok=True)
    prefix = f"{SKILL_NAME}"
    version = summary["version"]
    plugin = output / f"{prefix}-plugin-v{version}.zip"
    skill = output / f"{prefix}-skill-v{version}.zip"
    prompt = output / f"{prefix}-chatgpt-ko.txt"
    write_zip(plugin, [(p.as_posix(), local_file(root, p).read_bytes()) for p in plugin_files(root)])
    skill_paths = [p for p in plugin_files(root) if p.is_relative_to(SKILL_DIR)]
    files = [(str(Path(SKILL_NAME) / p.relative_to(SKILL_DIR)), local_file(root, p).read_bytes()) for p in skill_paths]
    files.append((f"{SKILL_NAME}/LICENSE", (root / "LICENSE").read_bytes()))
    write_zip(skill, files)
    prompt.write_text(standalone(root), encoding="utf-8")
    products = [plugin, skill, prompt]
    sums = "".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n" for p in products)
    (output / "SHA256SUMS").write_text(sums, encoding="utf-8")
    return products


def main():
    parser = argparse.ArgumentParser(description="중고책 Skill의 오프라인 구조 검증·패키징")
    parser.add_argument("command", choices=("check", "guide", "build"))
    args = parser.parse_args()
    try:
        if args.command == "guide":
            write_guide()
        summary = validate()
        print(json.dumps(summary, ensure_ascii=False))
        if args.command == "build":
            for product in build():
                print(product.relative_to(ROOT))
        print("패키지 구조 검증 완료. 이미지 판독 성능·포털 심사 통과를 의미하지 않습니다.")
    except (ValueError, KeyError, OSError, ET.ParseError) as exc:
        print(f"검증 실패: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
