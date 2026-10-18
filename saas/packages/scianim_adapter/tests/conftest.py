import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def _engine_root():
    cands = [os.environ.get("P2V_ENGINE_ROOT"), "/home/claude/p2v-main/pdf2video"]
    for c in cands:
        if c and (Path(c) / "pdf2video" / "cli.py").exists():
            return Path(c)
    return None


@pytest.fixture(scope="session")
def engine_root():
    r = _engine_root()
    if r is None:
        pytest.skip("pdf2video engine not found (set P2V_ENGINE_ROOT)")
    return r


@pytest.fixture(scope="session")
def physics(engine_root):
    d = engine_root / "examples" / "physics"
    return d / "physics_worksheet.pdf", json.loads((d / "spec.json").read_text())


@pytest.fixture()
def cfg(engine_root):
    from scianim_adapter import JobConfig
    return JobConfig(engine_root=engine_root, python=sys.executable, render=False)
