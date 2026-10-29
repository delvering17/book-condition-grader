# 설치와 공개 배포

확인일: 2026-10-29. [OpenAI 패키징](https://developers.openai.com/plugins/build/plugins), [제출 절차](https://developers.openai.com/plugins/deploy/submission), [지침](https://developers.openai.com/plugins/plugin-guidelines)을 직접 확인했다. 문서상 지원과 이 프로젝트의 실기기 시험 결과는 [호환성 현황](compatibility.md)에서 구분한다.

## 일반 ChatGPT 사용자

책 사진을 첨부하고 아래 저장소 링크만 보낸다:

```text
https://github.com/delvering17/book-condition-grader
```

README에서 [전체 판독 지침](../GRADING.md)으로 연결한다. 사용자에게 개별 참조 문서를 지정하거나 별도의 요청 문장을 덧붙이도록 요구하지 않는다. 사진이 없다면 외관 6방향 촬영을 안내하되 한 장부터 받을 수 있다. 이 사용 경로는 링크·이미지 열람을 지원하는 환경이 필요하며 실제 사진 판독은 아직 미검증이다.

## Skill 설치 또는 파일 첨부로 사용

현재 OpenAI 디렉터리에는 게시되지 않았다. [GitHub Releases](https://github.com/delvering17/book-condition-grader/releases)에서 제공하는 Skill ZIP을, 계정에 제공되는 Skills → New Skill → Upload from your computer 메뉴로 업로드한다. 새 대화에서 Skill을 선택하고 사진을 첨부한다. [공식 업로드 사용 예](https://developers.openai.com/cookbook/examples/chatgpt/chatgpt_prompt_guide/chatgpt_prompt_guide)를 참고한다.

링크를 열 수 없고 Skill 설치도 지원하지 않는 환경이라면 릴리스의 `book-condition-grader-chatgpt-ko.txt`를 사진과 함께 대화에 첨부하고 “첨부 지침으로 이거 품질판별해줘”라고 요청한다. 이 파일은 SKILL과 참조 문서를 합쳐 만든 것이어서 참조 파일이 빠지지 않는다. 텍스트 파일의 내용을 읽지 못하면 파일 내용을 메시지에 붙여 넣는다. 새 대화에는 다시 제공해야 한다. 일반 대화에 ZIP 업로드만 해서는 설치되지 않는다.

공개 승인 후의 목표 흐름은 Plugins에서 설치 → 책 사진 업로드 → 예상등급 확인이다. 공개 게시 URL·자격·설치 가능 계정은 승인 전까지 확약하지 않는다.

## Codex에서 Skill 직접 사용

저장소를 복제한 뒤 그 프로젝트의 Codex 대화에서 다음과 같이 요청하면 설치 없이도 참조를 읽어 사용할 수 있다.

> skills/book-condition-grader/SKILL.md를 읽고 그 판독 절차로 첨부한 사진을 검사해 줘.

지속적으로 발견되게 하려면 복제한 저장소의 루트에서 다음을 실행한다. 기존 같은 이름 폴더가 있으면 덮어쓰지 말고 먼저 차이를 확인한다.

```sh
mkdir -p ~/.agents/skills
cp -R skills/book-condition-grader ~/.agents/skills/
```

새 Codex 대화에서 `$book-condition-grader`를 선택하고 사진을 첨부한다. [공식 Skill 범위·발견 규칙](https://learn.chatgpt.com/docs/build-skills)을 참고한다. 이 프로젝트는 사용자의 전역 설정을 자동 수정하지 않는다.

## 로컬 플러그인으로 사용

이 저장소의 `.agents/plugins/marketplace.json`은 루트 `./`의 플러그인을 가리킨다. 공식 지침상 경로는 `.agents/plugins` 폴더가 아닌 **marketplace 루트** 기준이다. 이름은 `book-condition-grader-local`이다.

```sh
codex plugin marketplace add /absolute/path/to/book-condition-grader
codex plugin marketplace list
```

지원되는 ChatGPT/Codex 데스크톱 앱을 다시 열고 Plugins의 해당 로컬 소스에서 설치한다. 원격 카탈로그를 지원하는 CLI라면 `codex plugin marketplace add delvering17/book-condition-grader --ref main`도 사용할 수 있다. 이는 로컬·저장소 배포 경로이며 공개 디렉터리 게시가 아니다. 웹·모바일에 동일한 로컬 설치 메뉴가 있다고 가정하지 않는다.

## 배포물 만들기

Python 3.9 이상에서 외부 패키지 없이 검사·패키징할 수 있다. 백엔드·DB·MCP·별도 모델 학습이나 API 키는 필요 없다. 사진 이해는 실행 중인 ChatGPT/Codex 환경을 사용한다.

```sh
git clone https://github.com/delvering17/book-condition-grader.git
cd book-condition-grader
python3 scripts/package.py guide
python3 scripts/package.py check
python3 -m unittest discover -s tests -v
python3 scripts/package.py build
```

생성물:

- `GRADING.md`: 링크로 읽을 수 있게 자동 생성하는 전체 판독 지침
- `dist/book-condition-grader-plugin-v0.1.2.zip`: 루트 plugin.json, Skill, 아이콘, 이용·개인정보 안내 포함
- `dist/book-condition-grader-skill-v0.1.2.zip`: 최상위 book-condition-grader/ 아래 SKILL.md와 참조 문서
- `dist/book-condition-grader-chatgpt-ko.txt`: 일반 대화용 전체 지침
- `dist/SHA256SUMS`: 배포물 무결성 확인용

사용자의 사진·`.git`·로컬 인증정보·개발용 실행 스크립트는 플러그인 ZIP에 포함하지 않는다. 텍스트 평가 시나리오와 검증 현황은 포함한다. 패키저 검증은 포털의 보안 스캔이나 실제 사진 판독 평가를 대신하지 않는다.

`GRADING.md`는 Skill과 참조 문서를 합쳐 생성한다. 원본을 수정한 뒤 `guide`로 갱신해야 `check`를 통과한다. portable 패키지는 루트 `plugin.json`과 `skills/`를 사용하고, 개발용 로컬 카탈로그는 `.agents/plugins/marketplace.json`에 둔다. 공식 규격 출처는 [Skill 제작](https://developers.openai.com/plugins/build/skills)과 [Plugin 패키징](https://developers.openai.com/plugins/build/plugins)을 참고한다.

## OpenAI 공개 제출

1. [제출 포털](https://platform.openai.com/plugins) 접근과 제출 권한을 확인한다. 공식 문서에 따르면 조직 소유자 또는 Apps Management Write 권한이 필요하며 개인/사업자 신원 확인을 완료해야 한다.
2. 게시자명과 지원·개인정보·이용 안내 URL이 실제 게시자와 일치하고 외부에서 열리는지 확인한다. `plugin.json`의 이름·버전·설명·아이콘을 검토한다. 임시 URL이나 가짜 감정 결과를 제출하지 않는다.
3. 사진 평가와 새 대화에서의 설치·호출을 실제로 시험한다. 현재 미실행 항목은 [평가 지침](../evals/evaluation-guide.md)대로 기록하고 미검증 상태를 숨기지 않는다. 가이드라인은 완성도·안정성을 요구하며 시험용 데모의 승인을 보장하지 않는다.
4. 플러그인 ZIP을 업로드하고 Metadata & Skills 자동 검사 결과를 해결한다. 필수 Skill 스캔이 끝난 뒤 정책 확인과 심사 제출을 진행한다.
5. 승인 후 별도 Publish를 실행한다. 승인과 게시가 완료된 뒤에만 README에 공개 설치 링크를 추가한다.

Skill 전용 플러그인은 MCP 심사의 5개 긍정·3개 부정 사례와 데모 영상 요건이 적용되지 않는다. 이 저장소의 evals는 자체 품질 검증을 위한 것으로 포털 MCP review 필드에 넣지 않는다. Skill 전용도 메타데이터·개인정보·정책 요건을 충족해야 하며 추가 등록 자격이 적용될 수 있다. 이 프로젝트에는 로컬 실행 요구, 훅, 앱 참조, MCP 설정이 없으므로 관련 허용목록이나 서버 인증 절차를 추가하지 않았다.

디렉터리에 보이는 이름은 선택한 검증된 개발자 신원에서 설정된다. 업로드 성공이 심사 통과나 공개 게시를 뜻하지 않는다. 포털 제출과 법적·정책 확인은 게시자 본인이 완료해야 하며 이 구현 과정에서 수행하지 않았다.

## GitHub에 직접 게시할 때

GitHub 권한이 없는 환경에서 시작했다면 로컬 검증 후 아래 순서로 새 공개 저장소를 만들 수 있다. 기존 저장소라면 새로 만들지 말고 적절한 origin을 사용한다.

```sh
git init -b main
git add .
git commit -m "Add book condition grading skill MVP"
gh auth login
gh repo create book-condition-grader --public --source=. --remote=origin --push
```

버전을 올릴 때 manifest를 변경하고 재검증·재패키징한 뒤 배포한다. Skill·메타데이터 변경의 OpenAI 반영에는 새 ZIP과 해당 심사 절차가 필요하다.
