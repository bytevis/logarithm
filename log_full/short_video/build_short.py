import json
import subprocess
import shutil
from pathlib import Path

root = Path(r"C:\Users\Asus\Downloads\log_full")
short_dir = root / "short_video"
out_dir = root / "out"

with open(short_dir / "short_timing.json", "r", encoding="utf-8") as f:
    timing = json.load(f)

final_total_s = float(timing["final_total_s"])
print(f"Short video total duration: {final_total_s:.3f}s")

py_exe = r"C:\Users\Asus\AppData\Local\Programs\Python\Python311\python.exe"

# 1. Render Manim Short Scene
print("Rendering ShortLogExplainer...")
cmd = [py_exe, "-m", "manim", "-r", "1920,1080", "--fps", "30", "short_video/short_scene.py", "ShortLogExplainer"]
subprocess.run(cmd, cwd=root, check=True)

raw_video = root / "media" / "videos" / "short_scene" / "1080p30" / "ShortLogExplainer.mp4"

# 2. Build Captions
with open(short_dir / "short_words.json", "r", encoding="utf-8") as f:
    words = json.load(f)

caption_chunks = []
curr_chunk = []
curr_len = 0
for w in words:
    wt = w["word"]
    if len(curr_chunk) >= 6 or (curr_len + len(wt) + 1 > 36 and len(curr_chunk) >= 3):
        caption_chunks.append({
            "start_s": curr_chunk[0]["start_s"],
            "end_s": curr_chunk[-1]["end_s"],
            "text": " ".join(item["word"] for item in curr_chunk)
        })
        curr_chunk = [w]
        curr_len = len(wt)
    else:
        curr_chunk.append(w)
        curr_len += len(wt) + 1

if curr_chunk:
    caption_chunks.append({
        "start_s": curr_chunk[0]["start_s"],
        "end_s": curr_chunk[-1]["end_s"],
        "text": " ".join(item["word"] for item in curr_chunk)
    })

def fmt_ass(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100:
        s += 1
        cs -= 100
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"

ass_path = short_dir / "short_captions.ass"
with open(ass_path, "w", encoding="utf-8") as f:
    f.write("""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,54,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,4,0,2,200,200,45,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""")
    for c in caption_chunks:
        f.write(f"Dialogue: 0,{fmt_ass(c['start_s'])},{fmt_ass(c['end_s'])},Default,,200,200,45,,{c['text']}\n")

# 3. Mux clean video
raw_audio = short_dir / "short_voice.wav"
nocaptions_mp4 = out_dir / "log_short_nocaptions.mp4"
mux_cmd = [
    "ffmpeg", "-y",
    "-i", str(raw_video),
    "-i", str(raw_audio),
    "-filter_complex", f"[1:a]apad=whole_dur={final_total_s:.3f},loudnorm=I=-14:TP=-1.0:LRA=9[aout]",
    "-map", "0:v", "-map", "[aout]",
    "-c:v", "copy",
    "-c:a", "aac", "-b:a", "192k",
    "-t", f"{final_total_s:.3f}",
    str(nocaptions_mp4)
]
subprocess.run(mux_cmd, check=True)
print(f"Created {nocaptions_mp4}")

# 4. Burn in captions (NO watermark bar for short video)
captions_mp4 = out_dir / "log_short_captions.mp4"
burn_cmd = [
    "ffmpeg", "-y",
    "-i", str(nocaptions_mp4),
    "-vf", f"subtitles='{ass_path.as_posix()}'",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
    "-c:a", "copy",
    str(captions_mp4)
]
subprocess.run(burn_cmd, check=True)
print(f"Created {captions_mp4}")

print("\n=== SHORT VIDEO COMPLETE ===")
