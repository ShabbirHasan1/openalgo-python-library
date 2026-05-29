# -*- coding: utf-8 -*-
"""
TA-Lib vs OpenAlgo: VALUE comparison (not speed) + coverage gap.

Part A: for every indicator where both libraries have an equivalent, compute both on
real RELIANCE daily data and report max abs/rel difference over the common non-NaN
region, with a verdict (MATCH within 1e-6, or DIFFERS with the documented reason).
Part B: list TA-Lib functions that OpenAlgo does NOT yet have (coverage gap), grouped.

Writes benchmark/TALIB_COMPARISON.md.
"""
import os
os.environ.setdefault("NUMBA_DISABLE_JIT", "1")
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd
import talib
from openalgo import ta

DATA = Path(__file__).resolve().parent / "data"
MATCH_TOL = 1e-6


def _arr(x):
    if isinstance(x, tuple):
        x = x[0]
    return np.asarray(getattr(x, "values", x), dtype=np.float64)


def compare(tl, oa):
    """max abs/rel diff over common non-NaN tail region."""
    a, b = _arr(tl), _arr(oa)
    n = min(len(a), len(b))
    a, b = a[-n:], b[-n:]
    m = ~(np.isnan(a) | np.isnan(b))
    if not m.any():
        return float("nan"), float("nan"), 0
    da = np.abs(a[m] - b[m])
    rel = da / np.maximum(np.abs(a[m]), 1e-12)
    return float(da.max()), float(rel.max()), int(m.sum())


def main():
    df = pd.read_csv(DATA / "RELIANCE_D.csv", index_col=0)
    o = df["open"].to_numpy(np.float64)
    h = df["high"].to_numpy(np.float64)
    l = df["low"].to_numpy(np.float64)
    c = df["close"].to_numpy(np.float64)
    v = df["volume"].to_numpy(np.float64)

    # (talib name, talib value, openalgo value, expected-reason if known-different)
    cases = [
        ("SMA", talib.SMA(c, 20), ta.sma(c, 20), "identical definition"),
        ("EMA", talib.EMA(c, 20), ta.ema(c, 20), "seed: TA-Lib=SMA seed, OpenAlgo=first-value (TradingView)"),
        ("WMA", talib.WMA(c, 20), ta.wma(c, 20), "identical definition"),
        ("DEMA", talib.DEMA(c, 20), ta.dema(c, 20), "EMA seed convention (TradingView)"),
        ("TEMA", talib.TEMA(c, 20), ta.tema(c, 20), "EMA seed convention (TradingView)"),
        ("TRIMA", talib.TRIMA(c, 20), ta.trima(c, 20), "identical definition"),
        ("KAMA", talib.KAMA(c, 30), ta.kama(c, 30), "TA-Lib fixed 10/2/30 vs OpenAlgo TradingView ER(length)"),
        ("T3", talib.T3(c, 5), ta.t3(c, 5), "EMA seed / vfactor convention"),
        ("SAR", talib.SAR(h, l), ta.psar(h, l), "init/AF edge-rules differ slightly"),
        ("BBANDS.mid", talib.BBANDS(c, 20)[1], ta.bbands(c, 20)[1], "identical (SMA + population stdev)"),
        ("BBANDS.up", talib.BBANDS(c, 20)[0], ta.bbands(c, 20)[0], "identical"),
        ("RSI", talib.RSI(c, 14), ta.rsi(c, 14), "identical (Wilder)"),
        ("CCI", talib.CCI(h, l, c, 20), ta.cci(h, l, c, 20), "identical definition"),
        ("WILLR", talib.WILLR(h, l, c, 14), ta.williams_r(h, l, c, 14), "identical definition"),
        ("BOP", talib.BOP(o, h, l, c), ta.bop(o, h, l, c), "identical definition"),
        ("CMO", talib.CMO(c, 14), ta.cmo(c, 14), "TA-Lib Wilder-smoothed vs OpenAlgo simple sums"),
        ("ROC", talib.ROC(c, 12), ta.roc(c, 12), "identical ((p/prev-1)*100)"),
        ("MOM", talib.MOM(c, 12), ta.change(c, 12), "Momentum = change(n); identical"),
        ("MACD.line", talib.MACD(c)[0], ta.macd(c)[0], "EMA seed convention (TradingView)"),
        ("PPO", talib.PPO(c), ta.ppo(c)[0], "EMA seed convention"),
        ("TRIX", talib.TRIX(c, 18), ta.trix(c, 18), "TA-Lib ROC of EMA(price); OpenAlgo uses log-price*10000 (TradingView)"),
        ("ATR", talib.ATR(h, l, c, 14), ta.atr(h, l, c, 14), "Wilder seed index differs (TA-Lib seeds at period)"),
        ("NATR", talib.NATR(h, l, c, 14), ta.natr(h, l, c, 14), "follows ATR seed"),
        ("TRANGE", talib.TRANGE(h, l, c), ta.true_range(h, l, c), "identical from index 1"),
        ("ULTOSC", talib.ULTOSC(h, l, c), ta.ultimate_oscillator(h, l, c), "identical definition"),
        ("AROON.up", talib.AROON(h, l, 14)[1], ta.aroon(h, l, 14)[0], "lookback length+1 (TradingView) vs length (TA-Lib); matches except boundary bars"),
        ("AROONOSC", talib.AROONOSC(h, l, 14), ta.aroon_oscillator(h, l, 14), "lookback length+1 (TradingView) vs length (TA-Lib)"),
        ("ADX", talib.ADX(h, l, c, 14), ta.adx(h, l, c, 14)[2], "Wilder DI/DX; seed/warmup index differs"),
        ("PLUS_DI", talib.PLUS_DI(h, l, c, 14), ta.dmi(h, l, c, 14)[0], "Wilder; seed/warmup differs"),
        ("STOCH.k", talib.STOCH(h, l, c)[0], ta.stochastic(h, l, c)[0], "TA-Lib default slowing differs from OpenAlgo k/smooth/d"),
        ("CORREL", talib.CORREL(c, o, 20), ta.correlation(c, o, 20), "identical (Pearson)"),
        ("LINEARREG", talib.LINEARREG(c, 14), ta.linreg(c, 14), "identical endpoint"),
        ("LINEARREG_SLOPE", talib.LINEARREG_SLOPE(c, 14), ta.lrslope(c, 14), "TA-Lib OLS slope vs OpenAlgo TradingView (delta of endpoints)"),
        ("TSF", talib.TSF(c, 14), ta.tsf(c, 14), "identical forecast"),
        ("STDDEV", talib.STDDEV(c, 20), ta.stdev(c, 20), "identical (population)"),
        ("VAR", talib.VAR(c, 20), ta.variance(c, 20), "TA-Lib population /n vs OpenAlgo sample /(n-1)"),
        ("OBV", talib.OBV(c, v), ta.obv(c, v), "QUIRK: OpenAlgo treats close==prev as UP (+vol); TA-Lib AND TradingView treat flat as 0 -> increments differ on flat bars"),
        ("AD", talib.AD(h, l, c, v), ta.adl(h, l, c, v), "baseline offset only: OpenAlgo seeds 0, TA-Lib includes bar-0 MFV (increments identical, ~1e-6)"),
        ("ADOSC", talib.ADOSC(h, l, c, v), ta.cho(h, l, c, v), "EMA seed convention"),
    ]

    rows = []
    nmatch = ndiff = 0
    for name, tl, oa, reason in cases:
        mad, mrd, npts = compare(tl, oa)
        verdict = "MATCH" if (mad == mad and mad <= MATCH_TOL) else "DIFFERS"
        if verdict == "MATCH":
            nmatch += 1
        else:
            ndiff += 1
        rows.append((name, verdict, mad, mrd, reason if verdict == "DIFFERS" else "-"))

    lines = ["# TA-Lib vs OpenAlgo - Value Comparison", ""]
    lines.append(f"Data: RELIANCE daily ({len(c)} bars). MATCH if max abs diff <= {MATCH_TOL:g}.")
    lines.append(f"Result: {nmatch} MATCH, {ndiff} DIFFER.")
    lines.append("")
    lines.append("Classification of the DIFFER cases:")
    lines.append("- CONVENTION (intentional, OpenAlgo follows TradingView/Pine; changing would break "
                 "the byte-identical guarantee for existing users): EMA/DEMA/TEMA/T3/MACD/PPO (EMA "
                 "first-value seed vs TA-Lib SMA seed), ATR/NATR/ADX/PLUS_DI (Wilder seed/warmup "
                 "index), KAMA (ER window), TRIX (log-price), CMO (simple sums vs Wilder), VAR "
                 "(sample /(n-1) vs population /n), LINEARREG_SLOPE (endpoint-delta vs OLS slope), "
                 "STOCH (default smoothing params), AROON/AROONOSC (length+1 lookback), SAR (init/AF "
                 "edge rules), AD (cumulative baseline = constant offset, increments identical).")
    lines.append("- GENUINE QUIRK (matches NEITHER TA-Lib nor TradingView): OBV treats a flat close "
                 "(close==prev) as up-volume; both TA-Lib and TradingView treat it as no-change. "
                 "This is the only case worth an actual fix (it is pre-existing OpenAlgo behavior).")
    lines.append("")
    lines.append("| Indicator (TA-Lib) | Verdict | max abs diff | max rel diff | Reason if differs |")
    lines.append("|--------------------|---------|-------------:|-------------:|-------------------|")
    for name, verdict, mad, mrd, reason in rows:
        lines.append(f"| {name} | {verdict} | {mad:.3e} | {mrd:.3e} | {reason} |")

    # ---- Part B: coverage gap ----
    groups = talib.get_function_groups()
    # TA-Lib funcs that OpenAlgo HAS an equivalent for:
    covered = {
        "SMA", "EMA", "WMA", "DEMA", "TEMA", "TRIMA", "KAMA", "T3", "MA", "BBANDS", "SAR",
        "RSI", "CCI", "WILLR", "BOP", "CMO", "ROC", "MOM", "MACD", "PPO", "TRIX", "AROON",
        "AROONOSC", "ADX", "PLUS_DI", "MINUS_DI", "STOCH", "STOCHRSI", "MFI", "ULTOSC", "APO",
        "ATR", "NATR", "TRANGE", "CORREL", "BETA", "LINEARREG", "LINEARREG_SLOPE", "TSF",
        "STDDEV", "VAR", "OBV", "AD", "ADOSC", "MIDPRICE", "MAX", "MIN", "SUM",
    }
    exclude_groups = {"Math Operators", "Math Transform"}  # vector ops, not indicators
    gap = {}
    for grp, fns in groups.items():
        if grp in exclude_groups:
            continue
        miss = [f for f in fns if f not in covered]
        if miss:
            gap[grp] = miss
    lines += ["", "# Coverage Gap - TA-Lib functions OpenAlgo does NOT have", ""]
    lines.append("(Math Operators / Math Transform groups excluded - those are numpy-level vector "
                 "ops, not indicators. MAX/MIN/SUM are covered by ta.highest/lowest and the rolling-sum util.)")
    lines.append("")
    total_missing = sum(len(v) for v in gap.values())
    lines.append(f"Total missing indicator-type functions: {total_missing}")
    lines.append("")
    for grp, miss in gap.items():
        lines.append(f"## {grp} ({len(miss)} missing)")
        lines.append("- " + ", ".join(miss))
        lines.append("")

    out = Path(__file__).resolve().parent / "TALIB_COMPARISON.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
