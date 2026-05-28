# -*- coding: utf-8 -*-
"""
Parity gate: Rust core (openalgo._oaindicators) vs the Python reference kernels
(openalgo.indicators.utils, run with NUMBA_DISABLE_JIT=1 = identical algorithm),
with TA-Lib as a secondary cross-check where definitions align.

HARD GATE  = Rust must match the Python reference (this is the backend we replace):
             identical length, identical NaN mask, and finite values within
             atol=1e-12 / rtol=1e-9 (EMA-family) or exact (min/max/diff/bool).
TA-Lib      = informational. "match" rows are expected ~0; "info" rows differ by a
             known convention (seed/alignment) and are reported, not gated.

Exit code 0 only if every HARD gate passes on every dataset.
"""
import os
os.environ.setdefault("NUMBA_DISABLE_JIT", "1")

import sys
from pathlib import Path
# Ensure the LOCAL openalgo package (repo root) wins over any pip-installed copy.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd

import openalgo._oaindicators as rs
from openalgo.indicators import utils as ref
from openalgo.indicators.momentum import RSI as _RSI, Stochastic as _STO, CCI as _CCI, WilliamsR as _WR

try:
    import talib
    HAVE_TALIB = True
except Exception:  # noqa: BLE001
    HAVE_TALIB = False

DATA_DIR = Path(__file__).resolve().parent / "data"
ATOL, RTOL = 1e-12, 1e-9


def load(symbol, interval):
    df = pd.read_csv(DATA_DIR / f"{symbol}_{interval}.csv")
    return {
        "open": df["open"].to_numpy(np.float64),
        "high": df["high"].to_numpy(np.float64),
        "low": df["low"].to_numpy(np.float64),
        "close": df["close"].to_numpy(np.float64),
        "volume": df["volume"].to_numpy(np.float64),
    }


def cmp_float(a, b):
    """Return (ok, max_abs, max_rel, nan_ok) comparing two float arrays."""
    a = np.asarray(a, np.float64)
    b = np.asarray(b, np.float64)
    if a.shape != b.shape:
        return False, np.inf, np.inf, False
    na, nb = np.isnan(a), np.isnan(b)
    nan_ok = np.array_equal(na, nb)
    mask = ~(na | nb)
    if not mask.any():
        return nan_ok, 0.0, 0.0, nan_ok
    da = np.abs(a[mask] - b[mask])
    denom = np.maximum(np.abs(b[mask]), 1e-300)
    dr = da / denom
    max_abs, max_rel = float(da.max()), float(dr.max())
    ok = nan_ok and (max_abs <= ATOL or max_rel <= RTOL)
    return ok, max_abs, max_rel, nan_ok


def cmp_bool(a, b):
    a = np.asarray(a).astype(bool)
    b = np.asarray(b).astype(bool)
    if a.shape != b.shape:
        return False, 1, 1, False
    diff = int(np.sum(a != b))
    return diff == 0, float(diff), float(diff), True


# Each entry: (label, rust_fn, ref_fn, kind, talib_fn_or_None, talib_mode)
#   kind: "f" float gate, "b" bool gate
def build_cases(P):
    h, l, c, v = P["high"], P["low"], P["close"], P["volume"]
    per = 14
    cases = [
        ("sma(14)", lambda: rs.sma(c, per), lambda: ref.sma(c, per), "f",
         (lambda: talib.SMA(c, per)) if HAVE_TALIB else None, "match"),
        ("wma(14)", lambda: rs.wma(c, per), lambda: _ref_wma(c, per), "f",
         (lambda: talib.WMA(c, per)) if HAVE_TALIB else None, "match"),
        ("ema(14)", lambda: rs.ema(c, per), lambda: ref.ema(c, per), "f",
         (lambda: talib.EMA(c, per)) if HAVE_TALIB else None, "info"),
        ("ema_wilder(14)", lambda: rs.ema_wilder(c, per), lambda: ref.ema_wilder(c, per), "f",
         None, "info"),
        ("stdev(14)", lambda: rs.stdev(c, per), lambda: ref.stdev(c, per), "f",
         (lambda: talib.STDDEV(c, per, 1.0)) if HAVE_TALIB else None, "match"),
        ("rolling_sum(14)", lambda: rs.rolling_sum(c, per), lambda: ref.rolling_sum(c, per), "f",
         (lambda: talib.SUM(c, per)) if HAVE_TALIB else None, "match"),
        ("rolling_variance(14)", lambda: rs.rolling_variance(c, per),
         lambda: ref.rolling_variance(c, per), "f",
         (lambda: talib.VAR(c, per, 1.0)) if HAVE_TALIB else None, "match"),
        ("change(1)", lambda: rs.change(c, 1), lambda: ref.change(c, 1), "f", None, "info"),
        ("roc(10)", lambda: rs.roc(c, 10), lambda: ref.roc(c, 10), "f",
         (lambda: talib.ROC(c, 10)) if HAVE_TALIB else None, "match"),
        ("highest(14)", lambda: rs.highest(c, per), lambda: ref.highest(c, per), "f",
         (lambda: talib.MAX(c, per)) if HAVE_TALIB else None, "match"),
        ("lowest(14)", lambda: rs.lowest(c, per), lambda: ref.lowest(c, per), "f",
         (lambda: talib.MIN(c, per)) if HAVE_TALIB else None, "match"),
        ("true_range", lambda: rs.true_range(h, l, c), lambda: ref.true_range(h, l, c), "f",
         (lambda: talib.TRANGE(h, l, c)) if HAVE_TALIB else None, "info"),
        ("atr_wilder(14)", lambda: rs.atr_wilder(h, l, c, per),
         lambda: ref.atr_wilder(h, l, c, per), "f",
         (lambda: talib.ATR(h, l, c, per)) if HAVE_TALIB else None, "info"),
        ("atr_sma(14)", lambda: rs.atr_sma(h, l, c, per),
         lambda: ref.atr_sma(h, l, c, per), "f", None, "info"),
        ("vwma(14)", lambda: rs.vwma(c, v, per), lambda: ref.vwma_optimized(c, v, per), "f",
         None, "info"),
        ("cmo(14)", lambda: rs.cmo(c, per), lambda: ref.cmo_optimized(c, per), "f",
         (lambda: talib.CMO(c, per)) if HAVE_TALIB else None, "info"),
        ("kama(10,2,30)", lambda: rs.kama(c, 10, 2.0, 30.0),
         lambda: ref.kama_optimized(c, 10, 2.0, 30.0), "f", None, "info"),
        ("ulcer_index(14)", lambda: rs.ulcer_index(c, per),
         lambda: ref.ulcer_index_optimized(c, per), "f", None, "info"),
        # boolean kernels
        ("crossover", lambda: rs.crossover(c, ref.sma(c, per)),
         lambda: ref.crossover(c, ref.sma(c, per)), "b", None, ""),
        ("crossunder", lambda: rs.crossunder(c, ref.sma(c, per)),
         lambda: ref.crossunder(c, ref.sma(c, per)), "b", None, ""),
        ("cross", lambda: rs.cross(c, ref.sma(c, per)),
         lambda: ref.cross(c, ref.sma(c, per)), "b", None, ""),
        ("rising(5)", lambda: rs.rising(c, 5), lambda: ref.rising(c, 5), "b", None, ""),
        ("falling(5)", lambda: rs.falling(c, 5), lambda: ref.falling(c, 5), "b", None, ""),
        ("valuewhen", lambda: rs.valuewhen(_expr(c, per), c, 1),
         lambda: ref.valuewhen(_expr(c, per), c, 1), "f", None, ""),
        # Phase-1 indicators (reference = original numba staticmethods, pure-python)
        ("rsi(14)", lambda: rs.rsi(c, per), lambda: _RSI._calculate_rsi(c, per), "f",
         (lambda: talib.RSI(c, per)) if HAVE_TALIB else None, "match"),
        ("cci(14)", lambda: rs.cci(h, l, c, per),
         lambda: _CCI._calculate_cci(h, l, c, per), "f",
         (lambda: talib.CCI(h, l, c, per)) if HAVE_TALIB else None, "match"),
        ("williams_r(14)", lambda: rs.williams_r(h, l, c, per),
         lambda: _WR._calculate_williams_r(c, per, ref.highest(h, per), ref.lowest(l, per)), "f",
         (lambda: talib.WILLR(h, l, c, per)) if HAVE_TALIB else None, "match"),
        ("stoch_k", lambda: rs.stochastic(h, l, c, per, 3, 3)[0],
         lambda: _ref_stoch(h, l, c, per, 3, 3)[0], "f", None, ""),
        ("stoch_d", lambda: rs.stochastic(h, l, c, per, 3, 3)[1],
         lambda: _ref_stoch(h, l, c, per, 3, 3)[1], "f", None, ""),
    ]
    return cases


def _ref_stoch(h, l, c, k, sk, d):
    hh = ref.highest(h, k)
    ll = ref.lowest(l, k)
    return _STO._calculate_stochastic(c, k, sk, d, hh, ll)


def _ref_wma(c, period):
    n = len(c)
    out = np.full(n, np.nan)
    w = np.arange(1, period + 1, dtype=np.float64)
    ws = w.sum()
    for i in range(period - 1, n):
        out[i] = float(np.dot(c[i - period + 1:i + 1], w) / ws)
    return out


def _expr(c, period):
    """Boolean-like float array: close above its SMA (drives valuewhen)."""
    return (c > np.nan_to_num(ref.sma(c, period), nan=np.inf)).astype(np.float64)


def talib_diff(rust_vals, tfn):
    """Informational max abs diff Rust vs TA-Lib over common finite region."""
    try:
        tv = np.asarray(tfn(), np.float64)
        a = np.asarray(rust_vals, np.float64)
        n = min(len(a), len(tv))
        a, tv = a[-n:], tv[-n:]
        mask = ~(np.isnan(a) | np.isnan(tv))
        if not mask.any():
            return None
        return float(np.abs(a[mask] - tv[mask]).max())
    except Exception as exc:  # noqa: BLE001
        return f"err:{type(exc).__name__}"


def main():
    datasets = [("RELIANCE", "D"), ("RELIANCE", "1m"), ("SBIN", "D"), ("SBIN", "1m")]
    all_pass = True
    hard_fail = []
    print(f"Parity gate  (atol={ATOL}, rtol={RTOL}, TA-Lib={'yes' if HAVE_TALIB else 'no'})")
    for symbol, interval in datasets:
        P = load(symbol, interval)
        n = len(P["close"])
        print(f"\n=== {symbol} {interval}  ({n} bars) ===")
        print(f"{'kernel':22} {'gate':6} {'max_abs':>12} {'max_rel':>12}  {'talib':>12}")
        for label, rfn, reffn, kind, tfn, tmode in build_cases(P):
            rv = rfn()
            ev = reffn()
            if kind == "f":
                ok, ma, mr, nan_ok = cmp_float(rv, ev)
            else:
                ok, ma, mr, nan_ok = cmp_bool(rv, ev)
            td = ""
            if tfn is not None:
                d = talib_diff(rv, tfn)
                if isinstance(d, float):
                    td = f"{d:.2e}{'' if tmode=='match' else '*'}"
                elif d is not None:
                    td = str(d)
            gate = "PASS" if ok else "FAIL"
            if not ok:
                all_pass = False
                hard_fail.append(f"{symbol}/{interval}/{label} (nan_ok={nan_ok})")
            print(f"{label:22} {gate:6} {ma:>12.3e} {mr:>12.3e}  {td:>12}")
    print("\n" + ("=" * 60))
    print("* = TA-Lib differs by a known convention (seed/alignment); informational.")
    if all_pass:
        print("RESULT: ALL HARD GATES PASS (Rust == Python reference).")
        return 0
    print("RESULT: HARD GATE FAILURES:")
    for f in hard_fail:
        print("  -", f)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
