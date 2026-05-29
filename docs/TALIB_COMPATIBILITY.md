# TA-Lib Compatibility & Comparison

OpenAlgo's indicators run on a Rust core (`openalgo._oaindicators`) and follow
**TradingView / Pine Script** semantics. This page documents how OpenAlgo values
compare to **TA-Lib**, which differences are intentional conventions, what was fixed,
the new TA-Lib-compatible indicators that were added, and the remaining coverage gap.

A reproducible value comparison is in `benchmark/talib_compare.py` ->
`benchmark/TALIB_COMPARISON.md` (run on real RELIANCE daily data).

## Indicators that match TA-Lib (value parity, <=1e-6)
SMA, WMA, TRIMA, RSI, CCI, WILLR, BOP, ROC, MOM, TRANGE, ULTOSC, CORREL, LINEARREG,
TSF, STDDEV, ADOSC, BBANDS, plus the newly added price transforms / variants below.

## Intentional differences (OpenAlgo = TradingView, not TA-Lib)
These are NOT bugs - OpenAlgo deliberately matches TradingView, which is what most of
its users reconcile against. They are kept as-is to preserve byte-identical output for
existing users:

| Indicator(s) | Why it differs from TA-Lib |
|---|---|
| EMA, DEMA, TEMA, T3, MACD, PPO | EMA seeded with the first value (TradingView) vs TA-Lib's SMA seed |
| ATR, NATR, ADX, +DI/-DI | Wilder smoothing seed / warm-up index differs (converges quickly) |
| KAMA | TradingView efficiency-ratio over `length` vs TA-Lib fixed 10/2/30 |
| TRIX | log-price x 10000 (TradingView) vs TA-Lib ROC of EMA(price) |
| CMO | simple up/down sums (Chande) vs TA-Lib Wilder smoothing |
| VAR | sample variance /(n-1) vs TA-Lib population /n |
| LINEARREG_SLOPE | endpoint-delta (TradingView) vs TA-Lib OLS slope |
| STOCH | default smoothing parameters differ |
| AROON / AROONOSC | `length+1` lookback (TradingView) vs TA-Lib `length` (matches except boundary bars) |
| SAR | initialization / acceleration edge rules differ |
| AD (A/D line) | cumulative baseline only: OpenAlgo seeds 0, TA-Lib includes the first bar (increments identical) |

## Fixed to match TA-Lib + TradingView
- **OBV** - previously a flat close (`close == prev`) was counted as up-volume. It now
  contributes **0**, matching both TA-Lib and TradingView. OBV increments are now
  identical to TA-Lib (OpenAlgo seeds the running total at 0, like TradingView).

## New TA-Lib-compatible indicators (added; match TA-Lib exactly)
| OpenAlgo | TA-Lib | Formula |
|---|---|---|
| `ta.avgprice(o,h,l,c)` | AVGPRICE | (open+high+low+close)/4 |
| `ta.medprice(h,l)` | MEDPRICE | (high+low)/2 |
| `ta.typprice(h,l,c)` | TYPPRICE | (high+low+close)/3 |
| `ta.wclprice(h,l,c)` | WCLPRICE | (high+low+2*close)/4 |
| `ta.midpoint(data,n)` | MIDPOINT | (max+min)/2 of source over n |
| `ta.midprice(h,l,n)` | MIDPRICE | (highest(high,n)+lowest(low,n))/2 |
| `ta.mom(data,n)` | MOM | data - data[n] |
| `ta.rocp(data,n)` | ROCP | (price-prev)/prev |
| `ta.rocr(data,n)` | ROCR | price/prev |
| `ta.rocr100(data,n)` | ROCR100 | price/prev*100 |
| `ta.apo(data,fast,slow,ma_type)` | APO | MA(fast) - MA(slow) |

## Coverage gap (TA-Lib functions OpenAlgo does not yet have)
Vector math (ADD/SUB/COS/LN/...) and operators (MAX/MIN/SUM - available as
ta.highest/lowest and the rolling-sum util) are excluded as non-indicators.

- **Candlestick patterns (61):** CDL2CROWS ... CDLXSIDEGAP3METHODS - none yet.
- **Hilbert Transform / cycle (6):** HT_DCPERIOD, HT_DCPHASE, HT_PHASOR, HT_SINE,
  HT_TRENDMODE, HT_TRENDLINE - planned.
- **Momentum variants (7):** ADXR, DX, MACDEXT, MACDFIX, MINUS_DM, PLUS_DM, STOCHF.
- **Overlap (3):** MAMA, MAVP, SAREXT.
- **Statistic (2):** LINEARREG_ANGLE, LINEARREG_INTERCEPT.

See `benchmark/TALIB_COMPARISON.md` for the live numbers.
