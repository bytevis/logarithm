import json
import soundfile as sf
import numpy as np
from pathlib import Path
from kokoro import KPipeline

root = Path(r"C:\Users\Asus\Downloads\log_full\short_video")
root.mkdir(parents=True, exist_ok=True)

with open(root / "short_script.json", "r", encoding="utf-8") as f:
    takes = json.load(f)

pipeline = KPipeline(lang_code='a')

full_audio = []
all_words = []
curr_s = 0.0

print(f"Synthesizing {len(takes)} takes for short video...")

for t in takes:
    t_id = t["id"]
    text = t["text"]
    speed = float(t["speed"])
    pause_after_s = float(t["pause_after_s"])
    
    t_audio_chunks = []
    t_tokens = []
    
    for result in pipeline(text, voice='af_heart', speed=speed):
        t_audio_chunks.append(result.audio)
        if result.tokens:
            t_tokens.extend(result.tokens)
            
    t_wav = np.concatenate(t_audio_chunks)
    
    # Trim silence (threshold -45dB)
    thresh = 0.0056
    non_silent = np.where(np.abs(t_wav) > thresh)[0]
    if len(non_silent) > 0:
        start_trim = max(0, non_silent[0] - int(0.02 * 24000))
        end_trim = min(len(t_wav), non_silent[-1] + int(0.02 * 24000))
        trimmed_wav = t_wav[start_trim:end_trim]
        trim_offset_s = start_trim / 24000.0
    else:
        trimmed_wav = t_wav
        trim_offset_s = 0.0
        
    speech_dur = len(trimmed_wav) / 24000.0
    
    # Process word tokens
    for tok in t_tokens:
        tok_txt = tok.text.strip().lower()
        if tok_txt and tok.start_ts is not None and tok.end_ts is not None:
            w_start = max(0.0, tok.start_ts - trim_offset_s)
            w_end = min(speech_dur, tok.end_ts - trim_offset_s)
            if w_end > w_start:
                all_words.append({
                    "take": t_id,
                    "word": tok.text.strip(),
                    "start_s": round(curr_s + w_start, 3),
                    "end_s": round(curr_s + w_end, 3)
                })
                
    full_audio.append(trimmed_wav)
    t["start_s"] = round(curr_s, 3)
    t["speech_end_s"] = round(curr_s + speech_dur, 3)
    
    # Add pause
    pause_samples = int(pause_after_s * 24000)
    if pause_samples > 0:
        full_audio.append(np.zeros(pause_samples, dtype=np.float32))
        
    curr_s += speech_dur + pause_after_s
    t["end_s"] = round(curr_s, 3)
    print(f"Take {t_id}: speech {speech_dur:.2f}s, pause {pause_after_s:.2f}s -> end at {curr_s:.2f}s")

# Final 1.0s hold
hold_samples = int(1.0 * 24000)
full_audio.append(np.zeros(hold_samples, dtype=np.float32))
final_total_s = curr_s + 1.0

final_wav = np.concatenate(full_audio)
sf.write(str(root / "short_voice.wav"), final_wav, 24000)
print(f"Written {root / 'short_voice.wav'} - total {final_total_s:.3f}s")

with open(root / "short_timing.json", "w", encoding="utf-8") as f:
    json.dump({
        "total_s": round(curr_s, 3),
        "extra_hold_s": 1.0,
        "final_total_s": round(final_total_s, 3),
        "takes": takes
    }, f, indent=2)

with open(root / "short_words.json", "w", encoding="utf-8") as f:
    json.dump(all_words, f, indent=2)

print("Short voice generation complete!")
