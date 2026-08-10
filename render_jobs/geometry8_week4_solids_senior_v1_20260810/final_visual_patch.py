from pathlib import Path
import sys

p = Path(sys.argv[1])
s = p.read_text()

# Resolve the helper/scene method name collision.
old = '    def triangular_prism(self, *, center: np.ndarray = ORIGIN, scale: float = 1.0) -> VGroup:'
new = '    def triangular_prism_model(self, *, center: np.ndarray = ORIGIN, scale: float = 1.0) -> VGroup:'
assert s.count(old) == 1
s = s.replace(old, new, 1)
old = '        prism = self.triangular_prism(center=LEFT * 3.65 + DOWN * 0.55, scale=1.0)'
new = '        prism = self.triangular_prism_model(center=LEFT * 3.65 + DOWN * 0.55, scale=1.0)'
assert s.count(old) == 1
s = s.replace(old, new, 1)

# Make the triangular-base altitude explicit and perpendicular.
old = '''        prism = self.triangular_prism_model(center=LEFT * 3.65 + DOWN * 0.55, scale=1.0)\n        labels = VGroup(\n            self.math(r"6", 28).move_to(LEFT * 3.65 + DOWN * 1.92),\n            self.math(r"4", 28).move_to(LEFT * 3.65 + DOWN * 0.45),\n            self.math(r"5", 26).move_to(LEFT * 5.0 + DOWN * 0.30),\n            self.math(r"10", 28).move_to(LEFT * 1.25 + UP * 0.72),\n        )\n        fig = VGroup(prism, labels)\n'''
new = '''        prism_center = LEFT * 3.65 + DOWN * 0.55\n        prism = self.triangular_prism_model(center=prism_center, scale=1.0)\n        # The 4 cm measurement is the perpendicular altitude of the FRONT triangular base.\n        front_apex = prism_center + UP * 1.35\n        front_midpoint = prism_center + DOWN * 1.15\n        altitude = Line(front_apex, front_midpoint, color=BLACK_LINE, stroke_width=2.5)\n        right_mark = Square(\n            side_length=0.24, stroke_color=BLACK_LINE, stroke_width=1.7, fill_opacity=0\n        ).move_to(front_midpoint + UR * 0.12)\n        labels = VGroup(\n            self.math(r"6", 28).next_to(Line(prism_center + LEFT * 1.7 + DOWN * 1.15, prism_center + RIGHT * 1.7 + DOWN * 1.15), DOWN, buff=0.10),\n            self.math(r"4", 28).next_to(altitude, RIGHT, buff=0.12),\n            self.math(r"5", 26).move_to(LEFT * 5.0 + DOWN * 0.30),\n            self.math(r"10", 28).move_to(LEFT * 1.25 + UP * 0.72),\n        )\n        fig = VGroup(prism, altitude, right_mark, labels)\n'''
assert s.count(old) == 1
s = s.replace(old, new, 1)

# Keep scaling figures separate from the table.
old = '''        small = self.iso_prism(width=2.0, height=2.0, depth=0.65,\n                               center=LEFT * 4.2 + DOWN * 0.40)\n        large = self.iso_prism(width=3.4, height=3.4, depth=1.0,\n                               center=LEFT * 0.85 + DOWN * 0.48)\n'''
new = '''        small = self.iso_prism(width=1.65, height=1.65, depth=0.55,\n                               center=LEFT * 4.75 + DOWN * 0.45)\n        large = self.iso_prism(width=2.75, height=2.75, depth=0.82,\n                               center=LEFT * 2.05 + DOWN * 0.48)\n'''
assert s.count(old) == 1
s = s.replace(old, new, 1)

# Keep composite-solid contact annotation inside the figure region.
old = '        contact_label = self.text("internal contact", 21, BOLD).next_to(contact, RIGHT, buff=0.12)\n'
new = '        contact_label = self.text("hidden contact = 4 x 3", 18, BOLD).move_to(LEFT * 3.35 + DOWN * 0.22)\n'
assert s.count(old) == 1
s = s.replace(old, new, 1)

p.write_text(s)
