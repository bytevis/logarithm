from manim import *
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from common import (
    VoiceScene, C_YELLOW, C_BLUE, C_GREEN, C_RED, C_ORANGE, C_WHITE, C_GRAY,
    C_DARK_GRAY, txt, bold_txt, log_label, pow_label, tile, MoonIcon, PaperStack
)

class S1Hook(VoiceScene):
    section_id = "S1_HOOK"

    def construct(self):
        # Sheet, Moon, Dotted Line, Counters
        sheet = Rectangle(
            width=2.2, height=3.0,
            fill_color=C_WHITE, fill_opacity=0.95,
            stroke_color=C_GRAY, stroke_width=2
        ).move_to([-4.5, 0.4, 0])
        
        moon = MoonIcon(radius=0.8).move_to([5.2, 2.0, 0])
        dotted_line = DashedLine(sheet.get_right(), moon.get_left(), dash_length=0.15, dashed_ratio=0.5, color=C_GRAY)
        
        folds_lbl = bold_txt("Folds: 0", font_size=56, color=C_WHITE).to_corner(UL, buff=0.8)
        thick_lbl = txt("Thickness: 0.1 mm", font_size=48, color=C_WHITE).next_to(folds_lbl, DOWN, aligned_edge=LEFT, buff=0.2)
        
        self.add(sheet, moon, dotted_line, folds_lbl, thick_lbl)
        
        # t01: "How many times would you have to fold a sheet of paper to reach the Moon?"
        # At "fold": sheet folds in half and becomes stack, counter steps 1..7 (thickness 0.2..12.8 mm)
        t_fold = self.word_time("t01", "fold", occurrence=1)
        self.hold_until(t_fold)
        
        # Transform sheet to stack
        stack = PaperStack(n_layers=1, width=2.2, height=0.15).move_to(sheet.get_center())
        self.act(self.t, Transform(sheet, stack), run_time=0.35)
        
        thickness_vals = [0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 12.8]
        step_dt = 0.40
        for i, th in enumerate(thickness_vals, start=1):
            new_folds = bold_txt(f"Folds: {i}", font_size=56, color=C_WHITE).move_to(folds_lbl)
            new_thick = txt(f"Thickness: {th} mm", font_size=48, color=C_WHITE).move_to(thick_lbl)
            new_stack = PaperStack(n_layers=min(2**i, 32), width=2.2, height=0.15 + i * 0.12).move_to(sheet.get_center())
            self.act(self.t,
                Transform(folds_lbl, new_folds),
                Transform(thick_lbl, new_thick),
                Transform(sheet, new_stack),
                run_time=0.2
            )
            if i < len(thickness_vals):
                self.step(step_dt - 0.2)
                
        # t02: "Take a guess. Thousands? Millions?"
        t02_start = self.take_start("t02")
        self.hold_until(t02_start)
        
        q_folds = bold_txt("Folds: ?", font_size=56, color=C_YELLOW).move_to(folds_lbl)
        q_thick = txt("Thickness: ?", font_size=48, color=C_YELLOW).move_to(thick_lbl)
        self.act(self.t, Transform(folds_lbl, q_folds), Transform(thick_lbl, q_thick), run_time=0.3)
        
        t_thous = self.word_time("t02", "thousands", occurrence=1)
        chip_1k = tile("1,000?", color=C_ORANGE, text_color=C_WHITE, font_size=48).move_to([0.2, 0.8, 0])
        self.act(t_thous, FadeIn(chip_1k, scale=1.2), run_time=0.25)
        
        t_mill = self.word_time("t02", "millions", occurrence=1)
        chip_1m = tile("1,000,000?", color=C_ORANGE, text_color=C_WHITE, font_size=48).move_to([0.2, -0.4, 0])
        self.act(t_mill, FadeIn(chip_1m, scale=1.2), run_time=0.25)
        
        # t03: "The real answer is far smaller, and finding it takes one tool: a log."
        t03_start = self.take_start("t03")
        self.hold_until(t03_start)
        
        t_smaller = self.word_time("t03", "smaller", occurrence=1)
        self.act(t_smaller, FadeOut(chip_1k, shift=LEFT*0.5), FadeOut(chip_1m, shift=RIGHT*0.5), run_time=0.3)
        
        t_log = self.word_time("t03", "log", occurrence=1)
        big_log = bold_txt("log", font_size=140, color=C_YELLOW).move_to([0, 0.4, 0])
        self.act(t_log, FadeIn(big_log, scale=1.3), run_time=0.35)
        self.act(self.t + 0.1, big_log.animate.scale(1.08), run_time=0.2)
        self.act(self.t, big_log.animate.scale(1/1.08), run_time=0.2)
        
        # t04: "By the end of this video, you'll work it out in your head. No calculator."
        t04_start = self.take_start("t04")
        self.hold_until(t04_start)
        
        t_work = self.word_time("t04", "work", occurrence=1)
        small_log = bold_txt("log", font_size=64, color=C_YELLOW).to_corner(UL, buff=0.8)
        self.act(
            t_work,
            Transform(big_log, small_log),
            FadeOut(folds_lbl), FadeOut(thick_lbl),
            FadeOut(sheet), FadeOut(moon), FadeOut(dotted_line),
            run_time=0.5
        )
        
        t_calc = self.word_time("t04", "calculator", occurrence=1)
        calc_body = RoundedRectangle(corner_radius=0.2, width=1.8, height=2.4, fill_color=C_DARK_GRAY, fill_opacity=0.9, stroke_color=C_GRAY, stroke_width=3)
        calc_screen = Rectangle(width=1.3, height=0.5, fill_color="#333333", fill_opacity=1.0, stroke_width=0).shift(UP * 0.6)
        keys = VGroup()
        for r in range(2):
            for c in range(3):
                k = Square(side_length=0.28, fill_color=C_GRAY, fill_opacity=0.6, stroke_width=0)
                k.move_to(np.array([-0.45 + c * 0.45, -0.15 - r * 0.45, 0]))
                keys.add(k)
        calc_grp = VGroup(calc_body, calc_screen, keys).move_to([0, 0.4, 0])
        
        cross_line1 = Line(calc_body.get_corner(UL), calc_body.get_corner(DR), color=C_RED, stroke_width=6)
        cross_line2 = Line(calc_body.get_corner(UR), calc_body.get_corner(DL), color=C_RED, stroke_width=6)
        red_x = VGroup(cross_line1, cross_line2)
        
        no_calc_txt = bold_txt("No calculator", font_size=64, color=C_WHITE).next_to(calc_grp, DOWN, buff=0.5)
        
        self.act(t_calc, FadeIn(calc_grp), FadeIn(red_x), FadeIn(no_calc_txt), run_time=0.4)
        
        # Fade out before section end
        t04_end = self.take_end("t04")
        self.hold_until(t04_end - 0.4)
        self.act(self.t, FadeOut(calc_grp), FadeOut(red_x), FadeOut(no_calc_txt), FadeOut(big_log), run_time=0.4)
        
        self.finish()
