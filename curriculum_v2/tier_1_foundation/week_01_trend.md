# Week 1 — Multi-TF 추세 (small effect, confluence factor)

> **목표**: Multi-TF (5m+15m+1h) all-up vs all-down — small directional bias 인지. 단독 trade 불가.
> **검증**: 🟡 T1 small (B4)

---

## 1. 검증 데이터 (B4)

### All-up (Close > EMA20 on 5m + 15m + 1h) vs All-down

| Window | mu(all-up) h2y | mu(all-down) h2y | Cohen d |
|---|---|---|---|
| 12b | +0.026 | -0.050 | +0.025 |
| 24b | +0.079 | -0.061 | +0.032 |

last_2y at 24b: mu(up) +0.080, mu(down) -0.118 → Δ=0.20 ATR small

→ **Real but small effect** (d ~ 0.03 negligible-small).

---

## 2. 룰

### Multi-TF as confluence factor only

```
All-up (5m + 15m + 1h all close > EMA20):
  - +0.08 ATR LONG bias (24b)
  - Confluence factor for W14 plans
  - 단독 entry trigger X

All-down (대칭):
  - -0.06 ATR SHORT bias (24b)
  - Confluence factor only

Mixed:
  - 신호 약함, 다른 factor 우선
```

### Range LONG 충동 lock

기존 v1 룰 유지:
- Range (no clear HH/HL or LL/LH) → 진입 자제
- Multi-TF 부분 confirm (5m only) → 약한 setup

---

## 3. 차트 관찰

매일 5분:
1. 5m 차트 — 추세 명명 (up/down/range)
2. 15m 차트 — 추세 명명
3. 1h 차트 — 추세 명명
4. 3 TF alignment 체크

---

## 4. 일지 마킹

```json
{
  "trend_5m_w1": "up / down / range",
  "trend_15m_w1": "up / down / range",
  "trend_1h_w1": "up / down / range",
  "all_up_w1": false,
  "all_down_w1": false,
  "mixed_w1": true
}
```

---

## 5. 성공 기준

| 기준 | 합격선 |
|---|---|
| 3-TF 추세 식별 | 100% (시각 단순) |
| Range LONG 충동 진입 | 0회 |
| Multi-TF 단독 진입 | 0회 (룰) |

---

## 6. 원본 소스

- [research/results/B4_multi_tf/results.json](../../research/results/B4_multi_tf/results.json)
- [Al Brooks Price Action](https://www.youtube.com/@AlBrooksPriceAction)
- [02 Price Action sources](../../02_price_action/sources.md)

---

## 7. Caveat

- Cohen d=0.03 negligible-small — 단독 가치 거의 X
- 15m/1h EMA = 5m EMA span 곱 approximation (정확 X)
- W14 confluence 결합 시만 활용

---

*Verified: B4 — 100k bars sampled*
