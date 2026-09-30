from jp_manim_standard import *

class StandardSmokeTest(JPMathClassroomScene):
    def validate_lesson_data(self) -> None:
        assert_close(2 + 2, 4, label="smoke arithmetic")

    def construct(self) -> None:
        self.standard_opening("JP MANIM STANDARD","SMOKE TEST",
            "Validate typography, layout helpers and rendering.",
            "Fast enough for CI; representative enough to catch regressions.")
        self.set_header(1,"LAYOUT CONTRACT","A representative formula and note panel.")
        group=VGroup(
            self.formula_panel(r"2+2=4",width=5.2,height=1.1,font_size=44),
            self.note_panel("STATUS",["Visual library imported","Safe layout active","Render pipeline ready"],width=5.2),
        ).arrange(DOWN,buff=0.3)
        group.move_to(DOWN*0.25)
        self.assert_content_safe(group,"smoke group")
        self.play(FadeIn(group),run_time=RUN_NORMAL)
        self.wait(PAUSE_SHORT)
