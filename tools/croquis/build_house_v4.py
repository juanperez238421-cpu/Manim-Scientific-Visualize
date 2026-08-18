from pathlib import Path

src = Path('render_jobs/house_step_v3/House_Extrusion_3D_STEP_BY_STEP_V3_DECODED.py')
text = src.read_text(encoding='utf-8')


def replace1(old, new):
    global text
    if old not in text:
        raise RuntimeError(f'Expected source block not found:\n{old[:180]}')
    text = text.replace(old, new, 1)


replace1(
'''    HOUSE_W = 9.20
    HOUSE_D = 6.20

    def box(self, dims, center, color, opacity=1.0, stroke=DARK, stroke_width=0.8):
''',
'''    HOUSE_W = 9.20
    HOUSE_D = 6.20

    # Croquis protocol V1 — deterministic camera + semantic pacing states.
    # PLAN_2D: camera normal to horizontal sketch planes (XY).
    # FRONT_FACE_2D: camera normal to the front facade sketch plane (XZ).
    PLAN_2D_PHI = 0 * DEGREES
    PLAN_2D_THETA = -90 * DEGREES
    PLAN_2D_ZOOM = 0.80
    FRONT_2D_PHI = 90 * DEGREES
    FRONT_2D_THETA = -90 * DEGREES
    FRONT_2D_ZOOM = 0.82

    CAMERA_SETTLE_PAUSE = 0.75
    MICRO_PAUSE = 0.40
    CONSTRUCTION_PAUSE = 0.70
    READING_PAUSE = 1.20
    EXPLANATION_PAUSE = 1.55
    FINAL_OBSERVATION_PAUSE = 1.90

    def box(self, dims, center, color, opacity=1.0, stroke=DARK, stroke_width=0.8):
''')

replace1(
'''    def set_phase(self, state, number, label, color=DARK):
        old = state["text"]
        new = self.text(f"{number:02d} · {label}", 19, BOLD, color).move_to(state["box"])
        self.add_fixed_in_frame_mobjects(new)
        self.play(FadeOut(old), FadeIn(new), run_time=0.38)
        self.remove_fixed_in_frame_mobjects(old)
        self.remove(old)
        state["text"] = new

    # ------------------------------------------------------------------
    # 2D CAD sketches
''',
'''    def set_phase(self, state, number, label, color=DARK):
        old = state["text"]
        new = self.text(f"{number:02d} · {label}", 19, BOLD, color).move_to(state["box"])
        self.add_fixed_in_frame_mobjects(new)
        self.play(FadeOut(old), FadeIn(new), run_time=0.38)
        self.remove_fixed_in_frame_mobjects(old)
        self.remove(old)
        state["text"] = new

    # ------------------------------------------------------------------
    # Croquis camera protocol V1
    # ------------------------------------------------------------------
    def enter_plan_croquis(self, run_time=1.5, zoom=None, settle=None):
        """Enter a true top/plan 2D state before drawing on a horizontal face."""
        self.move_camera(
            phi=self.PLAN_2D_PHI, theta=self.PLAN_2D_THETA,
            zoom=self.PLAN_2D_ZOOM if zoom is None else zoom,
            run_time=run_time,
        )
        self.wait(self.CAMERA_SETTLE_PAUSE if settle is None else settle)

    def enter_front_face_croquis(self, run_time=1.5, zoom=None, settle=None):
        """Enter an orthographic-like face-normal 2D state for front-facade sketches."""
        self.move_camera(
            phi=self.FRONT_2D_PHI, theta=self.FRONT_2D_THETA,
            zoom=self.FRONT_2D_ZOOM if zoom is None else zoom,
            run_time=run_time,
        )
        self.wait(self.CAMERA_SETTLE_PAUSE if settle is None else settle)

    def return_model_view(self, phi, theta, zoom, run_time=1.5, settle=0.30):
        """Exit croquis mode deliberately before showing depth or volumetric operations."""
        self.move_camera(phi=phi, theta=theta, zoom=zoom, run_time=run_time)
        if settle > 0:
            self.wait(settle)

    # ------------------------------------------------------------------
    # 2D CAD sketches
''')

replace1(
'''        # 02 — slab footprint only
        self.set_phase(phase, 2, "CROQUIS · LOSA", SKETCH)
        slab_sketch = self.slab_outline(z=0.045)
        note = self.phase_note("Croquis 2D cerrado sobre el terreno", SKETCH)
        self.play(LaggedStart(*[Create(m) for m in slab_sketch], lag_ratio=0.16), run_time=2.3)
        self.wait(1.1)
        self.remove_note(note)
''',
'''        # 02 — slab footprint only: explicit PLAN_2D croquis state
        self.set_phase(phase, 2, "CROQUIS · LOSA", SKETCH)
        self.enter_plan_croquis(run_time=0.65, zoom=0.80, settle=0.70)
        slab_sketch = self.slab_outline(z=0.045)
        note = self.phase_note("Croquis 2D cerrado sobre el terreno", SKETCH)
        self.wait(self.MICRO_PAUSE)
        self.play(LaggedStart(*[Create(m) for m in slab_sketch], lag_ratio=0.16), run_time=2.3)
        self.wait(self.EXPLANATION_PAUSE)
        self.remove_note(note)
''')

replace1(
'        self.move_camera(phi=56*DEGREES, theta=-52*DEGREES, zoom=0.72, run_time=2.0)\n',
'        self.return_model_view(phi=56*DEGREES, theta=-52*DEGREES, zoom=0.72, run_time=2.0, settle=0.35)\n')

replace1(
'''        # 04 — NEW sketch on the top face of slab
        self.set_phase(phase, 4, "CROQUIS · MUROS + COLUMNAS", SKETCH)
        self.move_camera(phi=36*DEGREES, theta=-58*DEGREES, zoom=0.75, run_time=1.6)
        zsk = self.FLOOR_Z + 0.025
        ext_trace, int_trace = self.wall_trace(zsk)
        col_profiles = self.column_profiles(zsk + 0.003)
        note = self.phase_note("Nueva cara activa: dibujamos encima de la losa", SKETCH)
        self.play(LaggedStart(*[Create(m) for m in ext_trace], lag_ratio=0.12), run_time=1.8)
        self.play(LaggedStart(*[Create(m) for m in int_trace], lag_ratio=0.12), run_time=1.6)
        self.play(LaggedStart(*[Create(m) for m in col_profiles], lag_ratio=0.07), run_time=2.0)
        self.wait(1.6)
        self.remove_note(note)
''',
'''        # 04 — NEW sketch on the top face of slab: return to true PLAN_2D first
        self.set_phase(phase, 4, "CROQUIS · MUROS + COLUMNAS", SKETCH)
        self.enter_plan_croquis(run_time=1.75, zoom=0.78, settle=0.85)
        zsk = self.FLOOR_Z + 0.025
        ext_trace, int_trace = self.wall_trace(zsk)
        col_profiles = self.column_profiles(zsk + 0.003)
        note = self.phase_note("Nueva cara activa: dibujamos encima de la losa", SKETCH)
        self.wait(self.MICRO_PAUSE)
        self.play(LaggedStart(*[Create(m) for m in ext_trace], lag_ratio=0.12), run_time=1.8)
        self.wait(self.CONSTRUCTION_PAUSE)
        self.play(LaggedStart(*[Create(m) for m in int_trace], lag_ratio=0.12), run_time=1.6)
        self.wait(self.CONSTRUCTION_PAUSE)
        self.play(LaggedStart(*[Create(m) for m in col_profiles], lag_ratio=0.07), run_time=2.0)
        self.wait(self.FINAL_OBSERVATION_PAUSE)
        self.remove_note(note)
''')

replace1(
'''        # 05 — columns
        self.set_phase(phase, 5, "EXTRUSIÓN + · COLUMNAS", POSITIVE)
        note = self.phase_note("Cada cuadrado se extruye verticalmente", POSITIVE)
''',
'''        # 05 — columns: leave PLAN_2D before depth is introduced
        self.set_phase(phase, 5, "EXTRUSIÓN + · COLUMNAS", POSITIVE)
        self.return_model_view(phi=36*DEGREES, theta=-58*DEGREES, zoom=0.75, run_time=1.65, settle=0.35)
        note = self.phase_note("Cada cuadrado se extruye verticalmente", POSITIVE)
        self.wait(self.MICRO_PAUSE)
''')

replace1(
'''        self.play(LaggedStart(*[Transform(a,b) for a,b in zip(col_seeds,col_targets)], lag_ratio=0.10), run_time=3.6, rate_func=smooth)
        self.play(FadeOut(col_profiles), run_time=0.5)
        self.wait(0.9)
''',
'''        self.play(LaggedStart(*[Transform(a,b) for a,b in zip(col_seeds,col_targets)], lag_ratio=0.10), run_time=3.6, rate_func=smooth)
        self.wait(self.READING_PAUSE)
        self.play(FadeOut(col_profiles), run_time=0.5)
        self.wait(self.MICRO_PAUSE)
''')

replace1(
'''        self.play(LaggedStart(*[Transform(a,b) for a,b in zip(ext_seeds,ext_targets)], lag_ratio=0.10), run_time=3.7, rate_func=smooth)
        self.remove_note(note)
''',
'''        self.play(LaggedStart(*[Transform(a,b) for a,b in zip(ext_seeds,ext_targets)], lag_ratio=0.10), run_time=3.7, rate_func=smooth)
        self.wait(self.READING_PAUSE)
        self.remove_note(note)
''')

replace1(
'''        self.play(LaggedStart(*[Transform(a,b) for a,b in zip(int_seeds,int_targets)], lag_ratio=0.11), run_time=3.4, rate_func=smooth)
        self.play(FadeOut(int_trace), run_time=0.45)
        self.wait(0.8)
''',
'''        self.play(LaggedStart(*[Transform(a,b) for a,b in zip(int_seeds,int_targets)], lag_ratio=0.11), run_time=3.4, rate_func=smooth)
        self.wait(self.READING_PAUSE)
        self.play(FadeOut(int_trace), run_time=0.45)
        self.wait(self.MICRO_PAUSE)
''')

replace1(
'''        # 07 — negative extrusion door
        self.set_phase(phase, 7, "EXTRUSIÓN − · PUERTA", NEGATIVE)
        self.move_camera(phi=66*DEGREES, theta=-55*DEGREES, zoom=0.78, run_time=1.8)
        door_x, door_w = -1.95, 1.20
        door_bottom, door_h = self.FLOOR_Z, 2.15
        profile = self.vertical_profile(door_x, door_w, door_bottom, door_h, -self.HOUSE_D/2 - 0.12)
        note = self.phase_note("Perfil rojo = volumen que será retirado", NEGATIVE)
        self.play(Create(profile), run_time=1.2)
        cutter = self.cutter_front(door_x, door_w, door_bottom, door_h)
''',
'''        # 07 — negative extrusion door: sketch face-normal, then reveal depth in 3D
        self.set_phase(phase, 7, "EXTRUSIÓN − · PUERTA", NEGATIVE)
        self.enter_front_face_croquis(run_time=1.75, zoom=0.82, settle=0.85)
        door_x, door_w = -1.95, 1.20
        door_bottom, door_h = self.FLOOR_Z, 2.15
        profile = self.vertical_profile(door_x, door_w, door_bottom, door_h, -self.HOUSE_D/2 - 0.12)
        note = self.phase_note("Perfil rojo = volumen que será retirado", NEGATIVE)
        self.wait(self.MICRO_PAUSE)
        self.play(Create(profile), run_time=1.2)
        self.wait(self.READING_PAUSE)
        self.return_model_view(phi=66*DEGREES, theta=-55*DEGREES, zoom=0.78, run_time=1.55, settle=0.35)
        cutter = self.cutter_front(door_x, door_w, door_bottom, door_h)
''')

replace1(
'''        self.wait(1.0)
        self.remove_note(note)

        # 08 — negative extrusion window
''',
'''        self.wait(self.EXPLANATION_PAUSE)
        self.remove_note(note)

        # 08 — negative extrusion window
''')

replace1(
'''        # 08 — negative extrusion window
        self.set_phase(phase, 8, "EXTRUSIÓN − · VENTANA", NEGATIVE)
        win_x, win_w = 2.225, 1.85
        win_bottom, win_h = self.FLOOR_Z + 0.88, 1.17
        profile2 = self.vertical_profile(win_x, win_w, win_bottom, win_h, -self.HOUSE_D/2 - 0.12)
        note = self.phase_note("Misma operación: croquis → profundidad → corte", NEGATIVE)
        self.play(Create(profile2), run_time=1.1)
        cutter2 = self.cutter_front(win_x, win_w, win_bottom, win_h)
''',
'''        # 08 — negative extrusion window: repeat the same FACE_2D → 3D causal grammar
        self.set_phase(phase, 8, "EXTRUSIÓN − · VENTANA", NEGATIVE)
        self.enter_front_face_croquis(run_time=1.55, zoom=0.82, settle=0.75)
        win_x, win_w = 2.225, 1.85
        win_bottom, win_h = self.FLOOR_Z + 0.88, 1.17
        profile2 = self.vertical_profile(win_x, win_w, win_bottom, win_h, -self.HOUSE_D/2 - 0.12)
        note = self.phase_note("Misma operación: croquis → profundidad → corte", NEGATIVE)
        self.wait(self.MICRO_PAUSE)
        self.play(Create(profile2), run_time=1.1)
        self.wait(self.READING_PAUSE)
        self.return_model_view(phi=66*DEGREES, theta=-55*DEGREES, zoom=0.78, run_time=1.45, settle=0.30)
        cutter2 = self.cutter_front(win_x, win_w, win_bottom, win_h)
''')

replace1(
'''        self.play(FadeIn(glass), run_time=0.55)
        self.wait(1.0)
        self.remove_note(note)
''',
'''        self.play(FadeIn(glass), run_time=0.55)
        self.wait(self.EXPLANATION_PAUSE)
        self.remove_note(note)
''')

replace1(
'''        # 09 — roof positive extrusion
        self.set_phase(phase, 9, "EXTRUSIÓN + · CUBIERTA", POSITIVE)
        note = self.phase_note("Última operación aditiva: cubierta", POSITIVE)
        roof_base = self.FLOOR_Z + self.COL_H
''',
'''        # 09 — roof positive extrusion: roof outline is also a croquis, so enter PLAN_2D
        self.set_phase(phase, 9, "EXTRUSIÓN + · CUBIERTA", POSITIVE)
        self.enter_plan_croquis(run_time=1.75, zoom=0.77, settle=0.85)
        note = self.phase_note("Última operación aditiva: cubierta", POSITIVE)
        roof_base = self.FLOOR_Z + self.COL_H
''')

replace1(
'''        self.play(LaggedStart(*[Create(m) for m in roof_outline], lag_ratio=0.14), run_time=1.5)
        roof_seed = self.box((self.HOUSE_W+0.45,self.HOUSE_D+0.45,0.025), (0,0,roof_base+0.0125), SLAB, 0.72)
''',
'''        self.wait(self.MICRO_PAUSE)
        self.play(LaggedStart(*[Create(m) for m in roof_outline], lag_ratio=0.14), run_time=1.7)
        self.wait(self.READING_PAUSE)
        self.return_model_view(phi=58*DEGREES, theta=-52*DEGREES, zoom=0.73, run_time=1.65, settle=0.30)
        roof_seed = self.box((self.HOUSE_W+0.45,self.HOUSE_D+0.45,0.025), (0,0,roof_base+0.0125), SLAB, 0.72)
''')

replace1(
'''        self.play(roof_seed.animate.set_fill(opacity=0.22), run_time=0.8)
        self.wait(0.8)
''',
'''        self.play(roof_seed.animate.set_fill(opacity=0.22), run_time=0.8)
        self.wait(self.EXPLANATION_PAUSE)
''')

replace1(
'        self.move_camera(phi=63*DEGREES, theta=-50*DEGREES, zoom=0.72, run_time=1.8)\n',
'        self.return_model_view(phi=63*DEGREES, theta=-50*DEGREES, zoom=0.72, run_time=1.8, settle=0.35)\n')

out = Path('render_jobs/house_step_v3/House_Extrusion_3D_STEP_BY_STEP_V4_CROQUIS_PROTOCOL.py')
out.write_text(text, encoding='utf-8')
print(f'Wrote {out} ({len(text.splitlines())} lines)')
