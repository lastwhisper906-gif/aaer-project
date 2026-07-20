"""forward 사이클 봉인 (spec §9, D100) — 매니페스트·봉인 기록·OTS·push 명령.

usage: python tools/forward_seal.py --cycle forward/cycle_001

- 검증(forward_validate) 통과 후에만 봉인한다.
- MANIFEST.sha256 (결정론 순서) + SEAL_RECORD.md 생성.
- OpenTimestamps: `ots stamp MANIFEST.sha256` 시도 (무료·무계정). ots 부재
  시 정확한 설치·실행 명령을 SEAL_RECORD와 stdout에 기록 (봉인은 유효하되
  OTS 앵커 pending으로 표시).
- GitHub push는 소유자 자격증명 작업 — 정확한 명령을 방출한다 (§9-1).
- 재봉인 금지: MANIFEST.sha256 존재 시 거부 (교정은 새 사이클 — spec §3-5).
"""
import argparse
import datetime
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forward_common import (REPO, assert_subscription_only, manifest_text,
                            sha256_text, fail)
from forward_validate import validate


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycle", required=True)
    args = ap.parse_args()
    assert_subscription_only()
    cycle = REPO / args.cycle
    tag = f"forward-{cycle.name.replace('_', '-')}-seal"

    manifest = cycle / "MANIFEST.sha256"
    if manifest.exists():
        fail(f"{manifest} 이미 존재 — 재봉인 금지 (spec §3-5: "
             "교정은 새 사이클에서. aborted 처리는 SEAL_RECORD.md에 일자 기입)")
    errs = validate(cycle)
    if errs:
        fail("봉인 전 검증 위반 — forward_validate 참조:\n  " + "\n  ".join(errs))

    text = manifest_text(cycle)
    manifest.write_text(text, encoding="utf-8")
    mhash = sha256_text(text)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                          capture_output=True, text=True).stdout.strip()

    ots_bin = shutil.which("ots")
    ots_status = "pending — ots 클라이언트 부재"
    if ots_bin:
        r = subprocess.run([ots_bin, "stamp", str(manifest)], capture_output=True, text=True)
        ots_status = ("stamped — MANIFEST.sha256.ots 생성" if r.returncode == 0
                      else f"실패({r.returncode}): {r.stderr.strip()[:120]}")

    owner_cmds = (
        f"git add {cycle} && "
        f"git commit -m 'SEAL: {cycle.name} forward watchlist'\n"
        f"git tag -a {tag} -m 'forward seal {now} manifest sha256 {mhash}'\n"
        f"git push origin main --tags")
    record = cycle / "SEAL_RECORD.md"
    record.write_text(f"""# SEAL_RECORD.md — {cycle.name}

- sealed_at (UTC): {now}
- MANIFEST.sha256 자체의 sha256: `{mhash}`
- 봉인 시점 git HEAD (매니페스트 커밋 이전): `{head}`
- OpenTimestamps: {ots_status}
- 지연/중단 기록: (해당 시 일자 기입 — spec §3)

## 소유자 봉인 명령 (즉시 실행 — push 서버 시각이 외부 증거)

```bash
{owner_cmds}
```

## 외부 검증 방법 (제3자용)

1. **GitHub 서버 시각** (작성자 소급 조작 불가):
   `GET https://api.github.com/repos/lastwhisper906-gif/aaer-evals/git/refs/tags/{tag}`
   → tag object → tagger/commit의 서버 기록 시각 확인.
2. **OpenTimestamps** (무료·무계정): `ots verify MANIFEST.sha256.ots`
   (클라이언트: `pip install opentimestamps-client`). 앵커 pending이면
   수 시간 후 `ots upgrade MANIFEST.sha256.ots` 후 재검증.
3. **로컬 무결성**: `python tools/forward_verify_seal.py --cycle {cycle}`
""", encoding="utf-8")
    if ots_bin is None:
        print("NOTE — ots 부재: `pip install opentimestamps-client` 후 "
              f"`ots stamp {manifest}` 실행, .ots 파일 커밋 (무료)")
    print(f"SEALED — manifest {mhash}\n소유자 명령:\n{owner_cmds}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
