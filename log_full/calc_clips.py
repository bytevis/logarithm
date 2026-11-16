import json
from pathlib import Path

root = Path(r"C:\Users\Asus\Downloads\yt\project_log\log_full")
with open(root / "voice" / "timing.json", "r", encoding="utf-8") as f:
    timing = json.load(f)

takes_by_id = {}
for s in timing["sections"]:
    for t in s["takes"]:
        takes_by_id[t["id"]] = t

with open(root / "out" / "words" / "full.json", "r", encoding="utf-8") as f:
    words = json.load(f)

clips = {
    "A_paper_to_moon": [("t01", "t03"), ("t36", "t40")],
    "B_log_challenge": [("t09", "t14")],
    "C_numbers_start_with_1": [("t22", "t27")],
    "D_log_scales": [("t31", "t34")],
    "E_log_graph": [("t16", "t21")],
}

for cid, segs in clips.items():
    print(f"--- {cid} ---")
    tot_dur = 0
    for seg_idx, (t_start_id, t_end_id) in enumerate(segs):
        t_start = takes_by_id[t_start_id]["start_s"] - 0.05
        t_end = takes_by_id[t_end_id]["speech_end_s"] + 0.12
        dur = t_end - t_start
        tot_dur += dur
        # Find words in this range
        clip_words = [w for w in words if w["start_s"] >= t_start - 0.1 and w["end_s"] <= t_end + 0.1]
        first_3 = " ".join(w["word"] for w in clip_words[:3])
        last_3 = " ".join(w["word"] for w in clip_words[-3:])
        print(f"  Segment {seg_idx}: {t_start_id}..{t_end_id} -> start={t_start:.3f}, end={t_end:.3f}, dur={dur:.3f}s")
        print(f"     first 3: '{first_3}'")
        print(f"     last 3:  '{last_3}'")
    print(f"  Total duration: {tot_dur:.3f}s")
