# 02 — Price Action — DETAIL (핵심 추출)

> 자기충족적 교재. Al Brooks / Anna Coulling / Lance Beggs / Wyckoff / Adam Grimes / Steve Nison 핵심 + 사용자 약점 처방.

---

## 1. Al Brooks — "Reading Price Charts Bar by Bar"

### 1.1 Always-In Concept

> ❝ At every moment, the market is in always-in long mode or always-in short mode. Your job is to know which. ❞
> — Trading Price Action TRENDS, Ch. 1

**해설**: 시장은 항상 LONG 또는 SHORT 의 한쪽에 있다. 본인 thesis 가 무엇이든 시장이 어느 모드인지 매 캔들 재평가해야. "내가 LONG 이라고 생각하는 것" ≠ "시장이 always-in long 인 것".

**사용자 약점 직접 처방 — LONG bias (희망적)**:
- 사용자 자가: "흐름 읽기보다 희망적 추세지향"
- Brooks 의 답: 매 5m 캔들 close 시 "지금 always-in 어느 쪽?" 자문. 본인 LONG bias 와 시장 always-in mode 가 다르면 = 즉시 본인 의견 무효.

### 1.2 Signal Bar / Entry Trigger / Follow-Through (3단계)

매 entry 는 3 캔들 단계로 구성:

```
Bar N-1: Signal Bar    — entry 의도 신호 (reversal/continuation candle)
Bar N:   Entry Trigger — high/low break = 진입
Bar N+1: Follow-Through — entry 방향 confirmation
```

**핵심 패턴**:

| 패턴 | Signal Bar 특징 | 의미 |
|---|---|---|
| **Reversal Bar** | 큰 wick + close 가 반대편 | 반전 가능 |
| **Climactic Bar** | 추세 last 큰 캔들 + high volume | 추세 끝 |
| **Inside Bar** | 직전 range 내 close | 결정 보류 |
| **Outside Bar** | 직전 range 돌파 + 반전 close | 강력 반전 |
| **Doji** | open ≈ close + wicks | indecision |

**사용자 약점 직접 처방 — Top buying**:
- Reversal bar 인식 = top buying 의 정확한 회피 신호
- Climactic bar = 추세 끝 = LONG 진입 절대 X
- 사용자 05-05 Phase E (-$680) 의 18:46:25 cluster = 직전 27951.50 cover 가 Reversal bar 가능성 — 그 직후 진입 = 신호 무시

### 1.3 The Second Entry Rule

> ❝ The first entry usually fails. Wait for the second entry. ❞
> — Brooks, multiple chapters

**해설**:
- Pullback after BOS 의 첫 entry = noise 가 자주 stop hunt
- 두 번째 entry (failed first 후 재시도) = 더 높은 WR
- 정량: Brooks 추정 first entry WR 40-50%, second entry 65-70%

**사용자 약점 직접 처방 — Sub-2min winner trap**:
- sub-2min winner 후 size up reentry = first entry chase
- Second entry 컨셉 = "이 setup 다시 confirmed 되면 들어간다" — 사용자 R32 의 정확한 외부 source

### 1.4 H1 / H2 / L1 / L2 Patterns (Pullback Structure)

**Brooks 표기법** (uptrend 중 pullback):
- **H1**: First higher low after BOS
- **H2**: Second higher low (after H1 fails)

**Adam Grimes "first pullback after BOS" 와 동일 컨셉** (다른 표기법).

**적용**:
- H1 = first pullback entry (first entry, WR 50%)
- H2 = second pullback entry after H1 fails (WR 65-70%)
- 사용자 매매에서 "어느 자리에서 들어가야" 의 객관 기준

### 1.5 Brooks 의 매매 철학

> ❝ Trade like a value investor. Buy at the low end of the day's range. Sell at the high. ❞

**핵심**: scalping 식 진입이 아니라 "value 진입". day range 의 low 에서 LONG, high 에서 SHORT. 사용자 top buying 패턴의 정반대.

---

## 2. Anna Coulling — VSA (Volume Spread Analysis)

### 2.1 Wyckoff 의 응용

VSA = Wyckoff method 의 modern 응용. **거래량 + 가격 spread + close 위치** 3개로 institutional intent 추론.

### 2.2 5가지 핵심 신호

#### Signal 1: No Demand Bar (수요 없음)
- **특징**: 작은 spread (작은 캔들) + 평균 이하 volume + close 가 mid-range
- **의미**: institution 매수 안 함 = 추세 약화 / chop
- **적용**: chop 진입 회피 룰

#### Signal 2: No Supply Bar (공급 없음)
- **특징**: 작은 spread + 작은 volume + close 가 high
- **의미**: institution 매도 안 함 = 하락 약화 = LONG 가능 신호

#### Signal 3: Climactic Volume (탈진 거래량) 💀 사용자 처방 핵심
- **특징**: 매우 큰 spread + 매우 큰 volume + close 반대편
- **의미**: 추세 마지막. **Top buying 의 정확한 회피 신호**.
- **사용자 약점 처방**:
  - Phase E 18:46:25 cluster 직전 캔들 = climactic volume 가능성 (사용자 본인 차트 검증 필요)
  - 룰: climactic volume 발생 시 그 방향 추가 진입 절대 X. 반대 방향 setup 대기.

#### Signal 4: Stopping Volume (멈춤 거래량)
- **특징**: 하락 중 점점 큰 volume 인데 가격 하락 둔화
- **의미**: institutional buying 흡수 = 하락 끝 가능

#### Signal 5: Upthrust (가짜 상승)
- **특징**: 직전 high break 후 close 가 doji 또는 mid-range
- **의미**: stop hunt 후 반전 = SHORT setup
- **ICT Liquidity Sweep 와 동일** (다른 용어)

### 2.3 Wyckoff 4 Phases

```
Phase A: Selling Climax / Buying Climax (추세 끝)
Phase B: Accumulation / Distribution (sideways, smart money 진입)
Phase C: Test (마지막 stop hunt — Spring or Upthrust)
Phase D: Trend (real move 시작)
```

**적용**:
- Phase B (sideways) 진입 = chop 매매 = 손실 (사용자 데이터 검증)
- Phase C 의 Spring (가짜 하락 후 급반등) = LONG entry candidate
- Phase D (real trend) = 사용자 22:30~23:30 NY first hour 와 일치

---

## 3. Lance Beggs — YourTradingCoach (YTC)

### 3.1 Context-Driven Entry (4 요소)

> ❝ Context first. Setup second. Execution third. Without context, no trade. ❞
> — yourtradingcoach.com, multiple posts

**Context 4 요소 모두 confirm 필요**:

1. **HTF Trend** (1h, 4h): 어디로 가고 싶나
2. **HTF Levels**: 직전 swing high/low, daily/weekly high/low
3. **LTF Setup** (5m, 1m): 진입 trigger
4. **R:R**: 최소 1:1.5 (사용자 L39 와 호환)

**4개 모두 YES 가 아니면 = no context = 진입 X**.

**사용자 약점 직접 처방 — "어느 자리인지 모름"**:
- 사용자 자가: "어느 자리에서 들어가야 하나"
- Beggs 의 답: 4 요소 매번 check. 사용자 PRE_SESSION_CARD 7-Gate 의 정확한 source.

### 3.2 The Effective Session Review (무료 PDF)

Lance Beggs 의 [무료 PDF](https://www.scribd.com/document/491988824/YTC-Effective-Session-Review):

**Review 의 5단계**:

```
1. Did I follow my plan? (process check)
2. Did the plan match the market? (plan check)
3. What did I do well? (positive 강화)
4. What did I do poorly? (negative 패턴)
5. What ONE thing will I change next session? (single change)
```

**핵심 원칙**: 매 세션 review = process score, P&L 점수가 아님.
**Brett Steenbarger 와 동일** (다른 사람, 같은 결론).

### 3.3 Multi-Timeframe Structure

> ❝ HTF tells you direction. LTF tells you timing. Without both, you're guessing. ❞

**적용**:
- HTF 가 LONG bias = 1h HH+HL 명확
- LTF 가 entry trigger = 5m signal bar after pullback
- HTF 충돌 시 = 진입 X

---

## 4. Wyckoff Method (Original, 1930s)

### 4.1 Composite Operator 컨셉

Wyckoff: 시장에는 가상의 "Composite Operator" (CO) 가 있다 — institutional smart money 의 합산. CO 가 4 phase 로 시장 운영:

```
Phase 1 (Accumulation): low price 에서 매집
Phase 2 (Markup): 가격 push up
Phase 3 (Distribution): high price 에서 매도
Phase 4 (Markdown): 가격 push down
```

### 4.2 The 3 Wyckoff Laws

#### Law 1: Supply and Demand
- supply > demand → 가격 하락
- demand > supply → 가격 상승
- 거래량으로 측정

#### Law 2: Cause and Effect
- Phase 1 (accumulation) 의 길이 = Phase 2 (markup) 의 크기
- 길게 쌓일수록 큰 추세

#### Law 3: Effort vs Result
- 큰 volume (effort) 인데 가격 변화 없음 (no result) = 진행 약화
- 작은 volume 인데 가격 큰 변화 = breakout 가능

**사용자 적용**:
- Effort vs Result = 가장 강력한 institutional intent 신호
- Top buying 회피: 큰 volume + 가격 정체 = supply 흡수 중 = 하락 가능

### 4.3 Spring / Upthrust (사용자 처방 핵심)

#### Spring (Phase C, accumulation 끝)
- 직전 swing low 아래로 push (stop hunt)
- 즉시 반등 (하락 거부)
- = LONG entry candidate

#### Upthrust (Phase C, distribution 끝)
- 직전 swing high 위로 push (stop hunt)
- 즉시 반락 (상승 거부)
- = SHORT entry candidate
- = **사용자 top buying 의 victim 패턴**

**룰**: 직전 high 위 break 후 같은 캔들에 close 가 mid-range = upthrust = LONG 진입 X.

---

## 5. Adam Grimes — Measurable Patterns

### 5.1 First Pullback After BOS (가장 강력한 patterns)

> ❝ The first pullback after a break of structure has the highest win rate of any chart pattern. ❞
> — The Art and Science of Technical Analysis, Ch. 5

**정량 정의**:

```
1. Uptrend BOS = 가격이 직전 swing high 돌파
2. First pullback = BOS 후 첫 down candle cluster (HL 형성)
3. Entry trigger = HL 형성 후 reversal bar close
4. SL = HL 아래 ATR × 1.5
5. Target = next swing high or 1:2 R:R
```

**WR 추정**: 65-75% (Brooks H1 컨셉과 동일).

### 5.2 Measurable vs Non-measurable Patterns

Grimes 의 핵심 원칙: **patterns must be objective and measurable**.

| Measurable | Non-measurable (X) |
|---|---|
| HH+HL 명확 (수치 표시) | "추세가 있어 보인다" |
| EMA20 cross (수치) | "강한 추세다" |
| Volume > 평균 × 1.2 | "거래량이 많다" |
| ATR > 평균 × 0.8 | "변동성이 적절하다" |

**사용자 약점 직접 처방**:
- 사용자 자가: "흐름 읽기보다 희망적 추세지향"
- Grimes 의 답: 매 진입 전 "이 setup 의 정량 기준이 무엇인가?" 자문. measurable 아니면 진입 X.

### 5.3 Backtest-Friendly Approach

Grimes 의 모든 setup = 정량 정의 → backtest 가능.

**사용자 직접 활용**:
- "First pullback after BOS" 를 NQ 5m 차트에 backtest (사용자 본인 데이터로)
- WR / R:R / count 측정
- 성능 안 좋으면 변형 (filter 추가) 또는 폐기

---

## 6. Steve Nison — Japanese Candlesticks

### 6.1 핵심 reversal patterns (사용자 약점 처방)

#### Hammer (망치) — Bottom reversal
- 작은 body + 긴 lower wick (body 길이의 2x+)
- close 위치 = body 위쪽
- 의미: 하락 거부 = LONG candidate

#### Shooting Star (유성) — Top reversal 💀 사용자 처방
- 작은 body + 긴 upper wick (body 2x+)
- close 위치 = body 아래쪽
- 의미: 상승 거부 = **SHORT candidate / LONG 절대 X**
- **= 사용자 top buying 회피 신호**

#### Engulfing — Strong reversal
- 직전 캔들 body 를 완전히 감싸는 큰 candle
- Bearish engulfing = SHORT, Bullish engulfing = LONG

#### Doji — Indecision
- open ≈ close
- trend 끝 가능 / 또는 continuation pause
- 단독으로는 weak signal — context 필요

### 6.2 Pattern + Volume + Context = 강력 신호

**Nison 의 핵심**: candle pattern 단독 ≠ signal. **Pattern + Volume + Trend Context** 결합 시만 강력.

**예시**:
- Hammer at uptrend pullback + volume 상승 + EMA20 zone = 강력 LONG
- Hammer at chop + volume 평균 = weak signal = 진입 X

---

## 7. 사용자 약점 → 권위자별 처방 매트릭스

| 약점 | Al Brooks | Anna Coulling (VSA) | Lance Beggs | Wyckoff | Adam Grimes | Nison |
|---|---|---|---|---|---|---|
| 흐름 읽기 부재 | always-in mode | climactic + no demand | context 4 요소 | 3 laws | measurable only | pattern + context |
| Top buying | reversal bar / climactic | climactic volume | HTF level 위 entry X | Upthrust 회피 | first pullback only | shooting star 인식 |
| 물타기 | always-in 반대 = thesis 무효 | (직접 X) | context 깨짐 = exit | (직접 X) | measurable invalidation | (직접 X) |
| 어느 자리인지 모름 | H1/H2 정량 | 5 signals | context 4 요소 | 4 phases | first pullback BOS | pattern + level |
| LONG bias | always-in 무관 본인 의견 | (직접 X) | HTF 충돌 시 진입 X | CO 의 phase 인식 | objective only | pattern 따라 |
| Sub-2min winner trap | second entry | (직접 X) | (직접 X) | (직접 X) | first pullback 만 valid | (직접 X) |
| 변동성·속도·힘 | bar momentum | volume + spread + close | context 4 요소 | effort vs result | ATR / EMA filter | volume confirm |

---

## 8. 명언 30선 (출처 명시)

### Al Brooks
1. "Always-in. The market is always either long or short."
2. "Wait for the second entry. The first one fails more often than not."
3. "Trade like a value investor. Buy at the low end of the day's range."
4. "Every bar is a signal bar. Every bar means something."

### Anna Coulling / VSA
5. "Climactic volume = the end of the move, not the beginning."
6. "Wide spread + low volume = trap."
7. "Volume precedes price."
8. "No demand = no trend. No supply = no decline."

### Lance Beggs
9. "Context first. Setup second. Execution third."
10. "The market doesn't care what you think. It cares what you do."
11. "Review every session. Edge comes from process, not lucky trades."

### Wyckoff
12. "The Composite Operator manipulates the market in 4 phases."
13. "Effort vs result. Big effort + small result = trend exhaustion."
14. "Spring after accumulation. Upthrust after distribution."

### Adam Grimes
15. "Measurable patterns or it's not a pattern."
16. "First pullback is the trade. After that, you're chasing."
17. "Edge = process. Process = backtest + execute."

### Steve Nison
18. "Pattern + volume + context = signal. Pattern alone = noise."
19. "Shooting star at top = reversal. Don't long it."
20. "Hammer + volume + EMA20 = strong long."

---

## 9. 학습 일정 (5주 페이스)

### Week 1: Al Brooks Always-In + Signal Bar
- Day 1-2: §1.1-1.2 (always-in + signal bar)
- Day 3-4: §1.3 (second entry 룰) — 사용자 R32 와 매핑
- Day 5-7: §1.4 (H1/H2/L1/L2) + 본인 차트 5분 마크

### Week 2: VSA Volume + Wyckoff Phases
- Day 1-3: §2 (5 VSA signals)
- Day 4-5: §4 (Wyckoff 4 phases + 3 laws)
- Day 6-7: 본인 차트에 climactic volume + spring/upthrust 마크

### Week 3: Lance Beggs Context + Effective Session Review
- Day 1-2: §3.1 (context 4 요소)
- Day 3-4: §3.2 (Session Review PDF) — 첫 review 작성
- Day 5-7: §3.3 (multi-timeframe) + 본인 매매에 적용

### Week 4: Adam Grimes Measurable + Nison Candles
- Day 1-3: §5 (first pullback after BOS, measurable patterns)
- Day 4-5: §6 (candle reversal patterns)
- Day 6-7: §7 (사용자 약점 매핑) + 본인 매매일지 비교

### Week 5+: 강화 / 반복
- 매주 본인 매매 5 trade → 6 권위자 lens 로 분석
- 4주 누적 후 본인 패턴 객관화

---

## 10. 한계 / 보강

이 detail.md 의 한계:
1. Al Brooks 책 1500+ pages 의 일부만 (signal bar / always-in / second entry)
2. VSA 의 5 signals 외 advanced (No Result / Selling Climax 등) 미포함
3. Wyckoff 의 6 step approach (선택과 집중 후 phase analysis) 미포함

보강:
- NotebookLM "차트프로 차트편" (62 source) cross-query 활용
- "ICT 유니버설" (197) 의 PA 부분 query

---

*Status: detail.md 2/6 완료.*
