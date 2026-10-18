import hashlib

from tests.conftest import make_pdf, upload_pdf


def test_upload_happy_path(alice, store, client):
    data = make_pdf(pages=2)
    fid = upload_pdf(alice, store, data)
    r = client.post(f"/v1/uploads/{fid}/complete", headers=alice.headers)
    assert r.status_code == 200
    b = r.json()
    assert b["status"] == "analyzed" and b["page_count"] == 2 and b["has_text_layer"] is True
    assert b["sha256"] == hashlib.sha256(data).hexdigest() and b["ocr_required"] is False
    # idempotente
    assert client.post(f"/v1/uploads/{fid}/complete", headers=alice.headers).json() == b


def test_init_returns_signed_put_without_secrets(alice, client):
    data = make_pdf()
    r = client.post("/v1/uploads/init", headers=alice.headers,
                    json={"filename": "../../etc/passwd.pdf", "size_bytes": len(data),
                          "sha256": hashlib.sha256(data).hexdigest()})
    b = r.json()
    assert b["method"] == "PUT" and "sig=put" in b["upload_url"]
    assert "passwd" not in b["upload_url"]                 # la clave S3 no usa el nombre del cliente
    assert set(b) == {"file_id", "upload_url", "method", "headers", "expires_at"}


def test_422_invalid_pdfs(alice, store, client):
    # extensión
    r = client.post("/v1/uploads/init", headers=alice.headers,
                    json={"filename": "a.exe", "size_bytes": 10, "sha256": "a" * 64})
    assert r.status_code == 422 and r.json()["code"] == "invalid_pdf"
    # demasiado grande para el plan (free = 10 MiB)
    r = client.post("/v1/uploads/init", headers=alice.headers,
                    json={"filename": "a.pdf", "size_bytes": 11 * 1024 * 1024, "sha256": "a" * 64})
    assert r.status_code == 422 and r.json()["details"]["reason"] == "too_large"
    # no es PDF
    fid = upload_pdf(alice, store, b"hello world not a pdf")
    r = client.post(f"/v1/uploads/{fid}/complete", headers=alice.headers)
    assert r.status_code == 422 and r.json()["details"]["reason"] == "not_a_pdf"
    assert client.post(f"/v1/uploads/{fid}/complete", headers=alice.headers).status_code == 422  # sigue rechazado
    # hash alterado
    data = make_pdf()
    r = client.post("/v1/uploads/init", headers=alice.headers,
                    json={"filename": "a.pdf", "size_bytes": len(data), "sha256": "b" * 64})
    fid2 = r.json()["file_id"]
    store.objects[f"users/{alice.id}/pdfs/{fid2}.pdf"] = data
    r = client.post(f"/v1/uploads/{fid2}/complete", headers=alice.headers)
    assert r.status_code == 422 and r.json()["details"]["reason"] == "sha256_mismatch"
    # demasiadas páginas (free = 5)
    fid3 = upload_pdf(alice, store, make_pdf(pages=6))
    r = client.post(f"/v1/uploads/{fid3}/complete", headers=alice.headers)
    assert r.status_code == 422 and r.json()["details"]["reason"] == "too_many_pages"


def test_complete_before_upload_is_409(alice, client):
    data = make_pdf()
    r = client.post("/v1/uploads/init", headers=alice.headers,
                    json={"filename": "a.pdf", "size_bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    r = client.post(f"/v1/uploads/{r.json()['file_id']}/complete", headers=alice.headers)
    assert r.status_code == 409 and r.json()["code"] == "upload_incomplete"


def test_other_users_upload_is_404(alice, bob, store, client):
    fid = upload_pdf(alice, store)
    assert client.post(f"/v1/uploads/{fid}/complete", headers=bob.headers).status_code == 404


def test_render_options_published_by_plan(alice, bob, client):
    o = client.get("/v1/render-options", headers=alice.headers).json()
    assert o["languages"] == ["es"] and o["resolutions"] == ["480p", "720p"] and o["voices"] == []
    assert {"kind": "hybrid_lesson", "prologue_allowed": False} in o["kinds"]
    bob.set_plan("pro")
    o2 = client.get("/v1/render-options", headers=bob.headers).json()
    assert o2["resolutions"] == ["480p", "720p", "1080p"]
    assert {"kind": "hybrid_lesson", "prologue_allowed": True} in o2["kinds"]


def test_estimate_validates_against_published_options(alice, pdf_for, client):
    pid = pdf_for(alice)

    def est(kind, **cfg):
        return client.post("/v1/jobs/estimate", headers=alice.headers,
                           json={"pdf_file_id": pid, "kind": kind, "config": {"target_seconds": 30, **cfg}})
    assert est("solution_video", resolution="1080p").status_code == 422        # free: máx 720p
    assert est("solution_video", language="en").status_code == 422             # solo 'es'
    assert est("solution_video", target_seconds=61).status_code == 422
    assert est("solution_video", include_prologue=True).status_code == 422     # prohibido en solution_video
    assert est("hybrid_lesson", include_prologue=True).status_code == 422      # free no incluye prólogo
    r = est("hybrid_lesson")
    assert r.status_code == 200 and r.json()["breakdown"]["credits_by_engine"].get("threejs") is None
    assert est("solution_video", bogus=1).status_code == 422                   # campos extra prohibidos


def test_free_plan_can_afford_one_useful_video(alice, pdf_for, estimate_for):
    """Garantía de negocio (BORRADOR): con los pesos draft, 20 s Manim + 20 s SVG = 30 créditos;
    un solution_video de 40 s a 720p cabe dentro del presupuesto Free (30 créditos)."""
    e = estimate_for(alice, pdf_for(alice), target_seconds=40, resolution="720p")
    assert e["estimated_credits"] <= 30


import pytest  # noqa: E402


@pytest.mark.xfail(strict=True, reason="HALLAZGO DE NEGOCIO (tarifas borrador): 40 s a 720p estima 26 créditos pero "
                   "la RESERVA MÁXIMA es 33 (>30 del Free), así que el Free no puede crear ese job. Decisión de "
                   "tarifas pendiente: headroom menor, menos segundos o más créditos. strict: pasará a fallo al arreglarse.")
def test_free_plan_can_reserve_max_for_40s_video(alice, pdf_for, estimate_for):
    e = estimate_for(alice, pdf_for(alice), target_seconds=40, resolution="720p")
    assert e["max_credits"] <= 30, (e["estimated_credits"], e["max_credits"])
