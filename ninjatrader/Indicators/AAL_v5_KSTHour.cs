// =============================================================================
// AAL_v5_KSTHour — KST Hour Bias + Day of Week + 04:30 Squeeze Guard (NT8) v1.0
// =============================================================================
// Source: Phase D1 (KST hour) + D5 (Day of Week) + D6 (Squeeze GUARD) + Phase E
//
//   Verified KST hour signed return forward 24b (NQ 5m, 10y h2y / last_2y):
//
//     KST 04 LONG (BURN_X 시간):  +0.21 / -0.06 ATR   — v3.5 핵심 edge
//     KST 14 LONG (US lunch):     +0.06 / +0.06       — P3 PF 1.14 trade-able ⭐
//     KST 19 LONG (pre-NY):       +0.30 / +0.62 ⭐⭐⭐  — NEW best (last_2y)
//     KST 15 LONG (EU close):     +0.21 / -0.08
//
//     KST 20-22 SHORT cluster:    raw signed -0.15 ~ -0.45 ATR
//                                 ⚠ trade sim PF 0.84-1.01 = 단독 trade LOSE!
//                                 Confluence (Tue / bear_strong) 필수
//
//   Day of Week (h2y 48b):
//     Monday LONG:    +0.63 ATR ⭐ Phase E PF 1.05
//     Tuesday SHORT:  -0.27 ATR ⚠ 단독 PF 0.94 (confluence only)
//
//   04:30 BURN_X Guard (D6 verified):
//     KST 04:30 + ATR z 12-bar max < -0.5 (squeeze)
//       → forward 24b signed -3.54 ATR (Cohen d=-0.85 LARGE)
//     Action: SKIP entry (또는 reverse SHORT, careful — N=80 small)
//
//   Confluences (Phase E P3 PF cost-adjusted):
//     CONF_KST14_MON LONG:  P3 PF 1.22 ⭐⭐ best
//     CONF_KST19_MON LONG:  P3 PF 1.09 ⭐
//     CONF_KST21_TUE SHORT: P3 PF 1.04 (recent)
//
// Visual:
//   ⚡ 04:30 (clean, no squeeze): 큰 lime ▲ + ATM v2 라벨
//   🚨 04:30 + squeeze: red xcross + "SKIP"
//   ⭐ KST 19 LONG: aqua ▲ + "19" (Mon 결합 시 🔥 CONF flag)
//   KST 14 LONG: aqua ▲ + "14"
//   KST 15 LONG: aqua ▲ + "15" (smaller)
//   ⚠ KST 20-22: orange diamond (단독 trade X warning)
//
// ATM 권장:
//   04:30 BURN_X (no squeeze): SL 30 / Pre-Trail 18 / Trail 18 (HE-001 v2)
//   KST 19/14 + Mon LONG:      SL 60 / Pre-Trail 40 / Trail 30 (loose hold)
//   KST 21 + bear_strong:      SHORT only with strong confluence
//
// 의존: AAL_Shared.cs (standalone)
// 생성: 2026-05-07 (NT_AAL v5)
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
	public class AAL_v5_KSTHour : Indicator
	{
		#region Parameters
		[NinjaScriptProperty]
		[Display(Name = "Show KST 04:30 BURN_X (with squeeze GUARD)", Order = 1, GroupName = "1. KST Hours")]
		public bool ShowKst04 { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Show KST 14 LONG (US lunch)", Order = 2, GroupName = "1. KST Hours")]
		public bool ShowKst14 { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Show KST 19 LONG ⭐ (NEW best last_2y +0.62 ATR)", Order = 3, GroupName = "1. KST Hours")]
		public bool ShowKst19 { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Show KST 15 LONG (EU close)", Order = 4, GroupName = "1. KST Hours")]
		public bool ShowKst15 { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Show KST 20-22 SHORT solo warning", Order = 5, GroupName = "1. KST Hours")]
		public bool ShowKst2022Warn { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Show Mon LONG / Tue SHORT day filter (HUD)", Order = 6, GroupName = "2. Day of Week")]
		public bool ShowDayOfWeek { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Show 🔥 Confluence flag (KST + Mon)", Order = 7, GroupName = "2. Day of Week")]
		public bool ShowConfluence { get; set; }

		[NinjaScriptProperty]
		[Range(5, 30)]
		[Display(Name = "Squeeze lookback (bars)", Order = 8, GroupName = "3. Squeeze Guard")]
		[Description("ATR z rolling max within this window. 12 = D6 verified.")]
		public int SqueezeWindow { get; set; }

		[NinjaScriptProperty]
		[Range(-2.0, 0.0)]
		[Display(Name = "Squeeze z threshold", Order = 9, GroupName = "3. Squeeze Guard")]
		[Description("ATR z 12-bar max < this value → squeeze active. -0.5 = D6 verified.")]
		public double SqueezeZ { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Show ATM v2 ticks label (HE-001)", Order = 10, GroupName = "4. Display")]
		public bool ShowAtmTicks { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Alert on KST 04:30 (clean)", Order = 11, GroupName = "5. Alerts")]
		public bool AlertOnBurnX { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Alert on 04:30 SQUEEZE GUARD (SKIP)", Order = 12, GroupName = "5. Alerts")]
		public bool AlertOnSqueezeSkip { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Alert on KST 19 ⭐ (high priority)", Order = 13, GroupName = "5. Alerts")]
		public bool AlertOnKst19 { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Alert on KST 14", Order = 14, GroupName = "5. Alerts")]
		public bool AlertOnKst14 { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Alert on Confluence (KST + Mon)", Order = 15, GroupName = "5. Alerts")]
		public bool AlertOnConfluence { get; set; }
		#endregion

		#region Indicators
		private ATR atr14;
		private SMA atrMean60d;
		private StdDev atrStd60d;
		#endregion

		protected override void OnStateChange()
		{
			if (State == State.SetDefaults)
			{
				Description = "AAL v5 — KST hour bias (D1) + DOW (D5) + 04:30 Squeeze GUARD (D6)";
				Name = "AAL_v5_KSTHour";
				Calculate = Calculate.OnBarClose;
				IsOverlay = true;
				DisplayInDataBox = false;
				DrawOnPricePanel = true;
				PaintPriceMarkers = false;

				ShowKst04 = true;
				ShowKst14 = true;
				ShowKst19 = true;
				ShowKst15 = false;     // 보조, default OFF
				ShowKst2022Warn = true;
				ShowDayOfWeek = true;
				ShowConfluence = true;
				SqueezeWindow = 12;
				SqueezeZ = -0.5;
				ShowAtmTicks = true;
				AlertOnBurnX = true;
				AlertOnSqueezeSkip = true;
				AlertOnKst19 = true;
				AlertOnKst14 = false;
				AlertOnConfluence = true;
			}
			else if (State == State.DataLoaded)
			{
				if (BarsPeriod.BarsPeriodType != BarsPeriodType.Minute || BarsPeriod.Value != 5)
				{
					Print(string.Format(
						"⚠ AAL_v5_KSTHour: 5m TF 전제 (D1/D5/D6 검증). 현재 차트 TF = {0} {1}.",
						BarsPeriod.BarsPeriodType, BarsPeriod.Value));
				}
				atr14 = ATR(14);
				// ATR z 60-day rolling (5m × 60d × 24h × 12 bars/h = 17,280)
				atrMean60d = SMA(atr14, 17280);
				atrStd60d  = StdDev(atr14, 17280);
			}
		}

		protected override void OnBarUpdate()
		{
			if (CurrentBar < 1500) return;    // ATR z warmup (충분 sample 후)

			// === KST hour ===
			DateTime kst = Time[0].ToUniversalTime().AddHours(9);
			int kstH = kst.Hour;
			int kstM = kst.Minute;
			DayOfWeek dow = kst.DayOfWeek;
			bool isMon = dow == DayOfWeek.Monday;
			bool isTue = dow == DayOfWeek.Tuesday;

			// === ATR z (60-day rolling) ===
			double atrZ = atrStd60d[0] > 0.0001
				? (atr14[0] - atrMean60d[0]) / atrStd60d[0]
				: 0.0;

			// Squeeze active = ATR z 12-bar max < threshold
			double zMax = atrZ;
			for (int i = 1; i < SqueezeWindow; i++)
			{
				double zi = atrStd60d[i] > 0.0001
					? (atr14[i] - atrMean60d[i]) / atrStd60d[i]
					: 0.0;
				if (zi > zMax) zMax = zi;
			}
			bool squeezeActive = zMax < SqueezeZ;

			// === ATM v2 ticks (HE-001) ===
			int slV2 = (int)Math.Round(0.5 * atr14[0] * 4.0);   // ~30 ticks
			int trailV2 = (int)Math.Round(0.3 * atr14[0] * 4.0); // ~18 ticks
			string atmStr = string.Format("ATM v2: SL {0} / PT {1} / TD {1} ticks", slV2, trailV2);

			// =========================================================
			// ⚡ KST 04:30 BURN_X (clean, no squeeze)
			// =========================================================
			bool isKst0430 = kstH == 4 && kstM == 30;

			if (ShowKst04 && isKst0430 && !squeezeActive)
			{
				Draw.ArrowUp(this, "BurnX_" + CurrentBar, true, 0,
					Low[0] - atr14[0] * 0.5, Brushes.Lime);
				string label04 = "⚡ 04:30 BURN_X\n(no squeeze, clean)";
				if (ShowAtmTicks) label04 += "\n" + atmStr;
				if (ShowConfluence && isMon) label04 = "🔥 04:30+Mon CONF\n" + label04;
				Draw.Text(this, "BurnXtxt_" + CurrentBar, label04,
					0, Low[0] - atr14[0] * 1.5, Brushes.Lime);

				if (AlertOnBurnX)
					Alert("AAL_v5_BurnX_clean", Priority.High,
						string.Format("⚡ 04:30 BURN_X clean (no squeeze){0}. {1}",
							isMon ? " + Mon CONF 🔥" : "", atmStr),
						NinjaTrader.Core.Globals.InstallDir + @"\sounds\Alert1.wav",
						15, Brushes.Black, Brushes.Lime);
			}
			else if (ShowKst04 && isKst0430 && squeezeActive)
			{
				// 🚨 GUARD: SKIP entry (D6 LARGE effect -3.54 ATR if forced)
				Draw.Text(this, "BurnXSkip_" + CurrentBar,
					"🚨 04:30 SQUEEZE\nGUARD: SKIP\n(D6: -3.54 ATR if entered)",
					0, High[0] + atr14[0] * 1.0, Brushes.Red);

				if (AlertOnSqueezeSkip)
					Alert("AAL_v5_BurnX_SKIP", Priority.High,
						"🚨 04:30 SQUEEZE GUARD active — SKIP entry. (D6 verified: -3.54 ATR if forced LONG)",
						NinjaTrader.Core.Globals.InstallDir + @"\sounds\Alert4.wav",
						15, Brushes.White, Brushes.DarkRed);
			}

			// =========================================================
			// ⭐ KST 19 LONG (pre-NY, NEW best edge last_2y +0.62 ATR)
			// =========================================================
			bool isKst19 = kstH == 19 && kstM < 5;
			if (ShowKst19 && isKst19)
			{
				Draw.ArrowUp(this, "Kst19_" + CurrentBar, true, 0,
					Low[0] - atr14[0] * 0.4, Brushes.Aqua);
				string lab19 = "⭐ KST 19 LONG\n(last_2y +0.62 ATR)";
				if (ShowConfluence && isMon)
					lab19 = "🔥 KST19+Mon CONF\n(P3 PF 1.09)\n" + lab19;
				Draw.Text(this, "Kst19txt_" + CurrentBar, lab19,
					0, Low[0] - atr14[0] * 1.3, Brushes.Aqua);

				if (AlertOnKst19)
					Alert("AAL_v5_KST19", Priority.High,
						string.Format("⭐ KST 19 LONG (last_2y +0.62 ATR){0}",
							isMon ? " + Mon CONF 🔥 (P3 PF 1.09)" : ""),
						NinjaTrader.Core.Globals.InstallDir + @"\sounds\Alert1.wav",
						12, Brushes.Black, Brushes.Aqua);
			}

			// =========================================================
			// KST 14 LONG (US lunch, P3 PF 1.14 simple)
			// =========================================================
			bool isKst14 = kstH == 14 && kstM < 5;
			if (ShowKst14 && isKst14)
			{
				Draw.ArrowUp(this, "Kst14_" + CurrentBar, true, 0,
					Low[0] - atr14[0] * 0.4, Brushes.Cyan);
				string lab14 = "KST 14 LONG\n(US lunch)";
				if (ShowConfluence && isMon)
					lab14 = "🔥 KST14+Mon CONF\n(P3 PF 1.22 ⭐⭐ best)\n" + lab14;
				Draw.Text(this, "Kst14txt_" + CurrentBar, lab14,
					0, Low[0] - atr14[0] * 1.3, Brushes.Cyan);

				if (AlertOnKst14 || (AlertOnConfluence && isMon))
					Alert("AAL_v5_KST14", isMon ? Priority.High : Priority.Medium,
						string.Format("KST 14 LONG{0}",
							isMon ? " + Mon CONF 🔥 (P3 PF 1.22 ⭐⭐ best)" : ""),
						NinjaTrader.Core.Globals.InstallDir + @"\sounds\Alert2.wav",
						10, Brushes.Black, Brushes.Cyan);
			}

			// =========================================================
			// KST 15 LONG (EU close, optional)
			// =========================================================
			if (ShowKst15 && kstH == 15 && kstM < 5)
			{
				Draw.ArrowUp(this, "Kst15_" + CurrentBar, true, 0,
					Low[0] - atr14[0] * 0.3, Brushes.LightCyan);
				Draw.Text(this, "Kst15txt_" + CurrentBar, "KST 15 LONG (EU close)",
					0, Low[0] - atr14[0] * 0.9, Brushes.LightCyan);
			}

			// =========================================================
			// ⚠ KST 20-22 SHORT solo warning (단독 trade LOSE!)
			// =========================================================
			bool isKst2022 = (kstH >= 20 && kstH <= 22) && kstM < 5;
			if (ShowKst2022Warn && isKst2022)
			{
				Draw.Diamond(this, "Kst2022_" + CurrentBar, true, 0,
					High[0] + atr14[0] * 0.4, Brushes.Orange);
				string lab2022 = string.Format("⚠ KST {0} SHORT\n(단독 X — conf only)", kstH);
				if (kstH == 21 && isTue) lab2022 = "🔥 KST21+Tue SHORT\n(P3 PF 1.04, recent)\n" + lab2022;
				Draw.Text(this, "Kst2022txt_" + CurrentBar, lab2022,
					0, High[0] + atr14[0] * 1.0, Brushes.Orange);
			}

			// =========================================================
			// 📅 Day of Week label (always at session boundaries)
			// =========================================================
			if (ShowDayOfWeek && CurrentBar > 0
				&& (Time[0].Date != Time[1].Date))     // first bar of new day
			{
				string dowLabel = isMon ? "Mon LONG bias ⭐ (+0.63 ATR 48b)"
					: isTue ? "Tue SHORT (단독 X, conf only)"
					: dow == DayOfWeek.Thursday ? "Thu (L3 SKIP)"
					: dow.ToString();
				Brush dowColor = isMon ? Brushes.Lime
					: isTue ? Brushes.Orange
					: dow == DayOfWeek.Thursday ? Brushes.Purple
					: Brushes.Gray;
				Draw.Text(this, "DOW_" + CurrentBar, dowLabel,
					0, High[0] + atr14[0] * 2.5, dowColor);
			}
		}
	}
}

// =============================================================================
// 운영 권고:
//   1. KST 04:30 BURN_X: 알람 → squeeze 체크 → clean 시 ATM v2 진입
//   2. KST 19 + Mon: 우선 confluence 신호 (P3 PF 1.09)
//   3. KST 14 + Mon: 가장 robust confluence (P3 PF 1.22 ⭐⭐)
//   4. KST 20-22: 단독 SHORT 진입 X. Trail/v3.5 BURN_R ATM 결합 시만.
//   5. Day of Week label = session 시작 시 표시 (Mon/Tue/Thu)
//
// Phase E cost-adjusted P3 PF reference:
//   CONF_KST14_MON LONG:  1.22 ⭐⭐ best
//   CONF_KST19_MON LONG:  1.09 ⭐
//   KST14 single LONG:    1.14 (large N 846)
//   KST19 single LONG:    0.99 (single 단독은 약함)
//   MON_LONG (any):       1.08
//   04:30 BURN_X simple:  1.01 (Trail 필수 → 3.81 with v3.5 ATM)
//
// 의존: AAL_Shared.cs
// =============================================================================

#region NinjaScript generated code. Neither change nor remove.

namespace NinjaTrader.NinjaScript.Indicators
{
	public partial class Indicator : NinjaTrader.Gui.NinjaScript.IndicatorRenderBase
	{
		private AAL_v5_KSTHour[] cacheAAL_v5_KSTHour;
		public AAL_v5_KSTHour AAL_v5_KSTHour(bool showKst04, bool showKst14, bool showKst19, bool showKst15, bool showKst2022Warn, bool showDayOfWeek, bool showConfluence, int squeezeWindow, double squeezeZ, bool showAtmTicks, bool alertOnBurnX, bool alertOnSqueezeSkip, bool alertOnKst19, bool alertOnKst14, bool alertOnConfluence)
		{
			return AAL_v5_KSTHour(Input, showKst04, showKst14, showKst19, showKst15, showKst2022Warn, showDayOfWeek, showConfluence, squeezeWindow, squeezeZ, showAtmTicks, alertOnBurnX, alertOnSqueezeSkip, alertOnKst19, alertOnKst14, alertOnConfluence);
		}

		public AAL_v5_KSTHour AAL_v5_KSTHour(ISeries<double> input, bool showKst04, bool showKst14, bool showKst19, bool showKst15, bool showKst2022Warn, bool showDayOfWeek, bool showConfluence, int squeezeWindow, double squeezeZ, bool showAtmTicks, bool alertOnBurnX, bool alertOnSqueezeSkip, bool alertOnKst19, bool alertOnKst14, bool alertOnConfluence)
		{
			if (cacheAAL_v5_KSTHour != null)
				for (int idx = 0; idx < cacheAAL_v5_KSTHour.Length; idx++)
					if (cacheAAL_v5_KSTHour[idx] != null && cacheAAL_v5_KSTHour[idx].ShowKst04 == showKst04 && cacheAAL_v5_KSTHour[idx].ShowKst14 == showKst14 && cacheAAL_v5_KSTHour[idx].ShowKst19 == showKst19 && cacheAAL_v5_KSTHour[idx].ShowKst15 == showKst15 && cacheAAL_v5_KSTHour[idx].ShowKst2022Warn == showKst2022Warn && cacheAAL_v5_KSTHour[idx].ShowDayOfWeek == showDayOfWeek && cacheAAL_v5_KSTHour[idx].ShowConfluence == showConfluence && cacheAAL_v5_KSTHour[idx].SqueezeWindow == squeezeWindow && cacheAAL_v5_KSTHour[idx].SqueezeZ == squeezeZ && cacheAAL_v5_KSTHour[idx].ShowAtmTicks == showAtmTicks && cacheAAL_v5_KSTHour[idx].AlertOnBurnX == alertOnBurnX && cacheAAL_v5_KSTHour[idx].AlertOnSqueezeSkip == alertOnSqueezeSkip && cacheAAL_v5_KSTHour[idx].AlertOnKst19 == alertOnKst19 && cacheAAL_v5_KSTHour[idx].AlertOnKst14 == alertOnKst14 && cacheAAL_v5_KSTHour[idx].AlertOnConfluence == alertOnConfluence && cacheAAL_v5_KSTHour[idx].EqualsInput(input))
						return cacheAAL_v5_KSTHour[idx];
			return CacheIndicator<AAL_v5_KSTHour>(new AAL_v5_KSTHour(){ ShowKst04 = showKst04, ShowKst14 = showKst14, ShowKst19 = showKst19, ShowKst15 = showKst15, ShowKst2022Warn = showKst2022Warn, ShowDayOfWeek = showDayOfWeek, ShowConfluence = showConfluence, SqueezeWindow = squeezeWindow, SqueezeZ = squeezeZ, ShowAtmTicks = showAtmTicks, AlertOnBurnX = alertOnBurnX, AlertOnSqueezeSkip = alertOnSqueezeSkip, AlertOnKst19 = alertOnKst19, AlertOnKst14 = alertOnKst14, AlertOnConfluence = alertOnConfluence }, input, ref cacheAAL_v5_KSTHour);
		}
	}
}

namespace NinjaTrader.NinjaScript.MarketAnalyzerColumns
{
	public partial class MarketAnalyzerColumn : MarketAnalyzerColumnBase
	{
		public Indicators.AAL_v5_KSTHour AAL_v5_KSTHour(bool showKst04, bool showKst14, bool showKst19, bool showKst15, bool showKst2022Warn, bool showDayOfWeek, bool showConfluence, int squeezeWindow, double squeezeZ, bool showAtmTicks, bool alertOnBurnX, bool alertOnSqueezeSkip, bool alertOnKst19, bool alertOnKst14, bool alertOnConfluence)
		{
			return indicator.AAL_v5_KSTHour(Input, showKst04, showKst14, showKst19, showKst15, showKst2022Warn, showDayOfWeek, showConfluence, squeezeWindow, squeezeZ, showAtmTicks, alertOnBurnX, alertOnSqueezeSkip, alertOnKst19, alertOnKst14, alertOnConfluence);
		}

		public Indicators.AAL_v5_KSTHour AAL_v5_KSTHour(ISeries<double> input, bool showKst04, bool showKst14, bool showKst19, bool showKst15, bool showKst2022Warn, bool showDayOfWeek, bool showConfluence, int squeezeWindow, double squeezeZ, bool showAtmTicks, bool alertOnBurnX, bool alertOnSqueezeSkip, bool alertOnKst19, bool alertOnKst14, bool alertOnConfluence)
		{
			return indicator.AAL_v5_KSTHour(input, showKst04, showKst14, showKst19, showKst15, showKst2022Warn, showDayOfWeek, showConfluence, squeezeWindow, squeezeZ, showAtmTicks, alertOnBurnX, alertOnSqueezeSkip, alertOnKst19, alertOnKst14, alertOnConfluence);
		}
	}
}

namespace NinjaTrader.NinjaScript.Strategies
{
	public partial class Strategy : NinjaTrader.Gui.NinjaScript.StrategyRenderBase
	{
		public Indicators.AAL_v5_KSTHour AAL_v5_KSTHour(bool showKst04, bool showKst14, bool showKst19, bool showKst15, bool showKst2022Warn, bool showDayOfWeek, bool showConfluence, int squeezeWindow, double squeezeZ, bool showAtmTicks, bool alertOnBurnX, bool alertOnSqueezeSkip, bool alertOnKst19, bool alertOnKst14, bool alertOnConfluence)
		{
			return indicator.AAL_v5_KSTHour(Input, showKst04, showKst14, showKst19, showKst15, showKst2022Warn, showDayOfWeek, showConfluence, squeezeWindow, squeezeZ, showAtmTicks, alertOnBurnX, alertOnSqueezeSkip, alertOnKst19, alertOnKst14, alertOnConfluence);
		}

		public Indicators.AAL_v5_KSTHour AAL_v5_KSTHour(ISeries<double> input, bool showKst04, bool showKst14, bool showKst19, bool showKst15, bool showKst2022Warn, bool showDayOfWeek, bool showConfluence, int squeezeWindow, double squeezeZ, bool showAtmTicks, bool alertOnBurnX, bool alertOnSqueezeSkip, bool alertOnKst19, bool alertOnKst14, bool alertOnConfluence)
		{
			return indicator.AAL_v5_KSTHour(input, showKst04, showKst14, showKst19, showKst15, showKst2022Warn, showDayOfWeek, showConfluence, squeezeWindow, squeezeZ, showAtmTicks, alertOnBurnX, alertOnSqueezeSkip, alertOnKst19, alertOnKst14, alertOnConfluence);
		}
	}
}

#endregion
