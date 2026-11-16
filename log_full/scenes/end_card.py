import os
import sys
import json
from pathlib import Path
from manim import *

root = Path(r"C:\Users\Asus\Downloads\yt\project_log\log_full")
sys.path.insert(0, str(root))

C_YELLOW = "#F59E0B"
C_BLUE = "#3B82F6"
C_GREEN = "#10B981"
C_RED = "#EF4444"
C_WHITE = "#FFFFFF"
C_GRAY = "#94A3B8"
C_DARK_GRAY = "#334155"

def bold_txt(text, font_size=56, color=C_WHITE):
    return Text(text, font="Segoe UI", weight=BOLD, font_size=font_size, color=color)

def txt(text, font_size=40, color=C_WHITE):
    return Text(text, font="Segoe UI", font_size=font_size, color=color)

def make_heart(color=C_YELLOW, scale=1.0):
    left_c = Circle(radius=0.28*scale, fill_color=color, fill_opacity=1.0, stroke_width=0).shift(LEFT*0.2*scale + UP*0.1*scale)
    right_c = Circle(radius=0.28*scale, fill_color=color, fill_opacity=1.0, stroke_width=0).shift(RIGHT*0.2*scale + UP*0.1*scale)
    sq = Square(side_length=0.48*scale, fill_color=color, fill_opacity=1.0, stroke_width=0).rotate(45*DEGREES).shift(DOWN*0.12*scale)
    return VGroup(sq, left_c, right_c)

def make_comment_bubble(color=C_WHITE, scale=1.0):
    body = RoundedRectangle(corner_radius=0.2*scale, width=1.1*scale, height=0.75*scale, fill_color=color, fill_opacity=0.15, stroke_color=color, stroke_width=3)
    dot1 = Dot(radius=0.07*scale, color=color).shift(LEFT*0.25*scale)
    dot2 = Dot(radius=0.07*scale, color=color)
    dot3 = Dot(radius=0.07*scale, color=color).shift(RIGHT*0.25*scale)
    tail = Polygon(
        body.get_corner(DL) + RIGHT*0.2*scale,
        body.get_corner(DL) + UP*0.1*scale,
        body.get_corner(DL) + LEFT*0.15*scale + DOWN*0.2*scale,
        fill_color=color, fill_opacity=0.15, stroke_color=color, stroke_width=3
    )
    return VGroup(body, dot1, dot2, dot3, tail)

def make_share_arrow(color=C_WHITE, scale=1.0):
    arc = Arc(radius=0.38*scale, start_angle=PI/2, angle=-PI/2, stroke_color=color, stroke_width=4.5*scale).shift(LEFT*0.15*scale + DOWN*0.1*scale)
    tip = Triangle(fill_color=color, fill_opacity=1.0, stroke_width=0).scale(0.18*scale).rotate(-90*DEGREES).shift(RIGHT*0.23*scale + UP*0.28*scale)
    return VGroup(arc, tip)

def make_subscribe_btn(font_size=48, scale=1.0):
    btn_bg = RoundedRectangle(corner_radius=0.25*scale, width=4.3*scale, height=1.2*scale, fill_color=C_RED, fill_opacity=1.0, stroke_width=0)
    play_tri = Triangle(fill_color=C_WHITE, fill_opacity=1.0, stroke_width=0).scale(0.18*scale).rotate(-90*DEGREES).move_to(btn_bg.get_left() + RIGHT*0.75*scale)
    sub_t = bold_txt("Subscribe", font_size=font_size, color=C_WHITE).move_to(btn_bg.get_right() + LEFT*1.8*scale)
    return VGroup(btn_bg, play_tri, sub_t)

def make_follow_btn(font_size=48, scale=1.0):
    btn_bg = RoundedRectangle(corner_radius=0.25*scale, width=3.8*scale, height=1.2*scale, fill_color=C_YELLOW, fill_opacity=1.0, stroke_width=0)
    plus_center = btn_bg.get_left() + RIGHT*0.75*scale
    plus_h = Line(LEFT*0.18*scale, RIGHT*0.18*scale, color=C_WHITE, stroke_width=4.5*scale).move_to(plus_center)
    plus_v = Line(DOWN*0.18*scale, UP*0.18*scale, color=C_WHITE, stroke_width=4.5*scale).move_to(plus_center)
    fol_t = bold_txt("Follow", font_size=font_size, color=C_WHITE).move_to(btn_bg.get_right() + LEFT*1.55*scale)
    return VGroup(btn_bg, plus_h, plus_v, fol_t)

# -------------------------------------------------------------
# EndCard horizontal (yt_full) - 1920x1080
# -------------------------------------------------------------
class EndCardYtFull(Scene):
    def construct(self):
        like_icon = make_heart(color=C_YELLOW, scale=1.3)
        like_word = bold_txt("Like", font_size=56, color=C_WHITE).next_to(like_icon, DOWN, buff=0.18)
        card_like = VGroup(like_icon, like_word).move_to([-4.8, 1.8, 0])
        
        sub_card = make_subscribe_btn(font_size=52, scale=1.1).move_to([0, 2.0, 0])
        
        comm_icon = make_comment_bubble(color=C_WHITE, scale=1.3)
        comm_word = bold_txt("Comment", font_size=56, color=C_WHITE).next_to(comm_icon, DOWN, buff=0.18)
        card_comm = VGroup(comm_icon, comm_word).move_to([4.8, 1.8, 0])
        
        share_icon = make_share_arrow(color=C_WHITE, scale=1.3)
        share_word = bold_txt("Share", font_size=56, color=C_WHITE).next_to(share_icon, DOWN, buff=0.18)
        share_friend = txt("with a friend", font_size=36, color=C_GRAY).next_to(share_word, DOWN, buff=0.12)
        card_share = VGroup(share_icon, share_word, share_friend).move_to([0, -0.2, 0])
        
        self.wait(1.0)
        self.play(FadeIn(card_like, scale=1.2), run_time=0.35)
        self.wait(1.0)
        self.play(FadeIn(sub_card, scale=1.2), run_time=0.35)
        self.wait(1.0)
        self.play(FadeIn(card_comm, scale=1.2), run_time=0.35)
        self.wait(1.0)
        self.play(FadeIn(card_share, scale=1.2), run_time=0.35)
        
        self.wait(0.5)
        self.play(sub_card.animate.scale(1.05), run_time=1.0)
        self.play(sub_card.animate.scale(1/1.05), run_time=1.0)
        self.wait(2.2)

# -------------------------------------------------------------
# EndCard vertical (yt_short) - 1080x1920
# -------------------------------------------------------------
class EndCardYtShort(Scene):
    def construct(self):
        like_icon = make_heart(color=C_YELLOW, scale=1.2)
        like_word = bold_txt("Like", font_size=64, color=C_WHITE).next_to(like_icon, RIGHT, buff=0.35)
        row_like = VGroup(like_icon, like_word).move_to([0, 3.2, 0])
        
        comm_icon = make_comment_bubble(color=C_WHITE, scale=1.2)
        comm_word = bold_txt("Comment", font_size=64, color=C_WHITE).next_to(comm_icon, RIGHT, buff=0.35)
        row_comm = VGroup(comm_icon, comm_word).move_to([0, 1.6, 0])
        
        share_icon = make_share_arrow(color=C_WHITE, scale=1.2)
        share_word = bold_txt("Share", font_size=64, color=C_WHITE).next_to(share_icon, RIGHT, buff=0.35)
        share_sub = txt("with a friend", font_size=38, color=C_GRAY).next_to(share_word, DOWN, buff=0.15)
        row_share = VGroup(share_icon, share_word, share_sub).move_to([0, -0.2, 0])
        
        sub_btn = make_subscribe_btn(font_size=58, scale=1.2).move_to([0, -2.4, 0])
        
        self.wait(0.1)
        self.play(FadeIn(row_like, scale=1.15), run_time=0.25)
        self.wait(0.25)
        self.play(FadeIn(row_comm, scale=1.15), run_time=0.25)
        self.wait(0.35)
        self.play(FadeIn(row_share, scale=1.15), run_time=0.25)
        self.wait(0.65)
        self.play(FadeIn(sub_btn, scale=1.2), run_time=0.3)
        self.wait(1.1)

# -------------------------------------------------------------
# EndCard vertical (insta_short) - 1080x1920
# -------------------------------------------------------------
class EndCardInstaShort(Scene):
    def construct(self):
        fol_btn = make_follow_btn(font_size=58, scale=1.2).move_to([0, 3.2, 0])
        
        like_icon = make_heart(color=C_YELLOW, scale=1.2)
        like_word = bold_txt("Like", font_size=64, color=C_WHITE).next_to(like_icon, RIGHT, buff=0.35)
        row_like = VGroup(like_icon, like_word).move_to([0, 1.4, 0])
        
        comm_icon = make_comment_bubble(color=C_WHITE, scale=1.2)
        comm_word = bold_txt("Comment", font_size=64, color=C_WHITE).next_to(comm_icon, RIGHT, buff=0.35)
        row_comm = VGroup(comm_icon, comm_word).move_to([0, -0.2, 0])
        
        share_icon = make_share_arrow(color=C_WHITE, scale=1.2)
        share_word = bold_txt("Share", font_size=64, color=C_WHITE).next_to(share_icon, RIGHT, buff=0.35)
        share_sub = txt("with a friend", font_size=38, color=C_GRAY).next_to(share_word, DOWN, buff=0.15)
        row_share = VGroup(share_icon, share_word, share_sub).move_to([0, -2.0, 0])
        
        self.wait(0.1)
        self.play(FadeIn(fol_btn, scale=1.2), run_time=0.25)
        self.wait(0.55)
        self.play(FadeIn(row_like, scale=1.15), run_time=0.25)
        self.wait(0.35)
        self.play(FadeIn(row_comm, scale=1.15), run_time=0.25)
        self.wait(0.35)
        self.play(FadeIn(row_share, scale=1.15), run_time=0.25)
        self.wait(1.1)
