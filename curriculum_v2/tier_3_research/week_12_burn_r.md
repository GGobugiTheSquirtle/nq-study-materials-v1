# Week 12 — 22:30 BURN_R + Regime A/B

> **목표**: 22:30 KST NY open SHORT direction (gap up reversal) + Regime size 적용.
> **검증**: 🟢 T1 partial (D1 raw signal + Phase E sim trail-dependent)
> **Caveat**: simple SL/TP만으로 PF 1.01 — Trail/ATM 필수 (W11 와 동일)

---

## 1. 검증 데이터

### KST 22 raw signed return

| Window | h2y signed | last_2y signed |
|---|---|---|
| fwd 12b | -0.263 ATR | -0.451 |
| fwd 24b | -0.286 | -0.496 |
| fwd 48b | -0.335 | **-0.600** |

→ **NY open 후 SHORT bias 강함**. Recent (last_2y) 더 강함.

### Phase E Cost-adjusted Sim

| Trade plan | PF (Total) | P3 PF | P3 N |
|---|---|---|---|
| KST22 SHORT, SL 1.5×ATR, TP 2.0 | 1.01 | 0.97 | 845 |
| KST22 + Tuesday SHORT | 0.96 | 0.93 | 171 |
| KST22 + bear_strong | (skip, N small) | - | - |

→ **Simple SL/TP 만으로 marginal**. v3.5 BURN_R Sharpe 4.72 = 다른 trade management.

### Regime A/B (ADR-022)

```
Regime Score (4 지표 합산):
1. EMA200 slope >= +1%
2. Close > EMA200 비율 >= 70%
3. Momentum Sharpe-proxy >= +2
4. Recent MDD > -5%

Score 3+ → Level A (Aggressive) — 7-10ct sim
Score 2  → Mixed — 5-7ct sim
Score ≤1 → Level B (Defensive) — 3-5ct sim
```

→ Sharpe weighted 검증된 룰. Phase E 에서는 별도 미적용 (다음 라운드).

---

## 2. BURN_R Setup

### Trigger

```
Time: KST 22:30 ±2분 (NY 09:30 EST)

Direction logic:
  Open of 22:30 5m bar:
    - Gap up vs 직전 30분 high → SHORT bias (default)
    - Gap down vs 직전 30분 low → LONG bias (counter)
    - In-range → wait or skip
```

### ATM (BURN_R)

ATM #1 (60/30/2) 동일 사용 가능:
- SL: 60 ticks
- Pre-trail: 30 ticks
- Trail step: 2 ticks

또는 v3.5 검증 별도 BURN_R ATM (필요 시 ADR 참조).

### Caveat: HYP-021 후보

```
v3.4 검증 Sharpe 4.72 ✓
v3.5 tick 검증 marginal (PF 1.08)
→ Entry rule 재구성 후보 (사용 보류 가능)
```

→ Sim 으로 진행 OK, Live 신중. W11 BURN_X 가 더 robust.

---

## 3. Regime size 적용

### Level A (score ≥ 3) — Aggressive

- Size: 7-10 ct (sim)
- Conditions: BULL trend confirmed, low MDD

### Level B (score ≤ 1) — Defensive

- Size: 3-5 ct (sim)
- Conditions: BEAR or CHOP, high recent MDD

### Mixed (score = 2)

- Size: 5-7 ct
- Conditions: transition

---

## 4. 사용자 매뉴얼

```
21:30     일과 정리 시작
22:00     차트 ON, slow 모니터
22:20     Pre-Session Card 작성:
          □ Regime score 4 지표
          □ Level (A/B/Mixed)
          □ Size 결정
22:25     ATM 준비 (BURN_R / ATM #1)
22:28     주문 준비 (방향 미정, 22:30 봐서)
22:30:00  ⚡ Direction 결정:
          - Gap up vs 30분 high → SHORT
          - Gap down vs 30분 low → LONG
          - In-range → SKIP
22:31~22:35 Entry confirm
~23:00    1차 trail / SL / 종료
23:00     결과 기록
```

---

## 5. 일지 마킹

```json
{
  "burn_r_2230_w12": {
    "executed": "yes / skip-in-range",
    "regime_score": 3,
    "regime_level": "A / B / Mixed",
    "size_ct": 7,
    "open_vs_30min_hl": "above / below / inside",
    "direction": "short / long / skip",
    "atm": "MNQ_BURN_R / ATM #1",
    "exit_type": "trail / sl / time",
    "result_ticks": -22,
    "result_usd": -110.00
  }
}
```

---

## 6. 성공 기준 (5일 강제)

| 기준 | 합격선 |
|---|---|
| 5일 22:30 sim 실행 | 5/5 |
| Regime score 정확 | 4/5+ |
| Size 룰 정확 | 5/5 |
| 22:30 외 BURN_R 가짜 | 0회 |

---

## 7. 원본 소스

- [research/results/D1_time_of_day/results.json](../../research/results/D1_time_of_day/results.json)
- [research/results/E_edge_validation/results.json](../../research/results/E_edge_validation/results.json)
- ADR-022 Regime score (CLAUDE.md)
- [SMB Capital — opening drive](https://www.youtube.com/@smbcapital)
- [Mike Bellafiore "PlayBook"](https://www.amazon.com/PlayBook-Untold-Story-Quintessential-Trader/dp/1118415302)

---

## 8. Caveats

1. **Phase E simple PF 1.01 (P3 0.97) flat** — Trail 필수
2. **HYP-021 entry rule 재구성 후보** (v3.5 marginal)
3. KST 21 SHORT 더 강함 (-0.51 last_2y) but trade sim LOSE → Trail 사용
4. Live PA 진입 전 W11 BURN_X 우선 검증

---

## 9. 졸업 → Tier 4

W12 졸업 후:
- W13 Day of Week
- W14 Confluence + Trade management

→ 14주 졸업 = Tier 4 → Mastery → Apex Eval 자격
