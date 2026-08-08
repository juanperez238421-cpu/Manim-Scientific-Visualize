#!/usr/bin/env python3
# Render loader for the reviewed Vector Calculus V2 suite.
# The expanded, human-readable sources are reconstructed from payload.b64.
# Deterministic substitutions keep this temporary compressed CI transport
# synchronized with the expanded source delivered to the user.
from __future__ import annotations
import base64
import gzip
from pathlib import Path

_payload = Path(__file__).with_name("payload.b64").read_text(encoding="utf-8").strip()
_source = gzip.decompress(base64.b64decode(_payload)).decode("utf-8")

# 1) Fixed recap layout: explicit safe-area position and primitive validation.
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

# 2) Scene-specific recap zoom.  The classification workshop's downward
# paraboloid needs a wider final camera than the compact quadrics.
_old_recap_sig = '        *,\n        theta=-43,\n    ) -> None:\n'
_new_recap_sig = '        *,\n        theta=-43,\n        zoom=1.04,\n    ) -> None:\n'
_old_recap_camera = '        self.camera_focus(theta=theta, zoom=1.04, pause=0.55)\n'
_new_recap_camera = '        self.camera_focus(theta=theta, zoom=zoom, pause=0.55)\n'
_old_workshop_reveal = '        self.reveal_surface(surf, VGroup(vertex, rings), theta=-66, zoom=1.00)\n'
_new_workshop_reveal = '        self.reveal_surface(surf, VGroup(vertex, rings), theta=-66, zoom=0.92)\n'
_old_workshop_recap = '        ], theta=-45)\n'
_new_workshop_recap = '        ], theta=-45, zoom=0.92)\n'

_expected = [
    _old_title, _old_register, _old_recap_sig, _old_recap_camera,
    _old_workshop_reveal, _old_workshop_recap,
]
_missing = [token for token in _expected if token not in _source]
if _missing:
    raise RuntimeError(f'V2 transport payload does not match expected revision; missing {len(_missing)} patch tokens')

_source = _source.replace(_old_title, _new_title, 1)
_source = _source.replace(_old_register, _new_register, 1)
_source = _source.replace(_old_recap_sig, _new_recap_sig, 1)
_source = _source.replace(_old_recap_camera, _new_recap_camera, 1)
_source = _source.replace(_old_workshop_reveal, _new_workshop_reveal, 1)
_source = _source.replace(_old_workshop_recap, _new_workshop_recap, 1)

exec(compile(_source, str(Path(__file__).with_name("expanded_all_scenes_v2.py")), "exec"), globals(), globals())
