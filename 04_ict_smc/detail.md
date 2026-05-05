# 04 — ICT / Smart Money Concepts — DETAIL (핵심 추출)

> ⚠️ **IMPORTANT CAVEAT**: ICT 컨텐츠는 quality variance 큼. 일부 cult-language 또는 unrealistic claims. 본 detail.md = **검증된 핵심 컨셉만** 추출. ICT 영상 보면서 cult intro 부분 skip 권장.

---

## 1. ICT (Inner Circle Trader) 의 핵심 framework

### 1.1 ICT 의 전제

> ❝ Smart money operates in time-based models. Retail trades random. ❞
> — Michael Huddleston, multiple lectures (paraphrase)

**핵심 가정**:
- 시장은 random 이 아니라 institutional order flow 의 결과
- Institutional = 시간대별 / level별 / liquidity 별 행동 다름
- 이 행동을 인식하면 entry / exit 정확도 ↑

**검증 가능 부분 vs cult 부분**:

| 검증 가능 (학습 권장) | Cult-like (skip 권장) |
|---|---|
| Order Block 정의 | "Algo runs at this exact tick" |
| Fair Value Gap | "Judas swing" 신비화 |
| Liquidity Pool / Stop Hunt | "ICT model 100% WR" |
| Market Structure Shift | "Smart money knows my entry" |
| Kill Zones (시간) | "Institutional manipulation conspiracy" |
| Power of 3 (PO3) | "Daily SMT divergence proves manipulation" |

---

## 2. Order Block (OB)

### 2.1 정확한 정의

> **LONG OB**: 강한 상승 추세 직전 마지막 down candle (음봉)
> **SHORT OB**: 강한 하락 추세 직전 마지막 up candle (양봉)

**해석**: institutional trader 가 마지막 매도 (LONG OB 의 down candle) 후 매수 polarity shift = 그 가격대 = 향후 가격이 돌아올 때 institutional 재진입 자리.

### 2.2 OB Zone (선이 아니라 구간)

OB body 만 사용 vs body + wick 50% 사용 vs 전체 candle 사용 — 다양.

**사용자 표준 (CLAUDE.md SR zone 정의 일치)**:
- OB body (open ~ close) = primary zone
- ± 0.25 × ATR = buffer

### 2.3 OB 매매 룰

```
1. HTF (1h, 4h) 추세 확인 (LONG bias 시)
2. HTF LONG OB 식별 (직전 큰 상승 직전 음봉)
3. 가격이 OB zone 으로 돌아올 때 대기
4. OB zone 진입 시 reversal candle 확인
5. Entry = reversal candle close + 0.1 × ATR
6. SL = OB zone 아래 1 × ATR
7. Target = next swing high / 1:2 R:R
```

### 2.4 OB Win Rate 검증

**ICT 본인 주장**: 70-85% (cult inflation 가능)
**Independent backtest**: 50-60% (NQ 5m, 일반 검증)
**사용자 본인 검증 권장**: backtest 직접 + sample 대조

**사용자 약점 처방 — Top buying**:
- Top buying = 직전 high 위 진입 (no level)
- OB 매매 = 직전 institutional level 까지 기다린 후 진입
- → 사용자 처방: "직전 OB 까지 기다린다. 그 외 진입 X"

---

## 3. Fair Value Gap (FVG) / Imbalance

### 3.1 정확한 정의

> **3-candle gap pattern**:
> - Candle 1: 작은 to medium body
> - Candle 2: 강한 추세 candle (gap maker)
> - Candle 3: continuation
> - **Gap** = Candle 1 의 high (또는 low) 와 Candle 3 의 low (또는 high) 사이

**Visualization**:
```
Bullish FVG:
  Candle 1 high: 27940
  Candle 3 low:  27950
  Gap = 27940 ~ 27950 (10pt)
```

### 3.2 FVG 의 의미

- 가격이 너무 빨리 움직여서 "fair value" 채울 시간 없음
- 시장이 효율적이라면 결국 채움 (back-fill)
- = 가격이 FVG 로 돌아올 때 institutional re-balance

### 3.3 FVG 매매 룰

```
1. HTF 추세 확인 (LONG bias)
2. HTF Bullish FVG 식별 (강한 상승 후 미채움 gap)
3. 가격이 FVG 로 돌아올 때 대기
4. FVG 안에서 reversal bar 확인
5. Entry = reversal close
6. SL = FVG 아래 1 × ATR
7. Target = next swing or 1:2 R:R
```

### 3.4 FVG 강도 분류

| 강도 | 조건 |
|---|---|
| **Strong** | HTF (1h, 4h) FVG + channel 안 + 큰 gap (5+pt NQ) |
| **Medium** | LTF (5m, 15m) FVG + 추세 일치 |
| **Weak** | 1m FVG + 노이즈 |

**룰**: Strong / Medium 만 매매. Weak 무시.

### 3.5 사용자 약점 처방 — Sub-2min Winner Trap

- 사용자 패턴: sub-2min winner 후 size up reentry → top buy
- FVG 룰: FVG 안에서만 진입. FVG 밖 = 진입 X.
- → "Win 했다고 다음 진입 X. 다음 FVG 형성될 때까지 wait."

---

## 4. Liquidity Pool / Stop Hunt — 사용자 처방 핵심

### 4.1 Liquidity 정의

**Sell-Side Liquidity**: LONG positions 의 SL 가 모이는 자리 (== highs 위, 직전 swing high 위)
**Buy-Side Liquidity**: SHORT positions 의 SL 가 모이는 자리 (== lows 아래, 직전 swing low 아래)

### 4.2 Liquidity Sweep 패턴

```
1. == highs (equal highs) 형성 (LONG SL 모임)
2. 가격이 == highs 살짝 break (stop hunt)
3. 즉시 반대 방향 (down) 으로 급락
4. 새로운 LL 형성
5. = SHORT entry candidate (sweep 후 reversal)
```

**Bullish 변형 (반대)**:
1. == lows 형성
2. 가격이 == lows 아래로 break
3. 즉시 반등
4. = LONG entry candidate

### 4.3 사용자 약점 직접 처방 — Top Buying ⭐⭐⭐

**가장 명확한 처방**:

```
사용자 패턴: 직전 high 위에서 LONG (top buying)
ICT 진단: 직전 high 위 = sell-side liquidity = stop hunt target
ICT 처방:
  - 직전 high 위 0.2 × ATR 이내 = LONG 진입 절대 X
  - 대신 sweep 발생 대기 → SHORT 진입
  - 또는 sweep 후 반등 확인 → LONG 진입 (단, sweep 가 fully reversed 후)
```

**05-05 사용자 매매 검증**:
- Phase E #10 (LONG @27949.5) → 직전 high 27951.50 바로 아래
- Phase E #11 (LONG @27951.75) → 직전 high 위 (sweep candidate)
- → 모두 sell-side liquidity 위 / 근처 진입 = ICT 룰 위반

---

## 5. Market Structure Shift (MSS) / Change of Character (CHoCH)

### 5.1 BOS vs CHoCH

| | Definition | 의미 |
|---|---|---|
| **BOS** (Break of Structure) | 직전 swing high (uptrend) 돌파 | 추세 지속 |
| **CHoCH** (Change of Character) | 직전 추세의 swing 깨짐 (HL → LL) | 추세 반전 가능 |

### 5.2 MSS 3단계 confirmation

```
1. Uptrend (HH+HL 명확)
2. HL 가 LL 가 됨 ← MSS Stage 1 (early signal)
3. LH 형성 ← MSS Stage 2
4. LL 갱신 (BOS 반대 방향) ← MSS Stage 3 (확정)
```

**룰**: Stage 3 까지 confirm 후 SHORT entry. Stage 1 만으로 entry = early.

### 5.3 사용자 약점 처방 — 희망적 추세지향

- 사용자 자가: "흐름 읽기보다 희망적 추세지향"
- ICT 답: HTF MSS 발생 = "내 LONG bias 가 깨졌다"의 객관 신호
- 처방: HTF MSS 인식 시 본인 LONG thesis 즉시 무효화. chop / 반전 대기.

---

## 6. Time-Based Concepts

### 6.1 Kill Zones (시간대별 prime time)

| Kill Zone | 시간 (KST) | 시간 (NY) | 행동 |
|---|---|---|---|
| **London Open** | 16:00~19:00 | 03:00~06:00 | EU session start |
| **NY AM Killzone** | 22:30~23:30 | 09:30~10:30 | NY RTH first hour ⭐ |
| **NY Lunch** | 01:00~02:00 | 12:00~13:00 | low vol, fakeouts |
| **NY PM Killzone** | 03:00~04:00 | 14:00~15:00 | last hour active |
| **London Close** | 00:00~01:00 | 11:00~12:00 | EU close |

**사용자 검증 (LEARNINGS_NQ.md L35)**:
- 22:30 KST = WILD CHOP (사용자 검증)
- 23:30 KST = TREND BURST (사용자 검증)
- → ICT NY AM Killzone 와 정확히 일치

### 6.2 Power of 3 (PO3)

매일 시장 sequence:

```
Phase 1: ACCUMULATION (Asia / pre-NY)
- 좁은 range 에서 사이드웨이즈
- 시간: KST 06:00 ~ 22:30

Phase 2: MANIPULATION (NY open 직후)
- Fake move (보통 반대 방향)
- 사용자 22:30 KST WILD CHOP = 이 phase
- 시간: KST 22:30 ~ 23:00

Phase 3: DISTRIBUTION (real move)
- True direction 시작
- 사용자 23:30 KST TREND BURST = 이 phase
- 시간: KST 23:30 ~ 02:00
```

### 6.3 사용자 약점 처방 — 22:30 fake move

**사용자 05-05 #2-#5 cluster (18:10~18:25)** = 사실 KST 22:30 NY open 전. 진짜 manipulation phase 는 22:30 직후.

**룰**:
- Phase 1 (Asia / pre-NY) = 진입 X
- Phase 2 (manipulation, 22:30~23:00) = 진입 X (fake move)
- Phase 3 (distribution, 23:30+) = real move 진입

**= 사용자 R5 (2-Phase Session) + R26 (Trend-First) 의 정확한 ICT 버전**.

---

## 7. Optimal Trade Entry (OTE)

### 7.1 OTE 정의

> OTE = Fibonacci 0.618 ~ 0.786 retrace zone
> 이 zone 안에서 진입 시 R:R + WR 최적

**계산 예시**:
- Swing low 27900 → swing high 28000 (range 100pt)
- OTE LONG zone = 27921.4 ~ 27938.2 (38.2% ~ 61.8% retrace)
- (사용 0.618 ~ 0.786 fib retrace from low)

### 7.2 OTE + OB + FVG = Confluence

**최강 entry (ICT 표준)**:
```
1. HTF 추세 LONG bias
2. HTF OB 식별
3. OB 안에 FVG 위치 확인
4. 그 zone 이 OTE 0.618-0.786 안에 있는지 확인
5. → 3 confluence = highest probability entry
```

**사용자 적용**: 최소 2 confluence (OB + FVG 또는 OB + OTE) 필요. 단일 OB / FVG 만 = weak.

---

## 8. 사용자 약점 → ICT 처방 매트릭스

| 약점 | ICT 컨셉 처방 |
|---|---|
| Top buying | Liquidity sweep 대기 (== highs 위 LONG X) |
| 물타기 | OB / FVG 안에서만 진입. 깨지면 thesis 무효. |
| 희망적 추세 (LONG bias) | MSS / CHoCH 인식 = 추세 끝 객관화 |
| Sub-2min winner trap | FVG 안에서만 진입. 다음 FVG 까지 wait. |
| 의지 cooldown 실패 | Power of 3 manipulation phase = 진입 X (시간 강제) |
| 짤짤이 = right conditions | NY AM Killzone 만 진입 (시간 filter) |
| 어느 자리인지 모름 | OB + FVG + OTE 최소 2 confluence |
| Sub-2min winner trap | (위와 동일) |
| 추세 끝까지 못 봄 | MSS 발생 전까지 hold. MSS 시 partial exit |
| 새 계좌 fresh start (L43) | (직접 X) |

---

## 9. 명언 30선

### ICT (Michael Huddleston)
1. "Smart money operates in time-based models. Retail trades random."
2. "Liquidity is taken before the move begins."
3. "Every move starts with a sweep. Find the sweep, find the entry."
4. "Fair value gaps exist because the market is inefficient."
5. "Order block = institutional footprint. Re-test it for entry."

### Wysetrade / The Trading Channel (curators)
6. "Five-step entry: HTF bias, LTF setup, OB, FVG, BOS execution."
7. "If price doesn't respect your OB, your bias is wrong."
8. "MSS is the strongest reversal signal in price action."

### General SMC principle
9. "Don't fight the smart money. Identify what they did. Follow."
10. "Liquidity sweep is the signal. Not the move itself."
11. "Kill zones for entry. Lunch for sit-out."
12. "Power of 3: accumulation → manipulation → distribution. Trade phase 3."

---

## 10. 학습 일정 (5주 페이스)

### Week 1: Order Block + FVG
- Day 1-2: §2 (OB definition + zone)
- Day 3-4: §3 (FVG definition + 3-candle pattern)
- Day 5-7: 사용자 NQ 5m 차트에 OB / FVG 마크

### Week 2: Liquidity / Stop Hunt
- Day 1-3: §4 (Liquidity sweep 패턴)
- Day 4-5: 사용자 매매일지의 top buying clusters 와 sweep 패턴 비교
- Day 6-7: == highs / == lows 식별 연습

### Week 3: MSS / CHoCH + BOS
- Day 1-2: §5.1 (BOS vs CHoCH)
- Day 3-4: §5.2 (MSS 3 stages)
- Day 5-7: 사용자 매매 trend reversal 시점 MSS 적용

### Week 4: Time-Based + OTE
- Day 1-2: §6 (Kill Zones + Power of 3)
- Day 3-4: §7 (OTE + Confluence)
- Day 5-7: 사용자 22:30 KST 시간대 매매에 PO3 적용

### Week 5+: 통합
- 매 trade 진입 전 ICT 7-Step Check (PRE_SESSION_CARD R26 통합)
- NotebookLM "ICT 유니버설" (197 source) cross-query

---

## 11. ICT 학습 주의사항 ⚠️

### 회피 권장
1. **"100% WR ICT setup" 영상** = cherry-picked. 무시.
2. **"ICT proves Federal Reserve manipulates" 류 cult** = 무시.
3. **유료 ICT mentorship $5k+** = 본인 backtest 가 더 효율.
4. **"Algo runs at this tick" 신비화** = 핵심은 OB/FVG/Liquidity 컨셉 자체.

### 학습 권장
1. ICT 본인 영상 = core content (cult intro skip)
2. **Curators**: Wysetrade / The Trading Channel / Trading Concepts Explained / 팔콘트레이딩 한국어
3. **본인 backtest** = 사용자 NQ 5m 데이터로 OB/FVG 의 진짜 WR 검증 (NotebookLM "ICT Part 1+2+3" 156 source 활용)

---

## 12. 한계 / 보강

이 detail.md 의 한계:
1. ICT 의 advanced (SMT divergence, IPDA, Asian Range, NDOG 등) 미포함
2. OTE 의 specific Fibonacci 적용 사례 부족
3. ICT 의 daily/weekly bias 결정 framework 미포함

보강:
- NotebookLM "ICT 유니버설 트레이딩 모델" (197 source) cross-query
- "ICT Part 1+2+3" (156 source) 학습
- 팔콘트레이딩 SMC/ICT 한국어 풀코스 (사용자 한국어 학습 시)

---

*Status: detail.md 4/6 완료.*
