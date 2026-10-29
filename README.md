# Book Condition Grader · 중고책 품질등급 판독기

## 사진으로 바로 판독하기

ChatGPT에 **책 사진을 첨부하고 아래 두 줄을 보내세요.**

```text
https://github.com/delvering17/book-condition-grader/blob/main/GRADING.md
이거 품질판별해줘
```

[판독 지침](GRADING.md)에 검사 절차와 기준을 함께 담았습니다. 참조 문서를 따로 지정하거나 TXT를 내려받을 필요 없이 이 링크로 요청할 수 있도록 구성했습니다. 링크와 사진을 열람할 수 있는 환경이 필요하며, 링크만으로 실제 판독하는 방식은 아직 실사용 검증 전입니다.

저장소 홈 링크와 사진을 받은 AI는 위 판독 지침을 열어 첨부된 책의 품질을 검사합니다. 사진이 없다면 책 사진 한 장부터 요청합니다. 링크를 읽을 수 없다면 그 사실을 알리고 [대체 사용 방법](docs/installation-and-release.md)을 안내합니다.

책 사진을 ChatGPT 또는 Codex에 올리면 **알라딘 공개 품질표에 따른 예상등급**과 추가 확인 사항을 한국어로 안내하는 Skill 기반 오픈소스입니다. 사진 한 장부터 시작합니다. 알라딘·OpenAI와 제휴하거나 이들의 공식 감정을 제공하는 제품이 아닙니다.

백엔드·DB·MCP 서버·별도 모델 학습·외부 유료 API·API 키가 필요 없습니다. 이미지 이해는 사용 중인 ChatGPT/Codex가 수행하므로 해당 서비스의 요금제·사용 한도·이미지 접근 권한은 적용됩니다.

## 설치해서 계속 사용하기

**공개 플러그인 디렉터리: 미제출·미승인·미게시.** GitHub 공개와 OpenAI 디렉터리 승인은 별개입니다. 계정에서 Skill 설치를 지원하면 아래 방식으로 등록할 수 있습니다. 실제 사진 판독 정확도와 ChatGPT 화면에서의 설치 완료는 아직 검증하지 않았습니다.

1. [릴리스 페이지](https://github.com/delvering17/book-condition-grader/releases)에서 최신 버전의 `book-condition-grader-skill-*.zip`을 내려받습니다.
2. ChatGPT에서 **Skills → New Skill → Upload from your computer** 메뉴가 제공되면 이 ZIP을 업로드합니다. 메뉴 이름·제공 여부는 계정과 워크스페이스 정책에 따라 다를 수 있습니다.
3. 새 대화에서 Skill을 선택하고 책 사진을 올려 “이 책의 예상 품질등급을 알려줘”라고 요청합니다.

ZIP을 일반 대화에 첨부하는 것만으로 플러그인이 설치되지는 않습니다. 링크를 읽을 수 없는 환경을 위한 TXT 첨부 방법과 Codex·로컬 플러그인 설치법은 [설치·공개 배포 안내](docs/installation-and-release.md)를 참고하세요.

## 사용 예시

사진을 올린 뒤:

> 앞표지와 책등 사진이야. 중고로 팔기 전에 상태를 확인해 줘. 내부는 아직 확인하지 못했어.

응답 형식은 [예상등급 결과 예시](docs/grading-example.md)에서 확인할 수 있습니다. 예시는 가상 자료이며 실제 사진 시험 결과가 아닙니다.

## 권장 촬영 방법

- 밝고 균일한 빛에서 앞·뒤표지 전체와 책등·모서리를 찍습니다.
- 책배의 위·아래·옆 단면과 내부 처음·중간·끝, 펼친 제본을 보여줍니다.
- 손상은 근접 사진을 추가합니다. 2cm 전후라면 같은 평면에 자를 놓고 눈금과 양 끝을 함께 찍습니다.
- 필기·얼룩은 사진 장수가 아닌 서로 다른 **쪽수**를 알려줍니다. 일부 사진만으로 전체 쪽수를 확인할 수는 없습니다.
- 원래 겉표지·케이스·필수 부속물의 유무를 알려줍니다. 이름·전화번호 등은 가려도 됩니다.

모든 사진을 한꺼번에 준비할 필요는 없습니다. 결과에 영향을 주는 부족한 정보부터 안내합니다. [자세한 검사 안내](skills/book-condition-grader/references/inspection-guide.md)를 참고하세요.

## 기능과 제약

| 항목 | 범위 |
| --- | --- |
| 사진 | 표지·책등·책배·내부·제본의 관찰과 공식 기준 대조 |
| 등급 | 최상·상·중·매입불가, 근거 부족 시 판정 보류 |
| 미촬영 부위 | 확인 불가. 정상으로 가정하지 않음 |
| 크기·쪽수 | 근거 있는 측정·사용자 확인 필요. 수치 신뢰도 생성 안 함 |
| 매입 가능 여부 | 품질과 분리. ISBN·재고·가격 자동 조회 없음 |
| 동영상 | 직접 디코딩·프레임 추출 미구현. 열람 불가 시 캡처 사진 요청 |
| 계정 호환 | 이미지 및 Skill/플러그인 기능을 제공하는 환경 필요 |
| 검증 | 패키지 검증과 실제 사진 평가를 구분. [검증 현황](evals/validation-report.md) 참고 |

공식 표의 2cm·5쪽 경계와 반송 안내의 일부 표현이 다릅니다. 임의로 기준을 고치지 않고 품질표상 예상과 반송 가능성을 나누어 알립니다. [규칙 요약](skills/book-condition-grader/references/aladin-grading-rules.md)에 공식 규칙과 개발자 추론을 구분했습니다.

## 개발·패키징

Python 3.9 이상이면 외부 패키지 없이 패키징할 수 있습니다. 사진 판독 자체에는 Python도 필요 없습니다.

```sh
git clone https://github.com/delvering17/book-condition-grader.git
cd book-condition-grader
python3 scripts/package.py check
python3 -m unittest discover -s tests -v
python3 scripts/package.py build
```

`dist/`에 플러그인 ZIP, Skill ZIP, 일반 ChatGPT용 단일 지침 TXT와 SHA256 목록을 만듭니다. 링크용 `GRADING.md`는 Skill과 참조 문서에서 자동 생성합니다. 지침을 수정한 뒤 `python3 scripts/package.py guide`로 갱신하면, `check`가 원본과의 일치 여부도 확인합니다.

`plugin.json`은 최신 공식 문서의 portable Agent Plugins 형식이며, Skill은 루트 `skills/`에서 발견되므로 루트 `skills` 필드를 추가하지 않습니다. `.agents/plugins/marketplace.json`은 개발용 로컬 카탈로그입니다.

```text
plugin.json
GRADING.md                   링크 하나로 읽는 판독 지침 (자동 생성)
skills/book-condition-grader/
  SKILL.md
  agents/openai.yaml
  references/aladin-grading-rules.md
  references/inspection-guide.md
evals/                       시나리오·평가 지침·실행 현황
scripts/package.py           오프라인 구조 검증·패키징
tests/test_package.py        배포물과 검증기의 회귀 검사
docs/                        설치·호환성·개인정보 안내
assets/book.svg              프로젝트 자체 아이콘
.agents/plugins/marketplace.json
README.md / LICENSE / .gitignore
```

## 출처와 면책

판정 기준 확인일: **2026-10-29**. 필요한 조건만 요약했으며 공식 가이드 전체를 재배포하지 않습니다.

- [알라딘 PC 품질표·매입불가 안내](https://www.aladin.co.kr/shop/usedshop/wc2b_sales.aspx?tab=3)
- [알라딘 모바일 품질등급·반송조건](https://www.aladin.co.kr/m/c2b/c2b_help.aspx)
- [OpenAI Skill 제작](https://developers.openai.com/plugins/build/skills), [Plugin 패키징](https://developers.openai.com/plugins/build/plugins), [공개 제출](https://developers.openai.com/plugins/deploy/submission)

AI는 작은 손상·색·치수·누락을 오인할 수 있습니다. 실물 검사나 공식 매입 결정은 대신하지 않습니다. 본 프로젝트는 판매 신청·결제·배송을 처리하지 않습니다. [개인정보 안내](docs/privacy.md), [이용 안내](docs/terms.md), [기술 검증과 미구현 목록](docs/compatibility.md).

코드와 자체 작성 문서는 [MIT License](LICENSE)로 공개합니다. 제3자 상표·공식 문서는 각 권리자의 권리에 따릅니다.
