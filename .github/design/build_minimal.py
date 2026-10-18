"""Build the minimal profile masthead. Requires fonttools; fonts are bundled."""
from pathlib import Path
from html import escape
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[2]
FONTS = Path(__file__).parent / 'fonts'
OUT = ROOT / 'assets' / 'minimal'
OUT.mkdir(exist_ok=True)
SANS = instantiateVariableFont(TTFont(FONTS / 'SpaceGrotesk.ttf'), {'wght': 500})
SERIF = TTFont(FONTS / 'InstrumentSerif-Italic.ttf')
MONO = TTFont(FONTS / 'IBMPlexMono-Regular.ttf')


def lettering(value, x, y, size, font, fill, tracking=0):
    glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
    scale = size / font['head'].unitsPerEm
    paths, cursor = [], 0
    for char in value:
        glyph = glyphs[cmap[ord(char)]]
        pen = SVGPathPen(glyphs)
        glyph.draw(pen)
        paths.append(f'<path transform="translate({cursor:.2f} 0)" d="{pen.getCommands()}"/>')
        cursor += glyph.width + tracking / scale
    return f'<g aria-label="{escape(value)}" fill="{fill}" transform="translate({x} {y}) scale({scale} {-scale})">{"".join(paths)}</g>'


for theme in ('light', 'dark'):
    ink = '#222620' if theme == 'light' else '#e8e9e1'
    muted = '#697067' if theme == 'light' else '#a0a79b'
    accent = '#a45c3b' if theme == 'light' else '#d99874'
    rule = '#dedfd7' if theme == 'light' else '#353c34'
    for mobile in (False, True):
        width, height = (600, 242) if mobile else (1000, 254)
        body = f'<rect x="2" y="18" width="7" height="7" fill="{accent}"/>'
        body += lettering('ISTANBUL, TR', 22, 27, 16 if mobile else 13, MONO, muted, .7)
        if not mobile:
            body += lettering('@mertefekurt', 876, 27, 13, MONO, muted)
        body += lettering('Mert Efe Kurt', 2, 138 if mobile else 151, 82 if mobile else 104, SANS, ink, -3)
        body += lettering('Software developer.', 6, 199 if mobile else 215, 47, SERIF, muted)
        body += f'<path d="M0 {height-1}H{width}" stroke="{rule}"/>'
        title = 'Mert Efe Kurt — software developer. Istanbul, Türkiye.'
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title>{body}</svg>'
        suffix = '-mobile' if mobile else ''
        (OUT / f'header{suffix}-{theme}.svg').write_text(svg)

    icons = {
        'website': '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>',
        'linkedin': '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M7 10v7m0-10v.01M11 17v-7m0 3a3 3 0 0 1 6 0v4"/>',
        'mail': '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 5 10 8L22 5"/>',
    }
    for name, shape in icons.items():
        (OUT / f'{name}-{theme}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><g fill="none" stroke="{muted}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{shape}</g></svg>')
