import os
import sys
import json
import re
import subprocess
from pathlib import Path

root = Path(r"C:\Users\Asus\Downloads\yt\project_log\log_full")
final_dir = root / "out" / "final"
qa_dir = root / "out" / "final_qa"
qa_dir.mkdir(parents=True, exist_ok=True)

files = [
    "yt_full1.mp4",
    "yt_short2.mp4",
    "insta_short2.mp4",
    "yt_short3.mp4",
    "insta_short3.mp4",
    "yt_short4.mp4",
    "insta_short4.mp4",
    "yt_short5.mp4",
    "insta_short5.mp4"
]

print("=== 1. FFPROBE METADATA CHECK ===")
metadata = {}
for fname in files:
    fpath = final_dir / fname
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate",
        "-show_entries", "format=duration,size",
        "-of", "json",
        str(fpath)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    info = json.loads(res.stdout)
    w = info["streams"][0]["width"]
    h = info["streams"][0]["height"]
    fps = info["streams"][0]["r_frame_rate"]
    dur = float(info["format"]["duration"])
    sz = int(info["format"]["size"]) / (1024*1024)
    metadata[fname] = {"width": w, "height": h, "fps": fps, "dur": dur, "size_mb": sz}
    print(f"  {fname:18s} : {w}x{h}, {fps} fps, {dur:.2f}s, {sz:.2f} MB")

print("\n=== 2. SILENCE DETECTION (-45 dB, d=0.6s) ===")
silences = {}
for fname in files:
    fpath = final_dir / fname
    cmd = [
        "ffmpeg", "-i", str(fpath),
        "-af", "silencedetect=noise=-45dB:d=0.6",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    matches = re.findall(r"silence_start: ([\d\.]+)[\s\S]*?silence_duration: ([\d\.]+)", res.stderr)
    silences[fname] = matches
    print(f"  {fname:18s} : {len(matches)} silences >= 0.6s found")
    for start, d in matches:
        print(f"      start={float(start):.2f}s, dur={float(d):.2f}s")

print("\n=== 3. BANNED WORDS CHECK ===")
banned = ["binary", "merge", "sort", "video 1", "video 2"]
banned_matches = []
# Check filenames
for fname in files:
    for b in banned:
        if b in fname.lower():
            banned_matches.append(f"Filename {fname} contains {b}")

# Check ASS & SRT in shorts
for srt in (root / "out" / "shorts").glob("*.srt"):
    content = srt.read_text(encoding="utf-8").lower()
    for b in banned:
        if b in content:
            banned_matches.append(f"{srt.name} contains {b}")

for ass in (root / "out" / "shorts").glob("*.ass"):
    content = ass.read_text(encoding="utf-8").lower()
    for b in banned:
        if b in content:
            banned_matches.append(f"{ass.name} contains {b}")

# Check posting map
map_text = (final_dir / "posting_map.txt").read_text(encoding="utf-8").lower()
for b in banned:
    if b in map_text:
        banned_matches.append(f"posting_map.txt contains {b}")

print(f"  Total banned word matches: {len(banned_matches)}")
if banned_matches:
    for bm in banned_matches:
        print("    WARNING:", bm)
else:
    print("  CLEAN! Zero banned words found across headlines, captions, posting map, and file names.")

print("\n=== 4. END VOICE TEXT VERIFICATION ===")
for vname in ["end_yt_full", "end_yt_short", "end_insta_short"]:
    words_f = root / "voice" / f"{vname}_words.json"
    with open(words_f, "r", encoding="utf-8") as f:
        w_data = json.load(f)
    last_3 = " ".join(item["word"] for item in w_data["words"][-3:])
    print(f"  {vname:16s} total dur: {w_data['duration_s']:.3f}s, last 3 spoken words: '{last_3}'")

print("\n=== 5. EXTRACT QA FRAMES ===")
# Extract first frame, last frame, middle of end card, and logo frame for yt_full1 and yt_short2
qa_targets = [
    ("yt_full1.mp4", [0.5, 150.0, 320.0, 327.0]),
    ("yt_short2.mp4", [0.5, 18.0, 36.0, 38.0]),
    ("insta_short2.mp4", [0.5, 18.0, 36.0, 38.0]),
]
for fname, pts in qa_targets:
    fpath = final_dir / fname
    for idx, pt in enumerate(pts, 1):
        out_p = qa_dir / f"{fname.replace('.mp4','')}_pt{idx}_{int(pt)}s.png"
        subprocess.run(["ffmpeg", "-y", "-ss", str(pt), "-i", str(fpath), "-vframes", "1", str(out_p)], capture_output=True, check=True)
        print(f"  Saved {out_p.name}")
