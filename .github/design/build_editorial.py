"""Profile artwork: an original line-engraved K, informed by PixelMorph.

Rebuild with Python 3 and fonttools. No raster textures, remote fonts or scripts.
"""
from pathlib import Path
from html import escape
from math import sin, pi
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'assets' / 'editorial'
FONTS = Path(__file__).parent / 'fonts'
OUT.mkdir(exist_ok=True)
SANS = instantiateVariableFont(TTFont(FONTS / 'SpaceGrotesk.ttf'), {'wght': 500})
HEAVY = instantiateVariableFont(TTFont(FONTS / 'SpaceGrotesk.ttf'), {'wght': 700})
SERIF = TTFont(FONTS / 'InstrumentSerif-Italic.ttf')
MONO = TTFont(FONTS / 'IBMPlexMono-Regular.ttf')


def text(value, x, y, size, font, color, tracking=0):
    glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
    scale = size / font['head'].unitsPerEm
    paths, cursor = [], 0
    for char in value:
        glyph = glyphs[cmap[ord(char)]]
        pen = SVGPathPen(glyphs)
        glyph.draw(pen)
        paths.append(f'<path transform="translate({cursor:.3f} 0)" d="{pen.getCommands()}"/>')
        cursor += glyph.width + tracking / scale
    return f'<g aria-label="{escape(value)}" fill="{color}" transform="translate({x} {y}) scale({scale} {-scale})">{"".join(paths)}</g>'


def save(name,w,h,body,title):
    (OUT/f'{name}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">Original vector composition. An engraved K moves from displaced lines to ordered strokes, inspired by pixel sorting in PixelMorph.</desc>{body}</svg>')


def engraving(x, y, scale, ink, accent, quiet):
    # Letter geometry is outlined; each stroke is explicitly drawn.
    # Left: displaced pixels. Right: parallel strokes constrained to a K.
    b=f'<g transform="translate({x} {y}) scale({scale})">'
    mask=text('K',30,360,450,HEAVY,'#000')
    b+=f'<defs><clipPath id="letter">{mask}</clipPath></defs>'
    b+='<g clip-path="url(#letter)">'
    for i in range(76):
        yy=25+i*4.6
        phase=(yy-25)/350
        # The field becomes progressively regular across the horizontal axis.
        pts=[]
        for j in range(65):
            xx=j*6
            disp=sin(phase*pi*6+j*.12)*17*(1-j/64)**2
            pts.append(f'{xx:.2f},{yy+disp:.2f}')
        b+=f'<polyline points="{" ".join(pts)}" fill="none" stroke="{ink}" stroke-width="2.25"/>'
    b+='</g>'
    # One offset registration stroke makes the source process visible.
    b+=f'<path d="M-12 199H361" stroke="{accent}" stroke-width="1.6"/>'
    b+=f'<rect x="-17" y="195" width="8" height="8" fill="{accent}"/>'
    for i in range(13):
        xx=-12+i*4.6
        yy=113+sin(i*.7)*5
        b+=f'<path d="M{xx:.2f} {yy:.2f}v{14+i%4*3}" stroke="{quiet}" stroke-width="1.1"/>'
    b+='</g>'
    return b


for theme in ('light','dark'):
    ink='#272b30' if theme=='light' else '#eeeae3'
    muted='#727570' if theme=='light' else '#a8aaa3'
    quiet='#d4d5ce' if theme=='light' else '#404641'
    accent='#b44d32' if theme=='light' else '#df896b'
    for mobile in (False,True):
        w,h=(640,520) if mobile else (1120,440)
        b=text('SOFTWARE DEVELOPER',2,25,17 if mobile else 13,MONO,muted,1.2)
        if not mobile:
            b+=text('ISTANBUL, TR',978,25,13,MONO,muted,.5)
        b+=f'<path d="M0 46H{w}" stroke="{quiet}"/>'
        b+=text('Mert Efe',-1,170,101 if mobile else 115,SANS,ink,-4)
        b+=text('Kurt.',10,344,205,SERIF,ink,-4)
        if mobile:
            b+=engraving(355,158,.71,ink,accent,quiet)
            b+=text('PYTHON / APIS / DEVELOPER TOOLS',2,475,16,MONO,muted,.3)
            b+=text('ISTANBUL, TR',2,507,14,MONO,muted,.5)
        else:
            b+=engraving(731,45,.94,ink,accent,quiet)
            b+=text('PYTHON / APIS / DEVELOPER TOOLS',2,414,13,MONO,muted,.5)
            b+=text('PIXEL STUDY / K',842,414,12,MONO,muted,.5)
        b+=f'<path d="M0 {h-1}H{w}" stroke="{quiet}"/>'
        suffix='-mobile' if mobile else ''
        save(f'cover{suffix}-{theme}',w,h,b,'Mert Efe Kurt — software developer in Istanbul. Python, APIs and developer tools. A line-engraved K inspired by PixelMorph.')
