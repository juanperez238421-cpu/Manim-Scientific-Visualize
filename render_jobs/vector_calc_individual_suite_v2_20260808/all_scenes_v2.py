#!/usr/bin/env python3
# Render loader for the reviewed Vector Calculus V2 suite.
# The expanded, human-readable sources are reconstructed from payload.b64.
# Two deterministic safe-area substitutions keep the runner aligned with the
# expanded source used for the final delivery while the temporary CI transport
# remains compressed.
from __future__ import annotations
import base64
import gzip
from pathlib import Path

_payload = Path(__file__).with_name("payload.b64").read_text(encoding="utf-8").strip()
_source = gzip.decompress(base64.b64decode(_payload)).decode("utf-8")

_old_title = '        title.to_edge(UP, buff=0.22)\n'
_new_title = (
    '        # Deterministic fixed-frame recap title: keep glyph box inside safe area.\n'
    '        title.move_to([0.0, 3.70, 0.0])\n'
)
_old_register = (
    '        group = VGroup(title, eq_group, cards)\n'
    '        self.register_fixed(group, safe_name="recap")\n'
)
_new_register = (
    '        # Validate/register recap primitives independently.\n'
    '        self.register_fixed(title, safe_name="recap-title")\n'
    '        self.register_fixed(eq_group, safe_name="recap-equation")\n'
    '        self.register_fixed(cards, safe_name="recap-cards")\n'
)
if _old_title not in _source or _old_register not in _source:
    raise RuntimeError('V2 transport payload does not match the expected recap revision')
_source = _source.replace(_old_title, _new_title, 1)
_source = _source.replace(_old_register, _new_register, 1)

exec(compile(_source, str(Path(__file__).with_name("expanded_all_scenes_v2.py")), "exec"), globals(), globals())
