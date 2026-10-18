"""Ciclo del worker: reclamar -> descargar PDF -> adaptador/motor -> verificar MP4 -> subir -> completar/fallar.

Garantías:
  * Un job a la vez (concurrencia 1 hasta medir el hardware).
  * Latido en hilo aparte; si la API pide cancelar, el árbol de procesos del motor se termina.
  * Si se pierde el lease, el worker abandona SIN tocar el estado (otro worker es el dueño).
  * Solo se completa un job con verificación 'verified', render PASS, QA PASS, MP4 decodificado completo y resolución
    acorde al perfil; todo lo demás se cierra con /fail (reembolso total: no se cobra lo no entregado).
  * Nunca se envían tracebacks ni rutas a la API: solo códigos y mensajes cortos.
"""
from __future__ import annotations

import json
import shutil
import threading
import time
import traceback
from pathlib import Path

from scianim_adapter import (AIBudgetGuard, AnthropicProvider, JobCancelled, JobConfig, ProviderError, ReplayProvider,
                             profile_for, run_job)
from scianim_adapter.runner import PROFILES

from .api import ApiError, LeaseLost, WorkerApi
from .config import WorkerSettings
from .media import full_decode_errors, probe, sha256_file

# etapa del adaptador -> (etapa de la API, ¿cierra la etapa de la API?, progreso al cerrar)
STAGE_MAP = {
    "intake": ("extract", False, 5), "extract": ("extract", True, 15),
    "author": ("script", False, 35), "validate": ("script", True, 45),
    "render": ("render_manim", True, 90), "qa": ("compose", True, 95),
}
NEXT_API_STAGE = {"extract": "script", "script": "render_manim", "render_manim": "compose"}
FAIL_BY_STAGE = {
    "intake": ("invalid_pdf", "El PDF no cumple los requisitos de procesamiento."),
    "extract": ("extraction_failed", "No se pudieron extraer problemas numerados del documento."),
    "author": ("solution_failed", "No se pudo generar una solución estructurada."),
    "validate": ("verification_failed", "La solución no superó la verificación independiente; no se entrega."),
    "render": ("render_failed", "Falló la animación del video."),
    "qa": ("qa_failed", "El video no superó el control de calidad."),
}
SAFE = lambda s: (str(s) or "")[:240].replace("\r", " ").replace("\n", " ")  # noqa: E731


def build_provider(s: WorkerSettings):
    if s.provider == "replay":
        return ReplayProvider(json.loads(s.replay_spec.read_text(encoding="utf-8")))
    guard = AIBudgetGuard(s.budget_db, budget_usd=s.budget_usd, price_in_per_mtok=s.price_in,
                          price_out_per_mtok=s.price_out, max_request_usd=s.max_request_usd, journal_mode=s.budget_journal)
    return AnthropicProvider(model=s.model, max_input_tokens=s.max_in, max_output_tokens=s.max_out,
                             price_in_per_mtok=s.price_in, price_out_per_mtok=s.price_out, guard=guard,
                             prompt_path=s.engine_root / "prompts" / "spec_author.md")


class Worker:
    def __init__(self, settings: WorkerSettings, api: WorkerApi, provider_factory=build_provider, log=print):
        self.s, self.api, self.provider_factory, self.log = settings, api, provider_factory, log
        self.s.work_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------ bucle
    def run_forever(self, stop: threading.Event):
        self.log(f"worker {self.s.worker_id} -> {self.s.api_url} (proveedor: {self.s.provider})")
        while not stop.is_set():
            try:
                if not self.run_once():
                    stop.wait(self.s.poll_seconds)
            except ApiError as e:
                self.log(f"API no disponible: {e}")
                stop.wait(max(self.s.poll_seconds, 5))
            except Exception as e:  # noqa: BLE001
                self.log(f"error inesperado del bucle: {type(e).__name__}")
                stop.wait(5)

    def run_once(self) -> bool:
        job = self.api.claim()
        if job is None:
            return False
        self.process(job)
        return True

    # ------------------------------------------------------------ un job
    def process(self, job: dict):
        jid = job["id"]
        cancel, lost = threading.Event(), threading.Event()
        done = threading.Event()
        beat = threading.Thread(target=self._heartbeat, args=(jid, job.get("lease_seconds", 120), cancel, lost, done), daemon=True)
        beat.start()
        jd = self.s.work_dir / jid
        t0 = time.time()
        self.log(f"[{jid}] reclamado (intento {job.get('attempt')})")
        try:
            self._process(job, jd, cancel, lost)
        except LeaseLost:
            self.log(f"[{jid}] lease perdido: abandono sin modificar estado")
        except Exception as e:  # noqa: BLE001
            self.log(f"[{jid}] excepción {type(e).__name__}: {SAFE(e)}\n{traceback.format_exc()[-1500:]}")
            if not lost.is_set():
                try:
                    self.api.fail(jid, "worker_error", "Error interno del worker.", {"delivery_ready": False, "error": type(e).__name__})
                except Exception:  # noqa: BLE001
                    pass
        finally:
            done.set()
            beat.join(timeout=5)
            shutil.rmtree(jd, ignore_errors=True)
            shutil.rmtree(self.s.engine_root / "build" / jid, ignore_errors=True)
            self.log(f"[{jid}] terminado en {time.time() - t0:.1f}s")

    def _heartbeat(self, jid, lease, cancel, lost, done):
        interval = max(2.0, lease / 3)
        while not done.wait(interval):
            try:
                if self.api.heartbeat(jid) == "cancel_requested":
                    cancel.set()
            except LeaseLost:
                lost.set()
                cancel.set()
                return
            except ApiError:
                continue                     # la API puede reiniciarse; el lease aún no vence

    def _process(self, job, jd: Path, cancel: threading.Event, lost: threading.Event):
        jid, cfg_in = job["id"], job.get("config") or {}
        resolution = cfg_in.get("resolution", "1080p")
        profile = profile_for(resolution)
        quality, fps = PROFILES[profile]
        shutil.rmtree(jd, ignore_errors=True)
        jd.mkdir(parents=True)
        pdf = jd / "input.pdf"
        self.api.stage(jid, "extract", "running", 2)
        self.api.download(job["pdf"]["url"], pdf, job["pdf"]["sha256"], int(self.s.max_pdf_mb * 1024 * 1024) + 1)

        current = {"api": "extract"}

        def on_stage(name, status):
            if lost.is_set():
                return
            m = STAGE_MAP.get(name)
            if not m:
                return
            api_stage, closes, pct = m
            status = str(status).lower()                 # el adaptador publica PASS / FAIL / SKIPPED
            try:
                if status == "fail":
                    self.api.stage(jid, api_stage, "failed", pct)
                elif status == "pass" and closes:
                    self.api.stage(jid, api_stage, "succeeded", pct)
                    nxt = NEXT_API_STAGE.get(api_stage)
                    if nxt:
                        self.api.stage(jid, nxt, "running", pct)
                        current["api"] = nxt
            except LeaseLost:
                lost.set()
                cancel.set()
            except ApiError as e:                        # el progreso es informativo: no aborta el job, pero se registra
                self.log(f"[{jid}] no se pudo reportar la etapa {api_stage}: {e}")

        cfg = JobConfig(engine_root=self.s.engine_root, python=self.s.engine_python or __import__("sys").executable,
                        quality=quality, fps=fps, profile=profile, max_pdf_mb=self.s.max_pdf_mb, max_pages=self.s.max_pages,
                        render_timeout_s=self.s.render_timeout_s, cancel=cancel, on_stage=on_stage)
        try:
            provider = self.provider_factory(self.s)
            res = run_job(pdf, jd, provider, cfg, jid)
        except JobCancelled:
            if lost.is_set():
                raise LeaseLost() from None
            self.log(f"[{jid}] cancelado por el usuario")
            self.api.confirm_cancel(jid)
            return
        except ProviderError as e:
            self.api.fail(jid, "solution_failed", "El proveedor de IA no pudo producir una solución.",
                          {"delivery_ready": False, "verification": "requires_review", "provider_error": SAFE(e)})
            return
        if lost.is_set():
            raise LeaseLost()
        delivery = self._delivery(res, profile)
        if not res.delivery_ready:
            code, msg = self._classify(res)
            self.api.fail(jid, code, msg, delivery)
            return
        self._deliver(job, res, delivery, profile, resolution)

    # ------------------------------------------------------------ entrega
    def _deliver(self, job, res, delivery, profile, resolution):
        jid = job["id"]
        master, share = Path(res.artifacts["master_mp4"]), Path(res.artifacts["share_mp4"])
        info = probe(master)
        want_h = int(resolution.rstrip("p"))
        errs = []
        if info["codec"] != "h264" or info["pix_fmt"] != "yuv420p":
            errs.append("codec/pix_fmt inesperado")
        if info["height"] != want_h:
            errs.append(f"altura {info['height']} != {want_h}")
        if info["fps"] != PROFILES[profile][1]:
            errs.append(f"fps {info['fps']} != {PROFILES[profile][1]}")
        dec = full_decode_errors(master)
        if dec:
            errs.append("errores de decodificación")
        if info["duration_seconds"] < 1:
            errs.append("duración < 1 s")
        qa = {"ffprobe": info, "decode_errors": dec, "engine_qa_pass": bool(res.qa.get("pass")), "profile": profile,
              "problems_checked": errs}
        if errs:
            delivery["delivery_ready"] = False
            self.api.fail(jid, "qa_failed", "El video no superó el control de calidad.", {**delivery, "qa_local": qa})
            return
        self.api.stage(jid, "upload", "running", 96)
        self.api.upload(job["outputs"]["video_put_url"], master)
        has_share = share.is_file() and share.stat().st_size > 0
        if has_share:
            self.api.upload(job["outputs"]["share_put_url"], share)
        self.api.stage(jid, "upload", "succeeded", 99)
        video = {"duration_seconds": info["duration_seconds"], "width": info["width"], "height": info["height"],
                 "fps": info["fps"], "size_bytes": master.stat().st_size, "sha256": sha256_file(master),
                 "share_size_bytes": share.stat().st_size if has_share else None}
        out = self.api.complete(jid, video, delivery, qa)
        self.log(f"[{jid}] ENTREGADO {info['width']}x{info['height']}@{info['fps']} {info['duration_seconds']:.1f}s "
                 f"créditos={out.get('final_credits')}")

    @staticmethod
    def _classify(res) -> tuple[str, str]:
        for st in ("intake", "extract", "author", "validate", "render", "qa"):
            if res.stages.get(st) not in ("PASS", "SKIPPED"):
                return FAIL_BY_STAGE[st]
        return "job_failed", "El job no cumplió las condiciones de entrega."

    def _delivery(self, res, profile) -> dict:
        m = res.model or {}
        return {
            "delivery_ready": bool(res.delivery_ready), "verification": res.verification, "profile": profile,
            "stages": dict(res.stages), "problems": res.problems,
            "extraction": {k: res.extraction.get(k) for k in ("sha256", "pages", "problems_detected")},
            "model": {k: m.get(k) for k in ("provider", "model", "prompt_version", "calls", "input_tokens", "output_tokens", "cost_usd")},
            "mock": (m.get("provider") == "replay-mock"), "timings_s": res.timings_s, "qa_engine_pass": bool(res.qa.get("pass")),
            "errors": [{"stage": e.get("stage"), "message": SAFE(e.get("message", "")), "severity": e.get("severity", "error")} for e in res.errors][:10],
            "worker_id": self.s.worker_id,
        }
