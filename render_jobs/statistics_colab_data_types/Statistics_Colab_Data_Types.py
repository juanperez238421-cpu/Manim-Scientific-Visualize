#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Statistics class — Data Types in Google Colab.

ManimCE 0.20.x classroom presentation.
Visual architecture follows jp_classroom_style.py:
white background, black typography, numbered headers, safe margins,
progressive code construction, custom tables, and reproducible summary.

Render:
    manim -pql Statistics_Colab_Data_Types.py StatisticsColabDataTypes --disable_caching
    manim -pqh Statistics_Colab_Data_Types.py StatisticsColabDataTypes --disable_caching
"""

from __future__ import annotations

from jp_classroom_style import *


class StatisticsColabDataTypes(JPMathClassroomScene):
    """Introductory statistics lesson connecting Python/Colab types to data analysis."""

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

    def construct(self) -> None:
        self.opening()
        self.scene_01_why_types_matter()
        self.scene_02_scalar_types()
        self.scene_03_collections()
        self.scene_04_inspect_and_convert()
        self.scene_05_dataframe()
        self.scene_06_statistics_mapping()
        self.scene_07_summary()

    def code_cell(
        self,
        code_lines,
        output_lines=None,
        *,
        width=6.5,
        title="COLAB CELL",
        code_size=22,
        output_size=21,
    ):
        output_lines = output_lines or []

        title_mob = self.text(title, 19, BOLD)
        play_icon = Triangle(
            stroke_color=BLACK_LINE,
            stroke_width=1.5,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1,
        ).scale(0.13).rotate(-PI / 2)
        title_row = VGroup(play_icon, title_mob).arrange(RIGHT, buff=0.12)

        code = VGroup(*[
            self.text(line, code_size, font="DejaVu Sans Mono")
            for line in code_lines
        ])
        code.arrange(DOWN, aligned_edge=LEFT, buff=0.10)

        chunks = [title_row, code]
        if output_lines:
            divider = Line(LEFT, RIGHT, color=LIGHT_GRAY, stroke_width=1.2)
            divider.set_width(width - 0.55)
            output = VGroup(*[
                self.text(line, output_size, font="DejaVu Sans Mono")
                for line in output_lines
            ])
            output.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            chunks.extend([divider, output])

        content = VGroup(*chunks).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        self.fit(content, width - 0.52, 4.8)

        box = RoundedRectangle(
            width=width,
            height=max(1.15, content.height + 0.50),
            corner_radius=0.10,
            stroke_color=BLACK_LINE,
            stroke_width=1.6,
            fill_color=WHITE_FILL,
            fill_opacity=1,
        )
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.26)
        return VGroup(box, content)

    def type_card(self, label, example, meaning, *, width=3.25):
        type_name = self.text(label, 27, BOLD)
        example_mob = self.text(example, 22, font="DejaVu Sans Mono")
        meaning_mob = self.text(meaning, 19)
        self.fit(meaning_mob, width - 0.35, 0.75)
        content = VGroup(type_name, example_mob, meaning_mob)
        content.arrange(DOWN, buff=0.14)

        box = RoundedRectangle(
            width=width,
            height=1.75,
            corner_radius=0.10,
            stroke_color=BLACK_LINE,
            stroke_width=1.5,
            fill_color=WHITE_FILL,
            fill_opacity=1,
        )
        content.move_to(box)
        return VGroup(box, content)

    def opening(self) -> None:
        self.standard_opening(
            "STATISTICS • GOOGLE COLAB",
            "DATA TYPES",
            "How Colab stores values before we calculate with them",
            "Inspect first. Convert when needed. Then calculate and interpret.",
        )

    def scene_01_why_types_matter(self) -> None:
        self.set_header(
            1,
            "WHY DOES THE DATA TYPE MATTER?",
            "Two values can look similar on screen but behave very differently when Python performs an operation.",
        )

        numeric = self.code_cell(
            ["a = 10", "b = 5", "a + b"],
            ["15"],
            width=6.2,
            title="NUMBERS",
        )
        text = self.code_cell(
            ['a = "10"', 'b = "5"', "a + b"],
            ['"105"'],
            width=6.2,
            title="TEXT",
        )
        VGroup(numeric, text).arrange(RIGHT, buff=0.55).move_to(DOWN * 0.25)

        takeaway = self.note_panel(
            "KEY IDEA",
            [
                "The stored type controls what operations are valid.",
                "Before statistics, check what each column actually contains.",
            ],
            width=9.0,
            title_size=25,
            body_size=22,
        )
        takeaway.to_edge(DOWN, buff=0.25)

        self.play(FadeIn(numeric, shift=UP * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(text, shift=UP * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(takeaway), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def scene_02_scalar_types(self) -> None:
        self.set_header(
            2,
            "THE FIVE SCALAR TYPES YOU WILL SEE FIRST",
            "A scalar is one stored value. In statistics, each scalar may represent a count, measurement, label, condition, or missing value.",
        )

        cards = VGroup(
            self.type_card("int", "students = 28", "Whole-number count"),
            self.type_card("float", "mean = 4.25", "Decimal measurement"),
            self.type_card("str", 'group = "10A"', "Text or category label"),
            self.type_card("bool", "passed = True", "True / False condition"),
            self.type_card("None", "missing = None", "No value stored"),
        )
        cards.arrange_in_grid(cols=3, buff=(0.30, 0.34))
        cards.move_to(DOWN * 0.30)
        self.fit_content_zone(cards, 13.5, 4.8)

        for card in cards:
            self.play(FadeIn(card, shift=UP * 0.10), run_time=RUN_QUICK)
            self.wait(PAUSE_SHORT)

        warning = self.text(
            "Python type is not exactly the same thing as statistical variable type.",
            24,
            BOLD,
        )
        warning.to_edge(DOWN, buff=0.30)
        self.play(Write(warning), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def scene_03_collections(self) -> None:
        self.set_header(
            3,
            "COLLECTIONS STORE MORE THAN ONE VALUE",
            "Statistics usually begins with a group of observations, so lists and dictionaries are natural bridges toward pandas tables.",
        )

        list_cell = self.code_cell(
            ["scores = [4.2, 3.8, 4.5, 3.9]", "len(scores)", "sum(scores) / len(scores)"],
            ["4", "4.1"],
            width=7.0,
            title="LIST",
        )
        dict_cell = self.code_cell(
            ['student = {', '    "name": "Ana",', '    "score": 4.2,', '    "passed": True', '}', 'student["score"]'],
            ["4.2"],
            width=6.4,
            title="DICTIONARY",
            code_size=20,
        )
        pair = VGroup(list_cell, dict_cell).arrange(RIGHT, buff=0.45).move_to(DOWN * 0.25)
        self.fit_content_zone(pair, 14.2, 5.3)

        self.play(FadeIn(list_cell), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(dict_cell), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def scene_04_inspect_and_convert(self) -> None:
        self.set_header(
            4,
            "INSPECT FIRST: type() — THEN CONVERT IF NECESSARY",
            "A common Colab error is importing numbers as text. Conversion makes the intended mathematical operation explicit.",
        )

        inspect_cell = self.code_cell(
            ['score = "4.2"', "type(score)", "score = float(score)", "type(score)"],
            ["<class 'str'>", "<class 'float'>"],
            width=6.5,
            title="INSPECT + CONVERT",
        )

        conversion = self.code_cell(
            ['int("28")', 'float("4.2")', "str(28)", "bool(1)"],
            ["28", "4.2", "'28'", "True"],
            width=5.8,
            title="COMMON CONVERSIONS",
        )

        pair = VGroup(inspect_cell, conversion).arrange(RIGHT, buff=0.55).move_to(DOWN * 0.15)
        self.fit_content_zone(pair, 13.8, 5.0)
        self.play(FadeIn(inspect_cell), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(conversion), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)

        rule = self.formula_panel(
            r"\text{inspect} \rightarrow \text{convert} \rightarrow \text{calculate}",
            width=8.0,
            height=0.95,
            font_size=34,
        )
        rule.to_edge(DOWN, buff=0.28)
        self.play(FadeIn(rule), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def scene_05_dataframe(self) -> None:
        self.set_header(
            5,
            "PANDAS: A DATAFRAME COMBINES MULTIPLE COLUMN TYPES",
            "Each column has a dtype. Numerical columns can be summarized; categorical columns are usually counted, grouped, or filtered.",
        )

        rows = [
            ["Ana", "10A", "4.2", "True"],
            ["Luis", "10B", "3.8", "True"],
            ["Sara", "10A", "4.5", "True"],
            ["Tom", "10B", "3.9", "True"],
        ]
        table = self.build_table(
            headers=("Student", "Group", "Score", "Passed"),
            body_rows=rows,
            column_widths=(2.5, 2.1, 2.1, 2.1),
            row_height=0.62,
            header_height=0.72,
            body_font_size=23,
            header_font_size=22,
        )
        table.group.move_to(LEFT * 3.0 + DOWN * 0.15)

        dtype_cell = self.code_cell(
            ["df.dtypes"],
            [
                "Student     object",
                "Group       object",
                "Score      float64",
                "Passed        bool",
            ],
            width=5.0,
            title="COLUMN DTYPES",
            code_size=21,
            output_size=19,
        )
        dtype_cell.move_to(RIGHT * 4.35 + UP * 0.75)

        mean_cell = self.code_cell(
            ['df["Score"].mean()', 'df["Group"].value_counts()'],
            ["4.1", "10A    2", "10B    2"],
            width=5.0,
            title="STATISTICAL OPERATIONS",
            code_size=19,
            output_size=19,
        )
        mean_cell.move_to(RIGHT * 4.35 + DOWN * 1.65)

        self.animate_table_rows(table, include_header=True)
        self.play(FadeIn(dtype_cell), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(mean_cell), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def scene_06_statistics_mapping(self) -> None:
        self.set_header(
            6,
            "PYTHON TYPE ≠ STATISTICAL VARIABLE TYPE",
            "Programming types describe storage and operations; statistical types describe the meaning of the variable and which analyses are appropriate.",
        )

        rows = [
            ["Number of siblings", "int", "Quantitative discrete", "Count"],
            ["Height (m)", "float", "Quantitative continuous", "Mean / SD"],
            ["Blood group", "str/category", "Qualitative nominal", "Frequency"],
            ["Passed?", "bool", "Binary", "Proportion"],
            ["Missing score", "None / NaN", "Missing", "Clean / impute"],
        ]
        table = self.build_table(
            headers=("Variable", "Python", "Statistics", "Typical use"),
            body_rows=rows,
            column_widths=(3.4, 2.5, 4.0, 3.0),
            row_height=0.66,
            header_height=0.76,
            body_font_size=21,
            header_font_size=21,
        )
        table.group.move_to(DOWN * 0.15)
        self.fit_content_zone(table.group, 13.9, 5.2)
        self.animate_table_rows(table, include_header=True)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def scene_07_summary(self) -> None:
        self.set_header(
            7,
            "A SIMPLE WORKFLOW FOR EVERY NEW DATASET",
            "Use the same sequence before calculating a mean, variance, frequency table, graph, or statistical model.",
        )

        route = self.process_map(
            [
                ("1", "LOAD DATA"),
                ("2", "READ VALUES"),
                ("3", "CHECK TYPES"),
                ("4", "CONVERT / CLEAN"),
                ("5", "CALCULATE"),
                ("6", "INTERPRET"),
            ],
            columns=3,
        )
        route.move_to(DOWN * 0.15)
        self.fit(route, 13.7, 4.8)

        final = self.note_panel(
            "COLAB CHECKLIST",
            [
                "type(variable) for one value",
                "df.dtypes for every DataFrame column",
                "Convert only when the meaning of the variable requires it",
            ],
            width=8.8,
            title_size=25,
            body_size=22,
        )
        final.to_edge(DOWN, buff=0.25)

        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.10) for card in route], lag_ratio=0.10),
            run_time=RUN_SLOW * 1.7,
        )
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(final), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.standard_closing(
            "Correct data types make correct statistical calculations possible."
        )
