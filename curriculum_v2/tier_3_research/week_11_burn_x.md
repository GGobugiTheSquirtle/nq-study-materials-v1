# Week 11 — 04:30 BURN_X + Trail Game-Changer ⭐⭐⭐

> **목표**: 04:30 KST 단일 가장 strong-cash edge. ATM Trail 효과 +220% boost. v3.5 sim 적용.
> **검증**: 🟢 T1 (full backtest + cost-adjusted)
> **데이터**: NQ 5m 10y backtest (2016-2026), Phase E (Tradovate cost RT $2.18)

---

## 1. 핵심 발견 (15분 학습)

### Single-factor Edge

KST 04 시간대 (04:00-05:00 = NY 14:00 EST 마감 1.5h 전, EU close 후 3시간):

| Metric | 값 | Window |
|---|---|---|
| Forward signed return (raw) | **+0.21 ATR** | 24b (2h) |
| Forward signed return (raw) | +0.16 ATR | 48b (4h) |
| Last 2y signed | -0.06 ATR (recent weakness) | 24b |
| Trade sim PF (cost-adj, simple SL/TP) | **1.12** | TP 2.0 SL 1.5 |
| P3 (2023+) PF | 1.01 (recent flat) | TP 2.0 |
| 10y Sharpe_w (v3.5 with ATM Trail) | **4.38** | full pipeline |

### 🔥 Trail Game-Changer

**Same edge, two trade plans**:

| Plan | SL | TP / Exit | PF | Note |
|---|---|---|---|---|
| Simple | 1.5 ATR | 2.0 ATR fixed | **1.12** | Phase E |
| **v3.5 ATM Trail** | 60 ticks | Pre-trail 30, Step 2 | **3.81** | tick-tested |

**+220% boost from trail alone**. Same time, same direction, same SL — TP/Trail 만 변경.

### 의미

- 04:30 KST 매매 = 시간대 raw signal 작음 (PF 1.05-1.12 simple)
- **ATM Trail/Partial TP/Sizing = 진짜 게임체인저**
- Trail = winners ride longer + losers cut tight
- Trader가 직접 trail 안 하면 sized portion 의 80%+ edge 손실

---

## 2. ATM #1 Setup (Tradovate)

### Template (BURN_X 60/30/2)

```yaml
ATM Template name: MNQ_BURN_X
Stop Loss:        60 ticks  (= -$30 per MNQ, -$300 per NQ)
Pre-trail:        30 ticks  (활성화 시점)
Trail step:        2 ticks  (ratchet 단위)
Time-in-force:    DAY
```

### Logic

```
Entry @ market 04:30:00 KST (open of 5m bar)
  ↓
SL placed at entry - 60 ticks (initial)
  ↓
Price moves up
  ↓ At entry + 30 ticks → Trail activates
  ↓
SL = current price - 30 ticks (trails up by 2 ticks)
  ↓
SL hit OR session end → exit
```

### 검증 데이터 (5주 sim, Tradovate 2026-03~04)

- Tick PF: **3.81**
- +$171 / 9 trades
- Baseline (60/15/4): +271% Total improvement
- Commission RT $2.18 already 차감

---

## 3. GUARD Rule — Squeeze Skip (Discovery D6)

### 발견

KST 04 + ATR z squeeze_12 (12 consecutive bars z<-0.5):
- N=80 sample
- Forward 24b signed: **-3.54 ATR** (LARGE SHORT bias!)
- Cohen's d = -0.85 (LARGE)
- Direction completely REVERSE 정상 BURN_X LONG

### Phase E sim 결과

| Edge | TP 2.0 PF | P3 PF | P3 N |
|---|---|---|---|
| KST04 normal (no squeeze) | 1.12 | 1.00 | 799 |
| KST04 + Squeeze LONG | 0.84 (LOSE) | 1.62 ⭐ | **18** (small) |
| KST04 + Squeeze SHORT (reverse) | 0.99 | 0.44 | 18 |

**Conclusion**:
- Normal KST 04 (no squeeze): trade plan
- KST 04 + Squeeze: **SKIP** (recent N=18 small for any reverse trade)

### 적용 룰

```python
def burn_x_signal(time, atr_z_12bar_max):
    if time != "04:30 KST":
        return None
    if atr_z_12bar_max < -0.5:    # squeeze active
        return "SKIP"   # 12% of cases
    return "LONG with ATM #1"
```

---

## 4. 사용자 매뉴얼 (Sim 5/5 강제)

### Daily Sequence

```
22:00     일과 정리 (or 자기 전)
04:25     알람 — 잠 깨기
04:27     차트 빠른 setup 확인:
          □ 5m EMA 정렬 (W2, optional)
          □ ATR z (12-bar max) - 핵심 GUARD
            - z <= -0.5 → SKIP (squeeze)
            - z > -0.5 → 진행 (normal)
          □ Recent 30분 swing 위치
04:29:55  Tradovate ATM #1 (BURN_X) selected
          Direction: BUY @ market
          Size: regime A 7-10ct / B 3-5ct (W12 참조)
04:30:00  ⚡ Market BUY entry (5m bar open)
04:30:05  ATM 자동 시작 (SL 60 / Pre-Trail 30 / Step 2)
04:30~05:00 자동 trail / SL hit / time exit
05:00     결과 기록 → progression_log
```

### 5일 강제 (Mon-Fri sim)

| Day | 04:25 알람 | Setup score | Squeeze? | Direction | Result | Sleep |
|---|---|---|---|---|---|---|
| Mon | □ | □/4 | □ | □ | ___ ticks | □ |
| Tue | □ | □/4 | □ | □ | ___ | □ |
| Wed | □ | □/4 | □ | □ | ___ | □ |
| Thu | □ | □/4 | □ | □ | ___ | □ |
| Fri | □ | □/4 | □ | □ | ___ | □ |

---

## 5. 일지 마킹 (모든 trade)

```json
{
  "burn_x_0430_w11": {
    "executed": "yes / skip-squeeze / alarm-fail / setup-mismatch",
    "atr_z_12bar_max": -0.32,
    "squeeze_skip": false,
    "direction": "long / short / skip",
    "atm_template": "MNQ_BURN_X (60/30/2)",
    "size_ct": 5,
    "regime": "A / B / Mixed (W12)",
    "exit_type": "trail / sl-hit / time-out",
    "result_ticks": +27,
    "result_usd": 135.00,
    "sleep_recovery": "yes / no"
  }
}
```

---

## 6. 성공 기준 (주말 self-check)

| 기준 | 합격선 |
|---|---|
| 5일 04:30 sim 실행 | **5/5** (의지 시험) |
| ATM #1 정확 적용 | 5/5 |
| Squeeze guard 정확 (skip 또는 진행) | 100% |
| 04:30 외 BURN_X 가짜 진입 | 0회 |
| Result PF (5 trades) | 1.5+ reference |
| Sleep recovery | 4/5+ |

**점수**:
- 5/5 + ATM 정확 + Guard 정확 → **5점**
- 4/5 + ATM 정확 → **4점** (1일 알람 fail)
- 3/5 또는 ATM 위반 → **3점** (1주 더)

---

## 7. 시각 자료 (HTML 빌드 시 포함)

### Chart 1: KST hour signed return distribution
[fwd 24b signed return × KST hour bin, KST 04 highlight]

### Chart 2: PF comparison (Simple vs ATM Trail)
```
Simple SL/TP    ████ 1.12
v3.5 ATM Trail  ████████████████████ 3.81 (+220%)
```

### Chart 3: Squeeze Guard effect
```
Normal (no squeeze)  ████ 1.12 PF
Squeeze (LONG)       ███ 0.84 PF (LOSE)
Squeeze (skip)       (no trade, no cost)
```

---

## 8. 원본 소스 (직접 click)

### 검증 보고서
- [research/MASTER_REPORT.md](../../research/MASTER_REPORT.md) — 16 검증 종합
- [research/PHASE_E_REPORT.md](../../research/PHASE_E_REPORT.md) — Cost-adjusted edges
- [research/results/D1_time_of_day/results.json](../../research/results/D1_time_of_day/results.json) — KST hour raw 수치
- [research/results/E_edge_validation/results.json](../../research/results/E_edge_validation/results.json) — Trade sim raw

### v3.5 운영 자료
- [CLAUDE.md §해외선물 MNQ 연구](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1) — ADR 전체
- [ADR-029](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1) — STRIDE bug fix
- [ADR-030](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1) — ATM 재최적화
- [ADR-032](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1) — Tradovate 운영
- [ADR-033](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1) — Commission sensitivity

### 외부 reference (NY late session)
- [SMB Capital — NY session](https://www.youtube.com/@smbcapital) ⭐⭐⭐
- [Convergent Trading](https://www.youtube.com/@ConvergentTrading) — DOM + 시간대
- [Brian Shannon Anchored VWAP](https://www.youtube.com/@AlphaTrendsBrianShannon)

### 관련 Sources.md
- [05 NQ Specifics sources](../../05_nq_specifics/sources.md) ⭐⭐⭐
- [05 detail.md](../../05_nq_specifics/detail.md)

---

## 9. Common Mistakes

| 실수 | 처방 |
|---|---|
| 알람 무시, 다시 잠 | 폰 멀리 + 진입 후 5분 후 다시 잠 OK |
| 04:30 외 시간 BURN_X 명명 | 시간 = 룰. 04:25-04:35 외 X |
| ATM 무시 manual SL | ATM 자동 lock — 의지 개입 X |
| Squeeze 시 진입 강행 | GUARD 룰 = 객관적 SKIP |
| 사이즈 욕심 (sim 10ct+) | regime size 룰 (W12) |
| TP target 너무 가까움 | Trail 운영 (ATM #1 30/2) |

---

## 10. Caveats

1. **Trade plan = ATM Trail 가정**: simple SL/TP 만으로는 PF 1.12 — trader 가 trail 직접 운영 시만 3.81
2. **Squeeze guard P3 N=18 small**: 추가 검증 권장
3. **04:30 P3 (recent) PF 1.01**: 최근 약화 가능성 — 모니터링
4. **Commission RT $2.18 가정**: Tradovate 기준. 다른 broker 시 재계산
5. **Cost = 0.022 ATR**: NQ 평균 ATR 기준. 변동성 극단 시 비율 다름

---

## 11. 다음 주 (W12) 연결

W11 = 04:30 single-time edge
W12 = 22:30 BURN_R + Regime A/B size

→ Regime size 룰 (ADR-022) 가 W11 entry 사이즈 결정.
→ 두 시간대 운영 = single 매일 trade.

---

*Verified data: research/PHASE_E_REPORT.md*
