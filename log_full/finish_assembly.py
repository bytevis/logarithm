import os
import sys
import json
import math
import subprocess
from pathlib import Path

root = Path(r"C:\Users\Asus\Downloads\log_full")
voice_dir = root / "voice"
out_dir = root / "out"
sections_dir = out_dir / "sections"
words_dir = out_dir / "words"

with open(voice_dir / "timing.json", "r", encoding="utf-8") as f:
    timing = json.load(f)

total_s = float(timing["total_s"])
extra_hold_s = float(timing.get("extra_hold_s", 1.0))
final_total_s = total_s + extra_hold_s
final_total_frames = round(final_total_s * 30)

print(f"Assembly target duration: {final_total_s:.3f}s ({final_total_frames} frames)")

# 1. Concat video sections
concat_list_file = sections_dir / "concat_list.txt"
with open(concat_list_file, "w", encoding="utf-8") as f:
    for idx, name in enumerate(["S1Hook", "S2Idea", "S3Graph", "S4Pattern", "S5Scales", "S6Payoff"]):
        f.write(f"file 'sec_{idx}_{name}.mp4'\n")

video_concat = out_dir / "video_concat.mp4"
print("Concatenating section videos...")
concat_cmd = [
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", str(concat_list_file),
    "-c", "copy",
    str(video_concat)
]
subprocess.run(concat_cmd, capture_output=True, check=True)

# 2. Build Captions from out/words/full.json
with open(words_dir / "full.json", "r", encoding="utf-8") as f:
    words = json.load(f)

caption_chunks = []
curr_chunk = []
curr_char_len = 0

for w in words:
    w_text = w["word"]
    if len(curr_chunk) >= 7 or (curr_char_len + len(w_text) + 1 > 38 and len(curr_chunk) >= 4):
        # Flush chunk
        caption_chunks.append({
            "start_s": curr_chunk[0]["start_s"],
            "end_s": curr_chunk[-1]["end_s"],
            "text": " ".join(item["word"] for item in curr_chunk)
        })
        curr_chunk = [w]
        curr_char_len = len(w_text)
    else:
        curr_chunk.append(w)
        curr_char_len += len(w_text) + 1

if curr_chunk:
    caption_chunks.append({
        "start_s": curr_chunk[0]["start_s"],
        "end_s": curr_chunk[-1]["end_s"],
        "text": " ".join(item["word"] for item in curr_chunk)
    })

def format_time_srt(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(round((sec - int(sec)) * 1000))
    if ms >= 1000:
        s += 1
        ms -= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def format_time_ass(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100:
        s += 1
        cs -= 100
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"

# Write captions.srt
srt_path = out_dir / "captions.srt"
with open(srt_path, "w", encoding="utf-8") as f:
    for i, c in enumerate(caption_chunks, start=1):
        f.write(f"{i}\n")
        f.write(f"{format_time_srt(c['start_s'])} --> {format_time_srt(c['end_s'])}\n")
        f.write(f"{c['text']}\n\n")
print(f"Written {srt_path} ({len(caption_chunks)} lines)")

# Write captions.ass
ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,54,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,4,0,2,200,200,85,1
Style: BottomBar,Segoe UI,30,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,0,2,30,30,22,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ass_path = out_dir / "captions.ass"
final_ass_end = format_time_ass(final_total_s)
with open(ass_path, "w", encoding="utf-8") as f:
    f.write(ass_header)
    # Bottom branding bar per user request
    f.write(f"Dialogue: 0,0:00:00.00,{final_ass_end},BottomBar,,30,30,22,,👍 Like   •   💬 Comment   •   [▶ Subscribe]   •   ByteVis\n")
    for c in caption_chunks:
        start_t = format_time_ass(c["start_s"])
        end_t = format_time_ass(c["end_s"])
        f.write(f"Dialogue: 1,{start_t},{end_t},Default,,200,200,85,,{c['text']}\n")
print(f"Written {ass_path}")

# 3. Mux nocaptions MP4
nocaptions_mp4 = out_dir / "log_full_nocaptions.mp4"
raw_wav = voice_dir / "full.wav"

print("Muxing video and normalized audio (out/log_full_nocaptions.mp4)...")
mux_cmd = [
    "ffmpeg", "-y",
    "-i", str(video_concat),
    "-i", str(raw_wav),
    "-filter_complex", f"[1:a]apad=whole_dur={final_total_s:.3f},loudnorm=I=-14:TP=-1.0:LRA=9[aout]",
    "-map", "0:v", "-map", "[aout]",
    "-c:v", "copy",
    "-c:a", "aac", "-b:a", "192k",
    "-t", f"{final_total_s:.3f}",
    str(nocaptions_mp4)
]
subprocess.run(mux_cmd, capture_output=True, check=True)
print(f"Created {nocaptions_mp4}")

# 4. Burn captions (out/log_full_captions.mp4)
captions_mp4 = out_dir / "log_full_captions.mp4"
print("Burning in captions (out/log_full_captions.mp4)...")
burn_cmd = [
    "ffmpeg", "-y",
    "-i", "log_full_nocaptions.mp4",
    "-vf", "subtitles=captions.ass",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
    "-c:a", "copy",
    "log_full_captions.mp4"
]
subprocess.run(burn_cmd, cwd=out_dir, capture_output=True, check=True)
print(f"Created {captions_mp4}")

# 5. Write out/chapters.txt
chapter_titles = [
    "The Moon question",
    "What a log is",
    "The graph",
    "The strange pattern",
    "Logs in real life",
    "The payoff"
]

chapters_path = out_dir / "chapters.txt"
with open(chapters_path, "w", encoding="utf-8") as f:
    for sec, title in zip(timing["sections"], chapter_titles):
        s_time = float(sec["start_s"])
        m = int(s_time // 60)
        s = int(s_time % 60)
        f.write(f"{m:d}:{s:02d} {title}\n")
print(f"Written {chapters_path}")

print("\n=== ASSEMBLY COMPLETE ===")
