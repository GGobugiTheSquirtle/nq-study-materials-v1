# 자료 개요 v2 — 검증 데이터 기반 12주 (또는 14주) 재구성

> **Date**: 2026-05-06
> **Source**: MASTER_REPORT.md (16 검증 결과)
> **Principle**: T1 (직접 backtest) 비율 60%+, T5 (권위) < 10%

---

## 🎯 재구성 원칙

1. **검증된 컨셉만 main content**: NOGO/REVERSE 통설은 "REJECTED 1줄 요약" 으로 격하
2. **Discovery 기반 새 룰 추가**: KST hour / Day of Week / Squeeze→Expansion 룰 신규 챕터
3. **각 컨셉마다 검증 수치 표시**: "이 룰은 d=+X, N=Y, period=Z 에서 측정됨"
4. **Forward window 명시**: short (5b/25분) vs long (24b/2h) vs full (48b/4h) hold 결과 분리
5. **사용자 약점 처방 직접 mapping**: 약점 마다 "데이터 검증된 처방" 만 사용

---

## 📋 변경 요약 (v1 → v2)

| Week | v1 (markdown) | v2 (검증 후) | 변화 |
|---|---|---|---|
| W1 | 추세 인식 (HH/HL) | 추세 인식 + Multi-TF small effect 명시 | 약화 (small d=0.03) |
| W2 | EMA 정배열 LONG bias | EMA 정배열 = **장기 hold (24-48b) 시만 effect** | **major change** |
| W3 | SR zone vs 선 | SR zone ≈ line (NQ 5m 큰 차이 X) | 약화, 시각 도구로만 |
| W4 | 매매 시간대 | **KST hour bias 정량 룰** (D1 기반 신규) | **확장** |
| W5 | BB squeeze → expansion | **ATR z squeeze_12 → +44% range** (D3 검증) | 강화 |
| W6 | EMA20 1st touch | **REVERSE 통설**: 4th+ 더 좋음, "touch # 무관" | **major change** |
| W7 | PA candles (Engulf/Pin/Inside) | Strong body continuation ✓ / Hammer-Star REVERSE | **부분 변경** |
| W8 | Fib 38.2-61.8 sweet | Top buy 회피 ✓ + "deeper better" | **부분 변경** |
| W9 | ATR z high momentum | **REJECTED**, reframe = directional bias | **major change** |
| W10 | ICT FVG/OB 인식 | 그대로 (BTC HYP-CONF-001 + 인식 학습) | 변화 X |
| W11 | 04:30 BURN_X | **+ ATR z squeeze guard** (D6 발견) | **강화** |
| W12 | 22:30 BURN_R + Regime | direction-specific (KST 22 SHORT) + Regime | 강화 |
| **W13 NEW** | - | **Day of Week (Mon LONG / Tue SHORT)** | **신규** |
| **W14 NEW** | - | **Confluence top patterns + Cost-adjusted** | **신규** |

총 12주 → **14주**.

---

## 📚 W1 — 추세 인식 (v2)

### Tier badge: 🟡 T2 (parts measured) + 🟢 T1 (Multi-TF B4)

**검증 데이터**:
- B4 Multi-TF all-up vs all-down: d=+0.03 (negligible single-factor)
- last_2y at 24b: mu(up)=+0.080, mu(down)=-0.118 → Δ=0.20 ATR small
- A1 robustness: long forward window 일수록 effect ↑

**핵심 변경**:
- "추세 인식 = 강한 시그널" → "**추세 인식 = small confluence factor**"
- Multi-TF (5m+15m+1h) all-up = small +bias, but not standalone trade signal
- 통설 "uptrend 안에서만 LONG" 부분 confirmed (long hold)

**룰 변경**:
- Range 에서 LONG 충동 진입 lock (X)
- All-up Multi-TF + 다른 confluence (KST hour, etc.) 결합 시만 진입

---

## 📚 W2 — EMA 배열 (REWRITE)

### Tier badge: 🔴 T1 REJECTED short / 🟡 T1 PARTIAL long

**검증 데이터** (A1 + R3):
- fwd 5b: d=+0.014 negligible
- fwd 24b: d=+0.036 small (mu_정=+0.109, mu_역=-0.056)
- fwd 48b: d=+0.042 (mu_정=+0.158, mu_역=-0.119) → **Δ ≈ 0.28 ATR**

**핵심 변경**:
- "정배열 + Price > EMA20 = 90% LONG 자격" **삭제**
- 새 메시지: "**EMA 배열은 장기 hold (2-4시간) 시만 small edge**"
- BURN_X / BURN_R 같은 5분 매매에 EMA filter = no edge
- Hold 30분 이상 시 +0.16 ATR LONG bias 발현

**룰 변경**:
- short-term scalp (≤12b/1h hold): EMA 배열 무관
- 장기 hold (24b+/2h+): 정배열 LONG bias 인정 (small edge)

---

## 📚 W3 — SR zone vs Line (REWRITE)

### Tier badge: 🔴 T1 NOGO

**검증 데이터** (B1):
- Zone (touch≥3) HR = 80.79%, Line HR = 81.42% → Δ -0.62pp
- Touch ≥ 6 일수록 HR **감소** (80.79 → 77.80)

**핵심 변경**:
- "SR zone = single line 보다 우월" **삭제**
- "Strong SR (touch많음) = strong reaction" **삭제**
- 새 메시지: "**SR = visual aid 만, edge X**"

**룰 변경**:
- SR zone vs line 구분 학습 가치만 (시각 도구 조작)
- 진입 trigger 로 SR 단독 사용 금지
- Top buy 회피 (W8 fib < 23.6%) 가 더 정확한 SR 효과

---

## 📚 W4 — KST Hour Bias (RICH NEW CONTENT)

### Tier badge: 🟢 T1 verified (D1 + D6 confluence)

**핵심 신규 룰** (D1 검증):

| KST hour | 24b signed | 48b signed | last_2y 24b | 의미 |
|---|---|---|---|---|
| **04** | +0.21 | +0.16 | -0.06 | BURN_X (legacy edge) |
| **08** | +0.06 | +0.29 | +0.17 | Asian close |
| **14** | +0.06 | +0.37 | +0.06 | US lunch break ⭐ |
| **15** | +0.21 | +0.18 | -0.08 | EU close |
| **19** | **+0.30** | -0.08 | **+0.62** | **pre-NY ⭐⭐⭐** |
| **20** | **-0.18** | -0.45 | +0.09 | NY pre-open SHORT |
| **21** | **-0.15** | -0.51 | -0.38 | NY open lead-in SHORT |
| **22** | -0.05 | -0.34 | -0.45 | BURN_R direction |

**핵심 메시지**:
- **KST hour = NQ 5m 가장 강한 single factor**
- 단일 hour effect d ~ 0.05-0.08 (small), but 가장 큼
- Confluence (KST + Day) 조합 시 d 0.10-0.15

**룰**:
- Edge time (KST 04 / 14 / 19) LONG only
- Reverse time (KST 20-22) SHORT only or skip
- 비-edge time 진입 자제

---

## 📚 W5 — Squeeze → Expansion (UPGRADE)

### Tier badge: 🟢 T1 verified (D3)

**검증 데이터**:
- ATR z squeeze_12 (12 bar consecutive z<-0.5):
  - fwd 12b range +20%
  - fwd 24b range **+32%**
  - fwd 48b range **+44%**
- Direction: signed return 미미 (range expansion only)

**핵심 메시지**:
- BB squeeze 통설 NQ 5m **데이터 검증 ✓**
- 단, **direction 은 없음** (range만 expand)
- Trade plan: squeeze 후 expansion direction 확정 시 follow

**룰**:
- ATR z 12-bar rolling max < -0.5 = squeeze
- Squeeze 후 첫 directional break + 추가 confluence (KST hour 등) 필요
- Squeeze 동안 진입 금지 (방향 미정)

---

## 📚 W6 — EMA Touch # (REVERSE NEW CONTENT)

### Tier badge: 🔴 T1 REVERSE 통설

**검증 데이터** (A2 + R1):
- 1st vs 4th+ HR (12b fwd): -1.68pp h2y, -3.79pp last_1y
- 모든 fwd window (6/12/24/48) 에서 4th+ > 1st

**핵심 변경**:
- "1st/2nd touch best, 4th+ break" **REJECTED**
- "**Touch # 와 hit rate 거의 무관, 4th+ 약간 더 좋음**"
- Linda "Holy Grail" / Adam Grimes paraphrase REJECTED for NQ 5m

**룰**:
- EMA20 retest 자체는 valid setup (HR ~65% across all touches)
- "1st touch only" 룰 삭제
- 4th+ touch 회피 룰 삭제 (오히려 약간 better)

---

## 📚 W7 — PA Candles (PARTIAL)

### Tier badge: 🟢 T1 (strong body) / 🔴 T1 REVERSE (Hammer/Star)

**검증 데이터** (D4):

| Pattern | fwd 24b signed | last_2y |
|---|---|---|
| Bull strong body | +0.156 ✓ | +0.257 |
| Bear strong body | -0.085 (mild) | -0.155 |
| Hammer | -0.200 (REVERSE 통설) | -0.385 |
| Shooting Star | +0.093 (REVERSE) | +0.033 |

**핵심 변경**:
- Strong body 통설 ✓ (small effect, real)
- **Hammer/Shooting Star 통설 REJECTED** (context 없는 단순 wick ratio)
- 단순 패턴 매매 = 위험 (특히 Hammer LONG)

**룰**:
- Bull/Bear strong body candle (body ≥ 70% range) = continuation small bias
- Hammer/Star 단독 진입 금지
- Engulfing = 기존 통설 (별도 검증 안 했지만 strong body 로 cover됨)

---

## 📚 W8 — Pullback (PARTIAL — Top buy 회피만)

### Tier badge: 🟢 T1 verified (Top buy 회피) / 🔴 T1 REVERSE (78.6+ skip)

**검증 데이터** (A3):

| Fib retrace | HR (h2y) |
|---|---|
| <23.6% | 47.35% (lowest) |
| 23.6-38.2% | 53.29% |
| 38.2-50% | 55.29% |
| 50-61.8% | 57.65% |
| 61.8-78.6% | 59.91% |
| 78.6-100% | 60.38% |
| **>100% broken** | **62.65%** |

**핵심 변경**:
- "Top buy (< 23.6% pullback) 회피" **CONFIRMED ✓** ⭐⭐⭐
- "Sweet spot 38.2-61.8" 통설 = 부분 confirmed (+5pp vs 23.6 이전)
- "78.6%+ deep pullback 위험" **REJECTED** — 오히려 HR 가장 높음
- 새 메시지: "**Deeper pullback better** (broken trend 까지 OK)"

**룰** (사용자 핵심 약점 처방):
- LONG entry 시 직전 swing high 에서 ≥ 23.6% retrace 후만 (top buy 회피)
- 38.2-61.8% = "ideal range" 유지
- 78.6%+ 깊이 진입도 OK (data 가 더 좋음)
- > 100% (broken) 는 추세 전환 위험 — context 우선 (W14 confluence)

---

## 📚 W9 — ATR z (REWRITE)

### Tier badge: 🔴 T1 REJECTED H1 / 🟡 T1 NEW signed direction

**검증 데이터** (A4 + R2):
- Range/ATR ratio: REVERSE (z high → ratio low)
- Signed direction (R2 fwd 48b): high z (+) → +0.174 LONG, low z → -0.169 SHORT
- D3: Squeeze (low z extended) → range expansion

**핵심 변경**:
- "z high = momentum entry OK" **REJECTED**
- 새 메시지 1: "**ATR z 는 normalization 도구만**" (stop/TP sizing)
- 새 메시지 2: "**z high 장기 hold 시 LONG bias 약간 있음**" (직접 trade signal X)
- 새 메시지 3: "**Squeeze (low z extended) → expansion 진입 setup**" (W5 와 결합)

**룰**:
- ATR z = stop/TP 동적 sizing (예: SL = 1.5×ATR)
- z 단독 = entry filter X
- Squeeze (z<-0.5 12-bar consec) = setup signal

---

## 📚 W10 — ICT 인식 (UNCHANGED)

### Tier badge: 🟢 T1 (BTC HYP-CONF-001 REJECTED)

기존 v1 그대로. NQ replication 추가 검증은 다음 라운드.

**핵심**: "사용은 안 함, 인식만". 1주 self-experiment hit rate 측정.

---

## 📚 W11 — 04:30 BURN_X + ATR z GUARD (UPGRADE)

### Tier badge: 🟢 T1 ✓ + 🟢 T1 NEW guard rule

**기존 검증** (v3.5):
- 10y Sharpe_w 4.38 ✓
- ATM #1 (60/30/2) tick PF 3.81

**검증 데이터** (D1 + D6):
- KST 04 LONG +0.21 ATR (24b) raw signal confirmed
- **GUARD**: KST 04 + ATR z squeeze_12 → SHORT (-3.54 ATR, d=-0.85, N=80)

**핵심 변경**:
- 기존 BURN_X 룰 유지
- **새 GUARD 룰 추가**: 04:30 시점 ATR z 12-bar max < -0.5 (squeeze) 면 → SKIP (또는 reverse)
- 효과: edge 보존 + worst-case (-3.54 ATR drawdown) 회피

**룰**:
- 04:30 KST + ATR z 충분 (z >= -0.3) → LONG (기존 BURN_X)
- 04:30 KST + squeeze (z < -0.5 for 12 bars) → **SKIP** (또는 SHORT, careful)
- 사이즈: regime-adjusted (W12 ADR-022)

---

## 📚 W12 — 22:30 BURN_R + Regime (UPGRADE)

### Tier badge: 🟢 T1 ✓

**기존 검증**:
- 10y Sharpe 4.72, 2024-2026 4.77
- ADR-022 Regime 4 지표 score

**검증 데이터** (D1):
- KST 22 raw signed = -0.286 (24b), -0.335 (48b) → SHORT direction
- KST 21 -0.51 (48b last_2y -0.74) ⭐ 더 강함

**핵심 변경**:
- 기존 22:30 entry 유지
- **Direction = SHORT default** (gap up reversal). LONG 은 strong gap down 시만
- KST 21 추가 entry window (사이즈 작게) — last_2y -0.74 ATR signed

**룰**:
- 22:30 시점 gap up → SHORT (기존)
- 22:30 시점 gap down → LONG (기존, 약함)
- 21:30-22:00 KST 추가 SHORT setup 검토 (sim only)
- Regime A/B 사이즈 조절 그대로 ADR-022

---

## 📚 W13 NEW — Day of Week ⭐⭐⭐⭐⭐

### Tier badge: 🟢 T1 (D5)

**검증 데이터**:

| Day | 24b signed | 48b signed |
|---|---|---|
| Mon | **+0.30** | **+0.63** ⭐⭐⭐⭐⭐ |
| Tue | -0.19 | -0.27 |
| Wed | +0.11 | +0.21 |
| Thu | +0.01 | -0.09 |
| Fri | -0.08 | -0.19 |

**핵심 메시지**:
- **Monday 가장 강한 LONG bias day** (4시간 forward +0.63 ATR)
- Tuesday SHORT bias
- Mid-week 약함

**룰**:
- Monday LONG bias 강제 (다른 진입 결정 + Mon factor)
- Tuesday SHORT bias 강제
- Wed/Thu/Fri = 다른 factor 우선
- Confluence: KST 14 + Mon = +0.62 ATR / KST 21 + Tue = -0.48 ATR (D6)

---

## 📚 W14 NEW — Confluence + Cost-adjusted ⭐⭐⭐⭐

### Tier badge: 🟢 T1 (D6) + 🟡 T2 (cost not yet applied)

**핵심 메시지**:
- 단일 factor d ~ 0.05-0.08 작음
- 2-factor confluence d ~ 0.10-0.15 medium
- 3-factor d 0.13-0.15 (N drops fast)

**Top confluence rules**:

| Rule | mu (ATR) | d | N |
|---|---|---|---|
| KST 14 + Mon LONG | +0.62 | +0.14 | 656 |
| Squeeze_12 + Mon LONG | +0.49 | +0.11 | 5,076 |
| KST 21 + Tue SHORT | -0.48 | -0.12 | 694 |
| KST 19 + Mon LONG | +0.39 | +0.08 | 700 |

**Cost adjustment** (TODO 다음 라운드):
- Commission RT $2.18 (Tradovate, ADR-033)
- Slippage 0.03% one-way
- Effect 50-70% reduction 예상

**룰**:
- 단일 factor 진입 = 사이즈 ↓
- 2-factor confluence = 표준 사이즈
- 3-factor = ↑ but N small caveat
- Cost-adjusted Sharpe 재산정 후 sim 시작

---

## 🎯 사용자 약점 처방 매핑 v2

| 약점 | v1 처방 | v2 검증 결과 + 처방 |
|---|---|---|
| Top buying L5 | Pullback 38.2-61.8 | ✓ <23.6% 진입 47% HR (확정 회피) |
| 희망적 추세 L41 | 정배열 확인 후 LONG | ❌ short window edge X. 장기 hold 시만 |
| FOMO L4 | ATR z low → lock | ❌ REVERSED — low z = expansion 잠재 |
| 짤짤이 후 욕심 | ATR z high → 진입 | ❌ z 단독 entry signal 아님 |
| 의지 cooldown | edge time 강제 | ✓ KST hour 데이터 검증 (D1) |
| Sim size | regime-adjusted | ✓ ADR-022 그대로 |
| Day-of-week 무관심 | - | **새 처방**: Mon LONG / Tue SHORT (D5) |

---

## 🏗️ HTML 교재 빌드 다음 단계

이 outline 기준 14주 markdown → HTML 빌드:

```
14_curriculum/
├── README.md (이 outline)
├── PROGRESSION_MAP.md (스킬 트리)
├── tier_1_foundation/
│   ├── week_01_trend.md (Multi-TF small effect)
│   ├── week_02_ema_alignment.md (long-hold only)
│   ├── week_03_sr_visual.md (시각 도구만)
│   └── week_04_kst_hour.md ⭐ (NEW major chapter)
├── tier_2_setup/
│   ├── week_05_squeeze_expansion.md ⭐
│   ├── week_06_ema_touch.md (REVERSE 명시)
│   ├── week_07_pa_candles.md (partial)
│   └── week_08_pullback.md (Top buy 회피만)
├── tier_3_research/
│   ├── week_09_atr_normalization.md (reframe)
│   ├── week_10_ict_recognition.md (unchanged)
│   ├── week_11_burn_x_with_guard.md ⭐
│   └── week_12_burn_r_direction.md
├── tier_4_advanced/  (NEW)
│   ├── week_13_day_of_week.md ⭐⭐
│   └── week_14_confluence.md ⭐⭐
└── _logs/
    ├── progression_log.md
    └── observation_log.md
```

각 주차 markdown 마다:
- 🎯 목표
- 📊 **검증 데이터** (수치 표 + chart)
- 📚 핵심 개념 (시각 SVG)
- 🔬 검증 결과 detail (T1/T2/T5 tier badge)
- 📐 차트 관찰 과제
- 📝 일지 마킹
- 🎯 성공 기준
- 📚 원본 소스 (기존 sources)
- ⚠️ Caveats

---

## ⏭️ 다음 작업

1. ✅ Master report 완료
2. ✅ 자료 개요 v2 완료 (이 파일)
3. ⏭️ 14주 markdown 재작성 (각 주 v2 컨텐츠 + 검증 수치 embed)
4. ⏭️ HTML 교재 빌드 (single-page or multi-page)
5. ⏭️ Visual assets (SVG + Chart.js charts for distributions)
6. ⏭️ GitHub Pages 배포

추정 시간:
- 14주 markdown: 2일
- HTML 빌드: 2-3일
- Visual assets: 1일
- 배포: 0.5일
**합계 ~ 6일**

다음 결정:
- (A) Markdown 부터 갈지 / (B) HTML 통째로 갈지
- 추천: **(A) markdown 먼저** → 검증 후 HTML 일괄 빌드 (테스트 용이)
