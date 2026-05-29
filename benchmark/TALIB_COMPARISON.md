# TA-Lib vs OpenAlgo - Value Comparison

Data: RELIANCE daily (7629 bars). MATCH if max abs diff <= 1e-06.
Result: 18 MATCH, 21 DIFFER.

Classification of the DIFFER cases:
- CONVENTION (intentional, OpenAlgo follows TradingView/Pine; changing would break the byte-identical guarantee for existing users): EMA/DEMA/TEMA/T3/MACD/PPO (EMA first-value seed vs TA-Lib SMA seed), ATR/NATR/ADX/PLUS_DI (Wilder seed/warmup index), KAMA (ER window), TRIX (log-price), CMO (simple sums vs Wilder), VAR (sample /(n-1) vs population /n), LINEARREG_SLOPE (endpoint-delta vs OLS slope), STOCH (default smoothing params), AROON/AROONOSC (length+1 lookback), SAR (init/AF edge rules), AD (cumulative baseline = constant offset, increments identical).
- GENUINE QUIRK (matches NEITHER TA-Lib nor TradingView): OBV treats a flat close (close==prev) as up-volume; both TA-Lib and TradingView treat it as no-change. This is the only case worth an actual fix (it is pre-existing OpenAlgo behavior).

| Indicator (TA-Lib) | Verdict | max abs diff | max rel diff | Reason if differs |
|--------------------|---------|-------------:|-------------:|-------------------|
| SMA | MATCH | 0.000e+00 | 0.000e+00 | - |
| EMA | DIFFERS | 1.678e-01 | 2.563e-02 | seed: TA-Lib=SMA seed, OpenAlgo=first-value (TradingView) |
| WMA | MATCH | 0.000e+00 | 0.000e+00 | - |
| DEMA | DIFFERS | 1.224e-01 | 1.469e-02 | EMA seed convention (TradingView) |
| TEMA | DIFFERS | 2.940e-02 | 3.932e-03 | EMA seed convention (TradingView) |
| TRIMA | MATCH | 4.547e-13 | 4.430e-16 | - |
| KAMA | DIFFERS | 5.238e-01 | 6.194e-02 | TA-Lib fixed 10/2/30 vs OpenAlgo TradingView ER(length) |
| T3 | DIFFERS | 6.018e-03 | 9.611e-04 | EMA seed / vfactor convention |
| SAR | DIFFERS | 1.691e+02 | 3.435e+00 | init/AF edge-rules differ slightly |
| BBANDS.mid | MATCH | 0.000e+00 | 0.000e+00 | - |
| BBANDS.up | MATCH | 1.478e-12 | 3.147e-14 | - |
| RSI | MATCH | 2.132e-14 | 1.055e-15 | - |
| CCI | MATCH | 1.674e-11 | 6.895e-11 | - |
| WILLR | MATCH | 1.421e-14 | 2.726e-16 | - |
| BOP | MATCH | 0.000e+00 | 0.000e+00 | - |
| CMO | DIFFERS | 9.129e+01 | 1.966e+03 | TA-Lib Wilder-smoothed vs OpenAlgo simple sums |
| ROC | MATCH | 5.684e-14 | 1.771e-12 | - |
| MOM | MATCH | 0.000e+00 | 0.000e+00 | - |
| MACD.line | DIFFERS | 6.671e-02 | 3.396e+00 | EMA seed convention (TradingView) |
| PPO | DIFFERS | 1.940e+01 | 1.200e+03 | EMA seed convention |
| TRIX | DIFFERS | 1.452e+02 | 1.339e+04 | TA-Lib ROC of EMA(price); OpenAlgo uses log-price*10000 (TradingView) |
| ATR | DIFFERS | 1.048e-02 | 4.392e-02 | Wilder seed index differs (TA-Lib seeds at period) |
| NATR | DIFFERS | 1.721e-01 | 4.392e-02 | follows ATR seed |
| TRANGE | MATCH | 0.000e+00 | 0.000e+00 | - |
| ULTOSC | MATCH | 2.558e-13 | 5.307e-15 | - |
| AROON.up | DIFFERS | 6.429e+01 | 1.000e+00 | lookback length+1 (TradingView) vs length (TA-Lib); matches except boundary bars |
| AROONOSC | DIFFERS | 8.571e+01 | 1.800e+00 | lookback length+1 (TradingView) vs length (TA-Lib) |
| ADX | DIFFERS | 9.082e-01 | 2.481e-02 | Wilder DI/DX; seed/warmup index differs |
| PLUS_DI | DIFFERS | 4.163e-01 | 2.542e-02 | Wilder; seed/warmup differs |
| STOCH.k | DIFFERS | 6.890e+01 | 2.045e+01 | TA-Lib default slowing differs from OpenAlgo k/smooth/d |
| CORREL | MATCH | 1.876e-12 | 9.077e-11 | - |
| LINEARREG | MATCH | 1.705e-13 | 9.967e-16 | - |
| LINEARREG_SLOPE | DIFFERS | 3.831e+01 | 3.795e+03 | TA-Lib OLS slope vs OpenAlgo TradingView (delta of endpoints) |
| TSF | MATCH | 1.705e-13 | 1.241e-15 | - |
| STDDEV | MATCH | 6.963e-13 | 1.973e-12 | - |
| VAR | DIFFERS | 3.993e+02 | 5.263e-02 | TA-Lib population /n vs OpenAlgo sample /(n-1) |
| OBV | DIFFERS | 1.203e+09 | 2.005e+01 | QUIRK: OpenAlgo treats close==prev as UP (+vol); TA-Lib AND TradingView treat flat as 0 -> increments differ on flat bars |
| AD | DIFFERS | 7.437e+07 | 9.571e+00 | baseline offset only: OpenAlgo seeds 0, TA-Lib includes bar-0 MFV (increments identical, ~1e-6) |
| ADOSC | MATCH | 0.000e+00 | 0.000e+00 | - |

# Coverage Gap - TA-Lib functions OpenAlgo does NOT have

(Math Operators / Math Transform groups excluded - those are numpy-level vector ops, not indicators. MAX/MIN/SUM are covered by ta.highest/lowest and the rolling-sum util.)

Total missing indicator-type functions: 87

## Cycle Indicators (5 missing)
- HT_DCPERIOD, HT_DCPHASE, HT_PHASOR, HT_SINE, HT_TRENDMODE

## Momentum Indicators (10 missing)
- ADXR, DX, MACDEXT, MACDFIX, MINUS_DM, PLUS_DM, ROCP, ROCR, ROCR100, STOCHF

## Overlap Studies (5 missing)
- HT_TRENDLINE, MAMA, MAVP, MIDPOINT, SAREXT

## Pattern Recognition (61 missing)
- CDL2CROWS, CDL3BLACKCROWS, CDL3INSIDE, CDL3LINESTRIKE, CDL3OUTSIDE, CDL3STARSINSOUTH, CDL3WHITESOLDIERS, CDLABANDONEDBABY, CDLADVANCEBLOCK, CDLBELTHOLD, CDLBREAKAWAY, CDLCLOSINGMARUBOZU, CDLCONCEALBABYSWALL, CDLCOUNTERATTACK, CDLDARKCLOUDCOVER, CDLDOJI, CDLDOJISTAR, CDLDRAGONFLYDOJI, CDLENGULFING, CDLEVENINGDOJISTAR, CDLEVENINGSTAR, CDLGAPSIDESIDEWHITE, CDLGRAVESTONEDOJI, CDLHAMMER, CDLHANGINGMAN, CDLHARAMI, CDLHARAMICROSS, CDLHIGHWAVE, CDLHIKKAKE, CDLHIKKAKEMOD, CDLHOMINGPIGEON, CDLIDENTICAL3CROWS, CDLINNECK, CDLINVERTEDHAMMER, CDLKICKING, CDLKICKINGBYLENGTH, CDLLADDERBOTTOM, CDLLONGLEGGEDDOJI, CDLLONGLINE, CDLMARUBOZU, CDLMATCHINGLOW, CDLMATHOLD, CDLMORNINGDOJISTAR, CDLMORNINGSTAR, CDLONNECK, CDLPIERCING, CDLRICKSHAWMAN, CDLRISEFALL3METHODS, CDLSEPARATINGLINES, CDLSHOOTINGSTAR, CDLSHORTLINE, CDLSPINNINGTOP, CDLSTALLEDPATTERN, CDLSTICKSANDWICH, CDLTAKURI, CDLTASUKIGAP, CDLTHRUSTING, CDLTRISTAR, CDLUNIQUE3RIVER, CDLUPSIDEGAP2CROWS, CDLXSIDEGAP3METHODS

## Price Transform (4 missing)
- AVGPRICE, MEDPRICE, TYPPRICE, WCLPRICE

## Statistic Functions (2 missing)
- LINEARREG_ANGLE, LINEARREG_INTERCEPT

