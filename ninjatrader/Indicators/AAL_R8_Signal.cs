// =============================================================================
// AAL_R8_Signal — Cross + ADX + RETEST + R8 Exit (NinjaTrader 8) v1.0
// =============================================================================
// 검증: HYP-MAX-005 (2026-04-30) — BTC 3y + NQ 17.3y
//   BTC 4h: WR 81%, PF 3.08, mean_net +0.90%, AnnRet +4.78%, MDD -6.46%
//   NQ  4h: WR 80%, PF 1.96, mean_net +0.28%, AnnRet +0.75%, MDD -3.08%
//
// 룰 정의:
//   1. HTF (4h 권장) EMA20 × EMA50 GOLDEN cross
//   2. ADX14 ≥ 25 at cross bar (trend strength)
//   3. Retest reclaim within 6 bars (cross 후 EMA20 재테스트 후 close > EMA20)
//   4. Entry: retest reclaim bar close (다음 bar open 으로 매매)
//   5. SL_init = entry - 2.5 × ATR14[at_cross]
//   6. TP1    = entry + 1.2 × ATR14[at_cross]  → 50% close + SL → BE
//   7. 남은 50% = BE ride until time-stop 120h (5 days)
//
// TF guard: 4h 가 best (BTC PF 3.08, NQ PF 1.96).
//   1h: BTC marginal (PF 1.26, AnnRet +2.48%) / NQ NOGO (PF 0.66)
//   15m: 두 자산 모두 NOGO (R8 mechanism 부적합)
//
// 시각:
//   Cross bar: 작은 ▲ + "X" label
//   ADX OK: ▲ 색 진해짐 (lime)
//   Retest reclaim (entry armed): 큰 ★ + entry/SL/TP1 라인 표시
//   Entry, SL, TP1 horizontal line until session end or 120h
//
// 운영 권고:
//   - Bybit BTCUSDT.P linear perpetual (4h)
//   - MNQ futures (4h)
//   - Position sizing: 0.25% risk per trade (R8 spec)
//   - Leverage 1-3x (5x 이상 MDD 위험)
//   - Max concurrent: 1 per asset
//
// 의존: AAL_Shared.cs (AALDirection enum 미사용 — standalone)
// 생성: 2026-05-02 (NT_AAL/Indicators/AAL_R8_Signal.cs)
// =============================================================================

#region Using declarations
using System;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.Windows.Media;
using NinjaTrader.Cbi;
using NinjaTrader.Data;
using NinjaTrader.NinjaScript;
using NinjaTrader.NinjaScript.DrawingTools;
#endregion

namespace NinjaTrader.NinjaScript.Indicators
{
	public class AAL_R8_Signal : Indicator
	{
		#region Parameters — Cross
		[NinjaScriptProperty]
		[Range(5, 100)]
		[Display(Name = "EMA Fast Period", Order = 1, GroupName = "1. Cross")]
		public int EmaFastPeriod { get; set; }

		[NinjaScriptProperty]
		[Range(10, 200)]
		[Display(Name = "EMA Slow Period", Order = 2, GroupName = "1. Cross")]
		public int EmaSlowPeriod { get; set; }
		#endregion

		#region Parameters — Filter
		[NinjaScriptProperty]
		[Range(15, 40)]
		[Display(Name = "ADX Threshold (≥)", Order = 3, GroupName = "2. Filter")]
		[Description("Forensics 25 권장. 20 약함, 30 너무 strict.")]
		public int AdxThreshold { get; set; }

		[NinjaScriptProperty]
		[Range(2, 12)]
		[Display(Name = "Retest Window (bars)", Order = 4, GroupName = "2. Filter")]
		[Description("Cross 후 N bars 내 EMA20 retest reclaim 발생 시 entry. 미발생 시 신호 폐기.")]
		public int RetestWindow { get; set; }
		#endregion

		#region Parameters — Exit (R8)
		[NinjaScriptProperty]
		[Range(1.0, 5.0)]
		[Display(Name = "SL ATR multiplier", Order = 5, GroupName = "3. Exit (R8)")]
		[Description("R8: SL = entry - 2.5 × ATR (wide). 1.5 너무 좁아 wick SL hit. 3.0+ 너무 넓어 capital 비효율.")]
		public double SlAtrMult { get; set; }

		[NinjaScriptProperty]
		[Range(0.5, 3.0)]
		[Display(Name = "TP1 ATR multiplier", Order = 6, GroupName = "3. Exit (R8)")]
		[Description("R8 sweet spot 1.2 (76% TP1 hit rate). 50% close 후 BE 잠금.")]
		public double Tp1AtrMult { get; set; }

		[NinjaScriptProperty]
		[Range(24, 240)]
		[Display(Name = "Time-stop (hours)", Order = 7, GroupName = "3. Exit (R8)")]
		[Description("R8 spec 120h. AAL_HoldTimer CapHours 와 연동.")]
		public int TimeStopHours { get; set; }
		#endregion

		#region Parameters — Display & Alerts
		[NinjaScriptProperty]
		[Display(Name = "Show entry/SL/TP1 lines", Order = 8, GroupName = "4. Display")]
		public bool ShowLevels { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Show diagnostic markers (cross/ADX/retest)", Order = 9, GroupName = "4. Display")]
		public bool ShowMarkers { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Alert on Entry Armed", Order = 10, GroupName = "5. Alerts")]
		public bool AlertOnEntry { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Alert on Cross Detected", Order = 11, GroupName = "5. Alerts")]
		public bool AlertOnCross { get; set; }
		#endregion

		// Indicators
		private EMA emaFast, emaSlow;
		private ATR atr14;
		private ADX adx14;

		// State (per-cross tracking)
		private int crossBarIdx = -1;
		private double crossClose;
		private double crossAtr;
		private bool crossAdxPass;
		private bool retestSeen;
		private bool entryArmed;
		private int activeEntryBar = -1;
		private double activeEntryPx;
		private double activeSlPx;
		private double activeTp1Px;

		protected override void OnStateChange()
		{
			if (State == State.SetDefaults)
			{
				Description = "AAL R8 — 4h cross + ADX + RETEST + Wide SL/TP1+BE (HYP-MAX-005 검증)";
				Name        = "AAL_R8_Signal";
				Calculate   = Calculate.OnBarClose;
				IsOverlay   = true;
				DisplayInDataBox = false;
				DrawOnPricePanel = true;
				PaintPriceMarkers = false;

				EmaFastPeriod  = 20;
				EmaSlowPeriod  = 50;
				AdxThreshold   = 25;
				RetestWindow   = 6;
				SlAtrMult      = 2.5;
				Tp1AtrMult     = 1.2;
				TimeStopHours  = 120;
				ShowLevels     = true;
				ShowMarkers    = true;
				AlertOnEntry   = true;
				AlertOnCross   = false;
			}
			else if (State == State.DataLoaded)
			{
				// TF guard — 4h 권장 (HYP-MAX-005)
				if (BarsPeriod.BarsPeriodType == BarsPeriodType.Minute)
				{
					int v = BarsPeriod.Value;
					if (v != 240)        // not 4h
					{
						string warn = v == 60 ?
							"⚠ AAL_R8: 1h 차트 — BTC marginal (PF 1.26), NQ NOGO. 4h 권장." :
							v <= 15 ?
							"⚠ AAL_R8: " + v + "m — R8 메커니즘 부적합 (LTF 검증 NOGO). 4h 권장." :
							"⚠ AAL_R8: " + v + "m — Forensics 4h 전제. 신뢰도 보장 안 됨.";
						Print(warn);
					}
				}

				emaFast = EMA(EmaFastPeriod);
				emaSlow = EMA(EmaSlowPeriod);
				atr14   = ATR(14);
				adx14   = ADX(14);
			}
		}

		protected override void OnBarUpdate()
		{
			if (CurrentBar < EmaSlowPeriod + 14) return;

			// ─── 1. GOLDEN cross detection ───
			double diffNow = emaFast[0] - emaSlow[0];
			double diffPrev = emaFast[1] - emaSlow[1];
			bool golden = diffPrev <= 0 && diffNow > 0;

			if (golden)
			{
				crossBarIdx = CurrentBar;
				crossClose = Close[0];
				crossAtr = atr14[0];
				double curAdx = adx14[0];
				crossAdxPass = !double.IsNaN(curAdx) && curAdx >= AdxThreshold;
				retestSeen = false;
				entryArmed = false;

				if (ShowMarkers)
				{
					Brush crossBrush = crossAdxPass ? Brushes.Lime : Brushes.DimGray;
					Draw.TriangleUp(this, "R8_X_" + CurrentBar, true, 0,
						Low[0] - atr14[0] * 0.5, crossBrush);
					Draw.Text(this, "R8_Xtxt_" + CurrentBar,
						string.Format("X ADX{0:F0}", curAdx),
						0, Low[0] - atr14[0] * 1.0, crossBrush);
				}

				if (AlertOnCross)
					Alert("AAL_R8_X_" + CurrentBar, Priority.Medium,
						string.Format("R8 CROSS — ADX {0:F1} {1}", curAdx, crossAdxPass ? "PASS" : "FAIL"),
						NinjaTrader.Core.Globals.InstallDir + @"\sounds\Alert2.wav",
						5, Brushes.White, Brushes.DarkGreen);
			}

			// ─── 2. Retest watch (cross 통과 후 RetestWindow 내) ───
			if (crossBarIdx > 0 && crossAdxPass && !entryArmed)
			{
				int barsSinceCross = CurrentBar - crossBarIdx;

				// Window timeout
				if (barsSinceCross > RetestWindow)
				{
					crossBarIdx = -1;
					crossAdxPass = false;
				}
				else if (barsSinceCross > 0)
				{
					// Retest detection: low touches EMA20
					if (Low[0] <= emaFast[0])
						retestSeen = true;

					// Reclaim: after retest, close > EMA20 → entry armed
					if (retestSeen && Close[0] > emaFast[0])
					{
						entryArmed = true;
						activeEntryBar = CurrentBar;
						activeEntryPx = Close[0];
						activeSlPx = activeEntryPx - SlAtrMult * crossAtr;
						activeTp1Px = activeEntryPx + Tp1AtrMult * crossAtr;

						FireEntryArmed();
					}
				}
			}

			// ─── 3. Draw / update active levels ───
			if (entryArmed && ShowLevels && activeEntryBar > 0)
			{
				int barsSinceEntry = CurrentBar - activeEntryBar;

				// Auto-clear after time-stop (TimeStopHours / 4h = N bars)
				int periodMin = (BarsPeriod.BarsPeriodType == BarsPeriodType.Minute) ? BarsPeriod.Value : 240;
				int timeStopBars = (TimeStopHours * 60) / Math.Max(1, periodMin);

				if (barsSinceEntry > timeStopBars + 5)
				{
					// Clear
					RemoveDrawObject("R8_E_" + activeEntryBar);
					RemoveDrawObject("R8_SL_" + activeEntryBar);
					RemoveDrawObject("R8_TP1_" + activeEntryBar);
					entryArmed = false;
					activeEntryBar = -1;
				}
				else
				{
					// Entry / SL / TP1 horizontal lines (simple signature — dash style 생략)
					Draw.HorizontalLine(this, "R8_E_" + activeEntryBar, activeEntryPx, Brushes.DodgerBlue);
					Draw.HorizontalLine(this, "R8_SL_" + activeEntryBar, activeSlPx, Brushes.OrangeRed);
					Draw.HorizontalLine(this, "R8_TP1_" + activeEntryBar, activeTp1Px, Brushes.Lime);
				}
			}
		}

		private void FireEntryArmed()
		{
			if (ShowMarkers)
			{
				Draw.Text(this, "R8_ENT_" + CurrentBar,
					"R8 ★\n" + string.Format("E {0:F2}\nSL {1:F2}\nTP1 {2:F2}",
						activeEntryPx, activeSlPx, activeTp1Px),
					0, High[0] + atr14[0] * 1.0, Brushes.DodgerBlue);
			}

			if (AlertOnEntry)
				Alert("AAL_R8_E_" + CurrentBar, Priority.High,
					string.Format("⭐ R8 ENTRY ARMED — E {0:F2}, SL {1:F2}, TP1 {2:F2}",
						activeEntryPx, activeSlPx, activeTp1Px),
					NinjaTrader.Core.Globals.InstallDir + @"\sounds\Alert1.wav",
					10, Brushes.White, Brushes.DodgerBlue);
		}
	}
}

// =============================================================================
// 운영 노트:
//
// 매매 절차 (수동 운영):
//   1. ⭐ R8 ★ 신호 발생 → entry/SL/TP1 라인 시각화
//   2. 다음 bar OPEN 에 시장가 LONG 진입 (entry_px 와 미세 차이 가능)
//   3. Broker 에 SL stop + TP1 limit (50% qty) 자동 attach
//   4. TP1 hit 시 SL → BE move (수동 또는 ATM template)
//   5. 남은 50% 는 BE 또는 trail. TimeStopHours 도달 시 reduce_only close
//
// 자동매매 연동 (Strategy):
//   별도 AAL_R8_Strategy.cs 작성 시 본 indicator 의 entryArmed 시그널을
//   addOnExtension 패턴으로 호출 또는 직접 룰 재작성
//
// AAL_HoldTimer 와 연동:
//   - HoldTimer.CapHours = TimeStopHours (예: 120)
//   - HoldTimer.AccountFilter = 운영 계정 명
//   → Time-stop 도달 시 큰 빨간 BG + alert
//
// AAL_SignalLight 와 연동:
//   - PRESET mode → R8 entry 시점 GOLDEN_X zone 우선
//   - Thursday 는 SignalLight 의 _THU 표시 (StE skip 동기화)
//   - R8 자체는 요일 무관 (HYP-MAX-005 에서 weekday breakdown 작음)
//
// TF 권고:
//   ✅ 4h: BTC PF 3.08 / NQ PF 1.96 — production
//   ⚠ 1h: BTC marginal (PF 1.26) / NQ NOGO. 4h 보조용으로만
//   ❌ 15m: 두 자산 NOGO. R8 메커니즘 부적합 (다른 룰 필요)
//
// 빈도:
//   4h BTC: 5.3/year   (filter 통과 16/3y)
//   4h NQ:  2.7/year   (filter 통과 46/17.3y)
//   합산:   ~8/year (multi-asset 운영 시)
// =============================================================================

#region NinjaScript generated code. Neither change nor remove.

namespace NinjaTrader.NinjaScript.Indicators
{
	public partial class Indicator : NinjaTrader.Gui.NinjaScript.IndicatorRenderBase
	{
		private AAL_R8_Signal[] cacheAAL_R8_Signal;
		public AAL_R8_Signal AAL_R8_Signal(int emaFastPeriod, int emaSlowPeriod, int adxThreshold, int retestWindow, double slAtrMult, double tp1AtrMult, int timeStopHours, bool showLevels, bool showMarkers, bool alertOnEntry, bool alertOnCross)
		{
			return AAL_R8_Signal(Input, emaFastPeriod, emaSlowPeriod, adxThreshold, retestWindow, slAtrMult, tp1AtrMult, timeStopHours, showLevels, showMarkers, alertOnEntry, alertOnCross);
		}

		public AAL_R8_Signal AAL_R8_Signal(ISeries<double> input, int emaFastPeriod, int emaSlowPeriod, int adxThreshold, int retestWindow, double slAtrMult, double tp1AtrMult, int timeStopHours, bool showLevels, bool showMarkers, bool alertOnEntry, bool alertOnCross)
		{
			if (cacheAAL_R8_Signal != null)
				for (int idx = 0; idx < cacheAAL_R8_Signal.Length; idx++)
					if (cacheAAL_R8_Signal[idx] != null && cacheAAL_R8_Signal[idx].EmaFastPeriod == emaFastPeriod && cacheAAL_R8_Signal[idx].EmaSlowPeriod == emaSlowPeriod && cacheAAL_R8_Signal[idx].AdxThreshold == adxThreshold && cacheAAL_R8_Signal[idx].RetestWindow == retestWindow && cacheAAL_R8_Signal[idx].SlAtrMult == slAtrMult && cacheAAL_R8_Signal[idx].Tp1AtrMult == tp1AtrMult && cacheAAL_R8_Signal[idx].TimeStopHours == timeStopHours && cacheAAL_R8_Signal[idx].ShowLevels == showLevels && cacheAAL_R8_Signal[idx].ShowMarkers == showMarkers && cacheAAL_R8_Signal[idx].AlertOnEntry == alertOnEntry && cacheAAL_R8_Signal[idx].AlertOnCross == alertOnCross && cacheAAL_R8_Signal[idx].EqualsInput(input))
						return cacheAAL_R8_Signal[idx];
			return CacheIndicator<AAL_R8_Signal>(new AAL_R8_Signal(){ EmaFastPeriod = emaFastPeriod, EmaSlowPeriod = emaSlowPeriod, AdxThreshold = adxThreshold, RetestWindow = retestWindow, SlAtrMult = slAtrMult, Tp1AtrMult = tp1AtrMult, TimeStopHours = timeStopHours, ShowLevels = showLevels, ShowMarkers = showMarkers, AlertOnEntry = alertOnEntry, AlertOnCross = alertOnCross }, input, ref cacheAAL_R8_Signal);
		}
	}
}

namespace NinjaTrader.NinjaScript.MarketAnalyzerColumns
{
	public partial class MarketAnalyzerColumn : MarketAnalyzerColumnBase
	{
		public Indicators.AAL_R8_Signal AAL_R8_Signal(int emaFastPeriod, int emaSlowPeriod, int adxThreshold, int retestWindow, double slAtrMult, double tp1AtrMult, int timeStopHours, bool showLevels, bool showMarkers, bool alertOnEntry, bool alertOnCross)
		{
			return indicator.AAL_R8_Signal(Input, emaFastPeriod, emaSlowPeriod, adxThreshold, retestWindow, slAtrMult, tp1AtrMult, timeStopHours, showLevels, showMarkers, alertOnEntry, alertOnCross);
		}

		public Indicators.AAL_R8_Signal AAL_R8_Signal(ISeries<double> input , int emaFastPeriod, int emaSlowPeriod, int adxThreshold, int retestWindow, double slAtrMult, double tp1AtrMult, int timeStopHours, bool showLevels, bool showMarkers, bool alertOnEntry, bool alertOnCross)
		{
			return indicator.AAL_R8_Signal(input, emaFastPeriod, emaSlowPeriod, adxThreshold, retestWindow, slAtrMult, tp1AtrMult, timeStopHours, showLevels, showMarkers, alertOnEntry, alertOnCross);
		}
	}
}

namespace NinjaTrader.NinjaScript.Strategies
{
	public partial class Strategy : NinjaTrader.Gui.NinjaScript.StrategyRenderBase
	{
		public Indicators.AAL_R8_Signal AAL_R8_Signal(int emaFastPeriod, int emaSlowPeriod, int adxThreshold, int retestWindow, double slAtrMult, double tp1AtrMult, int timeStopHours, bool showLevels, bool showMarkers, bool alertOnEntry, bool alertOnCross)
		{
			return indicator.AAL_R8_Signal(Input, emaFastPeriod, emaSlowPeriod, adxThreshold, retestWindow, slAtrMult, tp1AtrMult, timeStopHours, showLevels, showMarkers, alertOnEntry, alertOnCross);
		}

		public Indicators.AAL_R8_Signal AAL_R8_Signal(ISeries<double> input , int emaFastPeriod, int emaSlowPeriod, int adxThreshold, int retestWindow, double slAtrMult, double tp1AtrMult, int timeStopHours, bool showLevels, bool showMarkers, bool alertOnEntry, bool alertOnCross)
		{
			return indicator.AAL_R8_Signal(input, emaFastPeriod, emaSlowPeriod, adxThreshold, retestWindow, slAtrMult, tp1AtrMult, timeStopHours, showLevels, showMarkers, alertOnEntry, alertOnCross);
		}
	}
}

#endregion
