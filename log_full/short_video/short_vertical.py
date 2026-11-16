import json
import numpy as np
from pathlib import Path
from manim import *

root = Path(r"C:\Users\Asus\Downloads\log_full")
short_dir = root / "short_video"

with open(short_dir / "short_timing.json", "r", encoding="utf-8") as f:
    timing_data = json.load(f)

with open(short_dir / "short_words.json", "r", encoding="utf-8") as f:
    words_data = json.load(f)

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 8.0
config.frame_height = 14.222222
config.frame_rate = 30
config.background_color = "#000000"

C_BLUE = "#3B82F6"
C_YELLOW = "#F59E0B"
C_RED = "#EF4444"
C_GREEN = "#10B981"
C_WHITE = "#FFFFFF"
C_GRAY = "#94A3B8"
C_ORANGE = "#F97316"

def bold_txt(text, font_size=44, color=C_WHITE):
    return Text(text, font="Segoe UI", weight=BOLD, font_size=font_size, color=color)

def txt(text, font_size=36, color=C_WHITE):
    return Text(text, font="Segoe UI", font_size=font_size, color=color)

def tile(text, color=C_BLUE, text_color=C_WHITE, font_size=46, width=1.5, height=1.3):
    bg = RoundedRectangle(corner_radius=0.18, width=width, height=height, fill_color=color, fill_opacity=0.18, stroke_color=color, stroke_width=2.5)
    t = bold_txt(text, font_size=font_size, color=text_color).move_to(bg.get_center())
    return VGroup(bg, t)

def log_label(base, arg, font_size=60, color=C_WHITE, arg_color=C_WHITE):
    t_log = bold_txt("log", font_size=font_size, color=color)
    t_base = bold_txt(str(base), font_size=int(font_size * 0.6), color=C_BLUE)
    t_base.next_to(t_log, RIGHT + DOWN * 0.35, buff=0.04)
    t_arg = bold_txt(f"({arg})", font_size=font_size, color=arg_color)
    t_arg.next_to(t_base, RIGHT, buff=0.08).align_to(t_log, DOWN)
    return VGroup(t_log, t_base, t_arg)

class ShortVerticalExplainer(Scene):
    @property
    def t(self):
        return self.renderer.time
        
    def take_start(self, take_id):
        for tk in timing_data["takes"]:
            if tk["id"] == take_id:
                return float(tk["start_s"])
        return 0.0

    def word_time(self, take_id, word_str, occurrence=1):
        clean_w = word_str.strip().lower()
        cnt = 0
        for w in words_data:
            if w["take"] == take_id and clean_w in w["word"].lower():
                cnt += 1
                if cnt == occurrence:
                    return float(w["start_s"])
        return self.take_start(take_id)

    def hold_until(self, target_t):
        dt = target_t - self.t
        if dt > 0.001:
            self.wait(dt)

    def act(self, target_t, *anims, run_time=None):
        if target_t > self.t:
            self.hold_until(target_t)
        if anims:
            rt = run_time if run_time is not None else 0.4
            self.play(*anims, run_time=rt)

    def construct(self):
        # ----------------------------------------------------
        # st01: Moon Question (Vertical Layout)
        # ----------------------------------------------------
        q_title = bold_txt("Folds to reach\nthe Moon?", font_size=52, color=C_YELLOW).move_to([0, 4.4, 0])
        
        moon = Circle(radius=1.1, fill_color=C_GRAY, fill_opacity=0.9, stroke_color=C_WHITE, stroke_width=2.5).move_to([0, 2.2, 0])
        moon_lbl = bold_txt("Moon: 384,400 km", font_size=36, color=C_YELLOW).next_to(moon, DOWN, buff=0.2)
        
        paper = Rectangle(width=2.6, height=0.09, fill_color=C_WHITE, fill_opacity=1.0, stroke_width=0).move_to([0, -2.2, 0])
        paper_lbl = txt("0.1 mm paper", font_size=34, color=C_GRAY).next_to(paper, DOWN, buff=0.2)
        
        dist_line = DashedLine(paper.get_top(), moon_lbl.get_bottom(), dash_length=0.2, color=C_GRAY)
        
        self.act(self.take_start("st01"), FadeIn(q_title), FadeIn(moon), FadeIn(moon_lbl), FadeIn(paper), FadeIn(paper_lbl), Create(dist_line), run_time=0.6)
        
        # st02: Guess bubble
        guess = tile("Millions?", color=C_ORANGE, text_color=C_WHITE, font_size=50, width=3.4, height=1.3).move_to([0, -0.3, 0])
        strike = Line(guess.get_left() + LEFT*0.2, guess.get_right() + RIGHT*0.2, color=C_RED, stroke_width=6)
        
        t_guess = self.word_time("st02", "guess", occurrence=1)
        self.act(t_guess, FadeIn(guess, scale=1.15), run_time=0.35)
        
        t_small = self.word_time("st02", "small", occurrence=1)
        self.act(t_small, Create(strike), run_time=0.3)
        
        # ----------------------------------------------------
        # st03: Doublings 1->2, 2->4, 3->8
        # ----------------------------------------------------
        t_st03 = self.take_start("st03")
        self.hold_until(t_st03)
        self.act(self.t, *[FadeOut(m) for m in self.mobjects], run_time=0.3)
        
        title_doubling = bold_txt("Every fold doubles\nthe thickness", font_size=48, color=C_WHITE).move_to([0, 4.2, 0])
        self.act(self.t, FadeIn(title_doubling), run_time=0.3)
        
        row1 = VGroup(
            txt("1 fold", font_size=38, color=C_GRAY),
            bold_txt("→", font_size=42, color=C_GRAY),
            tile("2 layers", color=C_BLUE, font_size=40, width=2.4, height=1.1)
        ).arrange(RIGHT, buff=0.3).move_to([0, 2.0, 0])
        
        row2 = VGroup(
            txt("2 folds", font_size=38, color=C_GRAY),
            bold_txt("→", font_size=42, color=C_GRAY),
            tile("4 layers", color=C_BLUE, font_size=40, width=2.4, height=1.1)
        ).arrange(RIGHT, buff=0.3).move_to([0, 0.4, 0])
        
        row3 = VGroup(
            txt("3 folds", font_size=38, color=C_GRAY),
            bold_txt("→", font_size=42, color=C_GRAY),
            tile("8 layers", color=C_BLUE, font_size=40, width=2.4, height=1.1)
        ).arrange(RIGHT, buff=0.3).move_to([0, -1.2, 0])
        
        t_two = self.word_time("st03", "two", occurrence=2)
        self.act(t_two, FadeIn(row1, shift=UP*0.2), run_time=0.3)
        
        t_four = self.word_time("st03", "four", occurrence=1)
        self.act(t_four, FadeIn(row2, shift=UP*0.2), run_time=0.3)
        
        t_eight = self.word_time("st03", "eight", occurrence=1)
        self.act(t_eight, FadeIn(row3, shift=UP*0.2), run_time=0.3)
        
        # ----------------------------------------------------
        # st04: Log Definition
        # ----------------------------------------------------
        t_st04 = self.take_start("st04")
        self.hold_until(t_st04)
        self.act(self.t, *[FadeOut(m) for m in self.mobjects], run_time=0.3)
        
        log_def = bold_txt("A logarithm counts\ndoublings", font_size=50, color=C_YELLOW).move_to([0, 3.8, 0])
        
        tiles_8 = VGroup(
            tile("2", color=C_BLUE, font_size=44, width=1.1, height=1.1),
            bold_txt("×", font_size=40, color=C_WHITE),
            tile("2", color=C_BLUE, font_size=44, width=1.1, height=1.1),
            bold_txt("×", font_size=40, color=C_WHITE),
            tile("2", color=C_BLUE, font_size=44, width=1.1, height=1.1),
            bold_txt("=", font_size=40, color=C_WHITE),
            tile("8", color=C_GREEN, font_size=44, width=1.2, height=1.1)
        ).arrange(RIGHT, buff=0.18).move_to([0, 1.8, 0])
        
        bracket_lbl = txt("3 doublings", font_size=36, color=C_YELLOW).next_to(tiles_8, DOWN, buff=0.25)
        
        self.act(self.t, FadeIn(log_def), FadeIn(tiles_8), FadeIn(bracket_lbl), run_time=0.4)
        
        # st05: log2(8) = 3
        t_st05 = self.take_start("st05")
        self.hold_until(t_st05)
        
        eq_log2_8 = VGroup(
            log_label(2, 8, font_size=64),
            bold_txt(" = ", font_size=64, color=C_WHITE),
            bold_txt("3", font_size=64, color=C_YELLOW)
        ).arrange(RIGHT, buff=0.15).move_to([0, -0.6, 0])
        
        eq_note = txt("How many 2s multiply to 8?", font_size=34, color=C_GRAY).next_to(eq_log2_8, DOWN, buff=0.3)
        
        self.act(self.t, FadeIn(eq_log2_8, shift=UP*0.2), FadeIn(eq_note), run_time=0.4)
        
        # ----------------------------------------------------
        # st06: Moon Distance Target (3.8 Trillion Layers)
        # ----------------------------------------------------
        t_st06 = self.take_start("st06")
        self.hold_until(t_st06)
        self.act(self.t, *[FadeOut(m) for m in self.mobjects], run_time=0.3)
        
        moon_hdr = bold_txt("Moon: 384,400 km", font_size=48, color=C_YELLOW).move_to([0, 3.8, 0])
        target_intro = txt("Target to reach the Moon:", font_size=36, color=C_GRAY).move_to([0, 2.2, 0])
        trillion_lbl = bold_txt("≈ 3.8 Trillion\nLayers", font_size=60, color=C_WHITE).move_to([0, 0.6, 0])
        sub_layers = txt("from a 0.1 mm sheet of paper", font_size=34, color=C_GRAY).next_to(trillion_lbl, DOWN, buff=0.3)
        
        self.act(self.t, FadeIn(moon_hdr), FadeIn(target_intro), run_time=0.3)
        t_trillion = self.word_time("st06", "trillion", occurrence=1)
        self.act(t_trillion, FadeIn(trillion_lbl, scale=1.15), FadeIn(sub_layers), run_time=0.4)
        
        # ----------------------------------------------------
        # st07 - st09: The Fold Ladder
        # ----------------------------------------------------
        t_st07 = self.take_start("st07")
        self.hold_until(t_st07)
        self.act(self.t, *[FadeOut(m) for m in self.mobjects], run_time=0.3)
        
        ladder_title = bold_txt("Exponential Growth", font_size=46, color=C_YELLOW).move_to([0, 4.4, 0])
        self.act(self.t, FadeIn(ladder_title), run_time=0.25)
        
        ladder_data = [
            ("10 folds", "≈ 1,000 layers", "(10 cm)", 2.4),
            ("20 folds", "≈ 1,000,000", "(100 m)", 1.0),
            ("30 folds", "≈ 1,000,000,000", "(107 km)", -0.4),
            ("40 folds", "≈ 1 Trillion", "(110,000 km)", -1.8)
        ]
        ladder_rows = []
        for folds_txt, layers_txt, height_txt, y in ladder_data:
            card = VGroup(
                bold_txt(folds_txt, font_size=38, color=C_BLUE),
                bold_txt(layers_txt, font_size=36, color=C_WHITE),
                txt(height_txt, font_size=32, color=C_GRAY)
            ).arrange(RIGHT, buff=0.25).move_to([0, y, 0])
            ladder_rows.append(card)
            
        t_10 = self.word_time("st07", "ten", occurrence=1)
        self.act(t_10, FadeIn(ladder_rows[0], shift=UP*0.2), run_time=0.35)
        
        t_20 = self.word_time("st08", "twenty", occurrence=1)
        self.act(t_20, FadeIn(ladder_rows[1], shift=UP*0.2), run_time=0.35)
        
        t_30 = self.word_time("st08", "thirty", occurrence=1)
        self.act(t_30, FadeIn(ladder_rows[2], shift=UP*0.2), run_time=0.35)
        
        t_40 = self.word_time("st09", "forty", occurrence=1)
        self.act(t_40, FadeIn(ladder_rows[3], shift=UP*0.2), run_time=0.35)
        
        # ----------------------------------------------------
        # st10 & st11: Scale Comparison to Moon
        # ----------------------------------------------------
        t_st10 = self.take_start("st10")
        self.hold_until(t_st10)
        self.act(self.t, *[FadeOut(m) for m in self.mobjects], run_time=0.3)
        
        v_axis = Line([0, -3.2, 0], [0, 3.8, 0], color=C_GRAY, stroke_width=3)
        
        # Moon threshold line
        moon_line = DashedLine([-3.2, 1.4, 0], [3.2, 1.4, 0], dash_length=0.15, color=C_YELLOW, stroke_width=3.5)
        moon_text = bold_txt("🌕 Moon: 384,400 km", font_size=38, color=C_YELLOW).move_to([0, 1.9, 0])
        
        # 40 folds marker
        m40 = Line([-1.2, -1.8, 0], [1.2, -1.8, 0], color=C_RED, stroke_width=4.5)
        lbl40 = txt("40 folds: 110,000 km", font_size=32, color=C_RED).next_to(m40, DOWN, buff=0.12)
        
        # 41 folds marker
        m41 = Line([-1.2, -0.2, 0], [1.2, -0.2, 0], color=C_ORANGE, stroke_width=4.5)
        lbl41 = txt("41 folds: 220,000 km", font_size=32, color=C_ORANGE).next_to(m41, DOWN, buff=0.12)
        
        self.act(self.t, Create(v_axis), Create(moon_line), FadeIn(moon_text), FadeIn(m40), FadeIn(lbl40), run_time=0.5)
        
        self.act(self.t + 0.3, FadeIn(m41), FadeIn(lbl41), run_time=0.35)
        
        # st11: 42 folds jumps ABOVE the Moon line!
        t_st11 = self.take_start("st11")
        m42 = Line([-1.5, 2.7, 0], [1.5, 2.7, 0], color=C_GREEN, stroke_width=6)
        lbl42 = bold_txt("42 folds: 440,000 km!", font_size=36, color=C_GREEN).next_to(m42, UP, buff=0.15)
        tag42 = bold_txt("PAST THE MOON", font_size=30, color=C_WHITE).next_to(m42, DOWN, buff=0.12)
        
        self.act(t_st11, FadeIn(m42), FadeIn(lbl42), FadeIn(tag42), run_time=0.4)
        
        # ----------------------------------------------------
        # st12: Grand Conclusion
        # ----------------------------------------------------
        t_st12 = self.take_start("st12")
        self.hold_until(t_st12)
        self.act(self.t, *[FadeOut(m) for m in self.mobjects], run_time=0.3)
        
        grand_42 = bold_txt("42", font_size=170, color=C_YELLOW).move_to([0, 1.8, 0])
        grand_folds = bold_txt("FOLDS TO REACH\nTHE MOON", font_size=48, color=C_WHITE).move_to([0, 0.1, 0])
        grand_sub = txt("A logarithm counts the\nhidden steps of explosive growth.", font_size=34, color=C_GRAY).move_to([0, -1.8, 0])
        
        self.act(self.t, FadeIn(grand_42, scale=1.3), FadeIn(grand_folds), FadeIn(grand_sub), run_time=0.5)
        self.act(self.t + 0.1, grand_42.animate.scale(1.1), run_time=0.2)
        self.act(self.t, grand_42.animate.scale(1/1.1), run_time=0.2)
        
        final_total_s = float(timing_data["final_total_s"])
        self.hold_until(final_total_s)
