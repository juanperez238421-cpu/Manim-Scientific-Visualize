import time
import uuid

from tests.conftest import ISSUER, make_token


def test_401_missing_token(client):
    r = client.get("/v1/me")
    assert r.status_code == 401
    b = r.json()
    assert b["code"] == "unauthorized" and b["request_id"] and r.headers["X-Request-ID"] == b["request_id"]


def test_401_bad_scheme_and_garbage(client):
    assert client.get("/v1/me", headers={"Authorization": "Basic abc"}).status_code == 401
    assert client.get("/v1/me", headers={"Authorization": "Bearer not.a.jwt"}).status_code == 401


def test_401_wrong_signature(client, other_key):
    t = make_token(other_key, "u1")
    # el verificador de test resuelve SIEMPRE la clave pública buena: firma ajena => 401
    assert client.get("/v1/me", headers={"Authorization": f"Bearer {t}"}).status_code == 401


def test_401_expired_wrong_issuer_wrong_azp(client, rsa_key):
    for tok in (make_token(rsa_key, "u1", exp_in=-10),
                make_token(rsa_key, "u1", iss="https://evil.example"),
                make_token(rsa_key, "u1", extra={"azp": "https://evil.example"})):
        assert client.get("/v1/me", headers={"Authorization": f"Bearer {tok}"}).status_code == 401


def test_identity_is_sub_not_email(client, rsa_key):
    a = client.get("/v1/me", headers={"Authorization": "Bearer " + make_token(rsa_key, "user_x", email="same@t.co")})
    b = client.get("/v1/me", headers={"Authorization": "Bearer " + make_token(rsa_key, "user_y", email="same@t.co")})
    # mismo email, distinto sub: son DOS usuarios; el email nunca identifica ni provoca error
    assert a.status_code == b.status_code == 200 and a.json()["id"] != b.json()["id"]


def test_me_returns_plan_and_creates_user_once(client, rsa_key):
    h = {"Authorization": "Bearer " + make_token(rsa_key, "user_z", email="z@t.co")}
    r1, r2 = client.get("/v1/me", headers=h).json(), client.get("/v1/me", headers=h).json()
    assert r1["id"] == r2["id"] and r1["plan"] == "free"


def test_error_shape_404_and_422(alice, client):
    r = client.get(f"/v1/jobs/{uuid.uuid4()}", headers=alice.headers)
    assert r.status_code == 404 and set(r.json()) >= {"code", "message", "request_id"}
    r = client.get("/v1/jobs/not-a-uuid", headers=alice.headers)
    assert r.status_code == 404
    r = client.post("/v1/uploads/init", headers=alice.headers, json={"filename": "a.pdf"})
    assert r.status_code == 422 and r.json()["code"] == "validation_error" and r.json()["request_id"]
    r = client.get("/v1/jobs?limit=0", headers=alice.headers)
    assert r.status_code == 422


def test_request_id_is_propagated(client):
    r = client.get("/v1/me", headers={"X-Request-ID": "req-123"})
    assert r.json()["request_id"] == "req-123"
