import subprocess
import shutil
from pathlib import Path

root = Path(r"C:\Users\Asus\Downloads\log_full")
cta_dir = root / "cta_clips"
yt_cta_dir = Path(r"C:\Users\Asus\Downloads\yt\cta_clips")
yt_cta_dir.mkdir(parents=True, exist_ok=True)

py_exe = r"C:\Users\Asus\AppData\Local\Programs\Python\Python311\python.exe"

# 1. Render LikeSubscribeComment
print("Rendering LikeSubscribeComment...")
cmd1 = [py_exe, "-m", "manim", "-r", "1920,1080", "--fps", "30", "cta_clips/cta_scenes.py", "LikeSubscribeComment"]
subprocess.run(cmd1, cwd=root, check=True)

# Mux CTA 1 with cta1.wav
raw_v1 = root / "media" / "videos" / "cta_scenes" / "1080p30" / "LikeSubscribeComment.mp4"
out_cta1 = cta_dir / "like_subscribe_comment.mp4"
mux1 = [
    "ffmpeg", "-y",
    "-i", str(raw_v1),
    "-i", str(cta_dir / "cta1.wav"),
    "-c:v", "copy",
    "-c:a", "aac", "-b:a", "192k",
    "-t", "3.0",
    str(out_cta1)
]
subprocess.run(mux1, check=True)
shutil.copy2(out_cta1, yt_cta_dir / "like_subscribe_comment.mp4")
print(f"Created {out_cta1}")

# 2. Render FollowCommentSubscribe
print("Rendering FollowCommentSubscribe...")
cmd2 = [py_exe, "-m", "manim", "-r", "1920,1080", "--fps", "30", "cta_clips/cta_scenes.py", "FollowCommentSubscribe"]
subprocess.run(cmd2, cwd=root, check=True)

# Mux CTA 2 with cta2.wav
raw_v2 = root / "media" / "videos" / "cta_scenes" / "1080p30" / "FollowCommentSubscribe.mp4"
out_cta2 = cta_dir / "follow_comment_subscribe.mp4"
mux2 = [
    "ffmpeg", "-y",
    "-i", str(raw_v2),
    "-i", str(cta_dir / "cta2.wav"),
    "-c:v", "copy",
    "-c:a", "aac", "-b:a", "192k",
    "-t", "3.0",
    str(out_cta2)
]
subprocess.run(mux2, check=True)
shutil.copy2(out_cta2, yt_cta_dir / "follow_comment_subscribe.mp4")
print(f"Created {out_cta2}")

print("\n=== BOTH CTA CLIPS COMPLETE ===")
