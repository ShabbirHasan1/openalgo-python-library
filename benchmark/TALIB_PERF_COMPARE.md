# OpenAlgo vs TA-Lib - Performance Comparison

- Dataset: `NIFTY 50.csv` - **924,782 bars**. Best-of-5 timings.
- **New (ms)** = OpenAlgo `ta.*` (Rust core). **TA-Lib (ms)** = C implementation.
- **Speed (TA-Lib/New)**: >1.0 = OpenAlgo faster; <1.0 = TA-Lib faster (target).
- **max|d|** = max abs difference OpenAlgo vs TA-Lib (intentional TradingView-
  convention differences inflate this for ema/adx/atr/macd/stoch/cci etc.; see
  TALIB_COMPATIBILITY.md).
- Summary: **7 at/faster than TA-Lib**, 49 slower (sorted slowest-first).

| Indicator | New (ms) | TA-Lib (ms) | Speed (TA-Lib/New) | max&#124;d&#124; |
|-----------|---------:|------------:|-------------------:|---------:|
| beta(60) | 66.93 | 5.05 | 0.08x | 2.31e+00 |
| adosc | 22.45 | 1.94 | 0.09x | 0.00e+00 |
| t3(21) | 20.65 | 2.64 | 0.13x | 3.38e-02 |
| ultosc | 47.66 | 7.63 | 0.16x | 1.42e-14 |
| wclprice | 7.35 | 1.19 | 0.16x | 0.00e+00 |
| adx(14) | 40.89 | 7.64 | 0.19x | 9.81e+01 |
| apo | 18.42 | 3.64 | 0.20x | 8.84e-10 |
| avgprice | 7.74 | 1.53 | 0.20x | 7.28e-12 |
| correl(20) | 24.86 | 5.70 | 0.23x | 2.72e+00 |
| midprice(14) | 20.54 | 4.78 | 0.23x | 0.00e+00 |
| typprice | 5.76 | 1.35 | 0.23x | 0.00e+00 |
| adl | 5.98 | 1.48 | 0.25x | 1.46e+03 |
| bop | 5.92 | 1.56 | 0.26x | 0.00e+00 |
| mom(10) | 3.61 | 1.04 | 0.29x | 0.00e+00 |
| variance(20) | 7.56 | 2.27 | 0.30x | 1.11e+04 |
| kama(14) | 7.60 | 2.29 | 0.30x | 1.64e+00 |
| medprice | 3.85 | 1.20 | 0.31x | 0.00e+00 |
| ppo | 13.14 | 4.30 | 0.33x | 2.42e+00 |
| rocp(10) | 4.59 | 1.54 | 0.34x | 0.00e+00 |
| trange | 3.93 | 1.35 | 0.34x | 0.00e+00 |
| williams_r(14) | 21.51 | 7.73 | 0.36x | 5.00e+01 |
| psar | 11.59 | 4.39 | 0.38x | 2.73e+02 |
| aroonosc(14) | 20.09 | 7.86 | 0.39x | 1.00e+02 |
| trima(20) | 4.72 | 1.95 | 0.41x | 1.15e-09 |
| trima(100) | 4.77 | 2.00 | 0.42x | 2.78e-09 |
| aroon(14) | 18.88 | 8.62 | 0.46x | 1.00e+02 |
| cmo(14) | 10.77 | 5.03 | 0.47x | 1.47e+02 |
| tema(20) | 14.44 | 6.97 | 0.48x | 5.01e-02 |
| rocr(10) | 3.16 | 1.53 | 0.48x | 0.00e+00 |
| stochastic | 24.34 | 11.86 | 0.49x | 1.00e+02 |
| stochf | 22.32 | 11.13 | 0.50x | 2.84e-14 |
| natr(14) | 10.06 | 5.38 | 0.54x | 3.16e-03 |
| sma(20) | 2.79 | 1.50 | 0.54x | 6.44e-10 |
| mfi(14) | 12.65 | 6.86 | 0.54x | 3.75e+02 |
| trix(18) | 11.64 | 6.46 | 0.55x | 3.12e+01 |
| wma(20) | 2.85 | 1.62 | 0.57x | 5.14e-09 |
| bbands(20) | 11.33 | 6.98 | 0.62x | 4.88e-04 |
| atr(14) | 8.31 | 5.18 | 0.62x | 2.73e-01 |
| minus_dm(14) | 6.26 | 4.30 | 0.69x | 0.00e+00 |
| adxr(14) | 12.52 | 8.60 | 0.69x | 4.26e-14 |
| plus_dm(14) | 6.26 | 4.48 | 0.72x | 0.00e+00 |
| dema(20) | 7.50 | 5.37 | 0.72x | 8.58e-01 |
| midpoint(14) | 19.50 | 14.15 | 0.73x | 0.00e+00 |
| dx(14) | 9.99 | 7.37 | 0.74x | 5.68e-14 |
| obv | 4.70 | 3.61 | 0.77x | 4.08e+04 |
| roc(12) | 1.92 | 1.52 | 0.79x | 1.15e-14 |
| stochrsi | 19.05 | 15.36 | 0.81x | 1.00e+02 |
| rsi(14) | 5.76 | 4.86 | 0.84x | 2.84e-14 |
| ema(20) | 2.28 | 2.01 | 0.88x | 1.67e+00 |
| stddev(20) | 3.60 | 4.11 | 1.14x | 2.44e-04 |
| macd | 7.29 | 8.49 | 1.17x | 1.18e+00 |
| cci(20) | 14.18 | 17.88 | 1.26x | 1.33e+02 |
| linregintercept(14) | 6.48 | 9.31 | 1.44x | 6.61e-05 |
| linregangle(14) | 11.71 | 16.92 | 1.45x | 5.82e-04 |
| linreg(14) | 6.13 | 9.20 | 1.50x | 6.61e-05 |
| tsf(14) | 6.01 | 9.06 | 1.51x | 7.62e-05 |
