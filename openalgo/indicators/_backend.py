# -*- coding: utf-8 -*-
"""
Indicator compute backend.

Single seam between the Python indicator wrappers and the compiled Rust core
(``openalgo._oaindicators``). When the extension is present every kernel runs in
Rust; when it is absent (a source checkout without a built wheel) a pure-NumPy
fallback returns the same values. Neither path depends on numba / llvmlite.

Wrappers should call these functions instead of the legacy numba kernels.
"""
import numpy as np

try:
    from openalgo import _oaindicators as _rs
    HAVE_RUST = True
except Exception:  # noqa: BLE001 - extension optional; fall back to numpy
    _rs = None
    HAVE_RUST = False


def _f(a):
    """Contiguous float64 view (Rust as_slice requires C-contiguous float64)."""
    return np.ascontiguousarray(a, dtype=np.float64)


def sma(data, period):
    data = _f(data)
    period = int(period)
    if HAVE_RUST:
        return _rs.sma(data, period)
    n = data.size
    out = np.full(n, np.nan)
    if period <= 0 or n < period:
        return out
    c = np.cumsum(data)
    out[period - 1] = c[period - 1] / period
    if n > period:
        out[period:] = (c[period:] - c[:-period]) / period
    return out


def wma(data, period):
    data = _f(data)
    period = int(period)
    if HAVE_RUST:
        return _rs.wma(data, period)
    n = data.size
    out = np.full(n, np.nan)
    if period <= 0 or n < period:
        return out
    weights = np.arange(1, period + 1, dtype=np.float64)
    wsum = weights.sum()
    valid = np.convolve(data, weights[::-1], mode="valid") / wsum
    out[period - 1:] = valid
    return out


def ema(data, period):
    data = _f(data)
    period = int(period)
    if HAVE_RUST:
        return _rs.ema(data, period)
    n = data.size
    out = np.empty(n)
    if n == 0:
        return out
    alpha = 2.0 / (period + 1.0)
    out[0] = data[0]
    for i in range(1, n):
        out[i] = alpha * data[i] + (1.0 - alpha) * out[i - 1]
    return out


def stdev(data, period):
    data = _f(data)
    period = int(period)
    if HAVE_RUST:
        return _rs.stdev(data, period)
    n = data.size
    out = np.full(n, np.nan)
    if period <= 0 or n < period:
        return out
    c = np.cumsum(data)
    csq = np.cumsum(data * data)
    s = np.empty(n)
    sq = np.empty(n)
    s[period - 1] = c[period - 1]
    sq[period - 1] = csq[period - 1]
    if n > period:
        s[period:] = c[period:] - c[:-period]
        sq[period:] = csq[period:] - csq[:-period]
    mean = s[period - 1:] / period
    var = sq[period - 1:] / period - mean * mean
    out[period - 1:] = np.sqrt(np.maximum(0.0, var))
    return out


def true_range(high, low, close):
    high, low, close = _f(high), _f(low), _f(close)
    if HAVE_RUST:
        return _rs.true_range(high, low, close)
    n = high.size
    tr = np.empty(n)
    if n == 0:
        return tr
    tr[0] = high[0] - low[0]
    hl = high[1:] - low[1:]
    hc = np.abs(high[1:] - close[:-1])
    lc = np.abs(low[1:] - close[:-1])
    tr[1:] = np.maximum(np.maximum(hl, hc), lc)
    return tr


def atr_wilder(high, low, close, period):
    high, low, close = _f(high), _f(low), _f(close)
    period = int(period)
    if HAVE_RUST:
        return _rs.atr_wilder(high, low, close, period)
    n = high.size
    atr = np.full(n, np.nan)
    if period <= 0 or n < period:
        return atr
    tr = true_range(high, low, close)
    atr[period - 1] = tr[:period].mean()
    for i in range(period, n):
        atr[i] = (atr[i - 1] * (period - 1) + tr[i]) / period
    return atr


def rsi(data, period):
    data = _f(data)
    period = int(period)
    if HAVE_RUST:
        return _rs.rsi(data, period)
    n = data.size
    out = np.full(n, np.nan)
    if period <= 0 or n < period + 1:
        return out
    deltas = np.diff(data)
    gains = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)
    avg_gain = gains[:period].mean()
    avg_loss = losses[:period].mean()
    out[period] = 100.0 if avg_loss == 0 else 100.0 - 100.0 / (1.0 + avg_gain / avg_loss)
    for i in range(period, n - 1):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        out[i + 1] = 100.0 if avg_loss == 0 else 100.0 - 100.0 / (1.0 + avg_gain / avg_loss)
    return out


def macd(data, fast_period, slow_period, signal_period):
    macd_line = ema(data, fast_period) - ema(data, slow_period)
    signal_line = ema(macd_line, signal_period)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def bbands(data, period, std_dev):
    middle = sma(data, period)
    sd = stdev(data, period)
    upper = middle + std_dev * sd
    lower = middle - std_dev * sd
    return upper, middle, lower


def stochastic(high, low, close, k_period, smooth_k, d_period):
    high, low, close = _f(high), _f(low), _f(close)
    if HAVE_RUST:
        return _rs.stochastic(high, low, close, int(k_period), int(smooth_k), int(d_period))
    hh = _roll(high, int(k_period), np.max)
    ll = _roll(low, int(k_period), np.min)
    n = close.size
    fast_k = np.full(n, np.nan)
    fk = k_period - 1
    for i in range(fk, n):
        fast_k[i] = 100.0 * (close[i] - ll[i]) / (hh[i] - ll[i]) if hh[i] != ll[i] else 50.0
    slow_k = sma(fast_k[fk:], smooth_k)
    slow_k = np.concatenate([np.full(fk, np.nan), slow_k])
    slow_d = sma(slow_k[fk + smooth_k - 1:], d_period)
    slow_d = np.concatenate([np.full(fk + smooth_k - 1, np.nan), slow_d])
    return slow_k, slow_d


def cci(high, low, close, period):
    high, low, close = _f(high), _f(low), _f(close)
    period = int(period)
    if HAVE_RUST:
        return _rs.cci(high, low, close, period)
    n = close.size
    out = np.full(n, np.nan)
    if period <= 0 or n < period:
        return out
    tp = (high + low + close) / 3.0
    sma_tp = sma(tp, period)
    for i in range(period - 1, n):
        md = np.abs(tp[i - period + 1:i + 1] - sma_tp[i]).mean()
        out[i] = (tp[i] - sma_tp[i]) / (0.015 * md) if md != 0 else 0.0
    return out


def williams_r(high, low, close, period):
    high, low, close = _f(high), _f(low), _f(close)
    period = int(period)
    if HAVE_RUST:
        return _rs.williams_r(high, low, close, period)
    hh = _roll(high, period, np.max)
    ll = _roll(low, period, np.min)
    n = close.size
    out = np.full(n, np.nan)
    for i in range(period - 1, n):
        out[i] = -100.0 * (hh[i] - close[i]) / (hh[i] - ll[i]) if hh[i] != ll[i] else -50.0
    return out


def _roll(data, period, fn):
    """Rolling reduction for numpy fallbacks (NaN warm-up)."""
    n = data.size
    out = np.full(n, np.nan)
    for i in range(period - 1, n):
        out[i] = fn(data[i - period + 1:i + 1])
    return out
