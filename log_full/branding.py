import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

# Paths
root = Path(r"C:\Users\Asus\Downloads\yt\project_log\log_full")
default_brand_path = Path(r"C:\Users\Asus\Downloads\yt\rule to follwo\brand.json")

def get_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "csv=p=0",
        str(file_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def finalize(video_in, kind, n, out_dir="out/final", brand="brand.json"):
    """
    Applies end card, watermark logo, audio normalization, and exports to out_dir.
    kind: 'yt_full', 'yt_short', or 'insta_short'
    n: integer clip index (e.g. 1 for full, 2..5 for shorts)
    """
    video_in = Path(video_in)
    if not video_in.is_absolute():
        video_in = root / video_in
        
    out_dir = Path(out_dir)
    if not out_dir.is_absolute():
        out_dir = root / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    
    brand_file = Path(brand)
    if not brand_file.is_absolute():
        if (root / brand).exists():
            brand_file = root / brand
        else:
            brand_file = default_brand_path
            
    with open(brand_file, "r", encoding="utf-8") as f:
        brand_cfg = json.load(f)
        
    logo_cfg = brand_cfg.get("logo", {})
    logo_rel_path = logo_cfg.get("path", "assets/logo.png")
    logo_file = root / logo_rel_path
    if not logo_file.exists():
        # Fallback to absolute assets
        logo_file = root / "assets" / "logo.png"
        
    if not logo_file.exists():
        raise FileNotFoundError(f"Logo file not found: {logo_file}")
        
    d_in = get_duration(video_in)
    print(f"\nFinalizing {kind}{n} from {video_in.name} (dur={d_in:.3f}s)...")
    
    # Select end card assets
    if kind == "yt_full":
        end_card_vid = root / "media" / "videos" / "end_card" / "1080p30" / "EndCardYtFull.mp4"
        end_card_aud = root / "voice" / "end_yt_full.wav"
        xfade_d = 0.30
        is_vertical = False
        out_filename = f"yt_full{n}.mp4"
    elif kind == "yt_short":
        end_card_vid = root / "media" / "videos" / "end_card" / "1920p30" / "EndCardYtShort.mp4"
        end_card_aud = root / "voice" / "end_yt_short.wav"
        xfade_d = 0.25
        is_vertical = True
        out_filename = f"yt_short{n}.mp4"
    elif kind == "insta_short":
        end_card_vid = root / "media" / "videos" / "end_card" / "1920p30" / "EndCardInstaShort.mp4"
        end_card_aud = root / "voice" / "end_insta_short.wav"
        xfade_d = 0.25
        is_vertical = True
        out_filename = f"insta_short{n}.mp4"
    else:
        raise ValueError(f"Unknown kind: {kind}")
        
    out_mp4 = out_dir / out_filename
    d_card = get_duration(end_card_vid)
    d_aud = get_duration(end_card_aud)
    
    # Build ffmpeg command with filter_complex
    # Video join: xfade between main video [0:v] and end_card [1:v]
    # Audio join:
    #   For shorts: main audio [0:a], then 0.25s silence, then end voice [2:a]
    #   For full: main audio [0:a], then end voice [2:a] starting when card starts (offset d_in - xfade_d)
    # Watermark overlay: [3:v] is logo
    
    offset_v = max(0.0, d_in - xfade_d)
    
    if is_vertical:
        # Vertical watermark: width 90, margin_right 36, margin_top 190, opacity 0.65
        # Inputs:
        #   0: video_in
        #   1: end_card_vid
        #   2: end_card_aud
        #   3: logo_file
        filter_str = (
            f"[0:v][1:v]xfade=transition=fade:duration={xfade_d:.2f}:offset={offset_v:.3f}[v_xfaded];"
            f"[3:v]scale=90:-1,format=rgba,colorchannelmixer=aa=0.65[wm];"
            f"[v_xfaded][wm]overlay=W-w-36:190:format=auto[v_final];"
            f"[0:a]apad=pad_dur=0.25[a0_pad];"
            f"[a0_pad][2:a]concat=n=2:v=0:a=1[a_joined];"
            f"[a_joined]loudnorm=I=-14:TP=-1.0:LRA=9[a_final]"
        )
    else:
        # Horizontal watermark: width 110, margin_right 36, margin_top 36, opacity 0.65
        filter_str = (
            f"[0:v][1:v]xfade=transition=fade:duration={xfade_d:.2f}:offset={offset_v:.3f}[v_xfaded];"
            f"[3:v]scale=110:-1,format=rgba,colorchannelmixer=aa=0.65[wm];"
            f"[v_xfaded][wm]overlay=W-w-36:36:format=auto[v_final];"
            f"[0:a][2:a]concat=n=2:v=0:a=1[a_joined];"
            f"[a_joined]loudnorm=I=-14:TP=-1.0:LRA=9[a_final]"
        )
        
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_in),
        "-i", str(end_card_vid),
        "-i", str(end_card_aud),
        "-i", str(logo_file),
        "-filter_complex", filter_str,
        "-map", "[v_final]",
        "-map", "[a_final]",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        str(out_mp4)
    ]
    
    print(f"Executing assembly for {out_filename}...")
    subprocess.run(cmd, cwd=root, check=True)
    dur_final = get_duration(out_mp4)
    print(f"-> Created {out_mp4} ({dur_final:.3f}s)")
    return out_mp4

def run_all():
    out_dir = root / "out" / "final"
    out_dir.mkdir(parents=True, exist_ok=True)
    yt_final_dir = Path(r"C:\Users\Asus\Downloads\yt\final")
    yt_final_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Finalize yt_full1
    full_in = root / "out" / "log_full_captions.mp4"
    f_full1 = finalize(full_in, "yt_full", 1, out_dir=out_dir)
    shutil.copy2(f_full1, yt_final_dir / f_full1.name)
    
    # 2. Finalize shorts 2, 3, 4, 5
    clips_mapping = [
        {"n": 2, "id": "B_log_challenge", "headline": "What does a log actually mean?", "yt_title": "What Is a Log? Try This One Without a Calculator"},
        {"n": 3, "id": "C_numbers_start_with_1", "headline": "Why do so many numbers start with 1?", "yt_title": "Why Do So Many Numbers Start With 1?"},
        {"n": 4, "id": "D_log_scales", "headline": "The same math hides in earthquakes, acid and sound", "yt_title": "Earthquakes, pH and Sound Use the Same Trick"},
        {"n": 5, "id": "E_log_graph", "headline": "The graph that never stops climbing", "yt_title": "The Log Graph Explained in 45 Seconds"},
    ]
    
    posting_map_entries = []
    
    # Add yt_full entry
    full_dur = get_duration(f_full1)
    posting_map_entries.append(
        f"yt_full1.mp4 | YouTube | Full Video | What a Log Actually Is | {full_dur:.2f}s | What a Log Actually Is: How 42 Folds Reach the Moon"
    )
    
    for item in clips_mapping:
        n = item["n"]
        cid = item["id"]
        vert_clip = root / "out" / "shorts" / f"{cid}_vertical.mp4"
        
        # yt_short
        f_yt = finalize(vert_clip, "yt_short", n, out_dir=out_dir)
        shutil.copy2(f_yt, yt_final_dir / f_yt.name)
        dur_yt = get_duration(f_yt)
        posting_map_entries.append(
            f"yt_short{n}.mp4 | YouTube Shorts | {cid} | {item['headline']} | {dur_yt:.2f}s | {item['yt_title']}"
        )
        
        # insta_short
        f_in = finalize(vert_clip, "insta_short", n, out_dir=out_dir)
        shutil.copy2(f_in, yt_final_dir / f_in.name)
        dur_in = get_duration(f_in)
        posting_map_entries.append(
            f"insta_short{n}.mp4 | Instagram Reels | {cid} | {item['headline']} | {dur_in:.2f}s | {item['yt_title']}"
        )
        
    # Write posting_map.txt
    map_file = out_dir / "posting_map.txt"
    with open(map_file, "w", encoding="utf-8") as f:
        f.write("\n".join(posting_map_entries) + "\n")
    print(f"\nWritten {map_file}")
    shutil.copy2(map_file, yt_final_dir / "posting_map.txt")
    
    print("\nAll files successfully finalized and copied to yt/final!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "all":
        # CLI mode: python branding.py <video_in> <kind> <n>
        vid = sys.argv[1]
        k = sys.argv[2]
        num = int(sys.argv[3])
        finalize(vid, k, num)
    else:
        run_all()
