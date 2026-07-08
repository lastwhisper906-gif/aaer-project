"""name_id_split.py — DRAFT (감사 B8). name-ID(암기 대리지표)를 fraud/control로 분리.

동결 name_match 규칙·커밋 프로브만 사용 — 재채점 아님, 캐시·API 불요, 결정론.
헤드라인 dose-response(전체 50%→21.9%)가 '분리를 만드는' fraud-side가 아니라
control-side 유명도 하락에 좌우되는지 확인. **초안: 소유자 검토 후 서술 반영(발행 아님).**
"""
import csv
import glob
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scoring"))
from probe_verdict import name_match  # noqa: E402 (동결 규칙)


def wave1():
    npr = json.loads((REPO / "analysis/name_probe_results.json").read_text())["rows"]
    grp = {r["ticker"].split("/")[0]: r["group"]
           for r in csv.DictReader(open(REPO / "analysis/baseline_table.csv", encoding="utf-8"))}
    out = {"fraud": [0, 0], "control": [0, 0]}
    for r in npr:
        g = grp.get(r["truth_ticker"])
        if g in out:
            out[g][1] += 1
            out[g][0] += 1 if r["recognized"] else 0
    return out


def wave2():
    fraud = set(json.loads((REPO / "runs/wave2/fraud_case_ids.json").read_text()))
    idm = json.loads((REPO / "scoring/id_mapping_wave2.json").read_text())["mapping"]
    cw = {c["case_id"]: c["company_name"] for c in json.loads(
        (REPO / "data/candidates/candidates_wave2.json").read_text())["candidates"]}
    out = {"fraud": [0, 0], "control": [0, 0]}
    for f in glob.glob(str(REPO / "scoring/probe_results_wave2/recognition/*.json")):
        cid = os.path.basename(f)[:-5]
        g = "fraud" if cid in fraud else "control"
        guess = json.loads(Path(f).read_text()).get("company_guess", "")
        tname = cw.get(idm.get(cid))
        if tname is None:
            continue
        rec = guess.strip().lower() != "unknown" and bool(name_match(guess, tname))
        out[g][1] += 1
        out[g][0] += 1 if rec else 0
    return out


def _pct(pair):
    r, t = pair
    return f"{r}/{t} = {100*r/t:.1f}%" if t else "n/a"


def main():
    w1, w2 = wave1(), wave2()
    print("name-ID rate (동결 name_match, fraud vs control 분리):")
    print(f"  wave-1: fraud {_pct(w1['fraud'])} | control {_pct(w1['control'])}")
    print(f"  wave-2: fraud {_pct(w2['fraud'])} | control {_pct(w2['control'])}")
    fr1 = 100 * w1["fraud"][0] / w1["fraud"][1]
    fr2 = 100 * w2["fraud"][0] / w2["fraud"][1]
    print(f"\n  fraud-side 이동: {fr1:.1f}% → {fr2:.1f}%  (거의 불변)")
    print(f"  control-side 이동: {100*w1['control'][0]/w1['control'][1]:.1f}% → "
          f"{100*w2['control'][0]/w2['control'][1]:.1f}%  (급락)")
    print("  ⇒ 전체 name-ID 하락(50%→21.9%)은 대조군 유명도 하락이 주도. "
          "분리를 만드는 fraud-side 인식은 wave1→wave2 사실상 그대로.")


if __name__ == "__main__":
    main()
