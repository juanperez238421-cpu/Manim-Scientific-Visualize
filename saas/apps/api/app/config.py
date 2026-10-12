"""Configuración por entorno. Ningún secreto se devuelve al navegador."""
from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    database_url: str = ""
    # Clerk
    clerk_jwks_url: str = ""
    clerk_issuer: str = ""
    clerk_audience: str | None = None          # Clerk suele usar 'azp'; 'aud' es opcional
    clerk_authorized_parties: tuple[str, ...] = ()
    # Objetos (MinIO en dev, Cloudflare R2 en prod: ambos S3-compatibles)
    s3_endpoint_url: str | None = None
    s3_bucket: str = "animotionpdf"
    s3_region: str = "auto"
    s3_access_key: str | None = None
    s3_secret_key: str | None = None
    signed_url_ttl_seconds: int = 900
    upload_url_ttl_seconds: int = 900
    estimate_ttl_seconds: int = 900
    pipeline_version: str = "sciviz-adapter-0.1"
    cors_origins: tuple[str, ...] = field(default_factory=tuple)

    @staticmethod
    def from_env() -> "Settings":
        e = os.environ.get
        return Settings(
            database_url=e("DATABASE_URL", ""),
            clerk_jwks_url=e("CLERK_JWKS_URL", ""),
            clerk_issuer=e("CLERK_ISSUER", ""),
            clerk_audience=e("CLERK_AUDIENCE") or None,
            clerk_authorized_parties=tuple(x for x in e("CLERK_AUTHORIZED_PARTIES", "").split(",") if x),
            s3_endpoint_url=e("S3_ENDPOINT_URL") or None,
            s3_bucket=e("S3_BUCKET", "animotionpdf"),
            s3_region=e("S3_REGION", "auto"),
            s3_access_key=e("S3_ACCESS_KEY"),
            s3_secret_key=e("S3_SECRET_KEY"),
            cors_origins=tuple(x for x in e("CORS_ORIGINS", "").split(",") if x),
        )
