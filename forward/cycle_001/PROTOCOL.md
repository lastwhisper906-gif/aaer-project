# PROTOCOL.md — cycle_001 동결 프로토콜 스냅샷

- generated: 2026-07-20 (tools/forward_prepare.py)
- spec: specs/FORWARD_WATCHLIST_V1.md (규범 원문)
- screening_cutoff: 2026-11-15 (ET, EDGAR acceptance)
- evaluatee_model (pin): `claude-sonnet-5`
- execution path: subscription OAuth only — `claude -p` + `CLAUDE_CODE_OAUTH_TOKEN` via `pipeline/cli_client.py` (INVARIANT 4)
- draws: k=1 · retry ≤2 · decision cuts: ≥70 flag / 40–69 review / <40 no_flag / insufficient→abstain (사전 등록 서수 컷)

## 동결 파일 해시 (준비 시점)

- `docs/UNIVERSE_SELECTION.md` sha256 `4eac2e56221883355038d63361ffdab1098e9b2c8a0bdb483042da5cbafa4796`
- `pipeline/build_payload.py` sha256 `0d14da873c877b12949c7d4b155dad8e9d7b9272154d27b0eef1e3f81bc6f0f4`
- `pipeline/cli_client.py` sha256 `4ed377d465ce159d1e8d46fb66387092b197fddf66d1125937ede0f0ad5d4d99`
- `pipeline/runner.py` sha256 `383f2429985fe720649503fdca800ba71548ed2f1350ecea05ce03029827eb33`
- `schemas/llm_output.json` sha256 `fd04a2375a3c6e73fe4dcede5f318670d1f774febfc10b151f20646773fdb346`
- `specs/FORWARD_WATCHLIST_V1.md` sha256 `39e5f348c2052e440286fbcbd201324a274fcc74ee6a126b748d86af3b23f561`
- `specs/RISK_SCORE_SEMANTICS.md` sha256 `93012e66b1ae86d5336bcc5888b28662b4307372b9134baff99c1f4112dafd53`

모델 승계 조항·중단 규칙: spec §5·§3. 봉인 후 본 파일 수정 금지.
