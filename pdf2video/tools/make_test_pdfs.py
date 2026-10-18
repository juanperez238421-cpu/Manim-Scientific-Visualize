"""Generate realistic test worksheets (English) for the four topics, plus a scanned (image-only) copy.

usage: python tools/make_test_pdfs.py examples/
"""
import sys
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "examples")
W, H = letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
_D = "/usr/share/fonts/truetype/dejavu/"
for nm, f in (("Serif", "DejaVuSerif.ttf"), ("Serif-Bold", "DejaVuSerif-Bold.ttf"), ("Serif-Italic", "DejaVuSerif-Italic.ttf"), ("Serif-BoldItalic", "DejaVuSerif-BoldItalic.ttf")):
    pdfmetrics.registerFont(TTFont(nm, _D + f))
addMapping("Serif", 0, 0, "Serif"); addMapping("Serif", 1, 0, "Serif-Bold"); addMapping("Serif", 0, 1, "Serif-Italic"); addMapping("Serif", 1, 1, "Serif-BoldItalic")
BODY = ParagraphStyle("b", fontName="Serif", fontSize=11, leading=16)


def header(c, school, course, title, instructions):
    c.setFont("Helvetica-Bold", 10); c.drawString(54, H - 50, school)
    c.setFont("Helvetica", 10); c.drawRightString(W - 54, H - 50, course)
    c.setLineWidth(0.8); c.line(54, H - 58, W - 54, H - 58)
    c.setFont("Helvetica-Bold", 16); c.drawString(54, H - 84, title)
    c.setFont("Helvetica", 10)
    c.drawString(54, H - 104, "Name: ______________________________")
    c.drawRightString(W - 54, H - 104, "Date: ______________   Score: ______ / 30")
    p = Paragraph("<i>" + instructions + "</i>", ParagraphStyle("i", parent=BODY, fontSize=10.5, leading=14))
    w, h = p.wrap(W - 108, 100); p.drawOn(c, 54, H - 116 - h)
    return H - 130 - h


def problem(c, y, n, html, work=96, pts=10, inside=None):
    c.setFont("Serif-Bold", 11); c.drawString(54, y - 13, f"{n}.")
    p = Paragraph(html, BODY)
    w, h = p.wrap(W - 190, 300); p.drawOn(c, 74, y - h)
    c.setFont("Helvetica", 9); c.drawRightString(W - 54, y - 12, f"({pts} pts)")
    y2 = y - h - 12
    c.setStrokeGray(0.75); c.setDash(2, 3); c.rect(74, y2 - work, W - 128, work); c.setDash(); c.setStrokeGray(0)
    if inside:
        inside(c, 74, y2, W - 128, work)
    return y2 - work - 18


def footer(c, txt):
    c.setFont("Helvetica", 8.5); c.setFillGray(0.4); c.drawCentredString(W / 2, 32, txt); c.setFillGray(0)


def physics(path):
    c = canvas.Canvas(str(path), pagesize=letter)
    y = header(c, "Riverside High School", "Physics 9 · Unit 2: Kinematics", "Worksheet 2.3 — Motion in One Dimension",
               "Show all your work. Use g = 9.8 m/s² and ignore air resistance. Round final answers to two decimal places where needed.")
    y = problem(c, y, 1, "A car starts from rest and accelerates uniformly at <b>2.5 m/s²</b> along a straight road. "
                "(a) How long does it take to reach a speed of <b>20 m/s</b>? (b) How far does it travel in that time?", 110)
    y = problem(c, y, 2, "A stone is dropped from the top of a building <b>45 m</b> tall. (a) How long does it take to hit the ground? "
                "(b) What is its speed just before impact?", 110)
    y = problem(c, y, 3, "Two cyclists start <b>600 m</b> apart and ride toward each other along a straight path. Cyclist A rides at "
                "<b>5 m/s</b> and cyclist B rides at <b>7 m/s</b>. When and where do they meet? Measure the position from A's starting point.", 110)
    footer(c, "Physics 9 — Worksheet 2.3 — page 1 of 1"); c.save()


def algebra(path):
    c = canvas.Canvas(str(path), pagesize=letter)
    y = header(c, "Lincoln Middle School", "Algebra I · Chapter 5", "Practice Set 5B — Equations and Linear Functions",
               "Solve each problem. Show every step. Check your solutions by substitution.")
    y = problem(c, y, 1, "Solve the system of equations:<br/>&nbsp;&nbsp;&nbsp;&nbsp;2x + 3y = 12<br/>&nbsp;&nbsp;&nbsp;&nbsp;x − y = 1", 105)
    y = problem(c, y, 2, "Solve the quadratic equation x² − 5x + 6 = 0 by factoring.", 105)
    y = problem(c, y, 3, "A line passes through the points (1, 3) and (4, 9). Find its slope and write its equation in the form y = mx + b.", 105)
    footer(c, "Algebra I — Practice Set 5B"); c.save()


def statistics(path):
    c = canvas.Canvas(str(path), pagesize=letter)
    y = header(c, "Westfield Academy", "Statistics 10 · Unit 1", "Worksheet 1.4 — Describing Data",
               "Use the data given in each problem. Round to two decimal places. For quartiles, use the median of each half.")
    def table(c, x, ytop, w, h):
        xs = [7, 9, 6, 8, 10, 7, 5, 9, 7]
        tx, ty, cw, rh = x + 70, ytop - 14, 40, 20
        c.setFont("Helvetica-Bold", 10); c.drawString(x + 12, ty - 14, "Student"); c.drawString(x + 12, ty - 14 - rh, "Score")
        c.setFont("Helvetica", 10)
        for i, v in enumerate(xs):
            c.rect(tx + i * cw, ty - rh, cw, rh); c.rect(tx + i * cw, ty - 2 * rh, cw, rh)
            c.drawCentredString(tx + i * cw + cw / 2, ty - 14, chr(65 + i)); c.drawCentredString(tx + i * cw + cw / 2, ty - 14 - rh, str(v))
    y = problem(c, y, 1, "The quiz scores of nine students are listed in the table below. Find the mean, the median, the mode and the range.", 140, inside=table)
    y = problem(c, y, 2, "The daily high temperatures for one week of school were 18, 20, 22, 24 and 26 °C. Find the mean and the population standard deviation.", 100)
    y = problem(c, y, 3, "For the data set 3, 5, 7, 8, 9, 11, 13, 15 find the first quartile, the median, the third quartile and the interquartile range.", 100)
    footer(c, "Statistics 10 — Worksheet 1.4"); c.save()


def chem_geo(path):
    c = canvas.Canvas(str(path), pagesize=letter)
    y = header(c, "Oak Valley High School", "Science & Math Review", "Review Sheet — Stoichiometry and Geometry",
               "Show your reasoning. Molar masses: H = 1.0 g/mol, O = 16.0 g/mol. Use the exact value of π.")
    y = problem(c, y, 1, "Hydrogen burns in oxygen according to 2H<sub>2</sub> + O<sub>2</sub> → 2H<sub>2</sub>O. How many grams of water are produced "
                "from <b>8.0 g</b> of H<sub>2</sub> with excess oxygen?", 100)
    def figure(c, x, ytop, w, h):
        sc = 10
        x0, y0 = x + 70, ytop - h + 22
        c.setLineWidth(1.2); c.rect(x0, y0, 10 * sc, 6 * sc)
        c.arc(x0 + 10 * sc - 3 * sc, y0, x0 + 10 * sc + 3 * sc, y0 + 6 * sc, -90, 180)
        c.setFont("Helvetica", 9); c.drawCentredString(x0 + 5 * sc, y0 - 12, "10 cm"); c.drawString(x0 - 32, y0 + 3 * sc - 3, "6 cm")
    y = problem(c, y, 2, "The figure shows a rectangle 10 cm long and 6 cm wide with a semicircle attached to its right side. "
                "Find the total area of the figure.", 120, inside=figure)
    y = problem(c, y, 3, "A right triangle has legs of length 6 cm and 8 cm. Find the length of its hypotenuse.", 95)
    footer(c, "Science & Math Review"); c.save()


def scanned(src, dst):
    """rasterise a PDF page, tilt it, add noise and blur, and wrap it as an image-only PDF (no text layer)"""
    import fitz
    import numpy as np
    from PIL import Image, ImageFilter
    d = fitz.open(str(src))
    pix = d[0].get_pixmap(dpi=200)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples).convert("L")
    im = im.rotate(0.6, resample=Image.BICUBIC, expand=False, fillcolor=255)
    a = np.asarray(im).astype(np.float32)
    rng = np.random.default_rng(3)
    a = np.clip(a * 0.92 + 14 + rng.normal(0, 7, a.shape), 0, 255).astype(np.uint8)
    im = Image.fromarray(a).filter(ImageFilter.GaussianBlur(0.6))
    tmp = dst.with_suffix(".png"); im.save(tmp)
    out = fitz.open(); page = out.new_page(width=612, height=792)
    page.insert_image(page.rect, filename=str(tmp)); out.save(str(dst)); tmp.unlink()


if __name__ == "__main__":
    for sub, fn in (("physics", physics), ("algebra", algebra), ("statistics", statistics), ("chem_geometry", chem_geo)):
        (OUT / sub).mkdir(parents=True, exist_ok=True)
        fn(OUT / sub / f"{sub}_worksheet.pdf")
    (OUT / "scanned").mkdir(parents=True, exist_ok=True)
    scanned(OUT / "physics" / "physics_worksheet.pdf", OUT / "scanned" / "physics_scanned.pdf")
    print("test PDFs written to", OUT)
