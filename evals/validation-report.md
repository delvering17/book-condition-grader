# 검증 보고서

기록일: 2026-10-29 · 패키지 버전: 0.1.1

현재 실제 이미지·영상 평가 자료는 제공되지 않았다. `results.json`의 판독 사례는 모두 `not_run`이며, 아래 패키지 검증 통과와 혼동해서는 안 된다.

| 검사 | 결과 | 범위 |
| --- | --- | --- |
| 알라딘 PC·모바일 기준 확인 | 완료 | 도서표·매입불가·반송 안내 대조, 2cm·5쪽 경계 차이 기록 |
| OpenAI 공식 문서 확인 | 완료 | Skill 전용·portable 형식·제출·로컬 카탈로그·이미지 입력 |
| 프로젝트 패키지 검사 | 통과 | scripts/package.py check: 32개 시나리오, 실제 판독 실행 0개 |
| 패키징 회귀 검사 | 8개 통과 | tests/test_package.py: ZIP 경로·참조·개인 자료 제외·재현성·증거 없는 성공 기록 거부·링크 지침 갱신 누락 거부 등 |
| 공식 Agent Plugins JSON Schema | 통과 | agent-plugins.org의 1.0.0 스키마 다운로드 후 jsonschema Draft202012Validator 적용 |
| Skill Creator quick_validate | 통과 | 공식 로컬 skill-creator의 검사기: Skill is valid! |
| Codex CLI 로컬 카탈로그 발견 | 통과 | 0.165.0-alpha.1.2, 일회성 -c marketplaces 설정으로 AVAILABLE·version 0.1.0 반환 |
| Codex 플러그인 설치·모델 호출 | 미실행 | 목록 결과는 installed=false이며 발견 성공만 확인 |
| 단일 링크 지침 | 생성·원본 일치 검사 통과 | GRADING.md에 Skill·참조 내용을 함께 수록. 링크와 사진으로 실제 대화 판독은 미실행 |
| 공개 지침 URL 접근 | 일반 HTTP 200·웹 읽기 도구 실패 | GitHub 보기·raw URL 모두 비로그인 GET 200. 현재 웹 읽기 도구에서는 두 URL이 Cache miss로 열리지 않아 해당 경로의 내용 열람 성공을 확인하지 못함 |
| 실제 사진 판독 평가 | 미실행 | 이미지 미제공; 성공 수·정확도 없음 |
| 동영상 실제 프레임 분석 | 미실행·미구현 | 미지원 환경에서의 사진 대체 안내를 시나리오로 정의 |
| ChatGPT 설치 UI·호출 | 미실행 | 일반 ChatGPT 계정의 업로드·선택·사진 결과 미확인 |
| OpenAI 제출·심사·게시 | 미수행 | ZIP 제작과 승인·공개 게시를 구분 |

## 재현 기록

패키지 검사·8개 회귀 검사·빌드: Python 3.9.6, 외부 의존성 없음. Skill Creator 검사와 JSON Schema 검사는 `/tmp`의 임시 Python 가상환경에 PyYAML·jsonschema를 설치해 실행했다. 이 개발용 도구들은 사용자 판독 실행에 필요하지 않다.

공식 스키마: [Agent Plugins 1.0.0](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json). 스키마 검사는 portable manifest만 검증하며 내부 OpenAI 확장 필드 전체의 포털 유효성은 보장하지 않는다. 확장 필드의 길이·경로·아이콘은 별도 패키지 검사로 확인했다.

로컬 발견은 사용자 설정을 저장하지 않는 일회성 재정의로 확인했다:

```sh
codex -c 'marketplaces.book-condition-grader-local.source="/absolute/path/to/book-condition-grader"' \
  -c 'marketplaces.book-condition-grader-local.source_type="local"' \
  plugin list --marketplace book-condition-grader-local --available --json
```

반환된 항목: `book-condition-grader@book-condition-grader-local`, `version=0.1.0`, `installPolicy=AVAILABLE`, `installed=false`. 플러그인 경로는 저장소 루트로 해석됐다. 사용자의 전역 marketplace 등록·설치 설정은 변경하지 않았다.

스키마 통과·ZIP 생성·카탈로그 발견은 이미지 판독 성공이나 공개 심사 승인을 입증하지 않는다.

0.1.1 변경: README 맨 앞에 링크와 짧은 요청 예시를 추가하고 단일 판독 문서 GRADING.md를 생성했다. 실제 사진 판독 32개는 계속 미실행이며, 링크 경로가 모든 ChatGPT 환경에서 실행된다는 의미는 아니다.

게시 후 일반 HTTP 요청으로 GRADING.md 공개 접근을 확인했다. 현재 웹 읽기 도구는 GitHub 보기·raw 링크 모두 Cache miss를 반환했다. 파일이 공개되어 있다는 사실과 ChatGPT가 그 링크 내용을 실제로 읽는다는 사실은 별도로 검증해야 한다.
