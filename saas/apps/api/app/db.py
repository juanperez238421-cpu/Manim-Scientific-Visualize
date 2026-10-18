from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool


def make_pool(url: str, max_size: int = 20) -> ConnectionPool:
    pool = ConnectionPool(url, min_size=1, max_size=max_size, kwargs={"row_factory": dict_row}, open=True)
    pool.wait()
    return pool


@contextmanager
def tx(pool: ConnectionPool) -> Iterator[psycopg.Connection]:
    """Una transacción: commit al salir, rollback si hay excepción."""
    with pool.connection() as conn:
        yield conn
