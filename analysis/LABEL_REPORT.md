# LABEL_REPORT — 홀드아웃 Big R / little r 태깅 (specs/label_taxonomy.md 이행)

- 사전 등록: 스펙 커밋 `d60a6e0` (태깅 산출 선행). 기계 산출:
  `analysis/label_tags_holdout.json` (`analysis/label_tags_holdout.py`, 결정론·무네트워크).
- **동결 홀드아웃 스코어보드 무변경** — 본 문서는 라벨 정밀화의 병기 층이다.

## 1. 태그 결과 (증거 accession 전건)

| case | ticker | 태그 | 증거 (revelation ± 90d 내 4.02) | 캐시 스냅샷 커버 |
|---|---|---|---|---|
| case_71 | HUBG | **bigR** | `0001193125-26-039396` (2026-02-05, items `2.02,4.02,9.01`) | 2026-06-29 ≥ 2026-05-06 ✓ |
| case_72 | WMK | **bigR** | `0000105418-26-000009` (2026-02-20, items `4.02`) | 2026-06-04 ≥ 2026-05-21 ✓ |
| case_73 | GNE | **bigR** | `0001437749-26-007981` (2026-03-12, items `4.02,9.01`) | 2026-06-11 ≥ 2026-06-10 ✓ (1일 마진) |

neighborhood 밖 관측 (숨기지 않음): HUBG `0001193125-26-218141`
(2026-05-12, 두 번째 4.02 — revelation +96일, 이웃 밖); GNE
`0001213900-17-011231` (2017-11-02 — 과거 별건). 판정 불변.

**결과**: 홀드아웃 treatment 3/3 전건 **Big R** (Item 4.02 비신뢰 선언 동반) —
"restatement"라는 동일 단어 아래 가장 강한 하위 범주다. little_r 케이스 0.

## 2. 기저율 (재작성 ≠ 집행 — 분모 상이 주의)

- **~2.2%**: Audit Analytics 재작성 중 SEC 집행 연계 (Karpoff, Koester, Lee,
  Martin, *The Accounting Review* 2017).
- **~89.4%** fraud 무관 / **~26.4%** irregularity (Hennes, Leone, Miller 2008 —
  GAO 표본). **26.4%는 의도성 프록시이지 집행률이 아니다** — 2.2%와 직접
  비교 금지.
- Chu, Dechow, Hui, Wang (2018): "AAER 조사 대부분이 재작성 계기" 방향의 정성
  지지 — **정확 수치 인용은 소유자 원문 대조 후에만** (OWNER_QUEUE Q-F02,
  발행 사용 금지 유지).

시사점: Big R 3/3이어도 기저율상 다수 경로는 "집행 없음"이다 — G2 잠정
라벨의 노이즈는 알려진 양이며, 아래 프로토콜이 양방향 모두를 기록한다.

## 3. 업그레이드 프로토콜 (사전 등록 — 대칭)

- 모니터링 윈도 4년: HUBG → **2030-02-05** · WMK → **2030-02-20** · GNE →
  **2030-03-12** (월간 재조사 루틴 `tools/holdout_rescan.py` 경로).
- AAER 지명 → provisional→confirmed, 신규 D-엔트리, **병기만** (스코어보드 불변).
- 윈도 만료 무집행 → "no enforcement within window" 주석 — 그 자체가 라벨
  노이즈에 관한 보고 가능한 결과 (기저율상 다수 기대치).

## 4. 명명 diff

발행 표면 반영은 `review_packets/RP-15_label_naming_diff.md` (diff-only,
소유자 서명 게이트 Q-F03) — 직접 수정 0.

**학습 노트 (이 판단에서 알아야 할 것)**: Big R/little r은 심각도 순서가
아니라 **공시 절차의 구분**이다 — 비신뢰 선언(4.02)은 과거 재무제표를 쓰지
말라는 회사 자신의 판정일 뿐, 의도성(fraud)도 집행 가능성도 확정하지 않는다.

*본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).*
