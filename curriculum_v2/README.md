# Curriculum v2 — 검증 데이터 기반 14주 NQ 5m 매매 교재

> **Date**: 2026-05-06
> **Version**: 2.0 (post-research, cost-adjusted)
> **Source**: 16 검증 + 20 cost-adjusted edge validation (research/MASTER_REPORT.md + PHASE_E_REPORT.md)
> **Data**: NQ 5m FirstRateData 2016-01 ~ 2026-04 (10.3y, 723k bars)

---

## 🎯 v1 → v2 핵심 변경

### 검증으로 REJECTED 된 통설 (v1 → 1줄 요약)

| 통설 | v1 위치 | v2 status |
|---|---|---|
| EMA 정배열 = 90% LONG | W2 | 🔴 REJECTED short window (d=0.014) — long-hold 시만 small effect |
| EMA20 1st touch best | W6 | 🔴 **REVERSE** — 4th+ touch HR 더 높음 |
| Fib 78.6+ 깊은 pullback 위험 | W8 | 🔴 REJECTED — deeper better |
| ATR z high = momentum | W9 | 🔴 REJECTED — range REVERSE, signed long-only |
| SR zone (touch≥3) > line | W3 | 🔴 NOGO — Δ -0.62pp |
| BB 95% inside | W5 | 🔴 89% NQ 5m (fat tails) |
| Hammer/Shooting Star reversal | W7 | 🔴 REVERSE — 단순 적용 시 |
| Linda Holy Grail | W6 | 🔴 ADR-028 + A2 confirmed REJECTED |

### Verified (T1 — 직접 backtest) 살아남은 룰

| 컨셉 | 위치 | 검증 결과 |
|---|---|---|
| Top buy 회피 (<23.6% pullback) | W8 | HR 47% (lowest) ✓ |
| Squeeze→Expansion (ATR z) | W5 | range +44% (48b) ✓ |
| Strong body continuation | W7 | Δμ +0.24 ATR ✓ |
| 04:30 BURN_X (with Trail) | W11 | Sharpe 4.38 ✓ + simple PF 1.12 |
| 22:30 BURN_R direction | W12 | KST 22 SHORT confirmed |
| Multi-TF all-up small | W1 | d=+0.03 small but real |

### NEW 발견 (Discovery 기반)

| 신규 룰 | 위치 | 데이터 |
|---|---|---|
| KST 14 LONG (US lunch) | W4 | +0.37 ATR (48b), P3 PF 1.14 ⭐ |
| KST 19 LONG (pre-NY) | W4 | +0.30 ATR (24b), last_2y +0.62 ⭐⭐⭐ |
| KST 04 LONG (BURN_X 시간 base) | W4 | +0.21 ATR (24b), PF 1.12 simple |
| KST 20-22 SHORT cluster | W4 | raw signed -0.15~-0.45 (단 SL hit 빈번, simple sim LOSE) |
| **Monday LONG bias** | W13 | +0.63 ATR (48b), PF 1.05 ⭐ |
| Tuesday SHORT | W13 | -0.27 (48b), simple PF 0.94 ❌ |
| **CONF_KST14+Mon LONG** | W14 | **PF 1.22 (P3) ⭐⭐ best confluence** |
| **CONF_KST19+Mon LONG** | W14 | PF 1.09 (P3) ⭐ |
| BURN_X + Squeeze GUARD | W11 | Squeeze 시 LONG → 0.84 PF (skip 룰) |

### Cost-adjusted 핵심 통찰

1. **Single-factor edge 거의 marginal** (cost 후 PF 1.00-1.12)
2. **Confluence (2-factor) 가 진짜 trade-able** — PF 1.07-1.22 (best)
3. **Trade management (Trail/ATM) = 진짜 game-changer** — v3.5 BURN_X simple 1.12 → ATM trail 3.81 = +220% boost
4. **시간대 SHORT (raw strong) 단독 trade 금지** — SL hit 빈번 (KST 20-22)
5. **Trade-off**: Confluence = 정확도 ↑ but freq 1/5-7

---

## 🎓 14주 진도 맵

### Tier 1: Foundation (Month 1) — 차트 읽기 기본
- W1: Multi-TF 추세 (small effect d=0.03)
- W2: EMA 배열 (long-hold only)
- W3: SR zone (visual aid only)
- W4: **KST hour bias** ⭐ (rich data)

### Tier 2: Setup (Month 2) — 진입 자리
- W5: ATR z Squeeze→Expansion ⭐
- W6: EMA touch (REVERSE 통설)
- W7: PA candle (strong body 만 valid)
- W8: Top Buy 회피 + Pullback

### Tier 3: Research Integration (Month 3) — 우리 v3.5
- W9: ATR z normalization (reframe)
- W10: ICT 인식 (사용 X)
- W11: **04:30 BURN_X with Trail ⭐⭐⭐** (game-changer chapter)
- W12: 22:30 BURN_R direction

### Tier 4: Advanced (Month 4) — Confluence + Real Trading ⭐ NEW
- W13: **Day of Week** (Mon LONG, Tue 단독 X)
- W14: **Confluence + Trade Management ⭐⭐⭐**

졸업 = Tier 4 완료 = Apex Eval 자격

---

## 📊 Phase E 종합 — Cost-adjusted Edge Survival

| Edge | Total PF | P3 PF | P3 N | Verdict |
|---|---|---|---|---|
| 🏆 CONF_KST14_MON LONG | 1.07 | **1.22** | 169 | ⭐⭐ Best |
| 🏆 KST14_LONG | 1.04 | 1.14 | 846 | ⭐ Larger N |
| 🏆 CONF_KST19_MON LONG | 1.12 | 1.09 | 169 | ⭐ Confluence |
| 🥈 MON_LONG | 1.05 | 1.08 | 11,924 | Small consistent |
| 🥈 KST04 BURN_X (simple) | 1.12 | 1.01 | 813 | Trail 필요 |
| 🥈 SQ12_MON_LONG | 1.03 | 1.07 | 14,009 | Big sample |
| 🥉 KST22 BURN_R | 1.01 | 0.97 | 845 | Trail 필요 |
| 🥉 SQUEEZE12_LONG | 1.02 | 0.99 | 10,881 | Flat |
| ❌ KST20/21 SHORT | 0.93 | 0.84 | 846 | LOSE single |
| ❌ TUE_SHORT | 0.94 | 1.04 | 11,575 | Flat recent |

**Trade plan recommendation** (sim 적용 우선순위):
1. **KST 14 + Mon LONG** (P3 PF 1.22, ~50 trades/y)
2. **KST 19 + Mon LONG** (P3 PF 1.09, ~50/y)
3. **04:30 BURN_X with v3.5 ATM Trail** (PF 3.81, ~250/y)

---

## 📚 자료 활용

매주 markdown 의 구조:
- 🎯 목표 + 검증 status
- 📊 검증 데이터 (수치 표 + 우리 측정 결과)
- 📚 핵심 개념 (시각 도식)
- 🔬 Tier badge (T1 verified / T2 path-sim / T3 logical / T5 authority)
- 📐 차트 관찰 과제
- 📝 일지 마킹 + Pre-Session Card 진화
- 🎯 성공 기준 (week-end self-test)
- 📚 원본 소스 (sources.md 링크)
- ⚠️ Caveats / limitations

---

## 🚀 시작

1. README 읽기 (이 파일)
2. [PROGRESSION_MAP.md](PROGRESSION_MAP.md) 확인
3. **[Week 1: Multi-TF 추세](tier_1_foundation/week_01_trend.md)** 부터 차근차근
4. 매주 self-test → [progression_log.md](_logs/progression_log.md)
5. 14주 후 Tier 4 졸업 → Apex Eval 진입 자격

---

*Curriculum v2 — research backed by 16 hypothesis tests + 20 cost-adjusted edge sim*
*Raw data: research/results/*
*Reports: research/MASTER_REPORT.md, PHASE_E_REPORT.md*
