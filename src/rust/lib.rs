use pyo3::prelude::*;

mod chat;

#[pymodule]
fn _rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<chat::Token>()?;
    m.add_class::<chat::Utterance>()?;
    m.add_class::<chat::Chat>()?;
    Ok(())
}
