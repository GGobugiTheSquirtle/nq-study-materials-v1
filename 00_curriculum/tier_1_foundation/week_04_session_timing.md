# Week 4: 매매 시간대 (Session Timing)

> **목표**: 진입 시점에 "어느 세션? Edge time 인가?" 즉답. 비-edge 시간 진입 자제.
> **기간**: 5 sim 세션 (~1주)
> **전제**: W1+W2+W3 4점 이상 통과
> **Tier 1 마지막 주** — Tier 2 진입 전 종합 self-test

---

## 1. 핵심 개념 (15분)

### NQ 24h 세션 구조 (KST 기준)

```
07:00 ─────────────────── 15:00 ─────────────────── 22:00 ────────────── 06:00 (다음날)
│      Asian session    │   EU session             │  NY session         │
│      (저변동)          │   (전이)                 │  (고변동, 핵심)      │
│                       │                          │                     │
│      특징:            │   특징:                  │  특징:              │
│      - 횡보           │   - 변동성 점진 증가      │  - 22:30 NY open   │
│      - 짤짤이 함정    │   - 15:30 EU open        │  - 23:30 EU close  │
│      - "심심" 진입 위험│   - 16:30 UK open        │  - 04:30 미 EU end │
│                       │                          │                     │
└───────────────────────┴──────────────────────────┴─────────────────────┘

KST 세부:
07:00-15:00 Asian        : 저변동 시간, NQ 큰 추세 X
15:00-22:00 EU             : 변동성 점진 증가, EU 데이터 reaction
22:30-01:00 NY-AM        : ⭐ 핵심 시간, 거래량 peak
01:00-04:00 NY mid-day   : 점심권 — 변동성 감소
04:00-06:00 NY-PM        : ⭐ 04:30 BURN_X edge time (W11)
06:00-07:00 settlement   : globex maintenance
```

### Edge Time vs Non-Edge

**Edge time (우리 v3.5 검증)**:

| 시간 (KST) | 이름 | Sharpe_w (10y) | 비고 |
|---|---|---|---|
| **04:30** | BURN_X | **4.38** | ⭐ 핵심 edge (W11) |
| **22:30** | BURN_R | **4.72** | ⭐ NY open momentum (W12) |
| **03:00** | BURN_X 보조 | 2.30 | regime-robust |
| 21:30 | STRAT_PB | TBD | sim 검증 중 |
| 01:00 | STRAT_PB | TBD | sim 검증 중 |
| 07:00 | STRAT_PB | TBD | sim 검증 중 |

**Non-Edge time** (진입 자제):

| 시간 (KST) | 특징 | 위험 |
|---|---|---|
| 02:00-04:00 | NY 점심권, 변동성 감소 | 짤짤이 함정 |
| 11:00-15:00 | Asian peak, 횡보 | "심심" 진입 (FOMO L4) |
| 06:00-07:00 | settlement 직전, gap risk | 불안정 |
| **22:00-22:30** | NY open 직전 | gap 위험 — 22:30 까지 wait |

### W1+W2+W3+W4 종합 setup

```
GREAT setup (모두 만족):
  W1: uptrend (HH+HL)
  W2: 정배열 + Price > EMA20
  W3: 위 resistance > 1.0 ATR (clear), 아래 support 가까움
  W4: edge time (04:30 / 22:30 / 03:00)
  
  = ⭐⭐⭐⭐⭐ LONG 진입 (사이즈 ↑)


GOOD setup (3/4 만족):
  - 1개 누락 (예: edge time X but 다른 모두 만족)
  
  = ⭐⭐⭐ 진입 OK (사이즈 보통)


WEAK setup (2/4):
  - 추세 약하거나 SR 모호
  
  = ⭐⭐ skip 우선


NO setup (1/4 이하):
  = 진입 금지
```

### 사용자 약점 직결

❌ **"심심해서 진입" (FOMO L4)** — Asian session 에 자주 발생
✅ **Edge time 만 진입 룰** — 비-edge 진입 lock

❌ **22:00-22:30 미리 진입** (NY open 전 fakeout)
✅ **22:30 시그널 확정 후만**

### 더 깊이

- **NotebookLM**: "NY open momentum + 김직선 100억 해외선물" + "오더플로우 Part 1" cross-query
- **detail.md**: `05_nq_specifics/detail.md` §session, `06_scalping/detail.md` §timing
- **차트프로 (한국어)**: NotebookLM "차트프로 해외선물편" 에서 "시간대" 검색

---

## 2. 차트 관찰 과제 (매일 5분)

### 매일 5분 루틴

1. NQ 5m 차트 + W1+W2+W3 마킹 유지
2. **시간대 vertical line** 표시 (07/15/22:30/04:30 KST)
3. **현재 시간 = 어느 세션?** 명명
4. **Edge time 까지 남은 분?** 계산
5. 비-edge 시간이면 진입 금지 자가 lock

### TV setup

- "Sessions" indicator (custom KST timezone) — 세션 자동 표시
- Vertical line tool: 22:30 KST / 04:30 KST 매일 표시
- 시계 widget (KST 표시)

### 체크리스트 (매일)

- [ ] 현재 세션 명명
- [ ] Edge time 인가 비-edge 인가
- [ ] Edge time 까지 남은 시간
- [ ] 비-edge 진입 충동 발생 시 → observation_log

### 어려운 케이스

- **22:30 ±5분** — 정확히 시그널 확정 vs 미리 진입
- **04:30 ±5분** — BURN_X timing
- **Asian peak 13:00 충동** — 가장 흔한 함정

---

## 3. 일지 마킹 (모든 트레이드)

JSON 추가:

```json
{
  ...,
  "session_w4": "asian / eu / ny-am / ny-pm / 0430 / overnight / settlement",
  "edge_time_w4": "yes (0430/2230/0300) / weak-edge (2130/0100/0700) / non-edge",
  "minutes_to_edge_w4": 12,
  "non_edge_entry_w4": "yes / no",
  "w1_w2_w3_w4_setup_score": 4    // 4/4 만족 = great setup
}
```

**진입 lock 룰** (이번 주 추가):

- `non_edge_entry_w4 = yes` AND **이유 없음** → **진입 금지**
- `setup_score = 4/4` → 사이즈 ↑ 가능
- `setup_score = 2/4 이하` → 진입 자제

---

## 4. 성공 기준 (주말 self-check) — Tier 1 졸업 시험

W4 자체 + Tier 1 종합 평가 (W1~W4 통합).

### W4 단독

| 기준 | 합격선 |
|---|---|
| 진입 시점 세션 마킹 | 100% |
| Edge time 외 진입 (이유 없음) | < 10% |
| 22:30 / 04:30 timing 정확 (±2분) | 90%+ |

### Tier 1 종합

| 기준 | 합격선 |
|---|---|
| W1 추세 식별 | 80%+ |
| W2 EMA 정렬 | 100% |
| W3 SR zone 식별 | 80%+ + top buy 0 |
| W4 세션 식별 | 100% + non-edge 진입 < 10% |
| **종합 setup_score 4/4 진입 비율** | **40%+** (낮아도 OK, 점진 향상) |

**점수**:
- 모두 충족 → **5점** (Tier 1 졸업, Tier 2 진입)
- 80%+ → **4점** (Tier 2 진행 OK)
- 60% → **3점** (1주 더 W4 / Tier 1 부분 보강)
- 미달 → **2점 이하** (Tier 1 다시)

---

## 5. 다음 주 연결 (W5 → Tier 2)

Tier 1 졸업 = "차트 읽기 기본기 4종" 체화
Tier 2 시작 = "진입 자리 정확도" 향상

W5 Bollinger Band: mean reversion vs squeeze breakout
→ W3 SR zone 과 결합하면 **상하단 = SR 보강**

---

## 6. Pre-Session Card 진화

```
W4 추가:
□ 현재 세션 = ? (asian/eu/ny-am/0430/non-edge)
□ Edge time 인가? = Y/N
□ Edge time 까지 남은 분 = ?
□ Setup score (W1+W2+W3+W4) = ?/4
```

누적: W1 4 + W2 3 + W3 4 + W4 4 = **15 항목 (W1~W4)**

→ **압축 필요**. 다음과 같이 통합:

```
[Pre-Entry 5초 통합 체크] (Tier 1 졸업 시점):
□ 추세 + EMA = ? (정합? 모순?)
□ SR 거리 = ? (top buy 위험?)
□ 세션 = ? (edge?)
□ Setup score = ?/4
```

→ 4 항목으로 압축. 각 항목은 W1~W4 마킹의 _aggregate_.

---

## 7. 권위자 인용

> "NY open 후 30분 = 하루의 90% edge."
> — SMB Capital (Bella/Steve)

> "Asian session 은 잠자야 하는 시간이다 — 매매가 아니라."
> — Linda Raschke (NQ 한정)

> "Edge time 외 매매는 도박이다. 시장은 시간을 가린다."
> — 김직선 (한국어, paraphrase)

> "04:30 EU close + NY 마감 직전 = NQ 최고의 momentum window."
> — 우리 v3.5 검증 (Sharpe_w 4.38)

---

## 🔧 Tools

- **TV indicators**:
  - "Sessions" (built-in or community) with KST timezone
  - "Time Vertical Lines" — 22:30 / 04:30 매일 표시
- **Clock**: Windows clock 에 KST + EST 동시 표시 (작업표시줄 추가 시계)
- **Alarm**: 22:25 / 04:25 알림 (5분 전)

---

## 📌 Common Mistakes (사용자 약점)

| 실수 | 처방 |
|---|---|
| **Asian session 심심해서 진입 (L4)** | non-edge 진입 lock |
| **22:30 직전 5분 미리 진입** | 22:30 시그널 확정 후만 |
| **04:30 BURN_X timing 놓침** | 알람 + 미리 차트 watching |
| **NY-PM 02:00 점심권 진입** | non-edge 시간, skip |
| **Settlement 직전 06:00 진입** | gap risk, skip |

---

## 💡 시간 관리 (사용자 라이프스타일)

**현실 권장**:
- **04:30 BURN_X** = 한국 새벽 — 알람 + 5분 만에 trade 후 다시 자기 (자연스럽게 짧은 hold)
- **22:30 BURN_R** = 한국 늦은 저녁 — 일과 후 1시간 집중
- **그 외 시간 = 매매 X, 공부 시간** (이 커리큘럼 시간 ↑)

**위클리 schedule 예시**:
```
월-금: 22:30 KST 1시간 + 04:30 알람 → 새벽 5분 + 다시 자기
주말: self-test + observation_log review + Pre-Session Card 갱신
```

---

## 🎓 Tier 1 졸업 selfie

W4 self-test 4점 이상 통과 시:

1. progression_log.md 에 "Tier 1 졸업 ✅" 기록
2. Pre-Session Card 압축 (4 항목 통합)
3. observation_log review — 가장 어려웠던 chart 5개 archive
4. **3일 break** (학습 휴식, 실전 적용 전 정리)
5. Tier 2 W5 시작

축하 — 차트 읽기 기본기 체화 완료. 이제 진입 자리 정확도 단계.

---

*W4 시작: W3 self-test 4점 이상 후 / Tier 1 종합 self-test: 5 세션 후*
