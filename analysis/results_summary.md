# results_summary — RP-10 Phase 2 (기계 생성, 계획 사전 커밋본 준수)

## primary: original(8) vs original(22)
- fraud 8 vs control 22 · 평균차 19.83pp · 중위 57.5 vs 33.0
- 순열 p(단측) = **0.00114** · Fisher p = 0.003145 (플래그 p≥50: TP 6/8, FP 3/22)
- Cliff's δ = 0.648 · AUC = 0.8239 (부트스트랩 95% [0.599, 0.983] — UNSTABLE at N=30 — 점 플롯이 1차 시각화)
- FPR: {'fp': 3, 'n': 22, 'rule': 'Clopper-Pearson 95%', 'lo_pct': 2.9, 'upper95_pct': 34.9}

## secondary: perturbed-fraud vs original-control (J14)
- fraud 8 vs control 22 · 평균차 15.08pp · 중위 50.0 vs 33.0
- 순열 p(단측) = **0.00207** · Fisher p = 0.059613 (플래그 p≥50: TP 4/8, FP 3/22)
- Cliff's δ = 0.727 · AUC = 0.8636 (부트스트랩 95% [0.722, 0.969] — UNSTABLE at N=30 — 점 플롯이 1차 시각화)
- FPR: {'fp': 3, 'n': 22, 'rule': 'Clopper-Pearson 95%', 'lo_pct': 2.9, 'upper95_pct': 34.9}

## 기준선 (동일 30사 PIT)
- **beneish_m** (계산가능 22/30): 자체 분리 p=0.498245, AUC=0.5104 · Spearman ρ(LLM)=-0.075 · R2 잔차 p=0.00529 → R2 발동=False
- **dechow_f** (계산가능 22/30): 자체 분리 p=0.267897, AUC=0.5729 · Spearman ρ(LLM)=-0.144 · R2 잔차 p=0.00097 → R2 발동=False

## R3 암기 분해: 5/8 케이스 산입 (발동 임계 ≥5)

## 결론 규칙 발동: **R3** (프레임별: primary=R3, secondary=R3)
