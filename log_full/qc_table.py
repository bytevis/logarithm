import json
import soundfile as sf
import numpy as np

with open(r"C:\Users\Asus\Downloads\log_full\voice\timing.json", "r", encoding="utf-8") as f:
    d = json.load(f)

wav, sr = sf.read(r"C:\Users\Asus\Downloads\log_full\voice\full.wav")
has_nan = np.isnan(wav).any()
peak = float(np.max(np.abs(wav)))
print(f"Global Voice QC: sr={sr}, has_nan={has_nan}, peak={peak:.4f} (limit < 0.99)")

takes = [t for s in d["sections"] for t in s["takes"]]
print(f"\nTotal takes: {len(takes)}")
print("| Take | Mode | Speed | Words | Speech Dur (s) | WPS | Flag |")
print("|---|---|---|---|---|---|---|")
for t in takes:
    num_words = len(t["text"].split())
    dur = t["speech_end_s"] - t["start_s"]
    wps = num_words / dur if dur > 0 else 0
    flag = "OK" if 2.0 <= wps <= 3.6 else "FLAG"
    print(f"| {t['id']} | {t['mode']} | {t['speed']} | {num_words} | {dur:.2f} | {wps:.2f} | {flag} |")
