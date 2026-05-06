# Week 4 — KST Hour Bias ⭐ (single 가장 강한 factor)

> **목표**: 매 trade 시 KST hour 즉답 + edge time 강제. 비-edge 시 진입 자제.
> **검증**: 🟢 T1 (D1 + Phase E)
> **데이터**: NQ 5m 10y, KST hour bin × forward return

---

## 1. 핵심 발견 (15분)

### KST hour = NQ 5m 단일 가장 강한 factor (Cohen's d 측정 기준)

NQ 5m 723k bars 분석:

**Top |return|/ATR (24b forward) — 변동성 큰 시간**:

| KST hr | |ret|/ATR | Signed | 의미 |
|---|---|---|---|
| 21 | 5.76 | -0.15 | NY open 직전 cluster |
| 20 | 5.60 | -0.18 | NY pre-open SHORT |
| 19 | 4.04 | **+0.30** | **pre-NY LONG ⭐⭐⭐** |
| 13/14 | ~3.8 | +0.06/+0.06 | US lunch period |

**Top signed (LONG bias) (24b)**:

| Rank | KST | Signed (h2y) | Signed (last_2y) | 사용 가치 |
|---|---|---|---|---|
| 1 | **19** | +0.30 | **+0.62** | 🏆 NEW edge |
| 2 | 15 | +0.21 | -0.08 | EU close (h2y) |
| 3 | 04 | +0.21 | -0.06 | BURN_X (W11) |
| 4 | 03 | +0.17 | +0.12 | NY late |

**Top signed (SHORT bias) (48b)**:

| Rank | KST | Signed (h2y) | Signed (last_2y) | 주의 |
|---|---|---|---|---|
| 1 | **21** | -0.51 | **-0.74** | 매우 강함 |
| 2 | 20 | -0.45 | -0.67 | NY pre-open |
| 3 | 22 | -0.34 | -0.50 | BURN_R 시간 |

### ⚠️ Cost-adjusted Trade Sim 결과 — 단독 trade 어려움

Phase E 결과:

| Edge | Raw | Trade sim PF | P3 PF | Verdict |
|---|---|---|---|---|
| KST 04 LONG | +0.21 | 1.12 | 1.01 | marginal |
| **KST 14 LONG** | +0.06 | **1.04** | **1.14 ⭐** | recent good |
| KST 19 LONG | +0.30 | 1.00 | 0.99 | flat (단독) |
| KST 15 LONG | +0.21 | 1.04 | 1.08 | OK |
| KST 20 SHORT | -0.18 | **0.93** | 0.84 | LOSE |
| KST 21 SHORT | -0.15 | 0.89 | 0.90 | LOSE |
| KST 22 SHORT | -0.05 | 1.01 | 0.97 | flat |

**핵심**: SHORT 시간대 raw signal 강해도 simple SL/TP 만으로는 LOSE (SL 빈번 hit). LONG side (KST 14 / 19) 가 trade-able.

### 결론

KST hour 단독 = small edge (PF 1.0-1.14)
**Confluence (KST + Day, KST + 다른) → trade-able** (W14 참조)

---

## 2. 24-hour Map

```
KST 시간대:
00:00 ─┬─ NY mid-day (점심권 약함)
01:00  │
02:00  │   (Asian early, low vol)
03:00  │
04:00  │ ⭐ BURN_X LONG (W11) — needs ATM Trail
05:00  │
06:00  │
07:00  │
08:00  │   Asian session ATR low
09:00  │
10:00  │
11:00  │
12:00  │
13:00  │   (US lunch, |ret| 큼)
14:00  │ ⭐ KST 14 LONG (P3 PF 1.14)
15:00  │   EU close LONG
16:00  │
17:00  │
18:00  │
19:00  │ ⭐⭐ KST 19 LONG (raw +0.30 ATR, NEW)
20:00  │ ⚠️ NY pre-open SHORT cluster
21:00  │ ⚠️ NY open SHORT lead-in
22:00  │ ⭐ BURN_R SHORT (W12) — needs trail
23:00  ┴─ NY 마감
```

### Edge time 정의

**LONG bias time** (raw signed > +0.15 ATR):
- KST 04 (BURN_X)
- **KST 14 (US lunch end) ⭐ trade-able**
- KST 15 (EU close)
- **KST 19 (pre-NY) ⭐ trade-able with confluence**

**SHORT bias time** (raw signed < -0.15 ATR):
- KST 20-22 cluster (단독 simple SL/TP LOSE)
- → Trail 또는 confluence 필수

**Non-edge** (signed ≈ 0):
- KST 23-12 (대부분), 16-18, 11-12

---

## 3. Edge Time 강제 룰

### 진입 자격 체크 (모든 매매)

```
Step 1: 현재 KST hour = ?
Step 2: Edge time 인가?
   - Edge LONG (04/14/15/19) → LONG entry consider
   - Edge SHORT (20/21/22) → 단독 X (W11/W12 trail or W14 confluence)
   - Non-edge → SKIP
Step 3: Confluence ATTACH (W14)?
   - Day of week (Mon LONG / Tue SHORT)
   - ATR z (Squeeze 등)
   - Multi-TF
Step 4: Trade plan 결정
```

### 비-edge 진입 lock

| 시간대 | 룰 |
|---|---|
| KST 23-03 (NY late mid) | 진입 자제 |
| KST 09-12 (Asian peak) | Skip (low vol, FOMO 위험) |
| KST 16-18 (EU early) | Skip (transition) |

---

## 4. 차트 관찰 과제 (매일 5분)

### Daily routine

1. NQ 5m 차트 + 시간 vertical line (KST 04, 14, 19, 22)
2. **현재 시간 = ? KST hour 명명**
3. **Edge time 까지 남은 분 = ?**
4. **방향 bias = ?** (LONG/SHORT/non-edge)
5. (옵션) confluence factor (Day of week, squeeze) 추가 식별

### TV setup
- "Sessions" indicator with KST timezone
- Custom vertical lines: 14:00 / 19:00 / 22:30 / 04:30 KST
- Phone alarm: 19:00 / 04:25 KST (Edge time 5분 전)

---

## 5. 일지 마킹

```json
{
  "kst_hour_w4": 14,
  "edge_time_w4": "yes-long-strong / yes-short-strong / yes-medium / non-edge",
  "minutes_to_next_edge": 25,
  "non_edge_entry_w4": "yes / no",
  "kst_hour_signed_expected": 0.21    // expected forward 24b signed return ATR
}
```

**진입 lock**:
- non_edge_entry = yes AND no other strong reason → 진입 금지

---

## 6. 성공 기준

| 기준 | 합격선 |
|---|---|
| 차트 진입 시점 KST hour 마킹 | 100% |
| Edge time 분류 정확 | 95%+ |
| Non-edge 진입 (이유 없음) | 0회 |
| KST 14/19 confluence sim 적용 | 1주 1회+ |

---

## 7. 시각 자료

### Chart 1: KST Hour × Forward Signed Return (24b)
```
[Bar chart: 24-hour KST × signed return ATR]
KST 19  ████████████ +0.30 ⭐
KST 14  ██████ +0.06
KST 04  ██████ +0.21 ⭐
KST 22  ███▓ -0.29
KST 21  ████▓ -0.15
KST 20  █████▓ -0.18
```

### Chart 2: |ret|/ATR distribution by KST hour
[Heat map showing volatility by hour]

### Chart 3: Last_2y vs Equal-weight comparison
[KST 19 last_2y +0.62 vs eq +0.30 = recent strengthening]

---

## 8. 원본 소스

### 검증 데이터
- [research/results/D1_time_of_day/results.json](../../research/results/D1_time_of_day/results.json) — 24-hour × fwd 12/24/48b
- [research/results/E_edge_validation/results.json](../../research/results/E_edge_validation/results.json) — Trade sim
- [research/PHASE_E_REPORT.md](../../research/PHASE_E_REPORT.md)

### 외부 reference
- [SMB Capital](https://www.youtube.com/@smbcapital) — NY open 매매
- [김직선 100억 해외선물 (NotebookLM 136 source)](https://notebooklm.google.com)
- [Mike Bellafiore "One Good Trade"](https://www.amazon.com/One-Good-Trade-Inside-Trading/dp/0470529660)
- [CME Group educational](https://www.cmegroup.com/education.html) — RTH/ETH

### Sources.md
- [05 NQ Specifics sources ⭐⭐⭐](../../05_nq_specifics/sources.md)

---

## 9. Common Mistakes

| 실수 | 처방 |
|---|---|
| Asian session 짤짤이 진입 | Non-edge time lock |
| KST 22:30 미리 진입 | 22:30 시그널 확정 후만 |
| KST 20-22 SHORT 단독 | trade sim LOSE — confluence 필수 |
| 04:30 timing 놓침 | 알람 + Pre-Session Card |
| KST 19 LONG 무시 | NEW edge — 검증된 신호 |

---

## 10. Caveats

1. **Single-factor PF 1.04-1.14 = small** — Trail/Confluence 결합 필수
2. **KST 22 SHORT 단독 simple sim = 1.01 (flat)** — Trail with v3.5 ATM 필수
3. **last_2y vs h2y 차이 큼**: KST 19 last_2y +0.62 vs h2y +0.30 — 최근 강화 (정/거짓 결론 미정)
4. **DST handling**: NY → KST 변환 시 일부 NaT (5h KST 9k bars 누락)

---

*Verified: D1 results + Phase E (16 + 20 edges)*
*Next: W11 BURN_X (04:30 deep-dive) / W14 Confluence (best plans)*
