# RP-15 — 홀드아웃 라벨 명명 diff 제안 (WS-3/F-6, diff-only, 미적용)

> **상태: PROPOSED — 소유자 서명 전 어떤 발행 표면도 수정하지 않았다.**
> 근거 산출물: `analysis/label_tags_holdout.json` (3/3 bigR, accession 증거) ·
> `analysis/LABEL_REPORT.md` · 스펙 `specs/label_taxonomy.md` (커밋 d60a6e0).
> 게이트: OWNER_QUEUE **Q-F03**. 발행된 Issue 본문 수정은 GitHub 편집이며
> 이력이 남는다 — 적용 시 "edited" 표시와 함께 수정 사유를 코멘트로 남기는
> 방식을 권장 (동결 원문 선언과의 정합).

## 배경 — 무엇이 문제이고 무엇이 이미 옳은가

발행 표면은 이미 "restatement / non-reliance events, never fraud"를 지킨다
(ISSUE_2 §0 배너·§7). 남은 정밀화는 하나다: **"restatement"가 Big R(4.02
비신뢰 동반)인지 little r인지의 구분이 없다.** 기계 태깅 결과 3/3 전건
Big R — 이 사실은 라벨의 강도를 명시하는 데 쓸 수 있고, 기저율(재작성→집행
~2.2%)은 잠정 라벨의 노이즈를 정직하게 한정한다.

## DIFF-4 (ISSUE_2 — GitHub Issue #3 본문 + `analysis/ISSUE_2_HOLDOUT_DRAFT.md` §7 첫 불릿)

**원문** (line 134–137):

```
- **All three are G2 provisional** (8-K Item 4.02). Item 4.02 is a company's own
  non-reliance determination, not an SEC finding. Monthly re-scan retro-upgrades
  tiers (G1 AAER > G2 4.02 > G3 SEC complaint > G4 DOJ). Until then: "restatement /
  non-reliance event", never "fraud".
```

**교체안**:

```
- **All three are G2 provisional — and all three are Big R restatements** (an
  8-K Item 4.02 non-reliance determination accompanies each event; mechanically
  verified with accession-level evidence in `analysis/label_tags_holdout.json`).
  Item 4.02 is a company's own non-reliance determination, not an SEC finding —
  and base rates cut against over-reading it: only ~2.2% of restatements are
  linked to SEC enforcement (Karpoff et al., TAR 2017). Monthly re-scan
  retro-upgrades tiers (G1 AAER > G2 4.02 > G3 SEC complaint > G4 DOJ), with a
  pre-registered 4-year monitoring window per case (to 2030-02/02/03); window
  expiry without enforcement will itself be reported as label-noise data. Until
  then: "restatement / non-reliance event", never "fraud".
```

## DIFF-5 (README.md — 홀드아웃 라벨 문장, line 106–108 부근)

**원문**:

```
companies carry provisional (G2) restatement labels, not confirmed enforcement:
```

**교체안**:

```
companies carry provisional (G2) restatement labels — all three Big R (Item 4.02
non-reliance), mechanically verified (`analysis/label_tags_holdout.json`) — not
confirmed enforcement:
```

README.ko.md 대응 절에는 동일 취지의 국문 병기를 적용한다 ("전건 Big R —
Item 4.02 비신뢰 선언 동반, 기계 검증").

## 검토했으나 변경하지 않는 지점 (기록)

- ISSUE_2의 "most misstatement-like case" (×2) — 이는 ground truth 명명이
  아니라 **점수 프로파일 서술**이다 (HUBG의 점수 형태가 misstatement 패턴과
  닮았다는 뜻). 라벨 분류 체계 diff의 범위 밖 — 무변경.
- README line 53 "confirmed misstatement cases" — wave-1/2 AAER 확정 tier
  서술로 정확 — 무변경.

## 적용 조건

- 소유자 Q-F03 서명 후에만. 적용 시 이 파일 하단에 서명 블록 추가 +
  decisions_log 기록 (RP-14 선례).
