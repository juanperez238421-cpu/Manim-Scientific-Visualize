#!/usr/bin/env python3
from pathlib import Path
import sys

path = Path(sys.argv[1])
source = path.read_text(encoding="utf-8")

old = '''        h = self.text(title, 31, BOLD)\n        row = VGroup(VGroup(badge, badge_text), h).arrange(RIGHT, buff=0.22)'''
new = '''        h = self.text(title, 31, BOLD)\n        if h.width > 13.15: h.scale_to_fit_width(13.15)\n        row = VGroup(VGroup(badge, badge_text), h).arrange(RIGHT, buff=0.22)'''
assert old in source, "section header target not found"
source = source.replace(old, new, 1)

old = '''        shaft_label = self.text("STEPPED SHAFT: one profile, many diameters", 24, BOLD)\n        shaft_label.move_to(LEFT * 3.2 + DOWN * 3.05)'''
new = '''        shaft_label = VGroup(self.text("STEPPED SHAFT", 24, BOLD), self.text("one profile, many diameters", 20)).arrange(DOWN, buff=0.05)\n        shaft_label.move_to(LEFT * 3.4 + DOWN * 3.05)'''
assert old in source, "shaft label target not found"
source = source.replace(old, new, 1)

old = '''        groove_label = self.text("REVOLVED CUT: a small profile removes a ring-shaped groove", 22, BOLD)\n        groove_label.move_to(RIGHT * 3.6 + DOWN * 3.05)'''
new = '''        groove_label = VGroup(self.text("REVOLVED CUT", 24, BOLD), self.text("small profile removes a ring-shaped groove", 19)).arrange(DOWN, buff=0.05)\n        groove_label.move_to(RIGHT * 3.6 + DOWN * 3.05)'''
assert old in source, "groove label target not found"
source = source.replace(old, new, 1)

path.write_text(source, encoding="utf-8")
