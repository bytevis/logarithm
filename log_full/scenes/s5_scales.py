from manim import *
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from common import (
    VoiceScene, C_YELLOW, C_BLUE, C_GREEN, C_RED, C_ORANGE, C_WHITE, C_GRAY,
    C_DARK_GRAY, txt, bold_txt, tile, ruler
)

class S5Scales(VoiceScene):
    section_id = "S5_SCALES"

    def construct(self):
        # t30: "That log ruler shows up wherever we need to squash a huge range into small numbers."
        t30_start = self.take_start("t30")
        self.hold_until(t30_start)
        
        log_r = ruler(length=10.0, is_log=True, color=C_WHITE).move_to([0, 1.2, 0])
        bar_mil = Rectangle(width=8.0, height=0.6, fill_color=C_ORANGE, fill_opacity=0.8, stroke_color=C_WHITE).move_to([0, -0.6, 0])
        lbl_mil = bold_txt("1,000,000", font_size=48, color=C_WHITE).move_to(bar_mil.get_center())
        
        self.act(self.t, Create(log_r), FadeIn(bar_mil), FadeIn(lbl_mil), run_time=0.6)
        
        t_squash = self.word_time("t30", "squash", occurrence=1)
        tile_20 = tile("≈ 20", color=C_YELLOW, text_color=C_WHITE, font_size=48).move_to([0, -0.6, 0])
        arr_l = Arrow([-4.5, -0.6, 0], [-2.0, -0.6, 0], color=C_YELLOW, stroke_width=5)
        arr_r = Arrow([4.5, -0.6, 0], [2.0, -0.6, 0], color=C_YELLOW, stroke_width=5)
        
        self.act(t_squash,
            Transform(bar_mil, tile_20.bg),
            Transform(lbl_mil, tile_20.text),
            FadeIn(arr_l), FadeIn(arr_r),
            run_time=0.4
        )
        self.act(self.t, FadeOut(arr_l), FadeOut(arr_r), run_time=0.2)
        
        # t31: "Earthquakes... ten times bigger waves on a seismograph... magnitude seven is a hundred times bigger than a five."
        t31_start = self.take_start("t31")
        self.hold_until(t31_start)
        self.act(self.t, FadeOut(log_r), FadeOut(bar_mil), FadeOut(lbl_mil), run_time=0.3)
        
        # Deterministic seismograph traces (np.random.seed(7)), width 4.0, max amp 0.15 and 1.5
        np.random.seed(7)
        x_pts = np.linspace(-2.0, 2.0, 120)
        
        # Raw noise normalized to max amp exactly 1.0
        raw_noise = np.random.randn(120) * np.exp(-((x_pts) / 1.2)**2)
        raw_noise = raw_noise / np.max(np.abs(raw_noise))
        
        # Trace 1: Mag 5 -> max amplitude exactly 0.15
        pts_m5 = [np.array([x - 0.2, 1.2 + raw_noise[i] * 0.15, 0]) for i, x in enumerate(x_pts)]
        trace_m5 = VMobject(color=C_BLUE, stroke_width=3).set_points_smoothly(pts_m5)
        lbl_m5 = bold_txt("Magnitude 5", font_size=40, color=C_WHITE).next_to(trace_m5, LEFT, buff=0.25)
        
        # Trace 2: Mag 6 -> max amplitude exactly 1.5
        pts_m6 = [np.array([x - 0.2, -1.0 + raw_noise[i] * 1.5, 0]) for i, x in enumerate(x_pts)]
        trace_m6 = VMobject(color=C_ORANGE, stroke_width=3.5).set_points_smoothly(pts_m6)
        lbl_m6 = bold_txt("Magnitude 6", font_size=40, color=C_WHITE).next_to(trace_m6, LEFT, buff=0.25)
        
        self.act(self.t, Create(trace_m5), FadeIn(lbl_m5), Create(trace_m6), FadeIn(lbl_m6), run_time=1.0)
        
        t_ten = self.word_time("t31", "ten", occurrence=1)
        brace_10x = Brace(VGroup(trace_m5, trace_m6), RIGHT, color=C_GREEN)
        lbl_10x = bold_txt("10× bigger", font_size=42, color=C_GREEN).next_to(brace_10x, RIGHT, buff=0.2)
        lbl_32x = txt("≈ 32× energy", font_size=36, color=C_GREEN).next_to(lbl_10x, DOWN, buff=0.15)
        
        self.act(t_ten, Create(brace_10x), FadeIn(lbl_10x), FadeIn(lbl_32x), run_time=0.4)
        
        # Ladder replaces them: tiles 5, 6, 7
        t_seven = self.word_time("t31", "seven", occurrence=1)
        self.hold_until(t_seven)
        self.act(self.t,
            FadeOut(trace_m5), FadeOut(lbl_m5),
            FadeOut(trace_m6), FadeOut(lbl_m6),
            FadeOut(brace_10x), FadeOut(lbl_10x), FadeOut(lbl_32x),
            run_time=0.3
        )
        
        t_m5 = tile("5", color=C_BLUE, font_size=56).move_to([-3.0, 0, 0])
        t_m6 = tile("6", color=C_ORANGE, font_size=56).move_to([0, 0, 0])
        t_m7 = tile("7", color=C_RED, font_size=56).move_to([3.0, 0, 0])
        
        arr_5_6 = Arrow(t_m5.get_right(), t_m6.get_left(), color=C_GREEN, stroke_width=4)
        lbl_x10_1 = bold_txt("×10", font_size=38, color=C_GREEN).next_to(arr_5_6, UP, buff=0.1)
        
        arr_6_7 = Arrow(t_m6.get_right(), t_m7.get_left(), color=C_GREEN, stroke_width=4)
        lbl_x10_2 = bold_txt("×10", font_size=38, color=C_GREEN).next_to(arr_6_7, UP, buff=0.1)
        
        brace_5_7 = Brace(VGroup(t_m5, t_m7), DOWN, color=C_GREEN)
        lbl_x100 = bold_txt("×100", font_size=56, color=C_GREEN).next_to(brace_5_7, DOWN, buff=0.15)
        
        ladder_m = VGroup(t_m5, arr_5_6, lbl_x10_1, t_m6, arr_6_7, lbl_x10_2, t_m7, brace_5_7, lbl_x100)
        self.act(self.t, FadeIn(ladder_m), run_time=0.6)
        
        # t32: "Acidity. On the pH scale... A pH of three is a thousand times more acidic than a pH of six."
        t32_start = self.take_start("t32")
        self.hold_until(t32_start)
        self.act(self.t, FadeOut(ladder_m), run_time=0.3)
        
        lbl_ph = bold_txt("pH", font_size=72, color=C_WHITE).move_to([0, 2.0, 0])
        
        # Tiles 6, 5, 4, 3 from green to red
        t_ph6 = tile("6", color=C_GREEN, font_size=52)
        t_ph5 = tile("5", color="#A0D911", font_size=52)
        t_ph4 = tile("4", color=C_ORANGE, font_size=52)
        t_ph3 = tile("3", color=C_RED, font_size=52)
        
        row_ph = VGroup(t_ph6, t_ph5, t_ph4, t_ph3).arrange(RIGHT, buff=0.6).move_to([0, 0.4, 0])
        brace_ph = Brace(row_ph, DOWN, color=C_RED)
        lbl_1000x = bold_txt("1,000×", font_size=56, color=C_RED).next_to(brace_ph, DOWN, buff=0.15)
        
        self.act(self.t, FadeIn(lbl_ph), FadeIn(row_ph), run_time=0.5)
        
        t_thousand = self.word_time("t32", "thousand", occurrence=1)
        self.act(t_thousand, Create(brace_ph), FadeIn(lbl_1000x, scale=1.2), run_time=0.4)
        
        # t33: "And sound. Every ten decibels means ten times more sound intensity. A whisper is about thirty decibels, a jet engine up close about one hundred forty..."
        t33_start = self.take_start("t33")
        self.hold_until(t33_start)
        self.act(self.t, FadeOut(lbl_ph), FadeOut(row_ph), FadeOut(brace_ph), FadeOut(lbl_1000x), run_time=0.3)
        
        lbl_sound = bold_txt("Sound", font_size=56, color=C_WHITE).move_to([-3.5, 2.4, 0])
        lbl_db = txt("decibels", font_size=36, color=C_GRAY).next_to(lbl_sound, DOWN, buff=0.1)
        
        # Vertical dB bar from 30 to 140 (lowered slightly so top is at y = 1.0, clear of headers)
        db_bar = Rectangle(width=0.6, height=3.8, fill_color="#222222", fill_opacity=0.9, stroke_color=C_WHITE).move_to([-3.5, -0.9, 0])
        
        m_30 = Line([-4.0, -2.4, 0], [-3.0, -2.4, 0], color=C_GREEN, stroke_width=4)
        lbl_30db = txt("30 dB", font_size=40, color=C_GREEN).next_to(m_30, LEFT, buff=0.2)
        
        m_140 = Line([-4.0, 0.7, 0], [-3.0, 0.7, 0], color=C_RED, stroke_width=4)
        lbl_140db = txt("140 dB", font_size=40, color=C_RED).next_to(m_140, LEFT, buff=0.2)
        
        # Step rule: +10 dB = ×10
        step_rule = bold_txt("+10 dB = ×10", font_size=46, color=C_GREEN).move_to([1.8, 1.2, 0])
        
        # 100,000,000,000x
        lbl_100b = bold_txt("100,000,000,000×", font_size=54, color=C_ORANGE).move_to([2.2, -0.9, 0])
        brace_sound = Brace(db_bar, RIGHT, color=C_ORANGE)
        
        self.act(self.t, FadeIn(lbl_sound), FadeIn(lbl_db), Create(db_bar), FadeIn(m_30), FadeIn(lbl_30db), FadeIn(m_140), FadeIn(lbl_140db), run_time=0.6)
        
        t_ten_db = self.word_time("t33", "ten", occurrence=1)
        self.act(t_ten_db, FadeIn(step_rule, shift=UP*0.2), run_time=0.3)
        
        t_hundred_b = self.word_time("t33", "hundred", occurrence=2) # "hundred billion"
        self.act(t_hundred_b, Create(brace_sound), FadeIn(lbl_100b, scale=1.2), run_time=0.4)
        
        # t34: "Same trick every time. A step on the ruler isn't adding. It's multiplying."
        t34_start = self.take_start("t34")
        self.hold_until(t34_start)
        self.act(self.t, *[FadeOut(m) for m in self.mobjects], run_time=0.3)
        
        # Montage: 3 mini-rulers
        r1 = ruler(length=8.0, is_log=True, color=C_BLUE).move_to([0, 1.5, 0])
        r2 = ruler(length=8.0, is_log=True, color=C_GREEN).move_to([0, 0.2, 0])
        r3 = ruler(length=8.0, is_log=True, color=C_RED).move_to([0, -1.1, 0])
        
        self.act(self.t, Create(r1), Create(r2), Create(r3), run_time=0.6)
        
        # Crossed out "+" and pulsing "×"
        plus_sym = bold_txt("+", font_size=80, color=C_GRAY).move_to([-3.0, -2.2, 0])
        cross_plus = Line(plus_sym.get_corner(UL), plus_sym.get_corner(DR), color=C_RED, stroke_width=5)
        
        mult_sym = bold_txt("×", font_size=90, color=C_BLUE).move_to([3.0, -2.2, 0])
        
        t_adding = self.word_time("t34", "adding", occurrence=1)
        self.act(t_adding, FadeIn(plus_sym), Create(cross_plus), run_time=0.3)
        
        t_mult_end = self.word_time("t34", "multiplying", occurrence=1)
        self.act(t_mult_end, FadeIn(mult_sym, scale=1.3), run_time=0.3)
        self.act(self.t, mult_sym.animate.scale(1.2), run_time=0.15)
        self.act(self.t, mult_sym.animate.scale(1/1.2), run_time=0.15)
        
        t34_end = self.take_end("t34")
        self.hold_until(t34_end - 0.4)
        self.act(self.t, *[FadeOut(m) for m in self.mobjects], run_time=0.4)
        
        self.finish()
