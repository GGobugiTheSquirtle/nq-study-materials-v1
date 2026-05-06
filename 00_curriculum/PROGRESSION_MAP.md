# Progression Map — 12주 스킬 트리

> 매주 자가 점검 후 ⬜ → ✅ 또는 🟡(in progress). 4점 미만은 1주 연장.
>
> **마지막 갱신**: 2026-05-06 (시작)

---

## 🌳 Skill Tree (Top-down)

```
                    [LIVE EXECUTION]
                          ▲
                          │
                ┌─────────┴─────────┐
                │  Tier 4: Mastery  │
                │  (Month 4+, 모라토리엄 해제 후) │
                └─────────▲─────────┘
                          │
        ┌─────────────────┴─────────────────┐
        │  Tier 3: Research Integration     │
        │  (W9-W12, Month 3)                │
        ├───────────────────────────────────┤
        │  W9  ⬜ Momentum vs 횡보           │
        │  W10 ⬜ ICT FVG/OB 인식 (사용 X)   │
        │  W11 ⬜ 04:30 BURN_X (우리 edge)   │
        │  W12 ⬜ 22:30 BURN_R + Regime A/B │
        └─────────────────▲─────────────────┘
                          │
        ┌─────────────────┴─────────────────┐
        │  Tier 2: Setup Building           │
        │  (W5-W8, Month 2)                 │
        ├───────────────────────────────────┤
        │  W5  ⬜ Bollinger Band             │
        │  W6  ⬜ MA as Dynamic SR           │
        │  W7  ⬜ PA Candle Patterns         │
        │  W8  ⬜ Pullback vs Top Buy        │
        └─────────────────▲─────────────────┘
                          │
        ┌─────────────────┴─────────────────┐
        │  Tier 1: Foundation               │
        │  (W1-W4, Month 1) ⭐ START HERE    │
        ├───────────────────────────────────┤
        │  W1  ⬜ 추세 인식 (HH/HL/LL/LH)   │
        │  W2  ⬜ EMA 정·역배열              │
        │  W3  ⬜ 지지·저항 zone             │
        │  W4  ⬜ 매매 시간대                │
        └───────────────────────────────────┘
```

**현재 위치**: 🚦 W0 (시작 전, 2026-05-06)

---

## 📋 Week-by-Week 상세

### Tier 1 — Foundation

#### W1: 추세 인식 (Trend Recognition) ⬜

**핵심 질문**: "지금 차트는 Up / Down / Range 중 무엇인가?"

| 항목 | 내용 |
|---|---|
| 학습 주제 | Higher High/Higher Low (uptrend), Lower High/Lower Low (downtrend), Range |
| 차트 식별 도구 | Swing point (좌우 5캔들) 으로 HH/HL 마킹 |
| 일지 추가 | `trend_w1`: "uptrend / downtrend / range / unclear" |
| 성공 기준 | 차트 5개에서 4개 이상 정확 (80%) |
| 매핑 약점 | L4 FOMO, L5 top buying — 추세 정의를 모르면 hopeful trend |

#### W2: EMA 정·역배열 ⬜

**핵심 질문**: "EMA 20/50/200 어떤 순서인가?"

| 항목 | 내용 |
|---|---|
| 학습 주제 | EMA 20 > 50 > 200 = 정배열 (강세) / 역배열 (약세) / 혼합 (전환) |
| 차트 식별 도구 | TV 차트에 EMA 20 (yellow) / 50 (orange) / 200 (red) overlay |
| 일지 추가 | `ma_alignment_w2`: "정 / 혼 / 역" |
| 성공 기준 | 차트 5개 중 4개 정확 (80%) |
| 매핑 약점 | hopeful trend — 정배열 아닌데 LONG = 진입 금지 룰 형성 |

#### W3: 지지·저항 zone ⬜

**핵심 질문**: "현재가 가장 가까운 valid SR zone 의 near edge 까지 거리는?"

| 항목 | 내용 |
|---|---|
| 학습 주제 | SR = zone (선 X). Touch ≥ 3, ±0.25×ATR. Pivot 클러스터 / POC / 전고/전저 |
| 차트 식별 도구 | 자동 pivot mark + 직접 zone box 그리기 |
| 일지 추가 | `sr_distance_w3`: "0.4×ATR (resistance) / 1.2×ATR (support) / clear" |
| 성공 기준 | 차트 5개 중 4개 zone 식별 (80%) + 진입 시 SR 거리 마킹 100% |
| 매핑 약점 | top buying — resistance zone 가까운데 LONG = 진입 금지 |

#### W4: 매매 시간대 (Session Timing) ⬜

**핵심 질문**: "지금 어느 세션? Edge time 인가?"

| 항목 | 내용 |
|---|---|
| 학습 주제 | KST 기준: Asian (07-15) / EU 진입 (15-22) / NY-AM (22:30-01:00) / NY-PM (01-04) / Overnight |
| 차트 식별 도구 | 시간대 vertical line + edge time hot zone (04:30 BURN_X 등) |
| 일지 추가 | `session_w4`: "asian / eu / ny-am / 0430 / overnight" |
| 성공 기준 | 진입 시점 매번 세션 마킹 100% + edge time 외 무리한 진입 0회 |
| 매핑 약점 | "심심해서 진입" — empty chart anxiety 처방 |

---

### Tier 2 — Setup Building

#### W5: Bollinger Band ⬜

**핵심 질문**: "현재 BB 위치? Squeeze 인가 Expansion 인가?"

| 항목 | 내용 |
|---|---|
| 학습 주제 | BB(20, 2σ) 상하단 = mean revert zone. Squeeze (BBW < hist 20%) = breakout 대기 |
| 차트 식별 도구 | BB overlay + BBW indicator |
| 일지 추가 | `bb_state_w5`: "upper-touch / mid / lower-touch / squeeze / expansion" |
| 성공 기준 | BB squeeze → expansion 전환 식별 80% |
| 매핑 약점 | range 에서 LONG/SHORT 양쪽 욕심 — BB 룰로 일방향만 |

#### W6: EMA as Dynamic SR ⬜

**핵심 질문**: "EMA20/50 dynamic SR 작동 중인가?"

| 항목 | 내용 |
|---|---|
| 학습 주제 | 정배열 + EMA20 위에서 거래 = EMA20 = dynamic support. Pullback target |
| 차트 식별 도구 | EMA20 touch count (최근 N봉) |
| 일지 추가 | `ema_test_w6`: "EMA20 ride / EMA50 hold / break / N/A" |
| 성공 기준 | EMA20 pullback 진입 vs random 진입 구분 정확 |
| 매핑 약점 | "추세 가기 전에 진입" → EMA20 retest 후만 |

#### W7: PA Candle Patterns ⬜

**핵심 질문**: "Engulf / Pin / Inside 식별 가능한가?"

| 항목 | 내용 |
|---|---|
| 학습 주제 | Bullish/Bearish Engulfing, Pin Bar, Inside Bar (Al Brooks/Volman 정의) |
| 차트 식별 도구 | 캔들 직접 마킹 (post-hoc) + live spotting |
| 일지 추가 | `pa_signal_w7`: "engulf / pin / inside / none" |
| 성공 기준 | 차트 100봉에서 정확한 PA signal 식별 80% |
| 매핑 약점 | 캔들 무시하고 진입 → PA 확인 룰 |

#### W8: Pullback vs Top Buy ⬜ ⭐⭐⭐

**핵심 질문**: "이게 pullback 진입인가, top buy 인가?"

| 항목 | 내용 |
|---|---|
| 학습 주제 | Pullback = 추세 within 20-40% retrace. Top buy = 추세 끝물에 신고가 직진입 |
| 차트 식별 도구 | swing high → fib retrace 38.2% / 50% / 61.8% 마킹 |
| 일지 추가 | `entry_type_w8`: "pullback (38.2%) / pullback (50%) / pullback (61.8%) / **top buy** / breakout" |
| 성공 기준 | top buy 진입 0회 (weekly) + pullback 진입 ratio 80%+ |
| 매핑 약점 | **사용자 핵심 약점 직접 처방**. L5 top buying / L17 pullback discipline |

---

### Tier 3 — Research Integration

#### W9: Momentum vs 횡보 ⬜

**핵심 질문**: "지금 변동성·속도 적절한가? (Volman scalping criteria)"

| 항목 | 내용 |
|---|---|
| 학습 주제 | ATR z-score, 캔들 body 평균, 1분 진폭 — momentum 정량 측정 |
| 차트 식별 도구 | ATR(14) + ATR pct rank (60d) overlay |
| 일지 추가 | `momentum_w9`: "high (ATR z>+1) / mid / low (z<-0.5)" |
| 성공 기준 | low momentum 시간대 진입 자제 (weekly < 10%) |
| 매핑 약점 | 횡보 짤짤이 후 욕심 — momentum 정량 룰화 |

#### W10: ICT FVG/OB 인식 ⬜ (사용 X, 인식만)

**핵심 질문**: "FVG / OB 가 차트에 있는가? (참고용)"

| 항목 | 내용 |
|---|---|
| 학습 주제 | Fair Value Gap (3캔들 imbalance), Order Block (last opposite candle before impulsive) |
| 차트 식별 도구 | 직접 마킹 (TV indicator OK) |
| 일지 추가 | `ict_w10_present`: "fvg-near / ob-near / both / none" |
| 성공 기준 | 식별 가능 (사용은 안 함) — REJECTED 결과 알면서 다른 트레이더 차트 이해용 |
| 매핑 약점 | 다른 트레이더 ICT 차트 reading 가능 (커뮤니티 노이즈 면역) |

#### W11: 04:30 BURN_X ⭐ ⬜

**핵심 질문**: "04:30 BURN_X 진입 조건 만족하는가?"

| 항목 | 내용 |
|---|---|
| 학습 주제 | 우리 v3.5 핵심 edge. 10y Sharpe_w 4.38. ATM #1 (SL 60 / Pre-Trail 30 / Trail Step 2) |
| 차트 식별 도구 | KST 04:30 vertical line + regime indicator |
| 일지 추가 | `burn_x_0430_w11`: "executed / skipped (regime B) / missed" |
| 성공 기준 | sim 04:30 시그널 4회 중 3회 ATM 정확 적용 |
| 매핑 약점 | 우리 edge 를 알고도 의지 부족으로 안 들어감 — sim 강제 |

#### W12: 22:30 BURN_R + Regime A/B ⬜

**핵심 질문**: "현재 Level A 인가 B 인가? 22:30 BURN_R 적용?"

| 항목 | 내용 |
|---|---|
| 학습 주제 | ADR-022 Regime score (4 지표). Level A = 7-10ct, B = 3-5ct, Mixed = 5-7ct |
| 차트 식별 도구 | EMA200 slope + Close>EMA200 ratio + Sharpe-proxy + Recent MDD |
| 일지 추가 | `regime_w12`: "A (score≥3) / Mixed (=2) / B (≤1)" + `burn_r_2230`: "..." |
| 성공 기준 | 매 세션 시작 regime 평가 + 사이즈 매핑 일관 |
| 매핑 약점 | regime 무시하고 동일 사이즈 — L48 sim size non-transferable 처방 |

---

## 📈 진도 % (자동 계산)

```
Tier 1: ▱▱▱▱ 0/4 (0%)
Tier 2: ▱▱▱▱ 0/4 (0%)
Tier 3: ▱▱▱▱ 0/4 (0%)
─────────────────────
Total:  ▱▱▱▱▱▱▱▱▱▱▱▱ 0/12 (0%)
```

(매주 self-test 후 README 와 함께 갱신)

---

## 🔥 Critical Path

만약 시간 압박이 있으면 **W1 → W2 → W3 → W4 → W8 → W11** 우선 (skip 가능 list: W7 / W10).

W8 (Pullback vs Top Buy) 와 W11 (04:30 BURN_X) 는 사용자 핵심 약점·핵심 edge 직결 → **절대 skip 금지**.

---

## 🎓 졸업 조건 (Tier 4 진입)

- 12주 모두 4점 이상 self-test 통과
- 일지 일관성: 마킹 누락 < 5%
- sim 4주 연속 모라토리엄 해제 조건 만족 (W18~W19 edge 재현)
- → **Apex Eval 진입 준비 완료**

---

*다음 갱신: W1 self-test 완료 시점*
