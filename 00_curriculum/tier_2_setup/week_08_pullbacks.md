# Week 8: Pullback vs Top Buy ⭐⭐⭐ (사용자 핵심 약점)

> **목표**: 모든 LONG 진입을 "Pullback (38.2%/50%/61.8%)" 또는 "Breakout retest" 로 분류. **Top Buy 진입 0회**.
> **기간**: 5 sim 세션 (필요 시 2주)
> **전제**: W7 4점+
> **중요도**: ⭐⭐⭐⭐⭐ — Tier 2 의 졸업 시험. L5 top buying 직접 처방.

---

## 1. 핵심 개념 (15분)

### Pullback 이란?

**상승 추세 안의 일시적 하락** (반대로, 하락 추세 안의 일시적 상승 = "pullup" 또는 retracement).

```
Uptrend Pullback:

           Swing High (H2)
              ╱╲
             ╱  ╲   ← Pullback (retracement)
            ╱    ╲
           ╱      ╲___ ← 38.2% / 50% / 61.8% retrace
          ╱           ╲
         ╱             ╲ ← bounce, 다음 leg up
        ╱_______________
       Swing Low (L1)

조건:
  - W1: uptrend (HH+HL)
  - W2: 정배열 유지
  - 가격이 swing high 에서 일정 % 하락
  - W6: EMA20 또는 EMA50 까지 (보통)
  - Bounce 확인 후 LONG 진입
```

### Fibonacci Retracement Levels

```
0%      = Swing Low (entry leg start)
23.6%   = shallow (강한 추세, 빠른 reversal)
38.2%   = ⭐⭐⭐ 가장 자주 작동
50.0%   = ⭐⭐⭐⭐ 50/50 균형점, 강한 SR
61.8%   = ⭐⭐⭐ 깊은 pullback, 추세 약화 신호
78.6%   = 너무 깊음 — 추세 전환 위험
100%    = Swing Low (전 leg 무효)
```

**적정 zone**: 38.2% ~ 61.8%. 23.6% 는 너무 얕고 78.6% 는 너무 깊음.

### Top Buy 정의 (사용자 핵심 약점)

```
Top Buy = "추세 끝물에 신고가에서 직진입"

증상:
  - swing high 만들고 + 1봉 안에 진입
  - pullback 안 기다림
  - "곧 더 갈 거야" 욕심
  - resistance zone 가까운데 LONG (W3 처방 무시)

결과:
  - 진입 즉시 pullback → 손실
  - SL 가까이 (top 직후 자연스러운 retrace)
  - 짤짤이 후 욕심 진입 패턴 (L5)
```

### Pullback vs Top Buy 구분 룰

```
Pullback 진입 조건 (모두 만족):
  ✓ swing high 만든 후 ≥ 5봉 경과
  ✓ 가격이 swing high 에서 ≥ 38.2% 하락
  ✓ W6: EMA20 또는 EMA50 touch
  ✓ W7: bullish PA candle (engulf/pin) 확인
  ✓ W3: 위 resistance zone 거리 ≥ 1.0 ATR

Top Buy = 위 조건 미충족인데 LONG → **즉시 exit, 자가 알람**
```

### Breakout Retest (대안)

Pullback 외 valid 진입 = **Breakout 후 retest**:

```
1. Resistance zone 돌파 (close above)
2. Pullback 후 broken resistance = new support
3. New support 에서 bounce → LONG

조건:
  - 돌파 봉 close 가 zone 위
  - Retest = 돌파 가격대 ±0.25×ATR
  - Retest 봉이 bullish (engulf/pin)
```

→ Pullback (위 38.2-61.8% 룰) **OR** Breakout retest = valid LONG 진입의 모든 형태.
→ 그 외 = Top Buy 또는 Random 진입 = **금지**.

### 진입 분류 결정 트리

```
LONG 진입 시:

1. swing high 만든 후 ≥ 5봉?
   No → Top Buy 위험. 진입 금지.
   Yes ↓

2. Pullback retracement %?
   < 23.6% → 너무 얕음. wait.
   23.6% ~ 38.2% → ⭐⭐ shallow pullback
   38.2% ~ 50% → ⭐⭐⭐ ideal
   50% ~ 61.8% → ⭐⭐⭐ ideal
   61.8% ~ 78.6% → ⭐⭐ deep pullback (caution)
   > 78.6% → 추세 전환 위험. wait.

3. EMA20 또는 EMA50 touch?
   No → 자리 약함. wait.
   Yes ↓

4. PA candle confirm?
   No → trigger 미달. wait.
   Yes → LONG 진입 ⭐⭐⭐
```

### 사용자 약점 직접 처방

❌ **신고가 직진입 (Top Buy)** — L5 핵심 약점
✅ **5봉 + 38.2% + EMA20 + PA candle 4 조건**

❌ **"곧 더 갈 거야" 욕심**
✅ **자리 미달 = skip. 다음 setup 기다림**

❌ **짤짤이 후 큰 베팅 (averaging up = top buy 변종)**
✅ **신규 setup 확인 후만**

### 더 깊이

- **NotebookLM**: "Pullback Fibonacci retracement + 차트프로 차트편 + 김직선" cross-query
- **detail.md**: `03_trend_following/detail.md` §Pullback (Linda Raschke)
- **권위자**: Linda Raschke ("Holy Grail" pattern), Adam Grimes (pullback statistics)

---

## 2. 차트 관찰 과제 (매일 5분)

### 매일 5분 루틴

1. NQ 5m + 모든 prior 마킹
2. **Fibonacci Retracement tool** 사용 — 최근 strong leg up 에 fib 그리기
3. 현재가 fib level 확인
4. EMA20/50 touch 여부
5. Pullback 진입 가능성 self-judge

### TV setup

- **Fib Retracement tool** (필수) — 가장 강한 도구. 단축키 alt+F
- "Auto Fib Retracement" indicator (TV 기본) — 자동 fib 그림 (검증용)

### 체크리스트

- [ ] 최근 leg 에 fib 그림
- [ ] 현재 retracement % 식별
- [ ] EMA20/50 confluence
- [ ] PA candle confirm
- [ ] Pullback 분류 (38.2% / 50% / 61.8%) vs Top Buy / Random

### 어려운 케이스

- **연속 leg** (1차 leg → 2차 leg 안에서 또 pullback)
- **Failed pullback** (50% 까지 가서 break 하는 case)
- **신고가 영역** (swing high 마다 갱신, fib 어디부터?)
- **너무 얕은 pullback** — 강한 추세인데 fib 23.6% 만 됨

---

## 3. 일지 마킹

JSON 추가:

```json
{
  ...,
  "fib_retrace_w8": "23.6 / 38.2 / 50 / 61.8 / 78.6 / outside",
  "entry_type_w8": "pullback-382 / pullback-50 / pullback-618 / breakout-retest / **top-buy** / random",
  "bars_since_swing_high_w8": 7,
  "ema20_50_touch_w8": "ema20 / ema50 / both / none",
  "pa_confirm_w8": "yes / no",
  "valid_pullback_setup_w8": "yes / no",
  "top_buy_alarm_w8": "yes (자가 알람) / no"
}
```

**진입 lock 룰** (이번 주 가장 엄격):

- `entry_type_w8 = top-buy` → **즉시 exit, 다시 계산**
- `bars_since_swing_high < 5` AND LONG → **진입 금지** (top buy 위험)
- `fib_retrace < 23.6%` AND `ema20_touch = none` → **wait**
- `valid_pullback_setup = no` → **진입 금지**

---

## 4. 성공 기준 (Tier 2 졸업 시험)

| 기준 | 합격선 |
|---|---|
| Pullback vs Top Buy 정확 분류 | 90%+ |
| **Top Buy 진입** | **0회** ⭐⭐⭐ |
| 38.2-61.8% 진입 비율 (LONG 중) | 70%+ |
| Fib retrace 식별 즉답 | < 30초 |
| **Tier 2 종합** | W5+W6+W7+W8 통합 setup score 4/4 진입 30%+ |

**점수**:
- 모두 충족 + Top Buy 0 → **5점 (Tier 2 졸업)**
- 90%+ + Top Buy 0 → **4점**
- 80% + Top Buy 1회 → **3점** (1주 더, Top Buy = 0 만족까지)
- Top Buy 2+회 → **2점 이하** (자료 다시, W8 반복)

---

## 5. 다음 주 연결 (W9 → Tier 3)

Tier 2 졸업 = "진입 자리 정확도" 체화
Tier 3 시작 = 우리 v3.5 edge 적용 (BURN_X 04:30, BURN_R 22:30)

W9: Momentum 정량 — 진입 timing 의 마지막 filter
W10: ICT 인식 (사용 X)
W11: 04:30 BURN_X
W12: 22:30 BURN_R + Regime A/B

→ Tier 1+2 = "어디서 진입" / Tier 3 = "어떤 edge 시점에"

---

## 6. Pre-Session Card 진화 (Tier 2 졸업 시점 통합)

```
[Pre-Entry 5초 통합 체크 — Tier 2 졸업 형태]:

[W1+W2] 추세 + EMA = 정합/모순?
[W3+W6] SR (static + dynamic) = top buy 위험? confluence?
[W4]    세션 = edge?
[W5]    BB state = mean revert / trend / wait?
[W7]    PA candle = trigger 확인?
[W8]    Pullback type = 38.2/50/61.8 OR breakout retest? (top buy = 진입 금지)
       
Setup score: ?/8
진입? Y/N
```

8 항목 통합 — 압축. 1분 안에 마쳐야.

---

## 7. 권위자 인용

> "Pullback 은 시장의 호흡이다. 호흡을 막으면 죽는다."
> — Linda Raschke

> "Top buy 는 매매가 아니라 도박이다."
> — Mark Douglas (paraphrase)

> "EMA 20 까지 pullback + Bullish engulf = 가장 신뢰할 수 있는 LONG signal."
> — Adam Grimes

> "신고가 직진입은 amateur, pullback 진입은 professional."
> — Brett Steenbarger (paraphrase)

---

## 🔧 Tools

- **Fib Retracement tool** (TV alt+F) — 필수
- **Auto Fib Retracement** indicator (검증용)
- **결합**: prior trend leg + current pullback → fib levels visible

---

## 📌 Common Mistakes (사용자 약점 처방 강화)

| 실수 | 처방 (룰) |
|---|---|
| **신고가 직진입 (Top Buy L5)** | 5봉 + 38.2% 룰 미달 진입 lock |
| **23.6% 만 보고 "pullback" 칭함** | 38.2% 이상만 valid |
| **"이번엔 다를 거야" 욕심** | 룰 = exception 없음 |
| **Pullback 깊을 때 진입 (78.6%+)** | 추세 전환 위험, skip |
| **2번째 leg 진입 timing 놓침** | Multi-leg fib 별도 그리기 |
| **짤짤이 후 averaging up** | 신규 setup 만 — 기존 포지션 add 금지 |

---

## 💡 Daily Discipline (Tier 2 졸업 후 강화)

매 진입 전:
1. **"이게 Pullback 인가, Top Buy 인가?"** 자문
2. 미답 시 진입 금지
3. 답 = "Top Buy 같다" → 즉시 차트 다시 분석
4. 답 = "Pullback 38.2%" → 다른 조건 (W6/W7) 확인 후 진입

---

## 🎓 Tier 2 졸업 selfie

W8 self-test 4점 + Top Buy 0 회 통과 시:

1. progression_log.md 에 "Tier 2 졸업 ✅ (Top Buy 면역 획득)" 기록
2. Pre-Session Card 8항목 통합 형태 정착
3. observation_log review — 가장 강한 pullback case 5개 archive
4. **3일 break** (정리)
5. Tier 3 W9 시작

축하 — 사용자 가장 큰 약점 (top buying) 면역 획득. 이제 우리 v3.5 edge 적용 단계.

---

*W8 시작: W7 통과 후. 어렵다 — 1주 더 가도 OK.*
*Top Buy 진입 0회 미달 시 W8 무한 반복 (절대 진행 X).*
