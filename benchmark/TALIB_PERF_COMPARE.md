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
| beta(60) | 65.70 | 4.84 | 0.07x | 2.31e+00 |
| adosc | 19.79 | 1.87 | 0.09x | 0.00e+00 |
| t3(21) | 19.81 | 2.44 | 0.12x | 3.38e-02 |
| aroonosc(14) | 49.95 | 7.40 | 0.15x | 1.00e+02 |
| wclprice | 8.13 | 1.27 | 0.16x | 0.00e+00 |
| avgprice | 7.42 | 1.18 | 0.16x | 7.28e-12 |
| apo | 17.42 | 3.12 | 0.18x | 8.84e-10 |
| aroon(14) | 48.94 | 8.85 | 0.18x | 1.00e+02 |
| ultosc | 37.83 | 7.25 | 0.19x | 1.42e-14 |
| midprice(14) | 21.26 | 4.27 | 0.20x | 0.00e+00 |
| adx(14) | 37.87 | 7.65 | 0.20x | 9.81e+01 |
| typprice | 5.69 | 1.41 | 0.25x | 0.00e+00 |
| adl | 5.60 | 1.45 | 0.26x | 1.46e+03 |
| correl(20) | 25.26 | 6.65 | 0.26x | 2.72e+00 |
| medprice | 3.69 | 1.02 | 0.28x | 0.00e+00 |
| mom(10) | 3.32 | 0.92 | 0.28x | 0.00e+00 |
| kama(14) | 7.54 | 2.20 | 0.29x | 1.64e+00 |
| variance(20) | 7.31 | 2.13 | 0.29x | 1.11e+04 |
| bop | 5.47 | 1.67 | 0.30x | 0.00e+00 |
| rocp(10) | 4.18 | 1.39 | 0.33x | 0.00e+00 |
| ppo | 11.86 | 4.01 | 0.34x | 2.42e+00 |
| williams_r(14) | 23.08 | 8.21 | 0.36x | 5.00e+01 |
| trima(100) | 4.84 | 1.93 | 0.40x | 2.78e-09 |
| psar | 10.54 | 4.28 | 0.41x | 2.73e+02 |
| rocr(10) | 3.17 | 1.32 | 0.42x | 0.00e+00 |
| trima(20) | 4.67 | 1.96 | 0.42x | 1.15e-09 |
| trange | 3.67 | 1.55 | 0.42x | 0.00e+00 |
| stochastic | 26.22 | 11.54 | 0.44x | 1.00e+02 |
| tema(20) | 14.09 | 6.31 | 0.45x | 5.01e-02 |
| stochf | 22.85 | 10.53 | 0.46x | 2.84e-14 |
| cmo(14) | 10.36 | 4.95 | 0.48x | 1.47e+02 |
| bbands(20) | 10.94 | 5.75 | 0.53x | 4.88e-04 |
| sma(20) | 2.73 | 1.46 | 0.53x | 6.44e-10 |
| natr(14) | 10.00 | 5.37 | 0.54x | 3.16e-03 |
| mfi(14) | 12.52 | 6.80 | 0.54x | 3.75e+02 |
| wma(20) | 2.69 | 1.55 | 0.57x | 5.14e-09 |
| trix(18) | 11.30 | 6.73 | 0.60x | 3.12e+01 |
| midpoint(14) | 21.50 | 13.51 | 0.63x | 0.00e+00 |
| atr(14) | 8.40 | 5.28 | 0.63x | 2.73e-01 |
| adxr(14) | 12.37 | 8.36 | 0.68x | 4.26e-14 |
| dema(20) | 7.04 | 4.86 | 0.69x | 8.58e-01 |
| minus_dm(14) | 6.07 | 4.28 | 0.71x | 0.00e+00 |
| plus_dm(14) | 6.04 | 4.40 | 0.73x | 0.00e+00 |
| obv | 4.61 | 3.54 | 0.77x | 4.08e+04 |
| roc(12) | 1.90 | 1.50 | 0.79x | 1.15e-14 |
| stochrsi | 18.61 | 14.83 | 0.80x | 1.00e+02 |
| dx(14) | 8.87 | 7.23 | 0.82x | 5.68e-14 |
| ema(20) | 2.35 | 1.97 | 0.84x | 1.67e+00 |
| rsi(14) | 5.42 | 4.90 | 0.91x | 2.84e-14 |
| stddev(20) | 3.64 | 3.78 | 1.04x | 2.44e-04 |
| macd | 7.60 | 8.28 | 1.09x | 1.18e+00 |
| linreg(14) | 7.13 | 9.12 | 1.28x | 6.61e-05 |
| cci(20) | 13.54 | 17.49 | 1.29x | 1.33e+02 |
| linregintercept(14) | 6.91 | 9.64 | 1.39x | 6.61e-05 |
| tsf(14) | 6.50 | 9.22 | 1.42x | 7.62e-05 |
| linregangle(14) | 10.33 | 16.50 | 1.60x | 5.82e-04 |
