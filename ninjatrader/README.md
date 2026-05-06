# NinjaTrader 8 — v5/v5.1 Setup Guide

> Pine v5.1 (`MNQ_All_v5.pine`, 980 lines) 의 NT8 포팅 + ATM Templates
>
> **Updated**: 2026-05-07 (schema 정정 — sample.xml 발견 후)
> **Source**: research/MASTER_REPORT.md + PHASE_E/F/G2/G3 + Pine v5.1

## 🚨 v2 정정 (2026-05-07): NT8 ATM = 2-tier 구조

**중요**: NT8 ATM template 은 **StopStrategy 와 ATM 이 별도 폴더 / 별도 파일**:

```
templates/
├── StopStrategy/         ← Auto Trail / Break Even spec (별도)
│   ├── R500_PH_SHORT_stop.xml
│   ├── BURN_X_v2_stop.xml
│   ├── BURN_X_v1_stop.xml
│   └── KST_CONF_LONG_stop.xml
└── AtmStrategy/          ← Quantity / SL / Target + StopStrategyTemplate name reference
    ├── MNQ_R500_PH_SHORT.xml
    ├── MNQ_BURN_X_v2.xml
    ├── MNQ_BURN_X_v1.xml
    ├── MNQ_KST_CONF_LONG.xml
    └── MNQ_SCALP_LIGHT_A.xml
```

ATM XML 의 `<StopStrategyTemplate>` 태그가 StopStrategy template **이름** 을 reference.

이전 (v1) XML 은 schema 잘못 — flat fields (`<AutoTrailFrequency>`, `<AutoTrailAmount>`) 였음.
정확 schema (sample.xml 기준) = `<AutoTrailSteps><AutoTrailStep>` nested.

---

## 📂 파일 구조

```
ninjatrader/
├── Indicators/                              (.cs → NT8 bin/Custom/Indicators/)
│   ├── AAL_Shared.cs
│   ├── AAL_StE_Signal.cs (v1.2)             L3/S2 Tier A/B + Thursday SKIP
│   ├── AAL_R8_Signal.cs                     4h cross+ADX+retest
│   ├── AAL_v5_RoundShort.cs ⭐ NEW          R500↑PH SHORT (G3 P3 PF 4.56)
│   └── AAL_v5_KSTHour.cs ⭐ NEW             KST 14/19/04:30 + Squeeze GUARD + DOW
├── StopStrategy/                            (.xml → NT8 templates/StopStrategy/)
│   ├── R500_PH_SHORT_stop.xml ⭐            Auto Trail 12/12/1 (G3)
│   ├── BURN_X_v2_stop.xml                   Auto Trail 18/18/1 (HE-001)
│   ├── BURN_X_v1_stop.xml                   Auto Trail 30/30/2 (legacy)
│   ├── KST_CONF_LONG_stop.xml               BreakEven 40+4
│   ├── sample.xml                           NT8 default (참조용)
│   └── sample1.xml                          NT8 default (참조용)
├── AtmStrategy/                             (.xml → NT8 templates/AtmStrategy/)
│   ├── MNQ_R500_PH_SHORT.xml ⭐             SL 18 + R500_PH_SHORT_stop ref
│   ├── MNQ_BURN_X_v2.xml                    SL 30 + BURN_X_v2_stop ref
│   ├── MNQ_BURN_X_v1.xml                    SL 60 + BURN_X_v1_stop ref
│   ├── MNQ_KST_CONF_LONG.xml                SL 60 / TP 120 + KST_CONF_LONG_stop
│   └── MNQ_SCALP_LIGHT_A.xml                SL 10 / TP 10 (no stop strategy)
└── README.md (이 파일)
```

---

## 🚀 설치 (1회)

### 1) Indicators (.cs)

NT8 → Control Center → New → NinjaScript Editor → Compile (F5).

```
.cs 파일들 → C:\Users\<user>\Documents\NinjaTrader 8\bin\Custom\Indicators\
```

NT8 → New → NinjaScript Editor → 첫 컴파일 시 F5. 새 indicators 가 차트 indicator list 에 등장.

### 2) StopStrategy + ATM Templates (.xml) — 2단계 설치

```
StopStrategy XMLs → templates/StopStrategy/  (4개)
ATM Strategy XMLs → templates/AtmStrategy/   (5개, 그 중 4개는 StopStrategy 참조)
```

NT8 재시작 후 ATM Strategy Selector dropdown 에서 5종 선택 가능.

> ⚠️ XML 로드 실패 시 → **GUI 로 직접 만들기 (가장 안전)**:
> Chart Trader → ATM Strategy → ▼ → Custom → 아래 값 입력 → Save as Template
> NT8 가 GUI 로 만든 XML 이 가장 정확. 이후 그 XML 을 본 repo 사본과 비교/패치 가능.

---

## ⚙️ ATM Templates 5종 — 각 파라미터 (GUI 입력용)

### 1) 🔴 MNQ_R500_PH_SHORT ⭐⭐⭐⭐⭐ (G3 P3 PF 4.56)

> 트리거: AAL_v5_RoundShort 의 R500↑PH SHORT 신호 발생 시

| GUI Field | Value |
|---|---|
| Order quantity | 1 |
| TIF | GTC |
| Parameter type | Ticks |
| Quantity (Target 1) | 1 |
| Stop loss | **18 ticks** (0.3 ATR @ NQ ATR 15pt) |
| Profit | 0 (no fixed TP, trail only) |
| Stop strategy | **Auto Trail** |
| Auto Trail — Threshold (active 시점) | 12 ticks |
| Auto Trail — Amount (trail 거리) | 12 ticks |
| Auto Trail — Frequency | 1 tick |

**검증**: P3 PF 4.559, WR 63.2%, +0.41 ATR/trade, N=1,197 (10y 270/y)

### 2) 🟢 MNQ_BURN_X_v2 (HE-001 optimal)

> 트리거: AAL_v5_KSTHour 의 04:30 BURN_X (no squeeze) 신호

| GUI Field | Value |
|---|---|
| Order quantity | 1 |
| TIF | GTC |
| Stop loss | **30 ticks** (0.5 ATR) |
| Profit | 0 (trail only) |
| Stop strategy | Auto Trail |
| Auto Trail Threshold | 18 ticks |
| Auto Trail Amount | 18 ticks |
| Auto Trail Frequency | 1 tick |

**검증**: P3 PF 1.516, WR 59.4%, +0.10 ATR/trade, N=798

### 3) 🟡 MNQ_BURN_X_v1 (current legacy)

> 기존 사용 중. v3.5 검증 spec.

| GUI Field | Value |
|---|---|
| Order quantity | 1 |
| TIF | GTC |
| Stop loss | **60 ticks** (1.0 ATR) |
| Profit | 0 |
| Stop strategy | Auto Trail |
| Auto Trail Threshold | 30 ticks |
| Auto Trail Amount | 30 ticks |
| Auto Trail Frequency | 2 ticks |

**검증**: P3 PF 1.408, WR 70.7% (v3.5 검증 + Phase F sim).

### 4) 🟢 MNQ_KST_CONF_LONG (KST 14/19 + Mon)

> 트리거: AAL_v5_KSTHour 의 🔥 KST14+Mon CONF 또는 KST19+Mon CONF

| GUI Field | Value |
|---|---|
| Order quantity | 1 |
| TIF | GTC |
| Stop loss | **60 ticks** (1.0 ATR) |
| Profit | **120 ticks** (2.0 ATR) |
| Stop strategy | **BreakEven** |
| BreakEven Trigger | 40 ticks (after +40 ticks profit) |
| BreakEven Plus | 4 ticks (BE + 4 = +1 pt safety) |

**검증**: KST14+Mon P3 PF 1.22, KST19+Mon P3 PF 1.09 (Phase E)

### 5) ⚡ MNQ_SCALP_LIGHT_A (1:1 RR fixed)

> 사용자 직관 진입 (1-5분 hold). Commission 친화 (ADR-033).

| GUI Field | Value |
|---|---|
| Order quantity | 1 |
| TIF | GTC |
| Stop loss | **10 ticks** |
| Profit | **10 ticks** |
| Stop strategy | None (no trail) |

**WR 임계**: 55% (commission RT $2.18 차감 후 양수 EV)

---

## 📊 Indicator 사용 가이드

### AAL_v5_RoundShort (NEW v5.1)

차트 add → 5m TF → default settings:
- Round Step: 500
- Pivot Strength: 5
- Show R1000: ON (보조 mark)
- Show KST 21 Extreme: ON (rare)
- Show ATM Label: ON
- Alert on R500: ON ⭐
- Alert on Extreme: ON

**시각**: 🔴 R500↑PH SHORT (orange ▼ + 라벨 with ATM ticks)

### AAL_v5_KSTHour (NEW v5)

차트 add → 5m TF → default settings:
- Show KST 04:30 BURN_X: ON ⭐
- Show KST 14: ON
- Show KST 19: ON ⭐⭐
- Show KST 15: OFF (보조)
- Show KST 20-22 Warn: ON
- Show Day of Week: ON
- Show Confluence: ON
- Squeeze Window: 12 / Threshold: -0.5 (D6 verified)
- Alert on BURN_X (clean): ON
- Alert on Squeeze SKIP: ON
- Alert on KST 19: ON

**시각**:
- ⚡ 04:30 (clean): lime ▲ + ATM ticks
- 🚨 04:30 + squeeze: red SKIP
- ⭐ KST 19: aqua ▲ + "19" (Mon 결합 시 🔥 CONF)
- KST 14: cyan ▲ + "14"
- ⚠ KST 20-22: orange diamond
- 📅 Day of Week: Mon LONG / Tue SHORT / Thu L3 SKIP label

### AAL_StE_Signal (existing v1.2)

기존 그대로 사용. L3/S2 Stoch Extreme + Tier A/B + Thursday L3 SKIP.

### AAL_R8_Signal (existing v1.0)

4h TF 전용. BTC/NQ Cross+ADX+Retest. v5와 별개 (HTF 전략).

---

## 🎯 통합 운영 권장 (5m 차트)

```
차트 indicator stack:
  1. AAL_StE_Signal (existing) — L3/S2 trigger
  2. AAL_v5_KSTHour (NEW)       — 시간대 + DOW + Squeeze GUARD
  3. AAL_v5_RoundShort (NEW)    — R500+PH SHORT trigger

ATM mapping:
  Signal type             ATM Template
  ─────────────────────   ───────────────────
  ⚡ 04:30 BURN_X clean   → MNQ_BURN_X_v2
  🚨 04:30 + squeeze     → SKIP (no entry)
  ⭐ KST 19 + Mon CONF   → MNQ_KST_CONF_LONG
  🔥 KST 14 + Mon CONF   → MNQ_KST_CONF_LONG
  ⚠ KST 20-22 (단독)    → SKIP (confluence 필요)
  🔴 R500↑PH SHORT       → MNQ_R500_PH_SHORT ⭐⭐⭐⭐⭐
  💀 KST21+R1k+PL extreme→ MNQ_R500_PH_SHORT (rare)
  L3 Tier A LONG (StE)   → 기존 BURN_REV (별도)
  S2 Tier A SHORT (StE)  → 기존 BURN_S (별도)
  스캘프 (사용자 직관)   → MNQ_SCALP_LIGHT_A
```

---

## ⚠️ Caveats

### 1. AAL_v5_RoundShort
- **Live ≠ backtest**. P3 PF 4.56 sim → live 1.5-3.0 추정
- Sim 4주 → PF < 1.5 시 즉시 중단
- Tight SL (18 ticks) — noise stop-out 발생 가능

### 2. AAL_v5_KSTHour
- KST 04:30 + Squeeze GUARD: small N (80) — 추가 검증 필요
- KST 20-22 단독 SHORT 진입 절대 금지 (raw signal 강해도 sim LOSE)
- ATR z 60-day rolling = warmup 1500+ bars 필요 (5m 5일+)

### 3. ATM Templates
- XML format은 NT8 버전에 따라 약간 다를 수 있음 → GUI 로 검증 권장
- BreakEven Plus 4 ticks = +1 pt (commission RT $2.18 차감 reference)

---

## 📁 GitHub 사본

- 본 폴더 = NT8 documents 폴더 사본 (배포용)
- 원본: `c:/Users/minb0/OneDrive/문서/NinjaTrader 8/`

업데이트 흐름:
1. NT8 documents 에서 .cs / .xml 수정
2. 본 폴더에 cp
3. Git commit + push

---

## 🔗 관련 자료

- [Pine v5.1 (MNQ_All_v5.pine)](../pine/MNQ_All_v5.pine) — 동일 기능 Pine 버전
- [Phase G3 Report](../research/PHASE_G3_REPORT.md) — R500 SHORT ATM grid 검증
- [Phase F Report](../research/PHASE_F_REPORT.md) — BURN_X ATM optimization
- [Master Report](../research/MASTER_REPORT.md) — 전체 검증 종합
- [Pine v5 통찰 교재 HTML](../pine_insights.html) — 12 insights detail
