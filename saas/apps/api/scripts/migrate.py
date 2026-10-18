"""Aplica db/schema.sql (si la BD está vacía) y db/migrations/*.sql en orden, con registro en schema_migrations.

    python scripts/migrate.py                       # usa DATABASE_URL
    python scripts/migrate.py --seed-dev-plans      # además carga db/seed_plans_DRAFT.sql (planes BORRADOR, solo desarrollo)
    python scripts/migrate.py --grant-credits EMAIL N   # crédito de desarrollo (entry 'grant') a un usuario ya registrado
    python scripts/migrate.py --set-plan EMAIL CODE     # plan de DESARROLLO (suscripción de 30 días) para pruebas de resolución

Nunca borra datos. Es seguro re-ejecutarlo.
"""
from __future__ import annotations

import argparse
import os
import sys
import uuid
from pathlib import Path

import psycopg

DB = Path(__file__).resolve().parents[3] / "db"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed-dev-plans", action="store_true")
    ap.add_argument("--grant-credits", nargs=2, metavar=("EMAIL", "N"))
    ap.add_argument("--set-plan", nargs=2, metavar=("EMAIL", "CODE"))
    a = ap.parse_args()
    url = os.environ.get("DATABASE_URL")
    if not url:
        print("DATABASE_URL no está definida", file=sys.stderr)
        return 2
    with psycopg.connect(url, autocommit=True) as c:
        c.execute("CREATE TABLE IF NOT EXISTS schema_migrations(name text PRIMARY KEY, applied_at timestamptz NOT NULL DEFAULT now())")
        has_users = c.execute("SELECT to_regclass('public.users') IS NOT NULL AS x").fetchone()[0]
        if not has_users:
            c.execute((DB / "schema.sql").read_text(encoding="utf-8"))
            c.execute("INSERT INTO schema_migrations(name) VALUES ('001_schema.sql') ON CONFLICT DO NOTHING")
            print("aplicado: schema.sql")
        else:
            c.execute("INSERT INTO schema_migrations(name) VALUES ('001_schema.sql') ON CONFLICT DO NOTHING")
        done = {r[0] for r in c.execute("SELECT name FROM schema_migrations")}
        for m in sorted((DB / "migrations").glob("*.sql")):
            if m.name in done:
                print(f"ya aplicado: {m.name}")
                continue
            c.execute(m.read_text(encoding="utf-8"))
            c.execute("INSERT INTO schema_migrations(name) VALUES (%s)", (m.name,))
            print(f"aplicado: {m.name}")
        if a.seed_dev_plans:
            n = c.execute("SELECT count(*) FROM plans").fetchone()[0]
            if n == 0:
                c.execute((DB / "seed_plans_DRAFT.sql").read_text(encoding="utf-8"))
                print("planes BORRADOR cargados (solo desarrollo)")
            else:
                print(f"planes ya existentes ({n}): no se tocan")
        if a.grant_credits:
            email, n = a.grant_credits[0], int(a.grant_credits[1])
            row = c.execute("SELECT id FROM users WHERE email=%s", (email,)).fetchone()
            if not row:
                print(f"usuario {email} no existe todavía: inicia sesión una vez en la app y repite", file=sys.stderr)
                return 3
            c.execute("INSERT INTO credit_ledger(user_id, entry_type, delta, reason, idempotency_key) "
                      "VALUES (%s,'grant',%s,'dev grant',%s)", (row[0], n, f"devgrant:{uuid.uuid4()}"))
            print(f"+{n} créditos de desarrollo para {email}")
        if a.set_plan:
            email, code = a.set_plan
            row = c.execute("SELECT id FROM users WHERE email=%s", (email,)).fetchone()
            plan = c.execute("SELECT id FROM plans WHERE code=%s", (code,)).fetchone()
            if not row or not plan:
                print("usuario o plan inexistente", file=sys.stderr)
                return 3
            c.execute("""INSERT INTO subscriptions(user_id, plan_id, status, current_period_start, current_period_end)
                         VALUES (%s,%s,'active', now() - interval '1 day', now() + interval '30 days')""", (row[0], plan[0]))
            print(f"plan {code} (desarrollo) para {email}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
