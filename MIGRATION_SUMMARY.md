# OpenAlgo Indicators: numba -> Rust+PyO3 Migration Summary

Branch: `rust-indicators-migration` (local commits only; nothing pushed).

## What changed
- The ~90 technical indicators in `openalgo/indicators/` now compute on a **Rust core**
  (`openalgo._oaindicators`, built with PyO3) reached through a single seam,
  `openalgo/indicators/_backend.py`. The public API is unchanged: `from openalgo import ta`
  and every indicator name, parameter, default, return shape and NaN placement are identical.
- **`numba` and `llvmlite` are no longer dependencies.** `openalgo/numba_shim.py` is now a
  pure no-op shim (legacy `@jit`/`@njit` decorators are passthroughs); the import-time
  numba warm-up and monkey-patch were removed. `import openalgo` works with numba never loaded.
- The legacy `pip install openalgo[indicators]` extra is removed; indicators are built in.

## Dependency: before / after
- Before: `numpy, pandas, httpx, websocket-client` + optional `numba>=0.63` (which pulls
  `llvmlite`). On Python 3.14 / numpy 2.x the numba stack failed to import (`np.trapz`),
  breaking `import openalgo` entirely.
- After: `numpy, pandas, httpx, websocket-client` only. Indicator math is a compiled
  Rust extension shipped in the wheel. No LLVM toolchain required to install or run.

## Architecture
```
rust/
  Cargo.toml            workspace (oa_core, oa_py)
  oa_core/              zero-dependency Rust kernels (cargo test: 33 passing)
  oa_py/                PyO3 cdylib -> openalgo._oaindicators (pyo3 0.22, numpy 0.22, abi3-py39)
openalgo/indicators/
  _backend.py           Rust-backed kernels + pure-numpy fallbacks (no numba in either path)
  trend/momentum/volatility/volume/oscillators/statistics/hybrid.py  -> route to _backend
benchmark/              fetch_data.py + 9 parity suites + ci_smoke.py + speed_bench.py
```
Most indicators are pure-Rust kernels. A few (per-window regression/median/mode and some
windowed-mean composites) stay in numpy inside `_backend.py` for exact bit-parity with the
original `np.mean`/`np.sum` semantics; they are numba-free.

## Parity (correctness)
Verified on real RELIANCE & SBIN daily + 1m data (yfinance) and against TA-Lib where the
definitions align. Reference = the original kernels run interpreted.
- 9 parity suites all green: `parity, wrapper_parity, trend_parity, momentum_parity,
  volatility_parity, volume_parity, oscillator_parity, statistics_parity, hybrid_parity`.
- The vast majority of kernels are **bit-exact (max diff 0.0)**. Recursive/transcendental
  ones (KAMA, ALMA, McGinley) differ by ~1e-13 absolute (<= 1e-12 relative target).
  TA-Lib differs only by documented seeding conventions for EMA/ATR/MACD/CMO.
- A key FP detail learned and applied: match Python's exact float association
  (`acc = acc + new - old`, `100*(a/b)`, thread the seed through `cumprod`).

## Speed (see benchmark/SPEED.md)
Rust vs the interpreted-Python reference (numba removed) on real + synthetic data:
common indicators are ~**50x-240x** faster (sma/ema/wma/rsi/macd/atr/stochastic/
supertrend/sar). Per-window numpy stats (linreg/adx/bbands-composite) are numpy-speed.
Rust timings are on par with TA-Lib for the pure kernels.

## Build
```
# local dev
cd rust && PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 cargo build --release -p oa_py
cp rust/target/release/_oaindicators.dll openalgo/_oaindicators.pyd   # .so/.dylib on unix
# wheel
PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 maturin build --release
```
`pyproject.toml` uses the maturin backend (python-source=".",
module-name="openalgo._oaindicators", manifest-path="rust/oa_py/Cargo.toml").

## CI/CD (.github/workflows/CI.yml)
cargo test (oa_core) -> Linux wheel smoke test -> abi3 wheels for linux x86_64/aarch64
(manylinux_2_28), macOS x86_64/arm64, windows -> sdist -> publish to PyPI on `v*` tags via
OIDC trusted publishing. Mirrors the opengreeks pipeline.

## Known follow-ups
- Real-data benchmarking currently uses yfinance because the OpenAlgo DuckDB/Historify
  store is empty and the Dhan market-data API is unsubscribed/under maintenance. Re-run
  `benchmark/fetch_data.py` (auto-prefers source="db"/"api") once that is available.
- The dead legacy `_calculate_*` numba staticmethods are retained as interpreted parity
  references; an optional tidy pass can delete them (and `setup.py`/`setup.cfg`, now
  superseded by `pyproject.toml`) and freeze parity to saved golden arrays.
