# CONTRIBUTIONS.md — AI-vs-human contribution statement (standing)

> Authority: D106 ⑤ (`governance/FEEDBACK_RESPONSE_v1.md`, owner-signed
> 2026-07-20). Kept current with the workflow; last updated 2026-07-21.
> The value of this document is precision — where the honest answer is
> "mostly AI," it says so. Every row is verifiable against the cited repo
> evidence (decision signatures, `human_finalized` flags, the overrides
> ledger, commit trailers).

| Work | AI performed | Owner performed | Evidence |
|---|---|---|---|
| Code drafting (pipeline, scoring, analysis, tools) | **Effectively all** — drafted and revised in Claude Code sessions | Directed tasks; audited via review packets; approved merges | GA-001(b) headers; commit trailers; `review_packets/INDEX.md` [OWNER CONFIRM: pre-GA-001 commits lack trailers] |
| Architecture & design decisions | Proposed options with rationale and rejected alternatives | **Selected and signed** — every D-entry decision is owner authority | `scoring/decisions_log.md` D1–D106 (근거·기각 대안 per entry; owner-signed entries D90–D106) |
| Data extraction & cutoff verification | Performed all EDGAR collection and payload assembly | Supervised network runs; look-ahead guard is code-enforced, verified by gates | `pipeline/cutoff_guard.py` · `data/manifests/` · access logs (D93 hash pin) · Q-E03/D26 supervision precedent |
| Accounting judgments (grades, error attribution, atlas CPA sections) | **First-pass author** with mandatory cited evidence | **Full review and finalization** — all published grades `human_finalized=true`; 0 overrides recorded (rubber-stamp check confirmed); atlas §7–9 pending owner finalization | grade `_meta.human_finalized` (D24/D26) · `scoring/overrides.md` · `atlas/INDEX.md` status column |
| Research design & pre-registration | Drafted specs, probes, thresholds, experiment plans | **Selected and pre-registered** — freeze-commit-then-run signatures; contamination threshold (D7) and conclusion rules R/H fixed under owner authority before any score | `scoring/eval_spec.md` · `analysis/*_PLAN.md` (commit `c1b85a7`) · freeze records in `scoring/decisions_log.md` |
| Error analysis (FP/FN dissection, taxonomy) | Performed and documented | Audits per §7: "model judgment error" class reviewed in full, others sampled; atlas set pending | `analysis/error_analysis*.md` · `scoring/error_taxonomy.md` · PROJECT.md §7 서명 규칙 |
| Publication claims (README, issues, memos, briefs) | **Drafted all text** | **Responsible for scope, wording, and numbers** — publication only after owner sign-off; post-publication edits by owner-signed diff only | D40/D41 (issues) · D91 (RP-15/16 diffs) · D92/D93 (GIL memo) · `tools/lint_publication.py` (mechanical claim guards) |
| Governance sign-offs | Transcribes decisions; may not fabricate or imply human signature (D15) | **Sole authority** — every gate, freeze, ratification, and publication dispatch | `scoring/decisions_log.md` · `scoring/overrides.md` · signature blocks in `governance/`, `docs/FREEZE_REV*` |
| Grading execution | Grader model (claude-fable-5) applies the frozen rubric; same-family risk disclosed (L-6) | 100% human final sign-off on every published grade | README "Grading & finalization status" · L-6 · `specs/cross_grader.md` (planned mitigation) |

**Accountability model.** AI output in this repository is **unaudited work
product until owner sign-off**. Documents carry either "Authored by Claude
Code, pending human audit" (unaudited) or an owner signature with a ledger
D-entry (finalized) — never a fabricated human signature (D15). **The owner
bears final responsibility for all published claims.** 채점: Claude 보조 +
인간 최종 확정 (PROJECT.md §7). 본 결과는 Claude 기반 단일 파이프라인에
한정된다 (§5-5).
