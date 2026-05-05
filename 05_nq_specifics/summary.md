# 05 — NQ 특화 / Index Futures — 핵심 정리

> **사용자 검증 자료 활용**: KST 21~23 NY open 핫스팟, 22:30 WILD CHOP, 23:30 TREND BURST (LEARNINGS_NQ.md L35).
>
> **외부 source 가 사용자 본인 데이터 보강**.

---

## 🎯 핵심 명제 5가지

### 1. NQ 의 시간대 특성 (사용자 데이터 + SMB Capital + ICT)

**NQ = 나스닥 100 E-mini Futures** (CME):
- ETH (Electronic Trading Hours): 거의 24시간 (KST 07:00 ~ 다음날 05:45, 1h 휴장)
- RTH (Regular Trading Hours): NY 09:30~16:00 = KST 22:30~05:00
- ETH 와 RTH 의 행동 차이가 핵심

**시간대별 핵심 (사용자 본인 검증 + 외부 일치)**:

| KST | 의미 | Action 권장 |
|---|---|---|
| 07:00~16:00 | Asia + EU pre-market | DEAD ZONE — 진입 X |
| 16:00~22:00 | EU session 활성 | 단조로운 추세 가능 |
| **22:30** | **NY RTH open** | **WILD CHOP** — 첫 30분 fake move (사용자 자체 검증) |
| **23:00~23:30** | first hour transition | **TREND BURST** — real move 시작 (Linda Raschke "first hour") |
| 00:00~02:00 | Lunch + reversal | mixed |
| 02:00~04:00 | Last hour | high vol fading |
| 05:00~05:45 | RTH close approach | EOD positioning |
| 05:45 sharp | RTH close | AutoLiq for many prop firms |

**SMB Capital + Mike Bellafiore 보강**:
- "First hour" (NY open 첫 시간) = 가장 자주 언급되는 trade window
- Opening range = 첫 5-30분의 high/low → break/fail = 매매 신호
- Initial Balance (IB) = NY RTH 첫 1시간 의 high/low → IB 돌파 후 retest = 진입

---

### 2. Opening Range Trading (Mark Fisher "ACD")

**Mark Fisher, "The Logical Trader"**:
- Opening Range (OR) = NY RTH 첫 5-15분의 high/low
- A-up: OR high 위로 break
- A-down: OR low 아래로 break
- C-up / C-down: A break 후 반대 방향 fail (= 위험 신호)

**NQ 적용**:
- 22:30 KST OR (5분) 정의
- 22:35 부터 A-up / A-down 신호 monitor
- C 신호 = top buying / bottom selling 의 함정 = 회피

**사용자 직접 적용**:
- 사용자 22:30 시간대 = OR 정의 시간
- 사용자 LONG bias = A-down (OR 아래 break) 무시 → counter-trend trap
- → A 방향과 본인 thesis 일치 시에만 진입 룰 추가 가능

---

### 3. AVWAP — Anchored VWAP (Brian Shannon)

**Brian Shannon, alphatrends.net**:
- VWAP = volume-weighted average price (intraday)
- AVWAP = "anchored" VWAP — 특정 시점부터 시작
- 핵심 anchor 시점:
  - 오늘 RTH open
  - 직전 swing high/low
  - 주요 뉴스 시점 (FOMC, CPI 발표 직후)
  - 주요 갭 시작 시점

**NQ 적용**:
- RTH open AVWAP = institutional buy/sell 평균 가격 = 강력 reference level
- 가격이 AVWAP 위 = bullish bias / 아래 = bearish bias
- AVWAP 터치 후 반등/반락 = 진입 자리

**사용자 직접 적용**:
- 22:30 RTH open AVWAP = 매일 자동 reference level
- 사용자 차트에 AVWAP 추가 권장 (TradingView 무료 indicator)
- AVWAP 위 LONG 만 / 아래 SHORT 만 = bias filter

---

### 4. Internals — TICK / ADD / VOLD

**SMB Capital + Brett Steenbarger**:
- **TICK** (NYSE TICK Index): 현재 +tick 종목 - -tick 종목 차이
  - +1000 이상 = 강력 buying
  - -1000 이하 = 강력 selling
- **ADD** (Advance-Decline): NYSE 상승/하락 종목 차이
- **VOLD** (Volume Differential): up volume - down volume

**NQ 의 한계**:
- NYSE TICK 은 NYSE 종목 → NASDAQ-100 (NQ 추종) 와 직접 매치 X
- **NQTICK** (NASDAQ TICK) 또는 **$ESINX** (S&P internals proxy) 사용 가능
- TradingView 에서 무료 access

**활용**:
- TICK +1000 + 가격 LONG 진입 = confluence
- TICK 약화 (직전 high 대비) + 가격 LONG = divergence = 위험 (top buying 신호)

---

### 5. Internals & Macro Context

**Macro Background (사용자 룰 R11 보강)**:
- **VIX** (volatility index): NQ 와 negative correlation
  - VIX 급등 = NQ 하락 가능
  - 매매 전 VIX 확인 권장
- **DXY** (US Dollar Index): NQ 와 weak negative correlation
- **10Y Yield** (TNX): NQ 와 weak negative correlation (특히 tech)
- **Fed Funds Futures**: rate expectation 변화 시 NQ 큰 움직임

**Economic Calendar Block (사용자 R11)**:
- CPI / NFP / FOMC / PPI / FOMC minutes = NQ 큰 움직임 trigger
- 발표 ±30분 진입 X (R11)
- 발표 후 5-10분 = volatility spike → fake move 다수

**사용자 직접 적용**:
- 매 세션 시작 전 30초 macro check:
  - VIX 수준 (15 이하 = calm / 25+ = 변동성 높음)
  - DXY 방향
  - 오늘 economic event (calendar)
- 1개라도 abnormal = size ↓ 또는 진입 X

---

## 📋 사용자 약점 → 직접 처방

| 사용자 약점 | 처방 | 출처 |
|---|---|---|
| 시간대 ignore | Kill zone / NY open / IB 사용 | SMB + ICT |
| Top buying | OR break + retest 후 진입 (A-up retest) | Mark Fisher ACD |
| 흐름 read 부재 | AVWAP 보조 reference + TICK confluence | Brian Shannon + SMB |
| 변동성 인지 부재 | VIX + economic calendar pre-check | macro |
| 짤짤이 = NY first hour 핫스팟 | 22:30~23:30 KST 만 활성 | 사용자 + 외부 일치 |

---

## 📚 권장 학습 순서

### Week 1 — 시간대 + Opening Range
1. **Mark Fisher — "The Logical Trader" (책)** + ACD 시스템
2. **SMB Capital — "One Good Trade" Ch. 1-3** (책)
3. **SMB Capital YouTube — opening range / first hour playlist**

### Week 2 — AVWAP
4. **Brian Shannon — AVWAP 영상 5-10개** ([@AlphatrendsTV](https://www.youtube.com/@AlphatrendsTV))
5. **alphatrends.net 핵심 글**

### Week 3 — Internals
6. **SMB Capital — TICK / VOLD 영상**
7. **Brett Steenbarger — TICK divergence 글** (TraderFeed)

### Week 4 — Macro + Practical
8. **Adam Mancini Twitter** ([@AdamMancini4](https://x.com/AdamMancini4)) — 매일 NQ levels
9. **CME Group Educational Materials** ([cmegroup.com/education](https://www.cmegroup.com/education.html))

---

## 🎬 핵심 영상 / 자료 직링크

| # | 자료 | 비고 |
|---|---|---|
| W1 | [SMB Capital website](https://smbcap.com/) | One Good Trade / The PlayBook |
| W2 | [alphatrends.net](https://www.alphatrends.net/) | AVWAP Brian Shannon |
| W3 | [Adam Mancini Twitter](https://x.com/AdamMancini4) | 매일 NQ levels |
| W4 | [CME Group Education](https://www.cmegroup.com/education.html) | NQ mechanics |
| V1 | [Mike Bellafiore SMB interview](https://www.youtube.com/watch?v=CWQB1vE_qfM) | prop firm intro |

---

## 💎 핵심 명언

### Mike Bellafiore (SMB)
- "One good trade. That's all you need today."
- "Playbook = process + setup + risk + outcome. Repeat."
- "Pros trade fewer, better. Beginners trade more, worse."

### Brian Shannon (AVWAP)
- "Only money matters. Volume-weighted price = where money is. Trade with money."
- "AVWAP from key anchors = institutional reference."

### Mark Fisher (ACD)
- "Opening range = market's opening statement. Listen first."
- "A breakout, then C failure, watch for reversal."

### Adam Mancini
- "Levels are levels. Don't predict — react at the level."

---

## 📝 사용자 매매 직접 적용 — NQ 7-Step Daily

```
[Pre-Session NQ Check — 5분]
1. □ Macro: VIX, DXY, 10Y Yield 확인
2. □ Economic Calendar: 오늘 발표 (FOMC/CPI/NFP)?
3. □ HTF: 1h, 4h NQ trend (HH+HL or LH+LL)
4. □ Daily levels (Adam Mancini Twitter): 주요 SR 표시
5. □ AVWAP from RTH open (22:30 KST) — anchor 표시
6. □ Opening Range: 22:30~22:35 첫 5분의 high/low 기록
7. □ A break direction: 22:35+ break 방향과 본인 thesis 일치 여부
```

---

## 🔗 NotebookLM 후속 query

1. "NQ NY open 22:30~23:30 KST 에 가장 자주 발생하는 setup 3가지"
2. "AVWAP 와 Adam Mancini levels 결합 시 entry 룰"
3. "TICK divergence 가 NQ top buying 회피에 어떻게 사용되는가"

---

*Status: Phase 1C draft (5/6). 다음: 06 Scalping*
