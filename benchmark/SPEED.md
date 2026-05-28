# OpenAlgo Indicators - Rust Core Speed Benchmark

Rust = current `ta.*` backend (openalgo._oaindicators). Py-ref = the original kernels run interpreted (numba removed). Speedup = Py-ref / Rust. TA-Lib shown where a comparable function exists.

TA-Lib available: True

### RELIANCE daily (real) (7629 bars)

| indicator | Rust (ms) | Py-ref (ms) | speedup | TA-Lib (ms) |
|-----------|----------:|------------:|--------:|------------:|
| sma(20) | 0.010 | 1.496 | 151.1x | 0.010 |
| ema(20) | 0.010 | 1.641 | 170.9x | 0.015 |
| wma(20) | 0.093 | 21.418 | 229.8x | 0.010 |
| rsi(14) | 0.031 | 4.092 | 131.2x | 0.030 |
| macd | 0.032 | 4.872 | 150.8x | 0.045 |
| bbands(20) | 0.038 | 0.038 | 1.0x | 0.033 |
| atr(14) | 0.033 | 4.694 | 144.0x | 0.034 |
| stochastic | 0.116 | 13.236 | 113.9x | 0.042 |
| supertrend | 0.058 | 10.670 | 182.4x | - |
| adx(14) | 10.199 | 40.519 | 4.0x | 0.049 |
| sar | 0.040 | 4.593 | 114.2x | 0.015 |
| linreg(14) | 59.747 | 63.157 | 1.1x | 0.066 |

### Synthetic 100k (100000 bars)

| indicator | Rust (ms) | Py-ref (ms) | speedup | TA-Lib (ms) |
|-----------|----------:|------------:|--------:|------------:|
| sma(20) | 0.123 | 19.953 | 162.2x | 0.114 |
| ema(20) | 0.119 | 21.629 | 181.1x | 0.171 |
| wma(20) | 1.200 | 289.153 | 240.9x | 0.117 |
| rsi(14) | 0.399 | 53.448 | 134.1x | 0.473 |
| macd | 0.800 | 65.675 | 82.1x | 0.839 |
| bbands(20) | 0.888 | 0.979 | 1.1x | 0.562 |
| atr(14) | 0.573 | 62.284 | 108.8x | 0.622 |
| stochastic | 2.432 | 178.140 | 73.2x | 1.266 |
| supertrend | 1.690 | 145.007 | 85.8x | - |
| adx(14) | 137.593 | 533.102 | 3.9x | 0.902 |
| sar | 1.034 | 59.027 | 57.1x | 0.413 |
| linreg(14) | 791.936 | 784.265 | 1.0x | 0.844 |
