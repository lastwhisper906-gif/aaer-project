# RP-10 Phase 2.3 — 분석 전체 재현: make analysis (결정론, 네트워크 없음)
.PHONY: analysis verify
analysis:
	.venv/bin/python analysis/baselines.py
	.venv/bin/python analysis/stats.py
verify:
	.venv/bin/python tools/reproduce_analysis.py
	.venv/bin/python tools/verify_blindness.py
	.venv/bin/python tools/verify_manifest.py
