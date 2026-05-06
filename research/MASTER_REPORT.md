# NQ 5m 검증·연구 Master Report v1

> **Date**: 2026-05-06
> **Data**: NQ 5m FirstRateData 2016-01-03 ~ 2026-04-13 (10.3y, 723,457 bars)
> **Weighting (5 schemes)**: w_eq, **w_h2y (primary)**, w_h1y, last_2y, last_1y
> **Cost / slippage**: not yet applied (raw forward returns). 다음 라운드.
> **Total experiments**: 4 (Phase A) + 3 (Robustness) + 6 (Discovery D1-D6) + 3 (Phase B) = **16 검증**

---

## 📋 Executive Summary

### 통설 결과 (Phase A + B)

| # | 통설 | 데이터 결과 | 판정 |
|---|---|---|---|
| A1 | EMA 정배열 = LONG bias | d=+0.014 (5b), 24/48b 에서 small (+0.04) growing | 🔴 NOGO short window, 🟡 PARTIAL long |
| A2 | EMA20 1st touch best | 4th+ touch HR 더 높음 (모든 fwd window) | 🔴 **REVERSE** |
| A3 | Fib 38.2-61.8 sweet spot | +5pp vs 23.6 이전 (top buy) ✓, but deeper better | 🟡 PARTIAL (top buy 회피만 ✓) |
| A4 | ATR z high = momentum | range/ATR REVERSE, signed ret 다른 결과 (R2 추가 분석) | 🔴 NOGO original H1 |
| B1 | SR zone (touch≥3) > 단일 line | Δ -0.62pp (zone 약간 낮음) | 🔴 NOGO |
| B2 | BB 95% 가격 inside | NQ 5m 89.18% (fat tails) | 🔴 NOGO (95% rule deviates) |
| B4 | Multi-TF all-up bias | d=+0.03, last_2y Δ=0.20 ATR small | 🟡 PARTIAL |

### 발견된 진짜 Edge (Discovery D1-D6)

| # | 신호 | 효과 | N | 강도 |
|---|---|---|---|---|
| **D1-1** | KST 04 LONG (BURN_X 시간) | +0.21 ATR (24b) | 2,612 | ⭐⭐⭐ small |
| **D1-2** | KST 19 (pre-NY) LONG | +0.30 ATR (24b), +0.62 last_2y | 2,533 | ⭐⭐⭐⭐ NEW |
| **D1-3** | KST 14 (US lunch) LONG | +0.37 ATR (48b) | 2,632 | ⭐⭐⭐ medium |
| **D1-4** | KST 20-22 SHORT cluster | -0.15 ~ -0.45 ATR (24-48b) | each ~2,700 | ⭐⭐⭐⭐ |
| **D3** | ATR z squeeze_12 → expansion | +44% range over 48b | 26,088 | ⭐⭐⭐⭐ huge |
| **D4-1** | Bull strong body → 24b LONG | +0.16 ATR (last_2y +0.26) | 3,437 | ⭐⭐⭐ small |
| **D4-2** | Hammer (lower wick ≥50%) → 24b SHORT | -0.20 ATR (last_2y -0.38) | 4,551 | ⭐⭐⭐ REVERSE 통설 |
| **D5-1** | Monday LONG | +0.30 ATR (24b), **+0.63 (48b)** | 7,734 | ⭐⭐⭐⭐⭐ massive |
| **D5-2** | Tuesday SHORT | -0.19 (24b), -0.27 (48b) | 9,975 | ⭐⭐⭐⭐ |
| **D6-1** | KST 14 + Monday LONG | +0.62 ATR, d=+0.14 | 656 | ⭐⭐⭐⭐ confluence |
| **D6-2** | KST 21 + Tuesday SHORT | -0.48 ATR, d=-0.12 | 694 | ⭐⭐⭐⭐ confluence |
| **D6-3** | Squeeze_12 + Monday LONG | +0.49 ATR, d=+0.11 | 5,076 | ⭐⭐⭐⭐ big sample |
| **D6-4** | KST 04 + Squeeze_12 | -3.54 ATR SHORT, d=-0.85 LARGE | 80 | ⚠️ N small but extreme |

### 핵심 통찰

1. **NQ 5m ≠ 통설**. 외부 권위자 (Linda/Adam Grimes/Hougaard) 인용 대부분 NQ 5m 에서 unsupported.
2. **Continuation < Mean reversion** at short horizons. 장기 (24-48b) 에서 trend signal 발현.
3. **Time-of-day (KST hour) = single 가장 강한 factor**. EMA/Candle 보다 훨씬 큰 효과.
4. **Day of Week 거대**. Monday +0.63 ATR (48b) = Cohen's d 약 +0.08 single factor 최대.
5. **Squeeze→Expansion 진짜**. ATR z squeeze (12 bar) 후 forward range +44% (48b).
6. **Confluence > 단일 factor**. 2-factor 결합 시 d=0.10-0.15 (single 0.05-0.08 보다 2배).
7. **04:30 BURN_X edge has guard rails missing**: ATR z squeeze 시 SHORT 으로 reverse 가능 (N=80, d=-0.85).
8. **Bull/Bear strong body candle = continuation** (Steve Nison 통설 부분 confirmed).
9. **Hammer/Shooting Star = REVERSE 통설** (단순 wick ratio 만으로 측정 시).

---

## 1. Phase A — 통설 4 가설

### A1 — EMA 정배열 효과 (W2)

**H1**: 정배열 vs 역배열 fwd 5b ATR-norm return Cohen's d ≥ 0.15

**Result**:

| Scheme | mu(정) | mu(역) | d(정 vs 역) | CI95 |
|---|---|---|---|---|
| w_eq | +0.042 | +0.031 | +0.005 | - |
| **w_h2y** | +0.057 | +0.031 | **+0.014** | **[-0.021, +0.057]** |
| w_h1y | +0.060 | +0.017 | +0.025 | - |
| last_2y | +0.082 | +0.012 | +0.041 | - |
| last_1y | +0.046 | +0.028 | +0.011 | - |

**By regime (w_h2y)**:
- BEAR: d=+0.089 (small) ⭐
- CHOP: d=+0.022 (negligible)
- BULL: insufficient bear sub-group

**Robustness (R3) — fwd window별**:

| fwd | d_h2y | mu(정) | mu(역) |
|---|---|---|---|
| 1b | -0.010 | +0.020 | +0.031 |
| 3b | +0.022 | +0.049 | +0.012 |
| 5b | +0.014 | +0.056 | +0.031 |
| 12b | +0.014 | +0.047 | +0.001 |
| **24b** | **+0.036** | +0.109 | -0.056 |
| **48b** | **+0.042** | **+0.158** | **-0.119** |

→ **장기 hold 시 edge growing**: 48b (4시간) hold 시 정배열 mu=+0.158 vs 역배열 mu=-0.119. Δ ≈ 0.28 ATR.

**판정**: NOGO original (5b), **PARTIAL long-window (24-48b)** + BEAR regime.

### A2 — EMA20 touch # (W6)

**H1**: 1st touch HR ≥ 4th+ touch HR + 10pp

**Result**:

| Bin | N | w_h2y HR | w_h1y HR | last_2y HR | last_1y HR |
|---|---|---|---|---|---|
| 1st | 11,408 | 64.84% | 64.85% | 65.36% | 64.81% |
| 2nd | 5,857 | 65.01% | 65.23% | 64.89% | 66.92% |
| 3rd | 2,907 | 64.72% | 64.68% | 65.44% | 65.83% |
| **4th+** | 2,465 | **66.52%** | 67.41% | **68.90%** | **68.60%** |

**Δ (1st vs 4th+) by scheme**: -0.94 / **-1.68** / -2.56 / **-3.54** / **-3.79 pp**

**Robustness (R1) — fwd window별**:

| fwd | Δ_h2y pp | Δ_l2y pp |
|---|---|---|
| 6b | -0.41 | -0.94 |
| 12b | -1.68 | -3.54 |
| 24b | -2.58 | -3.71 |
| 48b | -2.09 | -1.99 |

→ 모든 fwd window 에서 4th+ > 1st. Robust REVERSE.

**판정**: 🔴 **REVERSE**. Linda Holy Grail / Adam Grimes paraphrase NQ 5m 에서 REJECTED. 4th+ touch hit rate 더 높음.

### A3 — Fib 38.2-61.8 Pullback (W8)

**H1**: 38.2-61.8% level HR > 23.6% AND > 78.6%, w_h2y +5pp

**Result (h2y HR)**:

| Bin | N | HR |
|---|---|---|
| <23.6% | 55,423 | 47.35% (낮음 ⭐ Top buy 회피 confirmed) |
| 23.6-38.2% | 40,537 | 53.29% |
| 38.2-50% | 23,950 | 55.29% |
| 50-61.8% | 17,381 | 57.65% |
| 61.8-78.6% | 15,613 | 59.91% |
| 78.6-100% | 10,059 | 60.38% |
| **>100% broken** | 7,820 | **62.65%** |

**Sweet (38.2-61.8) vs Extreme (<23.6 + 78.6+)**:
- w_h2y: +5.40pp ✓
- last_2y: +4.46pp ✓

**판정**: 🟡 **PARTIAL**.
- "Top buy 회피" (<23.6% 진입 47% HR 가장 낮음) = **CONFIRMED ✓**
- "78.6%+ 깊은 pullback 위험" = **REJECTED** (오히려 HR 가장 높음 62.65%)
- Monotonic: 깊을수록 HR 높음 → "deeper better" 가 더 정확한 룰

### A4 — ATR z momentum (W9)

**H1**: z >= +1.0 forward range/ATR ratio ≥ 1.30 vs baseline (-0.5..+0.5)

**Result (h2y)**:

| z bin | N | mu range/ATR (12b fwd) |
|---|---|---|
| z < -1 | 2,673 | 4.310 (highest) |
| -1 ≤ z < -0.5 | 9,085 | 4.207 |
| baseline | 10,776 | 3.934 |
| +0.5 ≤ z < +1 | 2,759 | 3.437 |
| +1 ≤ z < +2 | 2,887 | 3.341 |
| z ≥ +2 | 1,820 | 3.157 (lowest) |

ratio (high/base) = 0.831 (h2y), 0.820 (last_2y) → REVERSE.

**Robustness (R2) — signed return 다른 결과**:

fwd=48b signed return:
- z<-0.5: -0.169 ATR (DOWN drift)
- baseline: -0.011
- mid (+0.5..+1): +0.066
- **high (z≥+1): +0.174 ATR (UP drift)** ⭐

→ **range/ATR mean reverts** (low z → big range/ATR ratio, high z → small ratio)
→ **signed direction**: high z → LONG drift, low z → SHORT drift (long horizon)
→ Original H1 NOGO. 그러나 **directional bias 발견**: high z 장기 LONG / low z SHORT.

**판정**: 🔴 NOGO H1 (range ratio), 🟡 NEW finding (signed direction high z LONG bias).

---

## 2. Robustness (R1-R3)

### R1 — A2 EMA touch 다양한 forward window

| fwd | 1st HR (h2y) | 4th+ HR (h2y) | Δ pp |
|---|---|---|---|
| 6b | 51.41% | 51.82% | -0.41 |
| 12b | 64.84% | 66.52% | -1.68 |
| 24b | 75.88% | 78.46% | -2.58 |
| 48b | 83.11% | 85.20% | -2.09 |

→ ALL forward windows 4th+ > 1st. REVERSE robust.

### R2 — A4 ATR z signed forward return

(이미 위 A4 에 포함)

### R3 — A1 EMA alignment fwd window

(이미 위 A1 에 포함)

---

## 3. Discovery (D1-D6)

### D1 — Time-of-day (KST hour) 단일 가장 강한 factor

**Top |ret|/ATR (24b)**:

| KST hour | |ret|/ATR (h2y) | signed |
|---|---|---|
| 21 | 5.755 | -0.153 SHORT |
| 20 | 5.598 | -0.181 SHORT |
| **19** | **4.042** | **+0.301 LONG** ⭐⭐⭐ |
| 13/14 | 3.87 / 3.77 | neutral |

**Top signed (LONG bias) (24b)**:
- KST 19: +0.301 ATR ⭐⭐⭐
- KST 15: +0.213 ATR
- KST 04: +0.210 ATR (BURN_X)
- KST 03: +0.167 ATR

**Top signed (SHORT bias) (24b)**:
- KST 22: -0.286 ATR (BURN_R)
- KST 20: -0.181
- KST 21: -0.153

**At fwd=48b**:
- KST 14: +0.375 ATR LONG ⭐
- KST 11: +0.277
- KST 08: +0.291 (last_2y +0.380)
- KST 04: +0.161
- **KST 21: -0.507 SHORT (last_2y -0.743!) ⭐⭐⭐**
- **KST 20: -0.448 SHORT (last_2y -0.673!) ⭐⭐⭐**
- KST 22: -0.335

→ **NQ 5m 가장 강한 single-factor signal = KST hour**.

### D2 — Mean reversion / momentum

correlation past↔fwd = +0.006 ~ +0.018 across 모든 (past_n, fwd_n) 조합.
→ Single past N-bar return = no edge.
**부분 momentum 신호**: extreme up (past ≥ +1.5 ATR) → fwd 24b +0.23 ATR. 그러나 N=2,295 작음.

### D3 — Volatility expansion (squeeze → expansion) ⭐⭐⭐⭐

squeeze_12 (12 consecutive bars z < -0.5):

| fwd | range_squeeze / ATR | range_no_sq / ATR | Δ |
|---|---|---|---|
| 12b | 4.36 | 3.64 | **+20%** |
| 24b | 6.93 | 5.25 | **+32%** |
| 48b | 11.22 | 7.76 | **+44%** |

→ **Squeeze breakout 통설 confirmed (NQ 5m 데이터)**. Direction 은 약함 (signed 미미), but range 확실히 큼.

### D4 — Candle structure

| Pattern | fwd 24b signed (h2y) | last_2y |
|---|---|---|
| Bull strong body (≥0.7) | +0.156 LONG | +0.257 |
| Bear strong body | -0.085 (mild SHORT) | -0.155 |
| **Hammer** (lower wick ≥0.5) | **-0.200 SHORT** | -0.385 |
| **Shooting Star** | **+0.093 LONG** | +0.033 |
| Doji | -0.106 | -0.238 |

→ **Strong body = continuation 통설 confirmed** (small effect, but consistent).
→ **Hammer/Shooting Star REVERSE 통설** (Steve Nison 무 컨텍스트 적용 = REJECTED).

### D5 — Day of Week 거대 효과 ⭐⭐⭐⭐⭐

| Day | fwd 12b signed | fwd 24b | fwd 48b |
|---|---|---|---|
| **Mon** | +0.198 | **+0.299** | **+0.630** ⭐⭐⭐⭐⭐ |
| Tue | -0.024 | -0.193 | -0.266 |
| Wed | +0.098 | +0.106 | +0.211 |
| Thu | +0.007 | +0.011 | -0.087 |
| Fri | -0.065 | -0.082 | -0.189 |
| Sat (limited) | -0.008 | +0.184 | +0.163 |

→ **Monday LONG bias 단일 가장 큰 day effect**: +0.63 ATR 4시간 forward.
→ **Tue SHORT** vs Mon LONG = magnitude 0.9 ATR difference.

### D6 — Multi-factor confluence

**Top 5 ranked by |d_h2y|** (filtered N>=50):

| Rank | Signal | mu_h2y (24b) | d_h2y | N |
|---|---|---|---|---|
| 1 | Squeeze_12 + KST 04 (SHORT!) | -3.538 | -0.853 LARGE | 80 |
| 2 | KST 14 + Monday LONG | +0.619 | +0.138 small | 656 |
| 3 | KST 19 + Mon + bull_strong (3F) | +0.600 | +0.133 small | 80 |
| 4 | KST 21 + Tuesday SHORT | -0.478 | -0.124 small | 694 |
| 5 | Squeeze_12 + Monday LONG | +0.487 | +0.112 small | 5,076 |

→ **2-factor confluence d ≈ 0.10-0.15**, single factor d ≈ 0.05-0.08. Confluence 효과 ~2배.
→ **3-factor d ≈ 0.13-0.15** but N drops fast.

**Critical guard for v3.5 BURN_X**:
- 04:30 KST 가 squeeze_12 와 만나면 LONG bias **REVERSE → SHORT** (-3.54 ATR, d=-0.85)
- N=80 작지만 effect 매우 큼 → 추가 검증 권장
- 실용 룰: BURN_X 시 ATR z >= -0.3 (squeeze 아님) 만 LONG entry

---

## 4. Phase B (B1 + B2 + B4)

### B1 — SR zone vs single line

| Threshold | zone HR | line HR | Δ pp |
|---|---|---|---|
| MFE 0.5×ATR | 80.79% | 81.42% | -0.62 |
| MFE 1.0×ATR | 62.56% | 63.01% | -0.44 |

By zone touch count: touch ≥ 3 (80.79%) → ≥ 6 (77.80%) **decreasing**.

→ **B1 NOGO**: SR zone 통설 NQ 5m unsupported. 단일 line 과 거의 차이 X. "Strong SR = bigger reaction" REVERSE (touch 많을수록 hit 적음).

### B2 — BB(20,2σ) 95% rule

- Inside BB: **89.18%** (h2y) — 95% rule **DEVIATES** (NQ 5m fat tail)
- Above upper: 5.36% / Below lower: 5.47%
- Walking band:
  - After upper touch → fwd 12b signed = -0.087 (mild mean revert)
  - After lower touch → fwd 12b signed = -0.187 (continuation DOWN!)

→ **B2 NOGO**: 95% 통설 NQ 5m 에서 89% 만족. Lower touch 후 추가 하락 (long-term bear?).

### B4 — Multi-TF alignment (5m + 15m + 1h)

| fwd | mu(all-up) h2y | mu(all-down) h2y | d_h2y |
|---|---|---|---|
| 12b | +0.026 | -0.050 | +0.025 |
| 24b | +0.079 | -0.061 | +0.032 |

last_2y at 24b: mu(up)=+0.080, mu(down)=-0.118 → Δ=0.20 ATR (small effect, real signal).

→ **B4 PARTIAL**: 작은 effect (d=0.03), but real bias.

---

## 5. 자료 개요 v2 영향

### Verified (T1 — direct backtest)

| 컨셉 | 데이터 결과 | 교재 활용 |
|---|---|---|
| Top buying 회피 (W8) | <23.6% pullback HR=47% (가장 낮음) | ✓ 룰 유지 |
| Squeeze → Expansion (W5) | +44% range fwd 48b | ✓ 룰 유지 (W5 BB → ATR z 결합) |
| Strong body continuation (W7) | Δμ ~0.24 ATR fwd 24b | ✓ 룰 유지 |
| Multi-TF all-up (W1) | small effect d=0.03, real | ✓ confluence 룰 |
| 04:30 BURN_X (W11) | KST 04 +0.21 ATR confirmed | ✓ +ATR z guard 추가 |
| 22:30 BURN_R (W12) | KST 22 -0.29 (SHORT direction confirm) | ✓ direction-specific 룰 |

### REJECTED (NOGO/REVERSE) — 요약만

| 통설 | 결과 | 처리 |
|---|---|---|
| EMA 정배열 = 90% LONG (W2) | d=0.014 short window | "long hold 시만 effect" 1줄 + 삭제 |
| EMA20 1st touch best (W6) | 4th+ HR 더 높음 | "REVERSE 통설" 1줄, 룰 reverse |
| Fib 38.2-61.8 sweet (W8) | deeper better | "23.6 회피만 ✓" 유지, 78.6+ skip rule 삭제 |
| ATR z high momentum (W9) | range REVERSE, signed LONG bias | reframe — directional only |
| SR zone (touch≥3) > line (W3) | Δ=-0.62pp | "zone vs line edge X" 1줄 |
| BB 95% rule | NQ 5m 89% | "fat tail" 1줄 |
| Hammer/Shooting Star reversal (W7) | REVERSE | "context 없으면 reverse 통설" |
| Linda Holy Grail (W6) | ADR-028 + A2 둘 다 REJECTED | 완전 삭제 |

### NEW Edge — Discovery 기반 추가

| 신규 룰 | 데이터 |
|---|---|
| **W4 NEW**: KST 19 LONG (pre-NY) | +0.30 ATR (24b), last_2y +0.62 |
| **W4 NEW**: KST 14 LONG (US lunch break) | +0.37 ATR (48b) |
| **W4 NEW**: KST 20-21 SHORT cluster | -0.45 ~ -0.51 ATR (48b) |
| **NEW Day-of-Week 룰**: Monday LONG bias | +0.63 ATR (48b) |
| **NEW Day-of-Week 룰**: Tuesday SHORT | -0.27 ATR (48b) |
| **W11 GUARD**: BURN_X 시 ATR z squeeze → SKIP (or reverse) | -3.54 ATR if squeeze |
| **NEW Confluence**: KST 14 + Mon | +0.62 ATR, d=+0.14 |
| **NEW Confluence**: KST 21 + Tue | -0.48 ATR, d=-0.12 |

---

## 6. Limitations / Caveats

1. **Cost not applied**: forward returns 은 raw. Commission $2.18 RT + slippage 차감 시 effect size 50-70% 감소 예상.
2. **Direction baseline 낮음**: Cohen's d 대부분 <0.15 (small). 단일 룰로 trade 어려움. 결합 (confluence) 필수.
3. **Sample size variance**: KST 04 + Squeeze_12 N=80 — 추가 검증 권장.
4. **Forward window 의존성**: 5b vs 24b vs 48b 결과 다름. Hold time 명시 필요.
5. **Regime conditioning** 부족: BULL/BEAR/CHOP 별 stratification 더 필요.
6. **Path-sim 단순**: SL hit 시점 close-only base, intra-bar 정확도 한계.
7. **DST handling**: NY → KST conversion 시 일부 NaT (5h KST 9k bars 누락).
8. **EMA20 indicator** = 5m 만. 15m/1h Multi-TF 계산은 5m 데이터에서 EMA span 곱하기 (정확 X).

---

## 7. 다음 라운드 권장

### 즉시 가능 (Phase B+)
- **B5 정밀**: 04:30 BURN_X 에 ATR z guard 추가 후 Sharpe 재측정 (full backtest)
- **B6**: KST 19 / 14 / Mon 신규 edge sim 적용 가능성
- **B7**: Cost / slippage 적용 후 effect size 재산정

### 자료 개요 직진
- 검증 결과 만으로 v2 outline 충분 — 위 표 그대로 적용

### 추가 깊이 (선택)
- 1m TF 검증 (5m 결과 robustness)
- Regime breakdown (D6 confluence × BULL/BEAR/CHOP)
- Walk-forward (2016-2018 / 2019-2021 / 2022+ split)

---

## 📁 산출물 구조

```
research/
├── _lib/                       (재사용 라이브러리)
│   ├── data_loader.py
│   ├── weighting.py            (5 schemes, ln(2)/half_life)
│   ├── stats.py                (Cohen's d, judge_phase_a)
│   ├── indicators.py           (EMA / ATR / Bollinger)
│   └── path_sim.py             (forward MFE/MAE, SL-first)
├── A1_ema_alignment.py         + results/A1_ema_alignment/results.json
├── A2_ema20_touch.py           + results/A2_ema20_touch/results.json
├── A3_fib_pullback.py          + results/A3_fib_pullback/results.json
├── A4_atr_zscore.py            + results/A4_atr_zscore/results.json
├── R_robustness.py             + results/R_robustness/results.json
├── D1_time_of_day.py           + results/D1_time_of_day/results.json
├── D2to5_batch.py              + results/D2_mean_reversion + D3_vol_expansion + D4_candle_structure + D5_dow
├── D6_confluence.py            + results/D6_confluence/results.json
├── B_batch.py                  + results/B1_sr_zone_vs_line + B2_bb_check + B4_multi_tf
├── PHASE_A_REPORT.md           (Phase A 단독)
└── MASTER_REPORT.md            (이 파일 — 전체 종합)
```

전체 raw 수치는 각 results.json 보존. 재현/추가 분석 가능.
