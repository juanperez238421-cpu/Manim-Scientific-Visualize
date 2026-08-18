from pathlib import Path

SRC = Path("job/House_Extrusion_3D_ManimCE.py")
s = SRC.read_text(encoding="utf-8")

old_group = '''        phase_group = VGroup(phase_box, phase)

        add_dot = Circle(radius=0.07, fill_color=POSITIVE, fill_opacity=1, stroke_width=0)
        add_text = self.text("+  AÑADIR MATERIAL", 17, BOLD, POSITIVE)
        rem_dot = Circle(radius=0.07, fill_color=NEGATIVE, fill_opacity=1, stroke_width=0)
        rem_text = self.text("−  RETIRAR MATERIAL", 17, BOLD, NEGATIVE)
        legend = VGroup(add_dot, add_text, rem_dot, rem_text).arrange(RIGHT, buff=0.25)
        legend.to_edge(DOWN, buff=0.25)

        self.add_fixed_in_frame_mobjects(title, subtitle, rule, phase_group, legend)
        self.add(title, subtitle, rule, phase_group, legend)
        return phase_group
'''

new_group = '''        phase_state = [phase_box, phase]

        add_dot = Circle(radius=0.07, fill_color=POSITIVE, fill_opacity=1, stroke_width=0)
        add_text = self.text("+  AÑADIR MATERIAL", 17, BOLD, POSITIVE)
        rem_dot = Circle(radius=0.07, fill_color=NEGATIVE, fill_opacity=1, stroke_width=0)
        rem_text = self.text("−  RETIRAR MATERIAL", 17, BOLD, NEGATIVE)
        legend = VGroup(add_dot, add_text, rem_dot, rem_text).arrange(RIGHT, buff=0.25)
        legend.to_edge(DOWN, buff=0.25)

        # Register static HUD elements directly. In Cairo, this also adds them to the scene.
        self.add_fixed_in_frame_mobjects(title, subtitle, rule, phase_box, phase, legend)
        return phase_state
'''

old_set = '''    def set_phase(self, phase_group, number, label, color=DARK):
        old_box, old_text = phase_group
        new_text = self.text(f"{number:02d} · {label}", 20, BOLD, color)
        new_text.move_to(old_box)
        self.play(Transform(old_text, new_text), run_time=0.55)
'''

new_set = '''    def set_phase(self, phase_state, number, label, color=DARK):
        old_box, old_text = phase_state
        new_text = self.text(f"{number:02d} · {label}", 20, BOLD, color)
        new_text.move_to(old_box)
        if new_text.width > old_box.width - 0.28:
            new_text.scale_to_fit_width(old_box.width - 0.28)
        new_text.set_opacity(0)

        # Do not Transform fixed-in-frame Text glyphs: new glyph submobjects would not
        # inherit the camera's fixed-in-frame registration under Cairo.
        self.play(old_text.animate.set_opacity(0), run_time=0.14)
        self.remove_fixed_in_frame_mobjects(old_text)
        self.remove(old_text)
        self.add_fixed_in_frame_mobjects(new_text)
        self.play(new_text.animate.set_opacity(1), run_time=0.22)
        phase_state[1] = new_text
'''

assert old_group in s, "fixed_hud phase group block not found"
assert old_set in s, "set_phase block not found"
s = s.replace(old_group, new_group).replace(old_set, new_set)
SRC.write_text(s, encoding="utf-8")
print("fixed_in_frame_hud_patch=applied")
