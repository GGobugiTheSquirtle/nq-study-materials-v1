# Week 2 — EMA 배열 🔴 (short-window REJECTED, long-hold small effect)

> **목표**: EMA 정/역배열 통설 NQ 5m 데이터로 short window REJECTED 확인. Long hold 시만 small effect.
> **검증**: 🔴 T1 NOGO short / 🟡 T1 PARTIAL long (A1 + R3)

---

## 1. 검증 데이터 (A1 + R3 robustness)

### Cohen's d (정 vs 역) by forward window (h2y)

| fwd window | d_h2y | mu(정) | mu(역) | Δμ ATR |
|---|---|---|---|---|
| 1 bar (5분) | -0.010 | +0.020 | +0.031 | -0.011 |
| 3 bars | +0.022 | +0.049 | +0.012 | +0.037 |
| **5 bars (25분)** | **+0.014** | +0.056 | +0.031 | +0.025 |
| 12 bars (1h) | +0.014 | +0.047 | +0.001 | +0.046 |
| 24 bars (2h) | +0.036 | +0.109 | -0.056 | +0.165 |
| **48 bars (4h)** | **+0.042** | +0.158 | -0.119 | **+0.277** |

→ Short window (5b) **negligible**. Long window (48b) **small but real**.

### Bootstrap CI95 (w_h2y, fwd 5b): [-0.021, +0.057] → 0 포함

### Regime breakdown (fwd 5b)

- BEAR: d=+0.089 (small) ⭐
- CHOP: d=+0.022 (negligible)
- BULL: insufficient bear sub-group

---

## 2. 룰

### Short window scalp (≤12b, 1시간 이하 hold)

❌ EMA 배열 무관. 통설 "정배열 LONG bias" 무시.

### Long window position (24-48b, 2-4시간 hold)

✓ 정배열 + LONG 약한 small bias (Δμ ~0.28 ATR over 4시간)
✓ BEAR regime 에서 약간 효과 큼

### 사용

```
Short scalp (W11 BURN_X 등):
  EMA 배열 X — 다른 factor 만 (KST hour, ATM trail)

Long position (장기 hold 시도):
  정배열 + LONG entry → +0.28 ATR over 4h expected
  단, single signal 약함 → confluence (W14) 필요
```

---

## 3. 통설 vs 데이터

| 통설 | 데이터 결과 |
|---|---|
| "EMA 정배열 + Price > EMA20 = 90% LONG 자격" | ❌ d=0.014 negligible (short window) |
| "역배열 LONG = 진입 금지" | 부분 ✓ (long-hold 시 mu 차이 있음) |
| "EMA 배열 = 추세 명확화" | ✓ 시각 도구로만, edge X |

---

## 4. 일지 마킹

```json
{
  "ema_alignment_w2": "정 / 혼 / 역",
  "long_hold_intended": false,    // true 면 EMA filter 적용
  "scalp_short_hold": true       // true 면 EMA filter 무시
}
```

---

## 5. 성공 기준

| 기준 | 합격선 |
|---|---|
| 정/혼/역 식별 정확 | 100% |
| Short scalp 시 EMA 단독 진입 lock | 0 violation |
| Long-hold + 정배열 + 다른 confluence | OK |

---

## 6. 원본 소스

- [research/results/A1_ema_alignment/results.json](../../research/results/A1_ema_alignment/results.json)
- [research/results/R_robustness/results.json](../../research/results/R_robustness/results.json)
- ADR-028 Linda HG REJECTED — pre-existing
- [Stan Weinstein book](https://www.amazon.com/Secrets-Profiting-Bull-Bear-Markets/dp/1556236832) — Stage analysis

---

## 7. Caveat

- 통설 short window REJECTED 강력 confirmed
- Long hold 시 small effect = 단독 trade 어려움 (cost > edge)
- W14 confluence 결합 시만 활용

---

*Verified: A1 (30k samples) + R3 (6 forward windows)*
