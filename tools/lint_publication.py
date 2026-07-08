"""P4 발행 정합 린트 — README + Issue 초안 + 공개 대상 패킷 섹션.

검사 (미션 P4):
  (A) 금지: "0% FPR"/"무오탐"/"0% 오탐" 등 (0% 오탐 헤드라인 금지 §37/L).
  (B) G2/현재 기업에 "fraud/분식/조작" (§6) — HUBG/WMK/GNE + 사명.
  (C) 대조군 회사가 주어인 부정 서술 (모델이 아니라 대조군을 주어로 한 유죄 문장).
  (D) pooled 수치가 standalone 병기 없이 등장.
  (E) E4/교차모델/opus 피평가자 언급에 EXPLORATORY 라벨 누락.
  (F) 동결 헤드라인 값 존재 확인(canon 표의 각 값이 발행 문서에 그대로 존재 — 값 drift·삭제
      차단) + deprecated/stale 값 금지. 전체 산문 통계의 JSON 대조 recompute는 아직 아님
      (reproduce_analysis 소관 확장 = OWNER_QUEUE 리서치 항목; Q-E02 name-ID 25% 미해소).
비영: 위반 0. 위반 시 라인·사유 출력 후 exit 1. `make verify`에 편입.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DOCS = ["README.md", "analysis/ISSUE_0_DRAFT.md", "analysis/ISSUE_1_WAVE2_DRAFT.md",
        "analysis/ISSUE_2_HOLDOUT_DRAFT.md"]

G2 = {"HUBG": ["hub group"], "WMK": ["weis markets", "weis"], "GNE": ["genie energy", "genie"]}
FRAUD_WORDS = ["fraud", "분식", "조작", "manipulat"]
# 대조군 티커 (unified_table에서 group=control) — 부정 서술의 주어 금지 대상
CONTROL_TICKERS = None  # lazy


def controls():
    global CONTROL_TICKERS
    if CONTROL_TICKERS is None:
        import csv
        rows = csv.DictReader(open(REPO / "analysis/unified_table.csv", encoding="utf-8"))
        CONTROL_TICKERS = {r["ticker"].split("/")[0] for r in rows if r["group"] == "control"}
    return CONTROL_TICKERS


def canon():
    """동결 헤드라인 값 — 각 문자열이 발행 문서에 그대로 존재해야 한다(값 drift·삭제 차단).
    r1/r2 로드는 동결 JSON의 존재·파싱을 함께 검증한다(desync 조기 발견)."""
    json.load(open(REPO / "analysis/results_stats.json", encoding="utf-8"))["primary"]
    json.load(open(REPO / "analysis/wave2_results.json", encoding="utf-8"))
    return {
        "wave1_perm_p": "0.00114", "wave2_perm_p": "0.00116", "wave2_auc": "0.829",
        "wave1_fpr_n": "3/22", "wave2_fpr_n": "5/23", "wave2_ece": "0.179",
        "name_id_w2_frozen": "21.9%",  # 동결 규칙값 — 25%(사람판독)는 Q-E02(병기 규약)
    }


STALE = [
    (r"316\s*파일", "stale manifest count (→ 402)"),
    (r"0%\s*FPR", "0% FPR 금지"),
    (r"FPR\s*[:=]?\s*0%", "0% FPR 금지"),
    (r"무오탐|오탐\s*0%|오탐률\s*0%", "0% 오탐 헤드라인 금지"),
    (r"0\.86\b(?!4)", None),  # 0.86 단독은 wave1 perturbed 0.864 축약 — 정보용(비차단)
    # deprecated RP-05 파일럿 값이 현행 헤드라인으로 등장 금지 (감사 A3)
    (r"\b0\.0226\b", "RP-05 파일럿 p — 현행 8v22 헤드라인은 0.00114"),
    (r"\b0\.797\b", "RP-05 파일럿 AUC — 현행 wave-1은 0.824"),
]
ADVERSE = re.compile(r"(overstat|misstat|분식|조작|manipulat|fraudulent|허위|은폐)", re.I)


def lint_doc(path):
    viol = []
    text = (REPO / path).read_text(encoding="utf-8")
    low = text.lower()
    lines = text.splitlines()

    # (A) 0% FPR / 무오탐
    for pat, why in [(r"0%\s*fpr", "0% FPR"), (r"무오탐", "무오탐"),
                     (r"오탐\s*0%|오탐률\s*0%", "0% 오탐"), (r"fpr[^\n]{0,12}0\s*%", "FPR 0%")]:
        for m in re.finditer(pat, low):
            ln = low[:m.start()].count("\n") + 1
            viol.append((ln, f"(A) 0% 오탐류 금지: {lines[ln-1].strip()[:80]}"))

    # (B) G2 + fraud word (동일 문장 내)
    for sent in re.split(r"(?<=[.。\n])", text):
        s = sent.lower()
        if any(fw in s for fw in FRAUD_WORDS):
            for tk, names in G2.items():
                if tk.lower() in s or any(n in s for n in names):
                    # provisional/non-reliance 부인 문맥이면 허용
                    if "provisional" in s or "non-reliance" in s or "restatement" in s or "금지" in s or "쓰지 않" in s:
                        continue
                    ln = text[:text.find(sent)].count("\n") + 1
                    viol.append((ln, f"(B) G2 {tk}에 fraud류 서술: {sent.strip()[:80]}"))

    # (C) 대조군 티커가 부정 서술 주어 — 티커 직후 8단어 내 부정 술어
    for tk in controls():
        for m in re.finditer(rf"\b{re.escape(tk)}\b", text):
            tail = text[m.end():m.end()+80]
            if ADVERSE.search(tail) and not re.search(r"오탐|false.positive|대조군|control|근거됨|양성 오독", tail, re.I):
                ln = text[:m.start()].count("\n") + 1
                viol.append((ln, f"(C) 대조군 {tk} 주어+부정술어 의심: …{tail.strip()[:60]}"))

    # (D) pooled without standalone
    if re.search(r"pooled", low) and "standalone" not in low and "병기 전용" not in text and "2차 병기" not in text:
        viol.append((0, "(D) pooled 언급에 standalone 병기 부재"))

    # (E) EXPLORATORY on cross-model / opus evaluatee
    for m in re.finditer(r"(교차모델|cross-?model|opus-4-8|e4\b)", low):
        win = low[max(0, m.start()-120):m.end()+120]
        if "exploratory" not in win:
            ln = low[:m.start()].count("\n") + 1
            viol.append((ln, f"(E) 교차모델/opus 언급에 EXPLORATORY 라벨 부재: {lines[ln-1].strip()[:70]}"))

    # (F) stale forbidden
    for pat, why in STALE:
        if why is None:
            continue
        for m in re.finditer(pat, text):
            ln = text[:m.start()].count("\n") + 1
            viol.append((ln, f"(F) stale/금지 '{why}': {lines[ln-1].strip()[:70]}"))

    return viol


def main():
    total = 0
    for path in DOCS:
        if not (REPO / path).exists():
            continue
        v = lint_doc(path)
        for ln, msg in v:
            print(f"  {path}:{ln}: {msg}")
        total += len(v)

    # (F) 동결 헤드라인 값 존재 확인 — 각 canon 값이 발행 문서 어딘가에 그대로 있어야
    alltext = "\n".join((REPO / p).read_text(encoding="utf-8")
                        for p in DOCS if (REPO / p).exists())
    for label, val in canon().items():
        if val not in alltext:
            print(f"  <docs>: (F) 동결 헤드라인 값 부재/변경 — {label}={val}")
            total += 1
    if total:
        print(f"\nFAIL — 발행 정합 위반 {total}건")
        return 1
    print("PASS — 발행 정합 (0% 오탐·G2-fraud·대조군주어·pooled·EXPLORATORY·stale 무위반)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
