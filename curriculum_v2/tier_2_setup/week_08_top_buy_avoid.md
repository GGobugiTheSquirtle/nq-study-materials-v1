# Week 8 — Top Buy 회피 ⭐ (사용자 핵심 약점 처방)

> **목표**: 신고가 직진입 금지. 23.6% 이상 retrace 후 진입.
> **검증**: 🟢 T1 (A3 fib pullback)

---

## 1. 검증 데이터 (A3)

### Forward MFE 1×ATR hit rate by Fib retrace level

| Fib retrace | N | h2y HR | Verdict |
|---|---|---|---|
| **<23.6%** (top buy) | 55,423 | **47.35%** ❌ | LOWEST — 회피 |
| 23.6-38.2% | 40,537 | 53.29% | OK |
| 38.2-50% | 23,950 | 55.29% | good |
| 50-61.8% | 17,381 | 57.65% | better |
| 61.8-78.6% | 15,613 | 59.91% | better |
| 78.6-100% | 10,059 | 60.38% | best |
| **>100% broken** | 7,820 | **62.65%** | highest |

### 핵심 발견

1. **<23.6% 진입 (Top Buy) HR 47%** — 가장 낮음, 통설 confirm ✓
2. **Deeper better** monotonic — 통설 "78.6+ 위험" REJECTED
3. **>100% broken trend** 까지 hit rate 가장 높음 (62.65%)

---

## 2. 룰

### Top Buy 회피 (필수)

```
LONG entry 시점:
  Step 1: 직전 swing high 식별
  Step 2: 현재가 vs swing high 거리 측정 (in ATR)
  Step 3: Retrace % = (swing_high - current) / leg_size
  Step 4:
    - retrace < 23.6%  →  ❌ TOP BUY 위험, 진입 금지
    - retrace 23.6%~78.6% →  ✓ entry 자격 (다른 confluence 필요)
    - retrace > 100% (broken) →  추세 전환 위험 (context 필수)
```

### Pullback entry checklist

```
□ Swing high 식별
□ Retrace % >= 23.6% ✓
□ EMA20 / EMA50 touch (W6, optional)
□ Bounce 확인 (다음 봉 close > 이전 close)
□ Confluence (KST hour, Day of week, W14)
```

---

## 3. 시각 도식

```
LONG entry valid zones:

  Swing High SH
       ╲
        ╲╲
         ╲╲    ← retrace 23.6% (lowest valid)
          ╲╲
           ╲╲    ← retrace 38.2% (good)
            ╲╲
             ╲╲    ← retrace 50% (better)
              ╲╲
               ╲╲    ← retrace 61.8% (better)
                ╲╲
                 ╲╲    ← retrace 78.6% (best)
                   ╲╲
                    ╲   ← retrace 100% (caution: broken)
                Swing Low
```

❌ 진입 금지 zone: swing high - 23.6% retrace 까지 (top buy)
✓ Valid: 23.6% ~ 100% retrace
⚠️ Caution: > 100% broken (trend 전환 가능)

---

## 4. 일지 마킹 (모든 LONG entry)

```json
{
  "fib_retrace_w8": 0.45,    // 38.2-50% bin
  "entry_type_w8": "pullback-50 / pullback-61.8 / breakout-retest / **top-buy** / random",
  "swing_high_idx": 12345,
  "leg_size_atr": 2.5,
  "retrace_atr": 1.1,
  "top_buy_alarm": false,    // true if retrace < 23.6% AND LONG
  "valid_pullback_setup": true
}
```

**진입 lock**:
- entry_type = "top-buy" → **즉시 cancel + recheck**
- retrace < 23.6% AND LONG → 진입 금지

---

## 5. 성공 기준

| 기준 | 합격선 |
|---|---|
| Top Buy 진입 | **0회** ⭐⭐⭐ |
| Retrace 식별 즉답 | < 30초 |
| Pullback 23.6%+ 진입 비율 | 80%+ (LONG 중) |
| Fib tool 사용 | 모든 LONG entry |

---

## 6. 사용자 약점 직접 처방

| 약점 (LEARNINGS) | v1 처방 | v2 데이터 | 결과 |
|---|---|---|---|
| L5 Top buying (신고가 진입) | 38.2-61.8 sweet spot | <23.6% HR=47% (lowest) | 처방 강화 ✓ |
| L17 Pullback discipline | Pullback 룰 | Deeper better | 통설 일부 REVERSE |

---

## 7. 원본 소스

- [research/results/A3_fib_pullback/results.json](../../research/results/A3_fib_pullback/results.json)
- [Linda Raschke "Street Smarts" Holy Grail chapter](https://www.amazon.com/Street-Smarts-High-Probability-Short-Term-Strategies/dp/0965046109)
- [Adam Grimes "Art and Science"](https://www.amazon.com/Art-Science-Technical-Analysis-Statistics/dp/1118115120)
- [Tom Hougaard "Best Loser Wins" (FREE PDF)](https://tradertom.com/wp-content/uploads/2021/03/BEST-LOSER-WINS-1.pdf)

### Sources.md
- [03 Trend Following sources ⭐⭐⭐](../../03_trend_following/sources.md)
- [01 Psychology sources](../../01_psychology/sources.md) — Hougaard

---

## 8. Caveat

- **Sweet spot 38.2-61.8% 통설 부분 REJECTED** — deeper better
- 단, "Top buy 회피" (<23.6%) 는 강력 confirmed
- W14 confluence 결합 시 trade-able

---

*Verified: A3 — 170,795 pullback events analyzed*
