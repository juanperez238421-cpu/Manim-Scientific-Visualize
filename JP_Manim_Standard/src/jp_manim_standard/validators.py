"""Data and asset validation helpers."""
from __future__ import annotations
from collections.abc import Callable, Sequence
from pathlib import Path

def assert_close(actual: float, expected: float, *, tol: float = 1e-10, label: str = "value") -> None:
    if abs(actual - expected) > tol:
        raise AssertionError(f"{label}: expected {expected}, got {actual}")

def validate_relative_asset(path: str | Path) -> Path:
    path = Path(path)
    if path.is_absolute():
        raise ValueError(f"Absolute asset path is not portable: {path}")
    if not path.exists():
        raise FileNotFoundError(path)
    return path

def validate_all(checks: Sequence[tuple[str, Callable[[], bool]]]) -> None:
    failed = [name for name, check in checks if not check()]
    if failed:
        raise AssertionError("Lesson validation failed: " + ", ".join(failed))
