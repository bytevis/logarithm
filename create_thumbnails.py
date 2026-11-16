import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

# Paths
base_project_log = Path(r"C:\Users\Asus\Downloads\project_log")
yt_project_log = Path(r"C:\Users\Asus\Downloads\yt\project_log")
logo_path = Path(r"C:\Users\Asus\Downloads\yt\project_log\log_full\assets\logo.png")

# Font paths
FONT_IMPACT = r"C:\Windows\Fonts\impact.ttf"
FONT_SEGOE_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_ARIAL_BOLD = r"C:\Windows\Fonts\arialbd.ttf"

# Colors
C_BG_TOP = (6, 12, 28)
C_BG_BOT = (2, 4, 10)
C_YELLOW = (245, 158, 11)
C_BRIGHT_YELLOW = (255, 204, 0)
C_BLUE = (59, 130, 246)
C_CYAN = (6, 182, 212)
C_WHITE = (255, 255, 255)
C_GRAY = (148, 163, 184)
C_RED = (239, 68, 68)
C_GREEN = (16, 185, 129)

def create_gradient_bg(width, height, c_top, c_bot, add_glow_center=None, glow_radius=400, glow_color=(30, 64, 175, 120)):
    base = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    draw = ImageDraw.Draw(base)
    # Linear gradient
    for y in range(height):
        factor = y / float(height)
        r = int(c_top[0] * (1 - factor) + c_bot[0] * factor)
        g = int(c_top[1] * (1 - factor) + c_bot[1] * factor)
        b = int(c_top[2] * (1 - factor) + c_bot[2] * factor)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
        
    # Subtle grid lines
    grid_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grid_overlay)
    grid_size = 80
    for x in range(0, width, grid_size):
        gdraw.line([(x, 0), (x, height)], fill=(255, 255, 255, 10), width=1)
    for y in range(0, height, grid_size):
        gdraw.line([(0, y), (width, y)], fill=(255, 255, 255, 10), width=1)
        
    base = Image.alpha_composite(base, grid_overlay)
    
    # Radial glow if specified
    if add_glow_center is not None:
        cx, cy = add_glow_center
        glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        g_draw = ImageDraw.Draw(glow)
        for r_step in range(glow_radius, 0, -10):
            alpha = int(glow_color[3] * (1.0 - (r_step / glow_radius)**1.5))
            g_draw.ellipse([cx - r_step, cy - r_step, cx + r_step, cy + r_step], fill=(glow_color[0], glow_color[1], glow_color[2], alpha))
        glow = glow.filter(ImageFilter.GaussianBlur(15))
        base = Image.alpha_composite(base, glow)
        
    return base

def draw_text_with_shadow(draw, pos, text, font, fill_color, shadow_color=(0, 0, 0, 240), shadow_offset=(4, 6), outline_color=None, outline_width=0):
    x, y = pos
    # Shadow
    if shadow_offset != (0, 0):
        draw.text((x + shadow_offset[0], y + shadow_offset[1]), text, font=font, fill=shadow_color)
    # Outline
    if outline_color and outline_width > 0:
        for ox in range(-outline_width, outline_width + 1):
            for oy in range(-outline_width, outline_width + 1):
                if ox != 0 or oy != 0:
                    draw.text((x + ox, y + oy), text, font=font, fill=outline_color)
    # Main text
    draw.text((x, y), text, font=font, fill=fill_color)

def draw_rounded_card(img, bbox, fill_color, border_color=None, border_width=2, radius=20):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle(bbox, radius=radius, fill=fill_color, outline=border_color, width=border_width)
    return Image.alpha_composite(img, overlay)

def draw_realistic_moon(img, center, radius):
    cx, cy = center
    moon_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(moon_layer)
    
    # Outer corona glow
    for gr in range(int(radius * 1.6), int(radius), -6):
        alpha = int(70 * (1.0 - (gr - radius) / (radius * 0.6)))
        d.ellipse([cx - gr, cy - gr, cx + gr, cy + gr], fill=(245, 210, 140, alpha))
    moon_layer = moon_layer.filter(ImageFilter.GaussianBlur(10))
    
    # Moon disc
    d2 = ImageDraw.Draw(moon_layer)
    d2.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=(225, 230, 240, 255), outline=(255, 255, 255, 255), width=3)
    
    # Craters and mare textures
    craters = [
        (cx - radius*0.3, cy - radius*0.25, radius*0.28),
        (cx + radius*0.2, cy - radius*0.35, radius*0.22),
        (cx - radius*0.15, cy + radius*0.3, radius*0.32),
        (cx + radius*0.35, cy + radius*0.15, radius*0.25),
        (cx + radius*0.1, cy + radius*0.4, radius*0.18),
        (cx - radius*0.45, cy + radius*0.05, radius*0.15),
    ]
    for kx, ky, kr in craters:
        d2.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(175, 185, 200, 160))
        d2.ellipse([kx - kr*0.8, ky - kr*0.8, kx + kr*0.8, ky + kr*0.8], fill=(150, 160, 175, 140))
        
    return Image.alpha_composite(img, moon_layer)

def add_bytevis_badge(img, is_vertical=False):
    if not logo_path.exists():
        return img
    logo = Image.open(logo_path).convert("RGBA")
    w = 120 if is_vertical else 130
    h = int(logo.height * (w / logo.width))
    logo_resized = logo.resize((w, h), Image.Resampling.LANCZOS)
    
    # Position top-right
    if is_vertical:
        pos = (img.width - w - 40, 50)
    else:
        pos = (img.width - w - 40, 40)
        
    badge_bg = Image.new("RGBA", img.size, (0, 0, 0, 0))
    # Paste logo
    badge_bg.paste(logo_resized, pos, logo_resized)
    return Image.alpha_composite(img, badge_bg)

# -------------------------------------------------------------------------
# 1. THUMBNAIL: 01_full_video_what_is_a_log (1920x1080)
# -------------------------------------------------------------------------
def make_thumbnail_01():
    W, H = 1920, 1080
    bg = create_gradient_bg(W, H, (8, 16, 40), (2, 4, 12), add_glow_center=(1450, 480), glow_radius=550, glow_color=(245, 158, 11, 70))
    
    # Draw glowing Moon on the right
    bg = draw_realistic_moon(bg, (1480, 490), radius=280)
    
    # Left side: Stack of paper
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    
    # Glowing trajectory line from paper stack to Moon
    px, py = 420, 820
    mx, my = 1200, 490
    # Beam
    for lw in range(16, 0, -3):
        alpha = int(120 * (1.0 - lw/16.0))
        d.line([(px, py), (mx, my)], fill=(6, 182, 212, alpha), width=lw)
    d.line([(px, py), (mx, my)], fill=(255, 255, 255, 230), width=3)
    
    # Distance marker on beam
    font_sub = ImageFont.truetype(FONT_SEGOE_BOLD, 36)
    font_bold = ImageFont.truetype(FONT_IMPACT, 120)
    font_h2 = ImageFont.truetype(FONT_IMPACT, 96)
    font_card = ImageFont.truetype(FONT_SEGOE_BOLD, 42)
    font_badge = ImageFont.truetype(FONT_SEGOE_BOLD, 48)
    
    bg = Image.alpha_composite(bg, overlay)
    
    # Text Header & Hook
    draw = ImageDraw.Draw(bg)
    draw_text_with_shadow(draw, (90, 90), "HOW MANY FOLDS", font_bold, C_WHITE, shadow_offset=(6, 8), outline_color=(0, 0, 0), outline_width=4)
    draw_text_with_shadow(draw, (90, 220), "TO REACH THE MOON?", font_h2, C_BRIGHT_YELLOW, shadow_offset=(6, 8), outline_color=(0, 0, 0), outline_width=4)
    
    # Yellow badge on moon
    bg = draw_rounded_card(bg, (1260, 820, 1780, 930), (16, 185, 129, 230), (255, 255, 255, 255), border_width=3, radius=18)
    draw2 = ImageDraw.Draw(bg)
    draw_text_with_shadow(draw2, (1310, 842), "JUST 42 FOLDS!", font_badge, C_WHITE, shadow_offset=(3, 3))
    
    # Distance callout
    bg = draw_rounded_card(bg, (650, 600, 1140, 690), (15, 23, 42, 220), (6, 182, 212, 240), border_width=2, radius=16)
    draw3 = ImageDraw.Draw(bg)
    draw_text_with_shadow(draw3, (680, 622), "384,400 KILOMETERS", font_sub, C_CYAN, shadow_offset=(2, 2))
    
    # Left folded paper stack visual card
    bg = draw_rounded_card(bg, (90, 680, 580, 950), (15, 23, 42, 230), (59, 130, 246, 220), border_width=3, radius=20)
    draw4 = ImageDraw.Draw(bg)
    draw_text_with_shadow(draw4, (120, 710), "PAPER: 0.1 mm", font_card, C_GRAY, shadow_offset=(2, 2))
    draw_text_with_shadow(draw4, (120, 770), "DOUBLING 42 TIMES", font_card, C_WHITE, shadow_offset=(2, 2))
    draw_text_with_shadow(draw4, (120, 840), "= 440,000 km", font_badge, C_BRIGHT_YELLOW, shadow_offset=(3, 3))
    
    # Badge: LOGARITHM
    bg = draw_rounded_card(bg, (90, 350, 480, 430), (239, 68, 68, 240), radius=14)
    draw5 = ImageDraw.Draw(bg)
    draw_text_with_shadow(draw5, (120, 362), "THE LOGARITHM SECRET", font_sub, C_WHITE, shadow_offset=(2, 2))
    
    bg = add_bytevis_badge(bg, is_vertical=False)
    return bg

# -------------------------------------------------------------------------
# 2. THUMBNAIL: 02_short_what_does_a_log_mean (1080x1920)
# -------------------------------------------------------------------------
def make_thumbnail_02():
    W, H = 1080, 1920
    bg = create_gradient_bg(W, H, (10, 20, 48), (2, 4, 12), add_glow_center=(540, 960), glow_radius=600, glow_color=(59, 130, 246, 90))
    
    font_giant = ImageFont.truetype(FONT_IMPACT, 140)
    font_h1 = ImageFont.truetype(FONT_IMPACT, 105)
    font_math = ImageFont.truetype(FONT_SEGOE_BOLD, 84)
    font_sub = ImageFont.truetype(FONT_SEGOE_BOLD, 48)
    font_tag = ImageFont.truetype(FONT_SEGOE_BOLD, 38)
    
    # Top Tag
    bg = draw_rounded_card(bg, (180, 140, 900, 225), (245, 158, 11, 230), radius=16)
    d_tag = ImageDraw.Draw(bg)
    draw_text_with_shadow(d_tag, (230, 155), "MENTAL MATH CHALLENGE", font_tag, C_WHITE, shadow_offset=(2, 2))
    
    # Main Header
    draw = ImageDraw.Draw(bg)
    draw_text_with_shadow(draw, (80, 270), "WHAT DOES", font_giant, C_WHITE, shadow_offset=(6, 8), outline_color=(0, 0, 0), outline_width=4)
    draw_text_with_shadow(draw, (80, 420), "A LOG ACTUALLY", font_h1, C_WHITE, shadow_offset=(6, 8), outline_color=(0, 0, 0), outline_width=4)
    draw_text_with_shadow(draw, (80, 540), "MEAN?", font_giant, C_BRIGHT_YELLOW, shadow_offset=(6, 8), outline_color=(0, 0, 0), outline_width=4)
    
    # Big Challenge Box
    bg = draw_rounded_card(bg, (80, 740, 1000, 1180), (15, 23, 42, 240), (59, 130, 246, 255), border_width=4, radius=28)
    d_card = ImageDraw.Draw(bg)
    draw_text_with_shadow(d_card, (140, 780), "CAN YOU SOLVE THIS?", font_sub, C_CYAN, shadow_offset=(2, 2))
    draw_text_with_shadow(d_card, (170, 870), "log₂(32) = ?", font_math, C_BRIGHT_YELLOW, shadow_offset=(4, 6))
    draw_text_with_shadow(d_card, (140, 1020), "How many doublings to 32?", font_tag, C_GRAY, shadow_offset=(2, 2))
    
    # Breakdown cards
    bg = draw_rounded_card(bg, (80, 1240, 1000, 1560), (15, 23, 42, 230), (16, 185, 129, 230), border_width=3, radius=24)
    d_step = ImageDraw.Draw(bg)
    draw_text_with_shadow(d_step, (140, 1280), "THE ANSWER:", font_sub, C_GREEN, shadow_offset=(2, 2))
    draw_text_with_shadow(d_step, (140, 1360), "2 × 2 × 2 × 2 × 2 = 32", font_math, C_WHITE, shadow_offset=(4, 5))
    draw_text_with_shadow(d_step, (260, 1470), "5 DOUBLINGS = 5!", font_sub, C_BRIGHT_YELLOW, shadow_offset=(2, 2))
    
    # Bottom CTA Pill
    bg = draw_rounded_card(bg, (140, 1640, 940, 1750), (239, 68, 68, 240), radius=22)
    d_cta = ImageDraw.Draw(bg)
    draw_text_with_shadow(d_cta, (200, 1665), "TRY IN YOUR HEAD • NO CALC", font_sub, C_WHITE, shadow_offset=(3, 3))
    
    bg = add_bytevis_badge(bg, is_vertical=True)
    return bg

# -------------------------------------------------------------------------
# 3. THUMBNAIL: 03_short_why_numbers_start_with_1 (1080x1920)
# -------------------------------------------------------------------------
def make_thumbnail_03():
    W, H = 1080, 1920
    bg = create_gradient_bg(W, H, (12, 18, 38), (2, 4, 10), add_glow_center=(540, 1000), glow_radius=600, glow_color=(245, 158, 11, 80))
    
    font_giant = ImageFont.truetype(FONT_IMPACT, 150)
    font_h1 = ImageFont.truetype(FONT_IMPACT, 100)
    font_num1 = ImageFont.truetype(FONT_IMPACT, 240)
    font_sub = ImageFont.truetype(FONT_SEGOE_BOLD, 52)
    font_tag = ImageFont.truetype(FONT_SEGOE_BOLD, 38)
    font_bar = ImageFont.truetype(FONT_SEGOE_BOLD, 36)
    
    # Tag
    bg = draw_rounded_card(bg, (220, 140, 860, 225), (6, 182, 212, 230), radius=16)
    d_tag = ImageDraw.Draw(bg)
    draw_text_with_shadow(d_tag, (280, 155), "BENFORD'S LAW MYSTERY", font_tag, C_WHITE, shadow_offset=(2, 2))
    
    # Header
    draw = ImageDraw.Draw(bg)
    draw_text_with_shadow(draw, (80, 270), "WHY DO 30% OF", font_h1, C_WHITE, shadow_offset=(6, 8), outline_color=(0, 0, 0), outline_width=4)
    draw_text_with_shadow(draw, (80, 390), "ALL NUMBERS", font_h1, C_WHITE, shadow_offset=(6, 8), outline_color=(0, 0, 0), outline_width=4)
    draw_text_with_shadow(draw, (80, 510), "START WITH", font_h1, C_WHITE, shadow_offset=(6, 8), outline_color=(0, 0, 0), outline_width=4)
    draw_text_with_shadow(draw, (680, 460), "1?", font_num1, C_BRIGHT_YELLOW, shadow_offset=(8, 10), outline_color=(0, 0, 0), outline_width=6)
    
    # Central Bar Chart Visual Box
    bg = draw_rounded_card(bg, (80, 780, 1000, 1500), (15, 23, 42, 240), (245, 158, 11, 230), border_width=4, radius=28)
    d_chart = ImageDraw.Draw(bg)
    draw_text_with_shadow(d_chart, (140, 820), "DIGIT DISTRIBUTION IN REAL DATA:", font_tag, C_GRAY, shadow_offset=(2, 2))
    
    # Bars for digits 1 to 5
    bar_data = [
        ("1", 30.1, C_BRIGHT_YELLOW, 540),
        ("2", 17.6, C_BLUE, 340),
        ("3", 12.5, C_BLUE, 250),
        ("4", 9.7,  C_BLUE, 200),
        ("5", 7.9,  C_BLUE, 160),
    ]
    by = 900
    for digit, pct, color, bar_w in bar_data:
        # Digit label
        draw_text_with_shadow(d_chart, (130, by), digit, font_sub, C_WHITE, shadow_offset=(2, 2))
        # Bar
        d_chart.rounded_rectangle([200, by + 8, 200 + bar_w, by + 58], radius=10, fill=color)
        # Percentage text
        draw_text_with_shadow(d_chart, (220 + bar_w, by + 10), f"{pct}%", font_bar, C_WHITE if digit != "1" else C_BRIGHT_YELLOW, shadow_offset=(2, 2))
        by += 85
        
    draw_text_with_shadow(d_chart, (140, 1370), "Not 11% each. It's logarithmic!", font_sub, C_CYAN, shadow_offset=(2, 2))
    
    # Bottom Callout Box
    bg = draw_rounded_card(bg, (100, 1580, 980, 1720), (239, 68, 68, 240), radius=22)
    d_bot = ImageDraw.Draw(bg)
    draw_text_with_shadow(d_bot, (160, 1620), "SIMON NEWCOMB'S DISCOVERY", font_sub, C_WHITE, shadow_offset=(3, 3))
    
    bg = add_bytevis_badge(bg, is_vertical=True)
    return bg

# -------------------------------------------------------------------------
# 4. THUMBNAIL: 04_short_earthquakes_ph_sound (1080x1920)
# -------------------------------------------------------------------------
def make_thumbnail_04():
    W, H = 1080, 1920
    bg = create_gradient_bg(W, H, (18, 12, 34), (2, 4, 10), add_glow_center=(540, 960), glow_radius=600, glow_color=(239, 68, 68, 70))
    
    font_giant = ImageFont.truetype(FONT_IMPACT, 125)
    font_h1 = ImageFont.truetype(FONT_IMPACT, 95)
    font_sub = ImageFont.truetype(FONT_SEGOE_BOLD, 46)
    font_card_h = ImageFont.truetype(FONT_SEGOE_BOLD, 44)
    font_card_sub = ImageFont.truetype(FONT_SEGOE_BOLD, 38)
    font_tag = ImageFont.truetype(FONT_SEGOE_BOLD, 36)
    
    # Tag
    bg = draw_rounded_card(bg, (240, 140, 840, 225), (239, 68, 68, 230), radius=16)
    d_tag = ImageDraw.Draw(bg)
    draw_text_with_shadow(d_tag, (290, 155), "HIDDEN MATH IN NATURE", font_tag, C_WHITE, shadow_offset=(2, 2))
    
    # Header
    draw = ImageDraw.Draw(bg)
    draw_text_with_shadow(draw, (80, 270), "THE SECRET SCALE", font_giant, C_WHITE, shadow_offset=(6, 8), outline_color=(0, 0, 0), outline_width=4)
    draw_text_with_shadow(draw, (80, 410), "HIDING IN NATURE", font_h1, C_BRIGHT_YELLOW, shadow_offset=(6, 8), outline_color=(0, 0, 0), outline_width=4)
    
    # 3 Real-World Cards
    cards_data = [
        ("EARTHQUAKES (RICHTER)", "Magnitude 7 = 32× Magnitude 6!", (239, 68, 68, 220), 570),
        ("ACIDITY (pH SCALE)", "pH 3 is 1,000× more acidic than 6!", (16, 185, 129, 220), 890),
        ("SOUND (DECIBELS)", "+10 dB = 10× More Energy!", (59, 130, 246, 220), 1210)
    ]
    for title, desc, border_c, cy in cards_data:
        bg = draw_rounded_card(bg, (80, cy, 1000, cy + 260), (15, 23, 42, 240), border_c, border_width=3, radius=24)
        d_c = ImageDraw.Draw(bg)
        draw_text_with_shadow(d_c, (130, cy + 35), title, font_card_h, C_WHITE, shadow_offset=(2, 2))
        draw_text_with_shadow(d_c, (130, cy + 120), desc, font_card_sub, C_BRIGHT_YELLOW, shadow_offset=(3, 3))
        
    # Bottom callout
    bg = draw_rounded_card(bg, (80, 1560, 1000, 1720), (245, 158, 11, 240), radius=22)
    d_bot = ImageDraw.Draw(bg)
    draw_text_with_shadow(d_bot, (140, 1610), "MULTIPLYING, NOT ADDING!", font_sub, C_WHITE, shadow_offset=(3, 3))
    
    bg = add_bytevis_badge(bg, is_vertical=True)
    return bg

# -------------------------------------------------------------------------
# 5. THUMBNAIL: 05_short_the_log_graph (1080x1920)
# -------------------------------------------------------------------------
def make_thumbnail_05():
    W, H = 1080, 1920
    bg = create_gradient_bg(W, H, (8, 20, 42), (2, 4, 10), add_glow_center=(540, 1050), glow_radius=600, glow_color=(6, 182, 212, 80))
    
    font_giant = ImageFont.truetype(FONT_IMPACT, 130)
    font_h1 = ImageFont.truetype(FONT_IMPACT, 95)
    font_sub = ImageFont.truetype(FONT_SEGOE_BOLD, 46)
    font_formula = ImageFont.truetype(FONT_SEGOE_BOLD, 64)
    font_tag = ImageFont.truetype(FONT_SEGOE_BOLD, 38)
    
    # Tag
    bg = draw_rounded_card(bg, (220, 140, 860, 225), (59, 130, 246, 230), radius=16)
    d_tag = ImageDraw.Draw(bg)
    draw_text_with_shadow(d_tag, (280, 155), "VISUAL MATH GRAPH", font_tag, C_WHITE, shadow_offset=(2, 2))
    
    # Header
    draw = ImageDraw.Draw(bg)
    draw_text_with_shadow(draw, (80, 270), "THE CURVE THAT", font_giant, C_WHITE, shadow_offset=(6, 8), outline_color=(0, 0, 0), outline_width=4)
    draw_text_with_shadow(draw, (80, 410), "NEVER STOPS", font_giant, C_BRIGHT_YELLOW, shadow_offset=(6, 8), outline_color=(0, 0, 0), outline_width=4)
    
    # Central Graph Visual Box
    bg = draw_rounded_card(bg, (80, 600, 1000, 1440), (12, 18, 32, 240), (6, 182, 212, 240), border_width=4, radius=28)
    d_graph = ImageDraw.Draw(bg)
    
    # Axes
    ox, oy = 240, 1300
    d_graph.line([(ox, oy), (ox + 640, oy)], fill=(148, 163, 184, 200), width=4)
    d_graph.line([(ox, oy), (ox, oy - 620)], fill=(148, 163, 184, 200), width=4)
    # Diagonal mirror line y = x
    d_graph.line([(ox, oy), (ox + 520, oy - 520)], fill=(148, 163, 184, 120), width=3)
    
    # Exponential curve (blue/cyan)
    pts_exp = []
    for t in np.linspace(0, 1, 80):
        gx = ox + t * 300
        gy = oy - (math.exp(t * 2.3) - 1) / (math.exp(2.3) - 1) * 580
        pts_exp.append((gx, gy))
    d_graph.line(pts_exp, fill=(59, 130, 246, 255), width=8)
    
    # Logarithm curve (yellow)
    pts_log = []
    for t in np.linspace(0.01, 1, 80):
        gx = ox + t * 580
        gy = oy - (math.log(1 + t * 9) / math.log(10)) * 300
        pts_log.append((gx, gy))
    d_graph.line(pts_log, fill=(245, 158, 11, 255), width=8)
    
    # Labels
    draw_text_with_shadow(d_graph, (ox + 40, oy - 600), "2ˣ (Explosion)", font_sub, C_CYAN, shadow_offset=(2, 2))
    draw_text_with_shadow(d_graph, (ox + 320, oy - 220), "log₂(x)", font_formula, C_BRIGHT_YELLOW, shadow_offset=(3, 3))
    draw_text_with_shadow(d_graph, (ox + 340, oy - 460), "y = x", font_tag, C_GRAY, shadow_offset=(2, 2))
    
    # Bottom callout
    bg = draw_rounded_card(bg, (80, 1520, 1000, 1720), (16, 185, 129, 230), radius=24)
    d_bot = ImageDraw.Draw(bg)
    draw_text_with_shadow(d_bot, (140, 1560), "FLATTENS OUT BUT", font_sub, C_WHITE, shadow_offset=(2, 2))
    draw_text_with_shadow(d_bot, (140, 1630), "CLIMBS FOREVER TO INFINITY!", font_sub, C_BRIGHT_YELLOW, shadow_offset=(3, 3))
    
    bg = add_bytevis_badge(bg, is_vertical=True)
    return bg

# -------------------------------------------------------------------------
# 6. THUMBNAIL: 06_short_paper_to_moon_native_explainer (1080x1920)
# -------------------------------------------------------------------------
def make_thumbnail_06():
    W, H = 1080, 1920
    bg = create_gradient_bg(W, H, (8, 16, 42), (2, 4, 12), add_glow_center=(540, 520), glow_radius=500, glow_color=(245, 158, 11, 80))
    
    # Glowing Moon at upper center
    bg = draw_realistic_moon(bg, (540, 480), radius=220)
    
    font_giant = ImageFont.truetype(FONT_IMPACT, 150)
    font_huge = ImageFont.truetype(FONT_IMPACT, 110)
    font_num42 = ImageFont.truetype(FONT_IMPACT, 260)
    font_sub = ImageFont.truetype(FONT_SEGOE_BOLD, 52)
    font_step = ImageFont.truetype(FONT_SEGOE_BOLD, 40)
    font_tag = ImageFont.truetype(FONT_SEGOE_BOLD, 38)
    
    # Tag
    bg = draw_rounded_card(bg, (220, 100, 860, 185), (239, 68, 68, 230), radius=16)
    d_tag = ImageDraw.Draw(bg)
    draw_text_with_shadow(d_tag, (270, 115), "THE FOLDING PUZZLE", font_tag, C_WHITE, shadow_offset=(2, 2))
    
    # Giant Moon distance label
    draw = ImageDraw.Draw(bg)
    draw_text_with_shadow(draw, (220, 720), "384,400 KM", font_sub, C_BRIGHT_YELLOW, shadow_offset=(3, 4), outline_color=(0, 0, 0), outline_width=3)
    
    # Giant 42 Badge
    bg = draw_rounded_card(bg, (80, 840, 1000, 1340), (15, 23, 42, 240), (16, 185, 129, 240), border_width=4, radius=28)
    d_card = ImageDraw.Draw(bg)
    draw_text_with_shadow(d_card, (140, 870), "JUST", font_huge, C_WHITE, shadow_offset=(4, 5))
    draw_text_with_shadow(d_card, (380, 820), "42", font_num42, C_BRIGHT_YELLOW, shadow_offset=(8, 10), outline_color=(0, 0, 0), outline_width=6)
    draw_text_with_shadow(d_card, (140, 1140), "FOLDS TO THE MOON", font_huge, C_WHITE, shadow_offset=(4, 5))
    
    # Ladder Box
    bg = draw_rounded_card(bg, (80, 1380, 1000, 1720), (15, 23, 42, 230), (59, 130, 246, 220), border_width=3, radius=24)
    d_ladder = ImageDraw.Draw(bg)
    draw_text_with_shadow(d_ladder, (130, 1410), "10 folds = 10 cm", font_step, C_GRAY, shadow_offset=(2, 2))
    draw_text_with_shadow(d_ladder, (130, 1475), "20 folds = 100 meters", font_step, C_GRAY, shadow_offset=(2, 2))
    draw_text_with_shadow(d_ladder, (130, 1540), "40 folds = 110,000 km", font_step, C_WHITE, shadow_offset=(2, 2))
    draw_text_with_shadow(d_ladder, (130, 1615), "42 folds = 440,000 km!", font_sub, C_GREEN, shadow_offset=(3, 3))
    
    bg = add_bytevis_badge(bg, is_vertical=True)
    return bg

# -------------------------------------------------------------------------
# Main Execution: Generate and save to each respective folder
# -------------------------------------------------------------------------
def main():
    print("Generating all 6 thumbnails...")
    
    # 1. Full video (1920x1080)
    print("Generating Thumbnail 1 (Full video)...")
    im1 = make_thumbnail_01()
    
    # 2. Short 2
    print("Generating Thumbnail 2 (What does a log mean)...")
    im2 = make_thumbnail_02()
    
    # 3. Short 3
    print("Generating Thumbnail 3 (Why numbers start with 1)...")
    im3 = make_thumbnail_03()
    
    # 4. Short 4
    print("Generating Thumbnail 4 (Earthquakes, pH, sound)...")
    im4 = make_thumbnail_04()
    
    # 5. Short 5
    print("Generating Thumbnail 5 (The log graph)...")
    im5 = make_thumbnail_05()
    
    # 6. Short 6
    print("Generating Thumbnail 6 (Paper to moon native)...")
    im6 = make_thumbnail_06()
    
    thumbnails = [
        ("01_full_video_what_is_a_log", im1, True),
        ("02_short_what_does_a_log_mean", im2, False),
        ("03_short_why_numbers_start_with_1", im3, False),
        ("04_short_earthquakes_ph_sound", im4, False),
        ("05_short_the_log_graph", im5, False),
        ("06_short_paper_to_moon_native_explainer", im6, False),
    ]
    
    # Save into each target directory
    roots_to_update = [
        base_project_log / "videos",
        yt_project_log / "videos"
    ]
    
    for r in roots_to_update:
        print(f"\nSaving thumbnails into: {r}")
        for folder_name, im, is_horizontal in thumbnails:
            fdir = r / folder_name
            fdir.mkdir(parents=True, exist_ok=True)
            
            # Save standard thumbnail.png
            dest_png = fdir / "thumbnail.png"
            im.save(dest_png, format="PNG", optimize=True)
            print(f"  Saved {dest_png} ({im.size[0]}x{im.size[1]})")
            
            # For YouTube horizontal, also save 1280x720 standard size
            if is_horizontal:
                im_720 = im.resize((1280, 720), Image.Resampling.LANCZOS)
                dest_720 = fdir / "thumbnail_1280x720.png"
                im_720.save(dest_720, format="PNG", optimize=True)
                print(f"  Saved {dest_720} (1280x720)")
                
    print("\nAll thumbnails generated and saved successfully!")

if __name__ == "__main__":
    main()
