# Earnings Quality Memo — Gildan Activewear Inc. (NYSE: GIL) · DRAFT (발행 전 인간 서명 필요)

**대상 공시**: [Form 40-F (FY2025, 2026-02-26 제출)](https://www.sec.gov/Archives/edgar/data/1061894/000106189426000006/gil-20251228.htm) — [감사 재무제표·주석 (Ex-99.2)](https://www.sec.gov/Archives/edgar/data/1061894/000106189426000006/gil-20251228_d2.htm) · [MD&A (Ex-99.1)](https://www.sec.gov/Archives/edgar/data/1061894/000106189426000006/exhibit991-mdax2025.htm) · [AIF (Ex-99.3)](https://www.sec.gov/Archives/edgar/data/1061894/000106189426000006/exhibit993-annualinformati.htm) / [Form 6-K (Q1 2026, 2026-04-30 제출)](https://www.sec.gov/Archives/edgar/data/1061894/000106189426000013/form6-kxinterimfilingq12026.htm) — [중간 재무제표 (Ex-99.2)](https://www.sec.gov/Archives/edgar/data/1061894/000106189426000013/exhibit992q12026fs.htm) · [중간 MD&A (Ex-99.1)](https://www.sec.gov/Archives/edgar/data/1061894/000106189426000013/exhibit991q12026mda.htm)

**방법**: LLM(claude-sonnet-5, 모델 고정)에 위 공시 원문 텍스트만 입력(뉴스·선정 사유·외부 정보 차단), 연차→분기 2단계 블라인드 프로토콜. 데이터 컷오프 2026-06-15(look-ahead 가드 코드 강제). 아래 모든 인용·수치는 결정론적 문자열 대조로 원문 추적 완료(정확 일치 14/19, "…" 병합 인용 5건 수기 확인 — `citation_adjudication.md`). 각 항목은 **사실**(공시 원문 발췌)과 **해석 가설**(모델의 미검증 가설)을 분리해 표기한다.

### 선정 배경 공개 (사후 선택 방어 — 이 메모가 주장하는 것과 주장하지 않는 것)

**사실**: GIL은 무작위로 선정되지 않았다. 선정 시점에 작성자는 Jehoshaphat Research의 공매도 리포트(2026-06-16 공개 — 매출 인식·결제조건 관련 **주장**이며, 회사는 부인)의 존재를 인지하고 있었다(`docs/FUTURE_HOLDOUT_CANDIDATES.md` 등재 케이스). 반면 **모델 입력 데이터는 컷오프 2026-06-15로 코드가 강제**되어(look-ahead 가드, 접근 로그 기록) 리포트 공개 이전에 제출된 공시만 사용되었고, 리포트 본문·뉴스·선정 사유는 입력에서 차단되었다.

**따라서 이 메모의 지위**: "무작위 스크리닝이 우연히 GIL을 집어냈다"가 **아니라**, "리포트 이전 공시만으로 같은 영역의 신호를 재구성할 수 있는가"에 대한 **봉인된 사전-리포트 복제(sealed pre-report replication)**다. 이 메모는 해당 리포트의 주장을 확인하지도 반박하지도 않는다 — 독자는 아래 5개 항목이 공개된 주장과 어디서 겹치고 어디서 다른지 원문 링크로 직접 대조할 수 있다.

**방법 신뢰 근거(부록)**: 이 방법이 백테스트에서 어떤 신호 유형으로 점수를 움직였는지의 기술 통계는 [`analysis/EVIDENCE_LINES.md`](../../analysis/EVIDENCE_LINES.md)에 있다 (신규 주장 없음 — 동결 산출물의 기술 전용 집계).

**접근 로그**: 컷오프 가드의 문서 접근 판정 로그 스냅샷 2026-07-16, sha256 `856d50f3984d` (해시 핀 — 원본 로그는 로컬 보존, Q-O01/Q-O03 서명 시 hash-only 규약).

---

### 1. Q1 2026: GAAP 순손실 전환 + 영업현금흐름 유출 확대 vs. 조정이익 흑자 유지 — 신뢰도: 높음

**사실**: Q1 2026 순손실 $(65.8)M(전년 동기 순이익 $84.7M), 계속영업 조정순이익 $80.0M(전년 $89.9M). 영업활동 현금흐름 $(279.5)M(전년 $(142.2)M). 조정 차이의 최대 항목은 Hanes 인수 재고 공정가치 step-up $106.3M이며, 잔여 $95M은 "expected to turn over within approximately five months" (6-K Ex-99.2 손익·현금흐름표; Ex-99.1 §5.5, §5.4.2).
**해석 가설**: GAAP·현금흐름과 조정지표의 괴리가 인수 후 확대. **검증 경로**: Q2·Q3에서 step-up 소멸 여부와 신규 조정 항목 추가 여부, 운전자본 유출($254.5M 스윙) 반복 여부 추적.

### 2. Hanes(매출의 약 45%)가 내부통제(ICFR)·공시통제(DC&P) 평가 범위에서 제외 — 신뢰도: 높음

**사실**: "we have limited the scope of our evaluation of internal controls over financial reporting (ICFR) to exclude controls over financial reporting of Hanes… also limited the scope of our evaluation of disclosure controls and procedures (DC&P)". Hanes 귀속분: 분기 순매출의 약 45%, 유동자산 $2,313M·비유동자산 $3,809M·유동부채 $986M·비유동부채 $1,703M (6-K Ex-99.1 §13.0). 신규 인수 기업에 대한 이런 제외는 규정상 허용되는 통상적 경과조치다.
**해석 가설**: 구조조정·PPA 조정이 집중되는 통합기에 연결재무제표의 절반 가까이가 통제 평가 밖에 있음. **검증 경로**: FY2026 연차보고서의 ICFR 평가에서 Hanes 편입 여부·중요한 취약점 식별 여부 확인.

### 3. 레버리지 지표 3종 병존: 헤드라인 3.3x vs 신용계약 기준 3.4x / USPP 기준 3.8x — 신뢰도: 높음

**사실**: 자체 정의 net debt leverage ratio 3.3x(FY2025말 3.0x). "for purposes of its term loans and revolving facility was 3.4x and for purposes of U.S. private placement notes was 3.8x". 산식의 pro-forma TTM 조정 EBITDA $1,453.3M 중 $472.0M(약 32%)이 Gildan 소유 이전 기간의 Hanes/HAA 실적 가산분. 자사주 매입은 2025-08부터 중단 (6-K Ex-99.1 §8.2).
**해석 가설**: 헤드라인 지표가 자사 차입계약 기준 대비 낮게 표시되며 격차가 분기 중 확대(0.4x→0.5x). **검증 경로**: 커버넌트 상한·여유폭 확인, pro-forma 가산분이 실제 실적으로 대체되는 향후 2~3개 분기 추이.

### 4. 부외 매출채권 팩토링 잔액 급변이 보고 현금흐름·채권 잔액을 좌우 — 신뢰도: 중간

**사실**: 부외 매각·관리 중 채권 $667.3M(FY말 $777.0M). 경영진은 채권 증가 요인으로 "lower sales of trade accounts receivables to financial institutions under receivables purchase agreements"를 명시. 은행 정산 시차 미지급금 $39.9M(FY말 $120.1M), 운전자본 내 매입채무 변동 $(211.5)M(전년 $(32.2)M). 최대 한도 $975M인 첫 번째 계약은 "expires on June 16, 2026, subject to annual extensions"이며, 회사는 매각 채권의 신용위험을 보유하지 않는다고 공시 (6-K Ex-99.2 Note 5·Note 10·Note 14(c); Ex-99.1 §6.1; 40-F Ex-99.2 Note 7).
**해석 가설**: 팩토링 물량의 재량적 변동이 보고 영업현금흐름·DSO에 유의한 영향 — FY2025에는 잔액이 $272.1M→$777.0M로 확대되며 반대 방향으로 작용. **검증 경로**: 2026-06 계약 갱신 결과, 분기별 팩토링 잔액-영업현금흐름 상관 추적.

### 5. 단일 고객이 총매출의 33.2%, 상위 10개 고객이 72.5% — 신뢰도: 중간

**사실**: "In fiscal 2025, our largest customer accounted for 33.2% of our total sales, and our top ten customers accounted for 72.5%". 고객 계약에 최소 구매 의무 없음. 2024-10 양대 도매 유통사 합병으로 결합 후 집중도 약 39%(FY2024 기준). Q1 2026 도매 채널 매출 $552M로 전년 $626M 대비 11.9% 감소, 사유는 "proactive inventory reduction across our combined customer channels" (40-F Ex-99.3 AIF; 6-K Ex-99.1 §5.4.1).
**해석 가설**: 단일 거래처 의존이 매출·채권 회수 변동성을 증폭(FY말 기준 해당 고객이 매출채권의 67%). **검증 경로**: 해당 유통사의 독립 신용 프로파일, 후속 분기 도매 매출·채권 연령 추이.

---

**한계·면책**: 본 결과는 Claude 기반 단일 파이프라인에 한정되며 다른 LLM·방법론으로 일반화할 수 없다. 채점: Claude 보조 + 인간 최종 확정. 위 "사실"은 공시 원문의 발췌이고 "해석 가설"은 검증되지 않은 가설이다. 본 메모는 회계기준 위반이나 부정행위를 주장하지 않으며, 모든 항목은 회사가 스스로 공시한 정보에 기반한다. 작성자는 GIL에 대한 보유·공매도 포지션이 없다. 본 자료는 교육·정보 목적이며 투자 자문이 아니다. 방법론·코드·검증 스크립트는 저장소에 공개되어 재현 가능하다.

**발행 승인**: [x] 사용자 서명 — (owner, 2026-07-16, this session's structured decision responses; Q-O01·Q-O03, $201.6M 파생값 노트 확인 포함, 원장 D93) 날짜 2026-07-16
