"""Verificación de JWT de Clerk: firma (JWKS), emisor, audiencia opcional, exp/nbf, sub, azp."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import jwt
from fastapi import Depends, Request

from .errors import ApiError


@dataclass(frozen=True)
class Identity:
    provider: str
    subject: str
    email: str | None
    name: str | None


class JwtVerifier:
    def __init__(self, key_resolver: Callable[[str], object], issuer: str,
                 audience: str | None = None, authorized_parties: tuple[str, ...] = ()):
        self._resolve, self.issuer = key_resolver, issuer
        self.audience, self.parties = audience, authorized_parties

    @classmethod
    def clerk(cls, jwks_url: str, issuer: str, audience=None, authorized_parties=()):
        client = jwt.PyJWKClient(jwks_url, cache_keys=True)
        return cls(lambda tok: client.get_signing_key_from_jwt(tok).key, issuer, audience, authorized_parties)

    def verify(self, token: str) -> Identity:
        try:
            key = self._resolve(token)
            claims = jwt.decode(
                token, key, algorithms=["RS256"], issuer=self.issuer, audience=self.audience,
                options={"require": ["exp", "iat", "sub", "iss"], "verify_aud": self.audience is not None},
            )
        except Exception:  # firma, exp, iss, aud, formato, JWKS caído: todo es 401
            raise ApiError(401, "unauthorized", "Token inválido o vencido.")
        if self.parties and claims.get("azp") not in self.parties:
            raise ApiError(401, "unauthorized", "Origen no autorizado.")
        return Identity("clerk", claims["sub"], claims.get("email"), claims.get("name"))


def get_identity(request: Request) -> Identity:
    header = request.headers.get("authorization", "")
    scheme, _, token = header.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise ApiError(401, "unauthorized", "Falta el token Bearer.")
    return request.app.state.verifier.verify(token.strip())


@dataclass(frozen=True)
class Plan:
    code: str
    max_pdf_pages: int
    max_pdf_bytes: int
    max_video_seconds: int
    max_resolution: str
    allows_prologue: bool
    monthly_credits: int
    max_concurrent_jobs: int


@dataclass(frozen=True)
class CurrentUser:
    id: str
    email: str
    plan: Plan


def get_current_user(request: Request, ident: Identity = Depends(get_identity)) -> CurrentUser:
    """Identidad = (provider, sub). El email NO identifica; solo se guarda."""
    pool = request.app.state.pool
    with pool.connection() as conn:
        email = ident.email or f"{ident.subject}@clerk.invalid"
        row = conn.execute(
            """INSERT INTO users(auth_provider, provider_subject, email, display_name)
               VALUES (%s,%s,%s,%s)
               ON CONFLICT (auth_provider, provider_subject) DO UPDATE SET updated_at = now()
               RETURNING id, email, status""",
            (ident.provider, ident.subject, email, ident.name),
        ).fetchone()
        if row["status"] != "active":
            raise ApiError(403, "user_inactive", "Cuenta no activa.")
        plan = conn.execute(
            """SELECT p.* FROM plans p
               LEFT JOIN subscriptions s ON s.plan_id = p.id AND s.user_id = %s
                    AND s.status IN ('trialing','active','past_due') AND s.current_period_end > now()
               WHERE s.id IS NOT NULL OR p.code = 'free'
               ORDER BY (s.id IS NULL) LIMIT 1""",
            (row["id"],),
        ).fetchone()
    if plan is None:
        raise ApiError(500, "plan_missing", "Plan no configurado.")
    return CurrentUser(str(row["id"]), row["email"], Plan(
        plan["code"], plan["max_pdf_pages"], plan["max_pdf_bytes"], plan["max_video_seconds"],
        plan["max_resolution"], plan["allows_prologue"], plan["monthly_credits"], plan["max_concurrent_jobs"]))
