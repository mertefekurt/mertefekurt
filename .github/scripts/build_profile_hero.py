from __future__ import annotations

import base64
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets"
TEXTURE = ASSETS / "profile-system-texture.jpg"

MERT_EFE = (
    "M4.13 72V10.77H12.56L23.82 43.19H23.99L35.17 10.77H43.69V72H34.92V34.76H34.74"
    "L26.06 61.08H21.67L13.07 34.76H12.9V72Z M50.44 72V10.77H76.59V19.02H59.22V37H74.35"
    "V45.25H59.22V63.23H76.59V72Z M89.54 19.02V38.12H94.52Q96.85 38.12 98.22 37.47Q99.6 36.83"
    " 100.37 35.62Q101.06 34.42 101.32 32.66Q101.58 30.89 101.58 28.57Q101.58 26.25 101.32 24.49"
    "Q101.06 22.72 100.29 21.43Q98.65 19.02 94.09 19.02ZM80.76 72V10.77H94.87Q110.35 10.77"
    " 110.35 28.74Q110.35 34.16 108.67 37.94Q106.99 41.73 102.78 44.05L112.24 72H102.95L94.78"
    " 45.86H89.54V72Z M121.66 72V19.02H111.51V10.77H140.58V19.02H130.43V72Z M157.45 72V10.77"
    "H183.59V19.02H166.22V37H181.36V45.25H166.22V63.23H183.59V72Z M187.77 72V10.77H213.91"
    "V19.02H196.54V37.6H211.68V45.86H196.54V72Z M218.09 72V10.77H244.23V19.02H226.86V37H242"
    "V45.25H226.86V63.23H244.23V72Z"
)

KURT = (
    "M4.13 154V92.77H12.9V120.72H13.07L25.89 92.77H34.66L22.7 117.28L36.89 154H27.61L17.63"
    " 126.82L12.9 135.68V154Z M67.64 92.77V140.24Q67.64 143.25 66.57 145.79Q65.49 148.32 63.52"
    " 150.3Q61.54 152.28 58.96 153.4Q56.38 154.52 53.45 154.52Q50.53 154.52 47.99 153.4Q45.46"
    " 152.28 43.48 150.3Q41.5 148.32 40.38 145.79Q39.26 143.25 39.26 140.24V92.77H48.04V139.38"
    "Q48.04 142.65 49.58 144.2Q51.13 145.74 53.45 145.74Q55.78 145.74 57.32 144.2Q58.87 142.65"
    " 58.87 139.38V92.77Z M83.17 101.02V120.12H88.16Q90.48 120.12 91.86 119.47Q93.23 118.83"
    " 94.01 117.62Q94.7 116.42 94.95 114.66Q95.21 112.89 95.21 110.57Q95.21 108.25 94.95 106.49"
    "Q94.7 104.72 93.92 103.43Q92.29 101.02 87.73 101.02ZM74.4 154V92.77H88.5Q103.98 92.77"
    " 103.98 110.74Q103.98 116.16 102.31 119.94Q100.63 123.73 96.42 126.05L105.88 154H96.59"
    "L88.42 127.86H83.17V154Z M115.3 154V101.02H105.15V92.77H134.22V101.02H124.07V154Z"
)

STYLE = """
  <style>
    .label { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
    .trace { stroke-dasharray: 1650; stroke-dashoffset: 0; }
    @media (prefers-reduced-motion: no-preference) {
      .word-a { animation: word-in .9s cubic-bezier(.16,1,.3,1) both; }
      .word-b { animation: word-in .9s .16s cubic-bezier(.16,1,.3,1) both; }
      .copy { animation: copy-in .7s .46s ease-out both; }
      .trace { animation: trace-pass 8s 1.1s ease-in-out infinite; }
    }
    @media (prefers-reduced-motion: reduce) {
      .word-a, .word-b, .copy { opacity: 1; transform: none; }
      .trace { stroke-dashoffset: 0; }
    }
    @keyframes word-in {
      from { opacity: 0; transform: translateY(26px); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes copy-in {
      from { opacity: 0; transform: translateX(-16px); }
      to { opacity: 1; transform: translateX(0); }
    }
    @keyframes trace-pass {
      0%, 12% { stroke-dashoffset: 1650; opacity: 0; }
      20% { opacity: 1; }
      62%, 78% { stroke-dashoffset: 0; opacity: 1; }
      92%, 100% { stroke-dashoffset: 0; opacity: 0; }
    }
  </style>
"""


def desktop(image_data: str) -> str:
    return f'''<svg width="1280" height="560" viewBox="0 0 1280 560" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
  <title id="title">Mert Efe Kurt, software developer</title>
  <desc id="desc">An animated editorial profile cover built from layered technical materials and a single inspection trace.</desc>
  <defs>
    <linearGradient id="scrim" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#0D1014" stop-opacity=".98"/>
      <stop offset=".43" stop-color="#0D1014" stop-opacity=".9"/>
      <stop offset=".68" stop-color="#0D1014" stop-opacity=".22"/>
      <stop offset="1" stop-color="#0D1014" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="shade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0D1014" stop-opacity=".08"/>
      <stop offset="1" stop-color="#0D1014" stop-opacity=".42"/>
    </linearGradient>
  </defs>
{STYLE}
  <image width="1280" height="560" href="data:image/jpeg;base64,{image_data}"/>
  <rect width="1280" height="560" fill="url(#scrim)"/>
  <rect width="1280" height="560" fill="url(#shade)"/>

  <g transform="translate(44 42) scale(1.82)">
    <g class="word-a"><path d="{MERT_EFE}" fill="#F3F5F7"/></g>
  </g>
  <g transform="translate(130 42) scale(1.82)">
    <g class="word-b"><path d="{KURT}" fill="#F3F5F7"/></g>
  </g>

  <g class="copy">
    <rect x="54" y="448" width="44" height="3" fill="#C8FF45"/>
    <text x="116" y="457" class="label" fill="#F3F5F7" font-size="20" font-weight="700" letter-spacing="1.1">SOFTWARE DEVELOPER + MIS STUDENT</text>
    <text x="54" y="500" fill="#C8CFD8" font-family="ui-sans-serif, system-ui, sans-serif" font-size="19">Python tools for testing, tracing, and securing AI integrations.</text>
  </g>

  <path class="trace" d="M600 257H807L838 243H1125L1171 285L1279 336" fill="none" stroke="#C8FF45" stroke-width="2.5"/>
</svg>
'''


def mobile(image_data: str) -> str:
    return f'''<svg width="760" height="720" viewBox="0 0 760 720" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
  <title id="title">Mert Efe Kurt, software developer</title>
  <desc id="desc">A mobile profile cover with large animated typography and layered technical materials.</desc>
  <defs>
    <linearGradient id="mobileScrim" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0D1014" stop-opacity=".9"/>
      <stop offset=".6" stop-color="#0D1014" stop-opacity=".72"/>
      <stop offset="1" stop-color="#0D1014" stop-opacity=".92"/>
    </linearGradient>
  </defs>
{STYLE}
  <image x="-440" width="1646" height="720" href="data:image/jpeg;base64,{image_data}" preserveAspectRatio="xMidYMid slice"/>
  <rect width="760" height="720" fill="url(#mobileScrim)"/>

  <g transform="translate(44 58) scale(1.86)">
    <g class="word-a"><path d="{MERT_EFE}" fill="#F3F5F7"/></g>
  </g>
  <g transform="translate(154 78) scale(1.86)">
    <g class="word-b"><path d="{KURT}" fill="#F3F5F7"/></g>
  </g>

  <g class="copy">
    <rect x="48" y="588" width="54" height="4" fill="#C8FF45"/>
    <text x="48" y="628" class="label" fill="#F3F5F7" font-size="23" font-weight="700">SOFTWARE DEVELOPER + MIS STUDENT</text>
    <text x="48" y="670" fill="#D5DAE0" font-family="ui-sans-serif, system-ui, sans-serif" font-size="20">Testing, tracing, and securing AI integrations.</text>
  </g>

  <path class="trace" d="M430 330H590L640 370L760 407" fill="none" stroke="#C8FF45" stroke-width="3"/>
</svg>
'''


def main() -> None:
    image_data = base64.b64encode(TEXTURE.read_bytes()).decode("ascii")
    (ASSETS / "profile-hero.svg").write_text(desktop(image_data), encoding="utf-8")
    (ASSETS / "profile-hero-mobile.svg").write_text(mobile(image_data), encoding="utf-8")


if __name__ == "__main__":
    main()
