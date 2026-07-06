# 오염 프로브 설계 — v1 (Phase 2-3, 실행은 Phase 3)

> Authored by Claude Code, pending human audit (GA-001 (b), D15).
> **These controls BOUND memorization risk; they do not eliminate it.**
> (전 프로브 결과 문서에 이 헤더 의무 — 소유자 지시.)
> 실행 대상 모델 = 피평가자 핀(`claude-sonnet-5`). freeze 후 설정 변경은 이력 공개.

## ① 인지 프로브 (recognition) — D7 분기 입력

- **입력**: 실험군 8건의 **교란 변형 페이로드** (② 규칙 적용: 사명·티커·CIK 익명화
  + 상수배 재스케일. 날짜 원본 유지 — D8).
- **질문(케이스별 독립 호출)**: "Based on the structured filing data above, which
  specific company is this? Answer with the company's real name, or 'unknown'."
  출력 스키마: `{company_guess: string, confidence: high|medium|low}`.
- **판정(기계)**: company_guess가 실제 회사(당시 사명 또는 통용 사명)와 일치 = 인지 1건.
  대소문자·법인 접미사 무시. 판정 근거로 guess 원문 보존.
- **분기 (D7, 사전 등록 — decisions_log 커밋 `9f0fb42`)**: 인지 ≥3/8 →
  CONTAMINATED: 본 분석 = 교란 실행 전용, 원본 결과는 부록 상한, 전 보고서
  헤드라인에 오염 명시. <3 → 본 분석 = 원본 실행, 교란 delta = 암기 기여 추정.

## ② 교란 집합 (perturbation) — D8

- **규칙 (기계, 케이스별 결정론)**:
  1. `company_name` → `Company {case_id 대문자}` / `ticker` → `XXX{순번}` /
     `cik` → 제공하지 않음 (교란 변형에서는 파이프라인이 사전 수집분을 사용).
  2. 모든 화폐 금액(XBRL USD 값) × 상수 k — k는 케이스별 고정: 시드
     `sha256(case_id + "perturb-v1")`의 첫 4바이트를 [0.4, 2.5] 로그균등 구간에
     사상. 비율·추세 보존(스크린·분석 불변), 절대 규모만 변경.
  3. 날짜(기간·제출일) 원본 유지 — D8 소유자 결정 (내용 기반 재식별은 어차피
     잔존; 교란은 암기 기여의 **측정** 장치이지 제거 장치가 아님 — 결과 문서 의무 문구).
  4. 주식수·비화폐 단위는 무변환 (비율 왜곡 방지: EPS류 파생값은 페이로드에서 제외).
- **용도**: 실험군 8건 교란 실행 (D5: 변형당 1회) → 원본−교란 delta = 암기 기여
  추정치 (분석 ④). D7 분기 시 본 분석 데이터.

## ③ 축어 회상 프로브 (verbatim recall)

- **입력**: 원본 케이스 필드 5개만 (재무 데이터 없이).
- **질문**: "Without any documents: state {company_name}'s exact reported total
  revenue and net income for the fiscal year ending immediately before
  {cutoff_date}, and the filing date of that annual report. If you do not know,
  say 'unknown'." 스키마: `{revenue, net_income, filing_date, known: bool}`.
- **판정(기계)**: 실제 point-in-time 값 대비 ±2% 이내 = 회상 성공. 결과는
  케이스별 잔여 위험 등급 입력.
- **케이스별 잔여 위험 등급 (3-2에서 부여)**: HIGH = 인지 성공 ∧ 회상 성공 /
  MED = 둘 중 하나 / LOW = 둘 다 실패. 등급은 분석 ①의 케이스 노트에 병기.

## ④ 카나리 GUID (D9 — 최저 우선순위, 미래 학습 유입 감지)

- 정답 키 카나리 (scoring/ 내부 문서 전용): `9FA11F98-6380-4BF5-AB3C-8542459ACA6F`
- 내부 문서 카나리 (docs/ 방법론 문서 전용): `A2D69CFE-CA8A-4DE1-8393-5B225099299B`
- 용도: 차기 사이클에서 신모델에 "이 GUID를 아는가" 프로브 → 본 저장소의 학습
  데이터 유입 감지. 이 GUID들은 피평가자 페이로드에 절대 포함하지 않는다
  (포함되는 순간 카나리가 아니라 누출이 됨).

## 실행 순서 (Phase 3-2)

인지 프로브 → D7 분기 결정 문서화 → 축어 프로브 → 잔여 위험 등급표 →
(파일럿·본 실행은 그 후). 프로브 출력은 `scoring/probe_results/`에 격리 —
본 실험 디렉토리 혼입 금지.
