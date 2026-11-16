import subprocess
from pathlib import Path

root = Path(r"C:\Users\Asus\Downloads\yt\project_log\log_full")
py_exe = r"C:\Users\Asus\AppData\Local\Programs\Python\Python311\python.exe"

cards = [
    ("EndCardYtFull", "1920,1080"),
    ("EndCardYtShort", "1080,1920"),
    ("EndCardInstaShort", "1080,1920"),
]

for name, res in cards:
    print(f"\n--- Rendering {name} ({res}) ---")
    cmd = [
        py_exe, "-m", "manim",
        "-r", res,
        "--fps", "30",
        "scenes/end_card.py",
        name
    ]
    subprocess.run(cmd, cwd=root, check=True)
    print(f"Finished {name}")
