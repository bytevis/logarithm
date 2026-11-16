from manim import *
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from common import (
    VoiceScene, C_YELLOW, C_BLUE, C_GREEN, C_RED, C_ORANGE, C_WHITE, C_GRAY,
    C_DARK_GRAY, txt, bold_txt, log_label, pow_label, tile, MoonIcon, PaperStack
)

class S6Payoff(VoiceScene):
    section_id = "S6_PAYOFF"

    def construct(self):
        # t35: "Now let's pay off that promise. How many folds to reach the Moon?"
        t35_start = self.take_start("t35")
        self.hold_until(t35_start)
        
        q_moon_title = bold_txt("Folds to the Moon?", font_size=72, color=C_WHITE).move_to([0, 2.3, 0])
        stack_p = PaperStack(n_layers=8, width=2.2, height=0.6).move_to([-4.5, 0.4, 0])
        moon_p = MoonIcon(radius=0.8).move_to([5.2, 1.8, 0])
        dot_line = DashedLine(stack_p.get_right(), moon_p.get_left(), color=C_GRAY)
        lbl_q_folds = bold_txt("Folds: ?", font_size=56, color=C_YELLOW).to_corner(UL, buff=0.8)
        
        log_tile_pulse = tile("log", color=C_YELLOW, font_size=56).move_to([0, 0.4, 0])
        
        self.act(self.t, FadeIn(q_moon_title), FadeIn(stack_p), FadeIn(moon_p), FadeIn(dot_line), FadeIn(lbl_q_folds), FadeIn(log_tile_pulse), run_time=0.5)
        self.act(self.t + 0.1, log_tile_pulse.animate.scale(1.15), run_time=0.2)
        self.act(self.t, log_tile_pulse.animate.scale(1/1.15), run_time=0.2)
        
        # t36: "The Moon is about three hundred eighty-four thousand kilometers away... about three point eight trillion times thicker."
        t36_start = self.take_start("t36")
        self.hold_until(t36_start)
        self.act(self.t, FadeOut(q_moon_title), FadeOut(dot_line), FadeOut(lbl_q_folds), FadeOut(log_tile_pulse), run_time=0.3)
        
        # Reposition moon and paper with distance labels
        t_moon_dist = bold_txt("Moon: ≈ 384,400 km", font_size=56, color=C_WHITE).next_to(moon_p, DOWN, buff=0.3)
        t_paper_thick = bold_txt("Paper: ≈ 0.1 mm", font_size=56, color=C_WHITE).next_to(stack_p, DOWN, buff=0.3)
        
        self.act(self.t, FadeIn(t_moon_dist), FadeIn(t_paper_thick), run_time=0.4)
        
        t_trillion = self.word_time("t36", "trillion", occurrence=1)
        lbl_grow = bold_txt("stack must grow ≈ 3.8 trillion ×", font_size=64, color=C_ORANGE).move_to([0, -1.8, 0])
        self.act(t_trillion, FadeIn(lbl_grow, scale=1.2), run_time=0.5)
        
        # t37: "Here's the mental trick. Two to the power of ten is one thousand twenty-four. Call it a thousand."
        t37_start = self.take_start("t37")
        self.hold_until(t37_start)
        self.act(self.t,
            FadeOut(stack_p), FadeOut(moon_p), FadeOut(t_moon_dist), FadeOut(t_paper_thick), FadeOut(lbl_grow),
            run_time=0.3
        )
        
        pow_10 = VGroup(
            pow_label(2, 10, font_size=84),
            bold_txt(" = 1,024", font_size=84, color=C_WHITE)
        ).arrange(RIGHT, buff=0.15).move_to([0, 1.2, 0])
        
        approx_1000 = bold_txt("≈ 1,000", font_size=90, color=C_ORANGE).move_to([0, -0.6, 0])
        
        self.act(self.t, FadeIn(pow_10, shift=UP*0.2), run_time=0.4)
        
        t_call_1000 = self.word_time("t37", "thousand", occurrence=1)
        self.act(t_call_1000, FadeIn(approx_1000, scale=1.2), run_time=0.4)
        
        # t38: "So ten doublings is about a thousand. Twenty is about a million. Thirty, a billion. Forty, about a trillion."
        t38_start = self.take_start("t38")
        self.hold_until(t38_start)
        self.act(self.t, FadeOut(pow_10), FadeOut(approx_1000), run_time=0.3)
        
        # Ladder rows:
        # 10 folds ≈ 1,000         (10 cm)
        # 20 folds ≈ 1,000,000     (105 m)
        # 30 folds ≈ 1,000,000,000 (107 km)
        # 40 folds ≈ 1,000,000,000,000 (110,000 km)
        ladder_data = [
            ("10 folds ≈ 1,000", "10 cm", 1.8),
            ("20 folds ≈ 1,000,000", "105 m", 0.7),
            ("30 folds ≈ 1,000,000,000", "107 km", -0.4),
            ("40 folds ≈ 1,000,000,000,000", "110,000 km", -1.5)
        ]
        ladder_mobs = []
        for text_l, text_r, y_pos in ladder_data:
            t_left = bold_txt(text_l, font_size=52, color=C_WHITE).move_to([-1.5, y_pos, 0])
            t_right = txt(text_r, font_size=40, color=C_GRAY).move_to([4.0, y_pos, 0])
            ladder_mobs.append(VGroup(t_left, t_right))
            
        t_ten_d = self.word_time("t38", "ten", occurrence=1)
        self.act(t_ten_d, FadeIn(ladder_mobs[0], shift=UP*0.2), run_time=0.35)
        
        t_twenty_d = self.word_time("t38", "twenty", occurrence=1)
        self.act(t_twenty_d, FadeIn(ladder_mobs[1], shift=UP*0.2), run_time=0.35)
        
        t_thirty_d = self.word_time("t38", "thirty", occurrence=1)
        self.act(t_thirty_d, FadeIn(ladder_mobs[2], shift=UP*0.2), run_time=0.35)
        
        t_forty_d = self.word_time("t38", "forty", occurrence=1)
        self.act(t_forty_d, FadeIn(ladder_mobs[3], shift=UP*0.2), run_time=0.35)
        
        # t39: "Forty doublings gets us about a trillion, still short. Forty-one isn't enough. But forty-two is a little over four trillion, and that's enough."
        t39_start = self.take_start("t39")
        self.hold_until(t39_start)
        self.act(self.t, *[FadeOut(m) for m in ladder_mobs], run_time=0.3)
        
        # Vertical distance scale with Moon line at 384,400 km
        v_line = Line([-1.0, -2.4, 0], [-1.0, 2.4, 0], color=C_GRAY, stroke_width=3)
        moon_bar = Line([-3.5, 1.2, 0], [1.5, 1.2, 0], color=C_YELLOW, stroke_width=4)
        moon_lbl = bold_txt("Moon: 384,400 km", font_size=42, color=C_YELLOW).next_to(moon_bar, RIGHT, buff=0.25)
        
        self.act(self.t, Create(v_line), Create(moon_bar), FadeIn(moon_lbl), run_time=0.5)
        
        # 40 folds marker: 110,000 km (stops under line)
        m40 = Line([-2.0, -1.2, 0], [0.0, -1.2, 0], color=C_RED, stroke_width=4)
        lbl40 = txt("110,000 km", font_size=40, color=C_RED).next_to(m40, LEFT, buff=0.2)
        lbl40_short = bold_txt("short", font_size=36, color=C_RED).next_to(m40, RIGHT, buff=0.2)
        
        self.act(self.t, FadeIn(m40), FadeIn(lbl40), FadeIn(lbl40_short), run_time=0.4)
        
        # 41 folds: 220,000 km (still under line)
        t_41 = self.word_time("t39", "fortyone", occurrence=1)
        m41 = Line([-2.0, 0.0, 0], [0.0, 0.0, 0], color=C_ORANGE, stroke_width=4)
        lbl41 = txt("220,000 km", font_size=40, color=C_ORANGE).next_to(m41, LEFT, buff=0.2)
        self.act(t_41, FadeIn(m41), FadeIn(lbl41), run_time=0.4)
        
        # 42 folds: 440,000 km (jumps above moon line, turns green)
        t_42 = self.word_time("t39", "fortytwo", occurrence=1)
        m42 = Line([-2.2, 1.9, 0], [0.2, 1.9, 0], color=C_GREEN, stroke_width=5)
        lbl42 = bold_txt("440,000 km", font_size=42, color=C_GREEN).next_to(m42, LEFT, buff=0.2)
        self.act(t_42, FadeIn(m42), FadeIn(lbl42), run_time=0.4)
        
        # t40: "Forty-two folds. The same answer a calculator gives, worked out in your head."
        t40_start = self.take_start("t40")
        self.hold_until(t40_start)
        self.act(self.t,
            FadeOut(v_line), FadeOut(moon_bar), FadeOut(moon_lbl),
            FadeOut(m40), FadeOut(lbl40), FadeOut(lbl40_short),
            FadeOut(m41), FadeOut(lbl41),
            FadeOut(m42), FadeOut(lbl42),
            run_time=0.3
        )
        
        # Big yellow 42 slams in with pulse
        big_42 = bold_txt("42", font_size=200, color=C_YELLOW).move_to([0, 0.6, 0])
        lbl_folds_42 = bold_txt("folds", font_size=72, color=C_WHITE).next_to(big_42, DOWN, buff=0.3)
        
        self.act(self.t, FadeIn(big_42, scale=1.5), FadeIn(lbl_folds_42), run_time=0.4)
        self.act(self.t + 0.1, big_42.animate.scale(1.1), run_time=0.2)
        self.act(self.t, big_42.animate.scale(1/1.1), run_time=0.2)
        
        # t41: "Of course, a normal sheet only folds about seven or eight times by hand. The record is twelve... Britney Gallivan... over a kilometer of toilet paper..."
        t41_start = self.take_start("t41")
        self.hold_until(t41_start)
        self.act(self.t, FadeOut(big_42), FadeOut(lbl_folds_42), run_time=0.3)
        
        # Left: by hand: about 7 to 8
        hand_icon = Square(side_length=1.2, fill_color=C_BLUE, fill_opacity=0.6, stroke_color=C_WHITE).move_to([-4.5, 0.8, 0])
        lbl_hand = VGroup(
            txt("by hand:", font_size=38, color=C_WHITE),
            bold_txt("7 to 8 folds", font_size=40, color=C_YELLOW)
        ).arrange(DOWN, buff=0.1).next_to(hand_icon, DOWN, buff=0.2)
        
        # Middle: 12, Britney Gallivan, 2002
        t_12 = bold_txt("12", font_size=130, color=C_YELLOW).move_to([0, 1.0, 0])
        lbl_britney = bold_txt("Britney Gallivan", font_size=52, color=C_WHITE).next_to(t_12, DOWN, buff=0.2)
        lbl_year = txt("2002", font_size=44, color=C_GRAY).next_to(lbl_britney, DOWN, buff=0.12)
        
        # Over 1 km roll
        roll = Circle(radius=0.7, color=C_WHITE, stroke_width=3).move_to([4.2, 1.2, 0])
        lbl_roll = bold_txt("over 1 km", font_size=46, color=C_WHITE).next_to(roll, DOWN, buff=0.2)
        
        # Log pulse at right
        t_math_log = bold_txt("log", font_size=80, color=C_YELLOW).next_to(lbl_roll, DOWN, buff=0.3)
        
        self.act(self.t, FadeIn(hand_icon), FadeIn(lbl_hand), run_time=0.4)
        
        t_record = self.word_time("t41", "twelve", occurrence=1)
        self.act(t_record, FadeIn(t_12, scale=1.3), FadeIn(lbl_britney), FadeIn(lbl_year), run_time=0.4)
        
        t_km = self.word_time("t41", "kilometer", occurrence=1)
        self.act(t_km, FadeIn(roll), FadeIn(lbl_roll), run_time=0.4)
        
        t_math = self.word_time("t41", "math", occurrence=1)
        self.act(t_math, FadeIn(t_math_log), t_math_log.animate.scale(1.2), run_time=0.4)
        
        # t42: "A log just counts how many times you multiply. Forty-two doublings, and a sheet of paper reaches the Moon."
        t42_start = self.take_start("t42")
        self.hold_until(t42_start)
        self.act(self.t,
            FadeOut(hand_icon), FadeOut(lbl_hand),
            FadeOut(t_12), FadeOut(lbl_britney), FadeOut(lbl_year),
            FadeOut(roll), FadeOut(lbl_roll), FadeOut(t_math_log),
            run_time=0.3
        )
        
        # Final frame:
        # Top row: 2 × 2 × 2 = 8
        # Below: log_2(8) = 3
        # Moon icon with "42" tile near it
        t_f1 = tile("2", color=C_BLUE, font_size=56)
        m_f1 = bold_txt("×", font_size=56, color=C_WHITE)
        t_f2 = tile("2", color=C_BLUE, font_size=56)
        m_f2 = bold_txt("×", font_size=56, color=C_WHITE)
        t_f3 = tile("2", color=C_BLUE, font_size=56)
        eq_f8 = tile("= 8", color=C_GREEN, font_size=56)
        row_f = VGroup(t_f1, m_f1, t_f2, m_f2, t_f3, eq_f8).arrange(RIGHT, buff=0.25).move_to([0, 1.8, 0])
        
        eq_final_log = VGroup(
            log_label(2, 8, font_size=72),
            bold_txt(" = ", font_size=72, color=C_WHITE),
            bold_txt("3", font_size=72, color=C_YELLOW)
        ).arrange(RIGHT, buff=0.15).move_to([0, 0.4, 0])
        
        moon_final = MoonIcon(radius=0.9).move_to([2.2, -1.6, 0])
        tile_42_final = tile("42", color=C_YELLOW, font_size=64).next_to(moon_final, LEFT, buff=0.4)
        
        self.act(self.t, FadeIn(row_f), FadeIn(eq_final_log), FadeIn(moon_final), FadeIn(tile_42_final), run_time=0.6)
        
        # Pulse "x" signs
        self.act(self.t + 0.2, m_f1.animate.scale(1.3), run_time=0.2)
        self.act(self.t, m_f1.animate.scale(1/1.3), m_f2.animate.scale(1.3), run_time=0.2)
        self.act(self.t, m_f2.animate.scale(1/1.3), run_time=0.2)
        
        self.finish()
