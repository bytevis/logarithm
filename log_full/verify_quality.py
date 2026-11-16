import os
import sys
import json
import re
import subprocess
from pathlib import Path

root = Path(r"C:\Users\Asus\Downloads\log_full")
out_dir = root / "out"
nocaptions_mp4 = out_dir / "log_full_nocaptions.mp4"
captions_mp4 = out_dir / "log_full_captions.mp4"

print("=== QUALITY CHECKS ===")

# 1. Math fact check
print("\n--- 1. Math Fact Check ---")
res = subprocess.run([sys.executable, "fact_check.py"], cwd=root, capture_output=True, text=True)
print(res.stdout.strip())
math_ok = "ALL FACTS OK" in res.stdout

# 2. Total duration & frame check
print("\n--- 2. Duration & Frame Check ---")
with open(root / "voice" / "timing.json", "r", encoding="utf-8") as f:
    timing = json.load(f)
target_total_s = float(timing["total_s"]) + float(timing.get("extra_hold_s", 1.0))
target_frames = round(target_total_s * 30)

cmd = [
    "ffprobe", "-v", "error",
    "-show_entries", "format=duration:stream=nb_frames,r_frame_rate,width,height",
    "-of", "json", str(nocaptions_mp4)
]
probe_res = subprocess.run(cmd, capture_output=True, text=True)
probe_data = json.loads(probe_res.stdout)
actual_dur = float(probe_data["format"]["duration"])
actual_frames = int(probe_data["streams"][0]["nb_frames"])
dur_diff = abs(actual_dur - target_total_s)
frame_diff = abs(actual_frames - target_frames)
print(f"Target duration: {target_total_s:.3f}s ({target_frames} frames)")
print(f"Actual duration: {actual_dur:.3f}s ({actual_frames} frames)")
print(f"Difference: {dur_diff:.3f}s, frame difference: {frame_diff} frames (limit: <= 1 frame)")

# 3. Silence Detection (>= 0.6s)
print("\n--- 3. Silence Detection (noise=-45dB, d=0.6s) ---")
silence_cmd = [
    "ffmpeg", "-i", str(nocaptions_mp4),
    "-af", "silencedetect=noise=-45dB:d=0.6",
    "-f", "null", "-"
]
sil_res = subprocess.run(silence_cmd, capture_output=True, text=True)
silence_lines = [l for l in sil_res.stderr.splitlines() if "silencedetect" in l]
print(f"Found {len(silence_lines)} silence report lines:")
for l in silence_lines:
    print(" ", l)

# 4. Freeze Detection (d=2.0s)
print("\n--- 4. Freeze Detection (n=-55dB, d=2.0s) ---")
freeze_cmd = [
    "ffmpeg", "-i", str(nocaptions_mp4),
    "-vf", "freezedetect=n=-55dB:d=2.0",
    "-f", "null", "-"
]
frz_res = subprocess.run(freeze_cmd, capture_output=True, text=True)
freeze_lines = [l for l in frz_res.stderr.splitlines() if "freezedetect" in l]
print(f"Found {len(freeze_lines)} freeze report lines:")
for l in freeze_lines:
    print(" ", l)

# 5. Banned words search
print("\n--- 5. Banned Words Search ---")
banned = ["binary", "merge", "sort", "subscribe", "video 1", "video 2"]
check_files = [
    root / "script.json",
    root / "common.py",
    out_dir / "captions.srt",
    out_dir / "captions.ass",
    out_dir / "chapters.txt"
]
for p in (root / "scenes").glob("*.py"):
    check_files.append(p)

banned_found = []
for cf in check_files:
    if cf.exists():
        txt_content = cf.read_text(encoding="utf-8", errors="ignore").lower()
        for b in banned:
            # check word boundary
            matches = re.findall(rf"\b{re.escape(b)}\b", txt_content)
            if matches:
                banned_found.append((cf.name, b, len(matches)))

if banned_found:
    print("WARNING: Banned words found:")
    for fn, b, count in banned_found:
        print(f"  {fn}: '{b}' ({count} occurrences)")
else:
    print("PASS: Zero banned words found across all project files, scenes, and captions!")

print("\n=== CHECKS COMPLETED ===")
