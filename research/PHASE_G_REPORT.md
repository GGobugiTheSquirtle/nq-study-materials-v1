# Phase G — Round Figures Research

> **Date**: 2026-05-06
> **Hypothesis**: 사용자 직관 — "라운드피겨 + K단위 뚫리는 곳 SHORT, 특히 전고점 뚫는 라운드"
> **Method**: NQ 5m 10y, round figure cross detection (50/100/250/500/1000) + swing high/low break flag
> **Forward**: 24-bar signed return / Reversal MFE / Continuation MFE

---

## 🎯 결론 — TL;DR

### 사용자 직관 "전고점 + R1000 → SHORT" → **PARTIAL** (h2y confirmed, l2y REVERSED)

| Metric | h2y (10y) | last_2y (recent) | N |
|---|---|---|---|
| R1000 up + 전고점 break signed | **−0.097** SHORT bias ⭐ | **+0.087 LONG (reversed!)** | 527 |

→ 10y 가중에서는 통설 confirmed (mean revert SHORT). 최근 2년 사이 시장 reverse — recent regime 변화.

### 🆕 더 강한 발견: **전저점 + R1000 → LONG bounce** (반대 setup, robust)

| Rank | Group | h2y signed | l2y signed | N |
|---|---|---|---|---|
| 1 ⭐⭐ | **R1000 + 전저점 break (down)** | **+0.208** | +0.103 | 606 |
| 2 ⭐ | **R500 + 전저점 break (down)** | **+0.120** | +0.165 | 1,120 |
| 3 | R250 down (any, large N) | +0.061 | +0.120 | 8,113 |

→ **GO** — Down-cross + swing low break + K-unit (1000) 시 forward 24b 평균 LONG bounce +0.21 ATR. **시간대 robust (h2y + l2y 동방향).**

---

## 📊 전체 결과 매트릭스

### Up-cross (가격 위로 라운드 돌파)

| Round | All Up | + 전고점 break | − 전고점 |
|---|---|---|---|
| R50 | +0.071 | +0.117 | +0.052 |
| R100 | +0.016 | +0.028 | +0.015 |
| R250 | +0.073 | +0.049 | +0.079 |
| R500 | +0.013 | +0.034 | +0.005 |
| **R1000** | +0.002 | **−0.097** ⭐ | +0.038 |

→ 전고점 + R1000 만 SHORT bias (h2y). 다른 조합은 약한 LONG drift.

### Down-cross (가격 아래로 라운드 돌파)

| Round | All Down | + 전저점 break | − 전저점 |
|---|---|---|---|
| R50 | -0.001 | -0.104 | +0.034 |
| R100 | -0.009 | +0.025 | -0.018 |
| R250 | +0.061 ⭐ | +0.035 | +0.070 ⭐ |
| **R500** | +0.006 | **+0.120** ⭐ | -0.041 |
| **R1000** | -0.047 | **+0.208** ⭐⭐ | -0.160 |

**핵심 패턴**:
- ⭐⭐ **R1000 down + 전저점 break = LONG bounce +0.208** (gold)
- R500 down + 전저점 = LONG +0.120
- R250 일반 down (전저점 무관) = LONG +0.061 (큰 표본 8k)
- 단, R1000 / R500 down (전저점 X) = SHORT continuation (-0.047 / -0.16) — 전저점 break flag 필수

### Reversal MFE (역방향 도달 거리)

| Round | up + SH rev MFE | down + SL rev MFE |
|---|---|---|
| R50 | 2.985 | 2.886 |
| R100 | 2.987 | 2.967 |
| R500 | 3.003 | **3.039** |
| **R1000** | **3.153** ⭐ | **3.043** |

→ K-unit (R1000) 에서 reversal MFE 가장 큼 (3.0+ ATR). 진입 시 reversal target 더 멀리 가능.

---

## 🔬 통계적 평가

### Cohen's d (R1000 down + SL vs random baseline)

- Random baseline: signed +0.005 ATR
- R1000 down + SL: signed +0.208 ATR
- Δ = +0.203 ATR

가장 큰 effect. Δ ATR / typical std (~3.0) = Cohen's d ≈ **0.07** (negligible-small, single-trade noise 거대).

→ **Small effect**, mean drift signal. Trade-able but small. Trail/Confluence 필수.

### N (sample size)

| Group | N (10y) | per-year |
|---|---|---|
| R1000 down + SL | 606 | ~60/y |
| R500 down + SL | 1,120 | ~110/y |
| R250 down (all) | 8,113 | ~800/y (1m TF 가능) |

→ R1000 + SL = 약 5일/주 1회 빈도. 충분.

---

## 📐 판정

### H1a: 라운드 breakout → mean revert
- 🟡 **PARTIAL**. 모든 round step 에 일관된 mean revert 없음.
- R1000 만 일관성 있음 (UP 약함 −0.097, DOWN +0.208).

### H1b: K-unit (R1000) 가장 강한 효과
- 🟢 **GO**. R1000 down + SL signed +0.208 = 최대 effect.
- R1000 up + SH signed -0.097 = 두번째 (h2y 한정).

### H1c: 전고점/전저점 결합 시 강함
- 🟢 **GO** for down direction (R1000 down + SL +0.208 vs all_down -0.047 = +0.255 delta).
- 🟡 PARTIAL for up direction (R1000 up + SH only h2y, l2y reverse).

### 사용자 직관 (전고점 + R1000 SHORT): 🟡 **PARTIAL** (10y confirmed, 최근 2년 reversed)

---

## 🆕 추천 — 새 Pine v5.1 Signal (선택적)

### Signal: "K-Bounce" — R1000 down + 전저점 break → LONG entry

```pinescript
// New v5.1: K-Bounce LONG (R1000 + 전저점 break)
//   Phase G verified: signed +0.208 ATR (h2y), +0.103 (l2y) — robust
//   N=606 (10y, ~60/y)

// Round step detection (1000 unit only — best edge)
prev_low = low[1]
crossed_r1000_down = false
r1000_value = na

// Find R1000 between prev_low and low
floor_1000 = math.floor(prev_low / 1000) * 1000
if floor_1000 < prev_low and floor_1000 >= low and (low <= floor_1000)
    crossed_r1000_down := true
    r1000_value := floor_1000

// Recent 50-bar low break flag
prev_50_low = ta.lowest(low[1], 50)
broke_swing_low = low < prev_50_low

// Combined
v5_k_bounce_long = crossed_r1000_down and broke_swing_low and ema_up    // optional ema filter
```

**판정**: GO 단, 추가 cost-adjusted trade sim (Phase E 같은) 권장.

---

## ⚠️ Caveats

1. **Cost not applied** — 0.022 ATR cost 차감 시 effect 감소 50-70% 예상 (~+0.05 ATR after cost). 여전히 small but trade-able.
2. **N=606 R1000+SL** — 충분하나 추가 OOS 권장.
3. **Up-cross direction reversal in last_2y** — 시장 변화 가능성. 모니터링 필요.
4. **Round step 100/500 도 small effect** — 약하지만 confluence factor 가치.
5. **Effect size small (Cohen d ~0.07)** — single trade noise 큼. Trail/SL 신중.

---

## ⏭️ 다음 단계

1. **Pine v5.1 추가**: K-Bounce LONG signal (R1000 down + 전저점)
2. **Trade sim** (Phase E 동일 방식): cost-adjusted PF / WR
3. **Confluence 결합**: KST hour + Mon + R1000 down + SL → super-confluence?
4. **Up-cross 재검증** — last_2y reverse 가 진짜 regime change 인지

---

## 📁 산출물

- `research/G_round_figures.py` (script)
- `research/results/G_round_figures/results.json` (raw, 5 round levels × 6 groups × 5 schemes)
- 본 보고서

```yaml
판정 매트릭스:
  H1a (round breakout mean revert): PARTIAL
  H1b (K-unit 최강): GO
  H1c (전고점/전저점 결합): GO down / PARTIAL up
  사용자 직관 (전고점+R1000 SHORT): PARTIAL (h2y 만)
  NEW: 전저점+R1000 LONG bounce: GO ⭐⭐
```
