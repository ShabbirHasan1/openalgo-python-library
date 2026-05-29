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
| t3(21) | 14.76 | 2.46 | 0.17x | 3.38e-02 |
| avgprice | 8.14 | 1.49 | 0.18x | 7.28e-12 |
| wclprice | 7.24 | 1.41 | 0.19x | 0.00e+00 |
| adosc | 9.22 | 1.97 | 0.21x | 0.00e+00 |
| midprice(14) | 19.76 | 4.52 | 0.23x | 0.00e+00 |
| apo | 16.06 | 3.70 | 0.23x | 8.84e-10 |
| typprice | 6.45 | 1.51 | 0.23x | 0.00e+00 |
| correl(20) | 24.56 | 6.00 | 0.24x | 2.72e+00 |
| adl | 5.82 | 1.52 | 0.26x | 1.46e+03 |
| bop | 6.02 | 1.69 | 0.28x | 0.00e+00 |
| variance(20) | 7.75 | 2.24 | 0.29x | 1.11e+04 |
| rocp(10) | 5.12 | 1.53 | 0.30x | 0.00e+00 |
| ppo | 13.66 | 4.25 | 0.31x | 2.42e+00 |
| kama(14) | 7.63 | 2.41 | 0.32x | 1.64e+00 |
| medprice | 3.97 | 1.27 | 0.32x | 0.00e+00 |
| williams_r(14) | 22.13 | 7.86 | 0.36x | 5.00e+01 |
| psar | 11.24 | 4.17 | 0.37x | 2.73e+02 |
| trima(20) | 5.14 | 1.97 | 0.38x | 1.15e-09 |
| trima(100) | 5.28 | 2.04 | 0.39x | 2.78e-09 |
| mom(10) | 3.76 | 1.46 | 0.39x | 0.00e+00 |
| aroonosc(14) | 19.29 | 7.83 | 0.41x | 1.00e+02 |
| tema(20) | 17.14 | 7.12 | 0.42x | 5.01e-02 |
| adx(14) | 19.13 | 8.06 | 0.42x | 9.81e+01 |
| cmo(14) | 10.97 | 4.83 | 0.44x | 1.47e+02 |
| trange | 3.80 | 1.69 | 0.44x | 0.00e+00 |
| aroon(14) | 18.87 | 8.41 | 0.45x | 1.00e+02 |
| stochf | 24.02 | 10.73 | 0.45x | 2.84e-14 |
| rocr(10) | 3.66 | 1.65 | 0.45x | 0.00e+00 |
| mfi(14) | 14.85 | 6.79 | 0.46x | 3.75e+02 |
| stochastic | 25.86 | 11.90 | 0.46x | 1.00e+02 |
| bbands(20) | 14.46 | 6.88 | 0.48x | 4.88e-04 |
| natr(14) | 11.41 | 5.63 | 0.49x | 3.16e-03 |
| sma(20) | 3.11 | 1.54 | 0.49x | 6.44e-10 |
| beta(60) | 8.59 | 4.58 | 0.53x | 2.31e+00 |
| trix(18) | 12.17 | 6.66 | 0.55x | 3.12e+01 |
| wma(20) | 2.88 | 1.67 | 0.58x | 5.14e-09 |
| atr(14) | 8.71 | 5.19 | 0.60x | 2.73e-01 |
| adxr(14) | 14.33 | 9.24 | 0.65x | 4.26e-14 |
| minus_dm(14) | 6.59 | 4.36 | 0.66x | 0.00e+00 |
| stochrsi | 23.56 | 16.16 | 0.69x | 1.00e+02 |
| plus_dm(14) | 6.48 | 4.48 | 0.69x | 0.00e+00 |
| dema(20) | 7.48 | 5.38 | 0.72x | 8.58e-01 |
| obv | 5.02 | 3.64 | 0.73x | 4.08e+04 |
| dx(14) | 9.94 | 7.27 | 0.73x | 5.68e-14 |
| midpoint(14) | 18.97 | 14.26 | 0.75x | 0.00e+00 |
| ultosc | 8.68 | 6.84 | 0.79x | 1.42e-14 |
| ema(20) | 2.38 | 1.94 | 0.81x | 1.67e+00 |
| roc(12) | 1.96 | 1.63 | 0.83x | 1.15e-14 |
| rsi(14) | 5.55 | 4.83 | 0.87x | 2.84e-14 |
| stddev(20) | 3.68 | 3.84 | 1.04x | 2.44e-04 |
| linreg(14) | 7.85 | 9.21 | 1.17x | 6.61e-05 |
| tsf(14) | 7.73 | 9.46 | 1.22x | 7.62e-05 |
| macd | 8.25 | 10.39 | 1.26x | 1.18e+00 |
| cci(20) | 13.53 | 17.29 | 1.28x | 1.33e+02 |
| linregintercept(14) | 6.07 | 8.86 | 1.46x | 6.61e-05 |
| linregangle(14) | 11.46 | 17.18 | 1.50x | 5.82e-04 |
