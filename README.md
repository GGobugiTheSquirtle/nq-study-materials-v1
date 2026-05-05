# NQ 매매 공부 자료 통합 (v1)

> **목적**: NQ (나스닥 100 선물) 단기·스캘프 매매에 통용되는 검증된 개념·기법·분석도구를 유튜브/책/블로그에서 망라 → 사용자 본인 약점 처방으로 활용.
>
> **사용자 약점 (2026-04~05 자가 진단)**: top buying / 물타기 / 희망적 추세지향 (LONG bias) / 짤짤이 후 욕심 / FOMO 식 / 의지 기반 cooldown 실패.
>
> **방향**: 매매 시간 ↓, 공부 시간 ↑. 틈만 나면 읽을 수 있는 자료.
>
> **시작**: 2026-05-06

---

## 우선순위 카테고리 (6)

사용자 약점 처방 우선순위 + scalping 추가:

| # | 카테고리 | 약점 처방 |
|---|---|---|
| 1 | [Trading Psychology](01_psychology/sources.md) | 욕심·물타기·top buying 의 근본 처방 (1순위) |
| 2 | [Price Action 기본](02_price_action/sources.md) | "흐름 읽기" vs "희망적 추세지향" 의 정확한 기준 |
| 3 | [Trend Following / Pullback Entry](03_trend_following/sources.md) | pullback vs top buy 구분 |
| 4 | [ICT / Smart Money Concepts](04_ict_smc/sources.md) | Order Block / FVG / Liquidity (사용자 차트 reference) |
| 5 | [NQ 특화 / Index Futures](05_nq_specifics/sources.md) | KST 21~23 NY open / overnight inventory / opening range |
| 6 | [Scalping 기법](06_scalping/sources.md) | 변동성·속도·힘 적절할 때 (사용자 자가 정의 정확) |

---

## 산출물 단계

| Phase | 내용 | 상태 |
|---|---|---|
| **1A** | 6 카테고리별 source 발견·검증 (이 파일들) | 🟡 진행 중 |
| **1B** | NotebookLM 일괄 import (youtube link / blog URL / book PDF) | ⏳ 대기 |
| **1C** | 카테고리별 핵심 요약 .md (NotebookLM query 활용) | ⏳ 대기 |
| **2 (B)** | HTML 통합 단일 페이지 (검색 가능, 카드형 UI) | ⏳ 대기 |
| **3 (C)** | GitHub Pages 게시 | ⏳ 대기 |

---

## 평가 기준 (각 source 마다)

| 항목 | 의미 |
|---|---|
| **권위 (Authority)** | 저자/채널의 시장 평가, 인용도 |
| **검증성 (Verifiable)** | 정량 근거 또는 long-running 자료 |
| **NQ 적합 (NQ Fit)** | 나스닥 선물 / 단기 매매 특화 정도 |
| **사용자 약점 처방** | top buying / 물타기 / 욕심 / hopeful trend 직접 효용 |
| **언어 / 접근성** | 영어 / 한국어 / 영상 / 책 |
| **무료 / 유료** | source 비용 |

신뢰도 표기: ⭐⭐⭐ (검증된 권위) / ⭐⭐ (참고할 만함) / ⭐ (보조)

---

## NotebookLM 통합 (Phase 1B 완료, 2026-05-06)

### 🆕 신규 notebook (영어 권위자 자료)
- **Title**: NQ Study v1 — English Authorities (Psychology + PA + Trend + Scalp)
- **ID**: `81fe9110-dfe2-4b64-bcd6-c221c36d84c6`
- **Link**: https://notebooklm.google.com/notebook/81fe9110-dfe2-4b64-bcd6-c221c36d84c6
- **Source count**: 19 (Tom Hougaard / Mark Douglas / SMB / ICT / Adam Grimes / Brett Steenbarger / 등)

### 📚 기존 활용 가능 notebook (사용자 NotebookLM 에 이미 import 됨, **총 1,090 source**)

| 카테고리 | 활용 notebook | source 합계 |
|---|---|---|
| **01 Psychology** | 차트프로 심리편 (18) + 전략적 트레이더 리포트 (9) + 월 4억 프로 7원칙 (28) + 잃지 않는 투자 본질 (9) | **64** |
| **02 Price Action** | 차트프로 차트편 (62) + 지지저항/이평선 4개 단편 | **71** |
| **03 Trend Following** | 보조지표편 Strategies (37) + 데이트레이딩편 (29) + 리스크 관리 전문편 (43) | **109** |
| **04 ICT/SMC** ⭐ | ICT Part 1+2+3 (156) + ICT 유니버설 (197) + SMC 전략편 Courses+Crypto (95) + 5개 단편 | **452** |
| **05 NQ Specifics** | 차트프로 해외선물편 (30) + 실전편 (25) + 김직선 100억 해외선물 (136) + 김직선 초보 (7) + 오더플로우 Part 1+2 (59) + 해외파생 위험고지 (19) | **276** |
| **06 Scalping** | 스캘핑 전략 (24) + 아시아 세션 유동성 스윕 스캘핑 (85) + 단타 4개 단편 | **118** |

### Cross-Notebook Query 사용 (NotebookLM MCP)

```
mcp__notebooklm-mcp__cross_notebook_query
- 여러 notebook 동시 query 가능
- 사용 예: "Top buying 욕심 패턴" → 신규 notebook + 차트프로 심리편 + 전략적 트레이더 리포트 통합 답변
```

---

## Source-Level Index

→ 각 카테고리 폴더의 `sources.md` 참조. 모든 source 의 master list 는 `_notebooklm/source_master.md` 에 통합.

---

*마지막 갱신: 2026-05-06*
