# Week 12: 22:30 BURN_R + Regime A/B (커리큘럼 졸업)

> **목표**: 22:30 NY open BURN_R 적용 + Regime A/B 자동 size 전환. 12주 커리큘럼 졸업 → Tier 4 (Mastery) 준비.
> **기간**: 5 sim 세션
> **전제**: W11 (04:30) 4점+
> **중요도**: ⭐⭐⭐⭐⭐ — Tier 3 졸업 시험 + 우리 v3.5 두번째 핵심 edge

---

## 1. 핵심 개념 (15분)

### 22:30 KST = NY Cash Open

```
KST 22:30 = EST 09:30 (NY)

NY open = 일중 가장 큰 이벤트 (US 주식 시장 open)
NQ futures 는 globex 24h, but 22:30 액션 폭발

검증 데이터:
- 10y Sharpe_w 4.72 (모든 weight 평균)
- 2024-2026 Sharpe 4.77 (CI95 [+3.01, +6.88])
- 2022 베어 시기에도 Sharpe 5.96 (regime robust)
- 진짜 edge 발현 = 2020+ (2016-2019 marginal)
```

### BURN_R Setup (Reversal vs Continuation)

BURN_R = "Burn at NY Reversal" — 22:30 시점 가격 reversal pattern.

```
시간: KST 22:30 정확 (±2분)

조건:
1. 22:25-22:30 마지막 5분 = pre-open positioning (작은 봉)
2. 22:30 5m 봉 시가 → 30분 직전 high/low 비교
   - Open > 직전 30분 high → SHORT bias (gap up reversal)
   - Open < 직전 30분 low  → LONG bias (gap down reversal)
   - Open in range → wait
3. 22:30 봉 close direction 으로 confirm

진입:
- 22:30 close 후 22:35 entry (1봉 confirm)
- 또는 22:30 + 1분 안 빠른 entry (advanced, 22:30 candle 진행 중)
```

### ATM (BURN_R 용)

```
SL: 60 ticks (= -$30 per MNQ)
Pre-Trail: 30 ticks
Trail Step: 2 ticks

→ ATM #1 (BURN_X 와 동일) 사용 OK
또는 2026-04-28 marginal 결과 (PF 1.08) 후 entry rule 재구성 중
```

⚠️ **HYP-021 후보 — entry rule 재구성**:
- v3.4 4.72 sharpe 검증 OK
- v3.5 tick 검증 marginal (PF 1.08)
- → BURN_R 자체 사용 보류 가능. **W12 학습 = 이론 + sim 적용 (실전 보류)**.

### Regime A/B 자동 전환 (ADR-022)

```
Regime Score (4 지표 합산):

1. EMA200 slope ≥ +1%      (5m 차트, 200봉 회귀)
2. Close > EMA200 비율 ≥ 70% (최근 200봉 중)
3. Momentum Sharpe-proxy ≥ +2 (최근 50봉 ROI/std)
4. Recent MDD > -5%        (최근 50봉)

각 만족 = +1 → score 0~4

Level A (Score ≥ 3): 🟢 Aggressive — 7~10 ct sim
Level B (Score ≤ 1): 🔴 Defensive  — 3~5 ct sim
Mixed (Score = 2):    🟡 5~7 ct sim
```

### 사이즈 자동 전환 룰 (Sim)

```
세션 시작 (22:25 또는 04:25):
1. Regime score 측정 (자동 또는 수동)
2. Level 결정
3. ATM size 매핑
4. 진입 시 size 적용

예:
22:25 score = 4 → Level A → 8 ct
22:25 score = 1 → Level B → 4 ct
```

### 사용자 약점 처방 (L48)

❌ **Sim 에서 250ct 같은 비현실 사이즈**
✅ **Regime size 룰 = sim 에서도 max 10ct**

❌ **모든 진입 동일 사이즈**
✅ **regime 따라 자동 변동**

❌ **Level B 인데 욕심으로 Level A 사이즈**
✅ **score 객관 측정 → 자동 적용**

### 12주 커리큘럼 통합 (W1~W11 모두 활용)

```
22:25 Pre-Session (1분):
  W1: 5m + 15m 추세
  W2: EMA 정렬
  W3: 22:30 직전 SR (위 / 아래)
  W4: 22:30 = edge time
  W5: BB state
  W6: EMA20 dynamic SR
  W7: 22:30 candle pending
  W8: 22:25 까지 pullback 형태 분석
  W9: ATR z (보통 ↑)
  W10: ICT confluence (참고)
  W11: 22:30 ≠ 04:30, 다른 edge
  W12: Regime score + size 결정
  
→ Setup score 8/8 (Tier 1+2) + Regime A → ⭐⭐⭐⭐⭐
```

### 사용자 매뉴얼

```
21:30     일과 정리 시작
22:00     차트 ON, 천천히 setup 모니터
22:20     Pre-Session Card 작성 (모든 W1~W12 통합)
22:25     Regime score 결정 → ATM size 매핑
22:28     주문 준비 (Tradovate ATM)
22:30:00  ⚡ 22:30 봉 시작 — 시가 vs 직전 30분 H/L
22:30:30  방향 결정 (gap up reversal SHORT vs gap down reversal LONG vs wait)
22:31~22:35  진입 또는 wait
~23:00    1차 trail / SL / 종료
```

### 더 깊이

- **CLAUDE.md** §22:30 BURN_R, §Regime A/B
- **ADR-022** (전략연구/06_decisions/)
- **ADR-030** (ATM 재최적화)

---

## 2. 차트 관찰 과제 (매일 5분)

### 매일 22:30 sim 강제 (월~금 5일)

1. 22:00 차트 ON
2. 22:20 Pre-Session Card 작성
3. 22:25 Regime score 측정 + Level 결정
4. 22:28 주문 준비
5. 22:30 entry 또는 skip
6. 23:00 결과 기록

### TV setup

- KST 22:30 vertical line
- Regime score indicator (custom 또는 수동)
- 직전 30분 H/L 라인

---

## 3. 일지 마킹

```json
{
  ...,
  "burn_r_2230_w12": {
    "executed": "yes / no",
    "regime_score": 3,
    "regime_level": "A / B / Mixed",
    "size_ct": 7,
    "open_vs_30min_hl": "above / below / inside",
    "direction": "long / short / skip",
    "atm_applied": "60/30/2",
    "result_ticks": +18,
    "result_usd": 90.00
  },
  "regime_assessment_w12": {
    "ema200_slope_w12": "+1.5%",
    "close_above_ema200_pct": 75,
    "momentum_sharpe_proxy": 2.4,
    "recent_mdd_pct": -3.2,
    "score": 4
  }
}
```

---

## 4. 성공 기준 (Tier 3 졸업 시험)

| 기준 | 합격선 |
|---|---|
| 5일 중 22:30 sim 실행 | 5/5 |
| Regime score 정확 (자동 검증) | 4/5+ |
| Size 룰 정확 | 5/5 |
| 22:30 외 BURN_R 가짜 진입 | 0 |
| **Tier 3 종합** | W9~W12 모두 4점+ |
| **12주 커리큘럼 통합** | Pre-Session Card 8 항목 + Regime + 04:30/22:30 강제 5/5 |

---

## 5. 12주 졸업 → Tier 4 (Mastery) 진입 조건

### Tier 3 졸업 (W12 5점)
- 모든 W1~W12 4점+ 통과
- Top Buy 진입 0 (W8 누적)
- 04:30 / 22:30 강제 5/5 × 2주 (sim)
- Regime A/B size 룰 자동 적용

### Tier 4 진입 (Mastery) — 모라토리엄 해제 조건과 결합

- 5분봉 컨트롤 체득
- W18~W19 sim 세션 edge 재현 (Python 결과와 ±20% 이내)
- Level B 전환 시나리오 대응 경험
- **+ 12주 커리큘럼 졸업** (이 추가)

→ 모두 만족 = **Apex Eval 진입 준비 완료**.

---

## 6. Pre-Session Card 최종 (12주 졸업 형태)

```
[Pre-Session Card v3 (12주 졸업, 1분 안에 마침)]

22:20 / 04:25 시작:

1. [W1+W2] 추세 + EMA = 정합?
2. [W3+W6] SR = 위/아래 거리, top buy 위험?
3. [W4]   세션 = edge?
4. [W5]   BB state
5. [W7]   PA candle pending
6. [W8]   Pullback or breakout retest?
7. [W9]   ATR z + momentum
8. [W12]  Regime score + Level
9. [W11/W12] ATM template selected?
10. [Sim] Size = ?

진입 결정: setup score ≥ 6/8 + Tier 1 모두 + regime ≥ 2 → entry
       그 외 → skip
```

10 항목, 1분 안에. 매일 22:25 + 04:25 자동.

---

## 7. 권위자 인용

> "NY open 후 30분 = 일중 90% edge."
> — SMB Capital

> "Regime 을 무시하면, 같은 전략이 다른 시장에서 망한다."
> — David Aronson ("Evidence-Based TA")

> "Size 가 곧 risk management. Regime 따라 size 자동 = 인간 약점 (욕심) bypass."
> — Brett Steenbarger

> "Sim 에서도 Regime size 강제 = 실전 transition 안전망."
> — 우리 L48 (sim size non-transferable)

---

## 🎓 12주 커리큘럼 졸업 selfie

W12 self-test 5점 통과 시:

1. progression_log.md 에 "12주 졸업 ✅" 기록
2. observation_log review — 12주 누적 가장 강한/약한 case 5+5 archive
3. Pre-Session Card v3 정착
4. **1주 break** (정리 + 회고)
5. **회고 글**: "12주 동안 무엇이 변했는가" 2 페이지 작성 → 매매일지/research/curriculum_completion_2026_xx.md
6. **모라토리엄 해제 조건 종합 self-evaluation**
7. Tier 4 (Mastery) 진입 준비

---

## 🌟 12주 후 변화 (예상)

- **Top Buy 진입 = 0** (L5 처방 완료)
- **차트 4 timeframe 동시 식별 = 자동**
- **04:30 / 22:30 강제 = habit**
- **Regime score 측정 = 자동**
- **Pre-Session Card 1분 안에 마침**
- **Sim PF 1.5+ 안정**
- **Apex Eval 진입 자격 완료**

---

## 📌 12주 후 다음 단계 (Tier 4 / Real Apex)

```
Month 4:    Tier 4 시작
            - Apex Eval $50k 시작 (real money)
            - R34 sim cap → real Apex Tier 1 size
            - HYP-APEX-001 회피 (5월 5일 사건 교훈)
            - 일중 MDD 매 15분 audit (R30 environment lock)

Month 5+:   Live PA 진입 OR continue sim
            - 12주 만에 모든 약점 처방 완료
            - 새 약점 발견 시 → 새 학습 cycle
```

---

## 📚 원본 소스 바로가기 (직접 click) — 12주 졸업 시험

### 우리 검증 (필수)
- ⭐⭐⭐⭐⭐ [CLAUDE.md §해외선물 MNQ 연구](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1) — 22:30 BURN_R Sharpe 4.72
- ⭐⭐⭐⭐⭐ [ADR-022 Regime-Aware Two-Level](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1) — Regime score 4 지표
- [ADR-029 stride bug fix](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1) — 22:30 진짜 수치
- [ADR-030 ATM 재최적화](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1)

### 영상 / 채널 — NY Open
- [SMB Capital — NY 09:30 EST open](https://www.youtube.com/@smbcapital) ⭐⭐⭐⭐⭐ — "30 분 = 90% edge"
- [Mike Bellafiore — opening drive](https://www.youtube.com/results?search_query=mike+bellafiore+opening+drive) ⭐⭐⭐
- [Adam Mancini Twitter (@AdamMancini4)](https://twitter.com/AdamMancini4) ⭐⭐⭐ — 매일 무료 NQ/ES levels (NY open 직전)
- [Convergent Trading (NY open + order flow)](https://www.youtube.com/@ConvergentTrading) ⭐⭐ — DOM + NY open

### 책 / Free PDF
- [Mike Bellafiore "One Good Trade"](https://www.amazon.com/One-Good-Trade-Inside-Trading/dp/0470529660) ⭐⭐⭐ — NY open prop firm
- [Mike Bellafiore "The PlayBook"](https://www.amazon.com/PlayBook-Untold-Story-Quintessential-Trader/dp/1118415302) ⭐⭐⭐ — 22:30 BURN_R = "playbook setup"
- [Brian Shannon "Maximum Trading Gains with AVWAP"](https://www.amazon.com/Maximum-Trading-Gains-Anchored-VWAP/dp/0982118503) ⭐⭐⭐ — session AVWAP at NY open
- [David Aronson "Evidence-Based TA"](https://www.amazon.com/Evidence-Based-Technical-Analysis-Statistical-Methods/dp/0470008741) ⭐⭐ — Regime detection 통계
- [CME Group educational](https://www.cmegroup.com/education.html) — RTH (NY) open 정의

### NQ 특화 한국어 (NotebookLM 1,090 source)
- [김직선 100억 해외선물 (136 source)](https://notebooklm.google.com) — KST 22:30 매매 사례
- [차트프로 해외선물편 (30) + 실전편 (25)](https://notebooklm.google.com)
- [오더플로우 Part 1+2 (59)](https://notebooklm.google.com)

### NotebookLM 검색
- 🆕 [영어 권위자 notebook](https://notebooklm.google.com/notebook/81fe9110-dfe2-4b64-bcd6-c221c36d84c6) — SMB + Bellafiore
- 추천 query: `"NY open 22:30 KST gap reversal" + 김직선 100억 + 차트프로 해외선물편`
- 추천 query: `"Regime detection trend regime market regime"` (영어)
- 추천 query: `"opening drive playbook NY"` (영어 + 한국어 통합)

### Apex / 프롭펌 호환 (Tier 4 준비)
- [Apex Trader Funding rules](https://www.apextraderfunding.com/) — Eval $50k / PA Tier 1 / DLL
- [LEARNINGS.md L48 (sim size non-transferable)](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1)
- [HYP-APEX-001 보고서](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1) — Apex Compatibility Bundle 5종

### 매매일지 / research
- [매매일지/해외선물/research/](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1) — 22:30 BURN_R sim 결과
- [LEARNINGS_NQ.md](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1) — NQ 22:30 / NY open lessons
- [PRE_SESSION_CARD.md](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1) — 운영 카드

### 카테고리 sources.md
- [05 NQ Specifics sources ⭐⭐⭐⭐⭐](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1/blob/main/05_nq_specifics/sources.md)
- [05 detail.md](https://github.com/GGobugiTheSquirtle/nq-study-materials-v1/blob/main/05_nq_specifics/detail.md)

---

*W12 시작: W11 통과 후 / 5 세션 22:30 강제*
*졸업 = Tier 4 진입 자격 + Apex Eval 준비 완료*
