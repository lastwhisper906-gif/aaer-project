# 장르 태그 — 실험군 8 + 워크드 예시 2 (Phase 1-4)

> Authored by Claude Code, pending human audit (GA-001 (b), D15).
> 태그 체계: **active**(거래·수치의 적극 조작 — 세부: revenue/cost/gains) /
> **omission-estimate**(추정·충당금·공시의 누락형 조작) / **mixed**(양쪽 실질 병존).
> 참조 매핑(소유자 지시문)을 1차 소스로 **검증**한 결과이며, 불일치 1건(ICON)은
> 아래에 명기. 인용은 명령문 원문(~/aaer-data 추출본) 또는 서명된 재검증 diff의
> 문단 pinpoint. 이 파일은 채점 쪽 정답 키의 일부 — 피평가자 노출 금지.

| ID | 티커 | 장르 태그 | 참조 매핑 | 일치 | 1차 소스 근거 (축어) |
|---|---|---|---|---|---|
| T07 | MON | **active(cost)** | active(cost) | ✓ | 리베이트 비용의 이연·오분류 — 원문 최초 행위 캐나다 프로그램 2009-04(¶37), 미국 통지 "late May 2009"(¶15, diff §A-2). scheme: "improperly deferred recognizing the related rebate costs (incl. via side agreements)" |
| T11 | OFIX | **active(revenue)** | active(revenue) | ✓ | 33-10281 Summary: "materially overstated its distributor revenue and operating income … entered into **contingent sales** … recognized revenue for product sales when the product could not be resold" |
| T12 | LOGI | **omission-estimate** | omission-estimate | ✓ | 34-77644: "fraudulently accounting for the **write-down** of a failed product [Revue] in FY11" + "accounting for the Company's **warranty liabilities** in the FY12 and FY13 financial statements, and … failure to correct … known error" — 추정(LCM·워런티) 시점 조작 |
| T13 | HTZ | **omission-estimate** | omission-estimate | ✓ | 33-10601: "Part of the misstated income resulted from errors made in various accounts that are **subject to management estimate** … allowance related expenses were understated … relied on inappropriate estimation" + 렌터카 보유기간 연장으로 감가 축소 |
| T16 | ICON | **mixed (active(gains) 우세)** | active(gains) | **부분 불일치** | 적극 축: JV buy-in 과지급의 수익/이익 인식 (소장 ¶45, ¶58-59 — diff §A-2). 누락 축: "failed to timely recognize $239M+ of brand **impairment**" (LR-24682) — 손상 미인식은 omission-estimate 실질. 태그는 mixed, 채점 분해 시 active(gains) 우세로 취급 |
| T17 | MRVL | **active(revenue)** | active(revenue) | ✓ | 34-77076: 미공시 'pull-in' — 미래 분기 예정 매출의 당기 가속 (Relevant Period 2015-01~07 ¶2; 규모 ¶12/¶18). 실제 판매의 시점 조작이므로 revenue 축의 적극 조작 + 공시 누락 병존 |
| T21 | SCOR | **active(revenue)** | active(revenue) | ✓ | 33-10692 ¶1: "materially overstated revenue by approximately $50 million"; ¶2 비화폐 데이터 교환 $34.5M + ¶3 연계 계약 ~$12M |
| T28 | KHC | **active(cost)** | active(cost) | ✓ | 33-10977 ¶1: "multi-year **expense management** scheme by KHC's procurement division to improperly reduce KHC's **cost of goods sold**" — Prebate/clawback/price-phasing로 미실현 공급자 할인 조기 인식 |
| T18 | VRX | **active(revenue)** (파일럿) | — | — | 33-10809 ¶15: Q3 2014~Q3 2015 오도 보고 창 — 미공시 전속 약국(Philidor) 경유 매출 인식 + 비GAAP 유기 성장 홍보. 공시 누락 축 병존하나 매출 인식 실질 우세 |
| T25 | GE | **omission-estimate** (파일럿) | — | — | 33-10899: 보험 준비금(LTC) 추정 악화의 미공시(Summary/¶36 창) + Power 이익의 원가 추정 변경 기여 미공시(¶15). 거래 날조 없음 — 추정·공시 누락 전형 |

## 학습 노트 (§10)

장르 태그는 "무엇을 조작했나"가 아니라 **"조작이 공개 데이터에 어떤 종류의 흔적을
남기는가"**의 분류다 — active(revenue)는 AR/DSO 발자국(F1), active(cost)는 마진
발자국(F4/F6)을 남기지만, omission-estimate는 '있어야 했던 숫자의 부재'라서 비율
지표가 원리적으로 잡기 어렵다. 이 비대칭이 Phase 3 분석 ⑥의 사전 가설이다.

본 태그는 Claude 기반 단일 파이프라인에 한정된 채점 인프라이며(§5-5),
ICON의 참조 매핑 불일치 처리는 인간 감사 대상 재량 판단이다 (Review Packet 색인 기재).
