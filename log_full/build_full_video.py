import os
import sys
import json
import math
import shutil
import subprocess
from pathlib import Path

root = Path(r"C:\Users\Asus\Downloads\log_full")
voice_dir = root / "voice"
out_dir = root / "out"
sections_dir = out_dir / "sections"
words_dir = out_dir / "words"

sections_dir.mkdir(parents=True, exist_ok=True)

with open(voice_dir / "timing.json", "r", encoding="utf-8") as f:
    timing = json.load(f)

total_s = float(timing["total_s"])
extra_hold_s = float(timing.get("extra_hold_s", 1.0))
final_total_s = total_s + extra_hold_s
final_total_frames = round(final_total_s * 30)

print(f"Total video duration required: {final_total_s:.3f}s ({final_total_frames} frames at 30 fps)")

sections = [
    ("scenes/s1_hook.py", "S1Hook", "S1_HOOK"),
    ("scenes/s2_idea.py", "S2Idea", "S2_IDEA"),
    ("scenes/s3_graph.py", "S3Graph", "S3_GRAPH"),
    ("scenes/s4_pattern.py", "S4Pattern", "S4_PATTERN"),
    ("scenes/s5_scales.py", "S5Scales", "S5_SCALES"),
    ("scenes/s6_payoff.py", "S6Payoff", "S6_PAYOFF"),
]

section_mp4s = []

def get_video_frames(path):
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=nb_frames,duration",
        "-of", "json", str(path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(res.stdout)
    frames = data["streams"][0].get("nb_frames")
    if frames:
        return int(frames)
    dur = float(data["format"]["duration"])
    return round(dur * 30)

for idx, (py_file, class_name, sec_id) in enumerate(sections):
    sec_data = next(s for s in timing["sections"] if s["id"] == sec_id)
    b_start = round(float(sec_data["start_s"]) * 30) / 30.0
    b_end = round(float(sec_data["end_s"]) * 30) / 30.0
    target_sec_dur = b_end - b_start
    target_frames = round(target_sec_dur * 30)
    
    print(f"\n==========================================")
    print(f"[{idx+1}/6] Rendering {class_name} ({sec_id})")
    print(f"Boundary: [{b_start:.3f}s -> {b_end:.3f}s] ({target_sec_dur:.3f}s, {target_frames} frames)")
    print(f"==========================================")
    
    # Run manim render at 1080p30
    cmd = [
        sys.executable, "-m", "manim",
        "-r", "1920,1080", "--fps", "30",
        str(root / py_file), class_name
    ]
    res = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error rendering {class_name}:")
        print(res.stderr[-2000:])
        sys.exit(1)
        
    # Locate output file
    stem = Path(py_file).stem
    candidate = root / "media" / "videos" / stem / "1080p30" / f"{class_name}.mp4"
    if not candidate.exists():
        # Check alternative location
        candidate = Path(r"C:\Users\Asus\Downloads\project_log\media\videos") / stem / "1080p30" / f"{class_name}.mp4"
    
    if not candidate.exists():
        print(f"Could not find rendered video at {candidate}")
        sys.exit(1)
        
    raw_frames = get_video_frames(candidate)
    print(f"Raw rendered frames: {raw_frames} (target: {target_frames})")
    
    final_sec_mp4 = sections_dir / f"sec_{idx}_{class_name}.mp4"
    
    # Exact frame padding or trimming if off by a frame
    if raw_frames < target_frames:
        pad_frames = target_frames - raw_frames
        print(f"Padding {pad_frames} frames with tpad...")
        pad_cmd = [
            "ffmpeg", "-y", "-i", str(candidate),
            "-vf", f"tpad=stop_mode=clone:stop={pad_frames}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
            str(final_sec_mp4)
        ]
        subprocess.run(pad_cmd, capture_output=True, check=True)
    elif raw_frames > target_frames:
        print(f"Trimming {raw_frames - target_frames} frames...")
        trim_cmd = [
            "ffmpeg", "-y", "-i", str(candidate),
            "-vframes", str(target_frames),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
            str(final_sec_mp4)
        ]
        subprocess.run(trim_cmd, capture_output=True, check=True)
    else:
        shutil.copy2(candidate, final_sec_mp4)
        
    actual_frames = get_video_frames(final_sec_mp4)
    print(f"Final section video: {final_sec_mp4.name} -> {actual_frames} frames ({actual_frames/30:.3f}s)")
    section_mp4s.append(final_sec_mp4)
    
    # Extract 3 check frames: +0.4s, middle, -0.4s
    f1_t = 0.4
    f2_t = target_sec_dur / 2.0
    f3_t = max(0.1, target_sec_dur - 0.4)
    for f_idx, t_pos in enumerate([f1_t, f2_t, f3_t], start=1):
        f_path = sections_dir / f"sec_{idx}_{class_name}_f{f_idx}.png"
        f_cmd = [
            "ffmpeg", "-y", "-ss", f"{t_pos:.3f}",
            "-i", str(final_sec_mp4),
            "-vframes", "1", str(f_path)
        ]
        subprocess.run(f_cmd, capture_output=True)

print("\nAll 6 sections rendered successfully!")
