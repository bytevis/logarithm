# BRIEF: Cut vertical Shorts/Reels from the finished full video

Goal: make 4 (optionally 5) vertical 1080x1920 clips from the finished full video "What a Log Actually Is", for YouTube Shorts and Instagram Reels. This is CUTTING and re-framing only. Do NOT re-render Manim scenes and do NOT change the voice.

Work independently, ask a question only if truly blocked, and list assumptions in the final report. Read `clips_plan.json` (what to cut) and follow this brief (how). The project folder is `C:\Users\Asus\Downloads\log_full\`. Use Python 3.11.9 and ffmpeg 9.0.1 (libass `subtitles` filter available). Run ffmpeg from the project folder with RELATIVE paths (a `C:\...` path breaks the `subtitles` filter).

## 1. Source and checks (report briefly)
1. Source: use `out\log_full_nocaptions.mp4` if it exists. Check one frame of it at 10 s: does it contain a bottom footer (for example "Like - Comment - Subscribe - ByteVis") or burned captions? If yes, crop them off (rule below). If `nocaptions` does not exist, use the captioned upload (1920x1080, 30 fps, 318.2 s, AAC mono) and crop.
2. Crop rule: the real content lives in y = 0 to 925 of the 1080 px frame; captions sit near y 960 and the footer near y 1060. If either exists in the source, crop to `crop=1920:925:0:0`; otherwise keep the full frame. Never keep a "Subscribe" footer in any clip.
3. Cut times come from `voice\timing.json` (take `start_s`, `speech_end_s`). If the source video length differs from `total_s + extra_hold_s` by more than 0.1 s, STOP and report (the timing file would not match this video). Silence markers in the upload (about): 15.3 s end of hook, 70.0 s end of the challenge pause, 81 s end of the idea section, 126 s end of the graph, 204.5 s end of the pattern section, 252 s end of the scales.
4. Risky frames: extract and LOOK at frames in the middle of takes t36 and t38 (around 256 s and 272 s). In the upload, the text "Paper: about 0.1 mm" was cut off at the left edge, "Moon: about 384,400 km" at the right edge, and the 40-folds row overlapped "110,000 km". Report whether this is still the case. If yes, mark clip A as BLOCKED, still make clips B, C, D, and tell me.

## 2. Cutting (frame-accurate, no clipped words)
- Start = first take's `start_s` minus 0.05 s. End = last take's `speech_end_s` plus 0.12 s. Do NOT include the pause after the last take.
- Re-encode (never `-c copy`) so cuts are frame-accurate. Fade audio in over 0.10 s at the start and out over 0.10 s at the end.
- Clip A has two segments (t01 to t03, then t36 to t40). Join them with a 0.25 s video crossfade (`xfade`) and a 0.25 s audio crossfade (`acrossfade`).
- Check every clip against `out\words\full.json`: print the first 3 and last 3 spoken words of each clip. They must be whole words from the planned takes.

## 3. Vertical layout ("A_letterbox_vertical")
The video has a pure black background, so a letterbox looks natural. Build a 1080x1920 black canvas:
- Scale the (cropped) source to width 1080 (`scale=1080:-2`), do NOT zoom or crop the sides, and center it vertically (`pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black`). Keep 30 fps.
- Top zone (above the video): the clip headline from `clips_plan.json`, burned in. Arial Bold 78, white, with the key word in yellow if easy, max 2 lines, centered, horizontal margins 90 px. Place its top at about y = 330 (keeps it below the Shorts/Reels top bar). Visible for the whole clip.
- Captions (below the video): word-timed from `out\words\full.json`, chunks of at most 4 words (about 24 characters), shown only while spoken, Arial Bold 76, white, black outline 5, no box, centered, top of caption at about y = 1320 (below the video band, above the bottom 300 px that Shorts and Reels cover with their buttons). Keep ALL text out of the bottom 300 px and out of the right 140 px.
- Build both with ONE ASS file per clip (`PlayResX=1080, PlayResY=1920`): style `Headline` with Alignment=8 and MarginV=330, style `Caption` with Alignment=8 and MarginV=1320. Burn with `ffmpeg -vf "...,subtitles=clip.ass"` run from the folder containing the file. Use proper capitalization and punctuation taken from `script.json`, not the raw lowercase transcript. Also write a `.srt` per clip.
- Banned words anywhere (headline, captions, file names): "binary", "merge", "sort", "subscribe", "Video 1", "Video 2". No call-to-action text.

## 4. Audio and export
- Normalize each clip to -14 LUFS, true peak -1.0 (`loudnorm=I=-14:TP=-1.0:LRA=9`). Do not otherwise change the voice.
- Output to `out\shorts\`: `<clip_id>_vertical.mp4` (1080x1920, 30 fps, H.264, yuv420p, AAC 192k, `-movflags +faststart`) plus `<clip_id>.srt`. Make clips in priority order (A, B, C, D, then E only if time allows).
- Also save a cover frame `<clip_id>_cover.png` (1080x1920) from the most readable moment of the clip.

## 5. Quality checks (do these yourself)
- Duration within 1 s of `est_duration_s` in the plan; every clip is under 60 s except if the plan says otherwise.
- `silencedetect` (noise -45 dB, d 0.6): report any silence of 0.6 s or more (expected: none; clip B may have the 1.6 s challenge pause, which is fine).
- Look at 4 frames per clip (start +0.5 s, 1/3, 2/3, end -0.5 s): headline readable, captions readable, nothing cut off, nothing in the bottom 300 px or right 140 px.
- Banned-word search over the ASS and SRT files, zero matches.

## 6. Final report (short, no long logs)
For each clip: file path, start and end seconds in the source, duration, first and last 3 words, any problem found. Then: whether clip A is blocked, what source you used (nocaptions or crop), and anything I should check by eye or ear (list the 3 riskiest moments).
