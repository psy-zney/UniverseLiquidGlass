# Reproduce the native Zen demo

The released video is in [`docs/media/theme-demo.mp4`](../../docs/media/theme-demo.mp4), with optional [Vietnamese subtitles](../../docs/media/theme-demo.vi.srt). It is silent by design.

## Windows capture

Install Python 3.10+ and `imageio-ffmpeg`, plus Zen Browser. Build the theme first:

```powershell
python scripts/build.py
python -m pip install -r videos/demo/source/requirements.txt
powershell -NoProfile -ExecutionPolicy Bypass -File videos/demo/source/record.ps1
```

Pass `-Python` or `-Zen` to `record.ps1` if those executables are installed elsewhere. Local Marionette port 2839 must be free.

The launcher creates a unique profile under ignored `renders/`, enables legacy CSS and starts headless Zen. The renderer verifies that profile path, loads only local demo pages, uses native tab clicks, samples CSS animation clocks at the frame times in `timeline.json`, and encodes the real browser screenshots with FFmpeg. At the end the launcher closes only its own profile. Personal Zen sessions are not used.

`render.py` saves the untouched capture as `renders/native-original.mp4`. The launcher then runs `edit.py` to produce the final `docs/media/theme-demo.mp4`. While each celestial source is visible, a fading **2.3× detail panel** follows its vertical path. The full native window stays visible behind the close-up; tab switching, loading, Downloads and installation scenes have no magnification panel. This is a video edit, not a change to browser behavior.

To repeat only the edit from an existing native capture:

```powershell
python videos/demo/source/edit.py
```

Use `--input`, `--output` and optionally `--font` for explicit paths. The original capture remains available locally and is ignored by Git.

The sidebar is set to 292 px for the recording; this width is not forced by the installed theme. Timing is edited: nine events each get a 3.5-second chapter, followed by tab switching, a controlled native loading state, synthetic Downloads fixtures and installation steps. The original sidebar loop is 70 seconds and the top loop 84 seconds.

`timeline.json` is the timing source. `brief.md`, `outline.md`, `storyboard.md`, `script.md`, `asset-manifest.json` and `qa.md` describe the delivered render. Intermediate captures and profiles are ignored by Git.
