# 호환성과 미구현 항목

확인일: 2026-10-29. 이 문서의 ‘공식 지원’은 문서 확인이며, 이 저장소에서 실기기 성공을 측정했다는 뜻이 아니다.

| 항목 | 공식 문서에서 확인한 범위 | 이 프로젝트의 상태 |
| --- | --- | --- |
| Skill 전용 Plugin | MCP 없이 지침·참조만 포함 가능 | 구현 |
| portable 패키지 | 루트 plugin.json + skills/, OpenAI 설정은 extensions.com.openai | 구현·공식 스키마 검사 통과 |
| 단일 링크 요청 | Skill 내용을 대화에서 읽어 적용하는 사용 경로이며 자동 설치를 뜻하지 않음 | GRADING.md 제공·원본 일치 검사 통과, 실제 링크+사진 판독 미시험 |
| 사진 입력 | ChatGPT 이미지 첨부, Codex 이미지 입력 제공 | 사진 시험 자료 없음, 정확도 미측정 |
| ChatGPT Skill 업로드 | 공식 사용 안내에 업로드 경로 제시 | 해당 계정 UI의 실제 설치·호출 미시험 |
| 로컬 카탈로그 | 데스크톱·CLI의 로컬/Git marketplace 지원 | Codex CLI 0.165.0-alpha.1.2에서 AVAILABLE 발견 확인. 설치·모델 호출은 미시험 |
| 공개 디렉터리 | 제출·신원 확인·스캔·심사·승인 후 게시 | 미제출·미승인·미게시 |
| 동영상 | 환경에서 실제 프레임을 열람할 수 있을 때 관찰 가능. 확인한 문서로 공통 영상 업로드 계약은 입증되지 않음 | 장면마다 최소 2초 촬영 안내·열람 가능한 장면 검사 지침 제공. 별도 디코더·프레임 추출기 없음, 미지원 시 사진 캡처 대체 |

실행 때 실제 픽셀·프레임에 접근할 수 있는지가 우선이다. 현재 대화 도구에도 동영상을 직접 디코딩해 관찰하는 전용 도구는 없다. 모든 환경의 동영상 지원이 없다고 단정하는 대신, 확인되지 않은 기능을 사용했다고 하지 않는다.

## MVP에 포함하지 않은 것

- 동영상 디코딩·프레임 추출·전체 페이지 자동 검사
- ISBN·재고·매입가·매입 대상의 실시간 조회
- cm 자동 계측, 필기 전체 쪽수의 자동 보장
- 모델 학습·외부 API·백엔드·사용자 사진 보관
- OpenAI 포털의 신원 확인·정책 확인·심사 제출·공개 게시

사진만으로 냄새·물 젖은 이력·미촬영 내부·원래 부속물은 확인할 수 없다. 사용자 진술도 별도 출처로 표시한다. 잠정 예상과 판정 보류는 이 한계를 드러내는 동작이다.

## 확인한 1차 문서

- [Skills 제작·지원 리소스](https://developers.openai.com/plugins/build/skills)
- [Plugin 형식·로컬 marketplace](https://developers.openai.com/plugins/build/plugins)
- [포털 제출·Skill 전용 심사 범위](https://developers.openai.com/plugins/deploy/submission)
- [공개 가이드라인](https://developers.openai.com/plugins/plugin-guidelines)
- [ChatGPT·Codex 이미지 입력](https://learn.chatgpt.com/docs/image-inputs)
- [ChatGPT Skill 업로드 예시](https://developers.openai.com/cookbook/examples/chatgpt/chatgpt_prompt_guide/chatgpt_prompt_guide)

실제 실행·통과·미실행의 구분은 [검증 보고서](../evals/validation-report.md)에 기록한다.
