//! PyO3 bindings: expose the zero-dependency `oa_core` indicator kernels to Python
//! as the `openalgo._oaindicators` extension module. The Python indicator wrappers
//! call these in place of the legacy numba kernels, keeping the public `ta` API
//! byte-identical.
//!
//! All numeric kernels take/return contiguous float64 numpy arrays. The Python side
//! already passes C-contiguous float64 (via `validate_input`), so `as_slice` succeeds.

use numpy::{IntoPyArray, PyArray1, PyReadonlyArray1};
use pyo3::prelude::*;

/// f64 slice -> f64 numpy array, for a kernel taking (data, period).
macro_rules! wrap_period {
    ($name:ident, $core:path) => {
        #[pyfunction]
        fn $name<'py>(
            py: Python<'py>,
            data: PyReadonlyArray1<'py, f64>,
            period: usize,
        ) -> PyResult<Py<PyArray1<f64>>> {
            let out = $core(data.as_slice()?, period);
            Ok(out.into_pyarray_bound(py).unbind())
        }
    };
}

wrap_period!(sma, oa_core::sma);
wrap_period!(rolling_sum, oa_core::rolling_sum);
wrap_period!(rolling_variance, oa_core::rolling_variance);
wrap_period!(stdev, oa_core::stdev);
wrap_period!(ema, oa_core::ema);
wrap_period!(ema_wilder, oa_core::ema_wilder);
wrap_period!(highest, oa_core::highest);
wrap_period!(lowest, oa_core::lowest);
wrap_period!(change, oa_core::change);
wrap_period!(roc, oa_core::roc);
wrap_period!(cmo, oa_core::cmo);
wrap_period!(ulcer_index, oa_core::ulcer_index);

#[pyfunction]
fn true_range<'py>(
    py: Python<'py>,
    high: PyReadonlyArray1<'py, f64>,
    low: PyReadonlyArray1<'py, f64>,
    close: PyReadonlyArray1<'py, f64>,
) -> PyResult<Py<PyArray1<f64>>> {
    let out = oa_core::true_range(high.as_slice()?, low.as_slice()?, close.as_slice()?);
    Ok(out.into_pyarray_bound(py).unbind())
}

#[pyfunction]
fn atr_wilder<'py>(
    py: Python<'py>,
    high: PyReadonlyArray1<'py, f64>,
    low: PyReadonlyArray1<'py, f64>,
    close: PyReadonlyArray1<'py, f64>,
    period: usize,
) -> PyResult<Py<PyArray1<f64>>> {
    let out = oa_core::atr_wilder(high.as_slice()?, low.as_slice()?, close.as_slice()?, period);
    Ok(out.into_pyarray_bound(py).unbind())
}

#[pyfunction]
fn atr_sma<'py>(
    py: Python<'py>,
    high: PyReadonlyArray1<'py, f64>,
    low: PyReadonlyArray1<'py, f64>,
    close: PyReadonlyArray1<'py, f64>,
    period: usize,
) -> PyResult<Py<PyArray1<f64>>> {
    let out = oa_core::atr_sma(high.as_slice()?, low.as_slice()?, close.as_slice()?, period);
    Ok(out.into_pyarray_bound(py).unbind())
}

#[pyfunction]
fn vwma<'py>(
    py: Python<'py>,
    data: PyReadonlyArray1<'py, f64>,
    volume: PyReadonlyArray1<'py, f64>,
    period: usize,
) -> PyResult<Py<PyArray1<f64>>> {
    let out = oa_core::vwma(data.as_slice()?, volume.as_slice()?, period);
    Ok(out.into_pyarray_bound(py).unbind())
}

#[pyfunction]
#[pyo3(signature = (data, period, fast_sc, slow_sc))]
fn kama<'py>(
    py: Python<'py>,
    data: PyReadonlyArray1<'py, f64>,
    period: usize,
    fast_sc: f64,
    slow_sc: f64,
) -> PyResult<Py<PyArray1<f64>>> {
    let out = oa_core::kama(data.as_slice()?, period, fast_sc, slow_sc);
    Ok(out.into_pyarray_bound(py).unbind())
}

// --- boolean kernels (inputs treated as truthy; outputs are numpy bool arrays) ---

macro_rules! wrap_cross {
    ($name:ident, $core:path) => {
        #[pyfunction]
        fn $name<'py>(
            py: Python<'py>,
            s1: PyReadonlyArray1<'py, f64>,
            s2: PyReadonlyArray1<'py, f64>,
        ) -> PyResult<Py<PyArray1<bool>>> {
            let out = $core(s1.as_slice()?, s2.as_slice()?);
            Ok(out.into_pyarray_bound(py).unbind())
        }
    };
}
wrap_cross!(crossover, oa_core::crossover);
wrap_cross!(crossunder, oa_core::crossunder);
wrap_cross!(cross, oa_core::cross);

macro_rules! wrap_riserun {
    ($name:ident, $core:path) => {
        #[pyfunction]
        fn $name<'py>(
            py: Python<'py>,
            data: PyReadonlyArray1<'py, f64>,
            length: usize,
        ) -> PyResult<Py<PyArray1<bool>>> {
            let out = $core(data.as_slice()?, length);
            Ok(out.into_pyarray_bound(py).unbind())
        }
    };
}
wrap_riserun!(rising, oa_core::rising);
wrap_riserun!(falling, oa_core::falling);

/// exrem/flip accept float "boolean-like" arrays (nonzero == true), matching the
/// legacy numba kernels which were called with float64 signal arrays.
macro_rules! wrap_latch {
    ($name:ident, $core:path) => {
        #[pyfunction]
        fn $name<'py>(
            py: Python<'py>,
            primary: PyReadonlyArray1<'py, f64>,
            secondary: PyReadonlyArray1<'py, f64>,
        ) -> PyResult<Py<PyArray1<bool>>> {
            let p: Vec<bool> = primary.as_slice()?.iter().map(|&x| x != 0.0).collect();
            let s: Vec<bool> = secondary.as_slice()?.iter().map(|&x| x != 0.0).collect();
            let out = $core(&p, &s);
            Ok(out.into_pyarray_bound(py).unbind())
        }
    };
}
wrap_latch!(exrem, oa_core::exrem);
wrap_latch!(flip, oa_core::flip);

#[pymodule]
fn _oaindicators(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sma, m)?)?;
    m.add_function(wrap_pyfunction!(rolling_sum, m)?)?;
    m.add_function(wrap_pyfunction!(rolling_variance, m)?)?;
    m.add_function(wrap_pyfunction!(stdev, m)?)?;
    m.add_function(wrap_pyfunction!(ema, m)?)?;
    m.add_function(wrap_pyfunction!(ema_wilder, m)?)?;
    m.add_function(wrap_pyfunction!(highest, m)?)?;
    m.add_function(wrap_pyfunction!(lowest, m)?)?;
    m.add_function(wrap_pyfunction!(change, m)?)?;
    m.add_function(wrap_pyfunction!(roc, m)?)?;
    m.add_function(wrap_pyfunction!(cmo, m)?)?;
    m.add_function(wrap_pyfunction!(ulcer_index, m)?)?;
    m.add_function(wrap_pyfunction!(true_range, m)?)?;
    m.add_function(wrap_pyfunction!(atr_wilder, m)?)?;
    m.add_function(wrap_pyfunction!(atr_sma, m)?)?;
    m.add_function(wrap_pyfunction!(vwma, m)?)?;
    m.add_function(wrap_pyfunction!(kama, m)?)?;
    m.add_function(wrap_pyfunction!(crossover, m)?)?;
    m.add_function(wrap_pyfunction!(crossunder, m)?)?;
    m.add_function(wrap_pyfunction!(cross, m)?)?;
    m.add_function(wrap_pyfunction!(rising, m)?)?;
    m.add_function(wrap_pyfunction!(falling, m)?)?;
    m.add_function(wrap_pyfunction!(exrem, m)?)?;
    m.add_function(wrap_pyfunction!(flip, m)?)?;
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    Ok(())
}
