# 04 — ICT / Smart Money Concepts — 핵심 정리

> **사용자 차트 reference**: 이전 NT_AAL forensics 에서 OB/FVG indicator 사용. ICT 정통 학습.
>
> **⚠️ 중요 caveat**: ICT 컨텐츠는 quality variance 큼. 일부 cult-like / unrealistic claims. **컨셉 학습은 OK, win rate 자랑은 무시.**

---

## 🎯 핵심 명제 5가지 (검증된 ICT 컨셉만)

### 1. Order Block (OB) — 기관 진입 자리

**정의**:
- 강한 추세 직전 마지막 반대 캔들 = institutional 진입 자리
- LONG OB: 큰 상승 직전 마지막 음봉 (down candle)
- SHORT OB: 큰 하락 직전 마지막 양봉 (up candle)
- OB body (open ~ close) 또는 OB body + wicks 50% = 가격 region

**실전 사용**:
- OB 가 sell-side liquidity (long 의 SL 들이 모인 곳) 위에 있으면 LONG OB 강력
- 가격이 다시 OB 로 돌아오면 = institutional 재진입 자리 = LONG entry candidate
- 단, OB 검증 필요: backtest WR 데이터 신뢰 / 사용자 자체 검증 (NT_AAL forensics)

**사용자 직접 적용**:
- Top buying 회피: 가격이 직전 SHORT OB 안에 있으면 LONG 진입 신중
- Pullback entry: 가격이 LONG OB 로 돌아오면 entry candidate

---

### 2. Fair Value Gap (FVG) / Imbalance

**정의**:
- 3 캔들 패턴 — 가운데 캔들이 강한 추세 → 1번 캔들의 high 와 3번 캔들의 low 사이에 gap
- LONG FVG (bullish gap): candle 1 high < candle 3 low — 가격이 너무 빨리 상승 = "fair value 결손"
- 가격이 FVG 로 다시 들어오면 = imbalance 채우기 = 진입/탈출 자리

**실전 사용**:
- FVG 가 channel 안 (HTF trend 방향) 에 있으면 = 강력
- HTF FVG (1h, 4h) = 더 강력 / LTF FVG (1m, 5m) = 더 자주 발생 / 약함

**사용자 직접 적용**:
- 5분 차트 FVG = 사용자 매매 시점 entry trigger 로 사용 가능
- 단, FVG 만으로는 약함 — 다른 confirmation (BOS, structure) 결합

---

### 3. Liquidity Pool / Stop Hunt

**정의**:
- Equal highs (==) 위 = sell-side liquidity (LONG 의 SL 가 모임)
- Equal lows (==) 아래 = buy-side liquidity (SHORT 의 SL 가 모임)
- Smart money = 이 liquidity 를 sweep (=쓸어가기) 하고 반대 방향으로 갈 때 큼

**Pattern**:
1. 가격이 ==highs 만들기
2. ==highs 위로 살짝 break (stop hunt)
3. **반대 방향으로 급락** = SHORT 진입 자리

**사용자 직접 적용 (Top buying 의 핵심 처방)**:
- 사용자 top buying 패턴 = 정확히 stop hunt 의 victim
- ==highs 위에서 LONG 진입 = liquidity 가 위에 있음 → smart money sweep target → 직후 반대 방향
- **회피 룰**: 직전 swing high 위 0.2×ATR 이내 = LONG 진입 X (대신 wait for sweep, then SHORT)

---

### 4. Market Structure Shift (MSS) — Change of Character (CHoCH)

**정의**:
- 직전 추세의 구조가 깨짐
- Uptrend (HH+HL) 중 HL 가 LL 가 됨 = MSS / CHoCH = 추세 반전 가능
- LTF (1m, 5m) 의 MSS 가 HTF (15m, 1h) 추세 전환의 early signal

**Confirmation 단계**:
1. HL → LL 전환 (LTF MSS)
2. LH 형성
3. LL 갱신 (BOS 반대 방향)
→ 3단계 모두 = 강력 SHORT 신호

**사용자 직접 적용 (희망적 추세지향 처방)**:
- HTF trend 가 LONG 인데 LTF MSS 발생 = "이번 LONG 그만 두고 chop / 반전 대기"
- 무지성 LONG 지속 = 희망적 매매 = 패배

---

### 5. Time-Based Concepts (Kill Zones, Power of 3)

**Kill Zones (KST 기준)**:
- **London open kill zone**: KST 16:00~19:00
- **NY open kill zone**: KST 22:30~23:30 (사용자 검증 22:30 WILD CHOP / 23:30 TREND BURST 와 일치)
- **London close kill zone**: KST 00:00~02:00
- 그 외 시간 = 진입 X (low quality)

**Power of 3 (PO3)**:
- 시장 일일 sequence:
  1. **Accumulation** (보통 Asia / pre-market)
  2. **Manipulation** (open 직후 fake move = stop hunt)
  3. **Distribution** (real move 시작)
- 사용자 적용: NY open 첫 30-60분 의 fake move 인지 → 따라가지 말고 wait → real move 진입

**사용자 직접 적용**:
- 22:30 WILD CHOP = manipulation phase → 진입 보류 가능
- 23:30 TREND BURST = distribution phase → real move 진입 자리
- 사용자 본인 데이터 (L35 TIME-VOL MAP) 와 정확히 일치

---

## 📋 사용자 약점 → 직접 처방

| 사용자 약점 | 처방 컨셉 | 비고 |
|---|---|---|
| Top buying | Liquidity sweep 회피 — ==highs 위 LONG X | ICT liquidity 컨셉 |
| 물타기 | 진입 자리 (OB) 깨지면 thesis 무효 = cut | OB invalidation |
| 희망적 추세 | MSS / CHoCH 인식 = 추세 끝 객관화 | ICT structure |
| Sub-2min winner trap | Power of 3 — manipulation phase 진입 회피 | Time concepts |
| 짤짤이 (variance·force) | NY open kill zone 만 진입 | Kill zone |

---

## 📚 권장 학습 순서

### Week 1 — 기초 컨셉 (cult-language 무시하고 컨셉만)
1. **The Trading Channel — SMC basics** ([@TheTradingChannel](https://www.youtube.com/channel/UCGL9ubdGcvZh_dvSV2z1hoQ))
   - 단순화된 SMC 입문
2. **Wysetrade — 5-step entry** ([@Wysetrade](https://www.youtube.com/@Wysetrade))
   - SMC 정형화

### Week 2 — Original Source
3. **Inner Circle Trader — 2026 Smart Money Concepts Lectures**
   - 본인 채널 ([@InnerCircleTrader](https://www.youtube.com/@InnerCircleTrader))
   - core content 영상 5-10개 (cult intro 영상 skip)
4. **Quantum Algo — ICT Strategy Complete Guide** ([link](https://www.quantum-algo.com/blog/guides/ict-trading-strategy-complete-guide/))
   - 정리된 reference

### Week 3 — Application
5. **Tanja Trades — Daily NQ ICT analysis**
   - 매일 라이브 9:15 EST
   - 실전 사례
6. **Stacey Burke Trading — Daily NQ analysis** ([@StaceyBurkeTrading](https://www.youtube.com/@StaceyBurkeTrading))
   - daily analysis

### Week 4 — 한국어 + 통합
7. **팔콘트레이딩 SMC/ICT 풀코스** ([playlist](https://www.youtube.com/playlist?list=PLkOanxbURicsR4fOq8lAmhD6p0JTcFc-S))
   - 한국어 정리
8. **Trading Concepts Explained** ([channel](https://www.youtube.com/channel/UCP_hOTEw12q8tdduG12kdnQ))
   - Smart Money 큐레이션

---

## 🎬 핵심 영상 / 자료 직링크

| # | 자료 | 비고 |
|---|---|---|
| V1 | [ICT 2026 Smart Money Concepts Feb 28](https://www.youtube.com/watch?v=FBxxYUvNaY4) | 최신 lecture |
| V2 | [ICT 2026 Smart Money Concepts Jan 02](https://www.youtube.com/watch?v=1X0A-Lgf9RY) | January lecture |
| W1 | [Quantum Algo ICT Strategy Complete Guide](https://www.quantum-algo.com/blog/guides/ict-trading-strategy-complete-guide/) | 정리된 reference |
| K1 | [팔콘트레이딩 SMC/ICT 풀코스](https://www.youtube.com/playlist?list=PLkOanxbURicsR4fOq8lAmhD6p0JTcFc-S) | 한국어 |
| Y1 | [Trading Concepts Explained](https://www.youtube.com/channel/UCP_hOTEw12q8tdduG12kdnQ) | curation |

---

## 💎 핵심 명언

### ICT (Michael Huddleston)
- "Smart money operates in time-based models. Retail trades random."
- "Liquidity is taken before the move begins."
- "Fair value gaps exist because the market is inefficient — institutions exploit them."

### Wysetrade
- "Five-step entry: HTF bias, LTF setup, OB, FVG confirmation, BOS execution."

### General SMC principle
- "Don't fight the smart money. Identify what they did, follow."
- "Liquidity sweep is the signal, not the move itself."

---

## 📝 사용자 매매 직접 적용 — ICT 7 체크

```
[Pre-Entry ICT Check — 30초]
□ Kill zone 시간대인가? (NY open 22:30~23:30 KST)
□ HTF (15m, 1h) trend 확인 — Uptrend / Downtrend / Range
□ MSS 발생했나? (CHoCH = trend 반전 신호)
□ OB 안에 있나? (HTF OB = 더 강력)
□ FVG 안에 있나? (LTF entry trigger)
□ Liquidity 위에 있나? (==highs 위 = LONG 위험)
□ Power of 3 — manipulation phase 끝났나? (real move 시작인가)

→ 7개 중 5개 미만 YES = 진입 X
```

---

## ⚠️ ICT 학습 주의사항

1. **Win rate 자랑 영상 무시** — "100% win rate" 같은 영상은 cherry-picked. 실제 backtest 결과 자료만 참고.
2. **Cult terminology 일부 ignore** — "Algo runs", "judas swing" 같은 용어 = 컨셉만 알면 됨, 신비화 X.
3. **Backtest 본인 검증** — 사용자 본인 데이터로 OB/FVG 의 NQ WR 검증 (이전 NT_AAL forensics 일부 진행)
4. **혼합 컨셉 위주** — 순수 ICT 만으로 매매 안 됨. 사용자 본인 룰 (R29/R30/R31) + ICT 컨셉 결합.

---

## 🔗 NotebookLM 후속 query

1. "OB 와 FVG 의 정량 정의 + 5분 차트 NQ 적용 시 entry/exit 룰"
2. "Liquidity sweep 패턴 인식 단계 — 5분/15분 NQ 사례"
3. "Kill zone NY open + Power of 3 결합 = NQ 22:30~23:30 KST entry 룰 정형화"

---

*Status: Phase 1C draft (4/6). 다음: 05 NQ Specifics + 06 Scalping*
