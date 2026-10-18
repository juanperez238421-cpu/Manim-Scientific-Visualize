"""Almacenamiento S3-compatible (MinIO en dev, Cloudflare R2 en prod). El navegador solo ve URLs firmadas."""
from __future__ import annotations

from typing import Protocol


class ObjectStore(Protocol):
    def presign_put(self, key: str, content_type: str, ttl: int) -> tuple[str, dict[str, str]]: ...
    def presign_get(self, key: str, ttl: int, filename: str | None = None) -> str: ...
    def head(self, key: str) -> int | None: ...            # tamaño o None si no existe
    def get_bytes(self, key: str, max_bytes: int) -> bytes: ...
    def delete(self, key: str) -> None: ...


class S3Store:
    def __init__(self, bucket: str, endpoint_url: str | None, region: str,
                 access_key: str | None, secret_key: str | None):
        import boto3
        from botocore.config import Config

        self.bucket = bucket
        self.client = boto3.client(
            "s3", endpoint_url=endpoint_url, region_name=region,
            aws_access_key_id=access_key, aws_secret_access_key=secret_key,
            config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
        )

    def presign_put(self, key, content_type, ttl):
        url = self.client.generate_presigned_url(
            "put_object", Params={"Bucket": self.bucket, "Key": key, "ContentType": content_type}, ExpiresIn=ttl)
        return url, {"Content-Type": content_type}

    def presign_get(self, key, ttl, filename=None):
        params = {"Bucket": self.bucket, "Key": key}
        if filename:
            params["ResponseContentDisposition"] = f'attachment; filename="{filename}"'
        return self.client.generate_presigned_url("get_object", Params=params, ExpiresIn=ttl)

    def head(self, key):
        from botocore.exceptions import ClientError
        try:
            return int(self.client.head_object(Bucket=self.bucket, Key=key)["ContentLength"])
        except ClientError as e:
            if e.response["Error"]["Code"] in ("404", "NoSuchKey", "NotFound"):
                return None
            raise

    def get_bytes(self, key, max_bytes):
        obj = self.client.get_object(Bucket=self.bucket, Key=key)
        data = obj["Body"].read(max_bytes + 1)
        return data

    def delete(self, key):
        self.client.delete_object(Bucket=self.bucket, Key=key)


# ---------------------------------------------------------------- almacenamiento local (desarrollo en localhost)
import hashlib as _hashlib
import hmac as _hmac
import re as _re
import time as _time
from pathlib import Path as _Path
from urllib.parse import quote as _quote

_KEY_OK = _re.compile(r"^[A-Za-z0-9][A-Za-z0-9/_.\-]{0,300}$")


class BadKey(ValueError):
    pass


class LocalFsStore:
    """Equivalente local de S3/R2: archivos bajo `root` y URLs firmadas con HMAC-SHA256 servidas por la propia API
    (`/blob/...`). Solo para desarrollo: en nube se usa S3Store (R2). Misma interfaz => la API pública no cambia."""

    def __init__(self, root, secret: str, public_base_url: str, max_object_bytes: int = 500 * 1024 * 1024):
        if len(secret) < 16:
            raise ValueError("storage secret demasiado corto (>=16 caracteres)")
        self.root = _Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.secret = secret.encode()
        self.base = public_base_url.rstrip("/")
        self.max_object_bytes = max_object_bytes

    # -- rutas seguras
    def path(self, key: str) -> _Path:
        if not _KEY_OK.match(key) or ".." in key.split("/") or "//" in key:
            raise BadKey(key)
        p = (self.root / key).resolve()
        if self.root not in p.parents:
            raise BadKey(key)
        return p

    # -- firmas
    def sign(self, method: str, key: str, exp: int, extra: str = "") -> str:
        msg = f"{method}\n{key}\n{exp}\n{extra}".encode()
        return _hmac.new(self.secret, msg, _hashlib.sha256).hexdigest()

    def verify(self, method: str, key: str, exp: int, sig: str, extra: str = "") -> bool:
        return exp >= int(_time.time()) and _hmac.compare_digest(self.sign(method, key, exp, extra), sig or "")

    def _url(self, method, key, ttl, filename=None):
        self.path(key)
        exp = int(_time.time()) + int(ttl)
        extra = filename or ""
        q = f"exp={exp}&sig={self.sign(method, key, exp, extra)}"
        if filename:
            q += f"&fn={_quote(filename)}"
        return f"{self.base}/blob/{_quote(key)}?{q}"

    def presign_put(self, key, content_type, ttl):
        return self._url("PUT", key, ttl), {"Content-Type": content_type}

    def presign_get(self, key, ttl, filename=None):
        return self._url("GET", key, ttl, filename)

    def head(self, key):
        p = self.path(key)
        return p.stat().st_size if p.is_file() else None

    def get_bytes(self, key, max_bytes):
        with self.path(key).open("rb") as f:
            return f.read(max_bytes + 1)

    def delete(self, key):
        try:
            self.path(key).unlink()
        except FileNotFoundError:
            pass
