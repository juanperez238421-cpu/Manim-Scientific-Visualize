"""Tests contra un PostgreSQL 16 REAL (cluster temporal, sin tocar ninguna BD existente)."""
from __future__ import annotations

import hashlib
import io
import os
import shutil
import subprocess
import tempfile
import time
import uuid
from pathlib import Path

import jwt
import psycopg
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from app.auth import JwtVerifier
from app.config import Settings
from app.main import create_app

ROOT = Path(__file__).resolve().parents[2].parent          # saas/
PG_BIN = next(Path("/usr/lib/postgresql").glob("*/bin"), None)
ISSUER = "https://clerk.test.example"


@pytest.fixture(scope="session")
def pg_url():
    if PG_BIN is None:
        pytest.skip("PostgreSQL no instalado")
    d = Path(tempfile.mkdtemp(prefix="pgtest_"))
    shutil.chown(d, "postgres", "postgres") if os.geteuid() == 0 else None
    run = (lambda cmd: subprocess.run(["su", "postgres", "-c", cmd], check=True, capture_output=True)
           if os.geteuid() == 0 else subprocess.run(cmd, shell=True, check=True, capture_output=True))
    run(f"{PG_BIN}/initdb -D {d}/data -A trust")
    port = 54000 + os.getpid() % 900
    run(f"{PG_BIN}/pg_ctl -D {d}/data -o '-p {port} -k {d} -c fsync=off -c max_connections=200' -l {d}/log -w start")
    url = f"host={d} port={port} user=postgres dbname=postgres"
    with psycopg.connect(url, autocommit=True) as c:
        c.execute((ROOT / "db" / "schema.sql").read_text())
    yield url
    run(f"{PG_BIN}/pg_ctl -D {d}/data -m immediate stop")
    shutil.rmtree(d, ignore_errors=True)


@pytest.fixture(scope="session")
def pool(pg_url):
    p = ConnectionPool(pg_url, min_size=2, max_size=40, kwargs={"row_factory": dict_row}, open=True)
    p.wait()
    yield p
    p.close()


@pytest.fixture(autouse=True)
def clean_db(pool):
    with pool.connection() as c:
        c.execute("""TRUNCATE outbox, idempotency_keys, credit_ledger, videos, job_scenes, job_stages, jobs,
                     job_estimates, pdf_files, subscriptions, payment_customers, users, plans CASCADE""")
        c.execute((ROOT / "db" / "seed_plans_DRAFT.sql").read_text())
    yield


# ---------------------------------------------------------------- JWT / app
@pytest.fixture(scope="session")
def rsa_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


@pytest.fixture(scope="session")
def other_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def make_token(key, sub, *, iss=ISSUER, exp_in=3600, email=None, extra=None):
    now = int(time.time())
    claims = {"sub": sub, "iss": iss, "iat": now, "exp": now + exp_in, "azp": "https://app.test"}
    if email:
        claims["email"] = email
    claims.update(extra or {})
    return jwt.encode(claims, key, algorithm="RS256")


class FakeStore:
    def __init__(self):
        self.objects: dict[str, bytes] = {}

    def presign_put(self, key, content_type, ttl):
        return f"https://store.test/{key}?sig=put&ttl={ttl}", {"Content-Type": content_type}

    def presign_get(self, key, ttl, filename=None):
        return f"https://store.test/{key}?sig=get&ttl={ttl}"

    def head(self, key):
        return len(self.objects[key]) if key in self.objects else None

    def get_bytes(self, key, max_bytes):
        return self.objects[key][: max_bytes + 1]

    def delete(self, key):
        self.objects.pop(key, None)


@pytest.fixture
def store():
    return FakeStore()


@pytest.fixture
def client(pool, store, rsa_key):
    verifier = JwtVerifier(lambda tok: rsa_key.public_key(), ISSUER, None, ("https://app.test",))
    app = create_app(Settings(), pool=pool, store=store, verifier=verifier)
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


class Actor:
    """Un usuario autenticado contra la API."""

    def __init__(self, client, key, sub, pool):
        self.client, self.sub, self.pool = client, sub, pool
        self.headers = {"Authorization": f"Bearer {make_token(key, sub, email=sub + '@t.co')}"}
        self.id = client.get("/v1/me", headers=self.headers).json()["id"]

    def h(self, **extra):
        return {**self.headers, **extra}

    def grant(self, n):
        with self.pool.connection() as c:
            c.execute("INSERT INTO credit_ledger(user_id, entry_type, delta, idempotency_key) VALUES (%s,'grant',%s,%s)",
                      (self.id, n, f"grant:{uuid.uuid4()}"))

    def set_plan(self, code):
        with self.pool.connection() as c:
            c.execute("""INSERT INTO subscriptions(user_id, plan_id, status, current_period_start, current_period_end)
                         SELECT %s, id, 'active', now() - interval '1 day', now() + interval '30 days'
                         FROM plans WHERE code=%s""", (self.id, code))

    def balance(self):
        return self.client.get("/v1/credits/balance", headers=self.headers).json()


@pytest.fixture
def make_actor(client, rsa_key, pool):
    return lambda sub: Actor(client, rsa_key, sub, pool)


@pytest.fixture
def alice(make_actor):
    return make_actor("user_alice")


@pytest.fixture
def bob(make_actor):
    return make_actor("user_bob")


# ---------------------------------------------------------------- PDFs
def make_pdf(pages=1, text="Resolver: x + 2 = 5") -> bytes:
    from pypdf import PdfWriter
    from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject
    w = PdfWriter()
    for _ in range(pages):
        page = w.add_blank_page(width=612, height=792)
        font = DictionaryObject({NameObject("/Type"): NameObject("/Font"), NameObject("/Subtype"): NameObject("/Type1"),
                                 NameObject("/BaseFont"): NameObject("/Helvetica")})
        page[NameObject("/Resources")] = DictionaryObject({NameObject("/Font"): DictionaryObject({NameObject("/F1"): font})})
        stream = DecodedStreamObject()
        stream.set_data(f"BT /F1 18 Tf 72 700 Td ({text}) Tj ET".encode())
        page[NameObject("/Contents")] = w._add_object(stream)
    buf = io.BytesIO()
    w.write(buf)
    return buf.getvalue()


def upload_pdf(actor, store, data: bytes | None = None, *, pages=1, filename="examen.pdf"):
    data = data if data is not None else make_pdf(pages)
    sha = hashlib.sha256(data).hexdigest()
    r = actor.client.post("/v1/uploads/init", headers=actor.headers,
                          json={"filename": filename, "size_bytes": len(data), "sha256": sha})
    assert r.status_code == 200, r.text
    fid = r.json()["file_id"]
    key = f"users/{actor.id}/pdfs/{fid}.pdf"
    store.objects[key] = data
    return fid


@pytest.fixture
def pdf_for(store):
    def _pdf_for(actor, **kw):
        fid = upload_pdf(actor, store, **kw)
        r = actor.client.post(f"/v1/uploads/{fid}/complete", headers=actor.headers)
        assert r.status_code == 200, r.text
        return fid
    return _pdf_for


@pytest.fixture
def estimate_for():
    def _estimate(actor, pdf_id, kind="solution_video", **cfg):
        config = {"target_seconds": 30, "resolution": "720p", **cfg}
        r = actor.client.post("/v1/jobs/estimate", headers=actor.headers,
                              json={"pdf_file_id": pdf_id, "kind": kind, "config": config})
        assert r.status_code == 200, r.text
        return r.json()
    return _estimate


def create_job(actor, est, *, key=None, max_auth=None):
    return actor.client.post("/v1/jobs", headers=actor.h(**{"Idempotency-Key": key or str(uuid.uuid4())}),
                             json={"estimate_id": est["estimate_id"], "estimate_hash": est["estimate_hash"],
                                   "max_authorized_credits": max_auth or est["max_credits"]})


@pytest.fixture
def make_job(pdf_for, estimate_for):
    """Crea un job encolado de punta a punta. Devuelve (job_json, estimate_json)."""
    def _make(actor, **cfg):
        est = estimate_for(actor, pdf_for(actor), **cfg)
        r = create_job(actor, est)
        assert r.status_code == 201, r.text
        return r.json(), est
    return _make
