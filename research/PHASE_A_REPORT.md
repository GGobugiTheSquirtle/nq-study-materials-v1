# Phase A — 4 hypotheses 종합 보고

> **Date**: 2026-05-06
> **Data**: NQ 5m FirstRateData 2016-01-03 ~ 2026-04-13 (10.3y, 723k bars)
> **Weighting**: 5 schemes (w_eq, w_h2y primary, w_h1y, last_2y, last_1y)
> **User policy**: 너무 보수적 X — 효과 크기 + 방향성 중심
> **NOGO 처리**: REJECTED 후 요약만

---

## 결과 매트릭스

| # | 가설 | W | 판정 | Primary metric (w_h2y) |
|---|---|---|---|---|
| **A1** | EMA 정배열 (정/혼/역) → forward 5-bar return | W2 | 🔴 **NOGO** | Cohen's d = +0.014 (negligible) |
| **A2** | EMA20 1st touch > 4th+ touch hit rate | W6 | 🟠 **REVERSE** | Δ = -1.68pp (1st < 4th+) |
| **A3** | Fib 38.2-61.8% pullback > 양 극단 hit rate | W8 | 🟡 **PARTIAL** | Δ = +5.40pp (단, monotonic) |
| **A4** | ATR z >= +1.0 → forward range/ATR ratio ≥ 1.30 | W9 | 🔴 **NOGO** | ratio = 0.831 (mean revert) |

---

## A1 — EMA 정배열 효과 (REJECTED)

### Result table (Cohen's d)

| Scheme | mu(정) | mu(혼) | mu(역) | d(정 vs 역) |
|---|---|---|---|---|
| w_eq | +0.042 | +0.020 | +0.031 | +0.005 |
| **w_h2y** | +0.057 | +0.013 | +0.031 | **+0.014** |
| w_h1y | +0.060 | +0.001 | +0.017 | +0.025 |
| last_2y | +0.082 | -0.021 | +0.012 | +0.041 |
| last_1y | +0.046 | +0.037 | +0.028 | +0.011 |

Bootstrap CI95 (w_h2y, n=500): **[-0.021, +0.057]** → 0 포함, 통계적 유의 X.

### Regime breakdown (w_h2y)

| Regime | N | mu(정) | mu(역) | d |
|---|---|---|---|---|
| BULL | 6,344 | (insufficient bear N=24) | - | - |
| **BEAR** | 4,698 | +0.294 | +0.075 | **+0.089** small |
| CHOP | 18,958 | +0.044 | +0.008 | +0.022 |

### Conclusion
**"EMA 정배열 = LONG bias 90% 자격" 통설 REJECTED for NQ 5m forward 25-min return**.
- 단, BEAR regime 에서 small effect (d=0.089) 발현
- BULL regime 은 거의 모든 bar 가 정배열 → 비교 불가
- last_2y 에서 약간 강해짐 (d=0.041) — 최근 약한 trend 확인
- **교재 영향**: W2 markdown 의 "정배열 + Price > EMA20 = 90% LONG 진입 자격" 인용 → **삭제 또는 "BEAR regime 만" 으로 한정**

---

## A2 — EMA20 touch # (REVERSED!)

### Hit rate (MFE >= 1×ATR within 12 bars)

| Bin | N | w_h2y | w_h1y | last_2y | last_1y |
|---|---|---|---|---|---|
| **1st** | 11,408 | 64.84% | 64.85% | 65.36% | 64.81% |
| 2nd | 5,857 | 65.01% | 65.23% | 64.89% | 66.92% |
| 3rd | 2,907 | 64.72% | 64.68% | 65.44% | 65.83% |
| **4th+** | 2,465 | **66.52%** | 67.41% | **68.90%** | **68.60%** |

### Δ (1st vs 4th+)
| Scheme | Δ pp |
|---|---|
| w_eq | -0.94 |
| w_h2y | **-1.68** |
| w_h1y | -2.56 |
| last_2y | -3.54 |
| last_1y | **-3.79** |

### Conclusion
**"EMA20 1st touch = best, 4th+ touch = 회피" 통설 NQ 5m 에서 REVERSE**.
- 4th+ touch hit rate **더 높음** (68.6% in last_1y vs 64.8% 1st)
- 가능 해석: 4th+ 까지 살아남은 trend = strong continuation
- Linda "Holy Grail" / Adam Grimes paraphrase → **NOT supported by NQ 5m**
- **교재 영향**: W6 markdown 의 "first/second touch only" 룰 → **삭제 또는 reverse**

---

## A3 — Fib pullback (PARTIAL, 그러나 traditional theory 부분 REJECTED)

### Hit rate (MFE >= 1×ATR within 12 bars)

| Bin | N | w_h2y | last_2y |
|---|---|---|---|
| <23.6% | 55,423 | 47.35% | 48.39% |
| 23.6-38.2% | 40,537 | 53.29% | 54.39% |
| 38.2-50% | 23,950 | 55.29% | 55.63% |
| 50-61.8% | 17,381 | 57.65% | 57.14% |
| 61.8-78.6% | 15,613 | 59.91% | 60.21% |
| 78.6-100% | 10,059 | 60.38% | 60.87% |
| **>100% broken** | 7,820 | **62.65%** | **62.19%** |

### "Sweet spot" (38.2-61.8%) vs "Extreme" (<23.6 + 78.6+) Δ
| Scheme | Δ pp |
|---|---|
| w_eq | +5.69 |
| **w_h2y** | **+5.40** |
| w_h1y | +5.17 |
| last_2y | +4.46 |
| last_1y | +3.42 |

### Conclusion
**부분 GO**: Fib 38.2-61.8 sweet spot exists (+5pp).
**부분 REJECT**: 그러나 monotonic — 깊은 pullback (78.6%+) hit rate **더 높음**.
- 통설 "Top buying = 23.6% 이전 진입은 위험" 데이터로 confirmed (47% hit rate, 가장 낮음)
- 통설 "78.6% 이상 = 추세 전환 위험" → REJECTED (실제로 hit rate 가장 높음)
- "Deeper pullback better" 가 더 정확
- **교재 영향**: W8 markdown 의 "fib 23.6%는 너무 얕고 78.6%는 너무 깊음" → **23.6 부분만 유지, 78.6+ 깊이 회피 룰 삭제**
- **사용자 약점 처방 강화**: Top buy (23.6% 이전 = 사실상 신고가 직진입) 회피는 **데이터로 검증 ✓**

---

## A4 — ATR z momentum (REJECTED)

### Forward range / current ATR ratio

| z bin | N | w_h2y | last_2y |
|---|---|---|---|
| **z < -1** | 2,673 | **4.310** | **4.202** |
| -1 ≤ z < -0.5 | 9,085 | 4.207 | 4.142 |
| -0.5 ≤ z < +0.5 | 10,776 | 3.934 | 3.967 |
| +0.5 ≤ z < +1.0 | 2,759 | 3.437 | 3.462 |
| +1.0 ≤ z < +2.0 | 2,887 | 3.341 | 3.368 |
| **z ≥ +2.0** | 1,820 | **3.157** | **3.104** |

### High vs Baseline ratio
| Scheme | ratio (high/base) | Δ |
|---|---|---|
| w_eq | 0.844 | -0.606 |
| **w_h2y** | **0.831** | -0.665 |
| last_2y | 0.820 | -0.714 |

### Conclusion
**REJECTED + REVERSE**: ATR z 와 forward range/ATR 가 **역상관** (mean reversion).
- z 높을수록 forward range / current ATR 작아짐
- Volatility mean reversion in NQ 5m
- **그러나** 절대 forward range = current ATR × ratio 이므로, z 높을 때 절대 range 는 여전히 큼 (예: ATR=20×3.16 = 63 vs ATR=8×4.31 = 34)
- 의미: stop 을 current ATR 기반 설정 시, z 높으면 reward 비율 상대적 작음
- **교재 영향**: W9 markdown 의 "z >= +0.5 = 진입 OK, z < -0.5 = 진입 자제" → **REVERSE!**
  - 데이터 base: z < 0 (저변동) 이 forward range/ATR 로 더 efficient
  - 단, 절대 movement 는 z 높을 때 여전히 큼 — 사용자 의도 ("순발력으로 매매") 와 결이 맞음
  - W9 결론 재구성: "ATR z 값 = setup quality 가 아니라, **stop/TP normalization** 용"

---

## 종합 통찰 (Cross-hypothesis)

### 1. NQ 5m ≠ traditional indicator wisdom

4 가설 중 3 개에서 통설 REJECTED 또는 REVERSE. 이유 추정:
- NQ 5m 은 짧은 timeframe → noise dominates over trend signal
- Index futures = mean-reverting tendency strong (vs 자유로운 commodity)
- 외부 권위자 (Linda/Grimes/Hougaard) 들은 다른 자산/timeframe 에서 검증

### 2. "Continuation" 보다 "Mean reversion" 신호 강함

- A2: 4th+ touch (continuation 의도) > 1st touch
- A3: 깊은 pullback (mean revert 의도) > 얕은
- A4: 저 vol → forward range/ATR 큼 (expansion expected)

→ NQ 5m 은 **반대로 쳐야** 하는 시장 (단기적). User v3.5 가 "BURN" 이라고 명명한 것도 일종의 reversal 진입 = 데이터와 일치.

### 3. Cohen's d 작음 — single-factor signal 약함

- 모든 가설에서 d < 0.10 (negligible) 또는 d ~ 0.10 small
- 결합 (regime × time × pattern) 이 필요
- 우리 v3.5 가 BURN_X (시간 + EMA + ATR) 결합으로 Sharpe 4.38 — 단일 factor 보다 결합이 답

### 4. 사용자 약점 매핑 재검증

| 약점 | 기존 처방 | 데이터 검증 결과 |
|---|---|---|
| Top buying L5 | "Pullback fib 38.2-61.8" | ✓ 부분 confirmed (23.6% 이전 hit rate 47% 최저) |
| 희망적 추세 L41 | "EMA 정배열 확인 후 LONG" | ❌ unsupported (5-bar forward d=0.014) |
| FOMO L4 | "ATR z low → 진입 lock" | ❌ REVERSED (오히려 low z 가 expansion 잠재력) |
| 짤짤이 후 욕심 L41 | "ATR z high → 진입 OK" | ❌ ratio < 1, normalize 시 비효율 |

→ **W2 / W6 / W9 룰들 거의 모두 재구성 필요**. W8 (Fib pullback) 는 부분 유지.

---

## Phase B 권장 (다음 단계)

추가 검증 가설:
- **B1** SR zone vs line MFE hit rate (W3) — 사용자 차트 시각 vs 측정
- **B2** BB(20,2σ) NQ 5m 95% rule 실측 (W5)
- **B3** Engulfing + SR confluence vs alone (W7)
- **B4** Multi-timeframe 일치 (W1) — 5m + 15m + 1h all-up
- **B5 NEW**: **Time-of-day × pattern** 결합 — 04:30 KST + EMA20 touch hit rate (W11 강화)

→ 사용자 결정: B1-B4 진행 OR B5 우선?

---

## 자료 개요 영향 (Phase 5 입력)

12주 커리큘럼 재배치 권장:

| Week | 기존 | 검증 후 |
|---|---|---|
| W2 EMA 정배열 | T5 권위 | **T1** REJECTED 명시 + BEAR regime 한정 |
| W6 EMA touch # | T5 권위 (Linda HG) | **T1** REVERSE 명시 (Linda HG NQ 5m REJECTED) |
| W8 Fib Pullback | T5 권위 | **T1** PARTIAL (23.6 회피 confirmed, 78.6+ 회피 REJECTED) |
| W9 ATR z momentum | T5 권위 | **T1** REJECTED + reframe (normalization 용도만) |
| W4/W11/W12 | T1 ✓ | T1 유지 (이미 검증) |
| W10 ICT | T1 ✓ (BTC) | NQ replication B5 추가 |

Phase B 결과 + 본 Phase A → **Phase 5 자료 개요 작성**. NOGO/REVERSE 룰들은 "REJECTED 1줄 요약 + 학습 가치만" 처리 (사용자 정책).
