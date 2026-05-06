# Week 6: 이평선 동적 SR (EMA as Dynamic Support/Resistance)

> **목표**: 정배열에서 EMA20 = dynamic support, 역배열에서 EMA20 = dynamic resistance 인식 + pullback retest 진입 자리.
> **기간**: 5 sim 세션 (~1주)
> **전제**: W5 4점+ 통과

---

## 1. 핵심 개념 (15분)

### Dynamic SR 이란?

W3 의 SR = **정적 (static)**. swing 기반, 가격 zone 고정.
W6 의 EMA SR = **동적 (dynamic)**. EMA 가 시간 지나며 이동, 가격이 따라옴.

```
Uptrend + 정배열:
  
       Price ──┐    EMA20 = dynamic support
              ╱╲   (가격이 EMA20 까지 pullback 후 반등)
             ╱  ╲
            ╱    ╲___
           ╱       │
          ╱        EMA20 (touching = potential entry)
         ╱
       EMA50 ───
       EMA200 ──
```

### Pullback Retest Pattern (가장 중요)

**조건 (모두 충족)**:
1. W1: uptrend (HH+HL 명확)
2. W2: 정배열 (EMA20 > 50 > 200)
3. Price > EMA20 (currently above)
4. Pullback 발생: Price → EMA20 까지 내려옴 (touch 또는 ±0.1×ATR)
5. **Bounce 확인**: pullback 후 다음 봉 close > EMA20 (또는 bullish PA candle, W7)

→ ⭐⭐⭐⭐ LONG 진입 zone (EMA20 dynamic support 작동)

### EMA Touch Quality

| Touch 횟수 | 해석 | 진입 가치 |
|---|---|---|
| 1st touch | 첫 retest, 가장 강함 | ⭐⭐⭐⭐ |
| 2nd touch | 여전히 valid, 약간 약함 | ⭐⭐⭐ |
| 3rd+ touch | 약해짐, breakdown 위험 | ⭐⭐ |
| 4th+ touch | 곧 break (자주 일어남) | ⚠️ 회피 |

→ **First / Second touch 만 진입**, 그 이상 회피 (W3 SR touch ≥ 3 와 반대 — dynamic 과 static 의 차이)

### 두 EMA SR

- **EMA20 dynamic SR**: 가장 자주 사용. Active uptrend pullback target.
- **EMA50 dynamic SR**: deeper pullback. EMA20 깨고 EMA50 까지 = 추세 약화 신호 (but 강한 추세에서 fresh start)
- **EMA200**: rare touch. 큰 그림 reversal 또는 long-term trend 유지 reference

### W3 (static SR) + W6 (dynamic SR) 결합

```
EMA20 + Static support zone 겹침 = ⭐⭐⭐⭐⭐ "stacked support"
```

→ 이런 confluence 자리는 sim 에서 적극 진입 (size up)
→ 단일 SR 만 있는 자리보다 reversal 확률 ↑

### 사용자 약점 직결

❌ **추세 한복판 random 진입** (pullback 안 기다림)
✅ **EMA20 retest 까지 인내**

❌ **EMA20 touch 4번째 진입** (이미 약함)
✅ **first/second touch 만**

❌ **EMA20 깨졌는데 LONG 유지** (정배열 망가짐)
✅ **EMA20 close break = LONG 종료 또는 보류**

### 더 깊이

- **NotebookLM**: "이평선 지지저항 + EMA pullback + 차트프로 차트편" cross-query
- **detail.md**: `03_trend_following/detail.md` §EMA, `02_price_action/detail.md` §pullback
- **권위자**: Linda Raschke (20-period MA as "Holy Grail" pullback target)

---

## 2. 차트 관찰 과제 (매일 5분)

### 매일 5분 루틴

1. NQ 5m + Tier 1 + W5 마킹 유지
2. **EMA20 의 최근 50봉 touch count** 세기
3. 정배열 confirm → 가장 최근 EMA20 touch 가 1st/2nd 인지 식별
4. (있다면) **Static SR 과 confluence** 식별
5. Pullback retest pattern 인지 self-judge

### TV setup

- 기존 EMA 20/50/200 유지 (W2)
- "Bar count since EMA20 touch" — TV 직접 표시 어려움 → 시각 mark

### 체크리스트

- [ ] EMA20 retest 패턴 식별
- [ ] Touch count (1st/2nd/3rd+)
- [ ] Static SR confluence 여부
- [ ] Bounce 확인 (다음 봉 close)

### 어려운 케이스

- **Steep pullback** (EMA20 안 닿고 EMA50 까지) — 추세 약화?
- **Multiple touches in short time** (변동성 ↑)
- **Walking-the-EMA** (price 가 EMA20 따라 거의 평행 — pullback X)

---

## 3. 일지 마킹

JSON 추가:

```json
{
  ...,
  "ema20_touch_w6": "1st / 2nd / 3rd+ / no-touch / broken",
  "ema_pullback_setup_w6": "yes / no",
  "static_dynamic_confluence_w6": "yes (EMA20 + W3 support) / no",
  "ema_bounce_confirmed_w6": "yes (close > EMA20) / no / pending"
}
```

**진입 lock 룰** (이번 주 추가):

- LONG + EMA20 broken (정배열 깨짐) → **진입 금지**
- LONG + EMA20 4th+ touch → **진입 자제** (skip 우선)
- LONG + bounce 미확정 → **진입 보류** (다음 봉 close 기다림)

---

## 4. 성공 기준

| 기준 | 합격선 |
|---|---|
| EMA20 retest 패턴 식별 | 80%+ |
| Touch count 정확 | 100% |
| Random 진입 (no pullback) → 0 | 0회 ⭐ |
| Confluence setup 진입 비율 | 30%+ |

---

## 5. 다음 주 연결 (W7)

W6 = "어디에서" (EMA20 touch zone)
W7 = "무엇으로 확인" (PA candle)

→ EMA20 touch + Bullish engulfing = 진입 trigger
→ EMA20 touch only → wait for trigger (W7)

---

## 6. Pre-Session Card 진화

```
W6 추가:
□ EMA20 retest 패턴 = Y/N
□ Touch count = ?
□ Confluence (static + dynamic SR) = Y/N
```

누적: 6 (W5) + 3 (W6) = **9 항목** (그러나 통합으로 6-7 유지)

---

## 7. 권위자 인용

> "20-period MA — 거의 모든 trend trade 의 진입 자리."
> — Linda Raschke ("Trading Sardines")

> "EMA pullback retest 가 1차 entry, breakout 진입은 2차다."
> — Brett Steenbarger

> "First touch 의 EMA20 = 80% 의 winning trade 자리."
> — Adam Grimes (paraphrase)

---

## 🔧 Tools

- "Bar Number" indicator → touch 후 봉 수 카운트 (선택)
- "Pivot Point Marker" 와 결합

---

## 📌 Common Mistakes

| 실수 | 처방 |
|---|---|
| Pullback 안 기다리고 진입 | EMA20 touch 룰 |
| 4th+ touch 진입 | first/second 만 |
| EMA20 깨졌는데 LONG 고집 | break = exit / skip |
| Walking EMA → 진입 자리 X | wait for clear pullback |

---

*W6 시작: W5 통과 후*
