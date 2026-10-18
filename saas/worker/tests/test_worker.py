"""Pruebas del worker con una API falsa (sin red, sin Manim). El recorrido real está en scripts/e2e_local.py."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import httpx
import pytest

from animotion_worker import service as S
from animotion_worker.api import ApiError, LeaseLost, WorkerApi
from animotion_worker.config import WorkerSettings
from scianim_adapter import JobCancelled
from scianim_adapter.runner import JobResult


class FakeApi:
    def __init__(self):
        self.calls = []
        self.puts = []

    def stage(self, job, stage, status, pct):
        self.calls.append(("stage", stage, status, pct))
        return "ok"

    def download(self, url, dest, sha, max_bytes):
        Path(dest).write_bytes(b"%PDF-1.4 fake")

    def upload(self, url, path):
        self.puts.append((url, Path(path).name))

    def complete(self, job, video, delivery, qa):
        self.calls.append(("complete", video, delivery, qa))
        return {"final_credits": 7}

    def fail(self, job, code, message, delivery):
        self.calls.append(("fail", code, message, delivery))
        return {"final_credits": 0}

    def confirm_cancel(self, job):
        self.calls.append(("confirm_cancel",))
        return {}

    def heartbeat(self, job):
        return "ok"


def settings(tmp_path, **kw):
    base = dict(api_url="http://x", worker_token="t" * 30, worker_id="w-test", engine_root=tmp_path / "eng", engine_python="",
                work_dir=tmp_path / "work", provider="replay", replay_spec=None, poll_seconds=0.1, max_pdf_mb=25, max_pages=30,
                model="", max_in=1, max_out=1, budget_usd=None, price_in=None, price_out=None, max_request_usd=None,
                budget_journal="WAL", budget_db=tmp_path / "b.sqlite3", render_timeout_s=60)
    base.update(kw)
    return WorkerSettings(**base)


def job(resolution="480p"):
    return {"id": "11111111-1111-1111-1111-111111111111", "kind": "solution_video", "config": {"resolution": resolution},
            "attempt": 1, "lease_seconds": 120,
            "pdf": {"url": "http://x/pdf", "sha256": "a" * 64, "size_bytes": 10, "pages": 1},
            "outputs": {"video_put_url": "http://x/v", "share_put_url": "http://x/s"}}


def make_mp4(path: Path, size="854x480", fps=15, secs=2):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=white:s={size}:r={fps}:d={secs}",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(path)], check=True)


@pytest.fixture
def worker(tmp_path):
    (tmp_path / "eng").mkdir()
    api = FakeApi()
    w = S.Worker(settings(tmp_path), api, provider_factory=lambda s: object(), log=lambda *_: None)
    return w, api, tmp_path


def fake_run(stages, *, verification="verified", ready=False, artifacts=None, errors=None, model=None, capture=None):
    def _run(pdf, jd, provider, cfg, job_id, problem_ids=None):
        if capture is not None:
            capture["cfg"] = cfg
        for name, st in stages:
            cfg.on_stage(name, st)
        r = JobResult(job_id=job_id)
        r.stages.update({k: v for k, v in stages})
        r.verification = verification
        r.delivery_ready = ready
        r.artifacts = artifacts or {}
        r.errors = errors or []
        r.model = model or {"provider": "replay-mock", "model": "none"}
        r.qa = {"pass": ready}
        return r
    return _run


ALL_PASS = [("intake", "PASS"), ("extract", "PASS"), ("author", "PASS"), ("validate", "PASS"), ("render", "PASS"), ("qa", "PASS")]


def test_stage_progress_is_reported_in_order(worker, monkeypatch):
    w, api, tmp = worker
    monkeypatch.setattr(S, "run_job", fake_run(ALL_PASS, ready=False, verification="requires_review"))
    w.process(job())
    st = [c for c in api.calls if c[0] == "stage"]
    assert st[0] == ("stage", "extract", "running", 2)
    names = [(c[1], c[2]) for c in st]
    assert names == [("extract", "running"), ("extract", "succeeded"), ("script", "running"), ("script", "succeeded"),
                     ("render_manim", "running"), ("render_manim", "succeeded"), ("compose", "running"), ("compose", "succeeded")]


@pytest.mark.parametrize("res,quality,fps,profile", [("480p", "ql", 15, "preview480"), ("720p", "qm", 30, "dev720"),
                                                      ("1080p", "qh", 30, "delivery1080")])
def test_resolution_selects_profile(worker, monkeypatch, res, quality, fps, profile):
    w, api, tmp = worker
    cap = {}
    monkeypatch.setattr(S, "run_job", fake_run(ALL_PASS, ready=False, verification="requires_review", capture=cap))
    w.process(job(res))
    c = cap["cfg"]
    assert (c.quality, c.fps, c.profile) == (quality, fps, profile) and c.cancel is not None


@pytest.mark.parametrize("failed_stage,code", [("intake", "invalid_pdf"), ("extract", "extraction_failed"), ("author", "solution_failed"),
                                               ("validate", "verification_failed"), ("render", "render_failed"), ("qa", "qa_failed")])
def test_undeliverable_job_fails_with_specific_code_and_no_traceback(worker, monkeypatch, failed_stage, code):
    w, api, tmp = worker
    order = ["intake", "extract", "author", "validate", "render", "qa"]
    stages = [(n, "PASS" if order.index(n) < order.index(failed_stage) else ("FAIL" if n == failed_stage else "NOT_RUN")) for n in order]
    err = [{"stage": failed_stage, "message": "Traceback (most recent call last):\n  File C:\\secret\\x.py\n" + "x" * 900}]
    monkeypatch.setattr(S, "run_job", fake_run(stages, verification="requires_review", errors=err))
    w.process(job())
    f = [c for c in api.calls if c[0] == "fail"][0]
    assert f[1] == code and not any(c[0] == "complete" for c in api.calls)
    msg = f[3]["errors"][0]["message"]
    assert len(msg) <= 240 and "\n" not in msg
    assert f[3]["mock"] is True and f[3]["delivery_ready"] is False
    assert not (tmp / "work" / job()["id"]).exists()          # limpieza del directorio de trabajo


def test_cancel_confirms_and_does_not_fail(worker, monkeypatch):
    w, api, tmp = worker

    def boom(*a, **k):
        raise JobCancelled("x")
    monkeypatch.setattr(S, "run_job", boom)
    w.process(job())
    assert ("confirm_cancel",) in api.calls and not any(c[0] in ("fail", "complete") for c in api.calls)


def test_unexpected_exception_fails_job_with_generic_message(worker, monkeypatch):
    w, api, tmp = worker
    monkeypatch.setattr(S, "run_job", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("secret path C:\\Users\\x")))
    w.process(job())
    f = [c for c in api.calls if c[0] == "fail"][0]
    assert f[1] == "worker_error" and "secret" not in json.dumps(f)


def test_provider_error_fails_without_charge(worker, monkeypatch):
    from scianim_adapter import ProviderError
    w, api, tmp = worker
    monkeypatch.setattr(S, "run_job", lambda *a, **k: (_ for _ in ()).throw(ProviderError("budget exhausted")))
    w.process(job())
    f = [c for c in api.calls if c[0] == "fail"][0]
    assert f[1] == "solution_failed" and f[3]["delivery_ready"] is False


def _delivered(tmp, size="854x480", fps=15):
    out = tmp / "media"
    out.mkdir(exist_ok=True)
    make_mp4(out / "m.mp4", size, fps)
    shutil.copy(out / "m.mp4", out / "s.mp4")
    return {"master_mp4": str(out / "m.mp4"), "share_mp4": str(out / "s.mp4")}


@pytest.mark.skipif(not shutil.which("ffmpeg"), reason="ffmpeg ausente")
def test_verified_video_is_probed_uploaded_and_completed(worker, monkeypatch):
    w, api, tmp = worker
    monkeypatch.setattr(S, "run_job", fake_run(ALL_PASS, ready=True, artifacts=_delivered(tmp)))
    w.process(job("480p"))
    c = [x for x in api.calls if x[0] == "complete"][0]
    video, delivery = c[1], c[2]
    assert (video["width"], video["height"], video["fps"]) == (854, 480, 15) and len(video["sha256"]) == 64
    assert video["size_bytes"] > 0 and video["duration_seconds"] >= 1.5
    assert [n for _, n in api.puts] == ["m.mp4", "s.mp4"]
    assert delivery["delivery_ready"] and delivery["verification"] == "verified" and delivery["profile"] == "preview480"
    assert ("stage", "upload", "succeeded", 99) in api.calls


@pytest.mark.skipif(not shutil.which("ffmpeg"), reason="ffmpeg ausente")
def test_wrong_resolution_for_profile_is_not_delivered(worker, monkeypatch):
    w, api, tmp = worker
    monkeypatch.setattr(S, "run_job", fake_run(ALL_PASS, ready=True, artifacts=_delivered(tmp, "1280x720", 30)))
    w.process(job("480p"))                 # pidió 480p pero el motor produjo 720p/30
    assert [x for x in api.calls if x[0] == "fail"][0][1] == "qa_failed" and not any(x[0] == "complete" for x in api.calls)
    assert api.puts == []


@pytest.mark.skipif(not shutil.which("ffmpeg"), reason="ffmpeg ausente")
def test_corrupt_video_is_not_delivered(worker, monkeypatch):
    w, api, tmp = worker
    art = _delivered(tmp)
    data = Path(art["master_mp4"]).read_bytes()
    Path(art["master_mp4"]).write_bytes(data[: len(data) // 2])     # truncado: ffprobe/decodificación deben detectarlo
    monkeypatch.setattr(S, "run_job", fake_run(ALL_PASS, ready=True, artifacts=art))
    w.process(job("480p"))
    assert not any(x[0] == "complete" for x in api.calls) and [x for x in api.calls if x[0] == "fail"]


# ---------------------------------------------------------------- cliente HTTP
def api_with(handler):
    return WorkerApi("http://api", "tok" * 10, "w-test", client=httpx.Client(transport=httpx.MockTransport(handler)))


def test_client_maps_lease_lost_and_sends_bearer():
    seen = {}

    def h(req):
        seen["auth"] = req.headers["authorization"]
        return httpx.Response(409, json={"code": "lease_lost", "message": "x"})
    with pytest.raises(LeaseLost):
        api_with(h).heartbeat("j")
    assert seen["auth"].startswith("Bearer ")


def test_client_retries_5xx_then_succeeds(monkeypatch):
    monkeypatch.setattr("animotion_worker.api.time.sleep", lambda s: None)
    n = {"i": 0}

    def h(req):
        n["i"] += 1
        return httpx.Response(503 if n["i"] < 3 else 200, json={"job": None})
    assert api_with(h).claim() is None and n["i"] == 3


def test_client_download_verifies_sha256(tmp_path):
    import hashlib
    data = b"%PDF-1.4 hola"
    ok = hashlib.sha256(data).hexdigest()
    a = api_with(lambda r: httpx.Response(200, content=data))
    a.download("http://x/pdf", tmp_path / "a.pdf", ok, 1000)
    with pytest.raises(ApiError) as e:
        a.download("http://x/pdf", tmp_path / "b.pdf", "0" * 64, 1000)
    assert e.value.code == "sha256_mismatch"
    with pytest.raises(ApiError) as e:
        a.download("http://x/pdf", tmp_path / "c.pdf", ok, 5)
    assert e.value.code == "too_large"


def test_config_validation_flags_missing_pieces(tmp_path, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    errs = settings(tmp_path, worker_token="", provider="anthropic").validate()
    assert any("WORKER_TOKEN" in e for e in errs) and any("ANTHROPIC_API_KEY" in e for e in errs)
    assert any("motor" in e for e in errs)
