BRANDING PASS INSTRUCTIONS
===========================
To finalize any video for YouTube or Instagram with logo and end card:
1. Ensure assets/logo.png exists (transparent PNG, >=400px).
2. Run: python branding.py <video_path> <kind> <n>
   - <kind>: yt_full, yt_short, or insta_short
   - <n>: clip number (e.g., 1 for full video, 2, 3... for shorts)
3. Outputs are written to out/final/ (e.g., yt_full1.mp4, yt_short2.mp4).
To run all configured videos at once, run: python branding.py
All outputs are normalized to -14 LUFS, 30 fps, 1080p, with faststart.
