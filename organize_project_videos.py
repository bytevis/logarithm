import os
import shutil
import json
from pathlib import Path

# Base roots
base_project_log = Path(r"C:\Users\Asus\Downloads\project_log")
yt_project_log = Path(r"C:\Users\Asus\Downloads\yt\project_log")
log_full = yt_project_log / "log_full"

# We will create the organized structure in both base_project_log/videos and yt_project_log/videos
target_roots = [
    base_project_log / "videos",
    yt_project_log / "videos"
]

# Generate SRT for native vertical short if needed
short_dir = log_full / "short_video"
words_file = short_dir / "short_words.json"
if words_file.exists():
    with open(words_file, "r", encoding="utf-8") as f:
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

    def fmt_srt(sec):
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        ms = int(round((sec - int(sec)) * 1000))
        if ms >= 1000:
            s += 1
            ms -= 1000
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    srt_path = short_dir / "short_vertical_captions.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, c in enumerate(caption_chunks, 1):
            ctext = c["text"]
            if ctext and ctext[0].islower():
                ctext = ctext[0].upper() + ctext[1:]
            f.write(f"{idx}\n{fmt_srt(c['start_s'])} --> {fmt_srt(c['end_s'])}\n{ctext}\n\n")
    print(f"Generated {srt_path}")

# Video collections to organize
video_folders_config = [
    {
        "folder_name": "01_full_video_what_is_a_log",
        "title": "What a Log Actually Is: How 42 Folds Reach the Moon",
        "type": "Full Horizontal Video (1920x1080, 5m 28s)",
        "description": "Full math explainer video with animated voiceover, chapters, captions, branding watermark, and YouTube end card.",
        "files_to_copy": [
            (log_full / "out" / "final" / "yt_full1.mp4", "yt_full1.mp4"),
            (log_full / "out" / "log_full_captions.mp4", "log_full_captions_clean.mp4"),
            (log_full / "out" / "captions.srt", "captions.srt"),
            (log_full / "out" / "captions.ass", "captions.ass"),
            (log_full / "out" / "chapters.txt", "chapters.txt"),
        ]
    },
    {
        "folder_name": "02_short_what_does_a_log_mean",
        "title": "What Is a Log? Try This One Without a Calculator",
        "type": "Vertical Short / Reel (1080x1920, 38.3s)",
        "description": "Clip B: Explains the definition of logarithm and gives the 2^5=32 mental-math pause challenge.",
        "files_to_copy": [
            (log_full / "out" / "final" / "yt_short2.mp4", "yt_short2.mp4"),
            (log_full / "out" / "final" / "insta_short2.mp4", "insta_short2.mp4"),
            (log_full / "out" / "shorts" / "B_log_challenge_vertical.mp4", "B_log_challenge_vertical.mp4"),
            (log_full / "out" / "shorts" / "B_log_challenge.srt", "B_log_challenge.srt"),
            (log_full / "out" / "shorts" / "B_log_challenge.ass", "B_log_challenge.ass"),
            (log_full / "out" / "shorts" / "B_log_challenge_cover.png", "B_log_challenge_cover.png"),
        ]
    },
    {
        "folder_name": "03_short_why_numbers_start_with_1",
        "title": "Why Do So Many Numbers Start With 1?",
        "type": "Vertical Short / Reel (1080x1920, 54.3s)",
        "description": "Clip C: Simon Newcomb's discovery in 1881, Benford's law frequency bars, and the logarithm ruler payoff.",
        "files_to_copy": [
            (log_full / "out" / "final" / "yt_short3.mp4", "yt_short3.mp4"),
            (log_full / "out" / "final" / "insta_short3.mp4", "insta_short3.mp4"),
            (log_full / "out" / "shorts" / "C_numbers_start_with_1_vertical.mp4", "C_numbers_start_with_1_vertical.mp4"),
            (log_full / "out" / "shorts" / "C_numbers_start_with_1.srt", "C_numbers_start_with_1.srt"),
            (log_full / "out" / "shorts" / "C_numbers_start_with_1.ass", "C_numbers_start_with_1.ass"),
            (log_full / "out" / "shorts" / "C_numbers_start_with_1_cover.png", "C_numbers_start_with_1_cover.png"),
        ]
    },
    {
        "folder_name": "04_short_earthquakes_ph_sound",
        "title": "Earthquakes, pH and Sound Use the Same Trick",
        "type": "Vertical Short / Reel (1080x1920, 45.2s)",
        "description": "Clip D: Real-world logarithmic scales across seismograph magnitude, pH acidity tiles, and decibels.",
        "files_to_copy": [
            (log_full / "out" / "final" / "yt_short4.mp4", "yt_short4.mp4"),
            (log_full / "out" / "final" / "insta_short4.mp4", "insta_short4.mp4"),
            (log_full / "out" / "shorts" / "D_log_scales_vertical.mp4", "D_log_scales_vertical.mp4"),
            (log_full / "out" / "shorts" / "D_log_scales.srt", "D_log_scales.srt"),
            (log_full / "out" / "shorts" / "D_log_scales.ass", "D_log_scales.ass"),
            (log_full / "out" / "shorts" / "D_log_scales_cover.png", "D_log_scales_cover.png"),
        ]
    },
    {
        "folder_name": "05_short_the_log_graph",
        "title": "The Log Graph Explained in 45 Seconds",
        "type": "Vertical Short / Reel (1080x1920, 47.6s)",
        "description": "Clip E: The exponential vs log mirror-image curves across the y=x diagonal line.",
        "files_to_copy": [
            (log_full / "out" / "final" / "yt_short5.mp4", "yt_short5.mp4"),
            (log_full / "out" / "final" / "insta_short5.mp4", "insta_short5.mp4"),
            (log_full / "out" / "shorts" / "E_log_graph_vertical.mp4", "E_log_graph_vertical.mp4"),
            (log_full / "out" / "shorts" / "E_log_graph.srt", "E_log_graph.srt"),
            (log_full / "out" / "shorts" / "E_log_graph.ass", "E_log_graph.ass"),
            (log_full / "out" / "shorts" / "E_log_graph_cover.png", "E_log_graph_cover.png"),
        ]
    },
    {
        "folder_name": "06_short_paper_to_moon_native_explainer",
        "title": "How 42 Folds Reach the Moon (Native Vertical Animation)",
        "type": "Native Vertical Manim Short (1080x1920, 75.4s)",
        "description": "Dedicated full-screen vertical animated short covering the entire paper fold puzzle and log payoff.",
        "files_to_copy": [
            (log_full / "out" / "log_vertical_shorts.mp4", "log_vertical_shorts.mp4"),
            (log_full / "short_video" / "short_vertical_captions.srt", "short_vertical_captions.srt"),
            (log_full / "short_video" / "short_vertical_captions.ass", "short_vertical_captions.ass"),
            (log_full / "short_video" / "short_voice.wav", "short_voice.wav"),
        ]
    }
]

for t_root in target_roots:
    t_root.mkdir(parents=True, exist_ok=True)
    print(f"\nPopulating organized folders into: {t_root}")
    
    # Also write a master README / catalog
    catalog_lines = [
        "# Video Deliverables Catalog",
        "============================",
        ""
    ]
    
    for cfg in video_folders_config:
        folder_dir = t_root / cfg["folder_name"]
        folder_dir.mkdir(parents=True, exist_ok=True)
        print(f"  Folder: {cfg['folder_name']}/")
        
        info_lines = [
            f"Title: {cfg['title']}",
            f"Format: {cfg['type']}",
            f"Description: {cfg['description']}",
            "",
            "Files in this folder:"
        ]
        
        for src_file, dest_name in cfg["files_to_copy"]:
            if src_file.exists():
                dest_file = folder_dir / dest_name
                shutil.copy2(src_file, dest_file)
                info_lines.append(f"  - {dest_name} ({dest_file.stat().st_size / (1024*1024):.2f} MB)")
                print(f"    Copied {dest_name}")
            else:
                print(f"    WARNING: {src_file} does not exist!")
                
        # Write info.txt
        (folder_dir / "info.txt").write_text("\n".join(info_lines) + "\n", encoding="utf-8")
        
        catalog_lines.append(f"## {cfg['folder_name']}")
        catalog_lines.append(f"- **Title**: {cfg['title']}")
        catalog_lines.append(f"- **Type**: {cfg['type']}")
        catalog_lines.append(f"- **Description**: {cfg['description']}")
        catalog_lines.append("")
        
    (t_root / "README.md").write_text("\n".join(catalog_lines) + "\n", encoding="utf-8")
    # Also copy posting_map.txt
    if (log_full / "out" / "final" / "posting_map.txt").exists():
        shutil.copy2(log_full / "out" / "final" / "posting_map.txt", t_root / "posting_map.txt")

print("\nDone organizing all videos into individual folders!")
