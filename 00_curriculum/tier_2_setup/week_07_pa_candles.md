# Week 7: Price Action 캔들 패턴

> **목표**: Engulfing / Pin Bar / Inside Bar 즉시 식별 + EMA20 touch + 이 캔들 = trigger.
> **기간**: 5 sim 세션
> **전제**: W6 4점+

---

## 1. 핵심 개념 (15분)

### 3가지 핵심 PA 캔들 (Al Brooks/Volman 표준)

#### 1) Engulfing (장악형)

```
Bullish Engulfing:
                ┌──┐
                │  │  ← 큰 양봉 body 가
                │  │     이전 음봉 body 를 완전히 cover
       ┌──┐     │  │
       │  │     │  │
       │  │     │  │
       │▼ │     │  │
       └──┘     └──┘

조건:
  - 직전 캔들과 반대 색
  - body 가 직전 캔들 body 를 완전히 cover (open ~ close 비교)
  - 강한 momentum signal

신뢰도: ⭐⭐⭐⭐
```

#### 2) Pin Bar (Hammer / Shooting Star)

```
Bullish Pin Bar (Hammer):
       ┌──┐
       │██│  ← 작은 body
       │██│
       │  │  ┐
       │  │  │
       │  │  │  긴 lower wick (body 의 2배 이상)
       │  │  │
       │  │  ┘
       └──┘

조건:
  - lower wick ≥ body × 2 (rejection)
  - upper wick 작음 (< body)
  - close 가 high 근처

해석: lower 측에서 sellers 는 push 했지만 buyers 가 reject → reversal 신호

신뢰도: ⭐⭐⭐ (context 중요)
```

#### 3) Inside Bar

```
Outer (이전):     Inside (현재):
   ┌──┐
   │  │            ┌──┐  ← outer 의 high/low 안에
   │  │            │  │     완전히 포함
   │  │            └──┘
   └──┘
                    
조건:
  - 현재 캔들 high < outer high
  - 현재 캔들 low > outer low
  - 압축 (consolidation) signal

해석: 변동성 압축 → 다음 봉 break direction = 진입
신뢰도: ⭐⭐ (context 절대 중요 — outer break 후 진입)
```

### 결합 시그널 = Trigger

| 자리 (W3/W6) | 캔들 (W7) | 결과 |
|---|---|---|
| EMA20 touch (W6) + Static support (W3) | Bullish Engulfing | ⭐⭐⭐⭐⭐ LONG |
| Resistance zone (W3) | Bearish Pin Bar | ⭐⭐⭐⭐ SHORT |
| BB Squeeze 끝 (W5) | Outer break + retest | ⭐⭐⭐⭐ Breakout |
| Range mid | Engulfing | ⭐⭐ (자리 약함) |
| Random | Engulfing | ⭐ (자리 X) |

→ **자리 (W3/W6) 가 우선, 캔들은 trigger**. 캔들만으로 진입 X.

### 사용자 약점 직결

❌ **캔들 무시하고 진입 (timing 안 맞음)**
✅ **자리 OK + 캔들 confirm 까지 wait**

❌ **모든 큰 양봉 = Engulfing 으로 오인**
✅ **정의 엄격 적용 (body cover 100%)**

❌ **Pin Bar 1개로 reversal 결정**
✅ **Pin Bar + 자리 + 다음 봉 confirm**

### Multi-bar pattern (참고)

- **Three White Soldiers** / **Three Black Crows** — 연속 3 캔들 같은 방향, 강한 momentum
- **Morning Star / Evening Star** — 3 캔들 reversal pattern
- **Bullish/Bearish Harami** — Inside bar 의 변형

(이번 주는 3 핵심만 집중. 나머지는 reference)

### 더 깊이

- **NotebookLM**: "Price Action candle Al Brooks + 차트프로 차트편" cross-query
- **detail.md**: `02_price_action/detail.md` §candles
- **권위자**: Al Brooks ("Trading Price Action" book), Bob Volman ("Forex PA Scalping")

---

## 2. 차트 관찰 과제 (매일 5분)

### 매일 5분 루틴

1. NQ 5m 차트, Tier 1 + W5/W6 마킹 유지
2. **최근 100봉 에서 Engulf / Pin Bar / Inside 식별** + 마킹
3. 각 candle 의 자리 (W3/W6) 와 결합 → setup quality 등급
4. 가장 강한 setup 1-2개 캡처

### TV setup

- "Candlestick Patterns" indicator (built-in TV) — 자동 식별 (검증용, 수동 식별이 우선)

### 체크리스트

- [ ] Engulf / Pin / Inside 식별
- [ ] 각 candle 자리 (W3/W6 결합)
- [ ] 자리 강한 candle 1개 + skip cases 식별

### 어려운 케이스

- **fake engulf** — body 거의 같아서 애매
- **Pin Bar wick 길이 미달** — 정의 엄격
- **Inside bar 연속** (compression — 곧 breakout)

---

## 3. 일지 마킹

JSON 추가:

```json
{
  ...,
  "pa_candle_w7": "engulf-bull / engulf-bear / pin-bull / pin-bear / inside / none",
  "pa_quality_w7": "high (자리 OK) / mid / low (자리 X)",
  "pa_trigger_used_w7": "yes (진입 시 candle confirm) / no"
}
```

**진입 룰**:
- 자리 OK + PA candle confirm = 진입
- 자리 OK + PA confirm 미달 = wait
- 자리 X + PA candle = skip (자리 우선)

---

## 4. 성공 기준

| 기준 | 합격선 |
|---|---|
| 3 패턴 식별 정확 | 80%+ |
| 자리 + candle 결합 판정 | 80%+ |
| 자리 X 인 candle 진입 | < 20% |

---

## 5. 다음 주 연결 (W8)

W7 = "trigger candle"
W8 = "trigger 까지의 entry timing — Pullback vs Top Buy"

→ W8 은 사용자 핵심 약점 (top buying) 직접 처방.
→ W7 의 candle 을 W8 에서 "어디에서 trigger" 로 정확화.

---

## 6. Pre-Session Card 진화

```
W7 추가:
□ Trigger candle (engulf/pin/inside) = ?
□ Candle 자리 quality = high/mid/low
```

누적: ~6-7 항목 (압축 유지)

---

## 7. 권위자 인용

> "Engulfing 이 자리에서 나오면, 거의 항상 답이다."
> — Al Brooks

> "Pin Bar 는 시장의 거짓말이다 — 누군가 push 했지만 거부당한 흔적."
> — Linda Raschke (paraphrase)

> "Inside bar 는 가장 무서운 candle 이다 — 폭발 직전."
> — Bob Volman

---

## 📌 Common Mistakes

| 실수 | 처방 |
|---|---|
| 자리 무시, candle 만 보고 진입 | 자리 우선 |
| 모든 큰 봉 = engulf | 정의 엄격 적용 |
| Pin bar 1개로 reversal 확정 | 다음 봉 confirm |

---

*W7 시작: W6 통과 후*
