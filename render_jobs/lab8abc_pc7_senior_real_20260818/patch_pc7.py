#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

DATA_BLOCK = '''SEAT_LETTERS = ("A", "B", "C")
SEATS_BY_PC: Dict[int, Tuple[str, ...]] = {pc: SEAT_LETTERS for pc in range(1, 10)}
SEATS_BY_PC[7] = ("A", "B")  # Physical room constraint: PC07 has only two chairs.
SEAT_ORDER: List[Tuple[int, str]] = [
    (pc, seat)
    for pc in range(1, 10)
    for seat in SEATS_BY_PC[pc]
]

# Actual room disposition from the laboratory top-view map.
# top: PC09, PC06, PC03; middle: PC08, PC05, PC02; bottom: PC07, PC04, PC01.
PC_POSITIONS: Dict[int, Tuple[float, float]] = {
    9: (-2.75, 1.55), 6: (0.0, 1.55), 3: (2.75, 1.55),
    8: (-2.75, 0.00), 5: (0.0, 0.00), 2: (2.75, 0.00),
    7: (-2.75, -1.55), 4: (0.0, -1.55), 1: (2.75, -1.55),
}

ASSIGNMENTS: List[Tuple[int, str, int, str]] = []
for student_number, name in enumerate(STUDENTS, start=1):
    pc, seat = SEAT_ORDER[student_number - 1]
    ASSIGNMENTS.append((student_number, name, pc, seat))

AVAILABLE = [f"PC{pc:02d}-{seat}" for pc, seat in SEAT_ORDER[len(STUDENTS):]]


def assignment_summary_lines() -> List[str]:
    lines: List[str] = []
    for pc in range(1, 10):
        numbers = [n for n, _name, assigned_pc, _seat in ASSIGNMENTS if assigned_pc == pc]
        if not numbers:
            continue
        if len(numbers) == 1:
            lines.append(f"Estudiante {numbers[0]} → PC{pc:02d}")
        else:
            lines.append(f"Estudiantes {numbers[0]}–{numbers[-1]} → PC{pc:02d}")
    return lines


def final_legend_lines() -> List[str]:
    lines: List[str] = []
    for pc in range(1, 10):
        numbers = [n for n, _name, assigned_pc, _seat in ASSIGNMENTS if assigned_pc == pc]
        free = [code[-1] for code in AVAILABLE if code.startswith(f"PC{pc:02d}-")]
        if numbers:
            occupied = str(numbers[0]) if len(numbers) == 1 else f"{numbers[0]}–{numbers[-1]}"
            suffix = f" · libres {'/'.join(free)}" if free else ""
            lines.append(f"PC{pc:02d}: {occupied}{suffix}")
        else:
            lines.append(f"PC{pc:02d}: disponible")
    return lines
'''

VALIDATE = '''def validate_roster() -> None:
    assert len(ASSIGNMENTS) == len(STUDENTS)
    assert len(SEAT_ORDER) == 26
    assert ASSIGNMENTS[0][2:] == (1, "A")
    assert (7, "C") not in SEAT_ORDER
    assert all(not (pc == 7 and seat == "C") for _n, _name, pc, seat in ASSIGNMENTS)
    assert len(AVAILABLE) == 26 - len(STUDENTS)
    assert len(set(STUDENTS)) == len(STUDENTS)
    assert set(PC_POSITIONS.keys()) == set(range(1, 10))
'''

SEAT_LOOP = '''            seat_group = VGroup()
            seats = SEATS_BY_PC[pc]
            offsets = (-0.30, 0.30) if pc == 7 else (-0.57, 0.0, 0.57)
            for seat, offset in zip(seats, offsets):
                sx = x + offset
                sy = y - 0.34
                circle = Circle(
                    radius=0.19,
                    stroke_color=BLACK_LINE,
                    stroke_width=1.1,
                    fill_opacity=0,
                ).move_to([sx, sy, 0])
                letter = self.text(seat, 11, BOLD).next_to(circle, DOWN, buff=0.035)
                seat_group.add(circle, letter)
                seat_points[(pc, seat)] = np.array([sx, sy, 0])
                seat_outlines[(pc, seat)] = circle'''

FREE_ROWS = '''        for free_code_value in [code for code in AVAILABLE if code.startswith(f"PC{pc:02d}-")]:
            free_badge = Circle(radius=0.22, stroke_color=BLACK_LINE, stroke_width=1.4, fill_opacity=0)
            free_mark = self.text("—", 18, BOLD).move_to(free_badge)
            free_box = RoundedRectangle(
                width=1.05, height=0.46, corner_radius=0.07,
                stroke_color=BLACK_LINE, stroke_width=1.2,
                fill_color=VERY_LIGHT_GRAY, fill_opacity=1.0,
            )
            free_code = self.text(free_code_value, 16, BOLD).move_to(free_box)
            free_name = self.text("PUESTO DISPONIBLE", 18, MEDIUM)
            self.fit(free_name, 4.6, 0.45)
            rows.add(
                VGroup(VGroup(free_badge, free_mark), free_name, VGroup(free_box, free_code))
                .arrange(RIGHT, buff=0.18)
            )
'''

PC7_CALLOUT = '''
        # Senior QA emphasis: this is the only workstation with two physical chairs.
        pc7_focus = SurroundingRectangle(lab.desks[7], buff=0.07, color=BLACK_LINE, stroke_width=3.0)
        pc7_label = self.text("PC07 · SOLO 2 SILLAS", 18, BOLD).next_to(pc7_focus, UP, buff=0.05)
        self.play(Create(pc7_focus), FadeIn(pc7_label, shift=UP * 0.06), run_time=RUN_NORMAL)
        self.play(
            LaggedStart(
                *[Indicate(lab.seat_outlines[(7, seat)], scale_factor=1.25) for seat in SEATS_BY_PC[7]],
                lag_ratio=0.18,
            ),
            run_time=RUN_NORMAL,
        )
        self.wait(PAUSE_READ)
        self.play(FadeOut(pc7_focus), FadeOut(pc7_label), run_time=RUN_QUICK)
'''


def patch(path: Path, group: str) -> None:
    s = path.read_text(encoding="utf-8")

    s, n = re.subn(
        r'SEAT_LETTERS = \("A", "B", "C"\).*?\n\n# =============================================================================\n# SMALL STRUCTURED COMPONENTS',
        DATA_BLOCK + '\n\n# =============================================================================\n# SMALL STRUCTURED COMPONENTS',
        s, count=1, flags=re.S,
    )
    assert n == 1, f"data block patch failed: {group}"

    s, n = re.subn(
        r'def validate_roster\(\) -> None:\n.*?\n\n\n# =============================================================================\n# MAIN SCENE',
        VALIDATE + '\n\n# =============================================================================\n# MAIN SCENE',
        s, count=1, flags=re.S,
    )
    assert n == 1, f"validate patch failed: {group}"

    seat_pattern = r'''            seat_group = VGroup\(\)\n            for idx, seat in enumerate\(SEAT_LETTERS\):\n                sx = x \+ \(idx - 1\) \* 0\.57\n                sy = y - 0\.34\n                circle = Circle\(\n                    radius=0\.19,\n                    stroke_color=BLACK_LINE,\n                    stroke_width=1\.1,\n                    fill_opacity=0,\n                \)\.move_to\(\[sx, sy, 0\]\)\n                letter = self\.text\(seat, 11, BOLD\)\.next_to\(circle, DOWN, buff=0\.035\)\n                seat_group\.add\(circle, letter\)\n                seat_points\[\(pc, seat\)\] = np\.array\(\[sx, sy, 0\]\)\n                seat_outlines\[\(pc, seat\)\] = circle'''
    s, n = re.subn(seat_pattern, SEAT_LOOP, s, count=1)
    assert n == 1, f"seat geometry patch failed: {group}"

    s = s.replace(
        'title = self.text(f"PC {pc:02d} · 3 PUESTOS", 27, BOLD)',
        'title = self.text(f"PC {pc:02d} · {len(SEATS_BY_PC[pc])} PUESTOS", 27, BOLD)',
        1,
    )

    # Remove group-specific placeholder rows from earlier versions, then insert generic free-seat rows.
    s = re.sub(r'\n        if pc == (8|9):\n.*?(?=        rows\.arrange\(DOWN, aligned_edge=LEFT, buff=0\.30\))', '\n', s, count=1, flags=re.S)
    s = s.replace('        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.30)', FREE_ROWS + '        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.30)', 1)

    s = re.sub(r'"\d+ estudiantes · 9 computadores · 3 puestos por computador",', 'f"{len(STUDENTS)} estudiantes · 9 computadores · PC07 con 2 sillas",', s, count=1)
    s = re.sub(r'"Orden de lista: 1 → \d+",', 'f"Orden de lista: 1 → {len(STUDENTS)}",', s, count=1)
    s = s.replace('"Dentro de cada PC: silla A → B → C",', '"Sillas A → B → C; PC07 solo tiene A → B",', 1)
    s = re.sub(r'"ASIGNACIÓN '+group+r': TRES ESTUDIANTES POR COMPUTADOR",', '"ASIGNACIÓN '+group+': PUESTO FIJO POR ORDEN DE LISTA",', s, count=1)

    # 8A now reaches PC08 because PC07 lost one seat. 8B and 8C already traverse far enough.
    if group == "8A":
        s = s.replace('for pc in range(1, 8):', 'for pc in range(1, 9):', 1)

    s, n = re.subn(
        r'''            \[\n                "Estudiantes 1–3   → PC01",.*?\n            \],\n            width=5\.35,''',
        '            assignment_summary_lines(),\n            width=5.35,',
        s, count=1, flags=re.S,
    )
    assert n == 1, f"summary patch failed: {group}"

    s = re.sub(
        r'"Con \d+ estudiantes quedan libres .*?; estos espacios solo se usarán si el docente lo indica\.",',
        'f"Con {len(STUDENTS)} estudiantes quedan libres {len(AVAILABLE)} puestos; estos espacios solo se usarán si el docente lo indica.",',
        s, count=1,
    )
    s = re.sub(r'available_title = self\.text\("\d+ PUESTOS DISPONIBLES", 25, BOLD\)', 'available_title = self.text(f"{len(AVAILABLE)} PUESTOS DISPONIBLES", 25, BOLD)', s, count=1)
    s = s.replace('for pc in (8, 9):', 'for pc in sorted({int(code[2:4]) for code in AVAILABLE}):', 1)
    s = s.replace('for pc in (9,):', 'for pc in sorted({int(code[2:4]) for code in AVAILABLE}):', 1)

    # PC07 callout is inserted only inside room_orientation, after the criterion panel is visible.
    anchor = '        self.play(FadeIn(note, shift=LEFT * 0.10), run_time=RUN_NORMAL)\n        self.wait(PAUSE_EXPLAIN)\n'
    assert anchor in s, f"orientation anchor missing: {group}"
    s = s.replace(anchor, anchor + PC7_CALLOUT, 1)

    s = s.replace(
        '"Para encontrar un estudiante: ubique su número de lista, identifique el computador y luego la silla A, B o C.",',
        '"Para encontrar un estudiante: ubique su número de lista, identifique el computador y la silla. PC07 solo tiene A y B.",',
        1,
    )
    s, n = re.subn(
        r'''        legend = VGroup\(\n            self\.text\("PC01: 1–3", 17, BOLD\),.*?\n        \)\.arrange_in_grid\(cols=3, buff=\(0\.32, 0\.12\)\)''',
        '        legend = VGroup(*[self.text(line, 17, BOLD) for line in final_legend_lines()]).arrange_in_grid(cols=3, buff=(0.32, 0.12))',
        s, count=1, flags=re.S,
    )
    assert n == 1, f"legend patch failed: {group}"

    compile(s, str(path), 'exec')
    path.write_text(s, encoding="utf-8")


for group in ("8A", "8B", "8C"):
    patch(ROOT / f"lab{group.lower()}_seating.py", group)

print("PC07 two-seat patch applied to 8A, 8B, and 8C")
