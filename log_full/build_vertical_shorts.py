import os
import sys
import json
import subprocess
from pathlib import Path

root = Path(r"C:\Users\Asus\Downloads\yt\project_log\log_full")
shorts_dir = root / "out" / "shorts"
shorts_dir.mkdir(parents=True, exist_ok=True)

with open(root / "voice" / "timing.json", "r", encoding="utf-8") as f:
    timing = json.load(f)

takes_by_id = {}
for s in timing["sections"]:
    for t in s["takes"]:
        takes_by_id[t["id"]] = t

with open(root / "out" / "words" / "full.json", "r", encoding="utf-8") as f:
    all_words = json.load(f)

with open(root / "script.json", "r", encoding="utf-8") as f:
    script_data = json.load(f)

script_takes = {}
for s in script_data["sections"]:
    for t in s["takes"]:
        script_takes[t["id"]] = t["text"]

# Source video
src_video = root / "out" / "log_full_nocaptions.mp4"

# Definitions from clips_plan.json
clips_cfg = [
    {
        "id": "B_log_challenge",
        "headline_raw": "What does a log actually mean?",
        "headline_ass": r"What does a {\c&H000B9EF5&}log{\c&H00FFFFFF&} actually mean?",
        "start_take": "t09",
        "end_take": "t14",
        "take_ids": ["t09", "t10", "t11", "t12", "t13", "t14"],
        "cover_offset_s": 15.0
    },
    {
        "id": "C_numbers_start_with_1",
        "headline_raw": "Why do so many numbers start with 1?",
        "headline_ass": r"Why do so many numbers start with {\c&H000B9EF5&}1{\c&H00FFFFFF&}?",
        "start_take": "t22",
        "end_take": "t27",
        "take_ids": ["t22", "t23", "t24", "t25", "t26", "t27"],
        "cover_offset_s": 25.0
    },
    {
        "id": "D_log_scales",
        "headline_raw": "The same math hides in earthquakes, acid and sound",
        "headline_ass": r"The same math hides in earthquakes, acid and {\c&H000B9EF5&}sound{\c&H00FFFFFF&}",
        "start_take": "t31",
        "end_take": "t34",
        "take_ids": ["t31", "t32", "t33", "t34"],
        "cover_offset_s": 18.0
    },
    {
        "id": "E_log_graph",
        "headline_raw": "The graph that never stops climbing",
        "headline_ass": r"The graph that never stops {\c&H000B9EF5&}climbing{\c&H00FFFFFF&}",
        "start_take": "t16",
        "end_take": "t21",
        "take_ids": ["t16", "t17", "t18", "t19", "t20", "t21"],
        "cover_offset_s": 22.0
    }
]

def fmt_ass(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100:
        s += 1
        cs -= 100
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"

def fmt_srt(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(round((sec - int(sec)) * 1000))
    if ms >= 1000:
        s += 1
        ms -= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

clip_summaries = []

for c in clips_cfg:
    cid = c["id"]
    t_start = takes_by_id[c["start_take"]]["start_s"] - 0.05
    t_end = takes_by_id[c["end_take"]]["speech_end_s"] + 0.12
    dur = t_end - t_start
    print(f"\n==========================================")
    print(f"Processing {cid}: {t_start:.3f}s to {t_end:.3f}s (dur={dur:.3f}s)")
    
    # 1. Filter words
    words = [w for w in all_words if w["take"] in c["take_ids"]]
    first_3 = " ".join(w["word"] for w in words[:3])
    last_3 = " ".join(w["word"] for w in words[-3:])
    print(f"  First 3 words: '{first_3}'")
    print(f"  Last 3 words:  '{last_3}'")
    
    # 2. Chunk captions (max 4 words, ~24 chars)
    caption_chunks = []
    curr_chunk = []
    curr_len = 0
    for w in words:
        wt = w["word"]
        # Words timed relative to clip start
        rel_start = max(0.0, w["start_s"] - t_start)
        rel_end = min(dur, w["end_s"] - t_start)
        w_item = {"word": wt, "start_s": rel_start, "end_s": rel_end}
        
        if len(curr_chunk) >= 4 or (curr_len + len(wt) + 1 > 24 and len(curr_chunk) >= 2):
            caption_chunks.append({
                "start_s": curr_chunk[0]["start_s"],
                "end_s": curr_chunk[-1]["end_s"],
                "text": " ".join(item["word"] for item in curr_chunk)
            })
            curr_chunk = [w_item]
            curr_len = len(wt)
        else:
            curr_chunk.append(w_item)
            curr_len += len(wt) + 1
            
    if curr_chunk:
        caption_chunks.append({
            "start_s": curr_chunk[0]["start_s"],
            "end_s": curr_chunk[-1]["end_s"],
            "text": " ".join(item["word"] for item in curr_chunk)
        })
        
    # 3. Write ASS file
    ass_file = shorts_dir / f"{cid}.ass"
    with open(ass_file, "w", encoding="utf-8") as f:
        f.write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Headline,Arial,78,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,8,90,90,330,1
Style: Caption,Arial,76,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,5,0,8,140,140,1320,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,{fmt_ass(dur)},Headline,,90,90,330,,{c['headline_ass']}
""")
        for chk in caption_chunks:
            # Capitalize first letter of chunk
            ctext = chk["text"]
            if ctext and ctext[0].islower():
                ctext = ctext[0].upper() + ctext[1:]
            f.write(f"Dialogue: 1,{fmt_ass(chk['start_s'])},{fmt_ass(chk['end_s'])},Caption,,140,140,1320,,{ctext}\n")
            
    # 4. Write SRT file
    srt_file = shorts_dir / f"{cid}.srt"
    with open(srt_file, "w", encoding="utf-8") as f:
        for idx, chk in enumerate(caption_chunks, 1):
            ctext = chk["text"]
            if ctext and ctext[0].islower():
                ctext = ctext[0].upper() + ctext[1:]
            f.write(f"{idx}\n{fmt_srt(chk['start_s'])} --> {fmt_srt(chk['end_s'])}\n{ctext}\n\n")
            
    # 5. Render vertical video using ffmpeg
    out_mp4 = shorts_dir / f"{cid}_vertical.mp4"
    fade_out_st = max(0.0, dur - 0.10)
    
    # Filter graph:
    # 1) scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black
    # 2) subtitles={cid}.ass
    # 3) afade in and out + loudnorm
    vf = f"scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,subtitles={cid}.ass"
    af = f"afade=t=in:ss=0:d=0.10,afade=t=out:st={fade_out_st:.3f}:d=0.10,loudnorm=I=-14:TP=-1.0:LRA=9"
    
    cmd = [
        "ffmpeg", "-y",
        "-ss", f"{t_start:.3f}",
        "-to", f"{t_end:.3f}",
        "-i", str(src_video),
        "-vf", vf,
        "-af", af,
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
    print(f"Running ffmpeg for {cid}...")
    subprocess.run(cmd, cwd=shorts_dir, check=True)
    print(f"Created {out_mp4}")
    
    # 6. Save cover frame
    cover_png = shorts_dir / f"{cid}_cover.png"
    cover_t = min(dur - 1.0, c["cover_offset_s"])
    cover_cmd = [
        "ffmpeg", "-y",
        "-ss", f"{cover_t:.2f}",
        "-i", str(out_mp4),
        "-vframes", "1",
        str(cover_png)
    ]
    subprocess.run(cover_cmd, check=True)
    print(f"Saved cover {cover_png}")
    
    clip_summaries.append({
        "id": cid,
        "path": str(out_mp4),
        "start_s": t_start,
        "end_s": t_end,
        "dur": dur,
        "first_3": first_3,
        "last_3": last_3
    })

print("\nAll vertical clips generated successfully:")
for cs in clip_summaries:
    print(f"  {cs['id']}: {cs['dur']:.2f}s, start={cs['start_s']:.2f}s, end={cs['end_s']:.2f}s")
