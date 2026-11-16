from manim import *
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from common import (
    VoiceScene, C_YELLOW, C_BLUE, C_GREEN, C_RED, C_ORANGE, C_WHITE, C_GRAY,
    C_DARK_GRAY, txt, bold_txt, log_label, pow_label, tile, MoonIcon, PaperStack
)

class S2Idea(VoiceScene):
    section_id = "S2_IDEA"

    def construct(self):
        # t05: "A sheet of paper is about a tenth of a millimeter thick."
        sheet = Rectangle(width=5.0, height=0.15, fill_color=C_BLUE, fill_opacity=0.9, stroke_color=C_WHITE, stroke_width=2).move_to([0, 0, 0])
        brace = Brace(sheet, RIGHT, color=C_WHITE)
        brace_lbl = txt("0.1 mm", font_size=56, color=C_WHITE).next_to(brace, RIGHT, buff=0.2)
        
        self.act(self.take_start("t05"), FadeIn(sheet), FadeIn(brace), FadeIn(brace_lbl), run_time=0.4)
        self.act(self.t + 0.1, VGroup(sheet, brace, brace_lbl).animate.scale(1.03), run_time=1.5)
        
        # t06: "Fold it once... two layers. Fold again, four. Then eight, sixteen, thirty-two."
        t06_start = self.take_start("t06")
        self.hold_until(t06_start)
        self.act(self.t, FadeOut(brace), FadeOut(brace_lbl), run_time=0.3)
        
        # Counter numbers popping: 2, 4, 8, 16, 32
        curr_counter = None
        layer_nums = [2, 4, 8, 16, 32]
        words_t06 = ["two", "four", "eight", "sixteen", "thirtytwo"]
        
        stack_layers = PaperStack(n_layers=1, width=4.0, height=0.15).move_to([0, -1.0, 0])
        self.act(self.t, Transform(sheet, stack_layers), run_time=0.2)
        
        for num, w in zip(layer_nums, words_t06):
            w_time = self.word_time("t06", w, occurrence=1)
            new_c = bold_txt(str(num), font_size=100, color=C_BLUE).move_to([0, 1.5, 0])
            new_stack = PaperStack(n_layers=num, width=4.0, height=0.15 + np.log2(num) * 0.35).move_to([0, -1.0, 0])
            if curr_counter is None:
                self.act(w_time, FadeIn(new_c, scale=1.2), Transform(sheet, new_stack), run_time=0.25)
                curr_counter = new_c
            else:
                self.act(w_time, ReplacementTransform(curr_counter, new_c), Transform(sheet, new_stack), run_time=0.25)
                curr_counter = new_c
            
        # t07: "Every fold doubles the thickness. After any number of folds, the stack is two multiplied by itself that many times."
        t07_start = self.take_start("t07")
        self.hold_until(t07_start)
        
        t_doubles = self.word_time("t07", "doubles", occurrence=1)
        x2_arrow = bold_txt("×2", font_size=72, color=C_BLUE).next_to(sheet, RIGHT, buff=0.4)
        self.act(t_doubles, FadeIn(x2_arrow, shift=UP*0.2), run_time=0.3)
        
        # Row of tiles "2 × 2 × 2 × 2"
        t_mult = self.word_time("t07", "multiplied", occurrence=1)
        self.act(t_mult, FadeOut(curr_counter), FadeOut(x2_arrow), FadeOut(sheet), run_time=0.3)
        
        tiles_row = VGroup(
            tile("2", color=C_BLUE, font_size=56),
            bold_txt("×", font_size=56, color=C_WHITE),
            tile("2", color=C_BLUE, font_size=56),
            bold_txt("×", font_size=56, color=C_WHITE),
            tile("2", color=C_BLUE, font_size=56),
            bold_txt("×", font_size=56, color=C_WHITE),
            tile("2", color=C_BLUE, font_size=56)
        ).arrange(RIGHT, buff=0.25).move_to([0, 0.4, 0])
        
        folds_brace = Brace(tiles_row, DOWN, color=C_GRAY)
        folds_brace_lbl = txt("folds", font_size=48, color=C_WHITE).next_to(folds_brace, DOWN, buff=0.15)
        
        self.act(self.t, FadeIn(tiles_row, shift=UP*0.2), FadeIn(folds_brace), FadeIn(folds_brace_lbl), run_time=0.4)
        
        # t08: "Now flip the question... ask how many doublings it takes to reach a target."
        t08_start = self.take_start("t08")
        self.hold_until(t08_start)
        self.act(self.t, *[FadeOut(m) for m in self.mobjects], run_time=0.3)
        
        q_thick = bold_txt("How thick?", font_size=60, color=C_WHITE).move_to([0, 1.4, 0])
        strike = Line(q_thick.get_left() + LEFT*0.2, q_thick.get_right() + RIGHT*0.2, color=C_RED, stroke_width=6)
        q_doublings = bold_txt("How many doublings?", font_size=58, color=C_YELLOW).move_to([0, -0.2, 0])
        
        flag_pole = Line(DOWN*0.5, UP*0.8, color=C_WHITE, stroke_width=4)
        flag_tri = Polygon([0, 0.8, 0], [0.8, 0.55, 0], [0, 0.3, 0], fill_color=C_GREEN, fill_opacity=1.0, stroke_width=0)
        flag = VGroup(flag_pole, flag_tri).next_to(q_doublings, RIGHT, buff=0.3)
        
        self.act(self.t, FadeIn(q_thick), run_time=0.3)
        self.act(self.t + 0.2, Create(strike), run_time=0.3)
        self.act(self.t, FadeIn(q_doublings, shift=UP*0.2), FadeIn(flag), run_time=0.4)
        
        # t09: "That's a log. A log answers one question: how many times do I multiply?"
        t09_start = self.take_start("t09")
        self.hold_until(t09_start)
        self.act(self.t, *[FadeOut(m) for m in self.mobjects], run_time=0.3)
        
        big_log2 = bold_txt("log", font_size=140, color=C_YELLOW).move_to([0, 1.2, 0])
        t_quest = self.word_time("t09", "question", occurrence=1)
        self.act(t_quest, FadeIn(big_log2, scale=1.2), run_time=0.35)
        
        line_q = bold_txt("How many times do I multiply?", font_size=64, color=C_WHITE).move_to([0, -0.6, 0])
        t_mult_q = self.word_time("t09", "multiply", occurrence=1)
        x_tile = tile("×", color=C_YELLOW, text_color=C_WHITE, font_size=64, width=0.9, height=0.9).next_to(line_q, DOWN, buff=0.4)
        self.act(t_mult_q, Write(line_q), FadeIn(x_tile), run_time=0.4)
        self.act(self.t, x_tile.animate.scale(1.2), run_time=0.15)
        self.act(self.t, x_tile.animate.scale(1/1.2), run_time=0.15)
        
        # t10: "Take eight... Two times two times two. Three twos. So log base two of eight is three."
        t10_start = self.take_start("t10")
        self.hold_until(t10_start)
        self.act(self.t, *[FadeOut(m) for m in self.mobjects], run_time=0.3)
        
        big_8 = bold_txt("8", font_size=180, color=C_WHITE).move_to([0, 2.0, 0])
        self.act(self.t, FadeIn(big_8, scale=1.2), run_time=0.3)
        
        t1 = tile("2", color=C_BLUE, font_size=56)
        m1 = bold_txt("×", font_size=56, color=C_WHITE)
        t2 = tile("2", color=C_BLUE, font_size=56)
        m2 = bold_txt("×", font_size=56, color=C_WHITE)
        t3 = tile("2", color=C_BLUE, font_size=56)
        eq8 = tile("= 8", color=C_GREEN, font_size=56)
        
        row_8 = VGroup(t1, m1, t2, m2, t3, eq8).arrange(RIGHT, buff=0.25).move_to([0, 0.2, 0])
        
        t_two1 = self.word_time("t10", "two", occurrence=2)
        self.act(t_two1, FadeIn(t1, scale=1.2), FadeIn(m1), run_time=0.25)
        t_two2 = self.word_time("t10", "two", occurrence=3)
        self.act(t_two2, FadeIn(t2, scale=1.2), FadeIn(m2), run_time=0.25)
        t_two3 = self.word_time("t10", "two", occurrence=4)
        self.act(t_two3, FadeIn(t3, scale=1.2), Transform(big_8, eq8), run_time=0.3)
        
        bracket_3 = Brace(VGroup(t1, m1, t2, m2, t3), DOWN, color=C_YELLOW)
        lbl_3 = bold_txt("3", font_size=72, color=C_YELLOW).next_to(bracket_3, DOWN, buff=0.15)
        t_three = self.word_time("t10", "three", occurrence=1)
        self.act(t_three, Create(bracket_3), FadeIn(lbl_3, scale=1.2), run_time=0.3)
        
        eq_log = VGroup(
            log_label(2, 8, font_size=72),
            bold_txt(" = ", font_size=72, color=C_WHITE),
            bold_txt("3", font_size=72, color=C_YELLOW)
        ).arrange(RIGHT, buff=0.15).move_to([0, -2.0, 0])
        
        t_eq = self.word_time("t10", "log", occurrence=1)
        self.act(t_eq, FadeIn(eq_log, shift=UP*0.2), run_time=0.4)
        
        # t11: "Same idea with tens. A thousand is ten times ten times ten, so log base ten of a thousand is three."
        t11_start = self.take_start("t11")
        self.hold_until(t11_start)
        self.act(self.t, *[FadeOut(m) for m in self.mobjects], run_time=0.3)
        
        t_10_1 = tile("10", color=C_ORANGE, font_size=52)
        m10_1 = bold_txt("×", font_size=52, color=C_WHITE)
        t_10_2 = tile("10", color=C_ORANGE, font_size=52)
        m10_2 = bold_txt("×", font_size=52, color=C_WHITE)
        t_10_3 = tile("10", color=C_ORANGE, font_size=52)
        eq_1000 = tile("= 1,000", color=C_GREEN, font_size=52)
        row_1000 = VGroup(t_10_1, m10_1, t_10_2, m10_2, t_10_3, eq_1000).arrange(RIGHT, buff=0.22).move_to([0, 0.8, 0])
        
        eq_log10 = VGroup(
            log_label(10, "1,000", font_size=72),
            bold_txt(" = ", font_size=72, color=C_WHITE),
            bold_txt("3", font_size=72, color=C_YELLOW)
        ).arrange(RIGHT, buff=0.15).move_to([0, -1.8, 0])
        
        self.act(self.t, FadeIn(row_1000, shift=UP*0.2), run_time=0.4)
        t_log10 = self.word_time("t11", "log", occurrence=1)
        self.act(t_log10, FadeIn(eq_log10, shift=UP*0.2), run_time=0.4)
        
        # t12: "That's the whole definition. A log counts multiplications. It's the exponent."
        t12_start = self.take_start("t12")
        self.hold_until(t12_start)
        self.act(self.t, *[FadeOut(m) for m in self.mobjects], run_time=0.3)
        
        pow_eq = VGroup(pow_label(2, 3, font_size=80), bold_txt(" = 8", font_size=80, color=C_WHITE)).arrange(RIGHT, buff=0.15).move_to([0, 1.2, 0])
        log_eq = VGroup(log_label(2, 8, font_size=80), bold_txt(" = ", font_size=80, color=C_WHITE), bold_txt("3", font_size=80, color=C_YELLOW)).arrange(RIGHT, buff=0.15).move_to([0, -0.6, 0])
        d_arrow = DoubleArrow(pow_eq.get_bottom(), log_eq.get_top(), color=C_GRAY, stroke_width=4)
        
        self.act(self.t, FadeIn(pow_eq), FadeIn(d_arrow), FadeIn(log_eq), run_time=0.4)
        
        t_exp = self.word_time("t12", "exponent", occurrence=1)
        exp_lbl = bold_txt("the exponent", font_size=42, color=C_YELLOW).move_to([pow_eq[0][1].get_x() + 0.3, 2.5, 0])
        exp_arr = Arrow(exp_lbl.get_bottom(), pow_eq[0][1].get_top(), color=C_YELLOW, stroke_width=4, buff=0.1)
        self.act(t_exp, FadeIn(exp_lbl, shift=DOWN*0.1), Create(exp_arr), run_time=0.3)
        
        # t13 (CHALLENGE): "Pause and try one. What is log base two of thirty-two?"
        t13_start = self.take_start("t13")
        self.hold_until(t13_start)
        self.act(self.t, *[FadeOut(m) for m in self.mobjects], run_time=0.3)
        
        q_32 = VGroup(
            log_label(2, 32, font_size=110),
            bold_txt(" = ", font_size=110, color=C_WHITE),
            bold_txt("?", font_size=110, color=C_YELLOW)
        ).arrange(RIGHT, buff=0.2).move_to([0, 1.2, 0])
        
        t_what = self.word_time("t13", "what", occurrence=1)
        self.act(t_what, FadeIn(q_32, scale=1.2), run_time=0.4)
        
        t13_pause_start = self.take_speech_end("t13")
        self.hold_until(t13_pause_start)
        
        cd_circle = Circle(radius=0.9, color=C_BLUE, stroke_width=5).move_to([0, -1.0, 0])
        self.act(self.t, Create(cd_circle), run_time=0.2)
        
        for c_val in [3, 2, 1]:
            num_t = bold_txt(str(c_val), font_size=64, color=C_YELLOW).move_to(cd_circle.get_center())
            self.act(self.t, FadeIn(num_t, scale=1.3), run_time=0.15)
            self.step(0.3)
            self.act(self.t, FadeOut(num_t), run_time=0.1)
        self.act(self.t, FadeOut(cd_circle), run_time=0.1)
        
        # t14: "Five. Two times two times two times two times two is thirty-two."
        t14_start = self.take_start("t14")
        self.hold_until(t14_start)
        
        ans_5 = bold_txt("5", font_size=110, color=C_YELLOW).move_to(q_32[2].get_center())
        self.act(self.t, Transform(q_32[2], ans_5), run_time=0.2)
        self.act(self.t, q_32[2].animate.scale(1.15), run_time=0.15)
        self.act(self.t, q_32[2].animate.scale(1/1.15), run_time=0.15)
        
        tiles_32 = VGroup(
            tile("2", color=C_BLUE, font_size=46),
            bold_txt("×", font_size=46, color=C_WHITE),
            tile("2", color=C_BLUE, font_size=46),
            bold_txt("×", font_size=46, color=C_WHITE),
            tile("2", color=C_BLUE, font_size=46),
            bold_txt("×", font_size=46, color=C_WHITE),
            tile("2", color=C_BLUE, font_size=46),
            bold_txt("×", font_size=46, color=C_WHITE),
            tile("2", color=C_BLUE, font_size=46),
            tile("= 32", color=C_GREEN, font_size=46)
        ).arrange(RIGHT, buff=0.18).scale_to_fit_width(11.5).move_to([0, -1.0, 0])
        
        self.act(self.t, FadeIn(tiles_32, shift=UP*0.2), run_time=0.4)
        
        # t15: "So our paper problem is a log. How many doublings make the stack reach the Moon? Hold that thought."
        t15_start = self.take_start("t15")
        self.hold_until(t15_start)
        self.act(self.t, *[FadeOut(m) for m in self.mobjects], run_time=0.3)
        
        sheet_ret = PaperStack(n_layers=8, width=2.2, height=0.6).move_to([-4.5, 0.4, 0])
        moon_ret = MoonIcon(radius=0.8).move_to([5.2, 2.0, 0])
        line_ret = DashedLine(sheet_ret.get_right(), moon_ret.get_left(), color=C_GRAY)
        lbl_ret = bold_txt("Folds: ?", font_size=56, color=C_YELLOW).to_corner(UL, buff=0.8)
        
        self.act(self.t, FadeIn(sheet_ret), FadeIn(moon_ret), FadeIn(line_ret), FadeIn(lbl_ret), run_time=0.4)
        
        t_hold = self.word_time("t15", "thought", occurrence=1)
        pulse_log = bold_txt("log", font_size=100, color=C_YELLOW).move_to([0, 0.4, 0])
        q_tile = tile("?", color=C_ORANGE, font_size=64).next_to(moon_ret, LEFT, buff=0.5)
        self.act(t_hold, FadeIn(pulse_log), FadeIn(q_tile), run_time=0.3)
        
        t15_end = self.take_end("t15")
        self.hold_until(t15_end - 0.4)
        self.act(self.t, *[FadeOut(m) for m in self.mobjects], run_time=0.4)
        
        self.finish()
