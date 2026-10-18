import json

import pytest

from scianim_adapter import IntakeError, SpecRejected, check_pdf, clean_env, sanitize_spec

PHYSICS_SHA = "8e5df34afc75a61140ceba6d66472b3cdf944aff9032f6f90580494976477b09"


def test_real_pdf_accepted_with_sha(physics):
    info = check_pdf(physics[0])
    assert info["sha256"] == PHYSICS_SHA and info["pages"] == 1


@pytest.mark.parametrize("payload,why", [
    (b"", "empty"),
    (b"GIF89a....", "signature"),
    (b"%PDF-1.4\n" + b"\x00garbage" * 50, "corrupt"),
])
def test_bad_files_rejected(tmp_path, payload, why):
    p = tmp_path / "x.pdf"
    p.write_bytes(payload)
    with pytest.raises(IntakeError):
        check_pdf(p)


def test_size_and_page_limits(physics):
    with pytest.raises(IntakeError, match="larger"):
        check_pdf(physics[0], max_mb=0.001)
    with pytest.raises(IntakeError, match="pages"):
        check_pdf(physics[0], max_pages=0)


def test_missing_file(tmp_path):
    with pytest.raises(IntakeError):
        check_pdf(tmp_path / "nope.pdf")


def test_sanitize_forces_document_and_drops_unknown_keys(physics):
    spec = json.loads(json.dumps(physics[1]))
    spec["document"] = "../../etc/passwd"
    spec["shell"] = "rm -rf /"
    spec["problems"][0]["python"] = "import os"
    clean, dropped = sanitize_spec(spec, document_name="document.pdf", sha256=PHYSICS_SHA)
    assert clean["document"] == "document.pdf" and clean["sha256"] == PHYSICS_SHA
    assert "shell" not in clean and "python" not in clean["problems"][0]
    assert "spec.shell" in dropped and "problems[0].python" in dropped


def test_all_engine_examples_pass_sanitizer_without_false_positives(engine_root):
    for sp in (engine_root / "examples").glob("*/spec.json"):
        spec = json.loads(sp.read_text(encoding="utf-8"))
        clean, _ = sanitize_spec(spec, document_name="document.pdf", sha256="0" * 64)
        assert clean["problems"], sp


@pytest.mark.parametrize("tex", [
    r"\input{/etc/passwd}", r"\include{secret}", r"\openin5=/etc/passwd", r"\immediate\write18{id}",
    r"x = \catcode`\~=0", r"\usepackage{shellesc}", r"\write-1{x}", r"\csname input\endcsname",
])
def test_dangerous_tex_rejected(physics, tex):
    spec = json.loads(json.dumps(physics[1]))
    spec["problems"][0]["steps"][0]["tex"] = tex
    with pytest.raises(SpecRejected):
        sanitize_spec(spec, document_name="document.pdf", sha256="0" * 64)


def test_dangerous_tex_in_chip_rejected(physics):
    spec = json.loads(json.dumps(physics[1]))
    spec["problems"][0]["given"][1]["chip"] = r"\input{/etc/hostname}"
    with pytest.raises(SpecRejected):
        sanitize_spec(spec, document_name="document.pdf", sha256="0" * 64)


def test_non_object_and_missing_problems_rejected():
    with pytest.raises(SpecRejected):
        sanitize_spec([], document_name="d.pdf", sha256="0")
    with pytest.raises(SpecRejected):
        sanitize_spec({"title": "x"}, document_name="d.pdf", sha256="0")


def test_clean_env_drops_secrets_keeps_path():
    base = {"PATH": "/usr/bin", "ANTHROPIC_API_KEY": "sk-x", "AWS_SECRET_ACCESS_KEY": "y",
            "CLERK_SECRET_KEY": "z", "R2_TOKEN": "t", "HOME": "/root", "LANG": "C.UTF-8"}
    env = clean_env(base, extra={"HOME": "/job/home"})
    assert env["PATH"] == "/usr/bin" and env["HOME"] == "/job/home" and env["LANG"] == "C.UTF-8"
    assert not any("KEY" in k or "TOKEN" in k or "SECRET" in k for k in env)
