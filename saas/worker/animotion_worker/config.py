"""Configuración del worker local (desde .env / entorno). La clave de Anthropic vive SOLO aquí, nunca en la API."""
from __future__ import annotations

import os
import platform
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load_dotenv():
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env", override=False)
    except ImportError:
        pass


def _path(v: str | None, default: str) -> Path:
    p = Path(v or default)
    return p if p.is_absolute() else (ROOT / p).resolve()


@dataclass(frozen=True)
class WorkerSettings:
    api_url: str
    worker_token: str
    worker_id: str
    engine_root: Path
    engine_python: str
    work_dir: Path
    provider: str                  # "anthropic" | "replay"
    replay_spec: Path | None
    poll_seconds: float
    max_pdf_mb: float
    max_pages: int
    model: str
    max_in: int
    max_out: int
    budget_usd: float | None
    price_in: float | None
    price_out: float | None
    max_request_usd: float | None
    budget_journal: str
    budget_db: Path
    render_timeout_s: int

    @staticmethod
    def from_env() -> "WorkerSettings":
        _load_dotenv()
        e = os.environ.get

        def f(name):
            v = (e(name) or "").strip()
            return float(v) if v else None
        py = (e("ENGINE_PYTHON") or "").strip()
        replay = (e("ANIMOTION_REPLAY_SPEC") or "").strip()
        return WorkerSettings(
            api_url=(e("SAAS_API_URL") or "http://127.0.0.1:8000").rstrip("/"),
            worker_token=(e("WORKER_TOKEN") or "").strip(),
            worker_id=(e("WORKER_ID") or f"local-{platform.node() or 'pc'}-1").replace(" ", "-")[:64],
            engine_root=_path(e("ENGINE_ROOT"), "./engine/pdf2video"),
            engine_python=str(_path(py, py)) if py else "",
            work_dir=_path(e("WORKER_WORK_DIR"), "./storage/worker"),
            provider=(e("ANIMOTION_PROVIDER") or "anthropic").strip().lower(),
            replay_spec=_path(replay, replay) if replay else None,
            poll_seconds=float(e("WORKER_POLL_SECONDS") or 3),
            max_pdf_mb=float(e("MAX_PDF_MB") or 25),
            max_pages=int(e("MAX_PAGES") or 30),
            model=(e("ANIMOTION_MODEL") or "").strip(),
            max_in=int(e("ANIMOTION_MAX_INPUT_TOKENS") or 60000),
            max_out=int(e("ANIMOTION_MAX_OUTPUT_TOKENS") or 8000),
            budget_usd=f("ANIMOTION_BUDGET_USD"),
            price_in=f("ANIMOTION_PRICE_IN_PER_MTOK"),
            price_out=f("ANIMOTION_PRICE_OUT_PER_MTOK"),
            max_request_usd=f("ANIMOTION_MAX_REQUEST_USD"),
            budget_journal=(e("ANIMOTION_BUDGET_JOURNAL") or "WAL").strip(),
            budget_db=_path(e("ANIMOTION_BUDGET_DB"), "./storage/budget.sqlite3"),
            render_timeout_s=int(e("RENDER_TIMEOUT_S") or 3 * 3600),
        )

    def validate(self) -> list[str]:
        errs = []
        if len(self.worker_token) < 24:
            errs.append("WORKER_TOKEN ausente o demasiado corto (>=24)")
        if not (self.engine_root / "pdf2video" / "cli.py").exists():
            errs.append(f"motor pdf2video no encontrado en {self.engine_root}")
        if self.provider not in ("anthropic", "replay"):
            errs.append("ANIMOTION_PROVIDER debe ser anthropic o replay")
        if self.provider == "replay" and not (self.replay_spec and self.replay_spec.is_file()):
            errs.append("ANIMOTION_REPLAY_SPEC no apunta a un archivo")
        if self.provider == "anthropic":
            k = (os.environ.get("ANTHROPIC_API_KEY") or "").strip()
            if not k or k.startswith("TU_CLAVE"):
                errs.append("ANTHROPIC_API_KEY no configurada")
            if not self.model:
                errs.append("ANIMOTION_MODEL no configurado")
            if None in (self.budget_usd, self.price_in, self.price_out, self.max_request_usd):
                errs.append("faltan ANIMOTION_BUDGET_USD / precios / ANIMOTION_MAX_REQUEST_USD")
        return errs
