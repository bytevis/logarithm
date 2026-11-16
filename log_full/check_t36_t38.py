import json
import subprocess
from pathlib import Path

root = Path(r"C:\Users\Asus\Downloads\yt\project_log\log_full")
with open(root / "voice" / "timing.json", "r", encoding="utf-8") as f:
    timing = json.load(f)

for s in timing["sections"]:
    for t in s["takes"]:
        if t["id"] in ("t36", "t38"):
            mid_s = (t["start_s"] + t["speech_end_s"]) / 2
            print(f"{t['id']}: start={t['start_s']}, mid={mid_s:.2f}, end={t['speech_end_s']}: {t['text']}")
            out_img = str(root / "out" / f"check_{t['id']}.png")
            subprocess.run(["ffmpeg", "-y", "-ss", f"{mid_s:.2f}", "-i", str(root / "out" / "log_full_nocaptions.mp4"), "-vframes", "1", out_img], capture_output=True, check=True)
