"""P4 발행 정합 린트 — README + Issue 초안 + 공개 대상 패킷 섹션.

검사 (미션 P4):
  (A) 금지: "0% FPR"/"무오탐"/"0% 오탐" 등 (0% 오탐 헤드라인 금지 §37/L).
  (B) G2/현재 기업에 "fraud/분식/조작" (§6) — HUBG/WMK/GNE + 사명.
  (C) 대조군 회사가 주어인 부정 서술 (모델이 아니라 대조군을 주어로 한 유죄 문장).
  (D) pooled 수치가 standalone 병기 없이 등장.
  (E) E4/교차모델/opus 피평가자 언급에 EXPLORATORY 라벨 누락.
  (F) 수치 정합: 산문 통계가 동결 json(results_stats/wave2_results/synthesis)과 불일치
      + 알려진 stale 값 금지.
  (G) 교란(identity-masked) 프레임을 "lower bound/하한"으로 서술 금지 (D31 0-2, W3) —
      교정 문구("not a clean lower bound"/"하한이 아니다"/구조적 하한=홀드아웃)는 allowlist.
  (H) README가 E1 결과를 다루면 GRDX·78 co-presence 강제 (D31 0-1 — 누락형 왜곡 기계 차단).
  (I) 발행 표면이 3-arm delta(+6.0pp/−2.0pp/b−a/c−b)를 언급하면 confound(혼입)와
      draw-noise(draw 잡음) 단서 동반 강제 (D39 A-2 — arm (c) 설계 교란변수, L-7).
비영: 위반 0. 위반 시 라인·사유 출력 후 exit 1. `make verify`에 편입.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DOCS = ["README.md", "README.ko.md", "analysis/ISSUE_0_DRAFT.md",
        "analysis/ISSUE_1_WAVE2_DRAFT.md", "analysis/ISSUE_2_HOLDOUT_DRAFT.md",
        "docs/reader_validation/ONE_PAGER.md"]  # D42: 독자 검증 원페이저도 발행 표면

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
    """결과 JSON에서 유도한 정본 수치 — README에 전건 존재해야 (드리프트 기계 검출)."""
    r1 = json.load(open(REPO / "analysis/results_stats.json", encoding="utf-8"))["primary"]
    r2 = json.load(open(REPO / "analysis/wave2_results.json", encoding="utf-8"))["original"]
    return {
        "wave1_perm_p": [f"{r1['perm_p_one_sided']:.5f}".rstrip("0")],  # 0.00114
        "wave2_perm_p": [f"{r2['perm_p']:.5f}".rstrip("0")],            # 0.00116
        "wave2_auc": [f"{r2['auc']:.3f}"],                              # 0.829
        "wave1_fpr": ["13.6%", "3/22"],
        "wave2_fpr": ["21.7%", "5/23"],
        "wave2_ece": ["0.179"],
        "name_id_w2_frozen": ["21.9%"],
        # D31 0-1: 홀드아웃 tier 최고점 = 대조군 오탐 (GRDX 78) — README에 존재 강제.
        # co-presence(GRDX와 78 동시)는 check_canon의 (H) 규칙이 양 README에 검사.
        "e1_top_control_fp": ["GRDX"],
    }


def check_canon():
    """README ↔ 결과 JSON 수치 드리프트 검사 (키당 허용 문자열 중 1개 이상 존재)."""
    text = (REPO / "README.md").read_text(encoding="utf-8")
    viols = [("README.md", 0, f"canon drift: {key} — 기대 {variants} 중 어느 것도 README에 없음")
             for key, variants in canon().items()
             if not any(v in text for v in variants)]
    # (H) D31 0-1: E1 결과를 다루는 README에는 GRDX와 78이 함께 존재해야 PASS.
    for doc in ["README.md", "README.ko.md"]:
        t = (REPO / doc).read_text(encoding="utf-8")
        if re.search(r"\bE1\b|matched controls|매칭 대조군", t):
            if "GRDX" not in t or not re.search(r"\b78\b", t):
                viols.append((doc, 0, "(H) E1 커버 문서에 GRDX·78 co-presence 부재 "
                                      "(홀드아웃 tier 최고점=대조군 오탐 GRDX 78 — D31 0-1)"))
    # (I) D39 A-2: 3-arm delta를 언급하는 발행 표면은 confound·draw-noise 단서 동반.
    for doc in DOCS + ["analysis/synthesis.md"]:
        if not (REPO / doc).exists():
            continue
        t = (REPO / doc).read_text(encoding="utf-8")
        if THREEARM_DELTA.search(t):
            missing = []
            if not CONFOUND_TERM.search(t):
                missing.append("confound(혼입)")
            if not DRAWNOISE_TERM.search(t):
                missing.append("draw-noise(draw 잡음)")
            if missing:
                viols.append((doc, 0, f"(I) 3-arm delta 언급에 {' · '.join(missing)} "
                                      "단서 부재 (arm (c) 설계 교란변수 — D39 A-2, L-7)"))
    return viols


# (I) D39 A-2: 3-arm delta 언급 감지 + 필수 동반 단서 (문서 단위, check_canon에서 검사).
THREEARM_DELTA = re.compile(
    r"median\(\s*b\s*[−-]\s*a\s*\)|median\(\s*c\s*[−-]\s*b\s*\)"
    r"|b[−-]a\s+(contrast|대비)|c[−-]b\s+(contrast|대비)"
    r"|\+6\.0\s*pp|[−-]2\.0\s*pp", re.I)
CONFOUND_TERM = re.compile(r"confound|혼입|혼재|교란변수", re.I)
DRAWNOISE_TERM = re.compile(r"draw[- ]?noise|draw\s*잡음|재추첨\s*잡음", re.I)

# (G) D31 0-2 (W3): 교란 프레임 + lower bound/하한 결합 서술 금지 — 교정 문구는 allowlist.
PERTURB_TERM = re.compile(r"perturb|identity.?mask|identity.?blind|교란|정체[- ]?가림", re.I)
LOWER_BOUND_TERM = re.compile(r"lower\s+bound|하한", re.I)
LOWER_BOUND_ALLOW = re.compile(
    r"not a clean lower bound|clean lower bound|하한이 아니|덜 오염|less.?contaminat"
    r"|structural lower bound|구조적 하한", re.I)


STALE = [
    (r"316\s*파일", "stale manifest count (→ 402)"),
    (r"0%\s*FPR", "0% FPR 금지"),
    (r"FPR\s*[:=]?\s*0%", "0% FPR 금지"),
    (r"무오탐|오탐\s*0%|오탐률\s*0%", "0% 오탐 헤드라인 금지"),
    (r"0\.86\b(?!4)", None),  # 0.86 단독은 wave1 perturbed 0.864 축약 — 정보용(비차단)
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

    # (G) 교란 프레임을 lower bound/하한으로 서술 (±160자 창, allowlist 문구 예외)
    for m in PERTURB_TERM.finditer(text):
        win = text[max(0, m.start() - 160):m.end() + 160]
        if LOWER_BOUND_TERM.search(win) and not LOWER_BOUND_ALLOW.search(win):
            ln = text[:m.start()].count("\n") + 1
            viol.append((ln, f"(G) 교란 프레임+lower bound/하한 결합 서술 금지 (W3): "
                             f"{lines[ln-1].strip()[:70]}"))

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
    for path, ln, msg in check_canon():
        print(f"  {path}:{ln}: {msg}")
        total += 1
    if total:
        print(f"\nFAIL — 발행 정합 위반 {total}건")
        return 1
    print("PASS — 발행 정합 (0% 오탐·G2-fraud·대조군주어·pooled·EXPLORATORY·stale"
          "·canon 무위반)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
