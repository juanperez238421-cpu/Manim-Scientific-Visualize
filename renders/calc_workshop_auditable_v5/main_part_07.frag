
# =============================================================================
# SENIOR QA PATCH V5.2 — non-overlapping persistent-header transitions
# =============================================================================
def _qa_set_header(self, number: int, title: str, subtitle: str) -> None:
    """Preserve the exact JP header layout while preventing glyph collisions.

    The canonical style uses ReplacementTransform for entire Text groups. That
    is elegant for similarly shaped formulas, but long classroom titles can
    cross through each other during interpolation. For auditable delivery we
    keep the same typography, coordinates, numbering, rule and subtitle logic,
    then use a short fade-out/fade-in handoff so no frame contains two titles
    superimposed.
    """
    number_box = RoundedRectangle(
        width=0.72,
        height=0.52,
        corner_radius=0.10,
        stroke_color=BLACK_LINE,
        stroke_width=2.0,
        fill_color=WHITE_FILL,
        fill_opacity=1.0,
    )
    number_text = self.text(f"{number:02d}", 23, BOLD).move_to(number_box)

    title_text = self.text(title, 34, BOLD)
    available_title_width = SAFE_WIDTH - number_box.width - 0.38
    self.fit(title_text, available_title_width, 0.56)
    title_row = VGroup(VGroup(number_box, number_text), title_text)
    title_row.arrange(RIGHT, buff=0.25)
    title_row.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.48)

    rule = Line(LEFT * 7.48, RIGHT * 7.48, color=LIGHT_GRAY, stroke_width=2)
    rule.next_to(title_row, DOWN, buff=0.07)

    words = subtitle.split()
    if len(subtitle) > 96:
        midpoint = len(words) // 2
        best = midpoint
        best_gap = 10**9
        for index in range(max(1, midpoint - 5), min(len(words), midpoint + 6)):
            gap = abs(len(" ".join(words[:index])) - len(" ".join(words[index:])))
            if gap < best_gap:
                best = index
                best_gap = gap
        subtitle_lines = [" ".join(words[:best]), " ".join(words[best:])]
        subtitle_text = VGroup(*[self.text(line, 20) for line in subtitle_lines])
        subtitle_text.arrange(DOWN, aligned_edge=LEFT, buff=0.04)
    else:
        subtitle_text = self.text(subtitle, 21)

    self.fit(subtitle_text, 14.25, 0.70)
    subtitle_text.next_to(rule, DOWN, buff=0.08).align_to(title_row, LEFT)
    new_header = VGroup(title_row, rule)

    old_header = self.header_group
    old_subtitle = self.subtitle_group
    if old_header is not None or old_subtitle is not None:
        outgoing = [m for m in (old_header, old_subtitle) if m is not None]
        self.play(
            *[FadeOut(m, shift=UP * 0.035) for m in outgoing],
            run_time=0.34,
            rate_func=smootherstep,
        )
        for mob in outgoing:
            self.remove(mob)

    self.header_group = new_header
    self.subtitle_group = subtitle_text
    self.play(
        FadeIn(new_header, shift=UP * 0.035),
        FadeIn(subtitle_text, shift=UP * 0.025),
        run_time=0.56,
        rate_func=smootherstep,
    )
    self.wait(0.18)


WorkshopBase.set_header = _qa_set_header
