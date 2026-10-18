"""Build self-contained profile SVGs; pip install fonttools.

Typography is outlined so GitHub needs no external font requests.
Font licenses and source fonts live alongside this file.
"""
from pathlib import Path
from html import escape
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'assets' / 'identity'
FONTS = Path(__file__).parent / 'fonts'
OUT.mkdir(exist_ok=True)
sans = instantiateVariableFont(TTFont(FONTS / 'SpaceGrotesk.ttf'), {'wght': 600})
serif = TTFont(FONTS / 'InstrumentSerif-Italic.ttf')
mono = TTFont(FONTS / 'IBMPlexMono-Regular.ttf')
INK, PAPER, LIME, MUTED = '#18382d', '#f3f1e8', '#d2ef87', '#64776c'

def text(value, x, y, size, font=sans, color=INK, tracking=0):
    glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
    scale = size / font['head'].unitsPerEm
    paths, cursor = [], 0
    for char in value:
        glyph = glyphs[cmap[ord(char)]]
        pen = SVGPathPen(glyphs)
        glyph.draw(pen)
        paths.append(f'<path transform="translate({cursor:.2f} 0)" d="{pen.getCommands()}"/>')
        cursor += glyph.width + tracking / scale
    return f'<g aria-label="{escape(value)}" fill="{color}" transform="translate({x} {y}) scale({scale} {-scale})">{"".join(paths)}</g>'

def rect(x,y,w,h,fill,rx=0,stroke='none'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'

def line(x1,y1,x2,y2,color=INK):
    return f'<path d="M{x1} {y1}H{x2}" stroke="{color}"/>' if y1==y2 else f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}"/>'

ICONS = {
 'code':'<path d="m8 6-6 6 6 6m8-12 6 6-6 6M14 3l-4 18"/>',
 'api':'<path d="M5 4h14v6H5zM5 14h14v6H5zM8 7h.01M8 17h.01M12 10v4"/>',
 'data':'<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 4 16 4 16 0V5M4 12c0 4 16 4 16 0"/>',
 'screen':'<rect x="2" y="3" width="20" height="15" rx="2"/><path d="M2 8h20M8 22h8m-4-4v4M5 5.5h.01M8 5.5h.01"/>',
 'git':'<circle cx="6" cy="5" r="3"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="20" r="3"/><path d="M6 8v9m0-4c7 0 12 0 12-4"/>',
 'check':'<path d="m5 12 4 4L20 5M4 3H2v19h19v-3"/>',
 'bolt':'<path d="m13 2-9 12h7l-1 8 10-12h-7z"/>',
 'box':'<path d="m12 2 10 5v10l-10 5-10-5V7zM2 7l10 5 10-5M12 12v10M7 4.5l10 5"/>',
 'chart':'<path d="M3 2v19h19M7 16v-4m5 4V7m5 9V4"/>',
 'terminal':'<rect x="1" y="3" width="22" height="18" rx="2"/><path d="m5 8 4 4-4 4m8 0h6"/>',
 'globe':'<circle cx="12" cy="12" r="10"/><ellipse cx="12" cy="12" rx="4" ry="10"/><path d="M2 12h20"/>',
 'mail':'<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 5 10 8L22 5"/>',
 'link':'<path d="M10 13a5 5 0 0 0 7 0l4-4a5 5 0 0 0-7-7l-3 3M14 11a5 5 0 0 0-7 0l-4 4a5 5 0 0 0 7 7l3-3"/>',
 'arrow':'<path d="M5 19 19 5H6m13 0v13"/>',
 'python':'<path d="M12 2H7a4 4 0 0 0-4 4v6h10V8h7V6a4 4 0 0 0-4-4h-4Zm0 20h5a4 4 0 0 0 4-4v-6H11v4H4v2a4 4 0 0 0 4 4h4Z"/><path d="M8 5h.01M16 19h.01"/>',
}

def icon(name,x,y,size=24,color=INK):
    return f'<g transform="translate({x} {y}) scale({size/24})" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>'

def save(name,w,h,body,title):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title>{body}</svg>'
    (OUT / f'{name}.svg').write_text(svg)

def hero(mobile=False):
    w,h=(640,700) if mobile else (1200,500)
    b=rect(0,0,w,h,PAPER,12)
    pad=36 if mobile else 48
    b+=rect(pad,32,9,9,INK)+text('MERTEFEKURT / GITHUB',pad+22,42,16 if mobile else 13,mono,tracking=.6)
    if not mobile: b+=text('ISTANBUL, TR',978,42,13,mono)
    b+=line(pad,64,w-pad,64,'#c9cfc3')
    b+=text('MERT EFE',pad,178,100 if mobile else 110,tracking=-4)
    b+=text('Kurt.',pad-3,304,151,serif)
    b+=text('Software developer',pad,365,26)
    b+=text('Management Information Systems student',pad,397,21 if mobile else 16,mono,MUTED)
    # A small architectural drawing: three layers of the same project.
    px,py,pw,ph=(36,436,568,176) if mobile else (770,94,382,318)
    b+=rect(px,py,pw,ph,INK,6)
    b+=text('WHAT I WORK ON',px+24,py+32,12,mono,LIME,tracking=1)
    labels=[('api','Backends','Python / FastAPI'),('data','Developer tools','Testing / automation'),('screen','Interfaces','Dashboards / data')]
    for i,(symbol,label,detail) in enumerate(labels):
        if mobile:
            x,y=px+22+i*184,py+60
            b+=icon(symbol,x,y,29,LIME)+text(label,x,y+53,20,sans,PAPER)
        else:
            x,y=px+24,py+65+i*78
            b+=icon(symbol,x,y+5,29,LIME)+text(label,x+51,y+19,21,sans,PAPER)+text(detail,x+51,y+43,12,mono,'#b7c9bb')
            if i<2: b+=line(x,y+61,px+pw-24,y+61,'#436052')
    fy=h-45
    b+=line(pad,fy-25,w-pad,fy-25,'#c9cfc3')
    b+=text('PYTHON  /  SYSTEMS  /  VISUAL THINKING',pad,fy+1,12,mono)
    b+=icon('arrow',w-pad-24,fy-17,24)
    save('hero-mobile' if mobile else 'hero',w,h,b,'Mert Efe Kurt. Software developer and MIS student in Istanbul. Python backends, developer tools and interfaces.')

hero();hero(True)

for slug,label,symbol,width in [('portfolio','Portfolio','globe',154),('linkedin','LinkedIn','link',148),('email','Email','mail',122),('repositories','Repositories','code',184)]:
    b=rect(1,1,width-2,42,INK,6)+icon(symbol,15,12,20,LIME)+text(label,45,28,15,sans,PAPER)
    save(slug,width,44,b,label)

for num,slug,title,caption in [('01','team','Built together.','TEAM PROJECTS'),('02','tools','Small tools, specific jobs.','SELECTED REPOSITORIES'),('03','stack','The working set.','LANGUAGES & TOOLS')]:
    for theme in ('light','dark'):
        fg=INK if theme=='light' else PAPER
        subtle='#bdc7bd' if theme=='light' else '#3c4a43'
        b=line(0,1,1200,1,subtle)+rect(0,22,44,33,LIME,3)+text(num,10,45,18,mono,INK)
        b+=text(title,62,57,42,serif,fg)+text(caption,62,84,13,mono,fg,tracking=1.5)
        save(f'{slug}-{theme}',1200,110,b,title+' '+caption)
        save(f'{slug}-mobile-{theme}',600,110,b.replace('H1200','H600'),title+' '+caption)

tools=[('Python','python'),('FastAPI','bolt'),('Pydantic','check'),('JavaScript','code'),('SQLite','data'),('Git','git'),('pytest','check'),('Ruff','bolt'),('GitHub Actions','git'),('MCP','box'),('R / Plotly','chart'),('Swift','code')]
for mobile in (False,True):
    cols=3 if mobile else 6
    cw,ch=200,104
    w,h=cols*cw,(len(tools)//cols)*ch
    b=''
    for i,(label,symbol) in enumerate(tools):
        x,y=(i%cols)*cw,(i//cols)*ch
        b+=rect(x+3,y+3,cw-6,ch-6,PAPER,5)
        b+=icon(symbol,x+18,y+19,28)+text(label,x+18,y+78,20 if mobile else 17)
        b+=rect(x+cw-23,y+16,5,5,'#6f9252')
    save('stack-mobile' if mobile else 'stack',w,h,b,'Python, FastAPI, Pydantic, JavaScript, SQLite, Git, pytest, Ruff, GitHub Actions, MCP, R and Plotly, Swift.')

b=rect(0,0,1200,148,INK,8)+text('Have a project in mind?',32,64,42,serif,PAPER)
b+=text('mertk.mek@gmail.com',34,112,18,mono,LIME)+icon('arrow',1120,52,40,LIME)
save('contact',1200,148,b,'Have a project in mind? Email Mert at mertk.mek@gmail.com.')
b=rect(0,0,600,160,INK,8)+text('Have a project in mind?',24,62,40,serif,PAPER)
b+=text('mertk.mek@gmail.com',26,118,23,mono,LIME)+icon('arrow',530,62,35,LIME)
save('contact-mobile',600,160,b,'Have a project in mind? Email Mert at mertk.mek@gmail.com.')
