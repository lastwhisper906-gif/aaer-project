# Post-publication note (2026-07-20) — v1 perturbed frame is partially de-identified

> Dated disclosure under the owner plan of 2026-07-20 §1.3, ledger D99.
> Audit basis: `analysis/V1_PARTIAL_DEIDENTIFICATION_AUDIT.md` +
> `pipeline/test_deid_disclosure.py`. This note narrows interpretation only.

## English

**v1 remains frozen; no original result is recomputed.** A post-publication
audit (2026-07-20) confirmed that the v1 perturbed ("identity-masked") payload
removed company names, tickers, and explicit CIK fields and rescaled monetary
values, but **retained original SEC accession numbers** (globally unique EDGAR
document IDs whose prefixes encode the submitting filer's CIK and whose middle
segments encode the filing year) **and the exact real filing chronology**.

The interpretation of the perturbation arm is therefore narrowed:

- The perturbed frame should be described as **partially de-identified**, not
  fully identity-masked.
- In the v1 design, company recognition may have occurred through **accession
  metadata, filing chronology, financial structure, or memorized financial
  patterns** — these channels are not separable.
- The measured recognition rates (wave-1 name-ID 50%, wave-2 21.9%) **cannot
  be attributed solely to financial-pattern reconstruction**.

This limitation does not invalidate the published separation statistics; it
limits the causal interpretation of the v1 perturbation experiment. The
already-published caveats (README "not a clean lower bound"; limitation L-5)
pointed in this direction; this note adds the accession channel explicitly.
Prospectively, any payload described as identity-masked must pass the machine
definition in `pipeline/test_deid_disclosure.py::assert_fully_deidentified`
(no original accessions, CIK, company name, or ticker) — the v2 date-shift
design (`specs/perturb_v2.md` §3) already meets it.

## 한국어

**v1은 동결 유지 — 원 결과 재계산 없음.** 2026-07-20 사후 감사에서 v1 교란
페이로드가 회사명·티커·CIK를 제거하고 금액을 재척도했으나, **원본 SEC
accession 번호**(접두부 = 제출 filer CIK, 중간부 = 제출 연도를 인코딩하는
전역 고유 EDGAR 문서 ID)**와 실제 제출 연대기를 그대로 유지**했음을
확인했다.

- 교란 프레임은 **부분 탈익명화**로만 서술한다 (완전 정체 가림 아님).
- v1 설계에서 정체 인지는 accession 메타데이터·제출 연대기·재무 구조·암기된
  재무 패턴 어느 경로로든 일어날 수 있었고, 이 경로들은 분리 불가하다.
- 측정된 인지율(wave-1 50%, wave-2 21.9%)을 **재무 패턴 복원만의 결과로
  귀속할 수 없다**.

이 한계는 발행된 분리 통계를 무효화하지 않는다 — v1 교란 실험의 인과 해석
범위를 좁힌다. 향후 "identity-masked" 급 서술은
`pipeline/test_deid_disclosure.py`의 기계 정의를 통과해야 한다.

*본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).*
