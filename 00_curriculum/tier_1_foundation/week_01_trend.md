# Week 1: 추세 인식 (Trend Recognition)

> **목표**: 매 차트마다 "Up / Down / Range" 무의식적으로 답할 수 있다.
> **기간**: 5 sim 세션 (~1주)
> **체화 단계**: 관찰 → 마킹 → 적용

---

## 1. 핵심 개념 (15분)

### Dow Theory 기본 — 추세 = 일련의 swing

가격은 직선이 아니라 **swing high (HH/LH) 와 swing low (HL/LL) 의 연속**.

```
Uptrend:                Downtrend:               Range:
        H2(HH)                                       H1=H2=H3
       /                  H1                         ─────
      H1                    \                       │
     / \  L2(HL)             H2(LH)                 │
    /   \/                    \                     │
   L1                          \                    │
                                H3(LH)              ─────
                                  \  L2(LL)         L1=L2=L3
                                   \ /
                                    L1
                                     \
                                      L2(LL)

HH = Higher High      LH = Lower High         flat highs
HL = Higher Low       LL = Lower Low          flat lows
```

**3 상태 정의 (조작적)**:

| 상태 | 정의 (5분 봉 N=20 캔들 기준) | 예시 |
|---|---|---|
| **Uptrend** | 직전 swing high > 그 전 high AND 직전 low > 그 전 low (HH+HL) | 04:30 EU close 후 NQ 모멘텀 |
| **Downtrend** | LH+LL (대칭) | NY-PM 23:00 후 약세 흐름 |
| **Range** | HH/HL 도 LH/LL 도 안 됨 (flat) | Asian session typical |

**Swing point 검출**: 한 캔들 좌우 N개 (보통 5) 캔들이 모두 lower → 그 캔들이 swing high (fractal). 자동 indicator 사용 가능 (TradingView "ZigZag" 또는 "Pivot Points HL").

### 흔한 오류 (사용자 약점 직결)

❌ **하나의 캔들로 판단** — "지금 빨간 캔들이니까 downtrend" → swing 봐야.
❌ **timeframe 혼동** — 1분 uptrend 인데 15분 downtrend → 큰 timeframe 우선.
❌ **희망적 추세지향 (LONG bias)** — Range 인데 "곧 추세 갈 거야" → Range 면 Range, fact 만.

### Multi-timeframe 검증

```
15m: Uptrend (HH+HL 명확)
 5m: Pullback within 15m uptrend (LH+LL 잠시)
 1m: Range (전이 구간)
```

→ 진입 timeframe (5m) 추세 vs 상위 (15m) 추세 일치 = 강한 setup.
→ 불일치 = 약한 setup, skip 우선.

### 더 깊이

- **NotebookLM cross-query**: "Dow Theory swing point 정의 + 차트프로 차트편" 검색
- **detail.md 연결**:
  - `02_price_action/detail.md` §추세 (Al Brooks 정의)
  - `03_trend_following/detail.md` §Dow Theory + Linda Raschke
- **차트프로 (한국어)**: NotebookLM "차트프로 차트편" notebook 에서 "추세선" 검색

---

## 2. 차트 관찰 과제 (매일 5분)

### 매일 5분 루틴

1. NQ 5분봉 차트 열기 (TradingView)
2. **최근 50봉** 에서 swing high (HH/LH) 와 swing low (HL/LL) 직접 마킹
3. **상위 timeframe (15m, 1h)** 같은 작업
4. 3 timeframe 모두에 대해 "Up / Down / Range" 명명
5. 일지 (옵션 — observation_log.md) 에 캡처 + 1줄 메모

### 체크리스트 (매일)

- [ ] 5분봉 swing 마킹 완료
- [ ] 15분봉 swing 마킹 완료
- [ ] 1시간봉 swing 마킹 완료
- [ ] 3 timeframe 일치/불일치 표기
- [ ] (선택) 어려운 chart 1개는 캡처 → observation_log

### 어려운 케이스 (의도적 노출)

3주차에 어려운 케이스 일부러 보기:

- **추세 전환 직후** (HH 깨짐, HL 형성 시작)
- **확장 횡보** (Asian session 02:00-04:30)
- **Fake breakout** (HH 만들고 즉시 LL)

---

## 3. 일지 마킹 (모든 트레이드)

### Pre-Entry (진입 전 5초)

JSON 추가 필드:

```json
{
  "trend_5m_w1": "uptrend / downtrend / range / unclear",
  "trend_15m_w1": "uptrend / downtrend / range / unclear",
  "trend_1h_w1": "uptrend / downtrend / range / unclear",
  "trend_alignment_w1": "all-up / all-down / mixed / none"
}
```

### Post-Trade (청산 후 1분)

- 진입 시 추세 명명이 정확했는지 self-check
- 부정확했으면 observation_log 에 "wrong call: ___ → 실제 ___" 기록

---

## 4. 성공 기준 (주말 self-check)

토요일/일요일 30분 self-test:

| 기준 | 합격선 |
|---|---|
| 차트 5개 (랜덤 NQ 5m, 50봉) → "Up/Down/Range" 정확 | **4/5 (80%)** |
| 일지 진입 마다 trend 마킹 누락률 | **< 10%** |
| 3 timeframe 동시 식별 시간 | **< 60초** |
| Range 인데 LONG 충동 진입 (희망적 추세) | **0회** |

**점수**:
- 모두 충족 → **5점** (체화 완료, W2 진행)
- 80% 정도 → **4점** (W2 진행 OK)
- 60% 정도 → **3점** (1주 더 W1)
- 50% 미만 → **2점 이하** (자료 추가 학습 + 1-2주 더)

---

## 5. 다음 주 연결 (W2)

W1 추세 = "전체 그림"
W2 EMA = "추세를 정량화한 도구"

→ Uptrend (W1) + EMA20 > EMA50 > EMA200 (W2) = "정배열 강세"
→ W1 차트만 보는 것 → W2 EMA 추가하면 더 빠르게 판단

W2 시작 전 W1 누적 유지: trend 마킹 계속.

---

## 6. Pre-Session Card 진화

세션 시작 전 추가할 항목:

```
W1 추가 (현재 W1 학습 중):
□ 5m 추세 = ? (Up/Down/Range)
□ 15m 추세 = ? (Up/Down/Range)
□ 정렬 = ? (all-up / all-down / mixed)
□ Range 인데 충동 진입 위험 자각?
```

기존 8 → 10 Gate 에 위 4개 추가 (총 12 항목) — 단, **Pre-flight 5분 안에**.

---

## 7. 권위자 인용 (학습 동기)

> "추세는 친구다 — 그러나 끝까지 가지 마라."
> — Marty Schwartz (1980s SnP 챔피언)

> "Higher highs and higher lows — 그게 전부다. 나머지는 노이즈."
> — Linda Raschke

> "추세를 안 보면, 당신은 random walk 에 베팅하고 있다."
> — Al Brooks

---

## 🔧 Tools

- **TradingView**: 기본. ZigZag indicator 추가 권장.
- **Indicator**: "Pivot Points HL" by LonesomeTheBlue (TV 무료)
- **Setting**: ZigZag depth = 5 (5m 봉 기준)

---

## 📌 Common Mistakes (사용자 약점)

| 실수 | 처방 |
|---|---|
| Range 에서 LONG 충동 (FOMO L4) | trend = range 마킹 시 자동 진입 lock |
| 1분만 보고 추세 판단 | 15m + 1h 필수 동시 보기 |
| swing 안 보고 캔들만 봄 | 5초 더 써서 swing 먼저 |
| "곧 추세 갈 거야" (희망) | Fact: HH+HL 형성됐는가? Yes/No |

---

*W1 시작: 2026-05-06 / 다음 self-test: 2026-05-12 (or 5 세션 후)*
