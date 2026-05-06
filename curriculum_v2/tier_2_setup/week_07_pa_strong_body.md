# Week 7 — PA Strong Body (continuation small edge)

> **목표**: Strong body candle (body ≥ 70% range) = continuation small bias 인지. Hammer/Star 단독 진입 X.
> **검증**: 🟢 T1 partial (D4)

---

## 1. 검증 데이터 (D4)

### Forward signed return by candle pattern (24b)

| Pattern | h2y signed | last_2y |
|---|---|---|
| **Bull strong body** (≥0.7 + bullish) | **+0.156** ✓ | +0.257 |
| **Bear strong body** (≥0.7 + bearish) | -0.085 (mild) | -0.155 |
| **Hammer** (lower wick ≥0.5) | **-0.200 SHORT** ❌ | -0.385 |
| **Shooting Star** | +0.093 LONG ❌ | +0.033 |
| Doji (body < 15%) | -0.106 | -0.238 |

### Phase E sim

| Pattern | Total PF | P3 PF | P3 N |
|---|---|---|---|
| BULL_BODY_CONT_LONG | 1.02 | 0.99 | 12,482 |
| BEAR_BODY_CONT_SHORT | 0.94 | 0.95 | 11,361 |

→ Strong body **continuation small bias** confirmed (signed +0.16 to -0.09)
→ Trade sim flat after cost (1.02 / 0.94)
→ Confluence 필요

---

## 2. 핵심 발견

### 통설 confirm (부분)

✓ **Strong body = continuation** (small effect)
- Bull body → fwd 24b +0.156 ATR (LONG)
- Bear body → -0.085 ATR (mild SHORT)

### 통설 REVERSE (단순 적용 시)

❌ **Hammer/Shooting Star reversal** (Steve Nison standard)
- Hammer 단독 → fwd 24b **-0.200 ATR (SHORT)**
- Shooting Star 단독 → +0.093 ATR (LONG, 약함)

**해석**: Hammer/Star 통설은 "context (downtrend bottom)" 가정. 무 컨텍스트 단순 wick ratio 만으로는 REVERSE.

---

## 3. 룰

### Strong Body — Continuation small bias

```
Bull strong body (body ≥ 70% range, bullish):
  - Forward LONG bias +0.16 ATR (24b)
  - Confluence factor (small)
  - Entry trigger 단독 X

Bear strong body (대칭):
  - Forward SHORT bias -0.085 (mild)
  - Confluence factor only
```

### Hammer/Shooting Star — DO NOT trade single signal

```
Hammer (lower wick ≥ 50%, body < 40%):
  - Single signal → SHORT bias (-0.20 ATR)
  - Reversal LONG 가정은 context (downtrend bottom) 시만
  - 단독 LONG 진입 금지

Shooting Star (upper wick ≥ 50%):
  - Single signal → LONG bias (+0.09 ATR weak)
  - 통설 SHORT reversal 가정 시 위험
  - 단독 SHORT 진입 금지
```

### 결합 (W14)

- Bull strong body + KST 14 + Mon → **W14 confluence trade plan**

---

## 4. 일지 마킹

```json
{
  "candle_w7": "bull-strong / bear-strong / hammer / shooting-star / doji / regular",
  "body_pct": 0.78,
  "wick_upper": 0.10,
  "wick_lower": 0.12,
  "continuation_bias": "long-small / short-mild / none"
}
```

---

## 5. 성공 기준

| 기준 | 합격선 |
|---|---|
| Strong body 식별 | 80%+ |
| Hammer/Star 단독 진입 | 0회 |
| Bull body + confluence (W14) 진입 | OK |

---

## 6. 원본 소스

- [research/results/D4_candle_structure/results.json](../../research/results/D4_candle_structure/results.json)
- [Steve Nison "Japanese Candlestick"](https://www.amazon.com/Japanese-Candlestick-Charting-Techniques-Second/dp/0735201811) — context 강조
- [Al Brooks Price Action](https://www.youtube.com/@AlBrooksPriceAction) — bar-by-bar
- [Bob Volman](https://www.amazon.com/Forex-Price-Action-Scalping-depth/dp/9090257098) — 5m PA scalp

---

## 7. Caveat

1. **Hammer/Star REVERSE 측정** = 단순 wick ratio 만 (context 무시)
2. Steve Nison 원전 = "다운트렌드 후 hammer = 반전" — 컨텍스트 필요. 우리 측정은 모든 hammer.
3. **Confluence 필수** (단독 effect 작음)
