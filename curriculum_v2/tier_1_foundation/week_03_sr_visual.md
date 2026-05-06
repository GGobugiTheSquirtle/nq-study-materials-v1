# Week 3 — SR Visual Aid (zone vs line edge X)

> **목표**: SR zone (touch≥3) 통설 NQ 5m REJECTED 인지. SR = 시각 도구만.
> **검증**: 🔴 T1 NOGO (B1)

---

## 1. 검증 데이터 (B1)

### Zone (touch≥3, ±0.25×ATR) vs single Line touch hit rate

| Threshold | Zone HR | Line HR | Δ pp |
|---|---|---|---|
| MFE 0.5×ATR fwd 12b | 80.79% | 81.42% | -0.62 |
| MFE 1.0×ATR fwd 12b | 62.56% | 63.01% | -0.44 |

### By touch count (zone 만)

| Touch count | HR | N |
|---|---|---|
| ≥3 | 80.79% | 9,007 |
| ≥4 | 80.19% | 4,432 |
| ≥5 | 78.62% | 2,250 |
| ≥6 | 77.80% | 1,234 |

→ **Touch 많을수록 HR 약간 낮아짐** (통설 "강한 SR = 강한 반응" REVERSE)

---

## 2. 결론

### 통설 REJECTED

❌ "SR zone (touch≥3) > 단일 line" — Δ -0.62pp
❌ "Strong SR (high touch count) = strong reaction"

### 데이터 결론

✓ **SR = 시각 도구로만**. Edge X.
✓ Zone vs line 거의 차이 X (0.5-1pp)
✓ 강한 SR (touch 많음) 오히려 hit rate 약간 낮음

---

## 3. 룰 (Update)

### SR 활용

```
Visual aid:
  - SR zone 그리기 OK (시각적 자리 인지)
  - 진입 trigger 단독 X
  - Confluence 표시용 (KST hour, candle 등과 결합 시)
```

### 진입 시 SR 체크 (참고용)

```
LONG entry 시:
  □ 위 resistance zone 거리 (참고)
  □ 아래 support zone 거리 (참고)
  □ Top buy 위험 (W8 fib < 23.6%) — 핵심 룰

→ SR 단독 진입 금지, top buy 회피 (W8) 가 더 정확한 SR 효과
```

---

## 4. 일지 마킹

```json
{
  "sr_above_atr": 1.2,       // 시각 참고
  "sr_below_atr": 0.8,
  "sr_quality_w3": "visual-only"   // edge X 인정
}
```

---

## 5. 성공 기준

| 기준 | 합격선 |
|---|---|
| Zone vs line 식별 (학습) | 80%+ |
| SR 단독 진입 | 0회 |
| Top buy 회피 (W8) 적용 | 100% (이게 진짜 SR 효과) |

---

## 6. 원본 소스

- [research/results/B1_sr_zone_vs_line/results.json](../../research/results/B1_sr_zone_vs_line/results.json)
- [Adam Grimes "Art and Science"](https://www.amazon.com/Art-Science-Technical-Analysis-Statistics/dp/1118115120) — measurable
- [Al Brooks Price Action](https://www.youtube.com/@AlBrooksPriceAction)
- [02 Price Action sources](../../02_price_action/sources.md)

---

## 7. Caveat

- 측정 = swing pivot 자동, ±0.25×ATR cluster
- 다른 SR 정의 (POC / VWAP / FVG / OB) 별도 검증 필요 (다음 라운드)
- W8 Top buy 회피 가 진짜 SR effect (HR 47% lowest)

---

*Verified: B1 — 9,007 zone events + 33,460 line events*
