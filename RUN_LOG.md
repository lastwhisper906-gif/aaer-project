# RUN_LOG.md — D106 follow-up continuous session (2026-07-20 시작)

> authority: D106 (`governance/FEEDBACK_RESPONSE_v1.md`, owner-signed
> 2026-07-20). 규약: 산출물 1건 완료당 1줄 (path · stage · status) 추가,
> 차단·생략 항목은 사유와 함께 기록. 단계 종료마다 커밋
> ("D106 follow-up: <stage>").

| # | path | stage | status |
|---|------|-------|--------|
| 1 | RUN_LOG.md | setup | created |
| 2 | atlas/TEMPLATE.md | A1 | created |
| 3 | atlas/INDEX.md | A2 | created |
| 4 | atlas/case_39.md | A3 wave-2 T | drafted (§5 partial: insufficient sealed evidence, forgery leg) |
| 5 | atlas/case_40.md | A3 wave-2 T | drafted |
| 6 | atlas/case_52.md | A3 wave-2 T | drafted (FN; §5/§9 partial markers) |
| 7 | atlas/case_59.md | A3 wave-2 T | drafted |
| 8 | atlas/case_60.md | A3 wave-2 T | drafted |
| 9 | atlas/case_61.md | A3 wave-2 T | drafted |
| 10 | atlas/case_65.md | A3 wave-2 T | drafted (TP-for-wrong-reasons documented) |
| 11 | atlas/case_66.md | A3 wave-2 T | drafted |
| 12 | atlas/case_67.md | A3 wave-2 T | drafted (FN; structural input-absence documented) |
| 13 | atlas/case_01.md | A3 wave-1 T | drafted (§5/§9 partial markers; probe-draw split noted) |
| 14 | atlas/case_02.md | A3 wave-1 T | drafted (ungraded E&O leg → [OWNER REVIEW]) |
| 15 | atlas/case_03.md | A3 wave-1 T | drafted (FN despite recognition — documented) |
| 16 | atlas/case_06.md | A3 wave-1 T | drafted (FN; frame-flip +30 delta documented) |
| 17 | atlas/case_08.md | A3 wave-1 T | drafted (TP mechanism-wrong documented) |
| 18 | atlas/case_09.md | A3 wave-1 T | drafted |
| 19 | atlas/case_12.md | A3 wave-1 T | drafted (TP wrong-reason + recognition — documented) |
| 20 | atlas/case_13.md | A3 wave-1 T | drafted (perturbed-frame miss documented) |
| 21 | atlas/case_71.md | A3 holdout T | drafted (§2/§5/§9 partial — 8-K body not sealed locally) |
| 22 | atlas/case_72.md | A3 holdout T | drafted (FN; in-set vs not-in-set split documented) |
| 23 | atlas/case_73.md | A3 holdout T | drafted (FN; missed in-set insurance signal documented) |
| 24 | atlas/case_10.md | A3 FP | drafted (sealed record contradicts model's restatement reading) |
| 25 | atlas/case_30.md | A3 FP | drafted (distress-vs-misstatement over-reading) |
| 26 | atlas/case_33.md | A3 FP | drafted (label-window mismatch; out-of-window 4.02s) |
| 27 | atlas/case_37.md | A3 FP | drafted (deck chronology artifact + wrong-accession cite) |
| 28 | atlas/case_44.md | A3 FP | drafted (XBRL tag re-mapping artifact over-read) |
| 29 | atlas/case_48.md | A3 FP | drafted (grounded over-reading; benign ties documented) |
| 30 | atlas/case_49.md | A3 FP | drafted (pre-revenue biotech over-reading) |
| 31 | atlas/case_54.md | A3 FP | drafted (genuine world-facts over-read; draw-stable) |
| 32 | atlas/case_69.md | A3 FP | drafted (at-threshold boundary; benign one-time gain resolves spike) |
| 33 | atlas/hc_03.md | A3 FP | drafted (highest holdout-control score; skipped disposal-group benign candidate) |
| 34 | atlas/hc_07.md | A3 FP | drafted (pair inversion vs WMK documented) |
| 35 | atlas/case_05.md | A3 TN-flagged | drafted (E2 any-snapshot rule; 5 breaching snapshots) |
| 36 | atlas/case_07.md | A3 TN-flagged | drafted (convertible-debt reclass under truncated windows) |
| 37 | atlas/case_11.md | A3 TN-flagged | drafted (E2 flag within recorded draw noise) |
| 38 | atlas/case_14.md | A3 TN-flagged | drafted (truncated-window re-read of resolved reserve declines) |
| 39 | atlas/PATTERNS.md | A4 | drafted [human_finalized=false] (wrong-reason TPs / genuine-figures FPs / input-visibility-floor misses) |
| 40 | docs/CONTROL_CRITERIA_v3.md | B1 | SKIPPED — already existed (d096ff6, this session); §4 roster corrected pre-run (1ce4cb8) |
| 41 | controls/retrospective_audit_v1.md | B2 | created — 62 controls; FAIL 8 rows (6 cos: NUVA·R·UPBD·LQDT·FLO (f) MTD-survived; GRDX (e) disagreement resignation; GO (d) unremediated MW); tiers A=35 B=12 prov=7; FPR untouched |
| 42 | controls/retrospective_audit_v1.json | B2 | created (machine verdicts + query log, audit date 2026-07-21) |
| 43 | docs/methodology_limitations.md | B2 | L-8 appended — published FPRs conditional on original v1/v1.1/v2 selection criteria |
| — | NOTE | B2 | Overlap finding: audit-FAIL controls GRDX/GO/NUVA/LQDT/R are also atlas FP/TN-flagged cases → label-noise angle queued for owner (no atlas/PATTERNS edit — drafted set frozen for owner review) |
| 44 | README.md | C1/C2/C4 | edited — "Three tasks, three evidence tiers" section + [TASK n] tags; 277→277 lines (flat); numbers unchanged; lint PASS |
| 45 | README.ko.md | C1/C2/C4 | edited — mirrored 태스크 분리 section + tags; 201→201 lines; lint PASS |
| 46 | tools/lint_publication.py | C3 | rule (L) added — results-language paragraph without task-tier token fails; governance phrase "task separation" exempt; frozen ISSUE drafts exempt (RP-15/16) |
| 47 | docs/reader_validation/ONE_PAGER.md | C2/C3 | 2 tier tags added ([TASK 1] Question / [TASK 3] GIL memo) to clear new rule L — OWNER: re-approve before reader dispatch (pre-dispatch surface, D92 queue) |
| — | NOTE | C2 | Frozen memo audit (report-only, no edits): ISSUE_0 7 untagged results-blocks — all single-cohort wave-1 statements, no cross-task pooling; ISSUE_1/2 0; GIL memo 1 spurious (disclaimer). Owner may add tags via signed diff; not required |
| 48 | CONTRIBUTIONS.md | D1 | created — 9-row AI/owner table, 1 [OWNER CONFIRM] (pre-GA-001 commit trailers), accountability model; linked from both README headers; 28 lines |
