#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Statistics class — Data Types in Google Colab, Senior QA V2.

Revision goals from rendered-video QA:
- Correct None/NoneType terminology.
- Use more of the safe content area and reduce dead whitespace.
- Make the Colab mental model explicit: value -> type -> statistical meaning.
- Improve motion grammar with progressive transformations, arrows and highlights.
- Preserve JP classroom style and ManimCE 0.20.x compatibility.
"""

from __future__ import annotations

from jp_classroom_style import *


class StatisticsColabDataTypesV2(JPMathClassroomScene):
    """Senior-QA revision of the Colab data-types statistics lesson."""

    SCORES = [4.2, 3.8, 4.5, 3.9]
    GROUPS = ["10A", "10B", "10A", "10B"]
    PASSED = [True, True, True, True]

    def validate_lesson_data(self) -> None:
        assert_close(sum(self.SCORES) / len(self.SCORES), 4.1, label="mean score")
        assert len(self.SCORES) == len(self.GROUPS) == len(self.PASSED) == 4
        assert sum(1 for g in self.GROUPS if g == "10A") == 2
        assert all(isinstance(x, float) for x in self.SCORES)
        assert all(isinstance(x, str) for x in self.GROUPS)
        assert all(isinstance(x, bool) for x in self.PASSED)
        assert type(None).__name__ == "NoneType"

    def construct(self) -> None:
        self.validate_lesson_data()
        self.opening()
        self.scene_01_value_type_meaning()
        self.scene_02_scalar_types()
        self.scene_03_collections()
        self.scene_04_inspect_convert()
        self.scene_05_dataframe()
        self.scene_06_statistics_mapping()
        self.scene_07_summary()

    def code_cell(self, code_lines, output_lines=None, *, width=6.5, title="COLAB CELL", code_size=24, output_size=22, execution="[ ]"):
        output_lines = output_lines or []
        run = self.text("▶", 18, BOLD)
        exec_mob = self.text(execution, 17, MEDIUM, font="DejaVu Sans Mono")
        title_mob = self.text(title, 19, BOLD)
        title_row = VGroup(run, exec_mob, title_mob).arrange(RIGHT, buff=0.11)
        code = VGroup(*[self.text(line, code_size, font="DejaVu Sans Mono") for line in code_lines])
        code.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        chunks = [title_row, code]
        if output_lines:
            divider = Line(LEFT, RIGHT, color=LIGHT_GRAY, stroke_width=1.2)
            divider.set_width(width - 0.55)
            output_label = self.text("OUTPUT", 16, BOLD)
            output = VGroup(*[self.text(line, output_size, font="DejaVu Sans Mono") for line in output_lines])
            output.arrange(DOWN, aligned_edge=LEFT, buff=0.07)
            chunks.extend([divider, output_label, output])
        content = VGroup(*chunks).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        self.fit(content, width - 0.54, 4.95)
        box = RoundedRectangle(width=width, height=max(1.25, content.height + 0.48), corner_radius=0.12, stroke_color=BLACK_LINE, stroke_width=1.7, fill_color=WHITE_FILL, fill_opacity=1.0)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.27)
        return VGroup(box, content)

    def concept_card(self, heading, example, meaning, *, width=4.1, height=1.65):
        heading_mob = self.text(heading, 27, BOLD)
        example_mob = self.text(example, 22, font="DejaVu Sans Mono")
        meaning_mob = self.text(meaning, 20)
        self.fit(meaning_mob, width - 0.42, 0.52)
        content = VGroup(heading_mob, example_mob, meaning_mob).arrange(DOWN, buff=0.11)
        box = RoundedRectangle(width=width, height=height, corner_radius=0.12, stroke_color=BLACK_LINE, stroke_width=1.6, fill_color=WHITE_FILL, fill_opacity=1)
        content.move_to(box)
        return VGroup(box, content)

    def label_box(self, text_value, *, width=3.25, size=22):
        box = RoundedRectangle(width=width, height=0.78, corner_radius=0.10, stroke_color=BLACK_LINE, stroke_width=1.5, fill_color=VERY_LIGHT_GRAY, fill_opacity=1)
        txt = self.text(text_value, size, BOLD)
        self.fit(txt, width - 0.35, 0.52)
        txt.move_to(box)
        return VGroup(box, txt)

    def arrow_between(self, left, right):
        return Arrow(left.get_right() + RIGHT * 0.08, right.get_left() + LEFT * 0.08, buff=0.06, stroke_width=2.2, color=BLACK_LINE, max_tip_length_to_length_ratio=0.18)

    def opening(self) -> None:
        self.standard_opening("STATISTICS • GOOGLE COLAB", "DATA TYPES", "From a stored value to a valid statistical calculation", "VALUE  →  TYPE  →  MEANING  →  OPERATION")

    def scene_01_value_type_meaning(self) -> None:
        self.set_header(1, "THE SAME SYMBOLS CAN REPRESENT DIFFERENT DATA", "In Colab, Python first sees a stored value and its programming type; statistics then asks what that value means.")
        numeric = self.code_cell(["a = 10", "b = 5", "a + b"], ["15"], width=5.85, title="NUMERIC VALUES", execution="[1]", code_size=25)
        text = self.code_cell(['a = "10"', 'b = "5"', "a + b"], ['"105"'], width=5.85, title="TEXT VALUES", execution="[2]", code_size=25)
        VGroup(numeric, text).arrange(RIGHT, buff=0.62).move_to(UP * 0.20)
        num_tag = self.label_box("int + int  →  arithmetic", width=5.2, size=21); num_tag.next_to(numeric, DOWN, buff=0.20)
        str_tag = self.label_box("str + str  →  concatenation", width=5.2, size=21); str_tag.next_to(text, DOWN, buff=0.20)
        takeaway = self.note_panel("FIRST CHECK", ["A value that looks like a number may still be stored as text.", "The stored type determines which operation Python performs."], width=10.4, title_size=26, body_size=23)
        takeaway.to_edge(DOWN, buff=0.24)
        self.play(FadeIn(numeric, shift=UP * 0.10), run_time=RUN_NORMAL); self.play(Write(num_tag), run_time=RUN_NORMAL); self.wait(PAUSE_READ)
        self.play(FadeIn(text, shift=UP * 0.10), run_time=RUN_NORMAL); self.play(Write(str_tag), run_time=RUN_NORMAL); self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(takeaway), run_time=RUN_NORMAL); self.wait(PAUSE_WORK); self.clear_stage()

    def scene_02_scalar_types(self) -> None:
        self.set_header(2, "CORE PYTHON VALUES YOU WILL MEET IN A DATASET", "Use Python terminology precisely: None is a value; type(None) is NoneType. In pandas, missing data may also appear as NaN or pd.NA.")
        cards = VGroup(self.concept_card("int", "students = 28", "Whole-number count", width=4.0), self.concept_card("float", "mean = 4.25", "Decimal measurement", width=4.0), self.concept_card("str", 'group = "10A"', "Text / category label", width=4.0), self.concept_card("bool", "passed = True", "Binary condition", width=4.0), self.concept_card("NoneType", "missing = None", "Missing-value marker", width=4.0))
        cards.arrange_in_grid(cols=3, buff=(0.34, 0.32)); cards.move_to(UP * 0.02); self.fit_content_zone(cards, 13.7, 4.45)
        meaning = self.label_box("PROGRAMMING TYPE  ≠  STATISTICAL VARIABLE TYPE", width=9.5, size=24); meaning.to_edge(DOWN, buff=0.28)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.12) for card in cards], lag_ratio=0.13), run_time=RUN_SLOW * 1.6); self.wait(PAUSE_READ)
        self.play(Write(meaning), run_time=RUN_NORMAL); self.wait(PAUSE_WORK); self.clear_stage()

    def scene_03_collections(self) -> None:
        self.set_header(3, "FROM ONE VALUE TO A DATASET: LISTS AND DICTIONARIES", "A list is useful for repeated observations; a dictionary groups named fields for one observation. Both lead naturally to pandas.")
        list_cell = self.code_cell(["scores = [4.2, 3.8, 4.5, 3.9]", "len(scores)", "sum(scores) / len(scores)"], ["4", "4.1"], width=6.65, title="LIST = ONE VARIABLE", execution="[3]", code_size=22)
        dict_cell = self.code_cell(['student = {', '  "name": "Ana",', '  "group": "10A",', '  "score": 4.2', '}', 'student["score"]'], ["4.2"], width=6.35, title="DICT = ONE OBSERVATION", execution="[4]", code_size=20)
        pair = VGroup(list_cell, dict_cell).arrange(RIGHT, buff=0.52).move_to(UP * 0.02); self.fit_content_zone(pair, 13.85, 4.70)
        left_tag = self.label_box("4 observations of Score", width=5.1, size=21); left_tag.next_to(list_cell, DOWN, buff=0.18)
        right_tag = self.label_box("4 fields describing Ana", width=5.1, size=21); right_tag.next_to(dict_cell, DOWN, buff=0.18)
        bridge = self.label_box("NEXT: combine many observations → DataFrame", width=7.6, size=22); bridge.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(list_cell), run_time=RUN_NORMAL); self.play(Write(left_tag), run_time=RUN_QUICK); self.wait(PAUSE_READ)
        self.play(FadeIn(dict_cell), run_time=RUN_NORMAL); self.play(Write(right_tag), run_time=RUN_QUICK); self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(bridge, shift=UP * 0.10), run_time=RUN_NORMAL); self.wait(PAUSE_WORK); self.clear_stage()

    def scene_04_inspect_convert(self) -> None:
        self.set_header(4, "INSPECT → CONVERT → CALCULATE", "Do not convert blindly. First inspect the stored type, then convert only when the variable meaning requires a numerical value.")
        step1 = self.code_cell(['score = "4.2"', "type(score)"], ["<class 'str'>"], width=4.25, title="1 • INSPECT", execution="[5]", code_size=22)
        step2 = self.code_cell(["score = float(score)", "type(score)"], ["<class 'float'>"], width=4.25, title="2 • CONVERT", execution="[6]", code_size=21)
        step3 = self.code_cell(["score + 0.8", "score >= 3.0"], ["5.0", "True"], width=4.25, title="3 • CALCULATE", execution="[7]", code_size=21)
        steps = VGroup(step1, step2, step3).arrange(RIGHT, buff=0.48).move_to(UP * 0.08); self.fit_content_zone(steps, 13.9, 4.55)
        a1 = self.arrow_between(step1, step2); a2 = self.arrow_between(step2, step3)
        rule = self.note_panel("RULE", ["Check type(value) or df.dtypes before the calculation.", "Convert because of meaning, not just because conversion is possible."], width=10.3, title_size=25, body_size=22); rule.to_edge(DOWN, buff=0.23)
        self.play(FadeIn(step1), run_time=RUN_NORMAL); self.wait(PAUSE_READ)
        self.play(GrowArrow(a1), FadeIn(step2), run_time=RUN_NORMAL); self.wait(PAUSE_READ)
        self.play(GrowArrow(a2), FadeIn(step3), run_time=RUN_NORMAL); self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(rule), run_time=RUN_NORMAL); self.wait(PAUSE_WORK); self.clear_stage()

    def scene_05_dataframe(self) -> None:
        self.set_header(5, "PANDAS DATAFRAME: EACH COLUMN HAS A DTYPE", "A DataFrame stores several variables together. Inspect column dtypes before choosing numerical summaries, counts, filters, or plots.")
        rows = [["Ana", "10A", "4.2", "True"], ["Luis", "10B", "3.8", "True"], ["Sara", "10A", "4.5", "True"], ["Tom", "10B", "3.9", "True"]]
        table = self.build_table(headers=("Student", "Group", "Score", "Passed"), body_rows=rows, column_widths=(2.5, 2.1, 2.1, 2.1), row_height=0.66, header_height=0.74, body_font_size=24, header_font_size=23); table.group.move_to(LEFT * 3.05 + DOWN * 0.02)
        dtype_cell = self.code_cell(["df.dtypes"], ["Student     object", "Group       object", "Score      float64", "Passed        bool"], width=5.0, title="INSPECT COLUMNS", execution="[8]", code_size=22, output_size=19); dtype_cell.move_to(RIGHT * 4.35 + UP * 0.92)
        mean_cell = self.code_cell(['df["Score"].mean()', 'df["Group"].value_counts()'], ["4.1", "10A    2", "10B    2"], width=5.0, title="USE THE RIGHT OPERATION", execution="[9]", code_size=19, output_size=19); mean_cell.move_to(RIGHT * 4.35 + DOWN * 1.55)
        self.animate_table_rows(table, include_header=True, pause=PAUSE_SHORT * 0.65); self.wait(PAUSE_READ)
        self.play(FadeIn(dtype_cell, shift=LEFT * 0.12), run_time=RUN_NORMAL); self.wait(PAUSE_READ)
        self.play(FadeIn(mean_cell, shift=LEFT * 0.12), run_time=RUN_NORMAL); self.wait(PAUSE_WORK); self.clear_stage()

    def scene_06_statistics_mapping(self) -> None:
        self.set_header(6, "PROGRAMMING TYPE AND STATISTICAL TYPE ANSWER DIFFERENT QUESTIONS", "Python describes storage and operations. Statistics describes variable meaning and therefore which summaries or graphs are valid.")
        rows = [["Number of siblings", "int", "Quantitative discrete", "Count / frequency"], ["Height (m)", "float", "Quantitative continuous", "Mean / SD"], ["Blood group", "str / category", "Qualitative nominal", "Frequency"], ["Passed?", "bool", "Binary", "Proportion"], ["Missing score", "None / NaN / pd.NA", "Missing value", "Clean / handle"]]
        table = self.build_table(headers=("Variable meaning", "Stored as", "Statistical type", "Typical use"), body_rows=rows, column_widths=(3.35, 2.85, 4.0, 3.25), row_height=0.70, header_height=0.78, body_font_size=21, header_font_size=21)
        table.group.move_to(DOWN * 0.05); self.fit_content_zone(table.group, 13.95, 5.25)
        self.animate_table_rows(table, include_header=True, pause=PAUSE_SHORT * 0.65); self.wait(PAUSE_WORK); self.clear_stage()

    def scene_07_summary(self) -> None:
        self.set_header(7, "A REPEATABLE COLAB WORKFLOW FOR STATISTICS", "Before calculating a mean, variance, frequency table, graph, or model, move through the same six checks in order.")
        route = self.process_map([("1", "LOAD DATA"), ("2", "READ VALUES"), ("3", "CHECK TYPES"), ("4", "CONVERT / CLEAN"), ("5", "CALCULATE"), ("6", "INTERPRET")], columns=3, card_width=4.45, card_height=1.12)
        route.move_to(UP * 0.10); self.fit(route, 13.8, 4.0)
        final = self.note_panel("THREE COMMANDS TO REMEMBER", ["type(value)  → inspect one Python value", "df.dtypes  → inspect every DataFrame column", "df.head()  → verify what the imported data actually looks like"], width=10.0, title_size=26, body_size=23); final.to_edge(DOWN, buff=0.24)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.10) for card in route], lag_ratio=0.12), run_time=RUN_SLOW * 1.8); self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(final, shift=UP * 0.10), run_time=RUN_NORMAL); self.wait(PAUSE_FINAL)
        self.standard_closing("Correct type → correct operation → valid statistical interpretation.")
