# Week 3: 지지·저항 zone (Support/Resistance)

> **목표**: 차트의 SR zone 을 **선이 아니라 box 로** 식별. 현재가에서 SR 까지 거리를 ATR 단위로 즉답.
> **기간**: 5 sim 세션 (~1주). 어렵다 — 1주 더 가도 OK.
> **전제**: W1 + W2 4점 이상 통과

---

## 1. 핵심 개념 (15분)

### ⚠️ SR 은 선(線)이 아니라 zone(구간)

**글로벌 CLAUDE.md 정의 (재확인)**:

> SR = "해당 가격 근처에서 가격이 자주 꺾이고 추세가 전환된 **구간**". 선이 아니라 **zone**. 주관적이 아니라 **조작적으로 탐지 가능**.

```
잘못된 SR:                  올바른 SR:
                                
  ───────── 18,500           ┌──────────────┐
                              │ 18,490~18,510│  ← zone (±0.25×ATR)
                              └──────────────┘
                              
  단일 가격 = subjective       구간 = objective (touch ≥ 3)
```

### 자동 탐지 알고리즘

1. **Swing pivot** 검출 (fractal, 좌우 5캔들 local max/min)
2. 각 pivot 주변 **±0.25×ATR** = candidate zone
3. 최근 **500봉** 내 해당 zone 범위에 pivot **≥ 3개** → valid SR
4. Zone 강도: `touch_count × time_decay × volume_weight`
5. 겹치는 zone 병합 (overlap > 50%)

### SR 구성 요소 (모두 zone 단위)

| 타입 | 정의 | 우선순위 |
|---|---|---|
| **Pivot 클러스터** | swing H/L ± 0.25×ATR, touch ≥ 3 | ⭐⭐⭐ |
| **POC** (Volume) | 24h/7d POC ± 0.25×ATR | ⭐⭐⭐ |
| **VWAP** | session VWAP ± 0.15×ATR | ⭐⭐ |
| **Order Block** (ICT) | bullish/bearish OB 본체 + 꼬리 반 | ⭐⭐ (W10 학습) |
| **FVG** (ICT) | 미채움 gap 본체 | ⭐⭐ (W10) |
| **전고/전저** | 직전 의미있는 swing H/L ± 0.2×ATR | ⭐⭐⭐ |
| **Round number** | 18,500 / 19,000 등 ± 0.15×ATR | ⭐ |
| **EMA/BB** | reference only — 주요 SR 아님 (W6/W5) | - |

### 거리 측정 = ATR 정규화

```
거리 = |현재가 - zone near edge| / ATR(14)

예:
  현재가: 18,520
  Resistance zone: 18,540~18,560 (NQ 5m, ATR=15)
  near edge = 18,540
  거리 = (18,540 - 18,520) / 15 = 1.33 ATR
```

**해석**:
- 거리 < 0.5 ATR = SR 가까움 (진입 위험)
- 0.5~1.5 ATR = 안전 거리
- > 1.5 ATR = SR 영향 미미

### 진입 룰 (이번 주 적용)

```
LONG 진입 가능 시그널:
  - 위 resistance zone 까지 거리 ≥ 1.0 ATR (위로 갈 공간)
  - 아래 support zone 에서 반등 (zone 내부 또는 edge ±0.1 ATR)

LONG 진입 금지 시그널:
  - 위 resistance zone 거리 < 0.5 ATR ← top buying L5 직접 처방
  - SR zone 정중앙 (방향 미정)

(SHORT 는 대칭)
```

### 사용자 약점 직결 (L5 top buying)

❌ **Resistance 가까운데 LONG** ← 가장 큰 약점
✅ **Support 반등 LONG** OR **Resistance 돌파 후 retest LONG**

❌ **선 하나 그어놓고 "여기 SR"** ← 너무 좁음
✅ **Zone box** 그리고 그 영역 어디든 = SR

### 더 깊이

- **NotebookLM**: "지지저항 zone + 차트프로 차트편" + "지지저항 단편"
- **detail.md**: `02_price_action/detail.md` §SR (Al Brooks/Volman)
- **글로벌 CLAUDE.md**: SR 정의 표준 (선 X, zone)

---

## 2. 차트 관찰 과제 (매일 5분)

### 매일 5분 루틴

1. NQ 5m 차트 열기 (W1+W2 마킹 유지)
2. **최근 500봉** 에서 swing high/low 자동 마킹 (Pivot Points HL indicator)
3. **각 pivot 주변에 box** (±0.25×ATR) 직접 그리기
4. **3+ touch 된 zone 만 강조** (강한 SR)
5. **현재가에서 가까운 SR 2개** (위/아래) 의 거리 ATR 단위 계산

### TV setup

- "Pivot Points HL" indicator (Lonesomethblue)
- ATR(14) indicator (수치 보기)
- "Rectangle" tool — zone box 직접 그리기

### 체크리스트 (매일)

- [ ] swing pivot 자동 마킹 visible
- [ ] zone box 5개 이상 그림
- [ ] 위 resistance 거리 (ATR)
- [ ] 아래 support 거리 (ATR)
- [ ] 진입 가능 / 위험 자가 판정

### 어려운 케이스 (의도적 노출)

- **신고가 영역** (위에 SR 없음 — 어떻게 처리?)
- **clustered SR** (여러 zone 겹침)
- **failed zone** (touch 5번인데 6번째에 깨진 case)
- **전일 high/low 만나는 경우**

---

## 3. 일지 마킹 (모든 트레이드)

JSON 추가:

```json
{
  ...,
  "ma_alignment_w2": "...",
  "sr_above_w3_atr": 1.2,           // resistance까지 거리 (ATR)
  "sr_below_w3_atr": 0.8,           // support까지 거리 (ATR)
  "sr_quality_w3": "strong (touch≥3) / weak (touch<3) / none / clear-air",
  "sr_setup_w3": "support-bounce / resistance-fail / breakout / breakdown / mid-zone / clear",
  "top_buy_risk_w3": "yes (sr<0.5 atr) / no"
}
```

**진입 lock 룰** (이번 주 추가):

- LONG + `top_buy_risk_w3 = yes` → **진입 금지** (top buying)
- SHORT + 아래 support 거리 < 0.5 ATR → **진입 금지** (대칭)
- mid-zone 진입 → **진입 금지** (방향 미정)

---

## 4. 성공 기준 (주말 self-check)

| 기준 | 합격선 |
|---|---|
| 차트 5개 → 강한 SR zone 식별 | 4/5 (80%) |
| 진입 시 SR 거리 마킹 누락 | < 10% |
| **top_buy_risk = yes 인데 LONG 진입** | **0회** ⭐ |
| zone vs 선 구분 무의식적 | 즉시 |

**점수**:
- 모두 충족 → **5점**
- 80% + top buy 진입 0 → **4점** (W4 진행 OK)
- 80% + top buy 1회 → **3점** (1주 더)
- 미달 → **2점 이하** (자료 추가 + 1-2주)

---

## 5. 다음 주 연결 (W4)

W3 SR = "공간축" (어디)
W4 Session = "시간축" (언제)

→ 둘 다 "진입 자리 / 진입 시점" 의 quality filter
→ 둘 다 통과해야 다음 단계로 (Tier 2 setup)

---

## 6. Pre-Session Card 진화

```
W3 추가:
□ 위 resistance zone 거리 = ? (ATR)
□ 아래 support zone 거리 = ? (ATR)
□ Top buy risk (resistance < 0.5 ATR + LONG 충동)? = Y/N
□ Zone 강도 (touch count) = ?
```

누적: W1 4 + W2 3 + W3 4 = **11 항목 (W1+W2+W3)**

이 시점부터 Pre-Session Card 가 "두툼" 해짐 — 압축 필요할 수 있음. **5분 안에 마쳐야**.
W4 후 압축안 도입 검토.

---

## 7. 권위자 인용

> "지지와 저항은 가격의 기억이다 — 가격이 다시 오면, 시장은 기억한다."
> — Adam Grimes

> "선을 긋지 말고 zone 을 그려라. 시장은 정확하지 않다."
> — Al Brooks

> "신고가 매수의 90% 는 잘못된 진입이다. resistance 너머에 다시 resistance 가 있다."
> — Linda Raschke (paraphrase)

> "POC 위에서 LONG, 아래에서 SHORT — 그게 first principle 이다."
> — Volume Profile 권위자 (TPO trading)

---

## 🔧 Tools

- **TV indicators**:
  - "Pivot Points HL" (LonesomeTheBlue) — swing point 자동
  - "ATR" (built-in) — 거리 측정
  - "Volume Profile Visible Range" (premium 기능, 무료 대체 OK)
- **Tool**: Rectangle tool 로 zone box 직접 (단축키 alt+R)
- **권장 컬러**: support = green box (semi-transparent), resistance = red box

---

## 📌 Common Mistakes (사용자 약점 — 가장 중요)

| 실수 | 처방 |
|---|---|
| **선만 긋고 zone 무시** | 모든 SR = box (±0.25×ATR) |
| **Resistance 가까운데 LONG (top buy L5)** | top_buy_risk = yes 면 진입 lock |
| **단일 touch zone 도 SR 로 봄** | touch ≥ 3 만 valid (또는 touch=2 + 강도) |
| **신고가 영역 무한 LONG** | clear-air 표시, but 가속도 hard stop 강화 |
| **"여기서 절대 안 떨어져"** | 모든 SR 은 깨진다 — 깨지면 즉시 룰 적용 |

---

## 💡 SR 식별 빠른 trick

1. **차트 줌 아웃** (1000봉) → 큰 그림 SR 보임
2. **수평 line 3개 이상 stacking 보이는 영역** = strong SR
3. **POC 자동 표시** (Volume Profile) — 자주 거래된 가격 = SR
4. **전일 high/low/close** 자동 표시 (TV pre-built)

5분 안에 **5개 zone box** 그리는 연습 — 일주일 반복하면 즉시 보임.

---

*W3 시작: W2 self-test 4점 이상 후 / 다음 self-test: 5 세션 후. 어려우면 1주 더.*
