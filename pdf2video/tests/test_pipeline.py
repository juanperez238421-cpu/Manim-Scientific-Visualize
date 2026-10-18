import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pdf2video.ir import Document  # noqa: E402
from pdf2video.segment import detect  # noqa: E402
from pdf2video.validate import UnsafeExpression, safe_eval, validate  # noqa: E402

EX = ROOT / "examples"
TOPICS = ["physics", "algebra", "statistics", "chem_geometry", "scanned"]


@pytest.fixture(scope="session")
def work(tmp_path_factory):
    return tmp_path_factory.mktemp("p2v")


@pytest.mark.parametrize("topic", TOPICS)
def test_examples_validate(topic, work):
    rep, doc, S = validate(EX / topic / "spec.json", workdir=work / topic, verbose=False)
    assert rep["pass"], json.dumps(rep, default=str)[:2000]
    assert [p["id"] for p in rep["problems"]] == ["1", "2", "3"]


@pytest.mark.parametrize("topic", TOPICS)
def test_segmentation(topic, work):
    pdf = next((EX / topic).glob("*.pdf"))
    doc = Document(pdf, work / f"seg_{topic}")
    probs = detect(doc)
    assert [p.id for p in probs] == ["1", "2", "3"]
    assert all(p.text.startswith(f"{p.id}.") for p in probs)


def test_word_start_matching(work):
    doc = Document(EX / "physics" / "physics_worksheet.pdf", work / "ws")
    m = doc.find(1, "5 m/s")
    assert m is not None and "2.5" not in m.text  # '5 m/s' must not match inside '2.5 m/s'


def test_ocr_fuzzy(work):
    doc = Document(EX / "scanned" / "physics_scanned.pdf", work / "ocr")
    assert doc.pages[0].source == "ocr"
    for q in ("2.5 m/s²", "45 m", "600 m", "g = 9.8 m/s²"):
        assert doc.find(1, q) is not None, q


def _tamper(tmp, topic, fn):
    S = json.loads((EX / topic / "spec.json").read_text())
    fn(S)
    S["document"] = str((EX / topic / S["document"]).resolve())
    p = tmp / f"{topic}_tampered.json"
    p.write_text(json.dumps(S))
    return p


def test_wrong_answer_rejected(work):
    p = _tamper(work, "physics", lambda S: S["problems"][0]["answers"][0].update(value=9))
    rep, _, _ = validate(p, workdir=work / "t1", verbose=False)
    assert not rep["pass"]


def test_value_not_in_quote_rejected(work):
    p = _tamper(work, "physics", lambda S: S["problems"][0]["given"][1].update(value=3.5))
    rep, _, _ = validate(p, workdir=work / "t2", verbose=False)
    assert not rep["pass"]


def test_quote_not_on_page_rejected(work):
    p = _tamper(work, "algebra", lambda S: S["problems"][2]["given"][0].update(quote="(2, 5)"))
    rep, _, _ = validate(p, workdir=work / "t3", verbose=False)
    assert not rep["pass"]


def test_quote_outside_problem_rejected(work):
    # '45 m' exists on the page but in problem 2, not in problem 1
    p = _tamper(work, "physics", lambda S: S["problems"][0]["given"][2].update(quote="45 m", value=45))
    rep, _, _ = validate(p, workdir=work / "t4", verbose=False)
    assert not rep["pass"]


def test_missing_verification_rejected(work):
    p = _tamper(work, "statistics", lambda S: S["problems"][1].update(verify=[]))
    rep, _, _ = validate(p, workdir=work / "t5", verbose=False)
    assert not rep["pass"]


@pytest.mark.parametrize("expr", ["__import__('os').system('id')", "a.__class__", "S[0]", "[x for x in S]", "open('f')", "lambda: 1", "'text'"])
def test_unsafe_expressions(expr):
    with pytest.raises((UnsafeExpression, SyntaxError)):
        safe_eval(expr, {"a": 1, "S": [1, 2]})


def test_exact_arithmetic():
    import sympy as sp
    assert safe_eval("sqrt(2*45/(49/5))*49/5", {}) ** 2 == 882
    assert safe_eval("pstdev([18, 20, 22, 24, 26])", {}) == sp.sqrt(8)
    assert safe_eval("q1([3, 5, 7, 8, 9, 11, 13, 15]) == 6", {}) is True
