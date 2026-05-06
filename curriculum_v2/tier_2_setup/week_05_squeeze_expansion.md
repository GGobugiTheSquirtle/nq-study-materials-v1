# Week 5 — ATR z Squeeze → Expansion ⭐

> **목표**: ATR z 12-bar squeeze 식별 + expansion direction 따라 entry.
> **검증**: 🟢 T1 (D3)

---

## 1. 검증 데이터 (D3)

### Squeeze 정의

```
ATR z = (current ATR - 60-day mean ATR) / 60-day std
squeeze_12 = past 12 bars 모두 z < -0.5
            (~1시간 동안 변동성 압축)
```

### Forward range expansion (squeeze vs no-squeeze)

| Forward window | range_squeeze | range_no | Δ % |
|---|---|---|---|
| 12b (1h) | 4.36 / ATR | 3.64 | **+20%** |
| 24b (2h) | 6.93 | 5.25 | **+32%** |
| **48b (4h)** | **11.22** | 7.76 | **+44%** |

→ Squeeze 후 forward range 확실히 큼. **방향 미정** (signed return ≈ 0).

### BB squeeze 통설 NQ 5m **데이터 검증 ✓**

(W1 v1 markdown 의 통설 부분 confirmed)

---

## 2. 룰

### Entry trigger

```
Step 1: ATR z 12-bar rolling max < -0.5 → SQUEEZE 활성
Step 2: Wait — direction 미정
Step 3: Squeeze 종료 후 첫 directional break (close 외부 BB?)
Step 4: + Confluence (KST hour, Day of Week) 가능
Step 5: Entry direction = break direction
```

### Squeeze 동안

- **진입 금지** (방향 미정)
- 차트 mark only

### Phase E sim (단독 SQ12 LONG)

- Total PF 1.02
- P3 PF 0.99 (flat)

→ 단독 LONG bias 약함. **Direction confluence 필수**.

### 결합 (D6 + Phase E)

| Combo | P3 PF | N |
|---|---|---|
| SQ12 + Mon LONG | 1.07 | 14,009 |
| SQ12 + KST 04 (BURN_X) | 1.62 (P3 N=18) | 18 (small) |

---

## 3. 차트 관찰 과제

매일 5분:
1. ATR(14) chart 추가
2. ATR z (60-day) 계산 (수동 또는 indicator)
3. **z < -0.5 가 12 bar 연속인지 mark**
4. Squeeze 후 directional break 시점 식별

---

## 4. 일지 마킹

```json
{
  "squeeze_w5": "active / inactive",
  "squeeze_duration_bars": 14,
  "expansion_breakout_w5": "long / short / not-yet",
  "entered_during_squeeze": false
}
```

---

## 5. 성공 기준

| 기준 | 합격선 |
|---|---|
| Squeeze 식별 정확 | 80%+ |
| Squeeze 동안 진입 | 0회 |
| Breakout direction 식별 | 80%+ |

---

## 6. 원본 소스

- [research/results/D3_vol_expansion/results.json](../../research/results/D3_vol_expansion/results.json)
- [John Bollinger book](https://www.amazon.com/Bollinger-Bands-John/dp/0071373683) — BB squeeze 표준
- [Linda Raschke "Street Smarts"](https://www.amazon.com/Street-Smarts-High-Probability-Short-Term-Strategies/dp/0965046109) — Volatility expansion

---

## 7. Caveat

- **Direction 약함** (signed return ≈ 0 in squeeze) — 단독 trade 어려움
- W14 confluence 와 결합 시만 trade-able
