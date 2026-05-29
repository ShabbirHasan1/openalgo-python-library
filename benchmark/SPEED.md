# OpenAlgo Indicators - Rust Core Speed Benchmark

Rust = current `ta.*` backend (openalgo._oaindicators). Py-ref = the original kernels run interpreted (numba removed). Speedup = Py-ref / Rust. TA-Lib shown where a comparable function exists.

TA-Lib available: True

### RELIANCE daily (real) (7629 bars)

| indicator | Rust (ms) | Py-ref (ms) | speedup | TA-Lib (ms) |
|-----------|----------:|------------:|--------:|------------:|
| sma(20) | 0.010 | 1.581 | 158.1x | 0.010 |
| ema(20) | 0.010 | 1.718 | 179.0x | 0.015 |
| wma(20) | 0.093 | 22.468 | 240.6x | 0.010 |
| rsi(14) | 0.031 | 4.092 | 130.7x | 0.030 |
| macd | 0.032 | 5.091 | 157.6x | 0.045 |
| bbands(20) | 0.037 | 0.038 | 1.0x | 0.033 |
| atr(14) | 0.033 | 5.245 | 160.4x | 0.034 |
| stochastic | 0.108 | 15.091 | 140.1x | 0.042 |
| supertrend | 0.061 | 12.584 | 206.6x | - |
| adx(14) | 0.199 | 41.259 | 207.4x | 0.049 |
| sar | 0.040 | 5.154 | 128.2x | 0.015 |
| linreg(14) | 0.068 | 59.965 | 887.1x | 0.066 |

### Synthetic 100k (100000 bars)

| indicator | Rust (ms) | Py-ref (ms) | speedup | TA-Lib (ms) |
|-----------|----------:|------------:|--------:|------------:|
| sma(20) | 0.123 | 20.925 | 170.0x | 0.116 |
| ema(20) | 0.121 | 22.447 | 185.1x | 0.173 |
| wma(20) | 1.194 | 299.451 | 250.8x | 0.128 |
| rsi(14) | 0.406 | 53.783 | 132.4x | 0.473 |
| macd | 0.782 | 68.969 | 88.2x | 0.871 |
| bbands(20) | 0.939 | 0.980 | 1.0x | 0.571 |
| atr(14) | 0.643 | 70.942 | 110.2x | 0.562 |
| stochastic | 2.421 | 199.702 | 82.5x | 1.284 |
| supertrend | 1.744 | 168.702 | 96.7x | - |
| adx(14) | 3.733 | 544.574 | 145.9x | 0.775 |
| sar | 0.991 | 66.380 | 67.0x | 0.411 |
| linreg(14) | 0.874 | 787.907 | 901.7x | 0.847 |
