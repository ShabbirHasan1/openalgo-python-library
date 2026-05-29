# -*- coding: utf-8 -*-
"""
CI smoke test: import the installed wheel and exercise the Rust-backed indicators on
synthetic OHLCV (no committed data needed). Confirms the extension loads, numba is not
imported, and a few representative indicators produce correct, finite output.
"""
import sys
from pathlib import Path

# Use the in-repo build only when the source tree actually contains the compiled
# extension (local dev copies `_oaindicators` into ./openalgo/). In CI the extension
# is not committed, so fall through to the installed wheel - the artifact we ship -
# instead of shadowing it with an extension-less source package.
_root = Path(__file__).resolve().parent.parent
if list((_root / "openalgo").glob("_oaindicators*")):
    sys.path.insert(0, str(_root))

import numpy as np
import pandas as pd

import openalgo
from openalgo import ta
import openalgo._oaindicators as _rs  # noqa: F401 -- must import (extension present)

FAILS = []


def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        FAILS.append(name)


def main():
    print(f"openalgo {openalgo.__version__}; rust core {_rs.__version__}")
    check("numba not imported", "numba" not in sys.modules)

    n = 2000
    # deterministic synthetic random walk OHLCV
    rng = np.random.default_rng(7)
    close = 100 + np.cumsum(rng.standard_normal(n))
    high = close + np.abs(rng.standard_normal(n))
    low = close - np.abs(rng.standard_normal(n))
    open_ = close + rng.standard_normal(n) * 0.1
    vol = rng.integers(1_000, 10_000, n).astype(float)

    sma = ta.sma(close, 20)
    check("sma matches pandas", np.allclose(
        sma[19:], pd.Series(close).rolling(20).mean().to_numpy()[19:], atol=1e-9))

    ema = ta.ema(close, 20)
    check("ema finite", np.isfinite(ema).all())

    rsi = ta.rsi(close, 14)
    check("rsi in 0..100", np.nanmin(rsi) >= 0 and np.nanmax(rsi) <= 100)

    up, mid, lo = ta.bbands(close, 20, 2.0)
    check("bbands ordered", np.all(up[19:] >= mid[19:]) and np.all(mid[19:] >= lo[19:]))

    macd, sig, hist = ta.macd(close)
    check("macd finite", np.isfinite(macd).all())

    st, dirn = ta.supertrend(high, low, close, 10, 3.0)
    check("supertrend direction set", set(np.unique(dirn[~np.isnan(dirn)])) <= {-1.0, 1.0})

    obv = ta.obv(close, vol)
    check("obv finite", np.isfinite(obv).all())

    adx_di_p, adx_di_m, adx = ta.adx(high, low, close, 14)
    check("adx finite tail", np.isfinite(adx[-1]))

    # Series in -> Series out preserved
    s = pd.Series(close)
    check("series typing", isinstance(ta.sma(s, 10), pd.Series))

    print("RESULT:", "SMOKE PASS" if not FAILS else f"FAIL: {FAILS}")
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
