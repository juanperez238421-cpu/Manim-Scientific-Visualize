#!/usr/bin/env python3
"""Generate Senior-QA V3 from the exact persisted V2 lesson source."""
from pathlib import Path
import sys

if len(sys.argv) != 3:
    raise SystemExit("usage: apply_senior_qa_v3.py INPUT_V2.py OUTPUT_V3.py")

src = Path(sys.argv[1])
out = Path(sys.argv[2])
s = src.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global s
    count = s.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    s = s.replace(old, new, 1)


replace_once(
    "Senior QA V2: improved graph-domain accuracy, stronger visual focus, larger comparison annotations, and clearer conceptual transitions.\n",
    "Senior QA V3: preserves V2 improvements and fixes scale-number visibility plus read-example annotation collisions.\n",
    "version note",
)

replace_once(
    '''        axis.move_to([0, y, 0])\n        return axis\n''',
    '''        # Senior-QA V3: NumberLine may construct numeric labels with their own\n        # default style. Recolor the complete submobject tree after construction so\n        # ticks AND numbers remain visible on the white classroom background.\n        axis.set_color(BLACK_LINE)\n        axis.move_to([0, y, 0])\n        return axis\n''',
    "axis color visibility",
)

replace_once(
    '''        uf_x = axis.n2p(summary.uf)[0]\n        uf_guide = DashedLine([uf_x, -1.35, 0], [uf_x, 1.20, 0], color=MID_GRAY, stroke_width=2.0)\n        uf_label = self.math(rf"UF={self._fmt(summary.uf)}", 25).next_to(uf_guide, UP, buff=0.06)\n        outlier_ring = Circle(radius=0.18, stroke_color=BLACK_LINE, stroke_width=2.4, fill_opacity=0).move_to([axis.n2p(35)[0], 0.65, 0])\n        outlier_note = self.text("35 is beyond the upper fence", 23, BOLD).next_to(outlier_ring, UP, buff=0.20)\n        self.fit(outlier_note, 4.5, 0.50)\n        self.play(Create(uf_guide), FadeIn(uf_label), Create(outlier_ring), FadeIn(outlier_note), run_time=RUN_NORMAL)\n''',
    '''        uf_x = axis.n2p(summary.uf)[0]\n        uf_guide = DashedLine([uf_x, -1.35, 0], [uf_x, 1.20, 0], color=MID_GRAY, stroke_width=2.0)\n        # Keep the fence label left of the guide and the outlier message above 35.\n        # This intentionally separates two different concepts: threshold vs datum.\n        uf_label = self.math(rf"UF={self._fmt(summary.uf)}", 25).move_to([uf_x - 0.62, 1.08, 0])\n        outlier_mark = plot[6][0]\n        outlier_note = self.text("35 is beyond the upper fence", 23, BOLD)\n        self.fit(outlier_note, 4.1, 0.50)\n        outlier_note.move_to([axis.n2p(35)[0], 1.58, 0])\n        self.play(\n            Create(uf_guide),\n            FadeIn(uf_label),\n            Circumscribe(outlier_mark, color=BLACK_LINE, buff=0.08),\n            FadeIn(outlier_note),\n            run_time=RUN_NORMAL,\n        )\n''',
    "read annotation separation",
)

out.write_text(s, encoding="utf-8")
print(f"Senior-QA V3 source written: {out}")
