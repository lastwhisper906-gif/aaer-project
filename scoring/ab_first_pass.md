# A/B 기준 1차 적용 표 (킬 스위치 판정 재료) — Claude 1차, 판정 확정은 인간

> 작성: 채점 보조 Claude 2026-07-05 (유도 서명 세션 직후). 적용 기준:
> `scoring/ab_criteria_draft.md` **v1 SIGNED** (G1 = 연차≥2 AND 총≥6, 40-F 포함).
> 규칙: G1/G2 no → B형; F/T ≥1 AND D 무 → A형; D 유 → B형(단 F/T ≥2 → borderline).
> G1은 결정론 계산(edgar_verification.json + 서명된 규약: 운영기 제외 T03/T05,
> 다중 CIK 합산 T04/T13). F/T/D는 scheme_summary(원문 대조 완료분) 인용 기반 1차.
> **A형 집계와 GO/STOP 선언은 본인 전속 (PROJECT.md §4·§7).**

## 결과 요약 (1차)

| 판정 | 건수 | 케이스 |
|---|---|---|
| **A형** | **23** | T02 T04 T06 T07 T08 T10 T11 T12 T13 T14 T16 T17 T18 T19 T20 T21 T22 T23 T24 T25 T26 T28 T29 |
| **B형** | 5 | T03 T05 T15 T27 T30 |
| **borderline** | 2 | T01 T09 |

킬 스위치 문턱: **A형 ≥8 GO / 5~7 스코프 축소 / <5 STOP** → 1차 집계 23은 GO 문턱의
약 3배. borderline 2건을 B로 쳐도, A형 중 판단 여지가 있는 3~4건(T18/T20/T25 특성 주석
참조)을 전부 빼도 문턱 위.

## 케이스별 판정 추적

| ID | G1(연차/총) | G2 | F/T (근거 요지 — scheme 원문 기반) | D | 1차 |
|---|---|---|---|---|---|
| T01 RINO | y(3/11) | y | F1 가공 판매계약·매출 15배("false sales contracts… ~$491M vs ~$31M"), F3 | **D1: 이중장부**("two conflicting sets of books") — D1 예시 그대로. F≥2라 규칙상 borderline | **BL** |
| T02 CSC | y(17/66) | y (FY09-10 연차 반영) | F3 P-o-C 이익 과대, F5 "cookie jar reserves", F2 "capitalized 'prepaid' costs" | 무 | **A** |
| T03 CCME | **n** (운영기 4<6, 서명 규약) | — | — | — | **B** |
| T04 WFT | y(3/34 — 전신 CIK 포함, diff §B-1) | y | F2/F3 유령 세금채권("phantom ~$461M income-tax receivable"), F5 ETR 가이던스 정합 | 무 | **A** |
| T05 KEYP | **n** (운영기 3<6 — 임계 의존 인지 서명분) | — | — | — | **B** |
| T06 PUDA | y(4/16) | y | T1 관련당사자: 자회사 90% 지분 비밀 이전 후 "SEC filings… still told US investors Puda owned 90%" — 공시 텍스트 채널. 위조 CITIC 서한은 감사위·SEC 대상 은폐 = D1 아님(서명 문언) | 무 | **A** |
| T07 MON | y(11/43) | y | F3 리베이트 비용 이연, F4/F6 "overstating… Roundup gross profit" | 무 | **A** |
| T08 MILL | y(3/16) | y | F2 자산 과대($2.25M 취득→$480M 계상), F3 "$277M bargain-purchase gain" | 무 | **A** |
| T09 FEED | y(4/15) | y | F1 가공 매출("~$239M fictitious… fake feed invoices"), F2 고정자산 과대 | **D1: 이중장부**("two sets of books"). F≥2 → borderline | **BL** |
| T10 DMND | y(7/25) | y | F4 원가 과소(walnut costs), F3 미지급 과소, F5 "beat analyst estimates" | 무 | **A** |
| T11 OFIX | y(11/42) | y | F1 반품가능·조건부 유통사 매출 인식 | 무 | **A** |
| T12 LOGI | y(6/21 — 신폭로일 기준 재계산) | y (조작 2008-04~2013-03 전체가 컷오프 전) | F4 재고 평가손 지연("~$30.7M… Revue inventory"), F5 가이던스 부합, F3 | 무 | **A** |
| T13 HTZ | y(8/29) | y | F5/F3 충당금·비용 시점 조작, F2 감가상각 조작(fleet 보유기간 연장) | 무 | **A** |
| T14 PWE | y(연차 8 = 40-F, 서명 구성) | y (FY12-13 40-F 반영) | F2 명시적: "reclassified… operating expenses as capital expenditures" | 무 | **A** (G3 no — 수기 추출 비용 플래그) |
| T15 RATE | y(3/13) | **n?** — 기록 조작창 2012-04~06 = 보고기간 1개(<2). 쿠션 계정 "since at least early 2011"(¶24)을 창에 포함하면 y | (D2도 촉발: ~$0.8M — 문언 예시보다 작은 규모) | **B** (G2 협의 해석. 광의 해석 시에도 D2로 B 방향) |
| T16 ICON | y(18/73) | y | F1 가공 라이선스 매출, F2 손상 미인식($239M+), T1 부실 라이선시 지원 거래 | 무 | **A** |
| T17 MRVL | y(15/60) | y (Relevant Period 2015-01~07, FY15 10-K·Q1 10-Q 반영) | F1 pull-in→분기말 AR 왜곡, F5 "close the gap to publicly issued revenue guidance" | 무 (규모 $88M — D2 아님) | **A** |
| T18 VRX | y(19/36 국내폼) | y (Q3'14~Q2'15 보고 반영) | F1 Philidor 채널 매출, F5 "touted… organic growth for five consecutive quarters"(¶15a) | 무. 주석: 관계 자체는 미공시라 T1은 no — 수치 채널이 주 경로 | **A** |
| T19 OSIR | y(9/37) | y | F1 "inflated prices… consignment… backdating"→AR/DSO. 백데이팅은 감사인 대상 은폐(D1 아님) | D2 검토: 정정 $1.8/1.0/1.1M — SEC가 중대성 주장·정정 실시로 1차 no | **A** (D2 판단 주석 + GP-7 근거 등급 주의문 대상) |
| T20 BRX | y(2/9) | y | F5 스무딩: "'cookie jar' ledger account('2617')"로 SP NOI 성장률 정합 | 무 | **A** (비GAAP 지표 사건 — GAAP 왜곡 아님 주석) |
| T21 SCOR | y(8/34) | y | F3 비화폐 매출(현금 무유입 ~$34.5M), F5 "beat consensus… seven straight quarters" | 무 | **A** |
| T22 TNGO | y(4/18) | y | F1 미수행 용역·회수불능 매출, F3. 기록 위조는 감사인 대상 | 무 | **A** |
| T23 HAIN | y(19/79) | y | F1 분기말 pull-forward→유통사 AR/재고, F5 내부 분기 목표 | 무 | **A** (무정정·비사기 조항 비전형 주석) |
| T24 CGI | y(21/84) | y (FY16 10-K + Q1-2 FY17 반영) | F2/F3 손상 회피("avoided… ~$20M impairment… 2-3x fair value 거래") | 무 | **A** |
| T25 GE | y(24/94) | y | F3 이익의 질: 비용추정 감소가 Power 이익 성장의 1/4~1/2 + 내부 채권매각이 산업부문 현금회수 $2.5B — 발생액·OCF 괴리 채널 | 무 | **A** (무정정·공시 사건 주석) |
| T26 MDXG | y(9/35 — 신폭로일 기준) | y (2013~2016 보고 반영) | F1 "channel-stuffing… side arrangements with five distributors"→DSO | 무 | **A** |
| T27 WAGE | y(5/22) | y | F1 미실현 매출 $3.6M | **D2: "$3.6M 단일 계약"** — D2 문언의 예시 수치 그대로. F/T 1개뿐 → B | **B** |
| T28 KHC | y(3/14) | y | F4/F6 COGS 과소(리베이트 선인식), F3 발생액, 허위 공급계약 유지 | 무 | **A** |
| T29 UAA | y(14/55) | y | F1 "pull forward ~$408M… six consecutive quarters"→DSO, F5 애널리스트 추정 부합 | 무 | **A** (fn.2: GAAP 위반 주장 없음 주석) |
| T30 LK | **n** (연차 0 — 서명 구성 요건 직격) | — | — | (참고: D1 성격도 강함 — 가짜 운영 DB·은행기록 변조) | **B** |

## 판정 노트 (인간 확정 시 주의)

1. **borderline 2건(T01/T09)**: 둘 다 '이중장부' D1 + F 신호 2개 이상 → 규칙이 의도적으로
   인간에게 넘긴 구간. A로 뒤집으려면 "이중장부라도 미국 공시 수치에 비율 이상이 남았다"는
   근거(T01: AR 15배 매출의 회수 불능 흔적)를 오버라이드로 기록할 것.
2. **T15 RATE**: G2의 '조작 기간' 협의(기록창 1분기) vs 광의(쿠션 계정 2011~) — 협의 채택
   시 B. 어느 쪽이든 D2(~$0.8M)가 독립적으로 B 방향.
3. **A형 중 특성 주석 3건**(T20 비GAAP / T25 공시 사건·무정정 / T29 무GAAP위반) — A형
   유지해도 채점 시 '탐지 대상 신호'의 정의가 다른 케이스임을 도시에에 명기 필요.
4. **T04 전신 CIK 수집 공백**: G1 판정은 서명된 diff §B-1(34분기, 다중 CIK)을 근거로
   했으나 전신 CIK 0001170565의 submissions JSON이 현재 ~/aaer-data에 없음 —
   fetch_primary_sources.py EXTRA_CIKS에 T04 추가 + 재수집 + 매니페스트 재생성 필요 (후속).
5. **학습 노트(§10)**: A형 23/30이라는 1차 분포 자체가 정보다 — 기준이 후하게 설계됐을
   가능성(F 채널의 낮은 문턱)과, AAER에 오를 정도의 사건은 애초에 재무제표 발자국이 큰
   선택 편향, 두 해석이 공존한다. Week 3 오류 귀속에서 이 표의 F/T 예측이 실제 파이프라인
   적중과 얼마나 갈리는지가 trust boundary의 핵심 데이터가 된다.

본 결과는 Claude 기반 단일 파이프라인에 한정되며(§5-5), 이 표는 1차 자료일 뿐 킬 스위치
GO/STOP 선언은 본인 확정 사항이다.
