# 03 — Trend Following / Pullback Entry — DETAIL (핵심 추출)

> 자기충족적 교재. Curtis Faith Turtle / Linda Raschke / Adam Grimes / Stan Weinstein / Tom Hougaard trail / Michael Covel 핵심 + 사용자 약점 처방.

---

## 1. Curtis Faith — Original Turtle Rules

### 1.1 Turtle 의 핵심 철학

> ❝ If you can follow the rules, you can be a turtle. The rules are 100% mechanical. ❞
> — Way of the Turtle, Ch. 1

**4가지 핵심**:
1. **Markets**: liquid futures only (NQ 적합)
2. **Position Sizing**: ATR-based (N system)
3. **Entries**: Donchian breakout (20일 high/low)
4. **Exits**: Trail stop (10일 low for long)

### 1.2 The N System (Position Sizing)

> N = 20-day Average True Range (ATR)
> Position size = (1% account risk) / N

**예시 (사용자 NQ 적용)**:
- 계좌 $50,000 / 1% risk = $500
- N (20-day ATR) ≈ 100 NQ points = $2,000 per contract
- Position size = $500 / $2,000 = 0.25 contracts (1ct 도 안 되는 micro-NQ 수준)
- → **사용자 sim 30ct = N system 의 ~120x.** 사용자 size 가 sim only 라는 정량 검증.

**적용**:
- N system = 사용자 R34 (Sim Position Cap) 의 정확한 외부 source
- N 기반 sizing = 모든 trade 의 risk 동일 = 사이즈 욕심 차단

### 1.3 Donchian Breakout (Entry)

```
System 1: 20-day high (long) / 20-day low (short)
System 2: 55-day high (long) / 55-day low (short) [missed S1 trades]
```

**사용자 적용 (5m 차트 변형)**:
- 5m 차트에서 240-bar (20시간 ≈ 1일) high/low 사용
- 단순화: 직전 swing high break = entry trigger
- → 사용자 pullback entry 와 보완 가능

### 1.4 Pyramiding Rules (winners 키우기)

> Add 1 unit at every 1/2 N of profit, up to 4 units max.

**사용자 약점 직접 처방 — 추세 끝까지 못 봄**:
- 사용자 자가: "추세 잡아도 진득히 못 봄 — 짤짤이 치다 짐"
- Turtle 의 답: 진입 후 +0.5N → add 1 unit. +1.0N → add 1. +1.5N → add 1.
- = winner 키우는 정량 시스템. 의지 X, 룰 O.
- **사용자 R20 (TPA) 와 정확히 동일 컨셉**.

### 1.5 Cut Rules (losers 끊기)

> Initial SL = 2N from entry
> Trailing exit = 10-day low (long) — turtle 의 "system 1" exit

**핵심 원칙**:
- SL 도달 = 즉시 cut. 망설임 0.
- "If signal then enter. If stop then exit. No exceptions."
- = Hougaard "Best Loser" 와 동일

---

## 2. Linda Raschke — "Street Smarts"

### 2.1 The "First Hour" Concept

Linda Raschke (전 floor trader): NY first hour = 매매의 황금 시간.

> ❝ The first hour reveals the market's intent. Trade the rest of the day in that direction. ❞

**사용자 적용**:
- KST 22:30~23:30 = NY first hour (사용자 검증 일치)
- 사용자 L35 TIME-VOL MAP 와 정확히 일치

### 2.2 Holy Grail (ADX + 20EMA) — 사용자 ADR-028 REJECTED 컨셉

**원본 룰**:
```
1. ADX > 30 (trend mode)
2. 가격이 20EMA 터치 (pullback)
3. ADX 유지 + EMA 터치 → entry
4. SL = 직전 swing low/high
5. Target = previous extreme
```

**사용자 ADR-028 결과**:
- NQ 10y backtest: stride bug 후 REJECTED
- 1차 +51% Sharpe = stride artifact 였음

**그러나 컨셉 자체는 valid** (다른 시장 / 다른 TF 에서 가능). 사용자 NQ 5m 에서 변형 backtest 가능.

### 2.3 The 80-20 Pattern (Reversal)

```
1. 어제 close 의 80% 하락 (open 보다 80% 하락한 자리)
2. 20% 반등 (반등 시작 신호)
3. → LONG entry candidate
```

**사용자 적용**: 5m 변형 가능. 매일 day's range 80% 하락 후 반등 = 단기 LONG.

### 2.4 The Anti Pattern (Counter-Trend Scalp)

> ❝ Anti = quick scalp against trend, then back to trend. Never hold counter-trend. ❞

**핵심**:
- 추세 = LONG (HTF)
- LTF pullback 중 = quick SHORT scalp (short hold)
- LTF pullback 끝 = 다시 LONG (main 방향)

**사용자 약점 직접 처방 — Counter-trend 진입**:
- 05-05 Phase B (-$406 SHORT 14ct) = counter-trend hold
- Linda 의 답: counter-trend = scalp only (sub-2min). hold X. Anti pattern 룰.

### 2.5 Linda 의 5 매매 원칙

> 1. Manage risk. Always know your max loss before entry.
> 2. Trade with the trend (HTF).
> 3. Anti = scalp only, never hold.
> 4. Add to winners, never to losers.
> 5. Take partial profits at first target.

---

## 3. Adam Grimes — Measurable Pullback Patterns (Continuation from Cat. 02)

### 3.1 The 5 Pullback Patterns (정량)

#### Pattern 1: First Pullback After BOS (가장 강력)
- **WR**: 65-75%
- **Definition**: BOS 후 첫 HL (or LH for short)
- **Entry**: HL reversal bar close
- **SL**: HL 아래 ATR × 1.5

#### Pattern 2: EMA20 Pullback (Trend strong)
- **WR**: 60-70%
- **Definition**: 가격이 EMA20 까지만 되돌림 (depth 50% 이하)
- **Entry**: EMA20 touch + reversal bar
- **SL**: EMA20 아래 ATR × 1

#### Pattern 3: AB=CD Symmetric
- **WR**: 55-65%
- **Definition**: 첫 impulse (A→B), pullback (B→C), 두 번째 impulse (C→D) 같은 size
- **Entry**: D 도달 시
- **SL**: D 너머

#### Pattern 4: Failed Test (Reversal)
- **Definition**: pullback 깊다가 reversal — Wyckoff Spring 과 동일
- **WR**: 50-60% (low) but R:R 1:3+

#### Pattern 5: Time Pullback
- **Definition**: 가격 아니라 시간 (2-5 candles) 의 pullback
- **Entry**: 5 candles 동안 sideways → trend resumption candle

### 3.2 Pullback 깊이 vs WR

> 깊은 pullback (50% 이상 depth) = WR 낮음
> 얕은 pullback (30% 이하 depth) = WR 높음, 진입 자리 적음

**사용자 적용**:
- Pattern 1 (first pullback after BOS) = 사용자 매매에 가장 적합
- 사용자 차트에 BOS / HL 표시 → entry candidate 식별

---

## 4. Stan Weinstein — Stage Analysis

### 4.1 4 Stages (HTF Context)

> Stage 1: Sideways accumulation (low base)
> Stage 2: Markup (uptrend) ⭐ TRADE
> Stage 3: Sideways distribution (high base)
> Stage 4: Markdown (downtrend) ⭐ TRADE
>
> — Secrets for Profiting in Bull and Bear Markets, Ch. 1

**핵심**: Stage 2 (uptrend) 와 Stage 4 (downtrend) 만 매매. Stage 1/3 (sideways) = 진입 X.

**사용자 적용**:
- HTF (1h, 4h) Stage 분석 매일 1회
- Stage 1/3 = chop = 진입 보류
- Stage 2/4 = trend = entry candidate

### 4.2 Weekly Chart Bias

Weinstein: weekly chart 의 30-week MA (≈ 200-day) = stage 결정자.

- Price > 30W MA + MA 상승 = Stage 2
- Price < 30W MA + MA 하락 = Stage 4

**사용자 NQ 적용 (5m 변형)**:
- 5m 차트에서 EMA200 (≈ 1000 minutes ≈ 17h) 사용
- Price > EMA200 + EMA 상승 = micro Stage 2
- → 사용자 R26 (Trend-First) 와 호환

---

## 5. Tom Hougaard — Trail Stop / Wide Win

(§ 01 Psychology 와 중복, trend-following 측면 강조)

### 5.1 The Wide Win Mechanism

> ❝ Most traders take profits too quickly. They cut their winners at +5R when the trend has +50R left. ❞

**핵심**: trend 잡으면 trail. partial 만 take, position 전부 close X.

### 5.2 Trail Stop Strategy (Hougaard 권장)

```
Stage 1 (entry): SL = 2 × ATR
Stage 2 (+1R): SL → BE
Stage 3 (+2R): partial 1/3 take, SL → +0.5R
Stage 4 (+3R): partial 1/3 take, SL → +1.5R (trail)
Stage 5 (+5R+): trail by 1 × ATR continuously
```

**사용자 표준 ratchet (CLAUDE.md) 와 호환**:
```
Stage 0 (entry):       SL = entry - 1.5×ATR
Stage 1 (+0.4R):   SL → entry (BE)
Stage 2 (+0.8R):   SL → entry + 0.3R
Stage 3 (+1.2R):   SL → entry + 0.6R, partial TP 50%
Stage 4 (+1.6R):   trail by 0.8×ATR dynamic
```

→ 사용자 standard 가 더 보수적 (earlier BE, smaller R triggers). 데이트레이딩 적합. trend 큰 swing 잡으려면 Hougaard 시스템 더 적합.

---

## 6. Michael Covel — Trend Following Philosophy

### 6.1 Why Trend Following Works

> ❝ Trend following is uncomfortable. You miss the start, miss the end, only catch the middle. But the middle is where the money is. ❞
> — Trend Following (Covel)

**핵심 원칙**:
1. **Markets trend 30-40% of time** — 장기적 truth
2. **You cannot predict trend** — 시작점 모름
3. **You can react to trend** — 시작 후 진입
4. **Big trends pay for many small losses** — Win rate 30-40% 도 PF > 1.5 가능 (skewed distribution)

### 6.2 Trend Follower 의 Mental Profile

Covel 의 인터뷰 정리:
- Patient (인내) — trend 시작 기다림
- Disciplined (룰 준수) — emotion 무관 실행
- Comfortable with uncertainty (불확실성 수용) — 미래 모름
- Loss-tolerant (손실 수용) — small loss 자주

**Best Trend Followers (Covel 인터뷰)**:
- Ed Seykota
- Bill Dunn
- John W. Henry
- David Harding (Winton)
- Andrea Unger (단기 변형)

---

## 7. 사용자 약점 → 권위자별 처방 매트릭스

| 약점 | Curtis Faith | Linda Raschke | Adam Grimes | Stan Weinstein | Tom Hougaard | Covel |
|---|---|---|---|---|---|---|
| Top buy vs pullback 혼동 | Donchian breakout 정의 | first hour direction | first pullback after BOS | Stage 2/4 만 trade | (간접) | (철학) |
| 추세 끝까지 못 봄 | Pyramid + trail | (직접 X) | trail rules | Stage 끝 인식 | wide win mechanism | "middle is the money" |
| Winner 짧게 끊음 | Pyramid + 10-day low exit | (직접 X) | trail by ATR | (직접 X) | partial only, trail rest | comfortable with uncertainty |
| 사이즈 욕심 / 물타기 | N system / pyramid only on profit | "add to winners not losers" | (간접) | (직접 X) | (간접) | (철학) |
| 룰 위반 (감정) | "If signal then enter" | (직접 X) | objective only | (직접 X) | (간접) | "uncomfortable but disciplined" |
| Counter-trend 진입 | (직접 X) | Anti = scalp only | (간접) | Stage 안 맞으면 X | (직접 X) | "trend with HTF" |
| 시간대 ignore | (직접 X) | first hour | (간접) | weekly chart | (간접) | (철학) |

---

## 8. 명언 30선 (출처 명시)

### Curtis Faith (Turtle)
1. "If you can follow the rules, you can be a turtle."
2. "When in doubt, do nothing."
3. "Pyramid winners, never losers."
4. "Trade the system, not the market."

### Linda Raschke
5. "The best traders manage risk. The rest are gamblers."
6. "Anti = quick scalp against trend. Never hold counter-trend."
7. "Holy Grail = ADX + EMA. Wait for trend, then for pullback."
8. "First hour reveals the day's intent."

### Adam Grimes
9. "First pullback is the trade. After that, you're chasing."
10. "Measurable patterns or it's not a pattern."
11. "Edge = process. Process = backtest + execute."
12. "Shallow pullback = high WR, fewer setups. Choose."

### Stan Weinstein
13. "Stage 2 or Stage 4. Never Stage 1 or Stage 3."
14. "Don't fight the tape. Don't fight the Fed."
15. "Weekly chart for context. Daily for entry."

### Tom Hougaard (trend-following 측면)
16. "Most traders cut winners at +5R when trend has +50R."
17. "Tight loss, wide win. Always."
18. "Trail with the trend, not your hopes."

### Michael Covel
19. "Trend following is uncomfortable. The middle is where the money is."
20. "You cannot predict. You can only react."
21. "Big trends pay for many small losses."

---

## 9. 학습 일정 (5주 페이스)

### Week 1: Curtis Faith Turtle System
- Day 1-2: §1.1-1.2 (Turtle 철학 + N system)
- Day 3-4: §1.3-1.4 (Donchian + Pyramid)
- Day 5-7: §1.5 (Cut rules) + Original Turtle Rules PDF read

### Week 2: Linda Raschke + Adam Grimes
- Day 1-2: §2 (Linda 5 원칙)
- Day 3-4: §3 (Grimes 5 pullback patterns)
- Day 5-7: 사용자 NQ 차트에 first pullback after BOS 마크

### Week 3: Stan Weinstein Stage Analysis
- Day 1-2: §4 (4 stages)
- Day 3-4: weekly + daily chart context 분석
- Day 5-7: 본인 NQ 매매에 stage 적용

### Week 4: Tom Hougaard Trail + Covel Philosophy
- Day 1-3: §5 (Hougaard trail stop strategy)
- Day 4-5: §6 (Covel philosophy)
- Day 6-7: 사용자 ratchet vs Hougaard ratchet 비교 + 적용 결정

### Week 5+: 실전 적용
- 매주 1-2 trade = first pullback after BOS only
- Trail stop 룰 적용 (winner 끝까지 hold)
- 4주 누적 후 본인 trend-following metric 검증

---

## 10. 한계 / 보강

이 detail.md 의 한계:
1. Linda Raschke 의 multiple patterns (Anti, 80-20, 3-bar swing 등) 일부만
2. Curtis Faith 의 system 2 (55-day breakout) 자세히 X
3. Adam Grimes 의 measurable filter (volume, ATR 등) 결합 X

보강:
- NotebookLM "보조지표편 - Strategies" (37) cross-query
- NotebookLM "데이트레이딩편" (29) query

---

*Status: detail.md 3/6 완료.*

---

# 📚 Extended Section (v1.1 보강, 2026-05-06)

## 11. 추가 권위자 — Ed Seykota + Bill Dunn + Jerry Parker

### 11.1 Ed Seykota — Trend Following Legend

> ❝ The trend is your friend. The end of the trend is your enemy. ❞
> ❝ Risk no more than you can afford to lose. Risk enough that winning is meaningful. ❞

**Seykota 의 5 원칙** (Schwager Market Wizards 인터뷰):
1. **Cut losses** — 모든 trader 의 첫 룰
2. **Ride winners** — 둘째 룰
3. **Keep bets small** — 셋째 룰
4. **Follow rules without question** — 넷째 룰
5. **Know when to break the rules** — 다섯째 룰 (가장 어려움 — 시스템 무효 인지)

**사용자 적용**:
- #4 = R29-R35 룰 시스템 정확 일치
- #5 = 사용자 매매일지 weekly review 의 "rule violation 분석" 부분

### 11.2 Bill Dunn — Long-term Trend Follower

**Dunn Capital** 의 25년 운영 통계:
- Win rate: ~35-40%
- PF: 1.6-2.0
- MDD: 30-40% (long-term)
- Sharpe: 1.0-1.4

→ **trend following 의 현실 metric**. 사용자 R29 (sim PF 2.27 from 1 day) 의 vs 25년 PF 1.6 비교 시 — 사용자 단기 매매가 fundamentally 다른 game.

### 11.3 Jerry Parker — Original Turtle (Faith 시리즈)

**Parker 의 핵심 통찰** (Curtis Faith 보다 더 오래 운영):
- "Volatility 가 entry signal" (volatility breakout)
- "Long-term trend 만 trade" (5-10 year horizons)
- "Discretion = the enemy" (rule based 100%)

→ 사용자 단기 NQ 매매와 long-term trend following 은 다른 strategy. **하지만 mental framework 는 동일** — rule-based, cut quickly, ride winners.

---

## 12. 한국어 자료 — 보조지표편 Strategies (NotebookLM 37 source) + 데이트레이딩편 (29 source)

**한국어 trend following 컨셉**:
- "추세 추종 = 인내" (사용자 L41 selectivity 와 호환)
- "거래량 기반 trend 확인" (VSA 한국어 버전)
- "시간 기반 hold rule" (R31 의 한국어 source)

→ NotebookLM cross_query: "한국어 자료의 trend pullback entry 와 Adam Grimes first pullback after BOS 비교"

---

## 13. 사용자 매매일지 Case Mapping (05-05 Phase 4 cluster #31)

### Day's Best — Cluster #31 (LONG 115ct, 4min hold, +$4,553)

**Phase 4 의 cluster #31** = day 최고 결과:
- Entry: 28039 (post-breakout continuation)
- Exit: 28069
- 4min hold, 30pt move
- Net: +$4,553 (sim, 28ct after sizing)

**Trend follower lens 진단**:

| 권위자 | 평가 |
|---|---|
| Curtis Faith (Turtle) | "Donchian breakout confirmed — pyramid OK" |
| Linda Raschke | "First hour direction respected — long bias confirmed" |
| Adam Grimes | "Post-BOS continuation, retest entry valid" |
| Ed Seykota | "Trend friend, riding winner" |
| Stan Weinstein | "Stage 2 markup phase, trade with the stage" |

→ **Phase 4 의 결과는 trend following 권위자 모두 valid 로 평가**. 단, **L47 (recovery skill ≠ trading skill)** 는 여전히 적용 — Phase 4 가 valid signal 이지만 Phase 3 cascade 후 entry 라 real account 에선 발현 X.

**룰화 (R31 revised exception)**:
- Cluster #25 (Phase 2, 37min hold +$1,212) = pullback retest type
- Cluster #31 (Phase 4, 4min hold +$4,553) = post-breakout continuation type
- 둘 다 R31 예외 적용 가능 (default 2-min cut 무효)

---

## 14. v1.1 신규 룰 통합

**R32 partial revision (post-breakout continuation 시 negation)**:
- Default: sub-2min winner → next entry size ≤ prev size
- **예외 추가**: post-breakout continuation 확인 시 (cluster #30-32 type, parabolic move 진행 중) → size up 허용

**Trend following 권위자 일치**:
- Curtis Faith Pyramid: "+0.5N 마다 1 unit add" — 정확히 size up rule
- Hougaard "wide win" — winner 키우기
- Ed Seykota "ride winners" — 동일

→ **R32 예외 = trend following 권위자 합의**. 단, BOS confirmation 명확해야.

---

## 15. 추가 명언 20선

### Ed Seykota (Schwager 인터뷰)
1. "The trend is your friend. The end of the trend is your enemy."
2. "Until the trend changes, the trend won't change."
3. "Risk no more than you can afford to lose."
4. "Win or lose, everybody gets what they want from the market."

### Bill Dunn / Jerry Parker
5. "Discretion is the enemy of trend following."
6. "Volatility breakout = entry signal. Volatility contraction = sit out."
7. "Trade the system, not your opinion."

### Linda Raschke (추가)
8. "First hour reveals intent. Trade with it the rest of the day."
9. "Anti = scalp only. Counter-trend hold = death."
10. "ADX > 30 + EMA20 touch = best pullback entry."

### Curtis Faith / Turtle (추가)
11. "If you can follow the rules, you can be a turtle."
12. "Turtles trade the system, not the market."
13. "When in doubt, do nothing."
14. "The rules are 100% mechanical."

### Adam Grimes (추가)
15. "First pullback is the trade. After that, you're chasing."
16. "Measurable patterns or it's not a pattern."
17. "Edge = process. Process = backtest + execute."

### Tom Hougaard (trend 측면 추가)
18. "Most traders cut winners at +5R when trend has +50R."
19. "Trail with the trend, not your hopes."
20. "Same setup every day. Variety is the trader's enemy."

---

*Status: Trend Following v1.1 보강 완료. ~3,500 chars 추가.*
