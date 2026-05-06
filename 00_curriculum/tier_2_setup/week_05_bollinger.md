# Week 5: 볼린저밴드 (Bollinger Bands)

> **목표**: BB 상하단 위치 + Squeeze/Expansion 즉답. Mean reversion vs Breakout 구분.
> **기간**: 5 sim 세션 (~1주)
> **전제**: Tier 1 (W1-W4) 졸업 (4점+)

---

## 1. 핵심 개념 (15분)

### Bollinger Band 정의

```
Middle Band  = SMA(20) (또는 EMA(20))
Upper Band   = Middle + 2σ (표준편차)
Lower Band   = Middle - 2σ
```

- σ (sigma) = 최근 20봉 close 의 표준편차
- 가격은 **95% 의 시간** Upper~Lower 사이 (정규분포 가정)
- 따라서 Upper touch / Lower touch = 통계적 outlier

### 두 가지 사용법 (정반대)

**1. Mean Reversion (평균 회귀)** — Range 시장

```
Lower touch → 반등 LONG (mid band 까지 target)
Upper touch → 반락 SHORT
```

조건: **W1 = Range AND W2 = 혼합**. 추세 시장에서 사용 X.

**2. Squeeze → Expansion Breakout** — 추세 시작

```
Squeeze: BBW (Band Width) < 최근 20일 BBW 의 20% (좁아짐)
↓
Expansion: 갑자기 vol 증가 → upper/lower 깨고 폭발
```

조건: BB 좁아진 후 broke out → 그 방향 LONG/SHORT.

### BBW (Bollinger Band Width)

```
BBW = (Upper - Lower) / Middle × 100
    = 2σ / Middle × 100

Squeeze: BBW < BBW.percentile(20) (역사적 하위 20%)
Expansion: BBW > BBW.percentile(80)
Normal: 20 ~ 80 percentile
```

### 결합 시그널

| W1 추세 | W2 EMA | W5 BB | 결론 |
|---|---|---|---|
| Range | 혼합 | Lower touch | ⭐⭐⭐ Mean revert LONG |
| Range | 혼합 | Upper touch | ⭐⭐⭐ Mean revert SHORT |
| Range | 혼합 | Squeeze | ⏳ Wait — breakout 대기 |
| Uptrend | 정배열 | Squeeze→Up break | ⭐⭐⭐ Trend continuation LONG |
| Uptrend | 정배열 | Upper touch | ⚠️ 강세 추세에 자주 발생 — SHORT 금지! |
| Downtrend | 역배열 | Lower touch | ⚠️ 약세 추세 normal — LONG 금지! |

**핵심 룰**: 추세 시장에서는 **upper touch ≠ SHORT signal** (계속 갈 수 있음).

### W3 SR 결합 = 강력

```
Lower BB + Support zone 겹침 → ⭐⭐⭐⭐ LONG
Upper BB + Resistance zone 겹침 → ⭐⭐⭐⭐ SHORT
BB Squeeze + SR 돌파 → ⭐⭐⭐⭐ Breakout
```

### 사용자 약점 직결

❌ **Uptrend 인데 Upper BB touch → SHORT** (역배열 진입, L41 selectivity collapse)
✅ **Range 확인 후 만 mean revert**

❌ **Squeeze 중에 진입** (방향 미정)
✅ **Breakout 후 retest 확인 후 진입 (W6/W8 연결)**

### 더 깊이

- **NotebookLM**: "Bollinger Band squeeze + 보조지표편 Strategies" cross-query
- **detail.md**: `03_trend_following/detail.md` §Bollinger
- **권위자**: John Bollinger 본인 ("Bollinger on Bollinger Bands" book)

---

## 2. 차트 관찰 과제 (매일 5분)

### 매일 5분 루틴

1. NQ 5m 차트 + W1+W2+W3+W4 마킹 유지
2. **BB(20, 2σ) overlay** 추가
3. **BBW indicator** 추가 (별도 panel)
4. 현재 BB 위치 명명: upper-touch / mid / lower-touch / squeeze / expansion
5. W1 추세와 결합해 mean revert vs trend continuation 판정

### TV setup

- "Bollinger Bands" indicator (built-in), length 20, stdev 2.0
- "Bollinger Bands Width" (built-in)
- BBW 에 horizontal line: percentile 20 / percentile 80 (수동 설정 또는 plugin)

### 체크리스트 (매일)

- [ ] BB 위치 명명
- [ ] BBW = squeeze / normal / expansion
- [ ] W1 추세와 결합 판정
- [ ] (선택) 진입 가능 setup vs skip 판정

### 어려운 케이스

- **BB walking the band** — uptrend 강할 때 upper band 따라 계속 감 (SHORT 함정)
- **False squeeze breakout** — squeeze 후 즉시 reverse
- **Squeeze extended** — 며칠 동안 squeeze 유지 (인내 필요)

---

## 3. 일지 마킹

JSON 추가:

```json
{
  ...,
  "bb_state_w5": "upper-touch / mid / lower-touch / squeeze / expansion",
  "bbw_percentile_w5": 25,        // 0~100
  "bb_setup_w5": "mean-revert / trend-continuation / breakout / wait",
  "bb_w1_consistency_w5": "ok / mismatch (예: trend 인데 mean revert 시도)"
}
```

**진입 lock 룰**:
- W1 = uptrend AND BB upper touch SHORT → **진입 금지** (walking the band 함정)
- BB squeeze 중 진입 → **진입 금지** (방향 미정)

---

## 4. 성공 기준

| 기준 | 합격선 |
|---|---|
| BB 위치 식별 | 5/5 |
| BBW squeeze 식별 | 80%+ |
| Walking-the-band 함정 진입 | **0회** ⭐ |
| W1 결합 판정 정확 | 80%+ |

---

## 5. 다음 주 연결 (W6)

W5 BB middle = SMA20/EMA20 (W2 와 같은 EMA) — 즉, **EMA20 이 dynamic SR**
W6 = EMA 자체를 SR 로 사용 (BB middle 의 본질)

→ W5 BB band 보다 BB middle (EMA) 이 더 자주 터치됨
→ W6 에서 EMA SR pullback 룰

---

## 6. Pre-Session Card 진화

W5 추가 (압축):
```
□ BB 위치 + BBW state = ?
□ Setup type (mean revert / trend cont / breakout / wait) = ?
```

누적 압축: 4 (Tier 1 통합) + 2 (W5) = **6 항목**

---

## 7. 권위자 인용

> "BB는 답을 주지 않는다. BB는 질문을 한다 — 정상인가, outlier 인가?"
> — John Bollinger

> "Walking the band — 강세장의 자연스러운 행동이다. SHORT 진입의 빨간 불."
> — Linda Raschke

---

## 📌 Common Mistakes

| 실수 | 처방 |
|---|---|
| Walking the band → SHORT | W1 trend 우선 룰 |
| Squeeze → 즉시 진입 | breakout 확인 후 retest 진입 |
| BB만 보고 W1/W3 무시 | Tier 1 통합 우선 |

---

## 📚 원본 소스 바로가기 (직접 click)

### 영상 / 채널
- [John Bollinger 본인 강연 (검색)](https://www.youtube.com/results?search_query=john+bollinger+bollinger+bands) ⭐⭐⭐ — 창시자 본인 정의
- [Linda Raschke — Volatility expansion 인터뷰](https://www.youtube.com/results?search_query=linda+raschke+volatility+expansion) ⭐⭐⭐ — squeeze→expansion 정의
- [Adam Grimes blog — BB statistics](https://adamhgrimes.com/blog/) ⭐⭐⭐ — BB walking-the-band 통계

### 책 / Free PDF
- [John Bollinger "Bollinger on Bollinger Bands" (2001)](https://www.amazon.com/Bollinger-Bands-John/dp/0071373683) — 창시자 표준 교과서
- [Linda Raschke "Street Smarts"](https://www.amazon.com/Street-Smarts-High-Probability-Short-Term-Strategies/dp/0965046109) — Volatility 기반 setup
- [TradingView Bollinger Bands docs](https://www.tradingview.com/support/solutions/43000501840/) — indicator 사용법

### NotebookLM 검색
- 🆕 [영어 권위자 notebook](https://notebooklm.google.com/notebook/81fe9110-dfe2-4b64-bcd6-c221c36d84c6)
- 추천 query: `"Bollinger Band squeeze" + 보조지표편 Strategies` (37 source)
- 추천 query: `"BB walking the band trend continuation"` (영어 + 한국어)

### 카테고리 sources.md
- [03 Trend Following sources](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1/blob/main/03_trend_following/sources.md)
- [03 detail.md](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1/blob/main/03_trend_following/detail.md)

---

*W5 시작: Tier 1 졸업 후 / 5 세션 후 self-test*
