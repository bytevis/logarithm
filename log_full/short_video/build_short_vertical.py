import json
import subprocess
import shutil
from pathlib import Path

root = Path(r"C:\Users\Asus\Downloads\log_full")
short_dir = root / "short_video"
out_dir = root / "out"
yt_dir = Path(r"C:\Users\Asus\Downloads\yt")

with open(short_dir / "short_timing.json", "r", encoding="utf-8") as f:
    timing = json.load(f)

final_total_s = float(timing["final_total_s"])
print(f"Short video total duration: {final_total_s:.3f}s")

py_exe = r"C:\Users\Asus\AppData\Local\Programs\Python\Python311\python.exe"

# 1. Render Manim Short Scene in Vertical 1080x1920
print("Rendering ShortVerticalExplainer (1080x1920)...")
cmd = [py_exe, "-m", "manim", "-r", "1080,1920", "--fps", "30", "short_video/short_vertical.py", "ShortVerticalExplainer"]
subprocess.run(cmd, cwd=root, check=True)

raw_video = root / "media" / "videos" / "short_vertical" / "1920p30" / "ShortVerticalExplainer.mp4"
if not raw_video.exists():
    # Check alternate path if manim saved under different folder
    candidates = list(root.glob("**/ShortVerticalExplainer.mp4"))
    if candidates:
        raw_video = candidates[0]
print(f"Found raw video: {raw_video}")

# 2. Build Vertical Captions (1080x1920, punchy 3-5 word chunks)
with open(short_dir / "short_words.json", "r", encoding="utf-8") as f:
    words = json.load(f)

caption_chunks = []
curr_chunk = []
curr_len = 0
for w in words:
    wt = w["word"]
    if len(curr_chunk) >= 5 or (curr_len + len(wt) + 1 > 24 and len(curr_chunk) >= 2):
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

ass_path = short_dir / "short_vertical_captions.ass"
with open(ass_path, "w", encoding="utf-8") as f:
    f.write("""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Segoe UI,58,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4.5,1.5,2,60,60,340,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""")
    for c in caption_chunks:
        f.write(f"Dialogue: 0,{fmt_ass(c['start_s'])},{fmt_ass(c['end_s'])},Default,,60,60,340,,{c['text']}\n")

print(f"Created {ass_path} with {len(caption_chunks)} dialogue lines.")

# 3. Mux clean vertical video with normalized voice
raw_audio = short_dir / "short_voice.wav"
nocaptions_mp4 = out_dir / "log_vertical_shorts_nocaptions.mp4"
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

# 4. Burn in vertical captions
captions_mp4 = out_dir / "log_vertical_shorts.mp4"
burn_cmd = [
    "ffmpeg", "-y",
    "-i", str(nocaptions_mp4),
    "-vf", f"subtitles=short_vertical_captions.ass",
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    "-r", "30",
    "-c:a", "copy",
    str(captions_mp4)
]
subprocess.run(burn_cmd, cwd=short_dir, check=True)
print(f"Created {captions_mp4}")

# 5. Copy to yt folder
dest_yt = yt_dir / "log_vertical_shorts.mp4"
shutil.copy2(captions_mp4, dest_yt)
print(f"Copied to {dest_yt}")
