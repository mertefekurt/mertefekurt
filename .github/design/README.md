# Profile design

The current README uses a minimal, transparent typographic masthead and native Markdown. There are four selected projects, an optional workbench list, and three small contact icons. Desktop/mobile and light/dark variants keep the masthead readable without a surrounding card or background panel.

## Rebuild current assets

With Python 3 and `fonttools` installed, run from the repository root:

```sh
python3 .github/design/build_minimal.py
```

Output: `assets/minimal/`. Type is outlined, so the README needs no remote fonts or image services. Project descriptions remain editable in `README.md`.

## Fonts

- Space Grotesk — https://github.com/google/fonts/tree/main/ofl/spacegrotesk
- Instrument Serif Italic — https://github.com/google/fonts/tree/main/ofl/instrumentserif
- IBM Plex Mono — https://github.com/google/fonts/tree/main/ofl/ibmplexmono

Source fonts and their SIL Open Font License notices are in `fonts/`.

The previous visual system is preserved in `build_identity.py` and `assets/identity/` for reference. Neither generator runs automatically. The existing metrics workflow does not overwrite the README or its current visual assets.
