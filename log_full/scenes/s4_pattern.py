from manim import *
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from common import (
    VoiceScene, C_YELLOW, C_BLUE, C_GREEN, C_RED, C_ORANGE, C_WHITE, C_GRAY,
    C_DARK_GRAY, C_BROWN, txt, bold_txt, log_label, tile, ruler, bar_chart
)

class S4Pattern(VoiceScene):
    section_id = "S4_PATTERN"

    def construct(self):
        # t22: "Now here's something strange... Look at just the first digit of each one."
        t22_start = self.take_start("t22")
        self.hold_until(t22_start)
        
        # Grid of numbers: 8,336,817 / 6,650 / 19.99 / 1,412,600
        num_strs = ["8,336,817", "6,650", "19.99", "1,412,600", "73,200", "285", "4,190", "91,400"]
        grid_mobs = []
        for i, ns in enumerate(num_strs):
            first_char = bold_txt(ns[0], font_size=56, color=C_WHITE)
            rest_chars = bold_txt(ns[1:], font_size=56, color=C_WHITE)
            rest_chars.next_to(first_char, RIGHT, buff=0.05)
            row = VGroup(first_char, rest_chars)
            grid_mobs.append(row)
            
        grid = VGroup(*grid_mobs).arrange_in_grid(rows=4, cols=2, buff=(1.5, 0.4)).move_to([0, 0.5, 0])
        self.act(self.t, FadeIn(grid, shift=UP*0.3), run_time=0.5)
        
        # Highlight first digits yellow at "first digit"
        t_digit = self.word_time("t22", "digit", occurrence=1)
        anim_hl = [g[0].animate.set_color(C_YELLOW).scale(1.15) for g in grid_mobs]
        self.act(t_digit, *anim_hl, run_time=0.4)
        
        # t23: "You'd expect the digits one through nine to show up about equally, roughly eleven percent each."
        t23_start = self.take_start("t23")
        self.hold_until(t23_start)
        self.act(self.t, FadeOut(grid), run_time=0.3)
        
        # Uniform 11.1% bar chart: 1..9
        equal_vals = [11.1] * 9
        labels_1_9 = [str(i) for i in range(1, 10)]
        chart_equal = bar_chart(equal_vals, labels_1_9, width=9.0, height=3.2, bar_color=C_GRAY).move_to([0, -0.4, 0])
        lbl_11 = bold_txt("11%", font_size=56, color=C_WHITE).move_to([0, 2.0, 0])
        
        self.act(self.t, FadeIn(chart_equal), FadeIn(lbl_11), run_time=0.5)
        
        # t24: "But they don't. The digit one leads about thirty percent of the time. The digit nine? Under five."
        t24_start = self.take_start("t24")
        self.hold_until(t24_start)
        
        # Morph to Benford heights: [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]
        benford_vals = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]
        benford_colors = [C_YELLOW] + [C_BLUE] * 7 + [C_RED]
        chart_benford = bar_chart(benford_vals, labels_1_9, width=9.0, height=3.5, bar_color=benford_colors).move_to([0, -0.4, 0])
        
        lbl_30 = bold_txt("30%", font_size=56, color=C_YELLOW).next_to(chart_benford[0][0], UP, buff=0.15)
        lbl_under5 = bold_txt("under 5%", font_size=46, color=C_RED).next_to(chart_benford[0][8], UP, buff=0.15)
        
        self.act(self.t, Transform(chart_equal, chart_benford), FadeOut(lbl_11), run_time=0.8)
        
        t_one_lead = self.word_time("t24", "one", occurrence=1)
        self.act(t_one_lead, FadeIn(lbl_30, scale=1.2), run_time=0.3)
        
        t_nine = self.word_time("t24", "nine", occurrence=1)
        self.act(t_nine, FadeIn(lbl_under5, scale=1.2), run_time=0.3)
        
        # t25: "In 1881, an astronomer named Simon Newcomb... first pages were far more worn than the last."
        t25_start = self.take_start("t25")
        self.hold_until(t25_start)
        self.act(self.t, FadeOut(chart_equal), FadeOut(lbl_30), FadeOut(lbl_under5), run_time=0.3)
        
        t_1881 = bold_txt("1881", font_size=90, color=C_YELLOW).move_to([-3.5, 2.2, 0])
        t_newcomb = bold_txt("Simon Newcomb", font_size=60, color=C_WHITE).move_to([1.5, 2.2, 0])
        
        # Primitive open book shifted slightly left to give room for log label
        spine = Rectangle(width=0.4, height=3.2, fill_color="#333333", fill_opacity=1.0, stroke_color=C_GRAY).move_to([-0.8, -0.2, 0])
        left_page_worn = Rectangle(width=3.0, height=3.0, fill_color=C_BROWN, fill_opacity=0.85, stroke_color=C_GRAY).next_to(spine, LEFT, buff=0)
        right_page_clean = Rectangle(width=3.0, height=3.0, fill_color=C_WHITE, fill_opacity=0.9, stroke_color=C_GRAY).next_to(spine, RIGHT, buff=0)
        book_lbl = txt("logarithm tables", font_size=42, color=C_WHITE).next_to(spine, DOWN, buff=0.4)
        book = VGroup(left_page_worn, spine, right_page_clean, book_lbl)
        
        self.act(self.t, FadeIn(t_1881), FadeIn(t_newcomb), FadeIn(book), run_time=0.5)
        
        # t26: "He guessed that people were looking up numbers starting with one far more often. And the reason is hiding in a log."
        t26_start = self.take_start("t26")
        self.hold_until(t26_start)
        
        # Arrow points to early worn pages
        pointer = Arrow([-3.6, 1.0, 0], [-2.5, 0.2, 0], color=C_YELLOW, stroke_width=5)
        self.act(self.t, FadeIn(pointer), run_time=0.2)
        self.act(self.t, pointer.animate.shift(DOWN*0.2 + RIGHT*0.1), run_time=0.2)
        self.act(self.t, pointer.animate.shift(UP*0.2 + LEFT*0.1), run_time=0.2)
        
        t_log_glow = self.word_time("t26", "log", occurrence=1)
        glow_log = bold_txt("log", font_size=96, color=C_YELLOW).move_to([4.2, -0.2, 0])
        self.act(t_log_glow, FadeIn(glow_log, scale=1.3), run_time=0.35)
        self.act(self.t, glow_log.animate.scale(1.1), run_time=0.2)
        self.act(self.t, glow_log.animate.scale(1/1.1), run_time=0.2)
        
        # t27: "Picture a log ruler... from one to two takes up about thirty percent... from nine to ten? Under five percent."
        t27_start = self.take_start("t27")
        self.hold_until(t27_start)
        self.act(self.t, FadeOut(t_1881), FadeOut(t_newcomb), FadeOut(book), FadeOut(pointer), FadeOut(glow_log), run_time=0.3)
        
        log_r = ruler(length=11.0, ticks=10, is_log=True, color=C_WHITE).move_to([0, 0.4, 0])
        r_title = bold_txt("log ruler", font_size=56, color=C_WHITE).next_to(log_r, UP, buff=0.6)
        
        self.act(self.t, Create(log_r), FadeIn(r_title), run_time=0.6)
        
        # Highlight 1->2 (30.1% of length)
        x_1 = -5.5 + np.log10(1) * 11.0 # -5.5
        x_2 = -5.5 + np.log10(2) * 11.0 # -5.5 + 3.31 = -2.19
        seg_1_2 = Line([x_1, 0.4, 0], [x_2, 0.4, 0], color=C_YELLOW, stroke_width=8)
        brace_1_2 = Brace(seg_1_2, UP, color=C_YELLOW)
        lbl_30_r = bold_txt("30%", font_size=48, color=C_YELLOW).next_to(brace_1_2, UP, buff=0.1)
        
        t_one_two = self.word_time("t27", "one", occurrence=2)
        self.act(t_one_two, Create(seg_1_2), Create(brace_1_2), FadeIn(lbl_30_r), run_time=0.4)
        
        # Highlight 9->10 (4.6% of length)
        x_9 = -5.5 + np.log10(9) * 11.0
        x_10 = -5.5 + np.log10(10) * 11.0 # 5.5
        seg_9_10 = Line([x_9, 0.4, 0], [x_10, 0.4, 0], color=C_RED, stroke_width=8)
        brace_9_10 = Brace(seg_9_10, UP, color=C_RED)
        lbl_under5_r = bold_txt("under 5%", font_size=40, color=C_RED).next_to(brace_9_10, UP, buff=0.1)
        
        t_nine_ten = self.word_time("t27", "nine", occurrence=1)
        self.act(t_nine_ten, Create(seg_9_10), Create(brace_9_10), FadeIn(lbl_under5_r), run_time=0.4)
        
        # t28: "Think of something growing by a steady percentage each year. Going from a thousand to two thousand takes more than six times as long..."
        t28_start = self.take_start("t28")
        self.hold_until(t28_start)
        self.act(self.t,
            FadeOut(log_r), FadeOut(r_title),
            FadeOut(seg_1_2), FadeOut(brace_1_2), FadeOut(lbl_30_r),
            FadeOut(seg_9_10), FadeOut(brace_9_10), FadeOut(lbl_under5_r),
            run_time=0.3
        )
        
        # Steady growth curve
        axes_growth = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 11000, 2000],
            x_length=7.0,
            y_length=4.5,
            axis_config={"color": C_GRAY},
            tips=True
        ).move_to([-1.5, 0.4, 0])
        
        curve_g = axes_growth.plot(lambda t: 1000 * np.exp(0.24 * t), x_range=[0, 9.6], color=C_GREEN, stroke_width=6)
        
        # Time bars: 1000 -> 2000 vs 9000 -> 10000
        # log(2)/0.24 = 2.89 units long; log(10/9)/0.24 = 0.44 units long (ratio 6.58x)
        bar_long = Rectangle(width=3.6, height=0.4, fill_color=C_GREEN, fill_opacity=0.8, stroke_color=C_WHITE).move_to([3.8, 1.8, 0])
        lbl_long = txt("1,000 → 2,000", font_size=36, color=C_WHITE).next_to(bar_long, UP, buff=0.12)
        
        lbl_6x = bold_txt("≈ 6.6×", font_size=52, color=C_GREEN).move_to([3.8, 0.75, 0])
        
        bar_short = Rectangle(width=0.55, height=0.4, fill_color=C_ORANGE, fill_opacity=0.8, stroke_color=C_WHITE).move_to([3.8, -0.6, 0])
        lbl_short = txt("9,000 → 10,000", font_size=36, color=C_WHITE).next_to(bar_short, UP, buff=0.12)
        
        self.act(self.t, Create(axes_growth), Create(curve_g), run_time=0.8)
        self.act(self.t, FadeIn(bar_long), FadeIn(lbl_long), FadeIn(bar_short), FadeIn(lbl_short), run_time=0.5)
        
        t_six_times = self.word_time("t28", "six", occurrence=1)
        self.act(t_six_times, FadeIn(lbl_6x, scale=1.2), run_time=0.4)
        
        # t29: "Auditors use this to spot fake data... it can't prove fraud. It just raises a flag."
        t29_start = self.take_start("t29")
        self.hold_until(t29_start)
        self.act(self.t,
            FadeOut(axes_growth), FadeOut(curve_g),
            FadeOut(bar_long), FadeOut(lbl_long), FadeOut(bar_short), FadeOut(lbl_short), FadeOut(lbl_6x),
            run_time=0.3
        )
        
        # Two side by side charts
        chart_real = bar_chart(benford_vals, labels_1_9, width=4.8, height=2.8, bar_color=C_YELLOW).move_to([-3.4, 0, 0])
        lbl_real = bold_txt("real data", font_size=48, color=C_WHITE).next_to(chart_real, UP, buff=0.3)
        
        fake_vals = [12, 11, 10, 11, 12, 10, 11, 12, 11]
        chart_fake = bar_chart(fake_vals, labels_1_9, width=4.8, height=2.8, bar_color=C_GRAY).move_to([3.4, 0, 0])
        lbl_fake = bold_txt("invented data", font_size=48, color=C_WHITE).next_to(chart_fake, UP, buff=0.3)
        
        # Red flag icon on right
        flag_p = Line(DOWN*0.5, UP*1.0, color=C_WHITE, stroke_width=4)
        flag_t = Polygon([0, 1.0, 0], [0.9, 0.7, 0], [0, 0.4, 0], fill_color=C_RED, fill_opacity=1.0, stroke_width=0)
        red_flag = VGroup(flag_p, flag_t).next_to(chart_fake, RIGHT, buff=0.1).shift(UP*1.0)
        
        lbl_flag_not_proof = bold_txt("a flag, not proof", font_size=56, color=C_WHITE).move_to([0, -2.2, 0])
        
        self.act(self.t, FadeIn(chart_real), FadeIn(lbl_real), FadeIn(chart_fake), FadeIn(lbl_fake), run_time=0.6)
        
        t_flag = self.word_time("t29", "flag", occurrence=1)
        self.act(t_flag, FadeIn(red_flag, shift=DOWN*0.3), FadeIn(lbl_flag_not_proof), run_time=0.4)
        
        t29_end = self.take_end("t29")
        self.hold_until(t29_end - 0.4)
        self.act(self.t, *[FadeOut(m) for m in self.mobjects], run_time=0.4)
        
        self.finish()
