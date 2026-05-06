# Week 9 — ATR z Normalization (REJECTED + reframe)

> **목표**: ATR z high momentum 통설 REJECTED. ATR z = stop/TP normalization 도구로만.
> **검증**: 🔴 T1 NOGO H1 (A4) / 🟡 T1 NEW directional bias (R2)

---

## 1. 검증 데이터 (A4 + R2)

### A4: Forward range/ATR by z bin (REVERSED)

| z bin | mu range/ATR (12b fwd, h2y) |
|---|---|
| z < -1 | **4.310** (highest) |
| -1 ≤ z < -0.5 | 4.207 |
| baseline | 3.934 |
| +0.5 ≤ z < +1 | 3.437 |
| +1 ≤ z < +2 | 3.341 |
| z ≥ +2 | 3.157 (lowest) |

→ **Mean reversion in volatility**. High z → low forward range/ATR. REVERSE 통설.

### R2: Forward signed return (다른 결과!)

fwd 48b signed:
| z bin | signed/ATR (h2y) |
|---|---|
| low (z < -0.5) | **-0.169 SHORT drift** |
| baseline | -0.011 |
| mid (+0.5..+1) | +0.066 |
| **high (z ≥ +1)** | **+0.174 LONG drift ⭐** |

→ **High z = LONG bias (long horizon)**. New finding.

---

## 2. 결론

### 통설 REJECTED

❌ "z high = momentum, enter LONG/SHORT direction" (range/ATR 측면)

### 새 NEW finding

✓ **z high (≥+1) → fwd 48b LONG bias +0.174 ATR** (4시간 hold 시)
✓ z low (<-0.5) → SHORT bias

### Squeeze (D3) — separate

D3 측정: z 12-bar max < -0.5 = squeeze → fwd range +44% (W5)

---

## 3. 룰 (Reframe)

### ATR z 활용

```
1. Stop/TP normalization 도구 (primary)
   SL = 1.5 × ATR(14)
   TP = 2.0 × ATR(14)
   → z 무관, ATR 절대값만 사용

2. Squeeze detection (W5)
   z 12-bar max < -0.5 → expansion 대기

3. Long-hold directional bias (NEW, R2)
   z >= +1 + 4시간 hold → small LONG bias (+0.174 ATR)
   z < -0.5 + 4시간 hold → small SHORT bias (-0.169)
   단 confluence 필수 (단독 trade 어려움)
```

### 단독 entry signal X

기존 v1 룰 "z >= +0.5 진입 OK" → REJECTED.

---

## 4. 일지 마킹

```json
{
  "atr_z_w9": 0.7,
  "z_role_w9": "stop-sizing",   // entry signal 아님
  "squeeze_w9": false,
  "long_hold_intent": false      // true 시 z direction bias 적용
}
```

---

## 5. 성공 기준

| 기준 | 합격선 |
|---|---|
| ATR z 단독 entry | 0회 |
| ATR 기반 SL sizing | 100% |
| Squeeze detection (W5) | 정확 |

---

## 6. 원본 소스

- [research/results/A4_atr_zscore/results.json](../../research/results/A4_atr_zscore/results.json)
- [research/results/R_robustness/results.json](../../research/results/R_robustness/results.json) — R2 directional
- [Bob Volman scalping](https://www.amazon.com/Forex-Price-Action-Scalping-depth/dp/9090257098)

---

## 7. Caveat

- 통설 z high momentum range REJECTED
- New directional bias (h igh z LONG long-hold) 약함 — confluence 필수
- 측정 60-day rolling window
