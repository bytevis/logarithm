import os
import sys
import json
import shutil
import numpy as np
import soundfile as sf
from pathlib import Path
from kokoro import KPipeline

root = Path(r"C:\Users\Asus\Downloads\log_full")
voice_dir = root / "voice"
words_dir = root / "out" / "words"
voice_dir.mkdir(parents=True, exist_ok=True)
words_dir.mkdir(parents=True, exist_ok=True)

with open(root / "script.json", "r", encoding="utf-8") as f:
    script_data = json.load(f)

extra_hold_s = script_data.get("extra_hold_s", 1.0)
sr = 24000
thresh = 10 ** (-45 / 20)  # ~0.005623
max_pad_samples = int(0.04 * sr)  # 960 samples

print("Initializing Kokoro pipeline...")
pipeline = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M')

full_audio_chunks = []
words_full = []
timing_sections = []
qc_table = []

current_time = 0.0

total_takes = sum(len(sec["takes"]) for sec in script_data["sections"])
print(f"Total sections: {len(script_data['sections'])}, Total takes: {total_takes}")

for s_idx, sec in enumerate(script_data["sections"]):
    sec_id = sec["id"]
    sec_takes = []
    sec_start_s = current_time
    
    print(f"\nProcessing Section {sec_id}...")
    
    for t_idx, take in enumerate(sec["takes"]):
        t_id = take["id"]
        t_text = take["text"]
        t_speed = take["speed"]
        t_pause = take["pause_after_s"]
        t_mode = take["mode"]
        
        # Synthesize with Kokoro
        results = list(pipeline(t_text, voice='af_heart', speed=t_speed))
        
        take_audio_chunks = []
        raw_tokens = []
        chunk_offset_samples = 0
        
        for r in results:
            aud = r.output.audio.cpu().numpy()
            take_audio_chunks.append(aud)
            
            chunk_time_offset = chunk_offset_samples / sr
            if r.tokens:
                for tok in r.tokens:
                    clean_t = tok.text.strip()
                    # Skip pure punctuation
                    if clean_t and any(c.isalnum() for c in clean_t):
                        raw_tokens.append({
                            "word": clean_t,
                            "raw_start": chunk_time_offset + tok.start_ts,
                            "raw_end": chunk_time_offset + tok.end_ts
                        })
            chunk_offset_samples += len(aud)
            
        concat_raw = np.concatenate(take_audio_chunks) if take_audio_chunks else np.zeros(0, dtype=np.float32)
        
        # Trim leading and trailing silence
        abs_aud = np.abs(concat_raw)
        active = np.where(abs_aud >= thresh)[0]
        
        if len(active) > 0:
            first_idx = active[0]
            last_idx = active[-1]
            start_idx = max(0, first_idx - max_pad_samples)
            end_idx = min(len(concat_raw), last_idx + max_pad_samples)
            trimmed_audio = concat_raw[start_idx:end_idx]
            trim_offset_s = start_idx / sr
        else:
            trimmed_audio = concat_raw
            trim_offset_s = 0.0
            
        speech_dur = len(trimmed_audio) / sr
        t_start = current_time
        t_speech_end = t_start + speech_dur
        t_end = t_speech_end + t_pause
        
        # Adjust tokens to full timeline
        for tok in raw_tokens:
            rel_start = max(0.0, tok["raw_start"] - trim_offset_s)
            rel_end = min(speech_dur, tok["raw_end"] - trim_offset_s)
            words_full.append({
                "take": t_id,
                "word": tok["word"],
                "start_s": round(t_start + rel_start, 3),
                "end_s": round(t_start + rel_end, 3)
            })
            
        # Append audio + silence pause
        full_audio_chunks.append(trimmed_audio)
        pause_samples = int(t_pause * sr)
        if pause_samples > 0:
            full_audio_chunks.append(np.zeros(pause_samples, dtype=np.float32))
            
        sec_takes.append({
            "id": t_id,
            "mode": t_mode,
            "speed": t_speed,
            "pause_after_s": t_pause,
            "start_s": round(t_start, 3),
            "speech_end_s": round(t_speech_end, 3),
            "end_s": round(t_end, 3),
            "text": t_text
        })
        
        # QC metrics
        word_count = len([w for w in t_text.split() if any(c.isalnum() for c in w)])
        wps = word_count / speech_dur if speech_dur > 0 else 0
        peak = float(np.max(abs_aud)) if len(abs_aud) > 0 else 0
        has_nan = bool(np.isnan(concat_raw).any())
        flag = "OK" if (2.0 <= wps <= 3.6) else "FLAG"
        
        qc_table.append({
            "take": t_id,
            "words": word_count,
            "speech_dur": round(speech_dur, 2),
            "wps": round(wps, 2),
            "peak": round(peak, 3),
            "has_nan": has_nan,
            "flag": flag
        })
        
        print(f"  Take {t_id}: {speech_dur:.2f}s speech + {t_pause:.2f}s pause -> [{t_start:.2f}s - {t_end:.2f}s] ({wps:.2f} wps, peak {peak:.2f}, {flag})")
        current_time = t_end
        
    timing_sections.append({
        "id": sec_id,
        "start_s": round(sec_start_s, 3),
        "end_s": 0.0, # to be set next
        "takes": sec_takes
    })

# Set section end_s
for i in range(len(timing_sections)):
    if i < len(timing_sections) - 1:
        timing_sections[i]["end_s"] = timing_sections[i + 1]["start_s"]
    else:
        timing_sections[i]["end_s"] = round(current_time + extra_hold_s, 3)

total_audio = np.concatenate(full_audio_chunks)
total_dur = len(total_audio) / sr

print(f"\nTotal speech + pauses duration: {total_dur:.2f}s ({total_dur/60:.2f} mins)")
print(f"Total with extra_hold_s (1.0s): {total_dur + extra_hold_s:.2f}s ({(total_dur + extra_hold_s)/60:.2f} mins)")

# Write audio files
out_wav = voice_dir / "full.wav"
sf.write(str(out_wav), total_audio, sr)
preview_wav = voice_dir / "preview.wav"
shutil.copy2(out_wav, preview_wav)
print(f"Saved {out_wav} and {preview_wav}")

# Write timing.json
timing_data = {
    "voice": "af_heart",
    "sample_rate": sr,
    "total_s": round(total_dur, 3),
    "extra_hold_s": extra_hold_s,
    "sections": timing_sections
}

with open(voice_dir / "timing.json", "w", encoding="utf-8") as f:
    json.dump(timing_data, f, indent=2)
print("Saved voice/timing.json")

# Write out/words/full.json
with open(words_dir / "full.json", "w", encoding="utf-8") as f:
    json.dump(words_full, f, indent=2)
print(f"Saved out/words/full.json ({len(words_full)} words)")

# QC Summary
flagged = [q for q in qc_table if q["flag"] != "OK"]
print("\n=== VOICE QC SUMMARY ===")
print(f"Total takes: {len(qc_table)}")
print(f"Flagged takes (wps outside 2.0-3.6): {len(flagged)}")
for q in flagged:
    print(f"  Take {q['take']}: {q['wps']} wps ({q['words']} words in {q['speech_dur']}s)")
max_peak = max(q["peak"] for q in qc_table)
print(f"Max peak across all takes: {max_peak:.3f} (must be < 0.99)")
any_nan = any(q["has_nan"] for q in qc_table)
print(f"Any NaN detected: {any_nan}")
