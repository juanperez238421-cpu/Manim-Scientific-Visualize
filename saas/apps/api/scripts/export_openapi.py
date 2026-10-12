"""Exporta el OpenAPI REAL generado por FastAPI (sin BD ni credenciales) a openapi.json."""
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.main import create_app  # noqa: E402

app = create_app(pool=MagicMock(), store=MagicMock(), verifier=MagicMock())
out = Path(__file__).resolve().parents[1] / "openapi.json"
out.write_text(json.dumps(app.openapi(), indent=2, ensure_ascii=False) + "\n")
print(f"wrote {out}")
