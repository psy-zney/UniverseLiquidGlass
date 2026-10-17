# Official Zen Mods submission status

Verified on **2026-10-18**.

## Connection

The local repository has an additional remote named `zen-store`, pointing to the official repository:

```sh
git remote add zen-store https://github.com/zen-browser/theme-store.git
git ls-remote zen-store HEAD
```

`origin` continues to point to `psy-zney/UniverseLiquidGlass`. The store remote is a reference to a different project; do not push this repository's `main` branch into it.

## Current blocker

GitHub reports `archived: true` for [zen-browser/theme-store](https://github.com/zen-browser/theme-store). Its page says it was archived on July 23, 2026. Archived repositories cannot accept new issues or pull requests.

The [official submission guidelines](https://docs.zen-browser.app/themes-store/themes-marketplace-submission-guidelines) still direct new themes to an issue in that repository. The current official website source (`zen-browser/www`, `src/mods.ts`) still reads its registry from `https://zen-browser.github.io/theme-store/themes.json`. No alternative submission channel was found in the checked official docs and website source.

**No submission issue, pull request or store entry has been created.** Installing from this project's Releases is currently available; that is separate from an official store listing.

## Prepared files

| File | Purpose |
| --- | --- |
| [`zen-mod/chrome.css`](../zen-mod/chrome.css) | Complete browser-chrome stylesheet |
| [`zen-mod/readme.md`](../zen-mod/readme.md) | English store-facing usage and compatibility notes |
| [`zen-mod/preview.png`](../zen-mod/preview.png) | 600×400 PNG from actual native Zen footage |
| [`zen-mod/submission.json`](../zen-mod/submission.json) | Candidate name, short description, source links and status; not a store-assigned record |

Regenerate the CSS and metadata after updating the theme:

```sh
python scripts/build.py
python scripts/prepare-store.py
```

## Requirements to resolve before submitting

- The official repository must reopen submissions, or Zen must publish another supported destination.
- The legacy form expects inline CSS. This theme exceeds the GitHub issue-body limit, so the submission path must accept a file, stylesheet URL or direct PR rather than truncating the CSS.
- The official repository requires **CC BY-NC-SA 4.0** for store themes. The main project remains MIT; this preparation does not change its license.
- The store stylesheet covers browser chrome. Optional website/content rules remain in `theme/userContent.css` for manual installation and must not be represented as a chrome-only mod feature.

The candidate name is under 25 characters, its description is under 100 characters and its PNG is exactly 600×400. The checked registry does not already contain this name. Approval and publication still belong to Zen's maintainers.
