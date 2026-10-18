"""Runner against the REAL pdf2video analyzer + validator (no render: cfg.render=False).
The model is a ReplayProvider MOCK, so these tests prove the adapter and the deterministic gates,
not the quality of any language model."""
import json
import shutil

import pytest

from scianim_adapter import ReplayProvider, run_job


def _run(tmp_path, cfg, pdf, spec, job_id):
    return run_job(pdf, tmp_path / job_id, ReplayProvider(spec), cfg, job_id=job_id)


def _cleanup(cfg, job_id):
    shutil.rmtree(cfg.engine_root / "build" / job_id, ignore_errors=True)


def test_happy_path_verified_without_render(tmp_path, cfg, physics):
    r = _run(tmp_path, cfg, physics[0], physics[1], "t_ok")
    try:
        assert r.verification == "verified"
        assert r.stages["intake"] == r.stages["extract"] == r.stages["author"] == r.stages["validate"] == "PASS"
        assert r.stages["render"] == r.stages["qa"] == "SKIPPED"
        assert r.delivery_ready is False                      # nothing rendered => never deliverable
        assert [p["pass"] for p in r.problems] == [True, True, True]
        assert r.extraction["sha256"].startswith("8e5df34a") and r.extraction["problems_detected"] == ["1", "2", "3"]
        spec = json.loads((tmp_path / "t_ok" / "spec.json").read_text())
        assert spec["document"] == "document.pdf"
        assert (tmp_path / "t_ok" / "document.pdf").exists()
    finally:
        _cleanup(cfg, "t_ok")


def test_wrong_answer_is_not_silently_accepted(tmp_path, cfg, physics):
    spec = json.loads(json.dumps(physics[1]))
    spec["problems"][0]["answers"][0]["value"] = 9          # true value is 8
    r = _run(tmp_path, cfg, physics[0], spec, "t_bad")
    try:
        assert r.verification == "partially_verified"       # problems 2 and 3 still pass
        assert [p["pass"] for p in r.problems] == [False, True, True]
        assert r.stages["validate"] == "FAIL" and r.stages["render"] == "NOT_RUN"
        assert r.delivery_ready is False
    finally:
        _cleanup(cfg, "t_bad")


def test_quote_not_on_page_is_rejected(tmp_path, cfg, physics):
    spec = json.loads(json.dumps(physics[1]))
    spec["problems"][0]["given"][1]["quote"] = "7.5 m/s²"   # not printed in the PDF
    spec["problems"][0]["given"][1]["value"] = 7.5
    r = _run(tmp_path, cfg, physics[0], spec, "t_quote")
    try:
        assert r.verification in {"partially_verified", "requires_review"} and r.delivery_ready is False
        assert r.stages["validate"] == "FAIL"
    finally:
        _cleanup(cfg, "t_quote")


def test_model_declining_goes_to_review(tmp_path, cfg, physics):
    r = _run(tmp_path, cfg, physics[0], {"error": "figure unreadable", "problems": []}, "t_decl")
    assert r.verification == "requires_review" and r.stages["author"] == "FAIL"
    assert r.stages["validate"] == "NOT_RUN"
    _cleanup(cfg, "t_decl")


def test_dangerous_tex_stops_before_engine_validate(tmp_path, cfg, physics):
    spec = json.loads(json.dumps(physics[1]))
    spec["problems"][0]["steps"][0]["tex"] = r"\input{/etc/passwd}"
    r = _run(tmp_path, cfg, physics[0], spec, "t_tex")
    assert r.verification == "requires_review" and "spec rejected" in r.errors[-1]["message"]
    assert r.stages["validate"] == "NOT_RUN"
    assert not (cfg.engine_root / "build" / "t_tex").exists()


def test_corrupt_pdf_never_reaches_engine(tmp_path, cfg, physics):
    bad = tmp_path / "bad.pdf"
    bad.write_bytes(b"%PDF-1.4\n" + b"\x00junk" * 100)
    r = _run(tmp_path, cfg, bad, physics[1], "t_corrupt")
    assert r.stages["intake"] == "FAIL" and r.stages["extract"] == "NOT_RUN" and r.verification == "unsupported"
    assert not (cfg.engine_root / "build" / "t_corrupt").exists()


def test_bad_job_id_rejected(tmp_path, cfg, physics):
    with pytest.raises(ValueError):
        run_job(physics[0], tmp_path / "x", ReplayProvider(physics[1]), cfg, job_id="../evil")


def test_user_filename_never_used_on_disk(tmp_path, cfg, physics):
    evil = tmp_path / "a;touch pwned.pdf"
    shutil.copyfile(physics[0], evil)
    r = _run(tmp_path, cfg, evil, physics[1], "t_name")
    try:
        assert r.verification == "verified"
        assert not (tmp_path / "pwned.pdf").exists() and not (cfg.engine_root / "pwned.pdf").exists()
    finally:
        _cleanup(cfg, "t_name")
