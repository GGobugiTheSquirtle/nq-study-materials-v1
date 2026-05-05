# NotebookLM Master Source List — Phase 1A Draft

> **목적**: 6 카테고리 source 통합 — NotebookLM import 우선순위 명시.
> **NotebookLM 한도** (참고): 무료 = 50 sources / Plus = 300 sources / 1 source 당 token 무관 (NLM 자체 처리).

---

## Tier 1 우선 import (NotebookLM 기본 50 source 한도 우선) — 약 30 source

### 📚 Books (5) — PDF 또는 link
| # | 카테고리 | 제목 | 저자 | 비고 |
|---|---|---|---|---|
| B1 | Psychology | Trading in the Zone | Mark Douglas | 1순위 필독 |
| B2 | Psychology | The Daily Trading Coach | Brett Steenbarger | 매매일지 방법론 |
| B3 | Price Action | Trading Price Action TRENDS | Al Brooks | 1500+ pages, reference |
| B4 | NQ Specific | One Good Trade | Mike Bellafiore | prop firm 환경 |
| B5 | Scalping | Forex Price Action Scalping | Bob Volman | 정량 scalp 룰 |

### 🎬 YouTube Channels — Top playlists / videos (15)
| # | 카테고리 | 채널 | 추출 우선 |
|---|---|---|---|
| Y1 | Psychology | Tom Hougaard (@traderTomHougaard) | "Best Loser Wins" 강의 영상 5-10개 |
| Y2 | Psychology | SMB Capital — Psychology playlist | 5-10개 |
| Y3 | Psychology | Anton Kreil (Institute of Trading) | masterclass 영상 핵심 |
| Y4 | Psychology | Mark Douglas lectures (재업로드 채널) | "Trading in the Zone" 오디오 |
| Y5 | Price Action | Al Brooks (@AlBrooksPriceAction) | 무료 강의 영상 |
| Y6 | Price Action | Lance Beggs (@LanceBeggs) | NQ 분석 영상 |
| Y7 | Price Action | Stacey Burke Trading | daily NQ + ICT mix |
| Y8 | Trend | Adam Grimes (@AdamHGrimes) | course material |
| Y9 | ICT/SMC | Inner Circle Trader (Michael Huddleston) | core content (cult-light 영상 우선) |
| Y10 | ICT/SMC | The Trading Channel (Patrick Wieland) | SMC 단순화 |
| Y11 | ICT/SMC | Wysetrade | SMC 5-step entry |
| Y12 | NQ | SMB Capital — NQ playlist | playbook 영상 |
| Y13 | NQ | Convergent Trading | order flow + NQ |
| Y14 | Scalping | BookMap Pro | order flow scalp |
| Y15 | NQ | Brian Shannon (alphatrends) | AVWAP |

### 📰 Blogs / Web articles (10)
| # | 카테고리 | URL | 비고 |
|---|---|---|---|
| W1 | Psychology | TraderFeed (Brett Steenbarger) | 핵심 archive 글 5개 |
| W2 | Psychology | Daniel Crosby blog | "Behavioral Investor" |
| W3 | Price Action | yourtradingcoach.com (Lance Beggs) | 핵심 글 5개 |
| W4 | Price Action | adamhgrimes.com | 핵심 글 |
| W5 | NQ | Adam Mancini Twitter (@AdamMancini4) | 최근 30일 levels |
| W6 | NQ | SMB Capital Blog | playbook posts |
| W7 | NQ | alphatrends.net (Brian Shannon) | AVWAP 글 |
| W8 | ICT | ICT Mentorship 정리 PDF (커뮤니티) | concept 정리 |
| W9 | Trend | CME Group Education | NQ mechanics |
| W10 | Scalping | BookMap blog / case studies | order flow scalp |

### 📄 PDFs / Free Documents (다수)
- Original Turtle Rules PDF (Curtis Faith)
- Wyckoff method PDF excerpts
- ICT concepts community PDF

---

## Tier 2 추후 import (50+ source 시 또는 NLM Plus)

### 한국어 자료 (search 발견 후)
- 한국어 NQ educator
- 한국어 ICT 채널
- 한국어 단타 educator
- 한국어 trading psychology 자료

### 보조 books
- Anna Coulling — VSA
- Van K. Tharp — Position Sizing
- Steve Nison — Candlesticks
- Linda Raschke — Street Smarts
- Mark Fisher — Logical Trader (ACD)

---

## NotebookLM 활용 전략

### Notebook 구조 (1 notebook 또는 6 notebooks?)

**Option A — 1 통합 notebook**:
- 장점: cross-category query 가능 (예: "Top buying 패턴이 ICT 와 Price Action 에서 어떻게 다르게 정의되는가?")
- 단점: 50 source 한도 빠르게 소진 / 응답 noise

**Option B — 6 카테고리 notebook**:
- 장점: 카테고리별 깊이, 각 50 source 가능
- 단점: cross-query 어려움 (notebooklm-mcp 의 cross_notebook_query tool 활용 가능)

**권장**: **Option B** (cross_notebook_query MCP tool 으로 통합 가능, 카테고리별 깊이 확보).

### 카테고리별 핵심 query (NotebookLM 활용)

각 notebook 마다 실행할 핵심 query:
1. "이 자료에서 정의된 [카테고리 핵심 컨셉] 를 한국어 5-10페이지로 요약"
2. "사용자 약점 (top buying / 물타기 / 욕심) 에 직접 적용 가능한 룰 추출"
3. "검증 가능한 entry / exit 정량 룰 추출"
4. "초보 → 중급 → 고급 학습 순서 제안"

---

## 다음 단계 (Phase 1B 진행 절차)

1. **사용자 컨펌**: 위 paradigm + Tier 1 source 30개 OK 인지
2. **WebSearch 보강**: 각 카테고리 핵심 영상 / 글 정확한 URL 확보
3. **NotebookLM 인증** 확인 (`nlm login` 등)
4. **Notebook 생성** (6개 또는 1개)
5. **Source 일괄 import** (URL 기반)
6. **Sample query 실행** → 1 카테고리 (Psychology) 의 summary.md 자동 생성 → 사용자 컨펌
7. 나머지 5 카테고리 일괄 처리

---

## 다음 응답 사용자 옵션

A. **이 paradigm + Tier 1 source list OK** → Phase 1B 진행 (WebSearch + NotebookLM)
B. **카테고리 추가 / 제거** (예: 한국 자료 좀 더, 또는 하나 빼기)
C. **source 추가 (특정 educator)** — 사용자가 알고 있는 인기 채널/책 추가
D. **깊이 조정** — 각 카테고리 30개 → 15개 (선택과 집중) 또는 50개 (전수)

---

*Status: Phase 1A complete. Awaiting user confirmation.*
