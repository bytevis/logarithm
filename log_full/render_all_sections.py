import subprocess
import shutil
from pathlib import Path

root = Path(r"C:\Users\Asus\Downloads\log_full")
scenes = [
    ("scenes/s2_idea.py", "S2Idea", 1),
    ("scenes/s3_graph.py", "S3Graph", 2),
    ("scenes/s4_pattern.py", "S4Pattern", 3),
    ("scenes/s5_scales.py", "S5Scales", 4),
    ("scenes/s6_payoff.py", "S6Payoff", 5),
]

py_exe = r"C:\Users\Asus\AppData\Local\Programs\Python\Python311\python.exe"

for script, cls_name, idx in scenes:
    print(f"\n>>> RENDERING {cls_name} (Section {idx})...")
    cmd = [py_exe, "-m", "manim", "-r", "1920,1080", "--fps", "30", script, cls_name]
    subprocess.run(cmd, cwd=root, check=True)
    
    script_stem = Path(script).stem
    src_mp4 = root / "media" / "videos" / script_stem / "1080p30" / f"{cls_name}.mp4"
    dst_mp4 = root / "out" / "sections" / f"sec_{idx}_{cls_name}.mp4"
    shutil.copy2(src_mp4, dst_mp4)
    print(f"Copied {src_mp4.name} -> {dst_mp4.name}")

print("\n=== ALL SECTIONS RENDERED SUCCESSFULLY ===")
