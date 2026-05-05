# 03 — Trend Following / Pullback Entry — 핵심 정리

> **사용자 약점 처방**: pullback vs top buy 구분. "추세 잡아도 진득히 못 봄" → trend ride 방법론.

---

## 🎯 핵심 명제 5가지

### 1. Pullback Entry = 추세 *방향* 으로의 일시 되돌림에 진입

**기본 정의**:
- **Trend**: HH+HL (uptrend) or LH+LL (downtrend) 명확
- **Pullback**: trend 중 반대 방향으로 일시 되돌림 (3-30 캔들)
- **Pullback entry**: 되돌림이 끝나고 trend 재개 신호 시 진입

**Top buying vs Pullback 의 결정적 차이**:

| 항목 | Top Buying | Pullback Entry |
|---|---|---|
| 진입 시점 | 직전 swing high 위에서 | 직전 swing high 아래에서 (되돌림 후) |
| Risk | swing high 가 SL — wide | 직전 HL 이 SL — tight |
| R:R | 1:0.5 흔함 | 1:2~3 가능 |
| 시장 정황 | 추세 끝물 | 추세 중간 |
| Win rate | 20-40% | 50-70% |

**사용자 약점 직접 적용**:
- 05-05 #10 LONG @27949.5 = top buying (직전 high 27951.50 위)
- 정상 pullback entry = LONG @27945 (직전 HL 27944 직후)

---

### 2. Linda Raschke — "First Hour" + 80-20 + Anti

**Linda Bradford Raschke, "Street Smarts"**:
- 시장 첫 1시간 = noise 가 크지만 reversal 자주 발생
- 22:30~23:30 KST = NY first hour = 사용자 데이터 검증
- 80-20: 어제 close 의 80% 하락 후 20% 반등 = LONG 가능
- Anti pattern: 추세 반대 방향의 짧은 되돌림 = quick scalp 가능

**Holy Grail (ADX + 20EMA)**:
- ADX > 30 → trend mode 확정
- 가격이 20EMA 터치 = pullback
- ADX 유지 + EMA 터치 = pullback entry signal
- **사용자 ADR-028**: stride bug 후 검증 결과 REJECTED. 컨셉은 OK 지만 정량 룰은 NQ에서 약함.

→ **결론**: Linda 컨셉 학습 valuable, 정량 룰은 본인 backtest 보강 필요.

---

### 3. Adam Grimes — Measurable Pullback Patterns

**Adam Grimes, "The Art and Science of Technical Analysis"**:
- Pullback 패턴 5가지를 정량 정의
  1. **First Pullback after BOS** = 가장 강력 (HH 이후 첫 HL)
  2. **EMA20 Pullback** = trend 강할 때 EMA20 까지만 되돌림
  3. **AB=CD pullback** = symmetric retrace pattern
  4. **Failed test** = pullback 깊다가 reversal
  5. **Time pullback** = 가격 보다 시간이 결정 (2-5 candles)

**사용자 적용**:
- "First pullback after BOS" 가 가장 권장 (highest WR)
- 정량 룰 가능 (BOS 명확 → HL 형성 → entry trigger)
- backtest 친화적 — 사용자가 본인 데이터로 검증 가능

---

### 4. Trail Stop — 추세 끝까지 타기

**Stan Weinstein, Tom Hougaard, Curtis Faith 공통**:
- Winners 키우는 핵심 = trail stop
- Initial SL → BE move → 단계별 trail
- "Cut trades that stop trending" — 추세 멈추면 cut

**사용자 R29/R30/R31 와 호환**:
- R31 (2분 cut) = 짧은 trade 의 trail
- 5분 살아남으면 = trend 진짜 시작
- 그 후엔 ATR-based trail 또는 swing-based trail
- 사용자 본인 ratchet 시스템 (CLAUDE.md 표준 정의) 활용 가능

**기본 ratchet (CLAUDE.md 사용자 표준)**:
```
Stage 0 (entry):       SL = entry - 1.5×ATR
Stage 1 (P ≥ +0.4R):   SL → entry (break-even)
Stage 2 (P ≥ +0.8R):   SL → entry + 0.3R
Stage 3 (P ≥ +1.2R):   SL → entry + 0.6R, partial TP 50%
Stage 4 (P ≥ +1.6R):   trail by 0.8×ATR dynamic
```

---

### 5. Turtle Rules — 시스템 사고 (Curtis Faith)

**원본 Turtle Rules** ([무료 PDF](https://bigpicture.typepad.com/comments/files/turtlerules.pdf)):
- Donchian breakout (20일 high/low 돌파)
- ATR-based position sizing (N system)
- Pyramid 1/2 N 마다
- Initial SL = 2N (2×ATR)

**핵심 가르침 (사용자 직접 적용)**:
- **시스템 = 룰 = 감정 무관 실행**
- "If signal then enter. Period."
- 결과 무관 (다음 룰 다음 trade)
- 룰 위반 = 시스템 무효
- → R29/R30/R31 룰 시스템 운영 정확히 일치

---

## 📋 사용자 약점 → 직접 처방

| 사용자 약점 | 처방 컨셉 | 출처 |
|---|---|---|
| Top buy vs pullback 혼동 | First pullback after BOS = 가장 안전 | Adam Grimes |
| 추세 끝까지 못 봄 | Ratchet trail stop (단계별) | All trend followers + 사용자 표준 |
| Winner 짧게 끊음 | "Cut losses, ride winners" — opposite of intuition | Tom Hougaard + Curtis Faith |
| 사이즈 욕심 / 물타기 | Pyramid only on profit, never on loss | Turtle Rules |
| 룰 위반 (감정) | "If signal then enter. No exceptions." | Curtis Faith |

---

## 📚 권장 학습 순서

### Week 1 — 기초
1. **Curtis Faith — Original Turtle Rules** ([무료 PDF](https://bigpicture.typepad.com/comments/files/turtlerules.pdf))
   - 1시간 반 분량, 시스템 사고의 근본
2. **Adam Grimes — YouTube core videos** ([@AdamHGrimes](https://www.youtube.com/@AdamHGrimes))
   - measurable pullback patterns
3. **Linda Raschke 인터뷰** (search Real Vision / Schwager Market Wizards)

### Week 2 — 적용
4. **Tom Hougaard — Trail stop 사례 영상**
   - winner 끝까지 타기 mindset
5. **Stan Weinstein — "Secrets for Profiting" Stage Analysis** (책)
   - HTF context (Stage 1-4)

### Week 3 — 시스템화
6. **Adam Grimes — "The Art and Science"** 책 chapter on patterns
   - quantitative entry/exit rules
7. **Andrea Unger — "The Unger Method"** (책)
   - systematic / 4x champion 사례

### Week 4 — 통합
8. **Michael Covel — "Trend Following"** 책 + 팟캐스트
   - 다양한 trend follower 인터뷰

---

## 🎬 핵심 영상 / 자료 직링크

| # | 자료 | 비고 |
|---|---|---|
| P1 | [Original Turtle Rules PDF](https://bigpicture.typepad.com/comments/files/turtlerules.pdf) | 무료 |
| V1 | [Adam Grimes YouTube](https://www.youtube.com/@AdamHGrimes) | course material |
| V2 | [Tom Hougaard YouTube](https://www.youtube.com/@traderTomHougaard) | trail stop 사례 |
| W1 | [TrendFollowing.com](https://www.trendfollowing.com/) | Michael Covel |

---

## 💎 핵심 명언

### Curtis Faith
- "If you can follow the rules, you can be a turtle."
- "When in doubt, do nothing."
- "Pyramid winners, never losers."

### Linda Raschke
- "The best traders manage risk. The rest are gamblers."
- "Anti-trend trades are scalps. Trend trades are positions."
- "Holy Grail = ADX + EMA. Wait for trend, then for pullback."

### Adam Grimes
- "First pullback is the trade. After that, you're chasing."
- "Measurable patterns or it's not a pattern."
- "Edge = process. Process = backtest + execute."

### Stan Weinstein
- "Stage analysis. What stage is the market in? Trade only stage 2 (uptrend) or stage 4 (downtrend)."
- "Don't fight the tape. Don't fight the Fed."

---

## 📝 사용자 매매 직접 적용 — Pullback Entry 5단계

```
[Pullback Entry Process]
1. HTF (15m or 1h) trend 확인 — HH+HL or LH+LL
2. BOS (직전 swing high/low 돌파) 발생 확인
3. 첫 pullback 시작 = HL 형성 시작 시점 (LONG 기준)
4. Pullback 종료 신호 = LTF (5m) 의 reversal candle + 거래량 확장
5. Entry trigger = 5m candle close 위에서 BUY (limit at HL price + small buffer)
6. Initial SL = HL 아래 ATR × 1.5
7. Ratchet trail stop 시작
```

---

## 🔗 NotebookLM 후속 query

1. "First pullback after BOS 의 정확한 정의와 정량 룰 (Adam Grimes 기준)"
2. "Linda Raschke Holy Grail 의 NQ 적용 시 ADX threshold 와 EMA period 권장값"
3. "Trail stop 의 ratchet 단계 — 사용자 표준 (CLAUDE.md) 와 Turtle N system 비교"

---

*Status: Phase 1C draft (3/6). 다음: 04 ICT/SMC*
