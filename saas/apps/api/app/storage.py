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
