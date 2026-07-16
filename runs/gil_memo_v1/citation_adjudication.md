# OUT-GIL-V1 — 인용 검증 판정 (1차: Claude 보조, 최종 확정: 인간 서명 대기)

- 대상: `runs/gil_memo_v1/flags_combined.json` (피평가자 최종 flag 5건, 인용 19건)
- 프로그램 판정 (`tools/blind_memo_verify.py`): **14/19 VERIFIED · 1 ALTERED · 4 NOT FOUND**
- 아래는 비-VERIFIED 5건에 대한 수기 판정. 모든 fragment는 `grep` 정확 일치로 원문 존재 확인 완료 (2026-07-15, 이 파일과 동일 커밋의 `data/gil/*.txt` 기준).

## 판정: 5건 전부 "원문 존재 — 생략(…) 병합 인용", 날조(hallucination) 0건

| # | 프로그램 판정 | 수기 판정 | 근거 |
|---|---|---|---|
| 1.4 | NOT FOUND (0.609) | 원문 존재 | 두 passage의 병합: 표 행 "Inventory fair value step-up cost recorded as part of the Hanes business acquisition(1) \| 106.3 \| —"(6-K MD&A L432, 원문은 행 끝에 "\| 106.3" 추가) + "The residual step up cost, of $95 million, is expected to turn over within approximately five months."(동 문서, 정확 일치) |
| 2.3 | NOT FOUND (0.740) | 원문 존재 | "primarily reflect expenses associated with the integration of Hanes", "$27.1 million for severance", "$14.5 million for the write-off of equipment" 전 fragment가 6-K ex99-2 Note 8 및 MD&A에 정확 일치. "…"로 중간 목록 생략 |
| 3.3 | ALTERED (0.846) | 원문 존재 | 6-K MD&A L872/874/875 세 표 행의 "…" 병합. 각 행("Adjusted EBITDA for the trailing twelve months (excluding discontinued operations) (1) \| 981.3 \| 926.3", "Business acquisitions(3) \| 472.0 \| 564.8", "Pro-forma adjusted EBITDA for the trailing twelve months \| 1,453.3 \| 1,491.1") 정확 일치 |
| 4.2 | NOT FOUND (0.781) | 원문 존재 | 6-K MD&A §6.1 단일 문장에서 중간절("compared to the end of fiscal 2025 mainly relating to the payout of annual rebate programs in the first quarter of fiscal 2026, and")을 "…"로 생략. 앞뒤 fragment 정확 일치 |
| 4.4 | NOT FOUND (0.792) | 원문 존재 | 6-K ex99-2 L684 "Accounts payable and accrued liabilities \| (211,526) \| (32,220)" — 피평가자가 "$ \|" 구분자를 삽입(추출 텍스트에 없음). 수치·계정명 정확 일치 |

## 추가 사실 검증 (memo에 실리는 주장)

- Flag 4 verification_path의 "$975M 계약 2026-06-16 만기" 주장: 원문 존재 — "The first agreement expires on June 16, 2026, subject to annual extensions" (6-K ex99-2 Note 5 L320; 40-F ex99-2 L2330 동일). **"subject to annual extensions" 단서를 memo에 반드시 병기.**
- 공정 병기 사항: 40-F ex99-2 Note는 매각 채권에 대해 "does not retain any credit risk with respect to any trade accounts receivables that have been sold"라고 명시 — 팩토링 flag 해석 시 신용위험 이전 사실을 누락하면 편향.

## 이 판단에서 알아야 할 것 (학습 노트)

스키마가 quote를 "단일 연속 passage"로 강제하지 않으면 모델은 "…" 병합 인용을 만들고, 문자열 검증기는 이를 NOT FOUND로 오판한다 — 검증기 v2는 "…" 분할 후 fragment 단위 대조가 필요하다 (이번 실행 기준은 사전 고정대로 유지, 결과 공개).

## 서명

- [x] 위 5건 수기 판정 및 memo 반영 승인 — 사용자: (owner, 2026-07-16,
  this session's structured decision responses — Q-O01, $201.6M 파생값
  assembly note 확인 포함, 원장 D93) 날짜: 2026-07-16
