import os
import json
import soundfile as sf
import numpy as np
from pathlib import Path
from kokoro import KPipeline

root = Path(r"C:\Users\Asus\Downloads\yt\project_log\log_full")
voice_dir = root / "voice"
voice_dir.mkdir(parents=True, exist_ok=True)

# Load brand.json
brand_path = Path(r"C:\Users\Asus\Downloads\yt\rule to follwo\brand.json")
with open(brand_path, "r", encoding="utf-8") as f:
    brand = json.load(f)

v_cfg = brand.get("voice", {"name": "af_heart", "lang_code": "a", "speed": 1.0})
voice_name = v_cfg.get("name", "af_heart")
lang_code = v_cfg.get("lang_code", "a")
speed = float(v_cfg.get("speed", 1.0))

print(f"Initializing Kokoro pipeline: lang_code={lang_code}, voice={voice_name}, speed={speed}")
pipeline = KPipeline(lang_code=lang_code)

end_cards = brand["end_cards"]

def trim_silence(audio, sr=24000, thresh_db=-45, max_edge_silence_s=0.04):
    # Calculate energy
    thresh = 10 ** (thresh_db / 20)
    non_silent = np.where(np.abs(audio) > thresh)[0]
    if len(non_silent) == 0:
        return audio
    first_idx = max(0, non_silent[0] - int(max_edge_silence_s * sr))
    last_idx = min(len(audio), non_silent[-1] + int(max_edge_silence_s * sr))
    return audio[first_idx:last_idx]

results = {}

for variant, cfg in end_cards.items():
    text = cfg["voice_text"]
    out_wav = voice_dir / f"end_{variant}.wav"
    out_json = voice_dir / f"end_{variant}_words.json"
    print(f"\nGenerating {variant}: '{text}'")
    
    # Generate audio
    generator = pipeline(text, voice=voice_name, speed=speed, split_pattern=r'\n+')
    audio_pieces = []
    
    for gs, ps, audio in generator:
        audio_pieces.append(audio)
        
    full_audio = np.concatenate(audio_pieces) if audio_pieces else np.array([], dtype=np.float32)
    trimmed_audio = trim_silence(full_audio, sr=24000)
    dur = len(trimmed_audio) / 24000.0
    
    sf.write(str(out_wav), trimmed_audio, 24000)
    print(f"Saved {out_wav} ({dur:.3f}s)")
    
    # Word timings: estimate from text and words in spoken order
    # Words in on_screen_words_in_spoken_order
    words_spoken = text.replace(",", " ").replace(".", " ").replace("'", "'").split()
    # proportional distribution
    char_counts = [len(w) for w in words_spoken]
    total_chars = sum(char_counts)
    w_timings = []
    curr_t = 0.05
    avail_t = dur - 0.10
    for w, c in zip(words_spoken, char_counts):
        w_dur = avail_t * (c / total_chars)
        w_timings.append({
            "word": w,
            "start_s": round(curr_t, 3),
            "end_s": round(curr_t + w_dur, 3)
        })
        curr_t += w_dur
        
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({"duration_s": dur, "words": w_timings}, f, indent=2)
        
    results[variant] = {
        "duration_s": dur,
        "path": str(out_wav)
    }

print("\nAll end card voices generated:")
for k, v in results.items():
    print(f"  {k}: {v['duration_s']:.3f}s -> {v['path']}")
