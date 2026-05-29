# OpenAlgo Indicators - Full Benchmark (NIFTY 50, 1-min)

- Dataset: `NIFTY 50.csv` - **924,782 bars** (OHLC real; volume synthesized, index feed has volume=0).
- **New (Rust)**: current `ta.*` backend (openalgo._oaindicators).
- **Old (OpenAlgo)**: original kernels run INTERPRETED. numba does not import on this Python 3.14 / numpy 2.x env (the reason for the migration), so this is a conservative lower bound on the old JIT speed - real numba would be faster, so true speedups are smaller.
- **TA-Lib**: shown where a comparable function exists (C implementation).
- Times are best-of-3 (New, TA-Lib) / single-run (Old, since interpreted is slow), in ms.
- `Speedup` = Old / New. `max|d|` = max abs difference New vs Old (accuracy).

| Indicator | New Rust (ms) | Old OpenAlgo (ms) | TA-Lib (ms) | Speedup (Old/New) | max&#124;d&#124; New-vs-Old |
|-----------|--------------:|------------------:|------------:|------------------:|---------------------:|
| **[Trend]** | | | | | |
| sma(20) | 3.05 | 191.1 | 1.48 | 62.7x | 6.4e-10 |
| ema(20) | 2.19 | 189.5 | 1.88 | 86.6x | 0.0e+00 |
| wma(20) | 12.81 | 2542.4 | 1.63 | 198.4x | 0.0e+00 |
| dema(20) | 7.86 | - | 5.03 | - | - |
| tema(20) | 14.43 | - | 7.04 | - | - |
| trima(20) | 33.63 | 5746.9 | 1.91 | 170.9x | 1.1e-11 |
| hma(20) | 27.99 | - | - | - | - |
| vwma(20) | 3.82 | 447.5 | - | 117.1x | 0.0e+00 |
| alma(21) | 9.38 | 3056.8 | - | 325.8x | 1.8e-11 |
| kama(14) | 7.33 | 3419.0 | 2.19 | 466.7x | 7.3e-12 |
| zlema(20) | 5.38 | 353.2 | - | 65.7x | 0.0e+00 |
| t3(21) | 19.95 | - | 2.36 | - | - |
| mcginley(14) | 9.20 | 437.3 | - | 47.5x | 3.6e-12 |
| vidya(14) | 54.38 | 3623.9 | - | 66.6x | 0.0e+00 |
| supertrend(10,3) | 20.63 | 1299.5 | - | 63.0x | 0.0e+00 |
| ichimoku | 70.44 | 3014.2 | - | 42.8x | 0.0e+00 |
| frama(26) | 45.59 | 11930.8 | - | 261.7x | 0.0e+00 |
| ckstop | 22.73 | 8647.2 | - | 380.5x | 0.0e+00 |
| **[Momentum]** | | | | | |
| rsi(14) | 6.01 | 479.5 | 4.74 | 79.7x | 0.0e+00 |
| macd | 7.34 | 572.0 | 8.72 | 77.9x | 0.0e+00 |
| stochastic | 26.65 | 1610.9 | 11.56 | 60.4x | 0.0e+00 |
| cci(20) | 13.49 | 3100.2 | 17.13 | 229.9x | 0.0e+00 |
| williams_r(14) | 22.84 | - | 7.67 | - | - |
| bop | 5.84 | 301.7 | 1.44 | 51.6x | 0.0e+00 |
| elderray(13) | 6.64 | - | - | - | - |
| fisher(9) | 15.52 | - | - | - | - |
| crsi | 37.17 | - | - | - | - |
| **[Volatility]** | | | | | |
| atr(14) | 8.06 | 579.7 | 5.03 | 72.0x | 0.0e+00 |
| natr(14) | 9.66 | - | 5.06 | - | - |
| bbands(20) | 10.72 | 10.0 | 5.19 | 0.9x | 0.0e+00 |
| keltner | 14.58 | 1597.1 | - | 109.5x | 0.0e+00 |
| donchian(20) | 22.22 | - | - | - | - |
| chaikin | 7.13 | - | - | - | - |
| trange | 4.15 | 377.2 | 1.22 | 90.8x | 0.0e+00 |
| ultosc | 37.68 | 9964.8 | 7.56 | 264.5x | 0.0e+00 |
| massindex | 12.25 | - | - | - | - |
| bbpercent(20) | 30.97 | - | - | - | - |
| bbwidth(20) | 29.72 | - | - | - | - |
| chandelier_exit | 33.67 | - | - | - | - |
| hv | 21.03 | - | - | - | - |
| ulcerindex | 20.13 | - | - | - | - |
| starc | 15.20 | - | - | - | - |
| **[Volume]** | | | | | |
| obv | 4.58 | 236.4 | 3.43 | 51.6x | 0.0e+00 |
| vwap | 14.58 | - | - | - | - |
| mfi(14) | 12.73 | 650.2 | 7.00 | 51.1x | 0.0e+00 |
| adl | 5.56 | 550.2 | 1.46 | 99.0x | 0.0e+00 |
| cmf(20) | 23.26 | 11767.7 | - | 505.9x | 0.0e+00 |
| emv | 8.80 | - | - | - | - |
| force_index(13) | 10.67 | - | - | - | - |
| nvi | 10.49 | - | - | - | - |
| pvi | 10.32 | - | - | - | - |
| volosc | 15.28 | - | - | - | - |
| vroc(25) | 8.21 | 269.2 | - | 32.8x | 0.0e+00 |
| kvo | 18.77 | - | - | - | - |
| pvt | 11.77 | 362.6 | - | 30.8x | 0.0e+00 |
| rvol(20) | 10.28 | 1529.1 | - | 148.7x | 0.0e+00 |
| **[Oscillators]** | | | | | |
| roc(12) | 1.66 | 269.5 | 1.27 | 162.8x | 0.0e+00 |
| cmo(14) | 10.57 | 1865.9 | 4.87 | 176.5x | 1.4e-14 |
| trix(18) | 11.46 | - | 6.61 | - | - |
| awesome_osc | 17.41 | - | - | - | - |
| accel_osc | 20.85 | - | - | - | - |
| ppo | 12.28 | - | 3.77 | - | - |
| po | 11.38 | - | - | - | - |
| dpo(21) | 10.35 | - | - | - | - |
| aroonosc(14) | 49.62 | 2864.6 | 7.53 | 57.7x | 0.0e+00 |
| stochrsi | 20.32 | - | - | - | - |
| rvi_osc | 17.83 | - | - | - | - |
| cho | 20.57 | - | 1.77 | - | - |
| chop(14) | 38.19 | - | - | - | - |
| kst | 56.40 | - | - | - | - |
| tsi | 16.53 | - | - | - | - |
| vi(14) | 26.88 | - | - | - | - |
| gator | 34.62 | - | - | - | - |
| stc | 23.01 | - | - | - | - |
| coppock | 17.09 | - | - | - | - |
| **[Statistics]** | | | | | |
| linreg(14) | 10.21 | 7392.7 | 9.02 | 724.2x | 3.3e-11 |
| lrslope(100) | 136.15 | - | 52.20 | - | - |
| correlation(20) | 24.30 | 11333.2 | 5.51 | 466.4x | 1.0e+00 |
| beta(60) | 67.20 | 19821.8 | 4.57 | 295.0x | 0.0e+00 |
| variance(20) | 7.14 | - | 2.15 | - | - |
| tsf(14) | 10.84 | 7344.2 | 8.77 | 677.5x | 3.6e-11 |
| median(3) | 10.55 | 1018.0 | - | 96.5x | 0.0e+00 |
| mode(20) | 99.13 | - | - | - | - |
| **[Hybrid]** | | | | | |
| adx(14) | 37.93 | 4840.3 | 7.62 | 127.6x | 0.0e+00 |
| aroon(14) | 48.91 | 3028.2 | 8.02 | 61.9x | 0.0e+00 |
| pivot_points | 21.55 | 1443.3 | - | 67.0x | 0.0e+00 |
| psar | 10.31 | 551.7 | 4.16 | 53.5x | 0.0e+00 |
| dmi(14) | 38.60 | - | - | - | - |
| fractals | 17.05 | - | - | - | - |
| rwi(14) | 13.43 | 4357.5 | - | 324.5x | 0.0e+00 |
