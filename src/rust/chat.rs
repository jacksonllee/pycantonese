use pyo3::prelude::*;
use pyo3::types::{PyAnyMethods, PyType};
use regex::Regex;
use rustling::chat::{
    BaseChat, BasePyChat, Chat as RustlingChat, ChatError, ChatFile, MisalignmentInfo,
    PyUtterances, Utterance as RustlingUtterance,
};
use rustling::ngram::{BaseNgrams, Ngrams, PyNgrams};
use std::collections::{HashMap, HashSet, VecDeque};
use std::sync::{LazyLock, Mutex};

type PyObject = Py<PyAny>;

// ---------------------------------------------------------------------------
// Jyutping validation
// ---------------------------------------------------------------------------

/// Compiled regex for validating concatenated Jyutping syllables.
/// Each syllable: optional onset + required nucleus + optional coda + tone [1-6].
static JYUTPING_RE: LazyLock<Regex> = LazyLock::new(|| {
    Regex::new(
        r"^(?:(?:gw|kw|ng|[bdgzptkcmnfhslwjv])?(?:aa|oe|eo|yu|ng|[aeioumn])(?:ng|[iptkmnu])?[1-6])+$",
    )
    .unwrap()
});

fn is_valid_jyutping(s: &str) -> bool {
    if s.is_empty() {
        return false;
    }
    JYUTPING_RE.is_match(&s.to_lowercase())
}

// ---------------------------------------------------------------------------
// Mor field parsing
// ---------------------------------------------------------------------------

/// Parse the CHAT %mor field into (jyutping, mor, gloss) components.
///
/// Examples:
///   "suk1&DIM=uncle" -> (Some("suk1"), Some("&DIM"), Some("uncle"))
///   "ngo5-PL=I"      -> (Some("ngo5"), Some("-PL"), Some("I"))
///   "wai3"           -> (Some("wai3"), None, None)
///   None             -> (None, None, None)
fn parse_mor_field(mor: Option<&str>) -> (Option<String>, Option<String>, Option<String>) {
    let mor = match mor {
        Some(m) => m,
        None => return (None, None, None),
    };

    // Split by "=" to extract gloss.
    let (jyutping_mor, gloss) = match mor.find('=') {
        Some(idx) => (&mor[..idx], Some(mor[idx + 1..].to_string())),
        None => (mor, None),
    };

    // Split by "-" to extract mor2.
    let (jyutping_mor, mor2) = match jyutping_mor.find('-') {
        Some(idx) => (&jyutping_mor[..idx], Some(&jyutping_mor[idx + 1..])),
        None => (jyutping_mor, None),
    };

    // Split by "&" to extract mor1.
    let (jyutping_str, mor1) = match jyutping_mor.find('&') {
        Some(idx) => (&jyutping_mor[..idx], Some(&jyutping_mor[idx + 1..])),
        None => (jyutping_mor, None),
    };

    // Reconstruct mor.
    let mut mor_result = String::new();
    if let Some(m1) = mor1 {
        mor_result.push('&');
        mor_result.push_str(m1);
    }
    if let Some(m2) = mor2 {
        mor_result.push('-');
        mor_result.push_str(m2);
    }

    // Validate jyutping.
    let jyutping = if is_valid_jyutping(jyutping_str) {
        Some(jyutping_str.to_string())
    } else {
        None
    };

    let mor_opt = if mor_result.is_empty() {
        None
    } else {
        Some(mor_result)
    };

    (jyutping, mor_opt, gloss)
}

// ---------------------------------------------------------------------------
// Punctuation marks (for Token.to_mor_tier)
// ---------------------------------------------------------------------------

static PUNCTUATION_MARKS: LazyLock<HashSet<&'static str>> = LazyLock::new(|| {
    let mut set = HashSet::new();
    // CHAT punctuation
    for p in &[".", "?", "!", ",", ";"] {
        set.insert(*p);
    }
    // Chinese punctuation
    for p in &[
        "，", "。", "！", "？", "；", "：", "（", "）", "「", "」", "［", "］", "【", "】", "《",
        "》", "〈", "〉", "、", "‧", "…", "—", "～",
    ] {
        set.insert(*p);
    }
    set
});

// ---------------------------------------------------------------------------
// Token
// ---------------------------------------------------------------------------

/// A token with Cantonese-specific fields parsed from a CHAT utterance.
#[pyclass]
#[derive(Debug)]
pub struct Token {
    #[pyo3(get)]
    pub word: String,
    #[pyo3(get)]
    pub pos: Option<String>,
    #[pyo3(get)]
    pub jyutping: Option<String>,
    #[pyo3(get)]
    pub mor: Option<String>,
    #[pyo3(get)]
    pub gloss: Option<String>,
    #[pyo3(get)]
    pub gra: Option<PyObject>,
}

#[pymethods]
impl Token {
    #[new]
    #[pyo3(signature = (word, pos=None, jyutping=None, mor=None, gloss=None, gra=None))]
    fn new(
        word: String,
        pos: Option<String>,
        jyutping: Option<String>,
        mor: Option<String>,
        gloss: Option<String>,
        gra: Option<PyObject>,
    ) -> Self {
        Self {
            word,
            pos,
            jyutping,
            mor,
            gloss,
            gra,
        }
    }

    fn __repr__(&self, py: Python<'_>) -> String {
        let gra_repr = match &self.gra {
            Some(g) => match g.bind(py).repr() {
                Ok(r) => r.to_string(),
                Err(_) => String::from("None"),
            },
            None => String::from("None"),
        };
        format!(
            "Token(word='{}', pos={}, jyutping={}, mor={}, gloss={}, gra={})",
            self.word,
            fmt_opt(&self.pos),
            fmt_opt(&self.jyutping),
            fmt_opt(&self.mor),
            fmt_opt(&self.gloss),
            gra_repr,
        )
    }

    fn __eq__(&self, py: Python<'_>, other: &Token) -> PyResult<bool> {
        if self.word != other.word
            || self.pos != other.pos
            || self.jyutping != other.jyutping
            || self.mor != other.mor
            || self.gloss != other.gloss
        {
            return Ok(false);
        }
        // Compare gra via Python equality.
        match (&self.gra, &other.gra) {
            (None, None) => Ok(true),
            (Some(a), Some(b)) => {
                let a_bound: &Bound<'_, PyAny> = a.bind(py);
                let b_bound: &Bound<'_, PyAny> = b.bind(py);
                a_bound.eq(b_bound)
            }
            _ => Ok(false),
        }
    }

    fn __hash__(&self, py: Python<'_>) -> PyResult<isize> {
        let mut h: isize = 0;
        h ^= hash_str(&self.word);
        h ^= hash_opt_str(&self.pos);
        h ^= hash_opt_str(&self.jyutping);
        h ^= hash_opt_str(&self.mor);
        h ^= hash_opt_str(&self.gloss);
        if let Some(ref g) = self.gra {
            h ^= g.bind(py).hash()?;
        }
        Ok(h)
    }

    fn to_mor_tier(&self) -> String {
        if PUNCTUATION_MARKS.contains(self.word.as_str()) {
            return self.word.clone();
        }
        let mut result = String::new();
        if let Some(ref pos) = self.pos {
            result.push_str(pos);
            result.push('|');
        }
        if let Some(ref jp) = self.jyutping {
            result.push_str(jp);
        }
        if let Some(ref m) = self.mor {
            result.push_str(m);
        }
        if let Some(ref g) = self.gloss {
            result.push('=');
            result.push_str(g);
        }
        result
    }

    fn to_gra_tier(&self, py: Python<'_>) -> PyResult<String> {
        let gra = self
            .gra
            .as_ref()
            .ok_or_else(|| pyo3::exceptions::PyValueError::new_err("gra is None"))?;
        let gra = gra.bind(py);
        let dep: usize = gra.getattr("dep")?.extract()?;
        let head: usize = gra.getattr("head")?.extract()?;
        let rel: String = gra.getattr("rel")?.extract()?;
        Ok(format!("{dep}|{head}|{rel}"))
    }
}

fn fmt_opt(opt: &Option<String>) -> String {
    match opt {
        Some(s) => format!("'{s}'"),
        None => "None".to_string(),
    }
}

fn hash_str(s: &str) -> isize {
    let mut h: isize = 0;
    for b in s.bytes() {
        h = h.wrapping_mul(31).wrapping_add(b as isize);
    }
    h
}

fn hash_opt_str(s: &Option<String>) -> isize {
    match s {
        Some(s) => hash_str(s),
        None => 0,
    }
}

// ---------------------------------------------------------------------------
// Utterance
// ---------------------------------------------------------------------------

/// An utterance from CHAT data with preprocessed Cantonese tokens.
#[pyclass]
#[derive(Debug)]
pub struct Utterance {
    #[pyo3(get)]
    pub participant: String,
    #[pyo3(get)]
    pub tokens: Vec<Py<Token>>,
    #[pyo3(get)]
    pub time_marks: Option<(i64, i64)>,
    #[pyo3(get)]
    pub tiers: HashMap<String, String>,
    #[pyo3(get)]
    pub audible: Option<String>,
    #[pyo3(get)]
    pub changeable_header: Option<PyObject>,
    #[pyo3(get)]
    pub mor_tier_name: Option<String>,
    #[pyo3(get)]
    pub gra_tier_name: Option<String>,
}

#[pymethods]
impl Utterance {
    #[new]
    #[allow(clippy::too_many_arguments)]
    #[pyo3(signature = (*, participant, tokens, time_marks=None, tiers=None, audible=None, changeable_header=None, mor_tier_name=Some("%mor".to_string()), gra_tier_name=Some("%gra".to_string())))]
    fn new(
        participant: String,
        tokens: Vec<Py<Token>>,
        time_marks: Option<(i64, i64)>,
        tiers: Option<HashMap<String, String>>,
        audible: Option<String>,
        changeable_header: Option<PyObject>,
        mor_tier_name: Option<String>,
        gra_tier_name: Option<String>,
    ) -> Self {
        Self {
            participant,
            tokens,
            time_marks,
            tiers: tiers.unwrap_or_default(),
            audible,
            changeable_header,
            mor_tier_name,
            gra_tier_name,
        }
    }

    fn __repr__(&self) -> String {
        format!(
            "Utterance(participant='{}', tokens=[...{} tokens], time_marks={:?})",
            self.participant,
            self.tokens.len(),
            self.time_marks,
        )
    }
}

// ---------------------------------------------------------------------------
// Token preprocessing
// ---------------------------------------------------------------------------

/// Preprocess a rustling Token into a pycantonese Token.
fn preprocess_token(py: Python<'_>, t: &rustling::chat::Token) -> PyResult<Py<Token>> {
    let (jyutping, mor, gloss) = parse_mor_field(t.mor.as_deref());
    let pos = t.pos.clone();

    let gra = match &t.gra {
        Some(g) => Some(
            Py::new(
                py,
                rustling::chat::Gra {
                    dep: g.dep,
                    head: g.head,
                    rel: g.rel.clone(),
                },
            )?
            .into_any(),
        ),
        None => None,
    };

    Py::new(
        py,
        Token {
            word: t.word.clone(),
            pos,
            jyutping,
            mor,
            gloss,
            gra,
        },
    )
}

/// Preprocess a rustling Utterance into a pycantonese Utterance.
fn preprocess_utterance(py: Python<'_>, u: &rustling::chat::Utterance) -> PyResult<Py<Utterance>> {
    let tokens: Vec<Py<Token>> = u
        .tokens
        .as_ref()
        .map(|toks| {
            toks.iter()
                .map(|t| preprocess_token(py, t))
                .collect::<PyResult<Vec<_>>>()
        })
        .unwrap_or_else(|| Ok(Vec::new()))?;

    let audible = u.audible();

    let participant = u.participant.clone().unwrap_or_default();
    let tiers = u.tiers.clone().unwrap_or_default();

    let changeable_header = match &u.changeable_header {
        Some(ch) => Some(Py::new(py, ch.clone())?.into_any()),
        None => None,
    };

    Py::new(
        py,
        Utterance {
            participant,
            tokens,
            time_marks: u.time_marks,
            tiers,
            audible,
            changeable_header,
            mor_tier_name: u.mor_tier_name.clone(),
            gra_tier_name: u.gra_tier_name.clone(),
        },
    )
}

/// Extract token references from a cached Py<Utterance>.
fn extract_tokens(py: Python<'_>, u: &Py<Utterance>) -> Vec<Py<Token>> {
    let utt = u.bind(py).borrow();
    utt.tokens.iter().map(|t| t.clone_ref(py)).collect()
}

// ---------------------------------------------------------------------------
// Reverse conversion: pycantonese types -> rustling types
// ---------------------------------------------------------------------------

/// Convert a pycantonese Token back to a rustling Token.
fn pycantonese_token_to_rustling(py: Python<'_>, t: &Token) -> PyResult<rustling::chat::Token> {
    // Reconstruct the raw mor field from jyutping + mor + gloss.
    let mor = {
        let mut parts = String::new();
        if let Some(ref jp) = t.jyutping {
            parts.push_str(jp);
        }
        if let Some(ref m) = t.mor {
            parts.push_str(m);
        }
        if let Some(ref g) = t.gloss {
            parts.push('=');
            parts.push_str(g);
        }
        if parts.is_empty() { None } else { Some(parts) }
    };

    let gra = match &t.gra {
        Some(g) => {
            let g = g.bind(py);
            Some(rustling::chat::Gra {
                dep: g.getattr("dep")?.extract()?,
                head: g.getattr("head")?.extract()?,
                rel: g.getattr("rel")?.extract()?,
            })
        }
        None => None,
    };

    Ok(rustling::chat::Token {
        word: t.word.clone(),
        pos: t.pos.clone(),
        mor,
        gra,
    })
}

/// Convert a pycantonese Utterance back to a rustling Utterance.
fn pycantonese_utt_to_rustling(py: Python<'_>, u: &Utterance) -> PyResult<RustlingUtterance> {
    let tokens = if u.tokens.is_empty() {
        None
    } else {
        let toks: Vec<rustling::chat::Token> = u
            .tokens
            .iter()
            .map(|t| {
                let tok = t.bind(py).borrow();
                pycantonese_token_to_rustling(py, &tok)
            })
            .collect::<PyResult<Vec<_>>>()?;
        Some(toks)
    };

    let participant = if u.participant.is_empty() {
        None
    } else {
        Some(u.participant.clone())
    };
    let tiers = if u.tiers.is_empty() {
        None
    } else {
        Some(u.tiers.clone())
    };

    let changeable_header = match &u.changeable_header {
        Some(ch) => Some(ch.bind(py).extract::<rustling::chat::ChangeableHeader>()?),
        None => None,
    };

    Ok(RustlingUtterance {
        participant,
        tokens,
        time_marks: u.time_marks,
        tiers,
        changeable_header,
        mor_tier_name: u.mor_tier_name.clone(),
        gra_tier_name: u.gra_tier_name.clone(),
    })
}

// ---------------------------------------------------------------------------
// File loading helpers
// ---------------------------------------------------------------------------

/// Check misalignments and raise if strict mode.
/// Convert user-facing tier names (without `%`) to internal `%`-prefixed keys.
///
/// If either tier is `None`, both are set to `None` (disabling mor+gra parsing).
fn tier_keys(mor_tier: Option<&str>, gra_tier: Option<&str>) -> (Option<String>, Option<String>) {
    match (mor_tier, gra_tier) {
        (Some(m), Some(g)) => {
            let mk = if m.starts_with('%') {
                m.to_string()
            } else {
                format!("%{m}")
            };
            let gk = if g.starts_with('%') {
                g.to_string()
            } else {
                format!("%{g}")
            };
            (Some(mk), Some(gk))
        }
        _ => (None, None),
    }
}

fn check_misalignments(misalignments: &[MisalignmentInfo], strict: bool) -> PyResult<()> {
    if strict && !misalignments.is_empty() {
        let msgs: Vec<String> = misalignments
            .iter()
            .map(|m| {
                format!(
                    "In file '{}', participant '{}': word count ({}) != mor count ({})\n\
                     Words: {:?}\nMor: {:?}",
                    m.file_path, m.participant, m.word_count, m.mor_count, m.words, m.mor_labels,
                )
            })
            .collect();
        return Err(pyo3::exceptions::PyValueError::new_err(msgs.join("\n\n")));
    }
    Ok(())
}

/// Convert a [`ChatError`] to a Python exception.
fn chat_error_to_pyerr(e: ChatError) -> pyo3::PyErr {
    match e {
        ChatError::Io(e) => pyo3::exceptions::PyIOError::new_err(e.to_string()),
        ChatError::InvalidPattern(e) => pyo3::exceptions::PyValueError::new_err(e),
        ChatError::Zip(e) => pyo3::exceptions::PyIOError::new_err(e),
    }
}

// ---------------------------------------------------------------------------
// Chat
// ---------------------------------------------------------------------------

type TokenCache = Vec<Vec<Vec<Py<Token>>>>;
type JyutpingCache = Vec<Vec<Vec<Option<String>>>>;

/// A reader for Cantonese CHAT corpus data.
///
/// Implements rustling's `BaseChat` trait directly for access to shared
/// CHAT reader behavior, and adds Cantonese-specific token preprocessing
/// (Jyutping extraction, morphology parsing).
#[pyclass(subclass)]
pub struct Chat {
    inner: RustlingChat,
    /// Cached preprocessed utterances: [file_idx][utt_idx].
    utterance_cache: Mutex<Option<Vec<Vec<Py<Utterance>>>>>,
    /// Cached preprocessed tokens: [file_idx][utt_idx][tok_idx].
    token_cache: Mutex<Option<TokenCache>>,
    /// Cached jyutping values: [file_idx][utt_idx][tok_idx].
    jyutping_cache: Mutex<Option<JyutpingCache>>,
}

impl Chat {
    /// Get or populate the preprocessed utterance cache.
    fn get_cached_utterances(&self, py: Python<'_>) -> PyResult<Vec<Vec<Py<Utterance>>>> {
        let mut guard = self.utterance_cache.lock().unwrap();
        if let Some(ref cached) = *guard {
            Ok(cached
                .iter()
                .map(|file_utts| file_utts.iter().map(|u| u.clone_ref(py)).collect())
                .collect())
        } else {
            let result: Vec<Vec<Py<Utterance>>> = self
                .inner
                .files()
                .iter()
                .map(|f| {
                    f.real_utterances()
                        .map(|u| preprocess_utterance(py, u))
                        .collect::<PyResult<Vec<_>>>()
                })
                .collect::<PyResult<Vec<_>>>()?;
            *guard = Some(
                result
                    .iter()
                    .map(|file_utts| file_utts.iter().map(|u| u.clone_ref(py)).collect())
                    .collect(),
            );
            Ok(result)
        }
    }

    /// Ensure the token cache is populated.
    fn ensure_token_cache(&self, py: Python<'_>) -> PyResult<()> {
        let mut guard = self.token_cache.lock().unwrap();
        if guard.is_none() {
            // Populate from utterance cache.
            let utts = self.get_cached_utterances(py)?;
            *guard = Some(
                utts.iter()
                    .map(|file_utts| file_utts.iter().map(|u| extract_tokens(py, u)).collect())
                    .collect(),
            );
        }
        Ok(())
    }

    /// Ensure the jyutping cache is populated.
    fn ensure_jyutping_cache(&self, py: Python<'_>) -> PyResult<()> {
        let mut guard = self.jyutping_cache.lock().unwrap();
        if guard.is_none() {
            // Populate from token cache.
            self.ensure_token_cache(py)?;
            let tok_guard = self.token_cache.lock().unwrap();
            let tokens = tok_guard.as_ref().unwrap();
            *guard = Some(
                tokens
                    .iter()
                    .map(|file| {
                        file.iter()
                            .map(|utt| {
                                utt.iter()
                                    .map(|t| {
                                        let tok = t.bind(py).borrow();
                                        tok.jyutping.clone()
                                    })
                                    .collect()
                            })
                            .collect()
                    })
                    .collect(),
            );
        }
        Ok(())
    }

    /// Invalidate all caches.
    fn invalidate_cache(&self) {
        *self.utterance_cache.lock().unwrap() = None;
        *self.token_cache.lock().unwrap() = None;
        *self.jyutping_cache.lock().unwrap() = None;
    }
}

impl BaseChat for Chat {
    fn files(&self) -> &VecDeque<ChatFile> {
        self.inner.files()
    }
    fn files_mut(&mut self) -> &mut VecDeque<ChatFile> {
        self.inner.files_mut()
    }
    fn from_files(files: VecDeque<ChatFile>) -> Self {
        Self {
            inner: RustlingChat::from_files(files),
            utterance_cache: Mutex::new(None),
            token_cache: Mutex::new(None),
            jyutping_cache: Mutex::new(None),
        }
    }
}

impl BasePyChat for Chat {}

#[pymethods]
impl Chat {
    #[new]
    fn new() -> Self {
        Self::from_files(VecDeque::new())
    }

    /// Read CHAT data from a directory.
    #[classmethod]
    #[allow(clippy::too_many_arguments)]
    #[pyo3(signature = (path, r#match=None, extension=".cha", parallel=true, strict=true, mor_tier=Some("%mor"), gra_tier=Some("%gra")))]
    fn from_dir(
        _cls: &Bound<'_, PyType>,
        path: &str,
        r#match: Option<&str>,
        extension: &str,
        parallel: bool,
        strict: bool,
        mor_tier: Option<&str>,
        gra_tier: Option<&str>,
    ) -> PyResult<Self> {
        let py = _cls.py();
        let (mor_key, gra_key) = tier_keys(mor_tier, gra_tier);
        let (chat, misalignments) = RustlingChat::read_dir(
            path,
            r#match,
            extension,
            parallel,
            mor_key.as_deref(),
            gra_key.as_deref(),
        )
        .map_err(chat_error_to_pyerr)?;
        check_misalignments(&misalignments, strict)?;
        let result = Self {
            inner: chat,
            utterance_cache: Mutex::new(None),
            token_cache: Mutex::new(None),
            jyutping_cache: Mutex::new(None),
        };
        result.ensure_jyutping_cache(py)?;
        Ok(result)
    }

    /// Read CHAT data from file paths.
    #[classmethod]
    #[pyo3(name = "from_files")]
    #[pyo3(signature = (paths, parallel=true, strict=true, mor_tier=Some("%mor"), gra_tier=Some("%gra")))]
    fn read_files(
        _cls: &Bound<'_, PyType>,
        paths: Vec<String>,
        parallel: bool,
        strict: bool,
        mor_tier: Option<&str>,
        gra_tier: Option<&str>,
    ) -> PyResult<Self> {
        let py = _cls.py();
        let (mor_key, gra_key) = tier_keys(mor_tier, gra_tier);
        let (chat, misalignments) =
            RustlingChat::read_files(&paths, parallel, mor_key.as_deref(), gra_key.as_deref())
                .map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))?;
        check_misalignments(&misalignments, strict)?;
        let result = Self {
            inner: chat,
            utterance_cache: Mutex::new(None),
            token_cache: Mutex::new(None),
            jyutping_cache: Mutex::new(None),
        };
        result.ensure_jyutping_cache(py)?;
        Ok(result)
    }

    /// Read CHAT data from strings.
    #[classmethod]
    #[pyo3(signature = (strs, ids=None, parallel=true, strict=true, mor_tier=Some("%mor"), gra_tier=Some("%gra")))]
    fn from_strs(
        _cls: &Bound<'_, PyType>,
        strs: Vec<String>,
        ids: Option<Vec<String>>,
        parallel: bool,
        strict: bool,
        mor_tier: Option<&str>,
        gra_tier: Option<&str>,
    ) -> PyResult<Self> {
        if let Some(ref ids) = ids
            && strs.len() != ids.len()
        {
            return Err(pyo3::exceptions::PyValueError::new_err(format!(
                "strs and ids must have the same length: {} vs {}",
                strs.len(),
                ids.len()
            )));
        }
        let py = _cls.py();
        let (mor_key, gra_key) = tier_keys(mor_tier, gra_tier);
        let (chat, misalignments) =
            RustlingChat::from_strs(strs, ids, parallel, mor_key.as_deref(), gra_key.as_deref());
        check_misalignments(&misalignments, strict)?;
        let result = Self {
            inner: chat,
            utterance_cache: Mutex::new(None),
            token_cache: Mutex::new(None),
            jyutping_cache: Mutex::new(None),
        };
        result.ensure_jyutping_cache(py)?;
        Ok(result)
    }

    /// Read CHAT data from a ZIP archive.
    #[classmethod]
    #[allow(clippy::too_many_arguments)]
    #[pyo3(signature = (path, r#match=None, extension=".cha", parallel=true, strict=true, mor_tier=Some("%mor"), gra_tier=Some("%gra")))]
    fn from_zip(
        _cls: &Bound<'_, PyType>,
        path: &str,
        r#match: Option<&str>,
        extension: &str,
        parallel: bool,
        strict: bool,
        mor_tier: Option<&str>,
        gra_tier: Option<&str>,
    ) -> PyResult<Self> {
        let py = _cls.py();
        let (mor_key, gra_key) = tier_keys(mor_tier, gra_tier);
        let (chat, misalignments) = RustlingChat::read_zip(
            path,
            r#match,
            extension,
            parallel,
            mor_key.as_deref(),
            gra_key.as_deref(),
        )
        .map_err(chat_error_to_pyerr)?;
        check_misalignments(&misalignments, strict)?;
        let result = Self {
            inner: chat,
            utterance_cache: Mutex::new(None),
            token_cache: Mutex::new(None),
            jyutping_cache: Mutex::new(None),
        };
        result.ensure_jyutping_cache(py)?;
        Ok(result)
    }

    /// Construct a Chat from a list of pycantonese Utterances.
    #[classmethod]
    #[pyo3(signature = (utterances))]
    fn from_utterances(_cls: &Bound<'_, PyType>, utterances: Vec<Py<Utterance>>) -> PyResult<Self> {
        let py = _cls.py();
        let rustling_utts: Vec<RustlingUtterance> = utterances
            .iter()
            .map(|u| {
                let utt = u.bind(py).borrow();
                pycantonese_utt_to_rustling(py, &utt)
            })
            .collect::<PyResult<Vec<_>>>()?;
        let result = <Self as BaseChat>::from_utterances(rustling_utts);
        result.ensure_jyutping_cache(py)?;
        Ok(result)
    }

    // -- Data access (with preprocessing) --

    /// Return preprocessed tokens.
    #[pyo3(signature = (*, by_utterance=false, by_file=false))]
    fn tokens(&self, py: Python<'_>, by_utterance: bool, by_file: bool) -> PyResult<PyObject> {
        self.ensure_token_cache(py)?;
        let guard = self.token_cache.lock().unwrap();
        let cached = guard.as_ref().unwrap();
        if by_file && by_utterance {
            let outer = pyo3::types::PyList::empty(py);
            for file in cached {
                let file_list = pyo3::types::PyList::empty(py);
                for utt in file {
                    file_list.append(pyo3::types::PyList::new(py, utt)?)?;
                }
                outer.append(file_list)?;
            }
            Ok(outer.into_any().unbind())
        } else if by_utterance {
            let outer = pyo3::types::PyList::empty(py);
            for file in cached {
                for utt in file {
                    outer.append(pyo3::types::PyList::new(py, utt)?)?;
                }
            }
            Ok(outer.into_any().unbind())
        } else if by_file {
            let outer = pyo3::types::PyList::empty(py);
            for file in cached {
                let flat: Vec<&Py<Token>> = file.iter().flat_map(|utt| utt.iter()).collect();
                outer.append(pyo3::types::PyList::new(py, flat)?)?;
            }
            Ok(outer.into_any().unbind())
        } else {
            let flat: Vec<&Py<Token>> = cached
                .iter()
                .flat_map(|file| file.iter())
                .flat_map(|utt| utt.iter())
                .collect();
            Ok(pyo3::types::PyList::new(py, flat)?.into_any().unbind())
        }
    }

    /// Return Jyutping romanization for all tokens.
    #[pyo3(signature = (*, by_utterance=false, by_file=false))]
    fn jyutping(&self, py: Python<'_>, by_utterance: bool, by_file: bool) -> PyResult<PyObject> {
        self.ensure_jyutping_cache(py)?;
        let guard = self.jyutping_cache.lock().unwrap();
        let cached = guard.as_ref().unwrap();
        if by_file && by_utterance {
            Ok(cached.into_pyobject(py)?.into_any().unbind())
        } else if by_utterance {
            let result: Vec<&Vec<Option<String>>> =
                cached.iter().flat_map(|file| file.iter()).collect();
            Ok(result.into_pyobject(py)?.into_any().unbind())
        } else if by_file {
            let result: Vec<Vec<&Option<String>>> = cached
                .iter()
                .map(|file| file.iter().flat_map(|utt| utt.iter()).collect())
                .collect();
            Ok(result.into_pyobject(py)?.into_any().unbind())
        } else {
            let result: Vec<&Option<String>> = cached
                .iter()
                .flat_map(|file| file.iter())
                .flat_map(|utt| utt.iter())
                .collect();
            Ok(result.into_pyobject(py)?.into_any().unbind())
        }
    }

    /// Return preprocessed utterances.
    #[pyo3(signature = (*, by_file=false))]
    fn utterances(&self, py: Python<'_>, by_file: bool) -> PyResult<PyObject> {
        let cached = self.get_cached_utterances(py)?;
        if by_file {
            Ok(cached.into_pyobject(py)?.into_any().unbind())
        } else {
            let result: Vec<Py<Utterance>> = cached.into_iter().flatten().collect();
            Ok(result.into_pyobject(py)?.into_any().unbind())
        }
    }

    /// Return words.
    #[pyo3(signature = (*, by_utterance=false, by_file=false))]
    fn words(&self, py: Python<'_>, by_utterance: bool, by_file: bool) -> PyResult<PyObject> {
        if by_file && by_utterance {
            let result: Vec<Vec<Vec<String>>> = self
                .files()
                .iter()
                .map(|f| {
                    f.real_utterances()
                        .filter_map(|u| u.tokens.as_ref())
                        .map(|tokens| tokens.iter().map(|t| t.word.clone()).collect())
                        .collect()
                })
                .collect();
            Ok(result.into_pyobject(py)?.into_any().unbind())
        } else if by_utterance {
            let result: Vec<Vec<String>> = self
                .files()
                .iter()
                .flat_map(|f| f.real_utterances())
                .filter_map(|u| u.tokens.as_ref())
                .map(|tokens| tokens.iter().map(|t| t.word.clone()).collect())
                .collect();
            Ok(result.into_pyobject(py)?.into_any().unbind())
        } else if by_file {
            let result: Vec<Vec<String>> = self
                .files()
                .iter()
                .map(|f| {
                    f.real_utterances()
                        .filter_map(|u| u.tokens.as_ref())
                        .flat_map(|tokens| tokens.iter())
                        .map(|t| t.word.clone())
                        .collect()
                })
                .collect();
            Ok(result.into_pyobject(py)?.into_any().unbind())
        } else {
            let result: Vec<String> = self
                .files()
                .iter()
                .flat_map(|f| f.real_utterances())
                .filter_map(|u| u.tokens.as_ref())
                .flat_map(|tokens| tokens.iter())
                .map(|t| t.word.clone())
                .collect();
            Ok(result.into_pyobject(py)?.into_any().unbind())
        }
    }

    // -- Properties --

    /// The number of files.
    #[getter]
    fn n_files(&self) -> usize {
        self.num_files()
    }

    /// The file paths.
    #[getter]
    #[pyo3(name = "file_paths")]
    fn py_file_paths(&self) -> Vec<String> {
        self.file_paths()
    }

    // -- Filter --

    /// Filter by participants and/or files.
    #[pyo3(signature = (*, participants=None, files=None))]
    fn filter(&self, participants: Option<&str>, files: Option<&str>) -> PyResult<Self> {
        let mut filtered: VecDeque<ChatFile> = if let Some(pattern) = files {
            let re = Regex::new(pattern).map_err(|e| {
                pyo3::exceptions::PyValueError::new_err(format!("Invalid regex: {e}"))
            })?;
            self.files()
                .iter()
                .filter(|f| re.is_match(&f.file_path))
                .cloned()
                .collect()
        } else {
            self.files().clone()
        };

        if let Some(pattern) = participants {
            let re = Regex::new(pattern).map_err(|e| {
                pyo3::exceptions::PyValueError::new_err(format!("Invalid regex: {e}"))
            })?;
            for file in filtered.iter_mut() {
                file.events.retain(|utt| {
                    if utt.changeable_header.is_some() {
                        return true;
                    }
                    if let Some(ref participant) = utt.participant {
                        re.is_match(participant)
                    } else {
                        false
                    }
                });
                // Reset stale rustling caches after mutating events.
                file.reset_caches();
            }
        }

        Ok(Self::from_files(filtered))
    }

    // -- Serialization --

    /// Return the data as CHAT-formatted strings.
    fn to_strs(&self) -> Vec<String> {
        self.to_strings()
    }

    /// Write the data to CHAT file(s).
    #[pyo3(signature = (path, *, is_dir=false, filenames=None))]
    fn to_chat(&self, path: &str, is_dir: bool, filenames: Option<Vec<String>>) -> PyResult<()> {
        let strs = self.to_strings();
        if !is_dir {
            if strs.len() > 1 {
                return Err(pyo3::exceptions::PyValueError::new_err(
                    "Multiple files in this reader. Use is_dir=True to write to a directory.",
                ));
            }
            if let Some(s) = strs.first() {
                std::fs::write(path, s).map_err(|e| {
                    pyo3::exceptions::PyIOError::new_err(format!("Write error: {e}"))
                })?;
            }
        } else {
            std::fs::create_dir_all(path).map_err(|e| {
                pyo3::exceptions::PyIOError::new_err(format!("Create dir error: {e}"))
            })?;
            let names: Vec<String> = filenames.unwrap_or_else(|| {
                self.files()
                    .iter()
                    .map(|f| {
                        std::path::Path::new(&f.file_path)
                            .file_name()
                            .map(|n| n.to_string_lossy().to_string())
                            .unwrap_or_else(|| f.file_path.clone())
                    })
                    .collect()
            });
            for (s, name) in strs.iter().zip(names.iter()) {
                let file_path = std::path::Path::new(path).join(name);
                std::fs::write(&file_path, s).map_err(|e| {
                    pyo3::exceptions::PyIOError::new_err(format!("Write error: {e}"))
                })?;
            }
        }
        Ok(())
    }

    // -- Mutation --

    /// Append another Chat's data.
    fn append(&mut self, other: &Chat) {
        self.files_mut().extend(other.files().iter().cloned());
        self.invalidate_cache();
    }

    /// Extend with data from multiple Chat objects.
    fn extend(&mut self, others: Vec<PyRef<'_, Chat>>) {
        for other in &others {
            self.files_mut().extend(other.files().iter().cloned());
        }
        self.invalidate_cache();
    }

    // -- Metadata --

    /// Return the headers for each file.
    #[pyo3(name = "headers")]
    fn py_headers(&self) -> Vec<rustling::chat::Headers> {
        self.headers()
    }

    /// Return the ages.
    #[pyo3(name = "ages")]
    fn py_ages(&self) -> Vec<Option<rustling::chat::Age>> {
        self.files()
            .iter()
            .map(|f| f.headers.participants.first().and_then(|p| p.age.clone()))
            .collect()
    }

    /// Return participants.
    #[pyo3(name = "participants")]
    #[pyo3(signature = (*, by_file=false))]
    fn py_participants(&self, py: Python<'_>, by_file: bool) -> PyResult<PyObject> {
        if by_file {
            Ok(self.participants().into_pyobject(py)?.into_any().unbind())
        } else {
            let result: Vec<rustling::chat::Participant> = self
                .files()
                .iter()
                .flat_map(|f| f.headers.participants.clone())
                .collect();
            Ok(result.into_pyobject(py)?.into_any().unbind())
        }
    }

    /// Return languages.
    #[pyo3(name = "languages")]
    #[pyo3(signature = (*, by_file=false))]
    fn py_languages(&self, py: Python<'_>, by_file: bool) -> PyResult<PyObject> {
        if by_file {
            Ok(self.languages().into_pyobject(py)?.into_any().unbind())
        } else {
            let result: Vec<String> = self
                .files()
                .iter()
                .flat_map(|f| f.headers.languages.clone())
                .collect();
            Ok(result.into_pyobject(py)?.into_any().unbind())
        }
    }

    /// Print summary info.
    #[pyo3(signature = (verbose=false))]
    fn info(&self, verbose: bool) {
        let n_files = self.num_files();
        let n_utterances: usize = self
            .files()
            .iter()
            .map(|f| f.events.iter().filter(|e| e.participant.is_some()).count())
            .sum();
        println!("{n_files} file(s), {n_utterances} utterance(s)");
        if verbose {
            for file in self.files() {
                let file_utts = file
                    .events
                    .iter()
                    .filter(|e| e.participant.is_some())
                    .count();
                println!("  {}: {file_utts} utterance(s)", file.file_path);
            }
        }
    }

    // -- Display --

    /// Return the first n utterances with a formatted display.
    #[pyo3(signature = (n=5))]
    fn head(&self, n: usize) -> PyUtterances {
        PyUtterances(self.inner.head(n))
    }

    /// Return the last n utterances with a formatted display.
    #[pyo3(signature = (n=5))]
    fn tail(&self, n: usize) -> PyUtterances {
        PyUtterances(self.inner.tail(n))
    }

    // -- Ngrams --

    /// Return word n-grams.
    fn word_ngrams(&self, n: usize) -> PyResult<PyNgrams> {
        let mut counter = Ngrams::new(n, None).map_err(PyErr::from)?;
        for file in self.files() {
            for utt in file.real_utterances() {
                let words: Vec<String> = utt
                    .tokens
                    .as_deref()
                    .unwrap_or(&[])
                    .iter()
                    .filter(|t| !t.word.is_empty())
                    .map(|t| t.word.clone())
                    .collect();
                counter.count(words);
            }
        }
        Ok(PyNgrams { inner: counter })
    }

    fn __bool__(&self) -> bool {
        !self.is_empty()
    }
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_is_valid_jyutping() {
        assert!(is_valid_jyutping("gwong2"));
        assert!(is_valid_jyutping("dung1"));
        assert!(is_valid_jyutping("waa2"));
        assert!(is_valid_jyutping("gwong2dung1waa2"));
        assert!(is_valid_jyutping("m4"));
        assert!(is_valid_jyutping("ng5"));
        assert!(is_valid_jyutping("hm4"));
        assert!(is_valid_jyutping("hng6"));
        assert!(is_valid_jyutping("wai3"));
        assert!(is_valid_jyutping("Wai3")); // case insensitive
        assert!(!is_valid_jyutping(""));
        assert!(!is_valid_jyutping("hello"));
        assert!(!is_valid_jyutping("abc123"));
        assert!(!is_valid_jyutping("gwong")); // no tone
    }

    #[test]
    fn test_parse_mor_field() {
        // suk1&DIM=uncle
        let (jp, mor, gloss) = parse_mor_field(Some("suk1&DIM=uncle"));
        assert_eq!(jp, Some("suk1".to_string()));
        assert_eq!(mor, Some("&DIM".to_string()));
        assert_eq!(gloss, Some("uncle".to_string()));

        // ngo5-PL=I
        let (jp, mor, gloss) = parse_mor_field(Some("ngo5-PL=I"));
        assert_eq!(jp, Some("ngo5".to_string()));
        assert_eq!(mor, Some("-PL".to_string()));
        assert_eq!(gloss, Some("I".to_string()));

        // wai3
        let (jp, mor, gloss) = parse_mor_field(Some("wai3"));
        assert_eq!(jp, Some("wai3".to_string()));
        assert_eq!(mor, None);
        assert_eq!(gloss, None);

        // None
        let (jp, mor, gloss) = parse_mor_field(None);
        assert_eq!(jp, None);
        assert_eq!(mor, None);
        assert_eq!(gloss, None);

        // Invalid jyutping
        let (jp, mor, gloss) = parse_mor_field(Some("hello=world"));
        assert_eq!(jp, None);
        assert_eq!(mor, None);
        assert_eq!(gloss, Some("world".to_string()));
    }
}
