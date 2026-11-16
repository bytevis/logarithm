# BRIEF: Build "What a Log Actually Is" (full YouTube video, 16:9, about 6 minutes)

You are building a finished, highly visual 3Blue1Brown-style explainer: black background, shapes, graphs that move to show the idea. You do EVERYTHING: generate the voice, build the Manim animation synced to that voice, make captions, export the final MP4.

Work independently. Ask me a question only if truly blocked; otherwise decide, continue, and list assumptions in the final report. The narration in `script.json` is FINAL: do not rewrite it. MATH ACCURACY IS CRITICAL: run `python fact_check.py` first and again before the final render; it must print ALL FACTS OK.

Files you were given (put them in the project folder): `script.json`, `storyboard.md`, `fact_sheet.json`, `fact_check.py`, `brief.md`.

## 0. My laptop (already inspected, do not re-inspect)
- Windows, user `C:\Users\Asus` (ASCII path, no spaces). Intel i5-12500H (16 threads), 15.7 GB RAM (only about 4.8 GB free: be careful), NO NVIDIA GPU (everything runs on CPU), 270 GB free disk.
- Use ONLY Python 3.11.9: `C:\Users\Asus\AppData\Local\Programs\Python\Python311\python.exe` (the default `python`). Python 3.14 has no Manim, never use it.
- Installed and usable: manim 0.22.1, kokoro 0.9.4 (+ misaki, espeakng-loader), numpy, scipy, soundfile, pydub, librosa, pillow, opencv, torch (CPU), ffmpeg + ffprobe 9.0.1 (with libass `subtitles` filter), VLC.
- NOT installed: faster-whisper, stable-ts, moviepy, SoX. Do not use moviepy or SoX. Install `faster-whisper` ONLY if Kokoro word timings are unavailable (section 2.5).
- Do NOT use LaTeX even though MiKTeX exists (no MathTex/Tex/DecimalNumber/Integer). Use `Text` only.
- Fonts available: Segoe UI Bold, Arial Bold, Calibri Bold, Verdana Bold. DejaVu Sans, Montserrat, Inter, Roboto are NOT installed. Use "Segoe UI" for Manim text and Arial (bold) for captions.
- Existing folders `StoryChannel` and `shot` are other projects: do not touch them and do not reuse their code. There is no `common.py` to reuse: write a new one.
- Shell quoting: you are on Windows. Prefer `python script.py` over shell one-liners. For ffmpeg, run from the project folder and use RELATIVE paths (a path such as `C:\...` breaks the `subtitles` filter).

## 1. Project folder and first steps
Create `C:\Users\Asus\Downloads\log_full\` with subfolders `voice\`, `out\`, `out\words\`, `out\sections\`, `scenes\`. Copy the five given files into the root.
1. `python fact_check.py` must print ALL FACTS OK.
2. Print `python --version`, `manim --version`, `ffmpeg -version | first line`, and confirm `ffmpeg -filters` lists `subtitles`. Report in one line each. Fix what you can; if impossible, stop and report exactly what is missing.

## 2. Voice generation (BEFORE any animation)
Voice: Kokoro `af_heart`, `KPipeline(lang_code='a')`, 24000 Hz mono. The voice already exists in Kokoro; just synthesize.

Procedure:
1. Read `script.json` (sections, then takes). Use each take's `speed` and `pause_after_s` exactly as given (modes: H hook, N normal, E emphasis, S slow). Takes marked `section_end` already include the extra section pause. The take marked `challenge_pause` has a 1.6 s pause on purpose (on-screen countdown).
2. For each take: `pipeline(text, voice='af_heart', speed=<speed>)`, concatenate chunks (`np.asarray`). Trim leading and trailing silence of the take to at most 0.04 s (threshold about -45 dB). Do NOT add silence inside a take.
3. Place takes back to back in ONE file `voice/full.wav`: speech, then `pause_after_s` seconds of zeros, next take. Do this on CPU; it takes a few minutes. Process take by take and do not keep everything in RAM longer than needed.
4. Do NOT change speeds to hit a length. Expected total about 5:50 to 6:30 including pauses. Report the real value.
5. WORD TIMINGS (needed for cues "at 'word'" in the storyboard). Try Kokoro first: each result from `KPipeline` has `result.tokens` with `start_ts` / `end_ts` in seconds for English; convert to take-relative times, then to scene times (account for the trim). If these are missing or look wrong, install `faster-whisper` and run it on `voice/full.wav` with model `small`, `compute_type="int8"`, `device="cpu"`, `word_timestamps=True`. Save to `out/words/full.json` as a list of `{take, word, start_s, end_s}`. If neither works, split each take's time span proportionally by syllables and say so in the report.
6. Write `voice/timing.json`: `{"voice","sample_rate","total_s","extra_hold_s":1.0,"sections":[{"id","start_s","end_s","takes":[{"id","mode","speed","pause_after_s","start_s","speech_end_s","end_s","text"}]}]}`. Times rounded to ms. `end_s` of a take includes its pause. Section `start_s` = start of its first take, `end_s` = start of the next section (last section: `total_s + extra_hold_s`).
7. Voice QC table: words per second per take (flag outside 2.0 to 3.6), no NaN, peak below 0.99. Copy `voice/full.wav` to `voice/preview.wav` so I can listen.
8. The voice is then FIXED. Never edit the WAV. If I change the voice later, only this step is re-run; animations read `timing.json` and re-sync.

## 3. Sync system (`common.py`)
Write `common.py` with:
- `config.pixel_width=1920; config.pixel_height=1080; config.frame_rate=30` (set before any scene), black background.
- Color constants and helpers per `storyboard.md` section 0. Helpers: `log_label(base, arg, ...)` (white "log", small blue base shifted down-right at about 55% size, then the argument), `pow_label(base, exp)`, `ruler(...)`, `bar_chart(...)`, `PaperStack`, `MoonIcon`, `tile(text, color)`.
- `VoiceScene(Scene)` with its OWN clock `self.t`, reading `voice/timing.json` (env `TIMING_JSON`) and `out/words/full.json`. Methods: `hold_until(t)`, `act(t, *animations, run_time=...)`, `step(dt)`, `take_start(id)`, `take_end(id)`, `word_time(take_id, word, occurrence=1)`, `finish()`. Every animation has an explicit `run_time`. Each section scene starts its clock at the section's `start_s` and must end exactly at the section's end.
- Never hard-code absolute seconds. Anchor every cue to a take start/end plus an offset, or to `word_time`.
- Safety: if a cue time has already passed, play the animation instantly (do not let the clock go backwards or crash).

## 4. Rendering (memory-safe, per section)
RAM is limited, so render ONE Scene class per section (`S1Hook`, `S2Idea`, `S3Graph`, `S4Pattern`, `S5Scales`, `S6Payoff`, files in `scenes\`) and concatenate. Do not make one giant scene.
- Frame-exact boundaries: `b[i] = round(section_start_s * 30) / 30`. Section video i must be exactly `b[i+1] - b[i]` long (last section: until `total_s + extra_hold_s`). Pad with a held last frame if needed.
- Dev renders with `-ql` (check sync and layout), final with `-r 1920,1080 --fps 30` (`-qh` style 1080p30 is enough; do not render 60 fps).
- Render sections in order. After each section render, extract 3 frames (section start +0.4 s, middle, end -0.4 s) with ffmpeg and LOOK at them. Fix overlaps, cut-off text, text smaller than 36 px-equivalent, anything in the caption band (y < -2.9), anything outside x in [-6.4, 6.4].
- Concatenate the silent section MP4s with the ffmpeg concat demuxer (`-c copy` if codecs match, otherwise re-encode H.264). Transitions between sections are inside the scenes (0.4 s crossfade/slide), not hard cuts.
- Do not leave `media\` junk growing: delete partial movie files after a successful concat if disk or time becomes an issue.

## 5. Mux, loudness, captions, export
1. Mux: video from the concat, audio from `voice/full.wav` padded with silence to `total_s + extra_hold_s` (`-af apad -t <TOTAL>`). Video length must equal `total_s + extra_hold_s` within 1 frame.
2. Loudness: normalize audio to -14 LUFS, true peak -1.0 (`loudnorm=I=-14:TP=-1.0:LRA=9`). The voice itself is not otherwise edited.
3. Captions (optional version): build from the word timings. Chunk into lines of at most 7 words (about 38 characters), shown only while spoken. Write `out/captions.srt` and `out/captions.ass` (`PlayResX=1920, PlayResY=1080`, Fontname Arial, Bold, Fontsize 56, white text, black outline 4, no box, Alignment=2, MarginV=40, MarginL/R=200). Burn in with `ffmpeg -vf "subtitles=captions.ass"` run from the `out` folder with RELATIVE paths.
4. Outputs: `out/log_full_nocaptions.mp4` and `out/log_full_captions.mp4`, H.264 yuv420p, 1920x1080, 30 fps, AAC 192k.
5. Write `out/chapters.txt`: YouTube chapter lines (`0:00 Title`, first must be 0:00, at least 3 chapters, each at least 10 s) from the section starts in `timing.json`, with these titles: `The Moon question`, `What a log is`, `The graph`, `The strange pattern`, `Logs in real life`, `The payoff`.

## 6. Hard rules
- ON-SCREEN TEXT: only what `storyboard.md` allows. No extra numbers or claims. "≈" always shown for approximate values. The base 2 (and base 10) must ALWAYS appear with every `log` equation (use `log_label`).
- BANNED words anywhere in the project (script, scene code, captions): "binary", "merge", "sort", "subscribe", "Video 1", "Video 2". Confirm zero matches at the end (search script.json, scenes\, common.py, out\captions.*; skip brief.md and storyboard.md, which list the words on purpose).
- No music, no external assets, no copyrighted material. Draw all icons from primitives.
- Colors and text sizes per `storyboard.md` section 0. Nothing smaller than 36. Captions band y < -2.9 kept EMPTY in Manim.
- Continuous motion: something visibly changes at least every 1.5 s; no picture frozen more than 2.0 s except the final 1.0 s hold. Pauses in the voice are short on purpose (the previous video had too many); never lengthen them.
- The answer "42" is hidden until take t40 (see storyboard). The hook shows only the counter up to 7 folds, then "?".

## 7. Work plan
1. Setup, fact check, environment line. 2. Voice + QC + `timing.json` + word timings; tell me the final length. 3. `common.py` + a tiny test scene (3 seconds) to verify the clock. 4. Build S1 and S2, render `-ql`, check frames. 5. Build S3 to S6, render `-ql`, check frames. 6. Final renders per section at 1080p30, concat, mux, loudness, captions, chapters. 7. Quality checks. 8. Report.

## 8. Quality checks (do these yourself)
- Math: every number on screen matches `fact_sheet.json`. The seismograph traces have max amplitudes 0.15 and 1.5. The tile counts match: 3 twos for 8, 5 twos for 32.
- `ffmpeg -i out/log_full_nocaptions.mp4 -af silencedetect=noise=-45dB:d=0.6 -f null -`: report silences of 0.6 s or more (expected: only the 1.6 s challenge pause and the final hold).
- `freezedetect` (n=-55dB, d=2.0) on the video: report any frozen stretch longer than 2.0 s and fix it by adding purposeful motion (except the final 1.0 s).
- Total length equals `total_s + extra_hold_s` within 1 frame. Audio is the original WAV (only loudness-normalized).
- Search for banned words (section 6), skipping brief.md and storyboard.md.

## 9. Final report (short, no long logs)
Files (full paths), final length, per-section lengths, voice QC table, how word timings were obtained, silence and freeze check results, banned-word search result, deviations and assumptions, and anything I should check by eye or ear (list the 3 riskiest moments).
