# -*- coding: utf-8 -*-
"""
Volatility parity: migrated _backend implementations vs the ORIGINAL numba kernels
(NUMBA_DISABLE_JIT=1) on real RELIANCE data.
"""
import os
os.environ.setdefault("NUMBA_DISABLE_JIT", "1")
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd

from openalgo.indicators import _backend as b
from openalgo.indicators import utils as u
from openalgo.indicators.volatility import (Keltner, Donchian, Chaikin, ULTOSC, RVI as VolRVI,
                                            MASS, BBPercent, BBWidth, ChandelierExit,
                                            HistoricalVolatility, UlcerIndex, STARC, TRANGE)

DATA = Path(__file__).resolve().parent / "data"
FAILS = []


def cmp(name, got, ref, tol=0.0):
    got = np.asarray(got, np.float64)
    ref = np.asarray(ref, np.float64)
    na, nb = np.isnan(got), np.isnan(ref)
    nan_ok = np.array_equal(na, nb)
    m = ~(na | nb)
    d = float(np.abs(got[m] - ref[m]).max()) if m.any() else 0.0
    ok = got.shape == ref.shape and nan_ok and d <= tol
    print(f"  [{'PASS' if ok else 'FAIL'}] {name:16} maxdiff={d:.3e} nan_ok={nan_ok}")
    if not ok:
        FAILS.append(name)


def main():
    df = pd.read_csv(DATA / "RELIANCE_D.csv", index_col=0)
    h = df["high"].to_numpy(np.float64)
    lo = df["low"].to_numpy(np.float64)
    c = df["close"].to_numpy(np.float64)

    ku, km, kl = b.keltner(h, lo, c, 20, 10, 2.0)
    rku, rkm, rkl = Keltner._calculate_keltner_channel(h, lo, c, 20, 10, 2.0)
    cmp("keltner.up", ku, rku)
    cmp("keltner.mid", km, rkm)
    cmp("keltner.low", kl, rkl)

    du, dm, dl = b.donchian(h, lo, 20)
    rdu, rdm, rdl = Donchian._calculate_donchian_channel(h, lo, 20)
    cmp("donchian.up", du, rdu)
    cmp("donchian.mid", dm, rdm)

    # Chaikin reference
    er = Chaikin._calculate_ema(h - lo, 10)
    cvref = np.full_like(er, np.nan)
    for i in range(10, len(er)):
        if er[i - 10] != 0:
            cvref[i] = (er[i] - er[i - 10]) / er[i - 10] * 100
    cmp("chaikin", b.chaikin(h, lo, 10, 10), cvref)

    # NATR reference
    atr = u.atr_wilder(h, lo, c, 14)
    natr_ref = np.where(c != 0, (atr / c) * 100, 0)
    cmp("natr", b.natr(h, lo, c, 14), natr_ref)

    # Volatility RVI
    rvi_ref = VolRVI._calculate_rsi_on_stdev(u.stdev(c, 10), 14)
    cmp("rvi_volatility", b.rvi_volatility(c, 10, 14), rvi_ref)

    # ULTOSC (rolling_sum vs np.sum -> recursive tolerance)
    cmp("ultosc", b.ultosc(h, lo, c, 7, 14, 28),
        ULTOSC._calculate_ultosc(h, lo, c, 7, 14, 28), tol=1e-9)

    cmp("trange", b.true_range(h, lo, c), TRANGE._calculate_trange(h, lo, c))
    cmp("mass", b.mass(h, lo, 10), _mass_ref(h, lo, 10))
    cmp("bbpercent", b.bbpercent(c, 20, 2.0), _bbp_ref(c, 20, 2.0), tol=1e-9)
    cmp("bbwidth", b.bbwidth(c, 20, 2.0), _bbw_ref(c, 20, 2.0), tol=1e-9)
    cel, ces = b.chandelier_exit(h, lo, c, 22, 3.0)
    rcel, rces = ChandelierExit._calculate_chandelier(h, lo, c, 22, 3.0)
    cmp("chandelier.long", cel, rcel, tol=1e-9)
    cmp("chandelier.short", ces, rces, tol=1e-9)
    cmp("hv", b.hv(c, 10, 365, 1), HistoricalVolatility._calculate_hv_tv(c, 10, 365, 1), tol=1e-9)
    cmp("ulcerindex", b.ulcerindex(c, 14, 14, 52, "SMA", False), _ulcer_ref(c, 14, 14))
    su, sm, sl = b.starc(h, lo, c, 5, 15, 1.33)
    cmp("starc.mid", sm, STARC._calculate_sma(c, 5))
    cmp("starc.up", su, STARC._calculate_sma(c, 5) + STARC._calculate_atr(h, lo, c, 15) * 1.33)

    print("\nRESULT:", "ALL VOLATILITY PARITY PASS" if not FAILS else f"FAILURES: {FAILS}")


def _mass_ref(h, lo, length):
    span = h - lo
    e1 = u.ema(span, 9)
    e2 = u.ema(e1, 9)
    ratio = np.where((e2 != 0) & ~np.isnan(e1) & ~np.isnan(e2), e1 / e2, np.nan)
    return u.rolling_sum(ratio, length)


def _bbp_ref(c, p, sd):
    m = BBPercent._calculate_sma(c, p)
    s = BBPercent._calculate_stddev(c, p)
    up, lo_ = m + s * sd, m - s * sd
    out = np.full_like(c, np.nan)
    for i in range(len(c)):
        out[i] = (c[i] - lo_[i]) / (up[i] - lo_[i]) if up[i] != lo_[i] else 0.5
    return out


def _bbw_ref(c, p, sd):
    m = BBWidth._calculate_sma(c, p)
    s = BBWidth._calculate_stddev(c, p)
    up, lo_ = m + s * sd, m - s * sd
    out = np.full_like(c, np.nan)
    for i in range(len(c)):
        out[i] = (up[i] - lo_[i]) / m[i] if m[i] != 0 else 0.0
    return out


def _ulcer_ref(c, length, smooth):
    hh = u.highest(c, length)
    dd = np.where((~np.isnan(hh)) & (hh != 0), 100 * (c - hh) / hh, np.nan)
    return np.sqrt(u.sma(dd ** 2, smooth))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
