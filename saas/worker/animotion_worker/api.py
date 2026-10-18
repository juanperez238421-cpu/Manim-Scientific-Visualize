"""Cliente HTTP del canal interno worker -> API. Solo conexiones SALIENTES; el token nunca se imprime."""
from __future__ import annotations

import time

import httpx


class LeaseLost(RuntimeError):
    pass


class ApiError(RuntimeError):
    def __init__(self, status: int, code: str, message: str):
        super().__init__(f"{status} {code}: {message}")
        self.status, self.code = status, code


class WorkerApi:
    def __init__(self, base_url: str, token: str, worker_id: str, *, client: httpx.Client | None = None):
        self.base, self.wid = base_url.rstrip("/") + "/internal/worker/v1", worker_id
        self._h = {"Authorization": f"Bearer {token}"}
        self.http = client or httpx.Client(timeout=httpx.Timeout(30.0, read=120.0))

    def _post(self, path: str, body: dict, retries: int = 3) -> dict:
        last = None
        for i in range(retries):
            try:
                r = self.http.post(self.base + path, headers=self._h, json=body)
            except httpx.TransportError as e:      # la API puede reiniciarse: reintento con backoff corto
                last = e
                time.sleep(0.5 * (2 ** i))
                continue
            if r.status_code >= 500 and i < retries - 1:
                time.sleep(0.5 * (2 ** i))
                continue
            if r.status_code >= 400:
                try:
                    j = r.json()
                except ValueError:
                    j = {}
                code = j.get("code", "http_error")
                if code == "lease_lost":
                    raise LeaseLost(j.get("message", "lease_lost"))
                raise ApiError(r.status_code, code, j.get("message", r.text[:200]))
            return r.json()
        raise ApiError(0, "unreachable", f"API no disponible: {type(last).__name__}")

    def claim(self) -> dict | None:
        return self._post("/claim", {"worker_id": self.wid})["job"]

    def heartbeat(self, job_id: str) -> str:
        return self._post(f"/jobs/{job_id}/heartbeat", {"worker_id": self.wid})["status"]

    def stage(self, job_id: str, stage: str, status: str, progress: int) -> str:
        return self._post(f"/jobs/{job_id}/stage", {"worker_id": self.wid, "stage": stage, "status": status,
                                                    "progress_pct": progress})["status"]

    def complete(self, job_id: str, video: dict, delivery: dict, qa: dict) -> dict:
        return self._post(f"/jobs/{job_id}/complete", {"worker_id": self.wid, "video": video, "delivery": delivery, "qa": qa})

    def fail(self, job_id: str, code: str, message: str, delivery: dict) -> dict:
        return self._post(f"/jobs/{job_id}/fail", {"worker_id": self.wid, "code": code, "message": message,
                                                   "platform_fault": True, "delivery": delivery})

    def confirm_cancel(self, job_id: str) -> dict:
        return self._post(f"/jobs/{job_id}/confirm-cancel", {"worker_id": self.wid, "consumed_credits": 0})

    # ---- bytes (URLs firmadas: no llevan token de worker)
    def download(self, url: str, dest, expected_sha256: str, max_bytes: int) -> None:
        import hashlib
        h, n = hashlib.sha256(), 0
        with self.http.stream("GET", url) as r:
            if r.status_code != 200:
                raise ApiError(r.status_code, "download_failed", "No se pudo descargar el PDF.")
            with open(dest, "wb") as f:
                for chunk in r.iter_bytes(1 << 20):
                    n += len(chunk)
                    if n > max_bytes:
                        raise ApiError(413, "too_large", "PDF demasiado grande.")
                    h.update(chunk)
                    f.write(chunk)
        if h.hexdigest() != expected_sha256:
            raise ApiError(422, "sha256_mismatch", "El PDF descargado no coincide con su hash registrado.")

    def upload(self, url: str, path) -> None:
        with open(path, "rb") as f:
            r = self.http.put(url, content=f, headers={"Content-Type": "video/mp4"}, timeout=httpx.Timeout(30.0, write=600.0))
        if r.status_code != 200:
            raise ApiError(r.status_code, "upload_failed", "No se pudo subir el video.")
