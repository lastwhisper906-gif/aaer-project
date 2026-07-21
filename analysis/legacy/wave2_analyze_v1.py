# FROZEN v1 implementation (produced the committed analysis/wave2_results.json).
# Kept for the record per ERRATA E-001; do not modify.
# Superseded by the rev2 path.
"""Wave-2 analysis per ANALYSIS_PLAN_WAVE2 — standalone primary + pooled secondary.
Writes analysis/wave2_results.json + analysis/wave2_summary.md. Deterministic (seed 20260707).
Run AFTER pipeline completes (uses scores, perturbed, grades, probes, baselines)."""
import json, glob, random, math, sys, statistics as st
from pathlib import Path
sys.path.insert(0, 'scoring/baselines')
from screens import run_case
REPO = Path('.')
SEED = 20260707

def load_scores(d, mapping):
    m = json.load(open(mapping))['mapping']
    out = {}
    for f in glob.glob(f'{d}/*.json'):
        j = json.load(open(f)); out[m[j['case_id']]] = j['misstatement_probability']
    return out

# wave-2 labels
w2c = {c['case_id']: c for c in json.load(open('data/candidates/candidates_wave2.json'))['candidates']}
sc2 = load_scores('runs/wave2/scores', 'scoring/id_mapping_wave2.json')
pt2 = load_scores('runs/wave2/perturbed', 'scoring/id_mapping_wave2.json')
fr = {s: p for s, p in sc2.items() if w2c[s]['group'] == 'treatment'}
co = {s: p for s, p in sc2.items() if w2c[s]['group'] == 'control'}
frv, cov = list(fr.values()), list(co.values())

def perm(a, b, seed=SEED, N=100000):
    obs = st.mean(a) - st.mean(b); pool = a + b; n = len(a); rng = random.Random(seed); ge = 0
    for _ in range(N):
        rng.shuffle(pool)
        if st.mean(pool[:n]) - st.mean(pool[n:]) >= obs - 1e-9: ge += 1
    return obs, (ge + 1) / (N + 1)
def cliff(a, b):
    g = sum(x > y for x in a for y in b); l = sum(x < y for x in a for y in b)
    return (g - l) / (len(a) * len(b))
def auc(a, b):
    return sum((1 if x > y else .5 if x == y else 0) for x in a for y in b) / (len(a) * len(b))
def boot_auc_ci(a, b, seed=SEED, N=10000):
    rng = random.Random(seed); vals = []
    for _ in range(N):
        ra = [rng.choice(a) for _ in a]; rb = [rng.choice(b) for _ in b]; vals.append(auc(ra, rb))
    vals.sort(); return vals[int(.025 * N)], vals[int(.975 * N)]
def spearman(a, b):
    def rank(x):
        idx = sorted(range(len(x)), key=lambda i: x[i]); r = [0] * len(x)
        for pos, i in enumerate(idx): r[i] = pos
        return r
    ra, rb = rank(a), rank(b); n = len(a); ma, mb = st.mean(ra), st.mean(rb)
    num = sum((ra[i]-ma)*(rb[i]-mb) for i in range(n))
    den = (sum((x-ma)**2 for x in ra)*sum((x-mb)**2 for x in rb))**.5
    return num/den if den else 0.0

R = {}
obs, p = perm(frv, cov); R['original'] = {'mean_diff': round(obs, 2), 'perm_p': p,
    'cliff': round(cliff(frv, cov), 3), 'auc': round(auc(frv, cov), 3),
    'auc_ci': [round(x, 3) for x in boot_auc_ci(frv, cov)],
    'fraud_mean': round(st.mean(frv), 1), 'control_mean': round(st.mean(cov), 1),
    'fraud_median': st.median(frv), 'control_median': st.median(cov),
    'fraud_scores': sorted(frv), 'control_scores': sorted(cov)}
if len(pt2) >= len(fr):
    ptv = [pt2[s] for s in fr if s in pt2]
    obs2, p2 = perm(ptv, cov); R['perturbed'] = {'mean_diff': round(obs2, 2), 'perm_p': p2,
        'auc': round(auc(ptv, cov), 3)}
# Fisher flags p>=50
ff = sum(x >= 50 for x in frv); cf = sum(x >= 50 for x in cov)
R['flags'] = {'fraud': f'{ff}/{len(frv)}', 'control_fp': f'{cf}/{len(cov)}',
    'fpr_pct': round(100*cf/len(cov), 1)}

# baselines M/F + R2
firms = [dict(json.load(open('data/candidates/candidates.json'))['candidates'][0], _x=1)]  # placeholder replaced below
cand = {c['case_id']: c for c in json.load(open('data/candidates/candidates.json'))['candidates']}
firms = [dict(cand[t], group='fraud') for t in ['T02','T04','T19','T20','T22','T23','T24','T26','T29']]
firms += [dict(c, group='control') for c in w2c.values() if c['group'] == 'control']
pm, pf = [], []
for c in firms:
    L = sc2.get(c['case_id'])
    if L is None: continue
    try: r = run_case(c)
    except Exception: continue
    m = r.get('beneish', {}).get('m_score'); f = r.get('dechow_f', {}).get('f_score')
    if m is not None: pm.append((L, m))
    if f is not None: pf.append((L, f))
rho_m = spearman([x[0] for x in pm], [x[1] for x in pm]) if pm else None
rho_f = spearman([x[0] for x in pf], [x[1] for x in pf]) if pf else None
R['baselines'] = {'rho_llm_m': round(rho_m, 3) if rho_m is not None else None,
    'rho_llm_f': round(rho_f, 3) if rho_f is not None else None,
    'm_computable': len(pm), 'f_computable': len(pf)}

# R3 memorization
cmed = st.median(cov); cross = []
for s in fr:
    if s in pt2:
        delta = fr[s] - pt2[s]; contrib = 0.5 * (fr[s] - cmed)
        if abs(delta) >= contrib or contrib <= 0: cross.append(s)
R['R3_memorization'] = {'crossed': len(cross), 'n': len(fr), 'cases': cross,
    'fires': len(cross) >= math.ceil(len(fr)/2 + 0.5) if len(fr)%2 else len(cross) > len(fr)/2}
# majority = >=5 of 9
R['R3_memorization']['fires'] = len(cross) >= 5

# R-rule determination (standalone)
r1 = R['original']['perm_p'] >= 0.05
r2 = (rho_m is not None and abs(rho_m) >= 0.7) or (rho_f is not None and abs(rho_f) >= 0.7)
r3 = R['R3_memorization']['fires']
fired = 'R1' if r1 else ('R3' if r3 else ('R2' if r2 else 'R4'))
R['conclusion_rule_standalone'] = {'R1_null': r1, 'R2_baseline': r2, 'R3_memorization': r3,
    'fired': fired}

# pooled secondary (wave1 8v22 + wave2 9v23) — frozen wave-1 scores reused, not re-scored
m1 = json.load(open('scoring/id_mapping.json'))['mapping']
w1fr = [json.load(open(p))['misstatement_probability'] for p in glob.glob('runs/main/case_*.json')
        if m1[json.load(open(p))['case_id']] in ['T07','T11','T12','T13','T16','T17','T21','T28']]
m1v2 = json.load(open('scoring/id_mapping_v2.json'))['mapping']
w1co = [json.load(open(p))['misstatement_probability'] for p in glob.glob('runs/rp09/scores/case_*.json')]
pool_fr = frv + w1fr; pool_co = cov + w1co
obsp, pp = perm(pool_fr, pool_co)
R['pooled_secondary'] = {'n_fraud': len(pool_fr), 'n_control': len(pool_co),
    'mean_diff': round(obsp, 2), 'perm_p': pp, 'auc': round(auc(pool_fr, pool_co), 3),
    'note': 'SECONDARY ONLY — never standalone headline (DO NOT). wave-1 frozen scores reused, not re-scored.'}

Path('analysis/wave2_results.json').write_text(json.dumps(R, indent=2, ensure_ascii=False))
print(json.dumps(R, indent=1, ensure_ascii=False))
