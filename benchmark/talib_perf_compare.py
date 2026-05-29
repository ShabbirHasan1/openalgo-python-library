# -*- coding: utf-8 -*-
"""
TA-Lib vs OpenAlgo performance + accuracy comparison across every mapped indicator.

For each OpenAlgo `ta.*` that has a TA-Lib counterpart, time both on the large
NIFTY series (best-of-N) and record the speed ratio (talib_ms / new_ms; >1 means
OpenAlgo is faster) and max abs diff. Output is sorted slowest-first so the next
optimization target is obvious. Writes benchmark/TALIB_PERF_COMPARE.md.

Env:
  OABENCH_NROWS  limit rows (default: full file)
  OABENCH_REPS   timing repetitions (default 5)
"""
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from openalgo import ta  # noqa: E402

try:
    import talib
    TL = True
except Exception:
    TL = False

CSV = Path(__file__).resolve().parents[1] / "NIFTY 50.csv"
REPS = int(os.environ.get("OABENCH_REPS", "5"))


def bench(fn):
    best = float("inf")
    for _ in range(REPS):
        s = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - s)
    return best * 1000.0


def first(x):
    return x[0] if isinstance(x, tuple) else x


def maxdiff(a, b):
    try:
        a = np.asarray(first(a), np.float64)
        b = np.asarray(first(b), np.float64)
        n = min(len(a), len(b))
        a, b = a[-n:], b[-n:]
        m = ~(np.isnan(a) | np.isnan(b))
        return float(np.abs(a[m] - b[m]).max()) if m.any() else 0.0
    except Exception:
        return float("nan")


def main():
    nrows = os.environ.get("OABENCH_NROWS")
    df = pd.read_csv(CSV, nrows=int(nrows) if nrows else None)
    o = df["OPEN"].to_numpy(np.float64)
    h = df["HIGH"].to_numpy(np.float64)
    lo = df["LOW"].to_numpy(np.float64)
    c = df["CLOSE"].to_numpy(np.float64)
    n = len(c)
    rng = np.random.default_rng(3)
    v = rng.integers(1_000, 50_000, n).astype(np.float64)
    c2 = lo  # second series for correl

    if not TL:
        print("TA-Lib not available; nothing to compare.")
        return 1

    # (label, openalgo_fn, talib_fn)
    cases = [
        # Overlap / trend
        ("sma(20)", lambda: ta.sma(c, 20), lambda: talib.SMA(c, 20)),
        ("ema(20)", lambda: ta.ema(c, 20), lambda: talib.EMA(c, 20)),
        ("wma(20)", lambda: ta.wma(c, 20), lambda: talib.WMA(c, 20)),
        ("dema(20)", lambda: ta.dema(c, 20), lambda: talib.DEMA(c, 20)),
        ("tema(20)", lambda: ta.tema(c, 20), lambda: talib.TEMA(c, 20)),
        ("trima(20)", lambda: ta.trima(c, 20), lambda: talib.TRIMA(c, 20)),
        ("trima(100)", lambda: ta.trima(c, 100), lambda: talib.TRIMA(c, 100)),
        ("kama(14)", lambda: ta.kama(c, 14), lambda: talib.KAMA(c, 14)),
        ("t3(21)", lambda: ta.t3(c, 21), lambda: talib.T3(c, 21)),
        ("midpoint(14)", lambda: ta.midpoint(c, 14), lambda: talib.MIDPOINT(c, 14)),
        ("midprice(14)", lambda: ta.midprice(h, lo, 14), lambda: talib.MIDPRICE(h, lo, 14)),
        # Momentum / oscillators
        ("rsi(14)", lambda: ta.rsi(c, 14), lambda: talib.RSI(c, 14)),
        ("macd", lambda: ta.macd(c), lambda: talib.MACD(c)),
        ("stochastic", lambda: ta.stochastic(h, lo, c), lambda: talib.STOCH(h, lo, c)),
        ("stochf", lambda: ta.stochf(h, lo, c, 5, 3), lambda: talib.STOCHF(h, lo, c, 5, 3, 0)),
        ("cci(20)", lambda: ta.cci(h, lo, c, 20), lambda: talib.CCI(h, lo, c, 20)),
        ("williams_r(14)", lambda: ta.williams_r(h, lo, c, 14), lambda: talib.WILLR(h, lo, c, 14)),
        ("bop", lambda: ta.bop(o, h, lo, c), lambda: talib.BOP(o, h, lo, c)),
        ("mom(10)", lambda: ta.mom(c, 10), lambda: talib.MOM(c, 10)),
        ("roc(12)", lambda: ta.roc(c, 12), lambda: talib.ROC(c, 12)),
        ("rocp(10)", lambda: ta.rocp(c, 10), lambda: talib.ROCP(c, 10)),
        ("rocr(10)", lambda: ta.rocr(c, 10), lambda: talib.ROCR(c, 10)),
        ("cmo(14)", lambda: ta.cmo(c, 14), lambda: talib.CMO(c, 14)),
        ("apo", lambda: ta.apo(c, 12, 26, "SMA"), lambda: talib.APO(c, 12, 26, 0)),
        ("ppo", lambda: ta.ppo(c), lambda: talib.PPO(c)),
        ("trix(18)", lambda: ta.trix(c, 18), lambda: talib.TRIX(c, 18)),
        ("ultosc", lambda: ta.ultimate_oscillator(h, lo, c), lambda: talib.ULTOSC(h, lo, c)),
        ("stochrsi", lambda: ta.stochrsi(c), lambda: talib.STOCHRSI(c)),
        # Volatility
        ("atr(14)", lambda: ta.atr(h, lo, c, 14), lambda: talib.ATR(h, lo, c, 14)),
        ("natr(14)", lambda: ta.natr(h, lo, c, 14), lambda: talib.NATR(h, lo, c, 14)),
        ("trange", lambda: ta.true_range(h, lo, c), lambda: talib.TRANGE(h, lo, c)),
        ("bbands(20)", lambda: ta.bbands(c, 20), lambda: talib.BBANDS(c, 20)),
        # Volume
        ("obv", lambda: ta.obv(c, v), lambda: talib.OBV(c, v)),
        ("adl", lambda: ta.adl(h, lo, c, v), lambda: talib.AD(h, lo, c, v)),
        ("adosc", lambda: ta.cho(h, lo, c, v), lambda: talib.ADOSC(h, lo, c, v)),
        ("mfi(14)", lambda: ta.mfi(h, lo, c, v, 14), lambda: talib.MFI(h, lo, c, v, 14)),
        # Directional movement / hybrid
        ("adx(14)", lambda: ta.adx(h, lo, c, 14), lambda: talib.ADX(h, lo, c, 14)),
        ("adxr(14)", lambda: ta.adxr(h, lo, c, 14), lambda: talib.ADXR(h, lo, c, 14)),
        ("dx(14)", lambda: ta.dx(h, lo, c, 14), lambda: talib.DX(h, lo, c, 14)),
        ("plus_dm(14)", lambda: ta.plus_dm(h, lo, 14), lambda: talib.PLUS_DM(h, lo, 14)),
        ("minus_dm(14)", lambda: ta.minus_dm(h, lo, 14), lambda: talib.MINUS_DM(h, lo, 14)),
        ("aroon(14)", lambda: ta.aroon(h, lo, 14), lambda: talib.AROON(h, lo, 14)),
        ("aroonosc(14)", lambda: ta.aroon_oscillator(h, lo, 14), lambda: talib.AROONOSC(h, lo, 14)),
        ("psar", lambda: ta.psar(h, lo), lambda: talib.SAR(h, lo)),
        # Price transforms
        ("avgprice", lambda: ta.avgprice(o, h, lo, c), lambda: talib.AVGPRICE(o, h, lo, c)),
        ("medprice", lambda: ta.medprice(h, lo), lambda: talib.MEDPRICE(h, lo)),
        ("typprice", lambda: ta.typprice(h, lo, c), lambda: talib.TYPPRICE(h, lo, c)),
        ("wclprice", lambda: ta.wclprice(h, lo, c), lambda: talib.WCLPRICE(h, lo, c)),
        # Statistics
        ("linreg(14)", lambda: ta.linreg(c, 14), lambda: talib.LINEARREG(c, 14)),
        ("tsf(14)", lambda: ta.tsf(c, 14), lambda: talib.TSF(c, 14)),
        ("linregangle(14)", lambda: ta.linregangle(c, 14), lambda: talib.LINEARREG_ANGLE(c, 14)),
        ("linregintercept(14)", lambda: ta.linregintercept(c, 14), lambda: talib.LINEARREG_INTERCEPT(c, 14)),
        ("correl(20)", lambda: ta.correlation(c, c2, 20), lambda: talib.CORREL(c, c2, 20)),
        ("beta(60)", lambda: ta.beta(c, c2, 60), lambda: talib.BETA(c, c2, 60)),
        ("variance(20)", lambda: ta.variance(c, 20), lambda: talib.VAR(c, 20)),
        ("stddev(20)", lambda: ta.stdev(c, 20), lambda: talib.STDDEV(c, 20)),
    ]

    rows = []
    for label, newf, tlf in cases:
        try:
            nr = newf()
        except Exception as e:
            rows.append((label, float("nan"), float("nan"), float("nan"), f"new err: {e}"))
            continue
        try:
            tr = tlf()
        except Exception as e:
            rows.append((label, bench(newf), float("nan"), float("nan"), f"talib err: {e}"))
            continue
        nm = bench(newf)
        tm = bench(tlf)
        ratio = tm / nm if nm > 0 else float("nan")
        rows.append((label, nm, tm, ratio, f"{maxdiff(nr, tr):.2e}"))

    # sort: worst speed ratio first (smallest talib/new), nan last
    def key(r):
        return (1e9 if (isinstance(r[3], float) and np.isnan(r[3])) else r[3])
    rows.sort(key=key)

    faster = sum(1 for r in rows if isinstance(r[3], float) and r[3] >= 1.0)
    slower = sum(1 for r in rows if isinstance(r[3], float) and r[3] < 1.0)

    lines = [
        "# OpenAlgo vs TA-Lib - Performance Comparison",
        "",
        f"- Dataset: `NIFTY 50.csv` - **{n:,} bars**. Best-of-{REPS} timings.",
        "- **New (ms)** = OpenAlgo `ta.*` (Rust core). **TA-Lib (ms)** = C implementation.",
        "- **Speed (TA-Lib/New)**: >1.0 = OpenAlgo faster; <1.0 = TA-Lib faster (target).",
        "- **max|d|** = max abs difference OpenAlgo vs TA-Lib (intentional TradingView-",
        "  convention differences inflate this for ema/adx/atr/macd/stoch/cci etc.; see",
        "  TALIB_COMPATIBILITY.md).",
        f"- Summary: **{faster} at/faster than TA-Lib**, {slower} slower (sorted slowest-first).",
        "",
        "| Indicator | New (ms) | TA-Lib (ms) | Speed (TA-Lib/New) | max&#124;d&#124; |",
        "|-----------|---------:|------------:|-------------------:|---------:|",
    ]
    for label, nm, tm, ratio, md in rows:
        nm_s = f"{nm:.2f}" if nm == nm else "err"
        tm_s = f"{tm:.2f}" if tm == tm else "err"
        r_s = f"{ratio:.2f}x" if isinstance(ratio, float) and ratio == ratio else "-"
        lines.append(f"| {label} | {nm_s} | {tm_s} | {r_s} | {md} |")

    out = Path(__file__).resolve().parent / "TALIB_PERF_COMPARE.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
