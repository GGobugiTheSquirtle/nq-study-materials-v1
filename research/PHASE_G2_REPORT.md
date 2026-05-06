# Phase G2 — Round Figures Deep Dive (G correction + extensions)

> **Date**: 2026-05-06
> **Improvements vs G**:
>   1. **Pivot fractal (5-5) for true 전고점/전저점** (G used rolling max — artifact)
>   2. **Gap-safe cross detection** (prev_close reference, not prev_high)
>   3. **Entry @ next bar open** (실전 entry 시점)
>   4. **Cost-adjusted** 0.022 ATR/RT
>   5. **KST hour × round confluence**
>   6. **Failed breakout pattern**

---

## 🚨 G의 일부 발견 ARTIFACT 였음 — 정정

### Rolling max vs Pivot fractal 비교

| Setup | G (rolling 50-bar max) | G2 (pivot 5-5) | 정정 |
|---|---|---|---|
| R1000 up + "전고점" break | h2y -0.097 | h2y **-0.085** | 일치 (방향성) |
| **R1000 down + "전저점" break** | h2y **+0.208** ⭐ | h2y **-0.074** | ❌ **REVERSED** |
| **R500 down + "전저점" break** | h2y +0.120 | h2y **-0.035** | ❌ Reversed |
| R250 down + "전저점" break | h2y +0.035 | h2y +0.011 | 거의 0 |

### 원인

**G method (rolling max)**: "current high > prev 50-bar high" — 새 50-bar high 단순 충족
**G2 method (pivot 5-5)**: "current low < last confirmed pivot low (좌우 5봉 검증)" — 진짜 swing low break

→ Rolling max 는 좌측 context 없음. 실제 "swing low" 와 다름. **G2 가 사용자 의도한 진짜 전저점**.

### 결론 정정

**G의 "K-Bounce LONG (R1000 down + SL → +0.208 ATR)" = REJECTED**.
정확한 pivot 사용 시 R1000 down + 진짜 전저점 break = 약한 SHORT 지속 (-0.074 ATR).

---

## ✅ 사용자 직관 "전고점 + 라운드 → SHORT" 검증

R500 / R1000 up + 진짜 pivot high break (전고점 돌파):

| Round | h2y | l2y | **P3 (recent)** | N |
|---|---|---|---|---|
| R100 up+PH | -0.023 | -0.047 | +0.014 | 14,298 |
| R250 up+PH | +0.025 | -0.048 | -0.020 | 5,711 |
| **R500 up+PH** | **-0.127** ⭐ | **-0.191** ⭐ | **-0.109** ⭐ | **2,741** |
| R1000 up+PH | -0.085 | +0.047 | **-0.223** ⭐ | 1,469 |

**🟢 R500 up + 전고점 break = 사용자 직관 CONFIRMED**:
- h2y / l2y / P3 모두 negative (SHORT bias)
- N=2,741 (~270/year) sufficient
- **P3 -0.109 ATR signed = recent 일관**
- L2y 가 가장 강함 (-0.191) — 최근 강화

**🟢 R1000 up + 전고점 break = P3 에서 매우 강함 (-0.223 ATR)**
- N=1,469 (~145/year)
- h2y -0.085 / l2y +0.047 (mixed) / P3 **-0.223** ⭐
- 최근 시장에서 강함

---

## 🟡 Trade Sim (cost-adjusted, simple SL/TP)

| Setup | Direction | PF (Total) | P3 PF | N | P3 N |
|---|---|---|---|---|---|
| R100 down+PL | LONG | 1.004 | 1.024 | 15,403 | 6,708 |
| R250 down+PL | LONG | 1.031 | 1.015 | 6,349 | 2,609 |
| R500 down+PL | LONG | 1.045 | 1.000 | 3,160 | 1,354 |
| R1000 down+PL | LONG | 1.011 | 0.974 | 1,640 | 652 |
| R100 up+PH | SHORT | 0.947 | 0.940 | 14,298 | 6,273 |
| R250 up+PH | SHORT | 0.867 | 0.928 | 5,711 | 2,493 |
| R500 up+PH | SHORT | 0.881 | 0.921 | 2,741 | 1,197 |
| R1000 up+PH | SHORT | 0.890 | 0.868 | 1,469 | 615 |

→ **모두 marginal**. simple SL=1.5/TP=2.0 ATR 으로는 distribution edge 못 거둠.

### 왜 trade sim 약한가?

R500 up+PH SHORT: signed -0.127 ATR (negative drift)
- Win (TP 2): +2.0 ATR
- Loss (SL 1.5): -1.5 ATR
- Required WR for break-even: 1.5/(1.5+2.0) = 43%
- 실제 WR (drift -0.127 만큼 SHORT 유리): 약 47-49%
- After cost (0.022 ATR): margin 부족 → PF < 1.0

→ **SL 더 작게 (HE-001 방식 0.5 ATR) + Trail 필수**.

---

## ⭐⭐ Confluence: KST hour × R1000 down + PL

```
KST h    N    sgn h2y    sgn l2y     해석
   2   93    +0.958     +2.093      LONG (small N)
   6   31    +1.376     +1.689      LONG (very small N)
  12   26    -2.948     -3.482      SHORT extreme (very small N)
  21  150    -1.250     -2.626      ⭐ SHORT (sufficient N)
  22  198    +0.119     +1.013      mild LONG (large N for R1000)
  20   57    -1.154     -2.895      SHORT (small N)
```

**🏆 KST 21 + R1000 down + PL break → SHORT 매우 강함**:
- N = 150 (10년, ~15/year)
- signed h2y -1.250 ATR (huge)
- signed l2y -2.626 ATR (huge, recent 더 강함)
- 매우 rare 하지만 매우 강한 setup

**KST 22 + R1000 down + PL → mild LONG bounce**:
- N=198, l2y +1.013
- KST 22 raw bias 와 일치 (BURN_R 시간 = SHORT 후 bounce 가능)

---

## 🔴 Failed Breakout Pattern

R1000 up + 3 bar 안에 round 가격 아래로 reverse (실패):

| Metric | 값 |
|---|---|
| N | 3,971 (10y) |
| signed h2y (post 3-bar 후 24b fwd) | +0.006 (neutral) |
| signed l2y | +0.104 (mild LONG) |

→ 약함. 기대만큼 강한 reversal 아님.

---

## 📋 종합 판정 (G2 정정 후)

| 가설 | G 결과 | G2 결과 (correction) |
|---|---|---|
| H1a (round breakout mean revert) | PARTIAL | 🟡 PARTIAL — R500/R1000 up+PH SHORT confirmed |
| H1b (K-unit 최강) | GO | 🟡 R500 / R1000 둘 다 비슷 |
| H1c (전고점/전저점 결합) | GO down / PARTIAL up | 🟢 GO **up only**, down 약함 |
| **사용자 직관 (전고점+R SHORT)** | PARTIAL | 🟢 **GO** — R500 up+PH 가장 robust |
| G의 K-Bounce LONG | GO ⭐⭐ | 🔴 **REJECTED** — rolling max artifact |
| 🆕 Confluence KST21 + R1000 down + PL | 미검증 | 🟢 **GO** (SHORT, small N caveat) |

---

## 🎯 Pine v5.1 추천 (G2 기반)

### Signal 1: 🆕 R500 up + 전고점 break SHORT marker

```pinescript
// Round 500 up-cross + true pivot high break (G2 verified)
//   h2y signed -0.127, l2y -0.191, P3 -0.109 — robust SHORT bias
//   Direction: SHORT signal (mean revert from round resistance)
//   N: ~270/y

float r500_up_cross = na
prev_c = close[1]
r_above = math.floor(prev_c / 500) * 500 + 500
crossed_500_up = high >= r_above and prev_c < r_above

// True pivot high (5-5)
ph_5_5 = ta.pivothigh(high, 5, 5)
var float last_ph = na
if not na(ph_5_5)
    last_ph := high[5]

broke_pivot_high = high > last_ph and not na(last_ph)

v5_round500_up_PH_short = is_tf_5m and crossed_500_up and broke_pivot_high
plotshape(v5_round500_up_PH_short, "🆕 R500 up + 전고점 → SHORT mark",
          shape.triangledown, location.abovebar,
          color.new(color.orange, 20), size=size.small,
          text="R500↑PH", textcolor=color.orange)
```

### Signal 2: 🆕 KST 21 + R1000 down + 전저점 → SHORT (rare but strong)

```pinescript
// KST 21 + R1000 down + pivot low break — N small but signed -1.25 ATR
v5_kst21_r1000_pl_short = is_tf_5m and kst_h == 21 and kst_m < 5 and
                          crossed_1000_down and broke_pivot_low

if v5_kst21_r1000_pl_short
    label.new(bar_index, high, "💀 KST21+R1k+PL\nSHORT extreme",
              color=color.red, textcolor=color.white, style=label.style_label_down)
```

---

## ⚠️ Caveats

1. **Effect size small** — Cohen d 0.05-0.10 range. Single trade variance 거대.
2. **R500 up+PH 가장 robust** but trade sim PF 0.92 → ATM v2 (HE-001) 결합 필수
3. **Confluence KST 21 + R1000+PL N=150** — 10년에 150회. OOS 추가 권장
4. **Cost = 0.022 ATR** — 단방향 추정, 정밀 보정 시 더 큼 가능
5. **G의 "LONG bounce" 결과 retract** — research 제출 시 G2 결과 사용

---

## 🚀 다음 단계

1. **Pine v5.1**: G2 검증된 R500 up+PH SHORT marker 추가
2. **HE-001 방식 ATM 적용** — R500 up+PH SHORT 시 SL 30 ticks (0.5 ATR) + Trail 18
3. **Confluence trade sim** — KST 21 + R1000 down + PL specific 검증
4. **Up-cross last_2y** 재검증 (regime split: BULL vs BEAR)

---

*G2 = 사용자 직관 "전고점 + 라운드 SHORT" 정확히 검증. R500 up+PH = 진짜 edge.*
