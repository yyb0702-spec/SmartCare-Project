# 규칙 정본 지도

같은 규칙을 여러 문서에 복제하지 않는다. 참조 문서는 아래 정본을 링크하고, 규칙을 바꿀 때는 정본만 수정한다.

| 규칙 영역 | 단일 정본 | 참조하는 문서 |
| --- | --- | --- |
| 프로젝트 진입·작업 순서·STRICT 신호 | `AGENTS.md` | `CLAUDE.md`(@import), Context Router |
| 문서 라우팅(무엇을 읽고 무엇을 읽지 않을지) | `docs/ai/context-router.md` | AGENTS.md |
| 제품 요구사항 | `docs/product/DoctorPet-PRD.md` | SA, Issue 본문 |
| 설계·ERD·API·상태 머신·확정 기술 결정 | `docs/architecture/DoctorPet-SA.md` | Context Router, 구현 코드 |
| 코드 스타일·클래스 규약·예외·응답 포맷 | `docs/architecture/DoctorPet-코드컨벤션.md` | Review Gate, 구현 가드레일 |
| 정책 배경(원본) | `docs/domain/반려동물병원예약-정책정리본.md` | PRD·SA와 다르면 PRD·SA 우선 |
| 브랜치·커밋·PR·리뷰 절차 | `docs/collaboration/github-rules.md` | AGENTS.md 요약, PR 템플릿 |
| 검증 Level·판정 값·기록 양식 | `docs/testing/verification-guide.md` | Issue/PR 템플릿, 완료 체크리스트 |
| 리뷰 판정 기준 | `docs/ai/review-gate.md` | Context Router |
| Dev 구현 경계·범위 제한 | `docs/ai/implementation-guardrails.md` | Review Gate |
| PR 전 완료 점검 | `docs/ai/completion-checklist.md` | PR 작성 절차 |
| 반복 실수와 재발 방지 | `docs/ai/agent-mistakes.md` | 다음 작업의 계획 단계 |
| 하네스 무결성 검사(링크·경로·섹션) | `scripts/harness_check.py` | Harness Check CI, 완료 체크리스트. PRD·SA 헤더는 `N-M. 제목` 마침표 형식을 유지해야 인식된다 |
| 작업 보드 Status 자동화 | `.github/workflows/project-status.yml` | PR 템플릿의 `Closes #` 안내. 보드 컬럼명 변경 시 이 워크플로도 수정 |

## 문서 우선순위

내용이 충돌하면 **PRD > SA > 코드컨벤션** 순으로 따르고, 충돌 사실을 사용자에게 알린 뒤 정본을 수정한다. 정책정리본은 PRD·SA 아래이며, 브랜치·커밋·PR 절차 규칙은 `docs/collaboration/github-rules.md`가 별도 영역의 정본이다.

## 변경 규칙

- 참조 문서에는 설명을 복사하지 않고 정본 경로와 읽어야 하는 조건만 남긴다.
- 정본의 규칙을 바꾸면 그것을 참조하는 문서(위 표의 오른쪽 열)의 링크·요약이 어긋나지 않는지 확인한다.
- 충돌하는 문구가 발견되면 이 표의 정본을 우선하고 참조 문서를 수정한다.
