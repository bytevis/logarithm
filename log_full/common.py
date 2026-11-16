from manim import *
import json
import os
import sys
from pathlib import Path
import numpy as np

# Configure 1080p 30fps black background
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30
config.background_color = "#000000"

# Color constants per storyboard
C_YELLOW = "#FADB14"   # The log value / answer / key highlight
C_BLUE = "#1890FF"     # Base 2, "x2" doubling marks, paper layers
C_GREEN = "#52C41A"    # Results, "+1", "x10"
C_RED = "#F5222D"      # The huge-number side
C_ORANGE = "#FA8C16"   # The huge-number side / chips
C_WHITE = "#FFFFFF"    # Normal text
C_GRAY = "#8C8C8C"     # Minor / helper
C_DARK_GRAY = "#262626"
C_BROWN = "#6B5B45"    # Worn book pages

FONT_NAME = "Segoe UI"
FALLBACK_FONT = "Arial"

def get_font():
    return FONT_NAME

def txt(text, font_size=48, color=C_WHITE, weight=NORMAL):
    return Text(str(text), font=get_font(), font_size=font_size, color=color, weight=weight)

def bold_txt(text, font_size=56, color=C_WHITE):
    return Text(str(text), font=get_font(), font_size=font_size, color=color, weight=BOLD)

def log_label(base, arg, font_size=72, color=C_WHITE, base_color=C_BLUE, arg_color=C_WHITE):
    log_t = txt("log", font_size=font_size, color=color, weight=BOLD)
    base_t = txt(str(base), font_size=int(font_size * 0.55), color=base_color, weight=BOLD)
    base_t.next_to(log_t, RIGHT, buff=0.08)
    base_t.align_to(log_t, DOWN).shift(DOWN * 0.12 * (font_size / 72.0))
    arg_t = txt(f"({arg})" if "(" not in str(arg) and str(arg) != "x" else f"({arg})", font_size=font_size, color=arg_color, weight=BOLD)
    arg_t.next_to(base_t, RIGHT, buff=0.1)
    arg_t.align_to(log_t, UP)
    grp = VGroup(log_t, base_t, arg_t)
    return grp

def pow_label(base, exp, font_size=72, color=C_BLUE, exp_color=C_YELLOW):
    base_t = txt(str(base), font_size=font_size, color=color, weight=BOLD)
    exp_t = txt(str(exp), font_size=int(font_size * 0.55), color=exp_color, weight=BOLD)
    exp_t.next_to(base_t, RIGHT, buff=0.06)
    exp_t.align_to(base_t, UP).shift(UP * 0.1 * (font_size / 72.0))
    return VGroup(base_t, exp_t)

def tile(text, color=C_BLUE, text_color=C_WHITE, font_size=56, width=None, height=1.0, corner_radius=0.15):
    t_obj = bold_txt(text, font_size=font_size, color=text_color)
    w = max(width or 0.0, t_obj.width + 0.4)
    h = max(height, t_obj.height + 0.3)
    bg = RoundedRectangle(corner_radius=corner_radius, width=w, height=h, fill_color=color, fill_opacity=0.25, stroke_color=color, stroke_width=3)
    t_obj.move_to(bg.get_center())
    grp = VGroup(bg, t_obj)
    grp.bg = bg
    grp.text = t_obj
    return grp

class MoonIcon(VGroup):
    def __init__(self, radius=0.8, **kwargs):
        super().__init__(**kwargs)
        moon = Circle(radius=radius, color=C_GRAY, fill_color="#CCCCCC", fill_opacity=0.9, stroke_width=2)
        c1 = Circle(radius=radius * 0.22, color="#999999", fill_color="#999999", fill_opacity=1.0, stroke_width=0)
        c1.move_to(moon.get_center() + np.array([-radius * 0.3, radius * 0.25, 0]))
        c2 = Circle(radius=radius * 0.15, color="#888888", fill_color="#888888", fill_opacity=1.0, stroke_width=0)
        c2.move_to(moon.get_center() + np.array([radius * 0.25, -radius * 0.2, 0]))
        c3 = Circle(radius=radius * 0.18, color="#AAAAAA", fill_color="#AAAAAA", fill_opacity=1.0, stroke_width=0)
        c3.move_to(moon.get_center() + np.array([radius * 0.3, radius * 0.3, 0]))
        self.add(moon, c1, c2, c3)

class PaperStack(VGroup):
    def __init__(self, n_layers=1, width=2.0, height=0.1, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.n_layers = n_layers
        self.layers_group = VGroup()
        self.add(self.layers_group)
        self.update_layers(n_layers, height)

    def update_layers(self, n, height=0.1):
        self.layers_group.submobjects = []
        clamped_n = min(n, 32)
        layer_h = max(0.04, min(height / max(1, clamped_n), 0.2))
        for i in range(clamped_n):
            rect = Rectangle(
                width=self.width,
                height=layer_h,
                fill_color=C_BLUE,
                fill_opacity=0.8,
                stroke_color=C_WHITE,
                stroke_width=1.5
            )
            rect.shift(UP * (i * layer_h))
            self.layers_group.add(rect)

def ruler(length=11.0, ticks=10, is_log=False, color=C_WHITE):
    line = Line(LEFT * (length / 2), RIGHT * (length / 2), stroke_color=color, stroke_width=3)
    t_group = VGroup()
    labels_group = VGroup()
    for i in range(1, 11):
        if is_log:
            pos_factor = np.log10(i) # 0 to 1
        else:
            pos_factor = (i - 1) / 9.0
        x = -length / 2 + pos_factor * length
        tick_line = Line(UP * 0.15, DOWN * 0.15, stroke_color=color, stroke_width=2.5).shift(RIGHT * x)
        f_sz = 32 if (is_log and i >= 8) else 38
        b_val = 0.38 if (is_log and i == 9) else 0.12
        lbl = txt(str(i), font_size=f_sz, color=color).next_to(tick_line, DOWN, buff=b_val)
        t_group.add(tick_line)
        labels_group.add(lbl)
    return VGroup(line, t_group, labels_group)

def bar_chart(values, labels, width=8.0, height=3.5, bar_color=C_GRAY):
    n = len(values)
    bar_w = (width / n) * 0.65
    spacing = width / n
    bars = VGroup()
    lbls = VGroup()
    start_x = -width / 2 + spacing / 2
    max_val = max(values) if max(values) > 0 else 1.0
    for i, (v, lbl) in enumerate(zip(values, labels)):
        bh = max(0.08, (v / max_val) * height)
        x = start_x + i * spacing
        rect = Rectangle(
            width=bar_w,
            height=bh,
            fill_color=bar_color if not isinstance(bar_color, list) else bar_color[i],
            fill_opacity=0.85,
            stroke_color=C_WHITE,
            stroke_width=1.5
        )
        rect.move_to(np.array([x, bh / 2, 0]))
        b_lbl = txt(str(lbl), font_size=38, color=C_WHITE).next_to(rect, DOWN, buff=0.12)
        bars.add(rect)
        lbls.add(b_lbl)
    return VGroup(bars, lbls)


class VoiceScene(Scene):
    section_id = "S1_HOOK"

    def setup(self):
        super().setup()
        root = Path(r"C:\Users\Asus\Downloads\log_full")
        timing_path = Path(os.environ.get("TIMING_JSON", root / "voice" / "timing.json"))
        words_path = Path(root / "out" / "words" / "full.json")

        with open(timing_path, "r", encoding="utf-8") as f:
            self.timing = json.load(f)

        self.words_data = []
        if words_path.exists():
            with open(words_path, "r", encoding="utf-8") as f:
                self.words_data = json.load(f)

        self.section_data = None
        for s in self.timing["sections"]:
            if s["id"] == self.section_id:
                self.section_data = s
                break

        if not self.section_data:
            raise ValueError(f"Section {self.section_id} not found in timing.json")

        self.section_start = float(self.section_data["start_s"])
        self.section_end = float(self.section_data["end_s"])

        # Frame exact boundaries: b[i] = round(section_start_s * 30) / 30
        self.b_start = round(self.section_start * 30) / 30.0
        self.b_end = round(self.section_end * 30) / 30.0
        self.target_duration = self.b_end - self.b_start

        self.take_map = {t["id"]: t for t in self.section_data["takes"]}

    @property
    def t(self):
        return self.section_start + self.renderer.time

    def take_start(self, take_id):
        if take_id in self.take_map:
            return float(self.take_map[take_id]["start_s"])
        for s in self.timing["sections"]:
            for t in s["takes"]:
                if t["id"] == take_id:
                    return float(t["start_s"])
        raise KeyError(f"Take {take_id} not found")

    def take_speech_end(self, take_id):
        if take_id in self.take_map:
            return float(self.take_map[take_id]["speech_end_s"])
        for s in self.timing["sections"]:
            for t in s["takes"]:
                if t["id"] == take_id:
                    return float(t["speech_end_s"])
        raise KeyError(f"Take {take_id} not found")

    def take_end(self, take_id):
        if take_id in self.take_map:
            return float(self.take_map[take_id]["end_s"])
        for s in self.timing["sections"]:
            for t in s["takes"]:
                if t["id"] == take_id:
                    return float(t["end_s"])
        raise KeyError(f"Take {take_id} not found")

    def word_time(self, take_id, word, occurrence=1):
        clean_target = word.strip().lower()
        count = 0
        for w in self.words_data:
            if w["take"] == take_id:
                w_clean = "".join(c for c in w["word"].lower() if c.isalnum())
                if w_clean == clean_target or clean_target in w_clean:
                    count += 1
                    if count == occurrence:
                        return float(w["start_s"])
        return self.take_start(take_id)

    def hold_until(self, target_t):
        target_t = float(target_t)
        dt = target_t - self.t
        if dt > 1e-4:
            self.wait(dt)

    def act(self, target_t, *animations, run_time=None):
        if target_t is not None:
            self.hold_until(target_t)
        if run_time is not None:
            self.play(*animations, run_time=run_time)
        else:
            self.play(*animations)

    def step(self, dt):
        dt = float(dt)
        if dt > 1e-4:
            self.wait(dt)

    def finish(self):
        elapsed = self.renderer.time
        rem = self.target_duration - elapsed
        if rem > 1e-4:
            self.wait(rem)
