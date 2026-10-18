# Profile identity assets

The profile uses a self-contained SVG identity: warm paper, forest green, lime accents, outlined type, and original line icons. The CloudSentinel image is the existing project screenshot, linked to the merged contribution that introduced the dashboard work.

## Rebuild

From the repository root, with Python 3 and `fonttools` installed:

```sh
python3 .github/design/build_identity.py
```

All generated files are in `assets/identity/`. Font outlines keep the typography consistent without web fonts, scripts, or external image services. The README selects separate mobile artwork and light/dark section headings through `<picture>`. Text descriptions and project links remain ordinary Markdown.

## Fonts

- Space Grotesk — https://github.com/google/fonts/tree/main/ofl/spacegrotesk
- Instrument Serif Italic — https://github.com/google/fonts/tree/main/ofl/instrumentserif
- IBM Plex Mono — https://github.com/google/fonts/tree/main/ofl/ibmplexmono

The source fonts and their SIL Open Font License notices are included in `fonts/`.

## Maintenance

Edit project descriptions in `README.md`; edit the visual system in `build_identity.py` and rebuild. The existing metrics workflow updates only the legacy metrics assets and does not overwrite this identity or README.
