# 06 — Scalping 기법 — 핵심 정리

> **사용자 자가 정의 (정확)**: "변동성·속도·힘 적절해서 방향 안 맞춰도 순발력·임기응변만으로 가능할 때"
>
> **데이터 검증** (05-05): ≤2min legs WR 66.7% / +$87 / >2min legs WR 13.5% / -$1,659
>
> **함정** (R32 후보): sub-2min winner = 욕심 발화점

---

## 🎯 핵심 명제 5가지

### 1. Scalping Conditions = "VTR" (Volatility Trading Range)

**Bob Volman, "Forex Price Action Scalping"**:
- VTR = 시장이 scalping 가능한 변동성 보이는 구간
- ATR (5분) > 평균의 80% 이상 = scalp 가능
- ATR < 평균의 50% = 진입 X (chop, 노이즈)

**사용자 자가 정의 직접 호환**:
- "변동성 적절" = ATR P40-P80 사이 (P=percentile)
- "속도 적절" = bar momentum (close-open / range > 0.5)
- "힘 적절" = volume > 평균 × 1.2

**정량화 룰**:
```
if ATR_5m_now > ATR_5m_30bar_avg × 0.8:
    if bar_momentum > 0.5 and volume > avg × 1.2:
        scalp_candidate = True
```

---

### 2. Setup Quality > Frequency (모든 scalp 권위자 공통)

**Mike Bellafiore, Tom Hougaard, Bob Volman 공통**:
- **Best scalp = 자주 X, 정확하게**
- 하루 3-5 setup 이 표준 (10+ = overtrading)
- 같은 setup 반복 = playbook (사용자 룰 시스템 호환)

**사용자 데이터 검증**:
- 05-05: 21 cluster / 1h 9min = 1 cluster / 3.3 min
- 04-28 / 05-04: 1 cluster / 5.5 min
- 05-04 보다 빠른 모든 세션 = 손실 발생

→ **목표 빈도**: 1 cluster / 5+ min (≤ 12 cluster / 1h)

---

### 3. Round Numbers + Levels = Pre-Defined Entry

**Bob Volman + Linda Raschke**:
- Round numbers (e.g., 27950, 28000) = 자연스러운 SR
- Daily levels (Adam Mancini) = institutional reference
- AVWAP (Brian Shannon) = volume reference
- ICT OB / FVG (이전 카테고리) = institutional zone
- → **모든 scalp entry = pre-defined level 에서만**

**Implementation**:
- 진입 전 차트에 ALL levels 표시
- 가격이 level 안 닿으면 진입 X
- Level 닿고 react 캔들 (reversal bar / breakout retest) 만 진입

**사용자 약점 직접 처방**:
- Top buying = level 보다 0.2×ATR 위 = "no level, just chase" = 진입 X
- Level pre-marked + 가격 닿음 → 진입 = 정확한 자리

---

### 4. Tight Loss / Quick Cut (Tom Hougaard 와 동일)

**Bob Volman, Tom Hougaard, Linda Raschke 공통**:
- Scalping = 작은 SL
  - 5-10 NQ point (사용자 5m TF 적합)
  - SL 도달 = 즉시 cut
- Win 시 partial 1/2 + trail
- Win 못 가면 BE move 또는 cut at 2 min (R31)

**사용자 R31 와 호환**:
- 2분 cut = scalp 의 표준
- Sub-2min winner = 짧은 win, 다음 진입 size up X (R32)

---

### 5. Order Flow + Tape Reading

**BookMap, Brett Steenbarger, classic tape reading**:
- DOM (Depth of Market): bid/offer 의 size 변화 = institutional intent
- Footprint chart: candle 안의 buyer vs seller volume
- Cumulative Delta: buying vs selling pressure 누적

**NQ 적용**:
- BookMap (유료 but free trial) = order flow visualization
- Tradovate / TradingView 의 DOM = 무료
- 사용자 micro-structure 인지 보강

**사용자 적용 (advanced)**:
- 5분 차트 만으로 부족 → DOM 추가 = institutional 진입/탈출 인지
- "변동성·속도·힘" 의 정량 = DOM 활성화 + footprint
- 단, 학습 cost 큼 — Phase 4-5 후 학습 권장

---

## 📋 사용자 약점 → 직접 처방

| 사용자 약점 | 처방 | 출처 |
|---|---|---|
| Sub-2min winner trap (R32) | Win 후 size up 금지, same setup 반복만 | Volman + Hougaard |
| Top buy after winner | Round number / level 외에서 진입 X | Volman + Mancini |
| Hold > 2min loss | Tight SL + 2min cut | Volman + Hougaard |
| 짤짤이 = right conditions | VTR + bar momentum 정량화 | Volman |
| 진입 빈도 과다 | 1 cluster / 5+ min target | SMB + Hougaard |

---

## 📚 권장 학습 순서

### Week 1 — 기초
1. **Bob Volman — "Forex Price Action Scalping"** (책)
   - VTR 컨셉 / 진입 조건 정량
2. **Steve Nison — Candlestick patterns** (한국어 번역본)
   - reversal/continuation 캔들 인식

### Week 2 — Implementation
3. **SMB Capital — Scalping playlist**
4. **Tom Hougaard — Short-term videos** (Best Loser Wins 컨셉의 scalp 적용)
5. **Linda Raschke — "Anti" pattern + 80-20 setups** (Street Smarts 책)

### Week 3 — Advanced (선택)
6. **BookMap educational content** ([youtube.com/@BookmapPro](https://www.youtube.com/@BookmapPro))
   - order flow 입문
7. **ATAS / Sierra Chart educational** — footprint chart

### Week 4 — 통합
8. **Joe Ross — "Trading by the Book" Hook patterns** (책)
9. **Al Brooks — scalp chapter** (위 02 Price Action 와 중복, 다시 보기)

---

## 🎬 핵심 영상 / 자료 직링크

| # | 자료 | 비고 |
|---|---|---|
| Y1 | [BookMap Pro YouTube](https://www.youtube.com/@BookmapPro) | order flow scalp |
| Y2 | [Tom Hougaard YouTube](https://www.youtube.com/@traderTomHougaard) | tight loss / wide win |
| Y3 | [SMB Capital YouTube](https://www.youtube.com/@smbcapital) | playbook scalp |
| W1 | [BookMap learn](https://bookmap.com/learn/) | order flow theory |

---

## 💎 핵심 명언

### Bob Volman
- "Scalping is not action. Scalping is patience for the right action."
- "VTR first. Setup second. Entry third. Cut fourth."
- "If the level isn't there, the trade isn't there."

### Tom Hougaard (scalp 적용)
- "Scalp the same setup every day. Don't chase variety."
- "Tight loss is a feature, not a bug."

### Linda Raschke
- "Anti = quick scalp against trend, then back to trend. Never hold counter-trend."

### Joe Ross (Hook)
- "Hook pattern: 3-bar setup. Same every time. Same exit every time."

---

## 📝 사용자 매매 직접 적용 — Scalp 8-Step

```
[Pre-Scalp Entry — 30초]
1. □ VTR? ATR_5m > 평균 × 0.8?
2. □ 시간대? KST 22:30~23:30 (NY first hour) — Yes 권장
3. □ Level pre-marked? (round number / Adam Mancini / AVWAP / OB)
4. □ 가격이 level 닿았나?
5. □ Reaction candle? (reversal bar / engulfing / pin bar)
6. □ Volume? 평균 × 1.2 이상?
7. □ R:R 1:1.5 이상 가능?
8. □ R30 cooldown clear?

→ 8개 중 6개 미만 = 진입 X
```

**진입 후**:
- SL = 5-10 NQ point (5m TF)
- 2분 timer (R31)
- 1분 → 1/2 partial 가능 (Volman 표준)
- Win 후 next entry size ≤ 직전 (R32)

---

## ⚠️ Scalping 주의사항

1. **Commission drag** — 사용자 L18 검증: scalp 수수료 잠식 37% vs trend 7%. 자주 거래 = 수수료 잠식 ↑.
2. **Sub-2min winner trap** — 위 §3 핵심. 짧은 win = pattern 신호, skill 신호 X.
3. **Rapid loss spiral** — 작은 SL × 자주 hit = 누적 큰 loss. R31 + R32 + R30 모두 적용 시에만 sustainable.
4. **사용자 본인 데이터** = 짧은 win 가능, but enforcement 안 되면 cascade 발생. 환경 강제 우선.

---

## 🔗 NotebookLM 후속 query

1. "Volman VTR 정의의 NQ 5분 차트 적용 — ATR threshold 정확한 값"
2. "Sub-2min winner 후 size lock 룰 (R32) 의 외부 source 검증"
3. "Hook pattern (Joe Ross) vs ICT OB — NQ scalp 적용 시 win rate 비교"

---

*Status: Phase 1C draft (6/6 카테고리 완료). 다음: HTML 통합*
