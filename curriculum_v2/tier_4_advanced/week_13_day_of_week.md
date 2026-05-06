# Week 13 — Day of Week ⭐⭐ (큰 sample, small consistent edge)

> **목표**: Day-of-week LONG/SHORT bias 적용. Mon LONG ✓, Tue SHORT 단독 ❌ (confluence 필수).
> **검증**: 🟢 T1 (D5 + Phase E)

---

## 1. 검증 데이터

### Forward signed return by Day of Week

| Day | fwd 12b | fwd 24b | fwd 48b | 등급 |
|---|---|---|---|---|
| **Mon** | +0.198 | **+0.299** | **+0.630** ⭐⭐⭐⭐⭐ | strong LONG |
| **Tue** | -0.024 | -0.193 | -0.266 | mild SHORT |
| Wed | +0.098 | +0.106 | +0.211 | mild LONG |
| Thu | +0.007 | +0.011 | -0.087 | flat |
| Fri | -0.065 | -0.082 | -0.189 | mild SHORT |

### Phase E Cost-adjusted Trade Sim

| Edge | Total PF | P3 PF | P3 N | Verdict |
|---|---|---|---|---|
| **MON_LONG** | 1.05 | **1.08** ⭐ | 11,924 | small consistent ✓ |
| TUE_SHORT | 0.94 | 1.04 | 11,575 | flat (single 단독 X) |

→ **Mon LONG 단독 = small but trade-able**. Tue SHORT 단독 = LOSE (cost 후).

### Confluence

| Combo | P3 PF | N | 등급 |
|---|---|---|---|
| **KST 14 + Mon LONG** | **1.22** ⭐⭐ | 169 | best (W14) |
| KST 19 + Mon LONG | 1.09 ⭐ | 169 | (W14) |
| **KST 21 + Tue SHORT** | 1.04 (recent flat) | 171 | (recent only) |
| Squeeze12 + Mon LONG | 1.07 | 14,009 | big sample |

---

## 2. 룰

### Mon LONG bias 강제 (small filter)

```
Monday 매매 시:
  - LONG entry preferred (+5% PF advantage)
  - SHORT entry: 다른 strong reason 필요
  - Confluence bonus: KST 14 + Mon = best (W14)
```

### Tue SHORT 단독 X

```
Tuesday 매매 시:
  - SHORT 단독 = lose (PF 0.94)
  - SHORT 진입: confluence 필수 (KST 21 + Tue 등)
  - LONG entry OK
```

### Mid-week (Wed/Thu/Fri)

```
Day-of-week bias 약함:
  - 다른 factor 우선 (KST hour, ATR z, candle)
  - Day filter 무시 OK
```

---

## 3. 일지 마킹

```json
{
  "kst_dow_w13": "Mon / Tue / Wed / Thu / Fri",
  "dow_bias_w13": "long-strong / mild-short / flat / mild-long / mild-short",
  "filter_violation": "yes (Mon SHORT no reason / Tue SHORT solo) / no"
}
```

---

## 4. 성공 기준

| 기준 | 합격선 |
|---|---|
| Day of Week 식별 누락 | 0% |
| Mon SHORT 진입 (이유 없음) | 0회 |
| Tue SHORT 단독 진입 | 0회 |
| Mon LONG bias 적용 | 100% |

---

## 5. 원본 소스

- [research/results/D5_dow/results.json](../../research/results/D5_dow/results.json)
- [research/results/E_edge_validation/results.json](../../research/results/E_edge_validation/results.json) (MON_LONG, TUE_SHORT)

### 외부 reference
- 학술 논문 "Day of Week effect in equity markets" (다수)
- Linda Raschke "Street Smarts" — weekend gap effect

---

## 6. Caveats

1. **Mon LONG +0.63 ATR (48b raw)** vs **PF 1.05 (cost adj)** 차이 = trade management 효과
2. **N 큼** (37k Mon, 35k Tue) but Cohen's d small (0.05-0.08)
3. Day-of-week effect 시장 효율성 증가로 **점진 약화** 가능성 모니터링

---

## 7. W14 연결

W13 = Day-of-week 단일 factor
W14 = Day + KST hour + 다른 factor confluence

→ W14 가 진짜 trade plan, W13 = building block.

---

*Verified: D5 + Phase E*
