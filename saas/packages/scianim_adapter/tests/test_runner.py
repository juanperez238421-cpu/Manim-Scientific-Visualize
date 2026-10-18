"""Runner against the REAL pdf2video analyzer + validator (no render: cfg.render=False).
The model is a ReplayProvider MOCK, so these tests prove the adapter and the deterministic gates,
not the quality of any language model."""
import json
import os
import shutil
import subprocess
import sys

import pytest

from scianim_adapter import JobConfig, ReplayProvider, run_job
from scianim_adapter import runner as R


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
        spec = json.loads((tmp_path / "t_ok" / "spec.json").read_text(encoding="utf-8"))
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


# ---------------------------------------------------------------- M2: perfiles y cancelación
def test_profiles_map_resolution_to_quality_fps_and_qa_profile():
    from scianim_adapter import PROFILES, profile_for
    assert profile_for("480p") == "preview480" and PROFILES["preview480"] == ("ql", 15)
    assert profile_for("720p") == "dev720" and PROFILES["dev720"] == ("qm", 30)
    assert profile_for("1080p") == "delivery1080" and PROFILES["delivery1080"] == ("qh", 30)
    with pytest.raises(ValueError):
        profile_for("4k")


def test_profile_is_forwarded_to_engine_env(monkeypatch, tmp_path, cfg):
    seen = {}
    monkeypatch.setattr(R.subprocess, "run", lambda cmd, **kw: seen.update(kw) or subprocess.CompletedProcess(cmd, 0, "", ""))
    cfg.profile = "dev720"
    R._run(cfg, ["qa", "x"], 5, tmp_path)
    assert seen["env"]["P2V_PROFILE"] == "dev720"


def _pid_alive(pid: int) -> bool:
    if os.name == "nt":                      # os.kill(pid, 0) en Windows TERMINA el proceso: se usa tasklist
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True).stdout
        return str(pid) in out
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    # zombi sin reaper (p. ej. PID 1 en contenedores) cuenta como muerto
    try:
        return "Z" not in open(f"/proc/{pid}/stat").read().split(")")[-1].split()[0]
    except OSError:
        return False


def test_cancel_kills_child_process_tree(tmp_path):
    """Un 'motor' falso que lanza un nieto y duerme: al cancelar mueren ambos y se lanza JobCancelled."""
    import threading
    import time
    from scianim_adapter import JobCancelled
    eng = tmp_path / "eng"
    (eng / "pdf2video").mkdir(parents=True)
    pidfile = tmp_path / "grandchild.pid"
    (eng / "pdf2video" / "__main__.py").write_text(
        "import subprocess, sys, time, pathlib\n"
        f"g = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])\n"
        f"pathlib.Path(r'{pidfile}').write_text(str(g.pid))\n"
        "time.sleep(60)\n", encoding="utf-8")
    ev = threading.Event()
    cfg = JobConfig(engine_root=eng, python=sys.executable, cancel=ev)
    threading.Timer(1.5, ev.set).start()
    t0 = time.time()
    with pytest.raises(JobCancelled):
        R._run(cfg, ["analyze", "x"], 120, tmp_path)
    assert time.time() - t0 < 15
    gpid = int(pidfile.read_text())
    time.sleep(0.3)
    assert not _pid_alive(gpid), "el nieto sigue vivo"


def test_cancel_before_start_never_spawns(tmp_path):
    import threading
    from scianim_adapter import JobCancelled
    ev = threading.Event()
    ev.set()
    with pytest.raises(JobCancelled):
        R._run(JobConfig(engine_root=tmp_path, python=sys.executable, cancel=ev), ["analyze", "x"], 5, tmp_path)
