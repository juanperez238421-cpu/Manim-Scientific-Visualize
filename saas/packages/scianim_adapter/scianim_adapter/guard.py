"""Intake guards, spec sanitising and subprocess environment scrubbing.

Everything here treats the PDF and the model output as untrusted data.
"""
from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path


class IntakeError(ValueError):
    """The uploaded file is not acceptable (reason is safe to show to the user)."""


class SpecRejected(ValueError):
    """The model-authored spec contains something the adapter never forwards to the renderer."""


# ------------------------------------------------------------------ PDF intake
def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_pdf(path: Path, *, max_mb: float = 25, max_pages: int = 30) -> dict:
    """Magic bytes, size, structure and page count. Returns {sha256, size_bytes, pages}."""
    path = Path(path)
    if not path.is_file():
        raise IntakeError("file not found")
    size = path.stat().st_size
    if size == 0:
        raise IntakeError("empty file")
    if size > max_mb * 1024 * 1024:
        raise IntakeError(f"file larger than {max_mb:g} MB")
    with open(path, "rb") as f:
        head = f.read(1024)
    if not head.lstrip(b"\x00\t\r\n ").startswith(b"%PDF-"):
        raise IntakeError("not a PDF (missing %PDF- signature)")
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(str(path))
    except Exception as e:  # noqa: BLE001 - any parser failure means rejection
        raise IntakeError(f"unreadable or corrupt PDF: {type(e).__name__}") from e
    try:
        if doc.needs_pass or doc.is_encrypted:
            raise IntakeError("encrypted PDFs are not supported")
        pages = doc.page_count
        if pages < 1:
            raise IntakeError("PDF has no pages")
        if pages > max_pages:
            raise IntakeError(f"PDF has {pages} pages (limit {max_pages})")
    finally:
        doc.close()
    return {"sha256": sha256_file(path), "size_bytes": size, "pages": pages}


# ------------------------------------------------------------------ spec sanitising
TOP_KEYS = {"document", "sha256", "title", "subject", "language", "constants", "problems"}
PROBLEM_KEYS = {"id", "title", "uses", "symbols", "given", "table", "find", "model", "steps",
                "answers", "verify", "interpretation", "visual"}

# TeX primitives that read/write files, change catcodes, load packages or reach the shell.
_TEX_DENY = re.compile(
    r"\\(?:input|include|includeonly|openin|openout|read|readline|write|immediate|catcode|"
    r"usepackage|RequirePackage|documentclass|verbatiminput|lstinputlisting|csname|"
    r"href|url|newwrite|newread|scantokens|pdfshellescape|ShellEscape|directlua|"
    r"special|InputIfFileExists|detokenize)(?![A-Za-z])",   # TeX control words end at the first non-letter
    re.I,
)
_TEX_FIELDS = {"tex", "chip", "find", "label_a", "label_b", "caption", "label", "short"}


def _walk(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from _walk(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _walk(v, f"{path}[{i}]")
    else:
        yield path, obj


def sanitize_spec(spec: dict, *, document_name: str, sha256: str) -> tuple[dict, list[str]]:
    """Return (clean spec, dropped-keys report). Raises SpecRejected for dangerous content.

    * only allow-listed keys survive (the model cannot add code/script/path fields);
    * `document` and `sha256` are forced to the adapter's own copy of the uploaded file;
    * no TeX primitive that touches files, packages or the shell may appear in any string.
    """
    if not isinstance(spec, dict):
        raise SpecRejected("spec is not a JSON object")
    dropped: list[str] = []
    clean = {k: v for k, v in spec.items() if k in TOP_KEYS}
    dropped += [f"spec.{k}" for k in spec if k not in TOP_KEYS]
    probs = clean.get("problems")
    if not isinstance(probs, list):
        raise SpecRejected("spec.problems must be a list")
    new_probs = []
    for i, p in enumerate(probs):
        if not isinstance(p, dict):
            raise SpecRejected(f"problems[{i}] is not an object")
        new_probs.append({k: v for k, v in p.items() if k in PROBLEM_KEYS})
        dropped += [f"problems[{i}].{k}" for k in p if k not in PROBLEM_KEYS]
    clean["problems"] = new_probs
    clean["document"] = document_name
    clean["sha256"] = sha256
    for path, val in _walk(clean):
        if not isinstance(val, str):
            continue
        if "\x00" in val:
            raise SpecRejected(f"NUL byte in {path}")
        leaf = path.rsplit(".", 1)[-1].split("[")[0]
        if (leaf in _TEX_FIELDS or "\\" in val) and _TEX_DENY.search(val):
            raise SpecRejected(f"forbidden TeX command in {path}")
        if len(val) > 4000:
            raise SpecRejected(f"string too long in {path}")
    return clean, dropped


# ------------------------------------------------------------------ subprocess environment
_SAFE_ENV = {"PATH", "SYSTEMROOT", "SYSTEMDRIVE", "WINDIR", "COMSPEC", "PATHEXT", "TEMP", "TMP", "TMPDIR",
             "LANG", "LC_ALL", "LC_CTYPE", "USERPROFILE", "APPDATA", "LOCALAPPDATA", "PROGRAMDATA",
             "PROGRAMFILES", "PROGRAMFILES(X86)", "NUMBER_OF_PROCESSORS", "PROCESSOR_ARCHITECTURE",
             "FONTCONFIG_PATH", "FONTCONFIG_FILE", "TEXMFHOME", "TEXMFVAR", "TEXMFCONFIG"}
_SECRETISH = re.compile(r"(KEY|TOKEN|SECRET|PASSWORD|PASSWD|CREDENTIAL|COOKIE|AUTH)", re.I)


def clean_env(base: dict | None = None, extra: dict | None = None) -> dict:
    """Allow-list environment for renderer subprocesses: no API keys, tokens or cloud credentials."""
    base = os.environ if base is None else base
    env = {k: v for k, v in base.items() if k.upper() in _SAFE_ENV and not _SECRETISH.search(k)}
    env.update(extra or {})
    return env
