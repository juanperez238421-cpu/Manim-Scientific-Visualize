# AniMotionPDF API (etapa 1)

FastAPI + PostgreSQL. Sin Celery/pipeline todavía. Ver `../CONTRACT.md`, `QA_REPORT.md`, `openapi.json`.

```
pip install -e '.[dev]' pytest-timeout
pytest                                   # levanta un PostgreSQL temporal propio (nunca usa BD existentes)
python scripts/export_openapi.py         # regenera openapi.json (un test falla si está desactualizado)
```
Variables: `DATABASE_URL`, `CLERK_JWKS_URL`, `CLERK_ISSUER`, `CLERK_AUDIENCE?`, `CLERK_AUTHORIZED_PARTIES`,
`S3_ENDPOINT_URL` (MinIO/R2), `S3_BUCKET`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`, `CORS_ORIGINS`.
El navegador nunca recibe credenciales de S3/Redis/Postgres/Claude: solo URLs firmadas de corta duración.
