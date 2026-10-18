# Profile design

The current README pairs a typographic masthead with an original engraved K. Its displaced-to-ordered line field takes its subject from PixelMorph rather than generic decorative artwork. Large sans type, an italic surname, and one warm registration line create an asymmetric composition; ordinary Markdown keeps the project list useful.

There are separate desktop/mobile compositions and light/dark variants, without background panels or remote rendering services. Four projects are visible; the workbench is expandable. Contact icons come from the earlier minimal system.

## Rebuild current assets

With Python 3 and `fonttools` installed, run from the repository root:

```sh
python3 .github/design/build_editorial.py
```

Output: `assets/editorial/`. Type is outlined. The engraved K uses vector clipping and explicit polylines; it has no embedded raster textures, scripts, or animation. Project descriptions remain editable in `README.md`.

## Fonts

- Space Grotesk — https://github.com/google/fonts/tree/main/ofl/spacegrotesk
- Instrument Serif Italic — https://github.com/google/fonts/tree/main/ofl/instrumentserif
- IBM Plex Mono — https://github.com/google/fonts/tree/main/ofl/ibmplexmono

Source fonts and their SIL Open Font License notices are in `fonts/`.

Previous systems are preserved in `build_identity.py`, `build_minimal.py`, `assets/identity/`, and `assets/minimal/`. Generators run manually. The existing metrics workflow does not overwrite the README or current artwork.
