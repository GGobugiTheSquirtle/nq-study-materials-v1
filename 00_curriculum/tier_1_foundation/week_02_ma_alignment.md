# Week 2: 이평선 정·역배열 (EMA Alignment)

> **목표**: EMA 20/50/200 의 위치만 보고 "정배열 / 혼합 / 역배열" 즉답.
> **기간**: 5 sim 세션 (~1주)
> **전제**: W1 (추세 인식) 4점 이상 통과

---

## 1. 핵심 개념 (15분)

### EMA 란?

Exponential Moving Average — 최근 값에 가중치 부여한 이동평균. SMA 대비 반응 빠름.

```
EMA(20) ≈ 최근 20봉 평균 (가중)
EMA(50) ≈ 최근 50봉 평균
EMA(200) ≈ 최근 200봉 평균 (큰 그림)
```

### 정배열 / 혼합 / 역배열 정의

```
정배열 (Bullish Alignment):
  EMA20 > EMA50 > EMA200
  Price > EMA20

  ↑↑↑ (강세 추세 진행 중)


혼합 (Mixed / Transition):
  EMA20 > EMA50 < EMA200    (or 다른 조합)
  Price ↔ EMA20

  ←→ (전환 중 / 횡보 / 약한 추세)


역배열 (Bearish Alignment):
  EMA20 < EMA50 < EMA200
  Price < EMA20

  ↓↓↓ (약세 추세 진행 중)
```

### 왜 EMA 인가? (vs SMA)

- **반응 속도**: 5m 봉 진입 timing → EMA가 SMA보다 빠르게 turn
- **NQ 특성**: NQ 는 빠른 momentum 자산 → 늦은 SMA 는 entry miss
- **글로벌 표준**: 김직선·차트프로·Brett Steenbarger 등 EMA 위주 사용

### W1 추세 + W2 EMA = 강한 신호

| W1 추세 | W2 EMA | 종합 신호 |
|---|---|---|
| Uptrend (HH+HL) | 정배열 | ⭐⭐⭐ 강세 LONG bias |
| Uptrend | 혼합 | ⭐⭐ 약한 LONG (확인 필요) |
| Uptrend | 역배열 | ⚠️ **모순** — 추세 전환 진행 중. 진입 보류. |
| Range | 정배열 | ⭐ 정배열 후 횡보 — 다음 추세 방향 가능성 LONG |
| Range | 역배열 | (대칭) SHORT 가능성 |
| Downtrend | 역배열 | ⭐⭐⭐ 강세 SHORT bias |

### 사용자 약점 직결

❌ **역배열인데 LONG 진입 (희망적 추세지향, L41)** — "곧 turn 하겠지"
✅ **EMA 정배열 확인 → LONG / 역배열 확인 → SHORT** (모순 시 진입 금지)

❌ **Price > EMA20 인데 SHORT** (W3 SR 까지 확인 후라면 OK 한정 케이스)
✅ **Price 와 EMA20 의 관계 = 1차 trend filter**

### 더 깊이

- **NotebookLM**: "EMA 50 200 정배열 매매 + 차트프로 차트편" cross-query
- **detail.md**: `03_trend_following/detail.md` §Moving Averages
- **김직선 (한국어)**: NotebookLM "김직선 100억 해외선물" notebook 에서 "이평선" 검색
- **글로벌 표준**: EMA 8/21 (단기 swing trader) vs 20/50/200 (포지션 trader) — 5m scalping 은 **20/50/200**

---

## 2. 차트 관찰 과제 (매일 5분)

### 매일 5분 루틴

1. NQ 5분봉 차트 열기 + EMA 20 (yellow) / 50 (orange) / 200 (red) overlay
2. **현재 시점 정렬 상태 명명**: 정 / 혼 / 역
3. **Price 와 EMA20 의 관계**: 위 / 아래 / touching
4. **W1 추세와 일치 여부**: 일치 / 모순
5. (선택) 캡처 → observation_log

### TV 차트 setup

```
Indicator 1: Moving Average — EMA, length 20, color yellow
Indicator 2: Moving Average — EMA, length 50, color orange
Indicator 3: Moving Average — EMA, length 200, color red
```

### 체크리스트

- [ ] EMA 3개 visible
- [ ] 정렬 명명 (정/혼/역)
- [ ] Price-EMA20 관계
- [ ] W1 추세와 일치 여부
- [ ] 모순 케이스 1개 발견 시 → observation_log

### 어려운 케이스 (의도적 노출)

- **EMA20 cross EMA50** (전환 시작) — 어떻게 보일지
- **Price 가 EMA20 위 아래 핑퐁** (혼합 → 어느 방향?)
- **Price > EMA200 + EMA20 < EMA50** (모순 시그널)

---

## 3. 일지 마킹 (모든 트레이드)

JSON 추가:

```json
{
  "trend_5m_w1": "uptrend / downtrend / range / unclear",
  "trend_15m_w1": "...",
  "trend_alignment_w1": "...",
  "ma_alignment_w2": "정 / 혼 / 역",
  "price_vs_ema20_w2": "above / below / touching",
  "w1_w2_consistency": "consistent / contradiction"
}
```

**진입 lock 룰** (이번 주 적용):

- W1 = uptrend AND W2 = 역배열 → **진입 금지** (모순 시그널)
- W1 = downtrend AND W2 = 정배열 → **진입 금지** (대칭)
- 일치 (consistent) 만 진입 OK

---

## 4. 성공 기준 (주말 self-check)

| 기준 | 합격선 |
|---|---|
| 차트 5개 → 정렬 정확 | 5/5 (100%) — 시각적 단순 |
| 일지 진입 시 EMA 마킹 누락 | < 5% |
| 모순 시그널 (W1 vs W2) 진입 | **0회** |
| Price-EMA20 관계 즉답 시간 | < 5초 |

**점수**:
- 5/5 + 모순 진입 0 → **5점**
- 4/5 + 모순 1회 → **4점** (W3 진행 OK)
- 3/5 + 모순 2+회 → **3점** (1주 더)

---

## 5. 다음 주 연결 (W3)

W2 EMA = "동적 reference"
W3 SR = "정적 reference (zone)"

→ EMA20 자체가 dynamic SR (W6 에서 다시) — 지금은 정렬만.
→ W3 SR = swing point 기반 zone (선이 아님!) — 진입 자리 정확도

W3 시작 후도 W1 + W2 마킹 계속 누적.

---

## 6. Pre-Session Card 진화

```
W2 추가:
□ 5m EMA 정렬 = ? (정/혼/역)
□ Price vs EMA20 = ? (위/아래/터치)
□ W1 추세와 모순? = ? (모순이면 진입 금지)
```

누적: W1 4 항목 + W2 3 항목 = **7 항목 (W1+W2)**.

---

## 7. 권위자 인용

> "이동평균은 추세의 그림자 — 추세를 보면 EMA가 따라온다."
> — Linda Raschke

> "EMA 200 위 = 강세장, 아래 = 약세장. 그 단순한 룰이 결국 옳다."
> — Stan Weinstein

> "정배열 + Price > EMA20 = 90% 의 LONG 진입 자격."
> — Brett Steenbarger (paraphrase)

---

## 🔧 Tools

- **TV indicators**: EMA 20/50/200 default
- **컬러 권장**: yellow (20) / orange (50) / red (200) — 직관적 contrast
- **추가**: "Moving Average Ribbon" 으로 multiple EMA 한꺼번에 보기 가능 (선택)

---

## 📌 Common Mistakes (사용자 약점)

| 실수 | 처방 |
|---|---|
| 역배열인데 LONG (hopeful trend) | 모순 시그널 진입 lock |
| EMA crossover 후 즉시 진입 | crossover ≠ 신호. retest 후 (W6) |
| EMA20 만 보고 200 무시 | 큰 그림 = EMA200, 작은 그림 = EMA20 |
| Price 가 EMA20 위인지 아래인지 모호 | "확실히 위" 가 아니면 진입 보류 |

---

## 📚 원본 소스 바로가기 (직접 click)

### 영상 (YouTube) — Tier 1
- [Brett Steenbarger blog YouTube + interviews](https://www.youtube.com/results?search_query=brett+steenbarger+moving+average) ⭐⭐⭐ — EMA 200 이상에서만 LONG 룰
- [Adam Grimes — pullback statistics](https://www.youtube.com/@AdamHGrimes) ⭐⭐⭐ — EMA pullback 정량 분석
- [Stacey Burke (NQ daily)](https://www.youtube.com/@StaceyBurkeTrading) ⭐⭐ — daily EMA confluence

### 책 / Free PDF / Blog
- [Linda Raschke "Holy Grail" (free article)](https://www.amazon.com/Street-Smarts-High-Probability-Short-Term-Strategies/dp/0965046109) — 20-period MA pullback (Street Smarts 안에)
- [Stan Weinstein "Secrets for Profiting"](https://www.amazon.com/Secrets-Profiting-Bull-Bear-Markets/dp/1556236832) — Stage analysis + EMA 200 시각
- [Brett Steenbarger TraderFeed blog](https://traderfeed.blogspot.com/) — performance + indicator 상관관계

### NotebookLM 검색
- 🆕 [영어 권위자 notebook](https://notebooklm.google.com/notebook/81fe9110-dfe2-4b64-bcd6-c221c36d84c6) — 위 권위자 자료 19 source
- 추천 query: `"EMA 50 200 정배열" + 김직선 100억 해외선물` (한국어 + 영어 통합)
- 추천 query: `"Moving Average pullback Holy Grail" + 보조지표편 Strategies`

### 카테고리 sources.md
- [03 Trend Following sources](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1/blob/main/03_trend_following/sources.md) ⭐ — Linda/Adam Grimes/Weinstein
- [03 detail.md](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1/blob/main/03_trend_following/detail.md)
- [05 NQ Specifics sources](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1/blob/main/05_nq_specifics/sources.md)

---

*W2 시작: W1 self-test 4점 이상 후 / 다음 self-test: 5 세션 후*
