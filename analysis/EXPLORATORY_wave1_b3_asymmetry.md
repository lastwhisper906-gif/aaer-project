# EXPLORATORY — wave-1 B3 귀속비 비대칭의 산술 분해 (D53)

> **EXPLORATORY / 발행 승인됨 (RP-18, owner 2026-07-16 — 배치 A: Issue #2
> 부록 코멘트, 게시 텍스트는 `review_packets/RP-18_body.md` 한정).** 게시
> 전까지 이 원본 메모 자체는 발행 표면이 아니다. 게시 후 URL은 D-엔트리로
> 기록한다. (원 표식 NOT-FOR-PUBLICATION은 RP-18 §2 게시 텍스트로만 대체
> 발행 — 본 메모 전문 게시 불가 원칙 유지.) 원인 서술은 사전 등록 문장 밖이며
> (specs/B3_metasignal.md §7 판독 노트), **아래의 어떤 문장도 인과 주장이 아니다** —
> 커밋된 산출물(`analysis/results_b3.json`)의 산술 재배열과, 질문형으로만 적은
> 가설 후보다. 공개 여부·형태는 전적으로 소유자 결정.

## 0. 비대칭의 동결값 (재계산 없음 — results_b3.json 인용)

| tier (W8) | B3 AUC | 동결 LLM AUC | 귀속비 (AUC−0.5)/(LLM−0.5) |
|---|---|---|---|
| wave-1 (8v22) | 0.7898 | 0.8239 | **0.8947** |
| wave-2 (9v23) | 0.5483 | 0.829 | **0.1468** (판정 tier, `non_trivial`) |

## 1. 지표 유병률 분해 (W8, per_case 산술 집계 — 이 표가 이 메모의 전부)

분자 = 지표 점화 케이스 수. 출처: `results_b3.json` `tiers.*.per_case.*.W8.indicators`
(집계 스크립트는 아래 §3 재현 명령 — 어떤 동결 파일도 수정하지 않음).

| 지표 | w1 실험군 (n=8) | w1 대조군 (n=22) | w2 실험군 (n=9) | w2 대조군 (n=23) |
|---|---|---|---|---|
| b_nt (NT 10-K/Q) | 1/8 | 1/22 | 2/9 | 1/23 |
| b_ka (10-K/A) | **4/8** | 2/22 | 1/9 | **6/23** |
| b_qa (10-Q/A) | 2/8 | 2/22 | 1/9 | 1/23 |
| b_401 (감사인 교체) | 0/8 | 1/22 | 1/9 | 0/23 |
| b_402 (비신뢰) | 1/8 | 0/22 | 0/9 | 0/23 |
| b_8kfreq (8-K 빈도) | 2/8 | 1/22 | 0/9 | 1/23 |
| **점수 분포 (정렬)** | 0,0,1,1,2,2,2,2 | 0×17, 1×4, 3 | 0×5, 1×3, 2 | 0×14, 1×9 |

산술 사실 (서술 아님, 표의 재진술):

- wave-1 분리의 최대 단일 기여는 **b_ka** (실험군 50% vs 대조군 9.1%). b_qa·
  b_8kfreq·b_nt·b_402가 각각 실험군 쪽으로 소폭 가산 — 실험군 8사 중 6사가
  점수 ≥1, 대조군 22사 중 17사가 0.
- wave-2에서는 **같은 b_ka가 방향이 뒤집힌다**: 실험군 11.1% vs 대조군 26.1%.
  실험군 9사 중 5사가 전 지표 0 — 어떤 지표도 실험군 쪽 우세가 2/9를 넘지 않는다.

## 2. 가설 후보 (전부 질문형 — 채택·기각·검정 계획 없음)

1. wave-1 실험군(유명 프라우드)의 10-K/A 유병률이 높은 것은 **폭로 전 정정
   문화·감독 강도가 시대(2000s)와 규모에 결합**한 표집 특성인가, 아니면 사기
   진행 자체의 흔적인가?
2. wave-2 대조군의 10-K/A 26.1%는 **대조군 매칭 풀(현 시점 SIC browse)의 생존
   특성**과 관련이 있는가 (Q-F08 감사와 겹치는 질문)?
3. wave-1의 LLM AUC(0.8239)와 B3 AUC(0.7898)가 근접한 것은 **LLM이 같은 연대기
   신호를 읽었기 때문**인가, **다른 신호로 같은 순위에 도달**한 것인가? (E4/E2
   계열 데이터 없이는 구분 불능 — 여기서는 질문으로만 둔다.)
4. 컷오프 시대 차 (wave-1 2000s 후반~2010s 초 vs wave-2 2010s) 가 8-K/정정
   제출 관행의 기저율 차로 이어져 지표 유병률에 반영된 것인가?

## 3. 재현 (결정론 — 동결 파일 무수정)

```bash
.venv/bin/python - << 'PY'
import json, csv
d = json.load(open('analysis/results_b3.json'))
w1 = {r['case_id']: 'treatment' if r['group']=='fraud' else 'control'
      for r in csv.DictReader(open('analysis/baseline_table.csv'))}
w2 = {c['case_id']: c['group'] for c in
      json.load(open('data/candidates/candidates_wave2.json'))['candidates']}
for tier, gmap in (('wave1', w1), ('wave2', w2)):
    pc = d['tiers'][tier]['per_case']
    for grp in ('treatment', 'control'):
        ids = [c for c in pc if gmap.get(c) == grp]
        print(tier, grp, len(ids),
              {i: sum(pc[c]['W8']['indicators'][i] for c in ids)
               for i in ['b_nt','b_ka','b_qa','b_401','b_402','b_8kfreq']})
PY
```

- 본 결과는 Claude 기반 단일 파이프라인에 한정 (§5-5). N=8/9 소표본 —
  유병률 차이의 어떤 것도 단독으로는 통계적 주장이 아니다.
