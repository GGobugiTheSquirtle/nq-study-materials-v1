# Week 11: 04:30 BURN_X ⭐⭐⭐⭐⭐ (우리 핵심 Edge)

> **목표**: 04:30 KST BURN_X setup 정확 식별 + ATM #1 (60/30/2) 적용 + 알람 + 5분 trade.
> **기간**: 5 sim 세션
> **전제**: Tier 1+2 졸업, W9+W10 통과
> **중요도**: ⭐⭐⭐⭐⭐ — 우리 검증된 진짜 edge (10년 Sharpe_w 4.38)

---

## 1. 핵심 개념 (15분)

### 04:30 KST 가 왜 특별한가?

```
시간대 분석 (10y backtest, ADR-029 stride fix 반영):

KST 04:30 = EST 14:30 (NY)
        = GMT 19:30
        = London close 직후 (GMT 17:00)
        = NY 마감 1시간 30분 전
        
Why edge?
1. London close = European liquidity 빠짐
2. NY 후반 trader 들 마감 reposition
3. 일중 가장 큰 momentum window 중 하나
4. 04:30 후 30분 이내 directional move 빈번
```

**검증 데이터**:
- 10y Sharpe_w **4.38** (모든 regime 에서 robust)
- 기존 6.48 = stride bug 영향 (ADR-029 수정 후 진짜 4.38)
- 2024-2026 Sharpe **유지**
- BULL/BEAR/MIXED 전 regime 작동

### BURN_X Setup 정의 (사용자 매뉴얼)

```
시간: KST 04:30 정확 (±2분)

조건:
1. 04:30 5분봉 시가 (open) 가 trigger 시점
2. W2 EMA20 와의 관계로 방향 결정
   - Open > EMA20 → LONG bias
   - Open < EMA20 → SHORT bias
   - Open = EMA20 ±0.1×ATR → wait (다음 봉)
3. W4 + W9: edge time + momentum 자동 만족
4. Setup score = 4/4 (Tier 1 대부분 자동)

진입:
- Market entry at 04:30 + 0~5 sec
- Pre-placement (기술적 OK, ADR-024 편의 목적)
```

### ATM #1 (60/30/2)

```
SL: 60 ticks (= -$30 per MNQ, -$300 per NQ)
Pre-Trail Distance: 30 ticks
Trail Step: 2 ticks

해석:
- 진입 시 SL = entry - 60 ticks
- profit 30 ticks 도달 시 trail 활성화
- Trail = current price - 30 ticks (2 tick 단위 ratchet)
```

**검증**:
- tick PF **3.81**
- +$171/9 trades (5주, 2026-03~04)
- baseline 60/15/4 대비 +271% Total
- Commission RT $2.18 차감 후 결과
- **trt/SL = 0.50 ≥ 0.30 (positive EV math)**

### 사용자 매뉴얼 Sequence

```
22:00     이른 저녁, normal life
04:25     알람 — 잠 깨기
04:27     차트 빠른 setup 확인:
          - W1: 5m 추세 (uptrend / downtrend / range?)
          - W2: EMA20 위치
          - W3: 가까운 SR
          - W9: 현재 ATR z (보통 +1.0 이상 자연 발생)
04:29:55  주문 준비 (Tradovate ATM #1 selected)
04:30:00  ⚡ Market Entry (방향 = open vs EMA20)
04:30:05  ATM 자동 작동 시작
04:30~05:00 hold (자동 trail or SL hit, 보통 30분 이내 결정)
05:00     trade 종료 → 다시 잠

총 거래 시간: 5분 (04:30 ~ 04:35) + 자동 hold 30분
```

### Regime A/B 결합 (W12 prerequisite)

```
Level A (Aggressive, score ≥ 3):  7~10 ct (sim)
Level B (Defensive, score ≤ 1):   3~5 ct (sim)
Mixed (= 2):                       5~7 ct
```

(W12 에서 자세히 — W11 은 우선 Level B size = 3 ct sim 만 사용)

### 사용자 약점 처방

❌ **04:30 시점 깨도 안 들어감 (의지 부족)**
✅ **알람 + Pre-placement + 5분 trade = 의지 부담 ↓**

❌ **04:30 외 시간 BURN_X 가짜 진입**
✅ **시간 = trigger, 04:30 외 진입 = 다른 setup (BURN_R 등)**

❌ **ATM 무시하고 manual SL/TP**
✅ **ATM #1 자동 — 의지 개입 lock**

### 더 깊이

- **검증 보고서**: `매매일지/해외선물/research/v3.5_burn_x_validation.md` (있으면)
- **CLAUDE.md** §해외선물 MNQ 연구
- **ADR-030 / ADR-029** (전략연구/06_decisions/)

---

## 2. 차트 관찰 과제 (매일 5분)

### 매일 5분 루틴 (5일 04:30)

이번 주는 **5일 동안 04:30 sim 진입 강제** (월~금):

1. 04:25 알람 → 차트 확인
2. 04:27 setup quality 평가 (Tier 1+2 통합)
3. 04:30 BURN_X market entry (방향 결정)
4. ATM #1 자동
5. 05:00 까지 결과 기록

### 일지 즉시 기록

```
04:25 alarm
04:30 entry: LONG @ 17,xxx (open vs EMA20 = +0.3×ATR above)
ATM: 60/30/2 set
04:38 trail activated (P=+30 ticks)
04:52 exit: trail hit @ +27 ticks → +$135 / contract
```

### 어려운 케이스

- **04:30 open 이 EMA20 정확히 통과** — 방향 모호 → wait 1봉
- **04:25 시점 매우 high momentum** (이미 ATR z = +2) — pullback 후 진입?
- **04:30 trade 즉시 SL hit** — discipline (다음 날 재시도)
- **잠 못 깸** — discipline 실패 (이번 주 막아 줘야)

---

## 3. 일지 마킹

매 04:30 trade JSON:

```json
{
  ...,
  "burn_x_0430_w11": {
    "executed": "yes / no (alarm fail / setup mismatch)",
    "open_vs_ema20": "+0.3atr / -0.5atr / equal",
    "direction": "long / short / skip",
    "atm_applied": "60/30/2",
    "size_ct": 3,
    "regime_assumed": "B (default until W12)",
    "exit_type": "trail / sl-hit / time-out",
    "result_ticks": +27,
    "result_usd": 135.00,
    "sleep_recovery": "yes / no (다시 잠 못 들음)"
  }
}
```

**규칙 lock**:
- 04:30 외 진입 BURN_X 명명 금지
- ATM #1 외 SL/TP manual = 룰 위반
- size > 3ct sim (W11 한정) = 룰 위반

---

## 4. 성공 기준

| 기준 | 합격선 |
|---|---|
| 5일 중 04:30 trade 실행 | **5/5** (100%, 의지 시험) |
| ATM #1 정확 적용 | 5/5 |
| 04:30 외 BURN_X 가짜 진입 | 0회 |
| 결과 PF (5 trade) | 1.5+ (small N, but reference) |
| 잠 회복 (다시 잠) | 4/5+ (life sustainability) |

**점수**:
- 5/5 + ATM 정확 → **5점**
- 4/5 + ATM 정확 → **4점** (1일 알람 fail)
- 3/5 또는 ATM 위반 → **3점** (1주 더)

---

## 5. 다음 주 연결 (W12)

W11 = "04:30 단일 edge 적용"
W12 = "22:30 BURN_R + Regime A/B size 자동 전환"

→ 두 edge time + regime size = v3.5 풀 적용
→ Tier 3 졸업 = Tier 4 (Mastery, Apex Eval) 진입 준비

---

## 6. Pre-Session Card 진화

```
W11 추가 (04:30 한정):
□ 04:30 setup score = ?/4
□ Open vs EMA20 = ?
□ ATM #1 selected? = Y/N
□ Size (sim) = 3 ct
```

04:30 모드는 **별도 mini-card**. Daily Pre-Session Card 와 분리.

---

## 7. 권위자 인용

> "Edge 는 시간과 시장 구조의 교차점이다 — 04:30 KST 가 NQ 의 그 점이다."
> — 우리 v3.5 검증 (Sharpe_w 4.38)

> "Mechanical entry + automated exit = remove the trader from the trade."
> — Larry Williams

> "5분 매매가 8시간 매매보다 수익이 클 때, 그건 진짜 edge다."
> — Marty Schwartz (paraphrase)

---

## 🔧 Tools

- **Tradovate**: ATM Templates 사전 생성 (BURN_X 60/30/2 명명)
- **TradingView**: 04:30 KST vertical line + alarm
- **Phone alarm**: 04:25 KST (5분 buffer)

---

## 📌 Common Mistakes

| 실수 | 처방 |
|---|---|
| 04:25 알람 무시, 다시 잠 | 알람 폰 멀리 + 진입 후 5분 후 다시 잠 OK |
| 04:30 외 시간 BURN_X 명명 | 시간 = 룰. 04:25 ~ 04:35 외 X |
| ATM #1 무시, manual SL | ATM 자동 lock, 의지 개입 X |
| Size 4ct+ sim 욕심 | W11 = 3ct lock |
| 잠 못 들어 다음 날 매매 영향 | sleep hygiene 우선 |

---

## 💡 Sleep Hygiene (04:30 매매의 부작용 방지)

- **22:00 취침** → 6.5h 후 04:30
- **04:30 trade 후 다시 잠** → 7-8시 정상 기상
- **trade 결과 즉시 기록** (잠 잊기 전, 1분 voice memo OK)
- **카페인 04:30 후 X** (다시 못 잠)
- **Light 노출 최소** (백라이트 어둡게)

---

## 📚 원본 소스 바로가기 (직접 click) — 우리 v3.5 검증 자료

### 우리 검증 (필수)
- ⭐⭐⭐⭐⭐ [CLAUDE.md §해외선물 MNQ 연구](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1) — 04:30 BURN_X 정의 + Sharpe_w 4.38
- [ADR-029 STRIDE_BARS bug fix](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1) — 진짜 수치 (6.48 → 4.38)
- [ADR-030 ATM 재최적화](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1) — ATM #1 60/30/2 도출
- [ADR-032 운영 플랫폼 (TDV+Tradovate)](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1)
- [ADR-033 Commission RT $2.18 sensitivity](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1)

### 영상 (외부 reference, NY 후반 + EU close)
- [SMB Capital — NY session](https://www.youtube.com/@smbcapital) ⭐⭐⭐ — NY trading hours edge
- [Convergent Trading (order flow + 시간대)](https://www.youtube.com/@ConvergentTrading) ⭐⭐ — NY end + EU close
- [Brian Shannon (Anchored VWAP)](https://www.youtube.com/@AlphaTrendsBrianShannon) ⭐⭐ — session VWAP

### 책 (NY session + Index futures)
- [Mike Bellafiore "One Good Trade" (2010)](https://www.amazon.com/One-Good-Trade-Inside-Trading/dp/0470529660) ⭐⭐⭐ — prop firm NY 세션
- [Mike Bellafiore "The PlayBook" (2013)](https://www.amazon.com/PlayBook-Untold-Story-Quintessential-Trader/dp/1118415302) — playbook = 04:30 BURN_X 와 호환
- [Linda Raschke "Street Smarts"](https://www.amazon.com/Street-Smarts-High-Probability-Short-Term-Strategies/dp/0965046109) — index futures momentum

### Tradovate / TradingView 운영 도구
- [Tradovate ATM Templates docs](https://documentation.tradovate.com/)
- [TradingView Desktop docs](https://www.tradingview.com/desktop/) — 사용자 v3.5 운영 환경
- [Phone alarm app (Android/iOS)](https://www.google.com/search?q=alarm+app) — 04:25 KST 알람 필수

### NotebookLM 검색
- 🆕 [영어 권위자 notebook](https://notebooklm.google.com/notebook/81fe9110-dfe2-4b64-bcd6-c221c36d84c6) — SMB / Bellafiore
- 추천 query: `"NY late afternoon trading + EU close + 04:30 KST"` (시간대 cross-check)
- 추천 query: `"Mike Bellafiore playbook prop firm NY"`

### 매매일지 / research
- [매매일지/해외선물/research/](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1) — 사용자 BURN_X sim 결과 archive
- [LEARNINGS_NQ.md](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1) — NQ 특화 lessons

### 카테고리 sources.md
- [05 NQ Specifics sources ⭐⭐⭐](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1/blob/main/05_nq_specifics/sources.md) — SMB / Bellafiore / CME
- [05 detail.md](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1/blob/main/05_nq_specifics/detail.md)

---

*W11 시작: W10 통과 후 / 5 세션 04:30 강제*
