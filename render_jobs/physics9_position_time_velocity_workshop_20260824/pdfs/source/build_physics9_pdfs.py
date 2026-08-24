#!/usr/bin/env python3
"""Build two polished Grade 9 Physics PDF companions with vector graphs."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


OUT = Path("output/pdf")
OUT.mkdir(parents=True, exist_ok=True)

PAGE_W, PAGE_H = letter
MARGIN_X = 0.58 * inch
MARGIN_TOP = 0.62 * inch
MARGIN_BOTTOM = 0.55 * inch
CONTENT_W = PAGE_W - 2 * MARGIN_X

BLACK = colors.HexColor("#111111")
DARK = colors.HexColor("#303030")
MID = colors.HexColor("#777777")
LIGHT = colors.HexColor("#D7D7D7")
PAPER = colors.HexColor("#F4F4F4")
PALE = colors.HexColor("#FAFAFA")


def register_fonts() -> tuple[str, str]:
    candidates = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ("/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf", "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"),
    ]
    for regular, bold in candidates:
        if Path(regular).exists() and Path(bold).exists():
            pdfmetrics.registerFont(TTFont("JPBody", regular))
            pdfmetrics.registerFont(TTFont("JPBodyBold", bold))
            return "JPBody", "JPBodyBold"
    return "Helvetica", "Helvetica-Bold"


BODY_FONT, BOLD_FONT = register_fonts()


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "JPTitle", parent=base["Title"], fontName=BOLD_FONT, fontSize=22,
            leading=26, textColor=BLACK, alignment=TA_CENTER, spaceAfter=10,
        ),
        "subtitle": ParagraphStyle(
            "JPSubtitle", parent=base["Normal"], fontName=BODY_FONT, fontSize=11.5,
            leading=15, textColor=DARK, alignment=TA_CENTER, spaceAfter=12,
        ),
        "h1": ParagraphStyle(
            "JPH1", parent=base["Heading1"], fontName=BOLD_FONT, fontSize=15.5,
            leading=19, textColor=BLACK, spaceBefore=4, spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "JPH2", parent=base["Heading2"], fontName=BOLD_FONT, fontSize=12.5,
            leading=15, textColor=BLACK, spaceBefore=5, spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "JPBodyStyle", parent=base["BodyText"], fontName=BODY_FONT,
            fontSize=9.7, leading=13.2, textColor=BLACK, spaceAfter=5,
        ),
        "small": ParagraphStyle(
            "JPSmall", parent=base["BodyText"], fontName=BODY_FONT,
            fontSize=8.2, leading=10.8, textColor=DARK, spaceAfter=3,
        ),
        "formula": ParagraphStyle(
            "JPFormula", parent=base["BodyText"], fontName=BOLD_FONT,
            fontSize=11.2, leading=15, textColor=BLACK, alignment=TA_CENTER,
            spaceBefore=3, spaceAfter=3,
        ),
        "question": ParagraphStyle(
            "JPQuestion", parent=base["BodyText"], fontName=BODY_FONT,
            fontSize=9.4, leading=12.4, textColor=BLACK, leftIndent=2,
            spaceAfter=4,
        ),
        "center": ParagraphStyle(
            "JPCenter", parent=base["BodyText"], fontName=BODY_FONT,
            fontSize=9.4, leading=12, alignment=TA_CENTER, textColor=BLACK,
        ),
    }


S = styles()


class PositionTimeGraph(Flowable):
    """Vector position-time graph for piecewise points."""

    def __init__(
        self,
        points: Sequence[tuple[float, float]],
        width: float = 6.55 * inch,
        height: float = 2.35 * inch,
        x_max: float | None = None,
        y_min: float | None = None,
        y_max: float | None = None,
        segment_labels: Sequence[str] | None = None,
        title: str = "Position vs. time",
    ):
        super().__init__()
        self.width = width
        self.height = height
        self.points = list(points)
        self.x_max = x_max if x_max is not None else max(x for x, _ in points)
        ys = [y for _, y in points]
        self.y_min = y_min if y_min is not None else min(0, min(ys))
        self.y_max = y_max if y_max is not None else max(ys)
        if self.y_max == self.y_min:
            self.y_max += 1
        self.segment_labels = list(segment_labels or [])
        self.title = title

    def draw(self):
        c = self.canv
        left, bottom = 44, 30
        right, top = self.width - 18, self.height - 25
        plot_w, plot_h = right - left, top - bottom
        x_max = max(self.x_max, 1)
        y_min, y_max = self.y_min, self.y_max

        def xp(x):
            return left + plot_w * x / x_max

        def yp(y):
            return bottom + plot_h * (y - y_min) / (y_max - y_min)

        c.saveState()
        c.setFont(BOLD_FONT, 9)
        c.setFillColor(BLACK)
        c.drawString(left, self.height - 13, self.title)
        c.setStrokeColor(LIGHT)
        c.setLineWidth(0.45)
        for i in range(int(x_max) + 1):
            c.line(xp(i), bottom, xp(i), top)
        y_ticks = 5
        for i in range(y_ticks + 1):
            y = y_min + (y_max - y_min) * i / y_ticks
            c.line(left, yp(y), right, yp(y))
        c.setStrokeColor(BLACK)
        c.setLineWidth(1.15)
        y_zero = yp(0) if y_min <= 0 <= y_max else bottom
        c.line(left, y_zero, right + 5, y_zero)
        c.line(left, bottom - 3, left, top + 5)
        c.setFont(BODY_FONT, 7.2)
        for i in range(int(x_max) + 1):
            c.drawCentredString(xp(i), bottom - 12, str(i))
        for i in range(y_ticks + 1):
            y = y_min + (y_max - y_min) * i / y_ticks
            label = f"{y:g}"
            c.drawRightString(left - 5, yp(y) - 2.5, label)
        c.setFont(BOLD_FONT, 8)
        c.drawString(right - 16, bottom - 22, "t (s)")
        c.drawString(left - 30, top + 6, "x (m)")
        c.setStrokeColor(BLACK)
        c.setLineWidth(2.0)
        path = c.beginPath()
        path.moveTo(xp(self.points[0][0]), yp(self.points[0][1]))
        for x, y in self.points[1:]:
            path.lineTo(xp(x), yp(y))
        c.drawPath(path)
        c.setFillColor(colors.white)
        c.setStrokeColor(BLACK)
        for x, y in self.points:
            c.circle(xp(x), yp(y), 3.0, stroke=1, fill=1)
        c.setFillColor(BLACK)
        c.setFont(BOLD_FONT, 7.2)
        for idx, label in enumerate(self.segment_labels):
            if idx + 1 >= len(self.points):
                break
            x0, y0 = self.points[idx]
            x1, y1 = self.points[idx + 1]
            c.drawCentredString((xp(x0) + xp(x1)) / 2, (yp(y0) + yp(y1)) / 2 + 8, label)
        c.restoreState()


class VelocityTimeGraph(Flowable):
    """Vector step graph defined by (t0, t1, velocity) segments."""

    def __init__(
        self,
        segments: Sequence[tuple[float, float, float]],
        width: float = 6.55 * inch,
        height: float = 2.35 * inch,
        title: str = "Velocity vs. time",
    ):
        super().__init__()
        self.width = width
        self.height = height
        self.segments = list(segments)
        self.title = title

    def draw(self):
        c = self.canv
        left, bottom = 44, 30
        right, top = self.width - 18, self.height - 25
        plot_w, plot_h = right - left, top - bottom
        x_max = max(t1 for _, t1, _ in self.segments)
        vals = [v for _, _, v in self.segments] + [0]
        y_min = min(vals)
        y_max = max(vals)
        padding = max(1, (y_max - y_min) * 0.18)
        y_min -= padding
        y_max += padding

        def xp(x):
            return left + plot_w * x / x_max

        def yp(y):
            return bottom + plot_h * (y - y_min) / (y_max - y_min)

        c.saveState()
        c.setFont(BOLD_FONT, 9)
        c.drawString(left, self.height - 13, self.title)
        c.setStrokeColor(LIGHT)
        c.setLineWidth(0.45)
        for i in range(int(x_max) + 1):
            c.line(xp(i), bottom, xp(i), top)
        c.setStrokeColor(BLACK)
        c.setLineWidth(1.1)
        c.line(left, yp(0), right + 5, yp(0))
        c.line(left, bottom - 3, left, top + 5)
        c.setFont(BODY_FONT, 7.2)
        for i in range(int(x_max) + 1):
            c.drawCentredString(xp(i), yp(0) - 12, str(i))
        c.setFont(BOLD_FONT, 8)
        c.drawString(right - 16, bottom - 22, "t (s)")
        c.drawString(left - 34, top + 6, "v (m/s)")
        for t0, t1, v in self.segments:
            c.setFillColor(PAPER)
            c.setStrokeColor(MID)
            y0, yv = yp(0), yp(v)
            c.rect(xp(t0), min(y0, yv), xp(t1) - xp(t0), abs(yv - y0), stroke=1, fill=1)
            c.setStrokeColor(BLACK)
            c.setLineWidth(2.0)
            c.line(xp(t0), yv, xp(t1), yv)
            c.setFillColor(BLACK)
            c.setFont(BOLD_FONT, 7.2)
            c.drawCentredString((xp(t0) + xp(t1)) / 2, yv + (7 if v >= 0 else -12), f"{v:g} m/s")
        c.restoreState()


class WorkspaceBox(Flowable):
    def __init__(self, lines=5, height=1.0 * inch, label="Calculation workspace"):
        super().__init__()
        self.width = CONTENT_W
        self.height = height
        self.lines = lines
        self.label = label

    def draw(self):
        c = self.canv
        c.saveState()
        c.setStrokeColor(LIGHT)
        c.setLineWidth(0.6)
        c.setFont(BODY_FONT, 7.5)
        c.setFillColor(MID)
        c.drawString(0, self.height - 9, self.label)
        usable = self.height - 16
        for i in range(self.lines):
            y = usable * (self.lines - i - 1) / max(self.lines, 1)
            c.line(0, y, self.width, y)
        c.restoreState()


def section_badge(number: str, title: str):
    data = [[Paragraph(number, S["center"]), Paragraph(title, S["h1"])]]
    table = Table(data, colWidths=[0.42 * inch, CONTENT_W - 0.42 * inch])
    table.setStyle(TableStyle([
        ("BOX", (0, 0), (0, 0), 1.2, BLACK),
        ("BACKGROUND", (0, 0), (0, 0), PAPER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (1, 0), (1, 0), 8),
        ("RIGHTPADDING", (1, 0), (1, 0), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return table


def formula_box(text: str):
    t = Table([[Paragraph(text, S["formula"])]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1.0, BLACK),
        ("BACKGROUND", (0, 0), (-1, -1), PAPER),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def info_cards(items: Sequence[tuple[str, str]], columns=3):
    cells = []
    for title, body in items:
        cells.append(Paragraph(f"<b>{title}</b><br/>{body}", S["small"]))
    while len(cells) % columns:
        cells.append(Paragraph("", S["small"]))
    rows = [cells[i:i + columns] for i in range(0, len(cells), columns)]
    table = Table(rows, colWidths=[CONTENT_W / columns] * columns, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.8, MID),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, LIGHT),
        ("BACKGROUND", (0, 0), (-1, -1), PALE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LIGHT)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_X, PAGE_H - 0.38 * inch, PAGE_W - MARGIN_X, PAGE_H - 0.38 * inch)
    canvas.setFont(BODY_FONT, 7.5)
    canvas.setFillColor(MID)
    canvas.drawString(MARGIN_X, 0.30 * inch, "Instituto Jorge Robledo - Physics 9 - Third Period 2026")
    canvas.drawRightString(PAGE_W - MARGIN_X, 0.30 * inch, f"Page {doc.page}")
    canvas.restoreState()


def doc_template(path: Path, title: str):
    doc = BaseDocTemplate(
        str(path), pagesize=letter,
        leftMargin=MARGIN_X, rightMargin=MARGIN_X,
        topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM,
        title=title, author="Juan Diego Perez Alvarez",
        subject="Grade 9 Physics classroom workshop",
    )
    frame = Frame(
        MARGIN_X, MARGIN_BOTTOM, CONTENT_W,
        PAGE_H - MARGIN_TOP - MARGIN_BOTTOM,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    doc.addPageTemplates(PageTemplate(id="main", frames=[frame], onPage=header_footer))
    return doc


def cover(story, title, subtitle, promise):
    story.extend([
        Spacer(1, 0.75 * inch),
        Paragraph("PHYSICS 9 - THIRD PERIOD", S["center"]),
        Spacer(1, 0.16 * inch),
        Paragraph(title, S["title"]),
        Paragraph(subtitle, S["subtitle"]),
        Spacer(1, 0.16 * inch),
        formula_box(promise),
        Spacer(1, 0.32 * inch),
        info_cards([
            ("READ", "Identify two points and their units."),
            ("CALCULATE", "Use change in position divided by change in time."),
            ("INTERPRET", "Connect sign and steepness with physical motion."),
        ]),
        Spacer(1, 0.30 * inch),
        Paragraph("Student: ____________________________________   Group: __________   Date: __________", S["body"]),
        PageBreak(),
    ])


def worked_example(story, number, title, points, explanation, equations, labels=None, v_segments=None):
    block = [
        section_badge(str(number), title),
        Spacer(1, 4),
        Paragraph(explanation, S["body"]),
        PositionTimeGraph(points, segment_labels=labels or []),
    ]
    for eq in equations:
        block.append(Paragraph(eq, S["formula"]))
    if v_segments:
        block.append(VelocityTimeGraph(v_segments, title="Matching velocity-time graph"))
    block.append(Spacer(1, 7))
    story.append(KeepTogether(block))


def build_position_workshop(path: Path):
    story = []
    cover(
        story,
        "POSITION-TIME GRAPHS: VELOCITY WORKSHOP",
        "Worked examples, graph interpretation and independent practice",
        "average velocity = change in position / change in time",
    )
    story.extend([
        section_badge("01", "THE SLOPE RECIPE"),
        Spacer(1, 6),
        Paragraph("For a straight segment on an x-t graph, velocity is the slope. Always read coordinates before substituting values.", S["body"]),
        formula_box("v_avg = (x2 - x1) / (t2 - t1) = Dx / Dt"),
        Spacer(1, 8),
        info_cards([
            ("1. Choose points", "Use two clear points on the same straight segment."),
            ("2. Write coordinates", "P1=(t1,x1) and P2=(t2,x2)."),
            ("3. Find changes", "Dx=x2-x1 and Dt=t2-t1."),
            ("4. Divide", "Velocity is Dx/Dt."),
            ("5. Keep the sign", "Positive, zero or negative tells direction."),
            ("6. Check units", "metres divided by seconds gives m/s."),
        ], columns=2),
        Spacer(1, 10),
        PositionTimeGraph([(0, 0), (1, 3), (2, 6), (3, 9)], segment_labels=["same slope", "same slope", "same slope"]),
        Paragraph("A straight line has constant slope, so it represents constant velocity.", S["formula"]),
        PageBreak(),
    ])

    worked_example(
        story, "02", "WORKED EXAMPLE A - POSITIVE VELOCITY",
        [(1, 2), (5, 14)],
        "The object moves from 2 m at 1 s to 14 m at 5 s. The line rises from left to right.",
        ["P1=(1 s, 2 m), P2=(5 s, 14 m)", "Dx=14-2=12 m; Dt=5-1=4 s", "v=12/4=+3 m/s"],
        labels=["+3 m/s"],
    )
    worked_example(
        story, "03", "WORKED EXAMPLE B - REST",
        [(0, 6), (4, 6)],
        "The position stays at 6 m while time passes. A horizontal x-t segment means the object is at rest.",
        ["Dx=6-6=0 m", "v=0/4=0 m/s"],
        labels=["rest"],
    )
    worked_example(
        story, "04", "WORKED EXAMPLE C - NEGATIVE VELOCITY",
        [(1, 12), (5, 4)],
        "The position decreases. The negative slope means the object moves in the negative direction.",
        ["Dx=4-12=-8 m; Dt=5-1=4 s", "v=-8/4=-2 m/s"],
        labels=["-2 m/s"],
    )
    story.append(PageBreak())

    worked_example(
        story, "05", "WORKED EXAMPLE D - COMPARE SPEEDS",
        [(0, 0), (2, 10)],
        "Object A changes 10 m in 2 s, so its slope is 5 m/s. Object B changes 6 m in the same 2 s, so its slope is 3 m/s. The steeper line represents the greater speed.",
        ["v_A=10/2=5 m/s", "v_B=6/2=3 m/s", "Therefore, A is faster."],
        labels=["A: steeper"],
    )
    story.extend([
        PositionTimeGraph([(0, 0), (2, 6)], segment_labels=["B: less steep"], title="Object B position-time graph"),
        Spacer(1, 6),
    ])
    worked_example(
        story, "06", "WORKED EXAMPLE E - PIECEWISE MOTION",
        [(0, 0), (2, 8), (5, 8), (7, 2)],
        "Calculate one slope per segment. Then draw a horizontal velocity level over the same time interval.",
        ["0-2 s: v1=(8-0)/(2-0)=4 m/s", "2-5 s: v2=(8-8)/(5-2)=0 m/s", "5-7 s: v3=(2-8)/(7-5)=-3 m/s"],
        labels=["+4", "0", "-3"],
        v_segments=[(0, 2, 4), (2, 5, 0), (5, 7, -3)],
    )
    story.append(PageBreak())

    story.extend([
        section_badge("07", "WORKSHOP - CALCULATE EACH VELOCITY"),
        Spacer(1, 5),
        Paragraph("Show coordinates, Dx, Dt, velocity and units. Do not use only visual guessing.", S["body"]),
        PositionTimeGraph([(0, 1), (3, 10)], title="Problem 1"),
        Paragraph("1. Calculate the velocity from 0 s to 3 s. State its sign and physical meaning.", S["question"]),
        WorkspaceBox(lines=3, height=0.62 * inch),
        PositionTimeGraph([(1, 9), (5, 1)], title="Problem 2"),
        Paragraph("2. Calculate the velocity. Is the object moving in the positive or negative direction?", S["question"]),
        WorkspaceBox(lines=3, height=0.62 * inch),
        PageBreak(),
        section_badge("08", "WORKSHOP - READ AND COMPARE"),
        Spacer(1, 5),
        PositionTimeGraph([(0, 4), (4, 4)], title="Problem 3"),
        Paragraph("3. Calculate the velocity and explain what a horizontal line means.", S["question"]),
        WorkspaceBox(lines=3, height=0.60 * inch),
        PositionTimeGraph([(0, 0), (2, 12)], title="Problem 4 - Object A"),
        PositionTimeGraph([(0, 0), (3, 12)], title="Problem 4 - Object B"),
        Paragraph("4. Calculate both velocities. Which object is faster? Explain using slope.", S["question"]),
        WorkspaceBox(lines=3, height=0.60 * inch),
        PageBreak(),
        section_badge("09", "WORKSHOP - FROM x-t TO v-t"),
        Spacer(1, 5),
        PositionTimeGraph([(0, 2), (2, 8), (4, 8), (6, 0)], segment_labels=["I", "II", "III"], title="Problem 5 - piecewise position"),
        Paragraph("5a. Calculate the velocity on segments I, II and III.<br/>5b. Draw the matching velocity-time graph.<br/>5c. During which interval is the object at rest?<br/>5d. During which interval does it move backward?", S["question"]),
        WorkspaceBox(lines=7, height=1.35 * inch),
        VelocityTimeGraph([(0, 2, 0), (2, 4, 0), (4, 6, 0)], title="Blank velocity-time axes - replace each level"),
        PageBreak(),
        section_badge("10", "CHALLENGE - WHOLE-TRIP AVERAGE VELOCITY"),
        Spacer(1, 5),
        PositionTimeGraph([(0, 0), (2, 8), (5, 8), (7, 2)], title="Problem 6"),
        Paragraph("6a. Calculate the average velocity for the whole trip using only the first and final points.<br/>6b. Compare it with the three segment velocities.<br/>6c. Explain why average velocity is not the arithmetic mean of the three slopes when the time intervals are different.", S["question"]),
        WorkspaceBox(lines=8, height=1.55 * inch),
        formula_box("Whole-trip average velocity uses total displacement / total time."),
        PageBreak(),
    ])

    story.extend([
        section_badge("11", "ANSWER KEY"),
        Spacer(1, 6),
        Paragraph("Problem 1: v=(10-1)/(3-0)=9/3=+3 m/s. Position increases.", S["body"]),
        Paragraph("Problem 2: v=(1-9)/(5-1)=-8/4=-2 m/s. The object moves in the negative direction.", S["body"]),
        Paragraph("Problem 3: v=(4-4)/(4-0)=0 m/s. The object remains at x=4 m.", S["body"]),
        Paragraph("Problem 4: v_A=12/2=6 m/s; v_B=12/3=4 m/s. A is faster and has the steeper line.", S["body"]),
        Paragraph("Problem 5: segment I=(8-2)/2=3 m/s; segment II=0 m/s; segment III=(0-8)/2=-4 m/s. Rest occurs from 2 to 4 s. Backward motion occurs from 4 to 6 s.", S["body"]),
        VelocityTimeGraph([(0, 2, 3), (2, 4, 0), (4, 6, -4)], title="Problem 5 - correct velocity-time graph"),
        Paragraph("Problem 6: whole-trip average velocity=(2-0)/(7-0)=2/7 m/s, approximately 0.286 m/s. Segment velocities are 4 m/s, 0 m/s and -3 m/s. Their intervals last 2 s, 3 s and 2 s, so an unweighted arithmetic mean does not represent the whole trip.", S["body"]),
        Spacer(1, 8),
        formula_box("Final check: positive slope -> positive v; horizontal -> zero v; negative slope -> negative v."),
    ])

    doc_template(path, "Physics 9 Position-Time Velocity Workshop").build(story)


def build_previous_companion(path: Path):
    story = []
    cover(
        story,
        "VELOCITY-TIME GRAPHS AND DISPLACEMENT",
        "PDF companion to the previous rendered presentation",
        "signed area under a velocity-time graph = displacement",
    )
    story.extend([
        section_badge("01", "FROM x-t SLOPE TO v-t HEIGHT"),
        Spacer(1, 6),
        Paragraph("An x-t graph encodes position. Its slope gives velocity. A v-t graph encodes that velocity directly as vertical height.", S["body"]),
        info_cards([
            ("x-t vertical value", "position x in metres"),
            ("x-t slope", "velocity in metres per second"),
            ("v-t vertical value", "velocity in metres per second"),
            ("v-t signed area", "displacement in metres"),
        ], columns=2),
        Spacer(1, 8),
        PositionTimeGraph([(0, 0), (4, 12)], segment_labels=["slope = 3 m/s"]),
        VelocityTimeGraph([(0, 4, 3)]),
        formula_box("Dx = area = base x height = Dt x v"),
        PageBreak(),
        section_badge("02", "THE ACHILLES MEETING RECONCILED"),
        Spacer(1, 6),
        Paragraph("Achilles has v_A=10 m/s. The tortoise has v_T=1 m/s and starts 10 m ahead. Their catch time is 10/9 s.", S["body"]),
        formula_box("t* = 10/9 s; x* = 100/9 m"),
        VelocityTimeGraph([(0, 10/9, 10)], title="Achilles - displacement area"),
        Paragraph("Achilles: Dx_A=(10 m/s)(10/9 s)=100/9 m.", S["formula"]),
        VelocityTimeGraph([(0, 10/9, 1)], title="Tortoise - displacement area"),
        Paragraph("Tortoise: Dx_T=(1 m/s)(10/9 s)=10/9 m; x_T=10+10/9=100/9 m.", S["formula"]),
        PageBreak(),
        section_badge("03", "PIECEWISE AREA RECIPE"),
        Spacer(1, 6),
        info_cards([
            ("1. Read axes", "Confirm seconds and m/s."),
            ("2. Split the region", "Use one rectangle or triangle per interval."),
            ("3. Find each area", "Base x height for rectangles."),
            ("4. Apply sign", "Above axis positive; below axis negative."),
            ("5. Add", "The signed total is displacement."),
            ("6. Check unit", "(s)(m/s)=m."),
        ], columns=2),
        VelocityTimeGraph([(0, 2, 4), (2, 5, 2)], title="Worked example"),
        Paragraph("A1=(2 s)(4 m/s)=8 m", S["formula"]),
        Paragraph("A2=(3 s)(2 m/s)=6 m", S["formula"]),
        formula_box("Total displacement = 8 m + 6 m = 14 m"),
        PageBreak(),
        section_badge("04", "DISPLACEMENT VS. DISTANCE"),
        Spacer(1, 6),
        VelocityTimeGraph([(0, 3, 2), (3, 5, -1)], title="Motion with a direction change"),
        Paragraph("Positive area: +6 m. Negative area: -2 m.", S["body"]),
        formula_box("Displacement = 6-2 = 4 m"),
        Spacer(1, 6),
        formula_box("Distance travelled = 6+2 = 8 m"),
        Spacer(1, 10),
        Paragraph("Displacement keeps direction through the signs. Distance counts the size of every travelled part.", S["body"]),
        PageBreak(),
        section_badge("05", "PRACTICE"),
        Spacer(1, 5),
        VelocityTimeGraph([(0, 4, 3)], title="Practice 1"),
        Paragraph("1. Find the displacement and explain why the final unit is metres.", S["question"]),
        WorkspaceBox(lines=3, height=0.62 * inch),
        VelocityTimeGraph([(0, 2, 5), (2, 5, 1)], title="Practice 2"),
        Paragraph("2. Split the region and calculate total displacement.", S["question"]),
        WorkspaceBox(lines=3, height=0.62 * inch),
        PageBreak(),
        section_badge("06", "PRACTICE WITH NEGATIVE VELOCITY"),
        Spacer(1, 5),
        VelocityTimeGraph([(0, 3, 4), (3, 5, -2)], title="Practice 3"),
        Paragraph("3a. Calculate displacement.<br/>3b. Calculate distance travelled.<br/>3c. Explain why the answers differ.", S["question"]),
        WorkspaceBox(lines=6, height=1.15 * inch),
        VelocityTimeGraph([(0, 2, -3), (2, 6, 2)], title="Practice 4"),
        Paragraph("4. Calculate the signed displacement. In which interval does the object move backward?", S["question"]),
        WorkspaceBox(lines=5, height=0.95 * inch),
        PageBreak(),
        section_badge("07", "ANSWER KEY"),
        Spacer(1, 6),
        Paragraph("Practice 1: Dx=(4 s)(3 m/s)=12 m. Seconds cancel, leaving metres.", S["body"]),
        Paragraph("Practice 2: Dx=(2)(5)+(3)(1)=10+3=13 m.", S["body"]),
        Paragraph("Practice 3: displacement=(3)(4)+(2)(-2)=12-4=8 m. Distance=12+4=16 m.", S["body"]),
        Paragraph("Practice 4: displacement=(2)(-3)+(4)(2)=-6+8=2 m. Backward motion occurs from 0 to 2 s.", S["body"]),
        Spacer(1, 10),
        formula_box("Height tells velocity. Signed area tells displacement."),
    ])
    doc_template(path, "Physics 9 Velocity-Time Displacement Companion").build(story)


if __name__ == "__main__":
    build_position_workshop(OUT / "Physics9_Position_Time_Velocity_Workshop.pdf")
    build_previous_companion(OUT / "Physics9_Velocity_Time_Displacement_Companion.pdf")
    print(OUT / "Physics9_Position_Time_Velocity_Workshop.pdf")
    print(OUT / "Physics9_Velocity_Time_Displacement_Companion.pdf")
