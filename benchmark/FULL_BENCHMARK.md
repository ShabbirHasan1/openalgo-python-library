# OpenAlgo Indicators - Full Benchmark (NIFTY 50, 1-min)

- Dataset: `NIFTY 50.csv` - **5,000 bars** (OHLC real; volume synthesized, index feed has volume=0).
- **New (Rust)**: current `ta.*` backend (openalgo._oaindicators).
- **Old (OpenAlgo)**: original kernels run INTERPRETED. numba does not import on this Python 3.14 / numpy 2.x env (the reason for the migration), so this is a conservative lower bound on the old JIT speed - real numba would be faster, so true speedups are smaller.
- **TA-Lib**: shown where a comparable function exists (C implementation).
- Times are best-of-3 (New, TA-Lib) / single-run (Old, since interpreted is slow), in ms.
- `Speedup` = Old / New. `max|d|` = max abs difference New vs Old (accuracy).

| Indicator | New Rust (ms) | Old OpenAlgo (ms) | TA-Lib (ms) | Speedup (Old/New) | max&#124;d&#124; New-vs-Old |
|-----------|--------------:|------------------:|------------:|------------------:|---------------------:|
| **[Trend]** | | | | | |
| sma(20) | 0.01 | 1.0 | 0.01 | 83.7x | 0.0e+00 |
| ema(20) | 0.01 | 1.0 | 0.01 | 114.3x | 0.0e+00 |
| wma(20) | 0.06 | 14.1 | 0.01 | 226.8x | 0.0e+00 |
| dema(20) | 0.02 | - | 0.02 | - | - |
| tema(20) | 0.04 | - | 0.03 | - | - |
| trima(20) | 31.12 | 31.2 | 0.01 | 1.0x | 0.0e+00 |
| hma(20) | 0.12 | - | - | - | - |
| vwma(20) | 0.01 | 2.4 | - | 215.6x | 0.0e+00 |
| alma(21) | 0.03 | 16.6 | - | 563.7x | 5.5e-12 |
| kama(14) | 0.03 | 18.5 | 0.01 | 531.3x | 0.0e+00 |
| zlema(20) | 0.01 | 1.9 | - | 134.6x | 0.0e+00 |
| t3(21) | 0.05 | - | 0.01 | - | - |
| mcginley(14) | 0.04 | 2.5 | - | 62.6x | 0.0e+00 |
| vidya(14) | 0.27 | 20.5 | - | 75.7x | 0.0e+00 |
| supertrend(10,3) | 0.05 | 7.2 | - | 143.7x | 0.0e+00 |
| ichimoku | 0.25 | 14.9 | - | 58.9x | 0.0e+00 |
| frama(26) | 0.23 | 64.4 | - | 282.2x | 0.0e+00 |
| ckstop | 0.08 | 45.9 | - | 559.3x | 0.0e+00 |
| **[Momentum]** | | | | | |
| rsi(14) | 0.02 | 2.7 | 0.02 | 120.0x | 0.0e+00 |
| macd | 0.02 | 3.1 | 0.03 | 126.4x | 0.0e+00 |
| stochastic | 0.08 | 8.9 | 0.03 | 106.2x | 0.0e+00 |
| cci(20) | 0.06 | 16.6 | 0.10 | 299.3x | 0.0e+00 |
| williams_r(14) | 0.07 | - | 0.03 | - | - |
| bop | 0.01 | 1.7 | 0.01 | 138.5x | 0.0e+00 |
| elderray(13) | 0.02 | - | - | - | - |
| fisher(9) | 0.06 | - | - | - | - |
| crsi | 0.15 | - | - | - | - |
| **[Volatility]** | | | | | |
| atr(14) | 0.03 | 3.1 | 0.02 | 116.3x | 0.0e+00 |
| natr(14) | 0.03 | - | 0.02 | - | - |
| bbands(20) | 0.03 | 0.0 | 0.02 | 1.0x | 0.0e+00 |
| keltner | 0.04 | 8.6 | - | 207.5x | 0.0e+00 |
| donchian(20) | 0.08 | - | - | - | - |
| chaikin | 0.02 | - | - | - | - |
| trange | 0.01 | 2.0 | 0.00 | 280.7x | 0.0e+00 |
| ultosc | 0.10 | 52.8 | 0.03 | 531.2x | 0.0e+00 |
| massindex | 0.04 | - | - | - | - |
| bbpercent(20) | 0.13 | - | - | - | - |
| bbwidth(20) | 0.12 | - | - | - | - |
| chandelier_exit | 0.11 | - | - | - | - |
| hv | 0.08 | - | - | - | - |
| ulcerindex | 0.05 | - | - | - | - |
| starc | 0.04 | - | - | - | - |
| **[Volume]** | | | | | |
| obv | 0.02 | 1.3 | 0.01 | 83.6x | 0.0e+00 |
| vwap | 0.03 | - | - | - | - |
| mfi(14) | 0.03 | 3.6 | 0.02 | 111.0x | 0.0e+00 |
| adl | 0.01 | 3.1 | 0.01 | 260.1x | 0.0e+00 |
| cmf(20) | 0.11 | 63.3 | - | 589.1x | 0.0e+00 |
| emv | 0.03 | - | - | - | - |
| force_index(13) | 0.03 | - | - | - | - |
| nvi | 0.03 | - | - | - | - |
| pvi | 0.03 | - | - | - | - |
| volosc | 0.05 | - | - | - | - |
| vroc(25) | 0.02 | 1.5 | - | 80.9x | 0.0e+00 |
| kvo | 0.04 | - | - | - | - |
| pvt | 0.03 | 2.1 | - | 62.6x | 0.0e+00 |
| rvol(20) | 0.04 | 8.5 | - | 197.7x | 0.0e+00 |
| **[Oscillators]** | | | | | |
| roc(12) | 1.44 | 1.5 | 0.01 | 1.0x | 0.0e+00 |
| cmo(14) | 0.02 | 10.9 | 0.02 | 513.4x | 1.4e-14 |
| trix(18) | 0.04 | - | 0.03 | - | - |
| awesome_osc | 0.07 | - | - | - | - |
| accel_osc | 0.08 | - | - | - | - |
| ppo | 0.04 | - | 0.02 | - | - |
| po | 0.05 | - | - | - | - |
| dpo(21) | 3.56 | - | - | - | - |
| aroonosc(14) | 15.14 | 15.2 | 0.03 | 1.0x | 0.0e+00 |
| stochrsi | 43.22 | - | - | - | - |
| rvi_osc | 62.81 | - | - | - | - |
| cho | 0.06 | - | 0.01 | - | - |
| chop(14) | 0.12 | - | - | - | - |
| kst | 0.15 | - | - | - | - |
| tsi | 0.05 | - | - | - | - |
| vi(14) | 0.06 | - | - | - | - |
| gator | 0.10 | - | - | - | - |
| stc | 35.26 | - | - | - | - |
| coppock | 40.10 | - | - | - | - |
| **[Statistics]** | | | | | |
| linreg(14) | 0.05 | 40.4 | 0.04 | 828.8x | 1.3e-11 |
| lrslope(100) | 0.69 | - | 0.27 | - | - |
| correlation(20) | 0.11 | 61.4 | 0.03 | 539.1x | 1.2e-15 |
| beta(60) | 0.32 | 104.5 | 0.02 | 328.0x | 0.0e+00 |
| variance(20) | 8.46 | - | 0.01 | - | - |
| tsf(14) | 0.05 | 39.8 | 0.04 | 806.5x | 1.5e-11 |
| median(3) | 37.10 | 5.6 | - | 0.2x | 0.0e+00 |
| mode(20) | 48.20 | - | - | - | - |
| **[Hybrid]** | | | | | |
| adx(14) | 6.58 | 27.2 | 0.03 | 4.1x | 0.0e+00 |
| aroon(14) | 16.90 | 16.5 | 0.02 | 1.0x | 0.0e+00 |
| pivot_points | 0.03 | 7.1 | - | 230.4x | 0.0e+00 |
| psar | 0.03 | 3.1 | 0.01 | 95.6x | 0.0e+00 |
| dmi(14) | 6.59 | - | - | - | - |
| fractals | 17.84 | - | - | - | - |
| rwi(14) | 2.56 | 24.4 | - | 9.5x | 0.0e+00 |
