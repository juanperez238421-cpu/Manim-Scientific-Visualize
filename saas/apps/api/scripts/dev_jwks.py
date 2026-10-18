"""IdP de DESARROLLO para pruebas automatizadas (NO es Clerk). Sirve /jwks.json y emite JWT RS256 en /token.

Solo escucha en 127.0.0.1. Permite ejercitar el MISMO camino de verificación (JWKS + firma RS256 + issuer + exp) que
usa la API con Clerk, sin cuenta externa. Para el flujo real con Clerk Development se usa CLERK_JWKS_URL de Clerk.
"""
from __future__ import annotations

import base64
import json
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

import jwt
from cryptography.hazmat.primitives.asymmetric import rsa

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 9100
ISSUER = f"http://127.0.0.1:{PORT}"
KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
KID = "dev-1"


def _b64(n: int) -> str:
    return base64.urlsafe_b64encode(n.to_bytes((n.bit_length() + 7) // 8, "big")).rstrip(b"=").decode()


def jwks() -> dict:
    pub = KEY.public_key().public_numbers()
    return {"keys": [{"kty": "RSA", "use": "sig", "alg": "RS256", "kid": KID, "n": _b64(pub.n), "e": _b64(pub.e)}]}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/jwks.json":
            body = json.dumps(jwks()).encode()
        elif u.path == "/token":
            q = parse_qs(u.query)
            sub = (q.get("sub") or ["user_dev"])[0]
            now = int(time.time())
            tok = jwt.encode({"sub": sub, "iss": ISSUER, "iat": now, "exp": now + 3600, "email": (q.get("email") or [f"{sub}@dev.test"])[0]},
                             KEY, algorithm="RS256", headers={"kid": KID})
            body = tok.encode()
        else:
            self.send_response(404); self.end_headers(); return
        self.send_response(200); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)


if __name__ == "__main__":
    print(f"dev-idp en {ISSUER}", flush=True)
    HTTPServer(("127.0.0.1", PORT), H).serve_forever()
