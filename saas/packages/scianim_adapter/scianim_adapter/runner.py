"""Job runner: PDF -> IR -> spec (model) -> validation -> render -> QA, driving the pdf2video engine.

The engine is invoked ONLY through its CLI with argv arrays (no shell), a scrubbed environment
(no API keys) and per-stage timeouts. Statuses are reported separately; `delivery_ready` is true only
when verification is `verified`, the render succeeded and the engine's video QA says PASS.

Known limitation: the engine writes to <engine_root>/build/<job_id>; the runner copies the
deliverables into <job_dir>/out and leaves the engine build folder for the caller to purge.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .guard import IntakeError, SpecRejected, check_pdf, clean_env, sanitize_spec
from .providers import ModelProvider, ProviderError
from .statuses import StageStatus as S
from .statuses import Verification as V

_JOB_ID = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


@dataclass
class JobConfig:
    engine_root: Path                      # the pdf2video project folder (contains the `pdf2video` package)
    python: str = sys.executable           # interpreter that has manim/pdfplumber/pymupdf/sympy installed
    quality: str = "qh"
    fps: int = 30
    render: bool = True                    # False = stop after validation (cheap, no LaTeX/Manim needed)
    max_pdf_mb: float = 25
    max_pages: int = 30
    analyze_timeout_s: int = 180
    validate_timeout_s: int = 180
    render_timeout_s: int = 3 * 3600
    profile: str = "delivery1080"          # preview480 | dev720 | delivery1080 -> P2V_PROFILE (QA tecnico diferenciado)
    cancel: object | None = None           # threading.Event: si se activa, el hijo (y sus nietos) se terminan
    on_stage: object | None = None         # callable(stage_name, status_value): progreso para el worker (nunca debe lanzar)


@dataclass
class JobResult:
    job_id: str
    stages: dict = field(default_factory=lambda: {k: S.NOT_RUN.value for k in
                         ("intake", "extract", "author", "validate", "render", "qa")})
    verification: str = V.UNSUPPORTED.value
    extraction: dict = field(default_factory=dict)
    problems: list = field(default_factory=list)       # per-problem validator verdicts
    model: dict = field(default_factory=dict)          # provider, model, prompt_version, usage
    timings_s: dict = field(default_factory=dict)
    artifacts: dict = field(default_factory=dict)
    qa: dict = field(default_factory=dict)
    errors: list = field(default_factory=list)
    delivery_ready: bool = False

    def to_dict(self):
        return asdict(self)


class JobCancelled(RuntimeError):
    """El usuario pidio cancelar: el proceso del motor fue terminado."""


PROFILES = {
    # perfil: (calidad manim, fps)  -- 480p/15 fps = borrador; 720p/30 = desarrollo; 1080p/30 = entrega
    "preview480": ("ql", 15),
    "dev720": ("qm", 30),
    "delivery1080": ("qh", 30),
}
RESOLUTION_PROFILE = {"480p": "preview480", "720p": "dev720", "1080p": "delivery1080"}


def profile_for(resolution: str) -> str:
    try:
        return RESOLUTION_PROFILE[resolution]
    except KeyError:
        raise ValueError(f"unsupported resolution {resolution!r}") from None


def _kill_tree(p: subprocess.Popen) -> None:
    """Termina el proceso y todos sus descendientes (manim lanza ffmpeg/latex/dvisvgm)."""
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True, timeout=30)
        else:
            os.killpg(p.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError, subprocess.SubprocessError, OSError):
        pass
    finally:
        try:
            p.kill()
        except OSError:
            pass


def _run(cfg: JobConfig, args: list[str], timeout: int, home: Path):
    cmd = [cfg.python, "-m", "pdf2video", *args]
    # UTF-8 explicito de extremo a extremo: PYTHONUTF8 hace que open()/Path.write_text() del hijo usen UTF-8 en vez de la
    # pagina de codigos ANSI de Windows (cp1252); PYTHONIOENCODING cubre stdio. No se oculta ningun error de decodificacion.
    env = clean_env(extra={"HOME": str(home), "PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8",
                           "PYTHONUTF8": "1", "P2V_PROFILE": cfg.profile})
    if cfg.cancel is None:
        return subprocess.run(cmd, cwd=cfg.engine_root, env=env, capture_output=True, text=True, encoding="utf-8",
                              errors="strict", timeout=timeout)
    if cfg.cancel.is_set():
        raise JobCancelled("cancelled before start")
    kw = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {"start_new_session": True}
    p = subprocess.Popen(cmd, cwd=cfg.engine_root, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                         encoding="utf-8", errors="strict", **kw)
    deadline = time.monotonic() + timeout
    while True:
        try:
            out, err = p.communicate(timeout=0.5)
            return subprocess.CompletedProcess(cmd, p.returncode, out, err)
        except subprocess.TimeoutExpired:
            if cfg.cancel.is_set():
                _kill_tree(p)
                p.communicate()
                raise JobCancelled("cancelled while running") from None
            if time.monotonic() > deadline:
                _kill_tree(p)
                p.communicate()
                raise subprocess.TimeoutExpired(cmd, timeout) from None


def _tail(s: str, n: int = 600) -> str:
    return (s or "")[-n:]


def run_job(pdf_path: str | Path, job_dir: str | Path, provider: ModelProvider, cfg: JobConfig,
            job_id: str, problem_ids: list[str] | None = None) -> JobResult:
    if not _JOB_ID.match(job_id):
        raise ValueError("job_id must match [A-Za-z0-9_-]{1,64}")
    res = JobResult(job_id=job_id)
    job_dir = Path(job_dir).resolve()
    (job_dir / "home").mkdir(parents=True, exist_ok=True)
    home = job_dir / "home"
    t_all = time.time()

    def stage(name, status):
        res.stages[name] = status.value if hasattr(status, "value") else status
        if cfg.on_stage is not None:
            try:
                cfg.on_stage(name, res.stages[name])
            except Exception:  # noqa: BLE001 - el reporte de progreso jamas debe romper el trabajo
                pass

    def clock(name, t0):
        res.timings_s[name] = round(time.time() - t0, 2)

    # ---- intake
    t0 = time.time()
    try:
        info = check_pdf(Path(pdf_path), max_mb=cfg.max_pdf_mb, max_pages=cfg.max_pages)
    except IntakeError as e:
        stage("intake", S.FAIL)
        res.errors.append({"stage": "intake", "message": str(e)})
        res.verification = V.UNSUPPORTED.value
        return res
    doc = job_dir / "document.pdf"          # fixed name: the user's file name is never used on disk
    shutil.copyfile(pdf_path, doc)
    res.extraction.update(sha256=info["sha256"], pages=info["pages"], size_bytes=info["size_bytes"])
    stage("intake", S.PASS)
    clock("intake", t0)

    # ---- extract (IR)
    t0 = time.time()
    try:
        r = _run(cfg, ["analyze", str(doc), "--out", str(job_dir / "analysis")], cfg.analyze_timeout_s, home)
    except subprocess.TimeoutExpired:
        stage("extract", S.FAIL)
        res.errors.append({"stage": "extract", "message": "analyze timed out"})
        return res
    clock("extract", t0)
    ir_path = job_dir / "analysis" / "ir.json"
    if r.returncode or not ir_path.exists():
        stage("extract", S.FAIL)
        res.errors.append({"stage": "extract", "message": _tail(r.stderr or r.stdout)})
        res.verification = V.UNSUPPORTED.value
        return res
    ir_text = ir_path.read_text(encoding="utf-8")
    ir = json.loads(ir_text)
    pages = ir.get("pages", [])
    res.extraction["page_sources"] = [p.get("source") for p in pages] if isinstance(pages, list) else []
    res.extraction["problems_detected"] = [p.get("id") for p in ir.get("problems", [])] if isinstance(ir.get("problems"), list) else None
    stage("extract", S.PASS)
    if not res.extraction["problems_detected"]:
        res.verification = V.UNSUPPORTED.value
        res.errors.append({"stage": "extract", "message": "no numbered problems detected"})
        return res

    # ---- author (model)
    t0 = time.time()
    try:
        sr = provider.author_spec(ir_text, problem_ids=problem_ids)
    except ProviderError as e:
        stage("author", S.FAIL)
        res.errors.append({"stage": "author", "message": str(e)})
        res.verification = V.REQUIRES_REVIEW.value
        return res
    finally:
        clock("author", t0)
    u = sr.usage
    res.model = {"provider": sr.provider, "model": sr.model, "prompt_version": sr.prompt_version,
                 "calls": u.calls, "input_tokens": u.input_tokens, "output_tokens": u.output_tokens, "cost_usd": u.cost_usd}
    if "error" in sr.spec or not sr.spec.get("problems"):
        stage("author", S.FAIL)
        res.verification = V.REQUIRES_REVIEW.value
        res.errors.append({"stage": "author", "message": f"model declined: {str(sr.spec.get('error'))[:300]}"})
        return res
    try:
        spec, dropped = sanitize_spec(sr.spec, document_name=doc.name, sha256=info["sha256"])
    except SpecRejected as e:
        stage("author", S.FAIL)
        res.verification = V.REQUIRES_REVIEW.value
        res.errors.append({"stage": "author", "message": f"spec rejected: {e}"})
        return res
    if dropped:
        res.errors.append({"stage": "author", "message": f"ignored non-schema keys: {dropped[:10]}", "severity": "warning"})
    spec_path = job_dir / "spec.json"
    spec_path.write_text(json.dumps(spec, indent=1, ensure_ascii=False), encoding="utf-8")
    stage("author", S.PASS)

    # ---- validate (deterministic gate; the model cannot override it)
    t0 = time.time()
    try:
        r = _run(cfg, ["validate", str(spec_path), "--name", job_id], cfg.validate_timeout_s, home)
    except subprocess.TimeoutExpired:
        stage("validate", S.FAIL)
        res.errors.append({"stage": "validate", "message": "validate timed out"})
        res.verification = V.REQUIRES_REVIEW.value
        return res
    clock("validate", t0)
    build = cfg.engine_root / "build" / job_id
    vpath = build / "validation.json"
    rep = json.loads(vpath.read_text(encoding="utf-8")) if vpath.exists() else {}
    res.problems = [{"id": p.get("id"), "pass": bool(p.get("pass"))} for p in rep.get("problems", [])]
    n_ok = sum(p["pass"] for p in res.problems)
    if rep.get("pass") and r.returncode == 0:
        res.verification = V.VERIFIED.value
        stage("validate", S.PASS)
    else:
        res.verification = V.PARTIALLY_VERIFIED.value if 0 < n_ok < len(res.problems) else V.REQUIRES_REVIEW.value
        stage("validate", S.FAIL)
        res.errors.append({"stage": "validate", "message": _tail(r.stdout or r.stderr, 1200)})
        return res

    out = job_dir / "out"
    out.mkdir(exist_ok=True)
    shutil.copyfile(spec_path, out / "spec.json")
    if vpath.exists():
        shutil.copyfile(vpath, out / "validation.json")
    res.artifacts.update(spec=str(out / "spec.json"), validation=str(out / "validation.json"))
    if not cfg.render:
        stage("render", S.SKIPPED); stage("qa", S.SKIPPED)
        clock("total", t_all)
        return res

    # ---- render + QA (engine `run` = validate -> render -> qa)
    t0 = time.time()
    try:
        r = _run(cfg, ["run", str(spec_path), "--name", job_id, "--quality", cfg.quality, "--fps", str(cfg.fps)],
                 cfg.render_timeout_s, home)
    except subprocess.TimeoutExpired:
        stage("render", S.FAIL)
        res.errors.append({"stage": "render", "message": f"render exceeded {cfg.render_timeout_s}s"})
        return res
    clock("render_and_qa", t0)
    qa_json = build / "qa" / "qa.json"
    if r.returncode == 0:
        stage("render", S.PASS)
    else:
        stage("render", S.FAIL if not (build / f"{job_id}.mp4").exists() else S.PASS)
        res.errors.append({"stage": "render", "message": f"engine exit {r.returncode}: {_tail(r.stdout or r.stderr, 1200)}"})
    if qa_json.exists():
        qa = json.loads(qa_json.read_text(encoding="utf-8"))
        res.qa = {"pass": bool(qa.get("pass")), "keys": sorted(qa.keys())}
        stage("qa", S.PASS if qa.get("pass") else S.FAIL)
        qdir = out / "qa"
        shutil.copytree(build / "qa", qdir, dirs_exist_ok=True)
        share = next(iter(sorted(qdir.glob("*_share.mp4"))), None)
        res.artifacts.update(qa_dir=str(qdir), share_mp4=str(share) if share else None,
                             master_mp4=str(build / f"{job_id}.mp4"))
    else:
        stage("qa", S.FAIL)
    res.delivery_ready = (res.verification == V.VERIFIED.value and res.stages["render"] == S.PASS.value
                          and res.stages["qa"] == S.PASS.value and bool(res.artifacts.get("share_mp4")))
    clock("total", t_all)
    (out / "result.json").write_text(json.dumps(res.to_dict(), indent=1, default=str), encoding="utf-8")
    return res
