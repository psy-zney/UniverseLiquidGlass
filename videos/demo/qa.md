# QA — rendered and reviewed

- PASS: MP4/H.264, 1600×900, 24 fps, 53.5 seconds, 1,702,824 bytes, no audio by design.
- PASS: all nine native CSS celestial event chapters captured; sampled midpoint PNGs retained locally in ignored `renders/`.
- PASS: decoded video frames show moving sidebar light (mean delta 3.406) and top-edge light (4.696) across the neutron chapter.
- PASS: decoded frames show changed native tab selection (mean delta 19.706) between Reading and Workspace.
- PASS: visually reviewed intro, black hole, neutron star, tab switch, Downloads and final installation frame; no personal account content.
- PASS: native Downloads uses local synthetic fixtures; short placeholder file sizes are expected.
- PASS: recorder verifies the exact profile path before modifying or capturing; launcher closes only its unique headless profile.
- NOTE: native compact top bar is collapsed, so light is visible in the exposed top edge. Full-width events remain native theme backgrounds.
- NOTE: each event's original timing is sampled into a 3.5-second chapter; this is an edited showcase, not an uncut real-time recording.
- NOTE: the loading chapter toggles the native busy state rather than downloading over the network.

## Event close-up edit — 2026-10-18

- The original native capture is preserved locally as ignored `renders/native-original.mp4`.
- PASS: nine event scenes include a tracked 2.3× detail panel with eased opacity transitions.
- PASS: visually inspected black-hole, comet and nebula detail crops plus the full-window Reading tab scene.
- PASS: detail labels stay inside their panel and the main event title remains visible.
- NOTE: close-ups magnify existing native footage; they do not add detail absent from the source. Theme CSS is unchanged.
