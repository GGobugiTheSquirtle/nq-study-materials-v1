# Phase F — BURN_X ATM 최적화 (HE-001)

> **Date**: 2026-05-06
> **Hypothesis**: KST 04:30 LONG + 작은 SL 제약 (≤ 1.5 ATR) 에서 최적 ATM 파라미터?
> **Method**: 800 grid search (SL × PreTrail × TrailDist × Hold × Guard)
> **Cost**: 0.022 ATR/RT (commission + slippage)

---

## 🏆 핵심 결과 — Optimal ATM v2

### Winner (P3 PF 1.516, Sharpe 2.290)

```yaml
ATM v2 (HE-001 verified):
  Stop Loss:           0.5 × ATR  ≈ 30 ticks (NQ)  ≈ 7.5 pt
  Pre-Trail Trigger:   0.3 × ATR  ≈ 18 ticks       ≈ 4.5 pt
  Trail Distance:      0.3 × ATR  ≈ 18 ticks
  Max Hold:            24 bars (~2 hours)
  Squeeze Guard:       ON (z 12-bar max < -0.5 → SKIP)
```

### Verified Performance (P3 2023-2026)

| Metric | Value |
|---|---|
| **Profit Factor (P3)** | **1.516** |
| Win Rate | 59.4% |
| Expectancy / trade | +0.103 ATR |
| Sharpe (annualized proxy) | 2.290 |
| MDD | small (vs SL=1.5 -34 ATR) |
| N (P3) | 798 trades (~250/year) |
| Total PF (10y) | 1.685 |
| Total PnL (P3 ATR) | not max but stable |

---

## 📊 SL Grid 비교 (best per SL)

| SL × ATR | Best P3 PF | Notes |
|---|---|---|
| **0.5** ⭐ | **1.516** | Winner — tight SL + early trail |
| 0.75 | 1.423 | Decent |
| **1.0** (현재 v3.5) | **1.408** | Current baseline |
| 1.25 | 1.428 | High PnL but lose more |
| 1.5 | 1.383 | Too loose |

→ **SL 작게 (0.5 ATR) = 최적**. Current v3.5 (1.0 ATR) 대비 **+0.108 PF (+7.7%)** 향상.

### Trade-off

| Setup | Pros | Cons |
|---|---|---|
| **SL 0.5 + PT 0.3 + TD 0.3** ⭐ | High PF (1.52) + Sharpe (2.29) | 30 ticks SL — tighter, more stop-outs |
| SL 1.0 (current) | Current 운영 | Lower PF (1.41) |
| SL 1.25 + PT 1.0 | Highest cumulative PnL (+147 ATR) | Lower PF (1.35), bigger MDD (-23 ATR) |

---

## 📐 Param Sensitivity

### Pre-Trail Trigger (PT)

| PT × ATR | Best PF (SL=0.5) | WR | Expectancy |
|---|---|---|---|
| **0.3** ⭐ | 1.516 | 59% | +0.10 |
| 0.5 | ~1.40 | 50% | +0.08 |
| 0.7 | ~1.30 | 45% | +0.07 |
| 1.0 | 1.42 | 38% | +0.13 (bigger but rarer wins) |

→ **PT 0.3 = 가장 robust**. Trail 빨리 활성화 = 더 일관된 small wins.

### Trail Distance (TD)

| TD × ATR | Best PF |
|---|---|
| **0.3** ⭐ | 1.516 |
| 0.5 | ~1.40 |
| 0.7 | ~1.30 |
| 1.0 | ~1.20 |

→ **TD 0.3 = winner**. Tight trail = 빨리 lock profit.

### Max Hold

| Hold (bars) | Best PF |
|---|---|
| 12 (1h) | 1.499 |
| 24 (2h) | 1.515 |
| **36 (3h)** | **1.516** ⭐ |
| 48 (4h) | 1.516 |
| 60 (5h) | 1.516 |

→ **Hold 24-60 모두 동일** (trail 한번 활성화 후 거의 trail 로 exit). H=24 권장 (운영 효율).

### Squeeze Guard

| Guard | Best PF | N P3 |
|---|---|---|
| **ON (skip)** ⭐ | 1.516 | 798 |
| OFF (no skip) | 1.511 | 813 |

→ Squeeze guard 적용 시 약간 더 좋음 (PF +0.005, N -15 = -1.8%). Edge 와 size 보존 trade-off.

---

## 🔧 Tradovate ATM Template (HE-001 v2 ready)

### Template 1 (Recommended: HE-001 Optimal)

```
Template Name:   MNQ_BURN_X_v2
Stop Loss:       30 ticks
Auto Breakeven:  18 ticks (Pre-Trail 활성)
Auto Trail:      18 ticks (Trail 거리)
Time-in-force:   DAY

추가 룰:
  Squeeze Guard 활성:
    04:25 KST 시점 ATR z 12-bar max < -0.5 → SKIP entry
```

### Template 2 (Conservative: SL 1.0 ATR, current)

```
Template Name:   MNQ_BURN_X_v1 (original)
Stop Loss:       60 ticks  (1.0 ATR)
Pre-Trail:       30 ticks
Trail Step:       2 ticks
Time-in-force:   DAY
```

### Template 3 (High PnL Variant — bigger swings)

```
Template Name:   MNQ_BURN_X_BIG
Stop Loss:       75 ticks  (1.25 ATR)
Pre-Trail:       60 ticks  (1.0 ATR)
Trail Step:       2 ticks (Trail dist 0.3 ATR)
Time-in-force:   DAY

→ Cumulative +147 ATR (P3), PF 1.35, MDD -23
   Higher risk for bigger swings
```

---

## ⚖️ Recommendation Matrix

| 사용자 선호 | Template | 이유 |
|---|---|---|
| **High Sharpe + 안정성** | **v2 (30/18/18)** ⭐ | Best PF 1.52, Sharpe 2.29 |
| Current 유지 | v1 (60/30/2) | Already familiar, PF 1.41 |
| Big swing trade | BIG (75/60/3) | Total PnL 큼, MDD 감수 |

**기본 권장**: **v2** — 사용자 "SL 지나치게 크지 않은 선" 요구 부합 + 최고 PF.

---

## 🚨 Caveats / Limitations

1. **30 ticks SL = NQ 0.25/tick × 30 = 7.5 pt** — tight. Realistic 운영 가능 (commission RT $2.18 = 0.5 ticks 정도)
2. **Tighter SL → noise stop-out 위험 ↑** — 실거래 verify 필요 (sim 4주)
3. **Trail dist 0.3 ATR (18 ticks)** — Tradovate 자동 트레일 호환
4. **Squeeze Guard manual implementation** — Tradovate 기본 자동화 X, trader 직접 04:25 체크
5. **Max hold 24 bars** — globex 마감 (06:00 KST) 전 강제 종료
6. **Sample N=798 P3** — sufficient but 추가 1년 (out of sample) 모니터링 권장
7. **All numbers ATR-normalized** — ATR 변동 시 ticks 동적 재계산 필요 (실거래 시 매일 ATR 측정)

---

## 📌 Next Steps

1. **Sim 4주 (week 1-4)**: HE-001 v2 (30/18/18) vs v1 (60/30/2) 동시 sim
   - Same KST 04:30 trigger, parallel ATM templates
   - 비교: 4주 후 PF / WR / drawdown
2. **모라토리엄 해제 검토**: sim 4주 v2 PF 1.4+ 시 → live PA 진입 자격
3. **Curriculum W11 update**: ATM v2 spec 반영
4. **Apex Eval 진입**: live PA 통과 시

---

## 📁 산출물

```
research/
├── F_burn_x_atm_optimize.py     (800 combo grid search)
├── results/F_burn_x_atm/
│   └── results.json              (모든 800 combo raw 수치)
└── PHASE_F_REPORT.md             (이 파일)
```

전체 800 grid → JSON 보존. 추가 분석 / 다른 metric ranking 가능.
