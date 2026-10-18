from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import errors
from .auth import JwtVerifier
from .config import Settings
from .db import make_pool
from .routers import credits, jobs, meta, uploads
from .storage import ObjectStore, S3Store


def create_app(settings: Settings | None = None, *, pool=None, store: ObjectStore | None = None,
               verifier: JwtVerifier | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    app = FastAPI(title="AniMotionPDF API", version="0.1.0",
                  description="Backend de AniMotionPDF. Contrato: saas/CONTRACT.md. Créditos: reserva del "
                              "máximo autorizado y liquidación solo por liberación.")
    app.state.settings = settings
    app.state.pool = pool or make_pool(settings.database_url)
    app.state.store = store or S3Store(settings.s3_bucket, settings.s3_endpoint_url, settings.s3_region,
                                       settings.s3_access_key, settings.s3_secret_key)
    app.state.verifier = verifier or JwtVerifier.clerk(
        settings.clerk_jwks_url, settings.clerk_issuer, settings.clerk_audience, settings.clerk_authorized_parties)
    if settings.cors_origins:        # CORS estricto: solo orígenes explícitos
        app.add_middleware(CORSMiddleware, allow_origins=list(settings.cors_origins), allow_credentials=False,
                           allow_methods=["GET", "POST"], allow_headers=["Authorization", "Content-Type",
                                                                         "Idempotency-Key", "X-Request-ID"])
    errors.install(app)
    for r in (meta.router, uploads.router, jobs.router, credits.router):
        app.include_router(r)

    @app.get("/healthz", include_in_schema=False)
    def healthz():
        return {"ok": True}

    return app
