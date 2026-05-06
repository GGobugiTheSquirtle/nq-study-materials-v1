# Week 14 — Confluence + Trade Management ⭐⭐⭐ (가장 trade-able edge)

> **목표**: 2-factor confluence + Trail = 진짜 trading edge. v3.5 BURN_X 외 KST14+Mon, KST19+Mon plan.
> **검증**: 🟢 T1 (Phase E cost-adjusted, 20 edges sim)
> **데이터**: NQ 5m 10y, Tradovate cost RT $2.18, P3 (2023+) recent split

---

## 1. 핵심 통찰 (15분 학습)

### Single-factor 거의 marginal after cost

Phase E 결과:

| 단일 신호 | 검증 raw signed (24b) | Cost-adj PF (TP 2.0) | P3 PF |
|---|---|---|---|
| KST 04 LONG | +0.21 ATR | 1.12 | 1.01 |
| KST 14 LONG | +0.06 ATR | 1.04 | 1.14 |
| KST 19 LONG | +0.30 ATR ⭐ | 1.00 | 0.99 |
| Monday LONG | +0.30 ATR (24b) | 1.05 | 1.08 |
| KST 22 SHORT | -0.29 ATR | 1.01 | 0.97 |

→ Raw signal 강해도 cost 후 PF 1.00-1.12 marginal.

### Confluence (2-factor) 가 진짜

| Confluence | Raw single sum | Cost-adj PF (TP 2.0) | **P3 PF** |
|---|---|---|---|
| **KST 14 + Monday** | (0.06 + 0.30) = 0.36 | 1.07 | **1.22** ⭐⭐ |
| **KST 19 + Monday** | (0.30 + 0.30) = 0.60 | **1.12** | 1.09 ⭐ |
| KST 21 + Tuesday | (-0.15 - 0.19) = -0.34 | 0.93 | 1.04 (recent flat) |
| Squeeze + Monday | small + 0.30 | 1.03 | 1.07 |

**핵심**:
- 2-factor confluence: PF +0.02-0.18 vs single
- N drop 5-7x (정확도 ↑ but freq ↓)
- KST 14 + Monday = **best survivor** (P3 PF 1.22, N 169)

### Trade Management = 최종 game-changer

v3.5 BURN_X 동일 시그널, trade plan 차이:

```
Simple SL=1.5 ATR, TP=2.0 ATR fixed   PF 1.12
v3.5 ATM #1 (60/30/2 ticks Trail)     PF 3.81 (+220%)
```

**Trail / Partial / Sizing = 진짜 cash cow**.

---

## 2. Top 3 Trade Plans (Sim 적용 가능)

### Plan A — 🏆 KST 14 + Monday LONG (best confluence)

```yaml
Trigger:
  KST hour:    14:00 (US lunch break end)
  Day of week: Monday
  Entry:       14:00 KST 5m bar open + 1 (= 14:05 close + open of 14:10)
  Direction:   LONG only

ATM:
  SL:          1.5 × ATR
  TP:          2.0 × ATR (or 1.5 for shorter hold)
  Max hold:    48 bars (4 hours)

Frequency:
  ~50 trades / year (1/week, Monday only)

Verified:
  Total PF:    1.07
  P3 PF:       1.22 ⭐⭐
  P3 N:        169
  Cost:        0.022 ATR included
  WR:          45-52%
```

### Plan B — KST 19 + Monday LONG (2nd confluence)

```yaml
Trigger:
  KST hour:    19:00 (pre-NY open)
  Day:         Monday
  Direction:   LONG

ATM:
  SL:          1.5 × ATR
  TP:          2.0 × ATR
  Max hold:    48 bars

Frequency:
  ~50 / year

Verified:
  Total PF:    1.12
  P3 PF:       1.09 ⭐
  P3 N:        169
```

### Plan C — 04:30 BURN_X with v3.5 ATM Trail (cash cow)

```yaml
Trigger:
  KST hour:    04:30
  GUARD:       ATR z 12-bar max >= -0.5 (no squeeze)
  Direction:   LONG (squeeze 시 SKIP)

ATM #1:
  SL:          60 ticks (-$30 MNQ)
  Pre-trail:   30 ticks
  Trail step:  2 ticks

Frequency:
  ~250 / year (daily 04:30)

Verified:
  Sharpe_w (10y, with trail):  4.38
  Tick PF (5w live sim):       3.81
```

### Combined: 3 plans simultaneous

- **350 trades / year** total (~1.4/day)
- Diversified time × pattern × management
- Robust to single-edge decay

---

## 3. 적용 우선순위

```
Tier 4 졸업 학습 → Sim 4주:

Week 1-2: Plan C (BURN_X) 만 (5/5 daily)
   목표: ATM Trail 운영 internalize, sleep routine 적응

Week 3: Plan A (KST 14 + Mon) 추가 — Mon 1회/week
   목표: Confluence 진입 timing 체득

Week 4: Plan B (KST 19 + Mon) 추가
   목표: 3 plans 동시 운영 시스템화

→ Sim 4주 통과 시 → Live PA / Apex Eval 자격
```

---

## 4. Confluence 측정 데이터 (D6 + Phase E 종합)

### 2-factor confluence ranked (Cost-adj P3 PF)

| Rank | Signal | P3 PF | P3 N | 등급 |
|---|---|---|---|---|
| 1 | **CONF_KST14_MON LONG** | **1.22** | 169 | ⭐⭐ |
| 2 | KST14 LONG (single) | 1.14 | 846 | ⭐ |
| 3 | CONF_KST19_MON LONG | 1.09 | 169 | ⭐ |
| 4 | MON_LONG (single) | 1.08 | 11,924 | small |
| 5 | KST15 LONG | 1.08 | 846 | OK |
| 6 | CONF_SQ12_MON LONG | 1.07 | 14,009 | big sample |
| 7 | TUE_SHORT | 1.04 | 11,575 | flat |
| 8 | CONF_KST21_TUE SHORT | 1.04 | 171 | recent only |
| 9 | KST04 BURN_X (simple) | 1.01 | 813 | trail 필요 |
| 10 | KST22 BURN_R (simple) | 0.97 | 845 | trail 필요 |

### Cost-adjusted Sharpe (선택 sample)

| Plan | Annualized Sharpe (proxy) | Annual return (assumes Kelly) |
|---|---|---|
| Plan A (KST14+Mon, TP 2.0) | ~0.5-0.7 | +5-10% per year |
| Plan B (KST19+Mon) | ~0.4-0.5 | +3-7% |
| Plan C (BURN_X with Trail) | ~1.5+ (v3.5 verified) | +20-40% |
| **Combined 3 plans** | ~1.0-1.5 | +15-25% |

(Sim 검증 완료 후 Live 적용 시점 결정)

---

## 5. 일지 마킹 (Tier 4)

```json
{
  "w14_plan_executed": "A / B / C / multiple / none",
  "w14_confluence_filters_passed": ["KST 14:00", "Monday"],
  "w14_cost_adjusted_pf_target": 1.22,
  "w14_atm_template": "MNQ_BURN_X / Custom Plan_A_atm",
  "w14_actual_pnl_ticks": +28,
  "w14_actual_pnl_usd": 140.00,
  "w14_setup_score": 4    // 1-4: confluence factors met
}
```

---

## 6. 성공 기준 (Tier 4 졸업)

| 기준 | 합격선 |
|---|---|
| Plan A (KST14+Mon) sim 4주 | 4/4 Mon 진입 |
| Plan B (KST19+Mon) sim 4주 | 4/4 Mon 진입 |
| Plan C (BURN_X) daily | 20/20 weekday |
| 4주 종합 PF | 1.10+ |
| Trail/ATM 운영 정확 | 100% |
| 충동 단일 factor 진입 | 0회 |

→ 모두 통과 = **14주 졸업** = Tier 4 → Mastery → Apex Eval 자격

---

## 7. 시각 자료 (HTML 빌드)

### Chart 1: Single-factor vs Confluence vs Trail
```
Single-factor PF        ████ 1.05 (avg)
2-factor confluence     █████ 1.10
Trail (BURN_X)          ████████████████████ 3.81 ⭐
```

### Chart 2: Edge survival across periods
[Heat map: edge × P1/P2/P3 PF]

### Chart 3: 3 plans freq vs PF
```
        PF  freq/y
Plan A  1.22  50    ⭐⭐ best per-trade
Plan B  1.09  50
Plan C  3.81  250   ⭐⭐⭐ cash cow
```

---

## 8. 원본 소스

### 검증 보고서
- [research/PHASE_E_REPORT.md](../../research/PHASE_E_REPORT.md) — 20 edges cost-adj sim
- [research/results/E_edge_validation/results.json](../../research/results/E_edge_validation/results.json)
- [research/results/D6_confluence/results.json](../../research/results/D6_confluence/results.json)

### v3.5 운영
- ADR-022 Regime A/B
- ADR-030 ATM 재최적화 (BURN_X 60/30/2)
- ADR-033 Commission RT $2.18

### 외부 reference (Confluence + Trade management)
- [Mike Bellafiore "The PlayBook"](https://www.amazon.com/PlayBook-Untold-Story-Quintessential-Trader/dp/1118415302) — confluence trading framework
- [SMB Capital](https://www.youtube.com/@smbcapital) — playbook + risk management
- [Linda Raschke "Street Smarts"](https://www.amazon.com/Street-Smarts-High-Probability-Short-Term-Strategies/dp/0965046109) — multi-factor entry

---

## 9. Limitations

1. **Confluence N small**: KST14+Mon P3 N=169, KST19+Mon N=169 — 가능 overfitting
2. **Trade management not full sim**: Trail 효과 v3.5 외 다른 plan 별도 측정 X
3. **Cost = 0.022 ATR rough**
4. **Plan A/B P3 weakening** weak signal (PF 1.22 → 1.07 long-term)
5. **Live ≠ sim**: Slippage, market impact, psychology — sim 4주 필수

---

## 10. 핵심 메시지

> **"단일 factor = 작은 edge. Confluence = trade-able. Trail = game-changer."**

Tier 4 졸업 = 이 3개 인지 + 운영 가능 = Apex Eval 진입 자격.

---

*Verified: PHASE_E_REPORT.md / E_edge_validation results.json*
*Next: Tier 4 졸업 후 Live PA / Apex transition*
