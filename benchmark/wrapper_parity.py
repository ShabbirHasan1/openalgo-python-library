# -*- coding: utf-8 -*-
"""
Wrapper parity: prove the public `from openalgo import ta` API is unchanged after
swapping a class to the Rust backend.

Deliberately does NOT set NUMBA_DISABLE_JIT -- importing openalgo must now succeed
on its own (warm-up is defensive; swapped indicators are numba-free). Each migrated
indicator is checked against an INDEPENDENT reference (pandas / TA-Lib / manual),
and for type/index preservation (pd.Series in -> pd.Series out with same index;
np.ndarray/list in -> np.ndarray out).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd

import openalgo
from openalgo import ta
import openalgo._oaindicators as _rs  # noqa: F401  (proves extension present)

try:
    import talib
    HAVE_TALIB = True
except Exception:  # noqa: BLE001
    HAVE_TALIB = False

DATA_DIR = Path(__file__).resolve().parent / "data"
FAILS = []


def check(name, cond, detail=""):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{(' - ' + detail) if detail else ''}")
    if not cond:
        FAILS.append(name)


def close_series():
    df = pd.read_csv(DATA_DIR / "RELIANCE_D.csv", index_col=0)
    return df["close"]


def main():
    print(f"openalgo {openalgo.__version__} imported WITHOUT NUMBA_DISABLE_JIT "
          f"(rust ext: {'yes' if getattr(_rs, '__version__', None) else 'no'})")
    s = close_series()
    arr = s.to_numpy(np.float64)
    per = 14

    # ---- SMA vs pandas rolling mean ----
    out = ta.sma(s, per)
    ref = s.rolling(per).mean()
    check("sma type/index", isinstance(out, pd.Series) and out.index.equals(s.index))
    m = ~(np.isnan(out.to_numpy()) | np.isnan(ref.to_numpy()))
    check("sma vs pandas", float(np.abs(out.to_numpy()[m] - ref.to_numpy()[m]).max()) < 1e-9)

    # ---- WMA vs TA-Lib ----
    outw = ta.wma(arr, per)
    check("wma returns ndarray", isinstance(outw, np.ndarray))
    if HAVE_TALIB:
        refw = talib.WMA(arr, per)
        mw = ~(np.isnan(outw) | np.isnan(refw))
        check("wma vs talib", float(np.abs(outw[mw] - refw[mw]).max()) < 1e-9,
              f"maxdiff={np.abs(outw[mw]-refw[mw]).max():.2e}")

    # ---- EMA vs manual recursion (first-value seed, alpha=2/(p+1)) ----
    oute = ta.ema(arr, per)
    alpha = 2.0 / (per + 1.0)
    refe = np.empty_like(arr)
    refe[0] = arr[0]
    for i in range(1, len(arr)):
        refe[i] = alpha * arr[i] + (1 - alpha) * refe[i - 1]
    check("ema vs manual", float(np.abs(oute - refe).max()) < 1e-9,
          f"maxdiff={np.abs(oute-refe).max():.2e}")

    h = pd.read_csv(DATA_DIR / "RELIANCE_D.csv", index_col=0)["high"].to_numpy(np.float64)
    lo_ = pd.read_csv(DATA_DIR / "RELIANCE_D.csv", index_col=0)["low"].to_numpy(np.float64)

    def gate_vs_talib(name, got, ref_vals, tol=1e-9):
        got = np.asarray(got, np.float64)
        ref_vals = np.asarray(ref_vals, np.float64)
        n = min(len(got), len(ref_vals))
        g, r = got[-n:], ref_vals[-n:]
        m = ~(np.isnan(g) | np.isnan(r))
        d = float(np.abs(g[m] - r[m]).max()) if m.any() else 0.0
        check(f"{name} vs talib", d < tol, f"maxdiff={d:.2e}")

    if HAVE_TALIB:
        gate_vs_talib("rsi", ta.rsi(arr, per), talib.RSI(arr, per))
        gate_vs_talib("cci", ta.cci(h, lo_, arr, 20), talib.CCI(h, lo_, arr, 20))
        gate_vs_talib("williams_r", ta.williams_r(h, lo_, arr, per), talib.WILLR(h, lo_, arr, per))
        up, mid, low = ta.bbands(arr, 20, 2.0)
        tu, tm, tl = talib.BBANDS(arr, 20, 2.0, 2.0, 0)
        gate_vs_talib("bbands.mid", mid, tm)
        gate_vs_talib("bbands.upper", up, tu)
        gate_vs_talib("bbands.lower", low, tl)
        # Informational (TA-Lib seeds EMA/ATR/STOCH differently from OpenAlgo):
        for name, got, tv in [
            ("atr", ta.atr(h, lo_, arr, per), talib.ATR(h, lo_, arr, per)),
            ("macd", ta.macd(arr)[0], talib.MACD(arr)[0]),
        ]:
            g = np.asarray(got, np.float64); t = np.asarray(tv, np.float64)
            m = ~(np.isnan(g) | np.isnan(t))
            print(f"  [info] {name} vs talib maxdiff={np.abs(g[m]-t[m]).max():.3e} "
                  f"(convention diff expected)")

    # tuple-returning wrappers preserve Series typing
    k, d = ta.stochastic(pd.Series(h), pd.Series(lo_), pd.Series(arr))
    check("stochastic returns Series tuple", isinstance(k, pd.Series) and isinstance(d, pd.Series))

    # ---- list input -> ndarray out ----
    outl = ta.sma([1.0, 2.0, 3.0, 4.0, 5.0], 2)
    check("sma list->ndarray", isinstance(outl, np.ndarray) and outl[1] == 1.5)

    print("\nRESULT:", "ALL WRAPPER GATES PASS" if not FAILS else f"FAILURES: {FAILS}")
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
