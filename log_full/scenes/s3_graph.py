from manim import *
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from common import (
    VoiceScene, C_YELLOW, C_BLUE, C_GREEN, C_RED, C_ORANGE, C_WHITE, C_GRAY,
    C_DARK_GRAY, txt, bold_txt, log_label, pow_label, tile
)

class S3Graph(VoiceScene):
    section_id = "S3_GRAPH"

    def construct(self):
        # t16: "Let's draw it. Folds along the bottom, layers up the side..."
        # Axes square: [0,8,1] x [0,8,1], length 5.8
        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 8, 1],
            x_length=5.6,
            y_length=5.6,
            axis_config={"color": C_GRAY, "stroke_width": 3},
            tips=True
        ).move_to([-1.2, 0.4, 0])
        
        lbl_x = txt("folds", font_size=38, color=C_WHITE).next_to(axes.x_axis.get_right(), RIGHT, buff=0.25)
        lbl_y = txt("layers", font_size=38, color=C_WHITE).next_to(axes.y_axis.get_top(), UP, buff=0.25)
        
        # Custom ticks
        x_ticks = VGroup(*[txt(str(x), font_size=36, color=C_GRAY).next_to(axes.c2p(x, 0), DOWN, buff=0.15) for x in [0, 1, 2, 3]])
        y_ticks = VGroup(*[txt(str(y), font_size=36, color=C_GRAY).next_to(axes.c2p(0, y), LEFT, buff=0.15) for y in [1, 2, 4, 8]])
        
        self.act(self.take_start("t16"), Create(axes), FadeIn(lbl_x), FadeIn(lbl_y), FadeIn(x_ticks), FadeIn(y_ticks), run_time=0.6)
        
        # Plot y = 2^x for x in [0, 3] (blue, stroke 8)
        exp_curve = axes.plot(lambda x: 2**x, x_range=[0, 3], color=C_BLUE, stroke_width=7)
        
        dots_exp = VGroup(*[Dot(axes.c2p(x, 2**x), color=C_BLUE, radius=0.1) for x in [0, 1, 2, 3]])
        
        self.act(self.t, Create(exp_curve), run_time=2.2)
        for dot in dots_exp:
            self.add(dot)
            
        t_exp_lbl = self.word_time("t16", "exponential", occurrence=1)
        exp_growth_lbl = bold_txt("exponential growth", font_size=46, color=C_WHITE).move_to([4.0, 2.0, 0])
        self.act(t_exp_lbl, FadeIn(exp_growth_lbl, shift=LEFT*0.2), run_time=0.4)
        
        # t17: "Now swap the axes... This is the graph of a log."
        t17_start = self.take_start("t17")
        self.hold_until(t17_start)
        
        # Swap axes labels
        new_lbl_x = txt("layers", font_size=38, color=C_WHITE).next_to(axes.x_axis.get_right(), RIGHT, buff=0.25)
        new_lbl_y = txt("folds", font_size=38, color=C_WHITE).next_to(axes.y_axis.get_top(), UP, buff=0.25)
        diag = DashedLine(axes.c2p(0, 0), axes.c2p(8, 8), dash_length=0.15, color=C_GRAY)
        
        self.act(self.t,
            Transform(lbl_x, new_lbl_x),
            Transform(lbl_y, new_lbl_y),
            FadeOut(exp_growth_lbl),
            Create(diag),
            run_time=0.6
        )
        
        # Reflect curve into yellow curve: y = log2(x) for x in [1, 8]
        log_curve = axes.plot(lambda x: np.log2(x), x_range=[1, 8], color=C_YELLOW, stroke_width=7)
        
        log_graph_lbl = log_label(2, "x", font_size=64, color=C_YELLOW, arg_color=C_YELLOW).move_to([3.8, 1.0, 0])
        
        self.act(self.t, Transform(exp_curve.copy(), log_curve), run_time=1.5)
        self.add(log_curve)
        self.act(self.t, FadeIn(log_graph_lbl), run_time=0.4)
        
        # t18: "Watch how it behaves. It shoots up at first, then flattens. And every time the number doubles, the log goes up by exactly one."
        t18_start = self.take_start("t18")
        self.hold_until(t18_start)
        
        # Tracer dot runs along yellow curve
        tracer_dot = Dot(axes.c2p(1, 0), color=C_YELLOW, radius=0.12)
        self.add(tracer_dot)
        self.act(self.t, MoveAlongPath(tracer_dot, log_curve), run_time=2.5)
        
        t_one = self.word_time("t18", "one", occurrence=1)
        plus_one = bold_txt("+1", font_size=50, color=C_GREEN).next_to(axes.c2p(0, 1), LEFT, buff=0.45)
        self.act(t_one, FadeIn(plus_one, scale=1.3), run_time=0.3)
        
        # t19: "One to two, one step. Two to four... Eight to sixteen, one more."
        t19_start = self.take_start("t19")
        self.hold_until(t19_start)
        
        self.act(self.t, FadeOut(axes), FadeOut(lbl_x), FadeOut(lbl_y), FadeOut(x_ticks), FadeOut(y_ticks),
                 FadeOut(diag), FadeOut(log_curve), FadeOut(exp_curve), FadeOut(log_graph_lbl),
                 FadeOut(tracer_dot), FadeOut(plus_one), FadeOut(dots_exp),
                 run_time=0.3)
        
        # Rescaled axes [0, 17, 4], y [0, 5, 1]
        axes_16 = Axes(
            x_range=[0, 18, 2],
            y_range=[0, 5, 1],
            x_length=6.5,
            y_length=5.0,
            axis_config={"color": C_GRAY, "stroke_width": 3},
            tips=True
        ).move_to([-1.0, 0.4, 0])
        
        curve_16 = axes_16.plot(lambda x: np.log2(x), x_range=[1, 16], color=C_YELLOW, stroke_width=6)
        lbl_layers16 = txt("layers", font_size=38, color=C_WHITE).next_to(axes_16.x_axis.get_right(), RIGHT, buff=0.25)
        lbl_folds16 = txt("folds", font_size=38, color=C_WHITE).next_to(axes_16.y_axis.get_top(), UP, buff=0.25)
        
        self.act(self.t, Create(axes_16), Create(curve_16), FadeIn(lbl_layers16), FadeIn(lbl_folds16), run_time=0.5)
        
        # Steps 1->2, 2->4, 4->8, 8->16
        step_pts = [(1, 0), (2, 1), (4, 2), (8, 3), (16, 4)]
        step_dots = [Dot(axes_16.c2p(x, y), color=C_YELLOW, radius=0.1) for x, y in step_pts]
        for d in step_dots:
            self.add(d)
            
        pairs = [(1, 2), (2, 4), (4, 8), (8, 16)]
        for idx, (x1, x2) in enumerate(pairs):
            y1 = np.log2(x1)
            y2 = np.log2(x2)
            step_lbl = VGroup(
                bold_txt("×2", font_size=38, color=C_BLUE).next_to(axes_16.c2p((x1+x2)/2, 0), DOWN, buff=0.1),
                bold_txt("+1", font_size=38, color=C_GREEN).next_to(axes_16.c2p(0, (y1+y2)/2), LEFT, buff=0.1)
            )
            self.act(self.t, FadeIn(step_lbl), run_time=0.35)
            self.step(0.4)
            
        # t20: "It never stops climbing... one to a million... about twenty."
        t20_start = self.take_start("t20")
        self.hold_until(t20_start)
        
        self.act(self.t, *[FadeOut(m) for m in self.mobjects], run_time=0.3)
        
        # Big axes for 1 to 1,000,000 -> log up to 22
        axes_mil = Axes(
            x_range=[0, 1000000, 200000],
            y_range=[0, 24, 4],
            x_length=7.5,
            y_length=5.0,
            axis_config={"color": C_GRAY, "stroke_width": 3},
            tips=True
        ).move_to([-1.2, 0.4, 0])
        
        # Parametric curve: x = 2^u, y = u for u in [0, 19.93]
        u_vals = np.linspace(0, 19.93, 200)
        curve_pts = [axes_mil.c2p(2**u, u) for u in u_vals]
        mil_curve = VMobject(color=C_YELLOW, stroke_width=6).set_points_smoothly(curve_pts)
        
        lbl_mil_x = txt("1,000,000", font_size=38, color=C_WHITE).next_to(axes_mil.c2p(1000000, 0), DOWN, buff=0.2)
        lbl_mil_y = txt("20", font_size=38, color=C_WHITE).next_to(axes_mil.c2p(0, 20), LEFT, buff=0.2)
        
        d16 = Dot(axes_mil.c2p(16, 4), color=C_YELLOW, radius=0.08)
        lbl16 = txt("16 → 4", font_size=34, color=C_WHITE).next_to(d16, RIGHT, buff=0.25)
        
        d1024 = Dot(axes_mil.c2p(1024, 10), color=C_YELLOW, radius=0.08)
        lbl1024 = txt("1,024 → 10", font_size=34, color=C_WHITE).next_to(d1024, RIGHT, buff=0.25)
        
        dmil = Dot(axes_mil.c2p(1000000, 19.93), color=C_YELLOW, radius=0.12)
        lbl_mil = bold_txt("1,000,000 → ≈ 20", font_size=40, color=C_YELLOW).next_to(dmil, LEFT, buff=0.25)
        
        self.act(self.t, Create(axes_mil), FadeIn(lbl_mil_x), FadeIn(lbl_mil_y), Create(mil_curve), run_time=0.8)
        self.act(self.t, FadeIn(d16), FadeIn(lbl16), FadeIn(d1024), FadeIn(lbl1024), run_time=0.4)
        
        t_twenty = self.word_time("t20", "twenty", occurrence=1)
        self.act(t_twenty, FadeIn(dmil), FadeIn(lbl_mil), dmil.animate.scale(1.3), run_time=0.4)
        self.act(self.t, dmil.animate.scale(1/1.3), run_time=0.2)
        
        # t21: "The two curves are mirror images across a diagonal line. A log is the undo button for an exponent."
        t21_start = self.take_start("t21")
        self.hold_until(t21_start)
        self.act(self.t, *[FadeOut(m) for m in self.mobjects], run_time=0.3)
        
        # Back to square axes [0, 8]
        sq_axes = Axes(x_range=[0, 8, 1], y_range=[0, 8, 1], x_length=5.6, y_length=5.6, axis_config={"color": C_GRAY}, tips=True).move_to([-1.0, 0.4, 0])
        sq_diag = DashedLine(sq_axes.c2p(0, 0), sq_axes.c2p(8, 8), color=C_GRAY)
        c_exp = sq_axes.plot(lambda x: 2**x, x_range=[0, 3], color=C_BLUE, stroke_width=6)
        c_log = sq_axes.plot(lambda x: np.log2(x), x_range=[1, 8], color=C_YELLOW, stroke_width=6)
        
        self.act(self.t, Create(sq_axes), Create(sq_diag), Create(c_exp), Create(c_log), run_time=0.6)
        
        # "undo" button with curved arrow
        undo_lbl = bold_txt("undo", font_size=72, color=C_WHITE).move_to([4.0, 0.5, 0])
        undo_arrow = CurvedArrow(sq_axes.c2p(4, 2), sq_axes.c2p(2, 4), color=C_YELLOW, stroke_width=4)
        
        t_undo = self.word_time("t21", "undo", occurrence=1)
        self.act(t_undo, FadeIn(undo_lbl), Create(undo_arrow), run_time=0.5)
        
        t21_end = self.take_end("t21")
        self.hold_until(t21_end - 0.4)
        self.act(self.t, *[FadeOut(m) for m in self.mobjects], run_time=0.4)
        
        self.finish()
