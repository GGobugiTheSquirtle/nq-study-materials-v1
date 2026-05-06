# Week 9: Momentum vs 횡보 (Volatility Quantification)

> **목표**: ATR z-score / 캔들 body / 진폭으로 "지금 momentum 충분한가" 정량 판단. 횡보 시간 진입 금지.
> **기간**: 5 sim 세션
> **전제**: Tier 2 졸업 (W8 4점, Top Buy = 0)

---

## 1. 핵심 개념 (15분)

### 왜 Momentum 정량인가?

기존 학습 (Tier 1+2) 은 "어디서 진입" 의 자리·구조 분석. 그러나 **변동성이 충분하지 않으면** 좋은 자리도 mean revert 안 함.

```
사용자 약점: "짤짤이 후 욕심 진입" (L5)

→ 짤짤이 = low momentum 시간 (ATR 낮음)
→ "조금 빠지면 들어가야지" 욕심 진입
→ 변동성 부족으로 즉시 mean revert 무동력
→ 손실
```

→ **Momentum 정량 룰**: 진입 trigger 의 마지막 filter.

### 측정 도구 3종

#### 1. ATR z-score

```
ATR(14) = 최근 14봉 평균 진폭
ATR z = (현재 ATR - 60일 평균 ATR) / 60일 표준편차

해석:
  z > +1.0 = 고변동성 (high momentum)
  z = 0    = 평균
  z < -0.5 = 저변동성 (low momentum, 횡보)
```

진입 룰:
- `z > +0.5` → 진입 OK
- `-0.5 < z < +0.5` → context 의존 (Tier 1+2 강한 setup 만)
- `z < -0.5` → 진입 자제

#### 2. 캔들 body 평균

```
Candle body avg (last 5 bars) = 5봉 |close - open| 평균
Candle body / ATR ratio = body avg / ATR

해석:
  ratio > 0.6 = 강한 momentum (강한 directional move)
  ratio = 0.4 = 평균
  ratio < 0.3 = 횡보 (작은 body, indecision)
```

#### 3. 1분 진폭 (sub-minute action)

```
1m candle range = high - low
1m ATR(14) — sub-minute

5m 봉 안의 1m 진폭이 클 = 진짜 momentum
1m 진폭 작 = 5m 봉 fake (한 방향 스무스 X)
```

### Volman scalping criteria (참고)

> Bob Volman ("Forex PA Scalping") — 5m TF momentum 기준:
> 1. ATR z > 0
> 2. last 3 bars body avg ≥ 0.5×ATR
> 3. 진입 candle body ≥ 0.7×ATR
> 4. wick / body ratio ≤ 1.0 (긴 꼬리 없음)

→ 이 4 조건 모두 만족 = "tradeable momentum". NQ 5m 에 그대로 적용 OK.

### Momentum 시간대 매핑 (W4 결합)

| 시간 (KST) | 일반 ATR z | 진입 가치 |
|---|---|---|
| 04:30 BURN_X | **+1.5** (피크) | ⭐⭐⭐⭐⭐ |
| 22:30-23:30 NY open | +1.2 ~ +1.5 | ⭐⭐⭐⭐ |
| 03:00 NY late | +0.8 ~ +1.0 | ⭐⭐⭐ |
| 23:30-01:00 NY mid | +0.5 ~ +0.8 | ⭐⭐⭐ |
| 01:00-04:00 점심권 | -0.3 ~ +0.3 | ⭐ (자제) |
| 11:00-15:00 Asian | -0.8 ~ -0.3 | ⚠️ skip |

→ Edge time = 자연스럽게 high momentum, 비-edge = 자연스럽게 low.

### 사용자 약점 직결

❌ **횡보 시간 (Asian, 점심권) 짤짤이 욕심**
✅ **ATR z < -0.5 = 진입 lock**

❌ **"이번엔 momentum 살아날 거야" 희망**
✅ **fact 기반 — 현재 ATR z 수치로 판단**

❌ **Tier 1+2 setup 충족했지만 momentum 부족**
✅ **모든 setup 통과해도 momentum 미달 = 사이즈 ↓ or skip**

### 더 깊이

- **NotebookLM**: "ATR volatility scalping + 06_scalping" + "오더플로우 Part 1" cross-query
- **detail.md**: `06_scalping/detail.md` §momentum (Volman)
- **권위자**: Bob Volman, Linda Raschke (volatility expansion)

---

## 2. 차트 관찰 과제 (매일 5분)

### 매일 5분 루틴

1. NQ 5m + 모든 prior 마킹
2. **ATR(14) 수치 표시** + ATR z-score (수동 또는 indicator)
3. **Last 5 bars body avg / ATR ratio** 시각 판단
4. **1m 차트 quick check** (5m 진입 시점)
5. Momentum 등급: high (⭐⭐⭐) / mid (⭐⭐) / low (⭐)

### TV setup

- "ATR" indicator (built-in), period 14
- **수동 z-score** — 60일 ATR 평균/std 알려진 값 (NQ 5m 평균 ATR ≈ 12-18, std ≈ 4-6)
- "Volatility Stop" 또는 "Range" indicator (참고)

### 체크리스트

- [ ] 현재 ATR 수치
- [ ] z-score 추정 (high/mid/low)
- [ ] Body/ATR ratio 시각 판정
- [ ] Momentum grade

### 어려운 케이스

- **Volatility expansion 첫 봉** — 갑자기 z 급상승, 진입 timing
- **Slow grind** — 긴 시간 z=0.3 같은 보통, 진입 가치?
- **Volatility spike** (이벤트, FOMC) — 너무 급격, skip 우선

---

## 3. 일지 마킹

JSON 추가:

```json
{
  ...,
  "atr_5m_w9": 14.2,
  "atr_z_w9": 0.7,
  "candle_body_ratio_w9": 0.55,
  "momentum_grade_w9": "high / mid / low",
  "volman_4criteria_w9": "4/4 / 3/4 / 2/4 / <2",
  "low_momentum_skip_w9": "yes / no"
}
```

**진입 lock 룰**:
- `atr_z < -0.5` → **진입 금지**
- `momentum_grade = low` AND `setup_score < 4/4` → **skip**
- `momentum_grade = low` AND `setup_score = 4/4` → 사이즈 ↓ (50%)

---

## 4. 성공 기준

| 기준 | 합격선 |
|---|---|
| Momentum grade 정확 | 80%+ |
| Low momentum 진입 (setup 미달) | 0회 |
| Volman 4 criteria 적용 | 모든 진입 |

---

## 5. 다음 주 연결 (W10)

W9 = "정량적 momentum" (객관 측정)
W10 = "ICT FVG/OB 인식" (사용 X, but 다른 트레이더 차트 reading 용)

W9 통과 후 진정한 v3.5 edge 적용 (W11) 으로.

---

## 6. Pre-Session Card 진화

```
W9 추가:
□ ATR z = ? (high/mid/low)
□ Volman 4 criteria = ?/4
□ Momentum grade = ?
```

8 항목 (Tier 2 통합) + 3 (W9) = **11 항목** (또는 압축 9)

---

## 7. 권위자 인용

> "Volatility expansion = 시장이 결심한 순간. 결심 안 했으면 매매 X."
> — Linda Raschke

> "Volume 과 Volatility 가 함께 = 진짜 trend. 둘 중 하나만 = 함정."
> — Brett Steenbarger

> "ATR 은 시장의 맥박이다. 맥박 약하면 진입 X."
> — Volman (paraphrase)

---

## 📌 Common Mistakes

| 실수 | 처방 |
|---|---|
| 횡보 시간 짤짤이 욕심 | ATR z < -0.5 lock |
| "곧 momentum 올 거야" | fact 기반, 현재 z 만 |
| Setup 만 보고 momentum 무시 | 마지막 filter |

---

## 📚 원본 소스 바로가기 (직접 click)

### 영상 / 채널
- [Linda Raschke — Volatility expansion](https://www.youtube.com/results?search_query=linda+raschke+volatility+expansion) ⭐⭐⭐ — momentum 정의 표준
- [Brett Steenbarger — pace + volatility](https://www.youtube.com/results?search_query=brett+steenbarger+volatility) ⭐⭐⭐
- [BookMap educational (volume + speed)](https://www.youtube.com/@bookmap) ⭐⭐ — DOM 기반 momentum
- [SMB Capital scalp playlist](https://www.youtube.com/@smbcapital) ⭐⭐⭐ — momentum × 시간대

### 책 / Free PDF
- [Bob Volman "Forex Price Action Scalping"](https://www.amazon.com/Forex-Price-Action-Scalping-depth/dp/9090257098) ⭐⭐⭐ — 4 momentum criteria 정의
- [Linda Raschke "Street Smarts" — Volatility chapter](https://www.amazon.com/Street-Smarts-High-Probability-Short-Term-Strategies/dp/0965046109)
- [Anna Coulling "Volume Price Analysis"](https://www.amazon.com/Complete-Guide-Volume-Price-Analysis/dp/1491249390) — VSA = volume + range
- [BookMap learn (free)](https://bookmap.com/learn/) — volume + speed visualization

### NotebookLM 검색
- 🆕 [영어 권위자 notebook](https://notebooklm.google.com/notebook/81fe9110-dfe2-4b64-bcd6-c221c36d84c6)
- 추천 query: `"ATR volatility expansion + 06_scalping + 오더플로우 Part 1"` (118 + 59 source)
- 추천 query: `"momentum criteria pace force"` (영어 + 한국어)
- 추천 query: `"Bob Volman scalping criteria 4"` (영어 specific)

### 카테고리 sources.md
- [06 Scalping sources](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1/blob/main/06_scalping/sources.md) ⭐⭐⭐
- [06 detail.md](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1/blob/main/06_scalping/detail.md)
- [03 Trend Following sources (Linda)](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1/blob/main/03_trend_following/sources.md)

---

*W9 시작: Tier 2 졸업 후 / 5 세션*
