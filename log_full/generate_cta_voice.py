import os
import soundfile as sf
import numpy as np
from pathlib import Path
from kokoro import KPipeline

cta_dir = Path(r"C:\Users\Asus\Downloads\log_full\cta_clips")
cta_dir.mkdir(parents=True, exist_ok=True)

pipeline = KPipeline(lang_code='a')

# 1. Like, subscribe, and comment!
print("Synthesizing CTA 1: Like, subscribe, and comment...")
chunks1 = []
for result in pipeline("Like, subscribe, and comment!", voice='af_heart', speed=1.05):
    chunks1.append(result.audio)
audio1 = np.concatenate(chunks1)
# Trim silence
thresh = 0.01
idx = np.where(np.abs(audio1) > thresh)[0]
if len(idx) > 0:
    audio1 = audio1[idx[0]:idx[-1]+1]

# Pad to exactly 3.0 seconds (24000 * 3 = 72000 samples)
target_samples = 24000 * 3
if len(audio1) < target_samples:
    pad_left = int(24000 * 0.2)
    pad_right = target_samples - len(audio1) - pad_left
    if pad_right < 0:
        pad_left = target_samples - len(audio1)
        pad_right = 0
    audio1 = np.pad(audio1, (pad_left, pad_right), mode='constant')
else:
    audio1 = audio1[:target_samples]

sf.write(str(cta_dir / "cta1.wav"), audio1, 24000)
print(f"Written {cta_dir / 'cta1.wav'}")

# 2. Follow, comment, and subscribe!
print("Synthesizing CTA 2: Follow, comment, and subscribe...")
chunks2 = []
for result in pipeline("Follow, comment, and subscribe!", voice='af_heart', speed=1.05):
    chunks2.append(result.audio)
audio2 = np.concatenate(chunks2)
# Trim silence
idx = np.where(np.abs(audio2) > thresh)[0]
if len(idx) > 0:
    audio2 = audio2[idx[0]:idx[-1]+1]

if len(audio2) < target_samples:
    pad_left = int(24000 * 0.2)
    pad_right = target_samples - len(audio2) - pad_left
    if pad_right < 0:
        pad_left = target_samples - len(audio2)
        pad_right = 0
    audio2 = np.pad(audio2, (pad_left, pad_right), mode='constant')
else:
    audio2 = audio2[:target_samples]

sf.write(str(cta_dir / "cta2.wav"), audio2, 24000)
print(f"Written {cta_dir / 'cta2.wav'}")
