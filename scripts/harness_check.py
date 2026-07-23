#!/usr/bin/env python3
"""DoctorPet 하네스 무결성 검사.

검사 범위 (의도적으로 3가지로 제한한다 — 검사기가 장애물이 되지 않게):
  1. 하네스 문서의 마크다운 상대 링크가 실제 파일을 가리키는가
  2. rule-source-map.md 표의 정본 경로가 실존하는가
  3. `PRD §X-Y` / `SA §X-Y` / `SA 부록 A·B` 참조가 실제 문서 헤더에 존재하는가
     (하네스 문서뿐 아니라 PRD·SA가 서로를 가리키는 상호 참조도 검사한다)

사용: python scripts/harness_check.py   (성공 시 exit 0, 결함 발견 시 exit 1)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 검사 대상 하네스 문서
HARNESS_DOCS = [
    "AGENTS.md",
    "CLAUDE.md",
    "docs/ai/context-router.md",
    "docs/ai/rule-source-map.md",
    "docs/ai/review-gate.md",
    "docs/ai/implementation-guardrails.md",
    "docs/ai/completion-checklist.md",
    "docs/ai/agent-mistakes.md",
    "docs/ai/remove-ai-slop.md",
    "docs/testing/verification-guide.md",
    ".github/ISSUE_TEMPLATE/feature.md",
]

PRD = ROOT / "docs/product/DoctorPet-PRD.md"
SA = ROOT / "docs/architecture/DoctorPet-SA.md"

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")
BACKTICK_PATH = re.compile(r"`((?:docs|scripts|\.github)/[^`\s]+\.(?:md|py|yml))`")
SECTION_REF = re.compile(r"(PRD|SA)\s*§(\d+(?:-\d+)?(?:~\d+(?:-\d+)?)?)")
APPENDIX_REF = re.compile(r"SA\s*부록\s*([AB])")


def load(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def headers_of(path: Path) -> set[str]:
    """문서의 '9-3.' '부록 A.' 같은 헤더 번호 집합.

    주의: PRD·SA 헤더는 반드시 `# N.` / `## N-M.` / `# 부록 A.`처럼
    번호 뒤 마침표 형식이어야 인식된다. 헤더 형식을 바꾸면 그 섹션을
    참조하는 모든 문서가 무더기 FAIL 나므로, 형식 변경 시 이 정규식도
    함께 갱신해야 한다 (rule-source-map.md에도 명시됨).
    """
    nums = set()
    for line in load(path).splitlines():
        m = re.match(r"^#{1,4}\s+(부록 [AB]|\d+(?:-\d+)?)\.", line)
        if m:
            nums.add(m.group(1))
    return nums


def expand_range(ref: str) -> list[str] | None:
    """'6-3~6-5' → ['6-3','6-4','6-5'], '9-3' → ['9-3'].

    역순(6-5~6-3)이나 대분류 교차(9-8~10-2)는 잘못된 표기이므로
    None을 반환한다 — 조용히 빈 리스트로 통과시키지 않는다.
    """
    if "~" not in ref:
        return [ref]
    start, end = ref.split("~")
    sm = re.match(r"(\d+)-(\d+)$", start)
    em = re.match(r"(?:(\d+)-)?(\d+)$", end)
    if not (sm and em):
        return None
    major = sm.group(1)
    if em.group(1) and em.group(1) != major:
        return None  # 대분류 교차 범위는 지원하지 않음
    lo, hi = int(sm.group(2)), int(em.group(2))
    if lo > hi:
        return None  # 역순 범위
    return [f"{major}-{i}" for i in range(lo, hi + 1)]


def check_section_refs(rel: str, text: str, prd_headers: set[str],
                       sa_headers: set[str], errors: list[str]) -> None:
    """`PRD §X` / `SA §X` / `SA 부록 A·B` 참조가 실제 헤더에 있는지 검사한다.

    알려진 한계: 코드펜스·인라인 코드 안의 표기도 검사 대상이다.
    현재 문서엔 해당 사례가 없어 방치하며, 예시에 섹션 표기를 쓰게 되면 펜스 스트립을 추가한다.
    """
    for m in SECTION_REF.finditer(text):
        doc_name, ref = m.group(1), m.group(2)
        headers = prd_headers if doc_name == "PRD" else sa_headers
        secs = expand_range(ref)
        if secs is None:
            errors.append(f"{rel}: 잘못된 섹션 범위 표기 → {doc_name} §{ref}")
            continue
        for sec in secs:
            if sec not in headers:
                errors.append(f"{rel}: {doc_name} §{sec} 헤더가 실제 문서에 없다")
    for m in APPENDIX_REF.finditer(text):
        if f"부록 {m.group(1)}" not in sa_headers:
            errors.append(f"{rel}: SA 부록 {m.group(1)} 헤더가 실제 문서에 없다")


def main() -> int:
    # Windows 콘솔(cp949)에서도 한글·특수문자 출력이 깨지지 않게 강제
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    errors: list[str] = []

    for name in ("PRD", "SA"):
        if not (PRD if name == "PRD" else SA).exists():
            print(f"FATAL: {name} 문서가 없다")
            return 1
    prd_headers = headers_of(PRD)
    sa_headers = headers_of(SA)

    for rel in HARNESS_DOCS:
        doc = ROOT / rel
        if not doc.exists():
            errors.append(f"{rel}: 파일이 없다")
            continue
        text = load(doc)

        # 1. 마크다운 상대 링크
        for m in MD_LINK.finditer(text):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (doc.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{rel}: 깨진 링크 → {target}")

        # 2. 백틱 경로 (rule-source-map 표 등)
        for m in BACKTICK_PATH.finditer(text):
            if not (ROOT / m.group(1)).exists():
                errors.append(f"{rel}: 없는 경로 참조 → `{m.group(1)}`")

        # 3. 섹션 참조
        check_section_refs(rel, text, prd_headers, sa_headers, errors)

    # PRD·SA 자체의 상호 §참조도 검증한다 (예: PRD가 "SA §9-6"을, SA가 "PRD §7"을 가리키는 경우).
    # 링크·백틱 경로 검사는 제외한다 — 프로즈·표가 많아 오탐이 나므로 섹션 참조만 본다.
    for doc in (PRD, SA):
        rel = doc.relative_to(ROOT).as_posix()
        check_section_refs(rel, load(doc), prd_headers, sa_headers, errors)

    if errors:
        print(f"FAIL — {len(errors)}건")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"PASS — 하네스 문서 {len(HARNESS_DOCS)}개 + PRD·SA 상호참조, 링크·경로·섹션 참조 이상 없음")
    return 0


if __name__ == "__main__":
    sys.exit(main())
