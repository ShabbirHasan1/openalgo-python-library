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
| t3(21) | 21.13 | 2.45 | 0.12x | 3.38e-02 |
| avgprice | 9.73 | 1.68 | 0.17x | 7.28e-12 |
| wclprice | 6.80 | 1.24 | 0.18x | 0.00e+00 |
| adx(14) | 41.98 | 7.92 | 0.19x | 9.81e+01 |
| adosc | 10.79 | 2.30 | 0.21x | 0.00e+00 |
| midprice(14) | 20.34 | 4.53 | 0.22x | 0.00e+00 |
| apo | 14.37 | 3.22 | 0.22x | 8.84e-10 |
| correl(20) | 24.65 | 5.60 | 0.23x | 2.72e+00 |
| typprice | 5.80 | 1.37 | 0.24x | 0.00e+00 |
| bop | 5.48 | 1.43 | 0.26x | 0.00e+00 |
| variance(20) | 8.17 | 2.16 | 0.26x | 1.11e+04 |
| adl | 6.85 | 1.95 | 0.28x | 1.46e+03 |
| medprice | 3.65 | 1.04 | 0.29x | 0.00e+00 |
| kama(14) | 7.72 | 2.24 | 0.29x | 1.64e+00 |
| ppo | 12.42 | 3.81 | 0.31x | 2.42e+00 |
| rocp(10) | 5.02 | 1.64 | 0.33x | 0.00e+00 |
| rocr(10) | 3.39 | 1.30 | 0.38x | 0.00e+00 |
| mom(10) | 2.92 | 1.12 | 0.38x | 0.00e+00 |
| psar | 11.28 | 4.37 | 0.39x | 2.73e+02 |
| trima(100) | 5.17 | 2.03 | 0.39x | 2.78e-09 |
| williams_r(14) | 21.31 | 8.41 | 0.39x | 5.00e+01 |
| trima(20) | 5.05 | 1.99 | 0.39x | 1.15e-09 |
| aroonosc(14) | 19.47 | 7.71 | 0.40x | 1.00e+02 |
| trange | 3.94 | 1.63 | 0.41x | 0.00e+00 |
| tema(20) | 14.70 | 6.98 | 0.47x | 5.01e-02 |
| stochf | 23.17 | 11.05 | 0.48x | 2.84e-14 |
| cmo(14) | 10.70 | 5.11 | 0.48x | 1.47e+02 |
| stochastic | 24.49 | 12.04 | 0.49x | 1.00e+02 |
| aroon(14) | 18.45 | 9.11 | 0.49x | 1.00e+02 |
| natr(14) | 11.06 | 5.77 | 0.52x | 3.16e-03 |
| wma(20) | 3.19 | 1.68 | 0.53x | 5.14e-09 |
| mfi(14) | 13.13 | 7.06 | 0.54x | 3.75e+02 |
| beta(60) | 9.18 | 5.09 | 0.55x | 2.31e+00 |
| trix(18) | 12.93 | 7.17 | 0.55x | 3.12e+01 |
| sma(20) | 2.84 | 1.59 | 0.56x | 6.44e-10 |
| bbands(20) | 12.48 | 7.12 | 0.57x | 4.88e-04 |
| atr(14) | 9.70 | 5.78 | 0.60x | 2.73e-01 |
| dema(20) | 7.34 | 4.93 | 0.67x | 8.58e-01 |
| stochrsi | 22.91 | 15.50 | 0.68x | 1.00e+02 |
| midpoint(14) | 20.12 | 13.68 | 0.68x | 0.00e+00 |
| minus_dm(14) | 6.26 | 4.36 | 0.70x | 0.00e+00 |
| plus_dm(14) | 6.41 | 4.48 | 0.70x | 0.00e+00 |
| obv | 5.23 | 3.72 | 0.71x | 4.08e+04 |
| adxr(14) | 12.10 | 8.64 | 0.71x | 4.26e-14 |
| roc(12) | 1.71 | 1.25 | 0.73x | 1.15e-14 |
| ultosc | 9.35 | 7.60 | 0.81x | 1.42e-14 |
| dx(14) | 8.91 | 7.25 | 0.81x | 5.68e-14 |
| ema(20) | 2.34 | 1.99 | 0.85x | 1.67e+00 |
| rsi(14) | 5.64 | 4.91 | 0.87x | 2.84e-14 |
| stddev(20) | 3.35 | 3.89 | 1.16x | 2.44e-04 |
| macd | 7.50 | 8.74 | 1.17x | 1.18e+00 |
| linreg(14) | 8.09 | 9.64 | 1.19x | 6.61e-05 |
| cci(20) | 14.11 | 17.49 | 1.24x | 1.33e+02 |
| linregintercept(14) | 7.39 | 9.21 | 1.25x | 6.61e-05 |
| linregangle(14) | 12.11 | 16.91 | 1.40x | 5.82e-04 |
| tsf(14) | 6.43 | 9.45 | 1.47x | 7.62e-05 |
