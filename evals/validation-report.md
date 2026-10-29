# 검증 보고서

기록일: 2026-10-29 · 패키지 버전: 0.2.0

기존 링크 방식의 일반 ChatGPT 실사용에서 지침 미준수 실패가 확인됐다. [실사용 검토](field-test-report.md)에 개인 사진·대화 전문 없이 문제를 기록했다. 수정된 0.2.0의 일반 ChatGPT 재시험은 아직 완료하지 않았다. `results.json`의 정형 시나리오 46개는 모두 `not_run`이며, 별도 실사용 실패 1건과 패키지 검사를 구분한다.

| 검사 | 결과 | 범위 |
| --- | --- | --- |
| 알라딘 PC·모바일 기준 확인 | 완료 | 도서표·매입불가·반송 안내 대조, 2cm·5쪽 경계 차이 기록 |
| OpenAI 공식 문서 확인 | 완료 | Skill 전용·portable 형식·제출·로컬 카탈로그·이미지 입력 |
| 프로젝트 패키지 검사 | 통과 | scripts/package.py check: 정형 시나리오 46개·실행 0개, 별도 실사용 실패 1건 기록 |
| 패키징 회귀 검사 | 17개 통과 | ZIP·참조·개인 자료 제외·재현성·증거 없는 성공 기록 거부·README 본문 기준 포함 및 변조·갱신 누락 검출 |
| ISBN 검증·URL 생성 | 7개 통과 (위 17개에 포함) | ISBN-13·ISBN-10·X·잘못된 체크 숫자·부가기호·쿼리 주입 거부, 정확한 읽기 전용 URL 생성 |
| 알라딘 ISBN 검색 폼·예시 HTTP 조회 | 직접 확인 | ActionType=1·SearchTarget=All·KeyWord GET 폼. 사용자 예시 번호의 ISBN 일치 상품·매입 안내 확인. 웹 읽기 도구는 검색 URL 접근 실패 |
| 공식 Agent Plugins JSON Schema | 통과 | agent-plugins.org의 1.0.0 스키마 다운로드 후 jsonschema Draft202012Validator 적용 |
| Skill Creator quick_validate | 통과 | 공식 로컬 skill-creator의 검사기: Skill is valid! |
| Codex CLI 로컬 카탈로그 발견 | 통과 | 0.165.0-alpha.1.2, 일회성 -c marketplaces 설정으로 AVAILABLE·version 0.1.0 반환 |
| Codex 플러그인 설치·모델 호출 | 미실행 | 목록 결과는 installed=false이며 발견 성공만 확인 |
| 단일 링크 지침 | 구조 보완·재시험 전 | README와 GRADING.md에 Skill·참조 내용을 함께 수록. 별도 링크 클릭을 하지 않아도 기준이 본문에 존재함을 검사 |
| 공개 지침 URL 접근 | 일반 HTTP 200·웹 읽기 도구 캐시 문제 | 이전 검사에서 파일 보기·raw URL은 HTTP 200이나 웹 읽기 도구는 Cache miss. 0.1.4 게시 후 저장소 홈의 웹 읽기는 성공했지만 사진 전용 안내가 있던 이전 README를 반환해 최신 지침 전달은 검증 실패 |
| 일반 ChatGPT 기존 링크 실사용 | 실패 확인 | 기준 적용 불명·미확인 제본 등급·불충분한 찢김 재판정. [검토 기록](field-test-report.md) 참고 |
| 정형 사진 평가·수정본 재시험 | 미실행 | 성공 수·정확도 없음. 기존 실사용 실패를 수정본 성공으로 표시하지 않음 |
| 동영상 장면 판독 | 미실행 | 열람 가능한 장면의 판독 지침·최소 2초 촬영 안내·미지원 시 캡처 대체 구현. 별도 디코더·프레임 추출기는 없음 |
| ChatGPT 설치 UI·호출 | 미실행 | 일반 ChatGPT 계정의 업로드·선택·사진 결과 미확인 |
| OpenAI 제출·심사·게시 | 미수행 | ZIP 제작과 승인·공개 게시를 구분 |

## 재현 기록

패키지 검사·17개 회귀 검사·빌드: Python 3.9.6, 외부 의존성 없음. Skill Creator 검사와 JSON Schema 검사는 `/tmp`의 임시 Python 가상환경에 PyYAML·jsonschema를 설치해 실행했다. 이 개발용 도구들은 사용자 판독 실행에 필요하지 않다.

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

0.1.2 변경: README 첫 코드블록을 저장소 홈 주소 한 줄로 바꾸고 일반 사용자용 외관 6방향 촬영표를 추가했다. 설치·배포·개발 설명은 별도 안내로 옮겼다. 사진 없는 링크 요청의 촬영 안내를 Skill과 T28 시나리오에 반영했으며, 실제 사진·링크 대화 평가는 여전히 미실행이다.

0.1.3 변경: 영상 내용을 실제로 읽을 수 있는 환경에서 사용할 수 있음을 안내하고, 각 외관 부위·펼친 페이지·손상 근접 장면에서 최소 2초씩 멈춰 촬영하도록 추가했다. 2초는 프로젝트의 촬영 권장사항이며 공식 등급 기준이나 영상 지원 보장이 아니다. T33의 영상 장면 시나리오를 포함해 33개 판독 사례는 모두 미실행이다.

0.1.4 변경: 기존 실사용 실패를 기록하고 README 본문에 판독 지침과 기준을 직접 포함했다. 일반 검색·개인 블로그 기준 대체를 하지 않도록 출처 절차를 명시하고, 적용 지침 표시·규칙 ID·제본 확인 불가·책등 찢김 보류를 보완했다. 새 회귀 시나리오 T34~T37은 아직 모델 실행을 하지 않았다.

0.1.4 게시 후 웹 읽기 확인에서는 저장소 홈이 새로 추가한 본문 지침과 영상 안내 없이 이전 README를 반환했다. 최신 GitHub 파일과 웹 읽기 서비스의 캐시 결과가 다를 수 있으므로, 같은 홈 주소만으로 최신 규칙 전달을 강제할 수 없다. 지침 패키지 버전을 본문에 표시하며 웹 도구가 최신 규칙을 읽었다고 보고하지 않는다.

0.2.0 변경: 뒷표지 ISBN 확인·체크 숫자 검증·공식 팔기 조회 링크와 조건부 응답 확인을 추가하고 간결한 결과 템플릿을 참조 문서로 통일했다. 예시 ISBN 9791141691370의 일반 HTTP 응답에는 일치 상품 1건과 매입 안내가 있었지만, 웹 읽기 도구의 같은 URL 열람은 실패했다. 이는 전체 사진 판독·ChatGPT 자동 조회의 성공을 의미하지 않는다. T38~T46을 포함한 정형 시나리오 46개는 미실행이다.
