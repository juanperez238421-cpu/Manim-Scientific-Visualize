"""Recorrido de punta a punta contra servicios REALES en ejecución (API + PostgreSQL + worker + motor).

PDF -> /v1/uploads (init/PUT firmado/complete) -> /v1/jobs/estimate -> /v1/jobs (reserva) -> espera -> /v1/jobs/{id}/assets
-> descarga con Range -> ffprobe + decodificación completa. Imprime un informe JSON; el código de salida es 0 solo si todo pasó.

  python scripts/e2e_local.py --api http://127.0.0.1:8000 --idp http://127.0.0.1:9100 --pdf x.pdf --resolution 480p
  (con Clerk real: --token <JWT de sesión> en lugar de --idp)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path

import httpx


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--api", default="http://127.0.0.1:8000")
    ap.add_argument("--idp", help="URL del IdP de desarrollo (scripts de pruebas)")
    ap.add_argument("--token", help="JWT ya emitido (p. ej. Clerk Development)")
    ap.add_argument("--sub", default="user_e2e")
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--resolution", default="480p", choices=["480p", "720p", "1080p"])
    ap.add_argument("--kind", default="solution_video")
    ap.add_argument("--seconds", type=int, default=60)
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--out", default="e2e_report.json")
    ap.add_argument("--download", default="e2e_video.mp4")
    ap.add_argument("--expect", default="succeeded", choices=["succeeded", "failed", "cancelled"])
    ap.add_argument("--cancel-after", type=float, default=None, help="segundos tras crear el job para pedir cancelación")
    a = ap.parse_args()

    rep: dict = {"steps": [], "pass": False}

    def step(name, ok, **kw):
        rep["steps"].append({"step": name, "pass": bool(ok), **kw})
        print(("PASS " if ok else "FAIL ") + name, {k: v for k, v in kw.items() if k != "detail"}, flush=True)
        return ok

    c = httpx.Client(timeout=60)
    tok = a.token or c.get(f"{a.idp}/token", params={"sub": a.sub}).text
    H = {"Authorization": f"Bearer {tok}"}
    me = c.get(f"{a.api}/v1/me", headers=H)
    if not step("auth /v1/me", me.status_code == 200, status=me.status_code):
        return _end(rep, a)
    rep["plan"] = me.json()["plan"]
    bal0 = c.get(f"{a.api}/v1/credits/balance", headers=H).json()
    rep["balance_before"] = bal0

    data = Path(a.pdf).read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    ini = c.post(f"{a.api}/v1/uploads/init", headers=H, json={"filename": Path(a.pdf).name, "size_bytes": len(data), "sha256": sha})
    if not step("uploads/init", ini.status_code == 200, status=ini.status_code):
        return _end(rep, a)
    put = c.put(ini.json()["upload_url"], content=data, headers=ini.json()["headers"])
    step("PUT firmado del PDF", put.status_code == 200, status=put.status_code)
    comp = c.post(f"{a.api}/v1/uploads/{ini.json()['file_id']}/complete", headers=H)
    if not step("uploads/complete (magic, sha256, páginas)", comp.status_code == 200, status=comp.status_code, body=comp.json() if comp.status_code != 200 else {"pages": comp.json()["page_count"]}):
        return _end(rep, a)

    cfg = {"language": "es", "detail_level": "standard", "target_seconds": a.seconds, "resolution": a.resolution, "include_prologue": False}
    est = c.post(f"{a.api}/v1/jobs/estimate", headers=H, json={"pdf_file_id": comp.json()["file_id"], "kind": a.kind, "config": cfg})
    if not step("jobs/estimate", est.status_code == 200, status=est.status_code, body=None if est.status_code == 200 else est.json()):
        return _end(rep, a)
    e = est.json()
    rep["estimate"] = {k: e[k] for k in ("estimated_credits", "max_credits", "pricing_version", "sufficient_credits")}
    cj = c.post(f"{a.api}/v1/jobs", headers={**H, "Idempotency-Key": str(uuid.uuid4())},
                json={"estimate_id": e["estimate_id"], "estimate_hash": e["estimate_hash"], "max_authorized_credits": e["max_credits"]})
    if not step("jobs (reserva de créditos)", cj.status_code == 201, status=cj.status_code, body=None if cj.status_code == 201 else cj.json()):
        return _end(rep, a)
    job = cj.json()
    jid = job["id"]
    rep["job_id"], rep["reserved_credits"] = jid, job["reserved_credits"]

    t0, seen, cancelled = time.time(), [], False
    while time.time() - t0 < a.timeout:
        j = c.get(f"{a.api}/v1/jobs/{jid}", headers=H).json()
        mark = (j["status"], j["current_stage"], j["progress_pct"])
        if not seen or seen[-1] != mark:
            seen.append(mark)
            print(f"   {time.time() - t0:6.1f}s  {mark}", flush=True)
        if a.cancel_after is not None and not cancelled and time.time() - t0 >= a.cancel_after and j["status"] in ("queued", "running"):
            r = c.post(f"{a.api}/v1/jobs/{jid}/cancel", headers={**H, "Idempotency-Key": str(uuid.uuid4())})
            step("jobs/cancel", r.status_code == 200, status=r.status_code)
            cancelled = True
        if j["status"] in ("succeeded", "failed", "cancelled"):
            break
        time.sleep(2)
    rep["wall_seconds"] = round(time.time() - t0, 1)
    rep["progress_trace"] = seen
    rep["final_job"] = {k: j.get(k) for k in ("status", "final_credits", "reserved_credits", "error_code", "error_message", "progress_pct")}
    rep["stages"] = {s["stage"]: s["status"] for s in j["stages"]}
    bal1 = c.get(f"{a.api}/v1/credits/balance", headers=H).json()
    rep["balance_after"] = bal1
    if not step(f"estado final == {a.expect}", j["status"] == a.expect, status=j["status"]):
        return _end(rep, a)
    if a.expect != "succeeded":
        step("créditos devueltos (sin retención)", bal1["held"] == 0 and bal1["available"] == bal0["available"], balance=bal1)
        rep["pass"] = all(s["pass"] for s in rep["steps"])
        return _end(rep, a)
    step("liquidación: retenido=0 y cobro<=reserva", bal1["held"] == 0 and 0 < j["final_credits"] <= j["reserved_credits"], balance=bal1, final=j["final_credits"])

    asr = c.get(f"{a.api}/v1/jobs/{jid}/assets", headers=H)
    if not step("assets (URL firmada)", asr.status_code == 200, status=asr.status_code):
        return _end(rep, a)
    url = asr.json()["video_url"]
    rg = c.get(url, headers={"Range": "bytes=0-1023"})
    step("Range 206 (reproducción/seek)", rg.status_code == 206 and "content-range" in rg.headers, status=rg.status_code)
    with c.stream("GET", url) as r:
        with open(a.download, "wb") as f:
            for chunk in r.iter_bytes(1 << 20):
                f.write(chunk)
        step("descarga completa 200", r.status_code == 200 and r.headers.get("content-type") == "video/mp4", status=r.status_code,
             disposition=r.headers.get("content-disposition"))
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", a.download],
                                   capture_output=True, text=True).stdout)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    dec = subprocess.run(["ffmpeg", "-v", "error", "-i", a.download, "-f", "null", "-"], capture_output=True, text=True).stderr.strip()
    want_h = int(a.resolution[:-1])
    info = {"codec": v["codec_name"], "size": f"{v['width']}x{v['height']}", "fps": v["r_frame_rate"], "pix_fmt": v["pix_fmt"],
            "duration_s": round(float(pr["format"]["duration"]), 2), "MB": round(Path(a.download).stat().st_size / 1e6, 2),
            "sha256": hashlib.sha256(Path(a.download).read_bytes()).hexdigest()}
    rep["video"] = info
    step("ffprobe: h264/yuv420p y resolución del perfil", v["codec_name"] == "h264" and v["pix_fmt"] == "yuv420p" and v["height"] == want_h, **info)
    step("decodificación completa sin errores", dec == "", errors=dec[:200])
    api_video = j.get("video") or {}
    step("API y archivo coinciden (alto/fps/duración)", api_video.get("height") == v["height"] and abs(api_video.get("duration_seconds", 0) - float(pr["format"]["duration"])) < 0.5)
    rep["pass"] = all(s["pass"] for s in rep["steps"])
    return _end(rep, a)


def _end(rep, a) -> int:
    rep["pass"] = rep.get("pass") or (bool(rep["steps"]) and all(s["pass"] for s in rep["steps"]))
    Path(a.out).write_text(json.dumps(rep, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    print("\nRESULTADO E2E:", "PASS" if rep["pass"] else "FAIL", "->", a.out)
    return 0 if rep["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
