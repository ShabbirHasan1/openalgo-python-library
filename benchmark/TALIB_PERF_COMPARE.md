# OpenAlgo vs TA-Lib - Performance Comparison

- Dataset: `NIFTY 50.csv` - **924,782 bars**. Best-of-5 timings.
- **New (ms)** = OpenAlgo `ta.*` (Rust core). **TA-Lib (ms)** = C implementation.
- **Speed (TA-Lib/New)**: >1.0 = OpenAlgo faster; <1.0 = TA-Lib faster (target).
- **max|d|** = max abs difference OpenAlgo vs TA-Lib (intentional TradingView-
  convention differences inflate this for ema/adx/atr/macd/stoch/cci etc.; see
  TALIB_COMPATIBILITY.md).
- NOTE on `correl`: TA-Lib's CORREL uses an unstable one-pass sum-of-squares and
  returns values OUTSIDE [-1,1] in near-constant windows (observed 2.72 here).
  OpenAlgo keeps a numerically stable per-window two-pass (O(n*period)) that stays
  in [-1,1] - it is intentionally NOT converted to rolling moments, which were
  measured to drift up to ~1.0 on this trending price data. OpenAlgo is the more
  correct of the two; the speed gap is the price of correctness.
- Summary: **7 at/faster than TA-Lib**, 49 slower (sorted slowest-first).

| Indicator | New (ms) | TA-Lib (ms) | Speed (TA-Lib/New) | max&#124;d&#124; |
|-----------|---------:|------------:|-------------------:|---------:|
| adosc | 21.80 | 2.18 | 0.10x | 0.00e+00 |
| t3(21) | 21.91 | 2.53 | 0.12x | 3.38e-02 |
| wclprice | 7.86 | 1.33 | 0.17x | 0.00e+00 |
| avgprice | 8.62 | 1.49 | 0.17x | 7.28e-12 |
| ultosc | 40.35 | 7.57 | 0.19x | 1.42e-14 |
| adx(14) | 39.66 | 7.72 | 0.19x | 9.81e+01 |
| apo | 17.69 | 3.88 | 0.22x | 8.84e-10 |
| correl(20) | 24.70 | 5.60 | 0.23x | 2.72e+00 |
| midprice(14) | 20.29 | 4.93 | 0.24x | 0.00e+00 |
| variance(20) | 8.27 | 2.15 | 0.26x | 1.11e+04 |
| typprice | 5.95 | 1.59 | 0.27x | 0.00e+00 |
| adl | 5.38 | 1.46 | 0.27x | 1.46e+03 |
| bop | 6.32 | 1.75 | 0.28x | 0.00e+00 |
| trange | 5.11 | 1.42 | 0.28x | 0.00e+00 |
| rocp(10) | 5.32 | 1.58 | 0.30x | 0.00e+00 |
| kama(14) | 7.83 | 2.33 | 0.30x | 1.64e+00 |
| ppo | 13.15 | 3.97 | 0.30x | 2.42e+00 |
| medprice | 4.22 | 1.29 | 0.31x | 0.00e+00 |
| mom(10) | 3.48 | 1.15 | 0.33x | 0.00e+00 |
| williams_r(14) | 20.98 | 7.85 | 0.37x | 5.00e+01 |
| aroonosc(14) | 19.91 | 7.54 | 0.38x | 1.00e+02 |
| trima(20) | 5.19 | 2.00 | 0.39x | 1.15e-09 |
| psar | 11.09 | 4.34 | 0.39x | 2.73e+02 |
| trima(100) | 4.94 | 2.01 | 0.41x | 2.78e-09 |
| rocr(10) | 3.66 | 1.56 | 0.43x | 0.00e+00 |
| cmo(14) | 10.77 | 4.92 | 0.46x | 1.47e+02 |
| tema(20) | 14.91 | 6.84 | 0.46x | 5.01e-02 |
| aroon(14) | 18.83 | 8.78 | 0.47x | 1.00e+02 |
| mfi(14) | 14.45 | 6.86 | 0.48x | 3.75e+02 |
| stochastic | 24.62 | 12.35 | 0.50x | 1.00e+02 |
| stochf | 22.26 | 11.18 | 0.50x | 2.84e-14 |
| natr(14) | 10.94 | 5.74 | 0.53x | 3.16e-03 |
| beta(60) | 8.68 | 4.66 | 0.54x | 2.31e+00 |
| sma(20) | 2.92 | 1.58 | 0.54x | 6.44e-10 |
| bbands(20) | 10.85 | 5.99 | 0.55x | 4.88e-04 |
| trix(18) | 12.13 | 7.07 | 0.58x | 3.12e+01 |
| wma(20) | 2.93 | 1.72 | 0.59x | 5.14e-09 |
| atr(14) | 8.79 | 5.64 | 0.64x | 2.73e-01 |
| plus_dm(14) | 6.68 | 4.37 | 0.66x | 0.00e+00 |
| dema(20) | 8.00 | 5.58 | 0.70x | 8.58e-01 |
| midpoint(14) | 19.73 | 13.90 | 0.70x | 0.00e+00 |
| stochrsi | 22.01 | 15.53 | 0.71x | 1.00e+02 |
| minus_dm(14) | 5.98 | 4.34 | 0.73x | 0.00e+00 |
| adxr(14) | 12.40 | 9.38 | 0.76x | 4.26e-14 |
| obv | 4.54 | 3.47 | 0.76x | 4.08e+04 |
| rsi(14) | 5.94 | 4.94 | 0.83x | 2.84e-14 |
| ema(20) | 2.39 | 2.00 | 0.84x | 1.67e+00 |
| dx(14) | 8.51 | 7.27 | 0.85x | 5.68e-14 |
| roc(12) | 1.74 | 1.55 | 0.89x | 1.15e-14 |
| stddev(20) | 3.48 | 3.79 | 1.09x | 2.44e-04 |
| macd | 7.94 | 8.79 | 1.11x | 1.18e+00 |
| cci(20) | 14.15 | 17.42 | 1.23x | 1.33e+02 |
| linreg(14) | 7.57 | 9.41 | 1.24x | 6.61e-05 |
| linregangle(14) | 11.77 | 16.10 | 1.37x | 5.82e-04 |
| linregintercept(14) | 6.82 | 9.44 | 1.38x | 6.61e-05 |
| tsf(14) | 6.04 | 8.91 | 1.47x | 7.62e-05 |
