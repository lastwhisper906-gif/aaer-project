"""가공(fictitious) 사명 결정론 생성 + EDGAR 전수 충돌 스크린 (IDENTITY_3ARM_PLAN §2, D36).

- 시드: sha256(case_id + "fictname-v1" + attempt) — 결정론, 충돌 시 attempt+1 (이력 로그).
- 충돌 스크린 (§6 실존 제3자 사명 사용 금지의 기계 강제):
  (a) 코인어 core(예: "Veldamont")가 EDGAR cik-lookup-data.txt(전 filer 사명,
      ~105만 행) 어느 행에도 부분 문자열로 등장하지 않아야 한다 (정규화: 대문자
      영숫자+공백).
  (b) 가공 티커가 company_tickers.json의 실존 티커와 불일치해야 한다.
- 참조 파일은 ~/aaer-data/reference/ (git 밖) — 스크린 전용, 페이로드 반입 없음.
출력: data/evaluatee/fict_names_wave2.json (case_id → name/ticker + 생성 이력).
"""
import hashlib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REF = Path.home() / "aaer-data/reference"
OUT = REPO / "data/evaluatee/fict_names_wave2.json"
FRAUD_IDS = json.loads((REPO / "runs/wave2/fraud_case_ids.json").read_text())

ONSETS = ["Var", "Nor", "Tel", "Mer", "Cal", "Dor", "Fen", "Gal", "Har", "Jor",
          "Kel", "Lan", "Mor", "Nel", "Orv", "Pel", "Quor", "Ral", "Sol", "Tal",
          "Ver", "Wel", "Xan", "Yor", "Zel"]
MIDS = ["a", "e", "i", "o", "u", "ia", "eo", "ai"]
CODAS = ["dine", "mont", "vale", "crest", "ford", "holm", "mere",
         "ridge", "stone", "wick", "worth", "fell", "brook", "field"]
SUFFIXES = ["Industries", "Holdings", "Group", "Corporation", "Enterprises",
            "Systems", "Manufacturing", "Logistics", "Brands"]


def norm(s: str) -> str:
    return re.sub(r"[^A-Z0-9 ]", " ", s.upper())


def candidate(case_id: str, attempt: int) -> tuple[str, str, str]:
    h = hashlib.sha256(f"{case_id}fictname-v1{attempt}".encode()).digest()
    core = (ONSETS[h[0] % len(ONSETS)] + MIDS[h[1] % len(MIDS)]
            + CODAS[h[2] % len(CODAS)])
    name = f"{core} {SUFFIXES[h[3] % len(SUFFIXES)]}"
    cons = [c for c in core.upper() if c.isalpha()]
    ticker = "".join(cons[:4])
    return core, name, ticker


def main() -> int:
    print("loading EDGAR reference lists...", flush=True)
    edgar_names = norm((REF / "cik-lookup-data.txt").read_text(encoding="latin-1"))
    tickers = {v["ticker"].upper() for v in
               json.loads((REF / "company_tickers.json").read_text()).values()}
    result = {"_meta": {
        "rule": "sha256(case_id+'fictname-v1'+attempt) 결정론; core가 EDGAR 전 filer명"
                " 부분문자열 불일치 AND 티커 실존 불일치일 때 채택 (D36)",
        "reference": "~/aaer-data/reference/{cik-lookup-data.txt(1,049,982행),"
                     "company_tickers.json(10,418)} — 스크린 전용, 페이로드 반입 없음",
        "warning": "가공 사명 — 실존 회사와 무관 (§6)"}, "names": {}}
    for cid in sorted(FRAUD_IDS):
        history = []
        for attempt in range(0, 50):
            core, name, ticker = candidate(cid, attempt)
            name_hit = norm(core) .strip() in edgar_names
            tick_hit = ticker in tickers
            history.append({"attempt": attempt, "core": core, "name": name,
                            "ticker": ticker, "edgar_name_collision": name_hit,
                            "ticker_collision": tick_hit})
            if not name_hit and not tick_hit:
                result["names"][cid] = {"company_name": name, "ticker": ticker,
                                        "core": core, "attempt_adopted": attempt,
                                        "history": history}
                print(f"{cid}: {name} ({ticker}) [attempt {attempt}]", flush=True)
                break
        else:
            print(f"FAIL — {cid}: 50 attempts 소진"); return 1
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    print(f"→ {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
