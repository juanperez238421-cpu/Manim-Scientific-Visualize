from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import errors
from .auth import JwtVerifier
from .config import Settings
from .db import make_pool
from .routers import blob, credits, jobs, meta, uploads, worker
from .storage import LocalFsStore, ObjectStore, S3Store


def create_app(settings: Settings | None = None, *, pool=None, store: ObjectStore | None = None,
               verifier: JwtVerifier | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    app = FastAPI(title="AniMotionPDF API", version="0.1.0",
                  description="Backend de AniMotionPDF. Contrato: saas/CONTRACT.md. Créditos: reserva del "
                              "máximo autorizado y liquidación solo por liberación.")
    app.state.settings = settings
    app.state.pool = pool or make_pool(settings.database_url)
    if store is None:
        if settings.local_storage_dir and not settings.s3_access_key:
            store = LocalFsStore(settings.local_storage_dir, settings.storage_secret, settings.public_base_url)
        else:
            store = S3Store(settings.s3_bucket, settings.s3_endpoint_url, settings.s3_region,
                            settings.s3_access_key, settings.s3_secret_key)
    app.state.store = store
    app.state.verifier = verifier or JwtVerifier.clerk(
        settings.clerk_jwks_url, settings.clerk_issuer, settings.clerk_audience, settings.clerk_authorized_parties)
    if settings.cors_origins:        # CORS estricto: solo orígenes explícitos
        app.add_middleware(CORSMiddleware, allow_origins=list(settings.cors_origins), allow_credentials=False,
                           allow_methods=["GET", "HEAD", "POST", "PUT"],
                           allow_headers=["Authorization", "Content-Type", "Idempotency-Key", "X-Request-ID", "Range"],
                           expose_headers=["Content-Range", "Accept-Ranges", "Content-Length", "X-Request-ID"])
    errors.install(app)
    for r in (meta.router, uploads.router, jobs.router, credits.router, blob.router, worker.router):
        app.include_router(r)

    @app.get("/healthz", include_in_schema=False)
    def healthz():
        return {"ok": True}

    return app
