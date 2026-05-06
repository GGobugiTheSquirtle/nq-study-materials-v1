# Week 10: ICT FVG/OB 인식 (사용 X, 인식만)

> **목표**: Fair Value Gap (FVG) 와 Order Block (OB) 식별. **사용은 안 함** — 다른 트레이더 차트 reading + 우리가 검증해서 REJECT 한 이유 이해.
> **기간**: 5 sim 세션 (가벼움)
> **전제**: W9 4점+

---

## 1. 핵심 개념 (15분)

### ⚠️ 우리는 ICT 를 안 쓴다 — 그러나 안다

**우리 검증 결과 (HYP-CONF-001)**:
- BTC standalone FVG/OB: 0/20 (REJECTED)
- LONG_DOWN_BOUNCE_v2 confluence: 0/3 (ΔWR -2.4~-4.7pp, p ≥ 0.67)
- → **edge 없음**, REJECTED

**그래도 배우는 이유**:
1. 다른 트레이더 차트 reading (커뮤니티 노이즈 면역)
2. 사용자 차트 도구 reference (TV 에서 자주 그어짐)
3. "왜 안 통하는지" 직관 ↔ 데이터 이해

### Fair Value Gap (FVG)

```
3-candle imbalance:

Bar 1: ┌───┐
       │   │
       │ ▲ │ ← high
       └─┬─┘  
         │  
Bar 2:   │  ┌──────┐
         │  │ Wide │  ← 큰 추진 봉
         │  │ Body │
         │  └──────┘
         │      
         └──── Bar 1 high < Bar 3 low ⇒ Gap (FVG)
              (gap = imbalance, 다시 채울 가능성)
              
Bar 3:           ┌───┐
                 │ ▼ │  ← low
                 └─┬─┘
                   │
                   └─ low > Bar 1 high

→ FVG = Bar 1 high ~ Bar 3 low 사이 gap
→ "Fair value" 채우러 다시 옴 (가설)
```

식별:
- Bullish FVG: Bar 1 high < Bar 3 low (gap up)
- Bearish FVG: Bar 1 low > Bar 3 high (gap down)
- 채워진 FVG = 무효
- 미채움 FVG = 미래 SR

### Order Block (OB)

```
Bullish OB = 강한 상승 직전 마지막 음봉

      ┌──────┐
      │ 강한 │  ← 강한 상승 (impulsive)
      │ 상승 │
      ┌─┴──┐ │
      │ ▼  │ │  ← 마지막 음봉 = Bullish OB
      └────┘ ┘   (미래 support 역할)
      
Bearish OB = 강한 하락 직전 마지막 양봉 (대칭)
```

식별:
- "마지막 반대 색 캔들 직후 강한 추진"
- OB body + 꼬리 절반 = SR zone (W3 에서 언급)
- Mitigation = OB 다시 touch 후 반등 (가설)

### 왜 우리는 사용 안 하나?

**측정 결과 (BTC, NQ 둘 다)**:
1. **Standalone**: WR 50% 안팎 (random)
2. **Confluence (Tier 1+2 결합)**: ΔWR 미미 (-2pp ~ +1pp), 통계적 무의미
3. **Pattern matching 가능**: 후행적 식별 (post-hoc) 만 됨, real-time 미달

**그러나 ICT 가 인기 있는 이유**:
- 시각적 명료 (그릴 수 있는 box)
- 후행적 차트 봤을 때 "맞은 것 같다" 효과 (survivorship bias)
- 커뮤니티 / SNS 영향 (Michael J. Huddleston aka ICT 본인)

→ **반례를 알면 면역됨**. 다른 트레이더가 "FVG 채우러 가야 함" 말할 때 "통계적 무의미" 알고 있어야.

### 사용자 가치

❌ **ICT 차트 보고 추가 fee 결제, 강의 구독**
✅ **무료 인식 → 면역**

❌ **FVG/OB 만 보고 진입 (no Tier 1+2)**
✅ **Tier 1+2 setup 우선, FVG/OB = 보조 마킹만**

❌ **"FVG 채우러 가야 한다" 확신**
✅ **확률적 표현 — "FVG 가 SR 일 수 있다, 그러나 보장 X"**

### 더 깊이

- **NotebookLM**: "ICT FVG OB + ICT Part 1+2+3" + "SMC 전략편" cross-query (사용자 1,090 source 중 452 ICT)
- **detail.md**: `04_ict_smc/detail.md` (ICT Michael Huddleston / SMC Mentfx)
- **반례 검증**: `f:/Apps_home/퀀트 리서트 v2/btc_trader/research/...` HYP-CONF-001 보고서

---

## 2. 차트 관찰 과제 (매일 5분)

### 매일 5분 루틴

1. NQ 5m + 모든 prior 마킹
2. **FVG / OB 식별** (자동 indicator OK)
3. 마킹된 FVG/OB 의 미래 hit 여부 추적 (1주 누적)
4. **Tier 1+2 setup 과 ICT 일치/불일치** 비교
5. observation_log 에 hit ratio 기록

### TV setup

- "ICT Order Blocks" indicator (community, 무료) — 자동 식별
- "Fair Value Gap" indicator (community)
- Pivot Points 와 결합

### 체크리스트

- [ ] FVG 식별
- [ ] OB 식별
- [ ] FVG/OB hit / unfilled 추적
- [ ] Tier 1+2 결합 시 추가 가치 self-judge

### 1주 후 self-experiment

```
50 FVG 마킹 → 1주일 후 hit rate 측정
50 OB 마킹 → 1주일 후 hit rate 측정

기대 결과: hit rate 50% 안팎 (random)
→ "ICT 가 random 보다 나을 게 없음" 직접 검증
```

---

## 3. 일지 마킹

JSON 추가 (참고용, 진입 trigger 아님):

```json
{
  ...,
  "ict_w10_fvg_near": "yes (within 0.5 ATR) / no",
  "ict_w10_ob_near": "yes / no",
  "ict_w10_used_for_entry": "no (always)" 
}
```

**진입 룰**:
- ICT signal **단독으로 진입 금지**
- Tier 1+2 setup 통과 + ICT confluence = 사이즈 보통 (사이즈 boost X)
- ICT 만 있고 Tier 1+2 미달 = **skip**

---

## 4. 성공 기준

| 기준 | 합격선 |
|---|---|
| FVG/OB 식별 정확 | 80%+ (시각 단순) |
| ICT 단독 진입 | 0회 |
| Tier 1+2 + ICT confluence 효과 self-측정 | 1주 hit rate 기록 |

---

## 5. 다음 주 연결 (W11)

W10 = "참고 도구" (인식만)
W11 = **우리 핵심 edge 04:30 BURN_X** ⭐⭐⭐⭐⭐

→ Tier 1+2+W9 통과한 자기에게 진짜 수익 거리.

---

## 6. Pre-Session Card 진화

```
W10 추가 (선택, 안 추가도 OK):
□ FVG/OB confluence 있는가? (참고만)
```

→ Pre-Entry Card 에 추가 부담 X. ICT 는 trigger 아님.

---

## 7. 권위자 인용 (양쪽)

**찬성 (ICT 측)**:
> "FVG 는 institutional algo 의 발자취 — 항상 채우러 온다."
> — Michael J. Huddleston (ICT)

**반대 (검증 측)**:
> "Pattern recognition without statistical validation = pareidolia."
> — Statistical Trading literature (paraphrase)

**우리 입장**:
> "FVG/OB 자체가 random 이 아닌 것은 사실. 그러나 trading edge 가 되기엔 통계적 효과 미달."
> — HYP-CONF-001 (2026-04-30)

---

## 📌 Common Mistakes

| 실수 | 처방 |
|---|---|
| ICT 만 보고 진입 | Tier 1+2 우선 |
| FVG 자동 채움 확신 | 확률적 — hit rate 50% |
| ICT 강의 / 시그널 구독 | 무료 인식만으로 충분 |

---

## 📚 원본 소스 바로가기 (직접 click) — 인식만, 사용 X

### 영상 / 채널 — Original
- [Michael J. Huddleston (ICT 본인)](https://www.youtube.com/@InnerCircleTrader) ⭐⭐⭐ — ICT 1차 source. **무료** (수백 영상)
- [The Trading Channel — Patrick Wieland](https://www.youtube.com/@TheTradingChannel) ⭐⭐⭐ — ICT 단순화 + daily 분석
- [Stacey Burke (ICT mentee, NQ daily)](https://www.youtube.com/@StaceyBurkeTrading) ⭐⭐⭐ — daily NQ + ICT concepts
- [Wysetrade — Riccardo Sturla (5-step sniper)](https://www.youtube.com/@Wysetrade) ⭐⭐ — ICT 단순화

### 책 / Free PDF
- [ICT Concepts PDF (커뮤니티 정리)](https://www.google.com/search?q=ICT+concepts+pdf+inner+circle+trader) — 검색 (무료 PDF 다수)
- [TradingView ICT indicators](https://www.tradingview.com/script/?text=ICT+order+block) — 자동 식별 community indicators

### 우리 검증 (REJECTED 결과)
- [HYP-CONF-001 보고서 (BTC FVG/OB 0/20)](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1) — 사용자 자체 검증
- 핵심 결론: **standalone 0% edge, confluence 통계적 무의미** → 사용 X, 인식만
- "왜 안 통하는지" 1주 self-experiment (50 FVG mark → 1주 후 hit rate 측정)

### NotebookLM 검색 — **사용자 1,090 source 중 452가 ICT** (가장 큰 집합)
- 🆕 [영어 권위자 notebook](https://notebooklm.google.com/notebook/81fe9110-dfe2-4b64-bcd6-c221c36d84c6)
- 사용자 보유 ICT notebook (notebooklm.google.com 검색):
  - **ICT Part 1+2+3 (156 source)**
  - **ICT 유니버설 (197 source)**
  - **SMC 전략편 Courses+Crypto (95 source)**
- 추천 query: `"FVG OB hit rate edge validation"` (REJECTED 결과 확인)
- 추천 query: `"Order Block fair value gap pattern recognition"` (인식만)

### 카테고리 sources.md
- [04 ICT/SMC sources ⭐⭐⭐](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1/blob/main/04_ict_smc/sources.md) — 완전 목록
- [04 detail.md](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1/blob/main/04_ict_smc/detail.md)

### ⚠️ Caveat
- ICT 컨텐츠는 **quality variance 큼**. cult-language / 과장 win rate 일부.
- 학습 목표 = "왜 random 인지 이해 + 다른 트레이더 차트 reading 가능" 만.

---

*W10 시작: W9 통과 후 / 가벼운 주, 5 세션 후 진행*
