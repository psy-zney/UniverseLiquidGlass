# Universe Liquid Glass

A deep black cosmic theme for Zen Browser: irregular twinkling stars, nine celestial events and bright liquid glass tabs.

[Download](https://github.com/psy-zney/UniverseLiquidGlass/releases/latest) · [Native demo video](media/theme-demo.mp4) · [Tiếng Việt](../README.md)

## Video demo

https://github.com/user-attachments/assets/b9ad681a-715a-4570-aad6-3a52f168c637

*53.5 seconds: all nine celestial events, sidebar tab switching, loading and Downloads. [Download MP4](media/theme-demo.mp4) · [Vietnamese subtitles](media/theme-demo.vi.srt).*

## Windows installation

1. Download and extract the ZIP from Releases.
2. If you have multiple profiles, find the intended **Root Directory** in `about:profiles`.
3. Close Zen completely, then run `install.cmd`.
4. Reopen Zen with a dark appearance and expanded vertical tabs.

For a specific profile:

```powershell
.\install.cmd -ProfilePath "C:\path\to\your\Zen\profile"
```

The installer backs up your CSS and user.js, stores the theme in `chrome/UniverseLiquidGlass/`, adds imports and enables legacy profile CSS. Existing custom CSS is preserved and may override the theme. A locked profile is rejected; the installer never closes your browser.

Uninstall while Zen is closed using `uninstall.cmd` with the same optional `-ProfilePath`. Backups and unrelated CSS remain intact.

## Manual installation

Copy both files from `theme/` to your profile's `chrome/UniverseLiquidGlass/`. Add these imports at the start of the corresponding entry files (after `@charset`, if present):

```css
/* chrome/userChrome.css */
@import url("UniverseLiquidGlass/userChrome.css");

/* chrome/userContent.css */
@import url("UniverseLiquidGlass/userContent.css");
```

Set `toolkit.legacyUserProfileCustomizations.stylesheets` to `true` in `about:config`, then restart Zen.

Tested on Zen 1.23.2b for Windows. Manual macOS/Linux installation is documented but untested. This repository is not an official Zen Mods store submission.

## Events and video

Comet, star, planet, white dwarf, black hole, neutron star, nebula, blue star and galaxy. Light follows each source behind controls; a local SVG simulation provides black-hole lensing. The sidebar loop lasts 70 seconds, the top loop 84 seconds.

The silent 54-second video captures actual isolated Zen chrome, sample pages, real sidebar tab switches, a controlled native loading state and synthetic Downloads entries. Event timing is edited for a compact showcase. See [video source](../videos/demo/).

## Build

Python 3.10+; no third-party packages required for CSS generation:

```sh
python scripts/build.py
```

Windows installer tests: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/test-install.ps1`.

Theme selectors can change with Zen updates. Blur/animation costs depend on your GPU. The theme fixes tested Zen panels and native select popup contrast; arbitrary website color combinations are not globally rewritten. Gravitational lensing is illustrative, not a complete physical simulation.

MIT — psy-zney.
