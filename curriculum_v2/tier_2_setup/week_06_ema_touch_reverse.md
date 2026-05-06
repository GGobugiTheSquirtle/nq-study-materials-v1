# Week 6 — EMA20 Touch # 🔴 REVERSE 통설

> **목표**: "1st touch best, 4th+ skip" 통설 NQ 5m 데이터로 REJECTED 된 것 학습.
> **검증**: 🔴 T1 REVERSE (A2 + R1)

---

## 1. 검증 데이터 (A2 + Robustness)

### Hit rate (MFE >= 1×ATR within 12 bars)

| Touch # | N | w_h2y HR | last_2y HR | last_1y HR |
|---|---|---|---|---|
| 1st | 11,408 | 64.84% | 65.36% | 64.81% |
| 2nd | 5,857 | 65.01% | 64.89% | 66.92% |
| 3rd | 2,907 | 64.72% | 65.44% | 65.83% |
| **4th+** | 2,465 | **66.52%** | **68.90%** | **68.60%** |

→ **4th+ touch HR 더 높음** (1.7-3.8pp).

### Robustness (R1 — different forward windows)

| fwd | 1st HR | 4th+ HR | Δ_h2y |
|---|---|---|---|
| 6b | 51.41% | 51.82% | -0.41 |
| 12b | 64.84% | 66.52% | -1.68 |
| 24b | 75.88% | 78.46% | -2.58 |
| 48b | 83.11% | 85.20% | -2.09 |

**모든 forward window 에서 4th+ > 1st. REVERSE robust.**

---

## 2. 결론

### 통설 REJECTED

- ❌ "EMA20 1st/2nd touch best, 4th+ touch break" — Linda HG / Adam Grimes paraphrase
- ❌ "Touch count 많을수록 SR 강하지만 곧 break"

### 데이터 결론

- ✓ Touch count 와 hit rate 거의 무관 (~65% 모든 touch)
- ✓ 4th+ touch 약간 더 높음 (continuation strong trend)
- ✓ "EMA20 retest 자체" = valid setup (HR ~65%)

---

## 3. 룰 (Update)

```
EMA20 retest valid setup (정배열):
  - Any touch count OK (1st/2nd/3rd/4th+)
  - Bounce 확인 (다음 봉 close > EMA20)
  - Confluence (W4 KST, W13 Day) 필수
  - "1st only" 룰 삭제
```

---

## 4. 일지 마킹

```json
{
  "ema20_touch_w6": "1st / 2nd / 3rd / 4th+",
  "bounce_confirmed": true,
  "ema20_break": false   // 정배열 깨졌는지
}
```

---

## 5. 성공 기준

| 기준 | 합격선 |
|---|---|
| Touch # 식별 | 100% |
| Touch # 만으로 진입/거부 결정 | 0회 (룰 삭제) |
| Bounce 확인 후만 진입 | 100% |

---

## 6. 원본 소스

- [research/results/A2_ema20_touch/results.json](../../research/results/A2_ema20_touch/results.json) — 22,639 touches measured
- [research/results/R_robustness/results.json](../../research/results/R_robustness/results.json) — fwd window check
- ADR-028 Linda Holy Grail REJECTED — pre-existing user research
- [Adam Grimes blog](https://adamhgrimes.com/blog/) — pullback (다른 자산/timeframe)

---

## 7. 통설 vs 데이터 — 학습 가치

| 외부 권위 (Linda/Grimes) | NQ 5m 데이터 |
|---|---|
| "1st touch = best entry" | ❌ Touch # 무관 |
| "4th+ touch break 위험" | ❌ 오히려 4th+ HR 높음 |
| "Holy Grail" effect | ❌ stride bug 영향 (ADR-028) + A2 confirm |

→ **통설 REVERSE = 학습 가치 (다른 트레이더 룰 면역)**.

---

## 8. Caveat

- 측정 방법 = "정배열 구간 + close ≤ EMA20 = touch event"
- 다른 정의 (예: low <= EMA20) 시 결과 다를 수 있음
- 추가 검증 권장 (다음 라운드)

---

*Verified: A2 + R1 — 22,639 events × 4 forward windows*
