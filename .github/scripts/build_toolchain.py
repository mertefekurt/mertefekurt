from __future__ import annotations

import html
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets"
SIMPLE_ICONS_REVISION = "34c22501f9ac9f22b12f825677ccbab1fb22e14b"
SOURCE = f"https://raw.githubusercontent.com/simple-icons/simple-icons/{SIMPLE_ICONS_REVISION}/icons"
ACCENT = "#C8FF45"


@dataclass(frozen=True)
class Tool:
    slug: str
    label: str


GROUPS = (
    ("BUILD", (Tool("python", "Python"), Tool("fastapi", "FastAPI"), Tool("pydantic", "Pydantic"), Tool("javascript", "JavaScript"))),
    ("VERIFY", (Tool("pytest", "pytest"), Tool("ruff", "Ruff"), Tool("githubactions", "GitHub Actions"), Tool("sqlite", "SQLite"))),
    ("AI + DATA", (Tool("googlegemini", "Gemini"), Tool("modelcontextprotocol", "MCP"), Tool("r", "R"), Tool("swift", "Swift"))),
)


def icon_path(slug: str) -> str:
    request = urllib.request.Request(
        f"{SOURCE}/{slug}.svg",
        headers={"User-Agent": "mertefekurt-profile-readme"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        root = ET.fromstring(response.read())
    path = root.find("{http://www.w3.org/2000/svg}path")
    if path is None or not path.get("d"):
        raise RuntimeError(f"No path found for Simple Icon: {slug}")
    return path.attrib["d"]


def shared_style() -> str:
    return """
  <style>
    .sans { font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif; }
    .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
    @media (prefers-reduced-motion: no-preference) {
      .row-a { animation: row-in .65s .08s cubic-bezier(.16,1,.3,1) both; }
      .row-b { animation: row-in .65s .20s cubic-bezier(.16,1,.3,1) both; }
      .row-c { animation: row-in .65s .32s cubic-bezier(.16,1,.3,1) both; }
      .icon { animation: icon-in .55s var(--delay) cubic-bezier(.16,1,.3,1) both; transform-box: fill-box; transform-origin: center; }
    }
    @media (prefers-reduced-motion: reduce) {
      .row-a, .row-b, .row-c, .icon { opacity: 1; transform: none; }
    }
    @keyframes row-in {
      from { opacity: 0; transform: translateY(9px); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes icon-in {
      from { opacity: 0; transform: scale(.72); }
      to { opacity: 1; transform: scale(1); }
    }
  </style>
"""


def icon(tool: Tool, paths: dict[str, str], *, x: int, y: int, scale: float, delay: float, label_size: int) -> str:
    label_x = x + round(24 * scale) + 16
    label_y = y + round(16 * scale)
    return (
        f'<g class="icon" style="--delay:{delay:.2f}s">'
        f'<path d="{paths[tool.slug]}" transform="translate({x} {y}) scale({scale})" fill="{ACCENT}"/>'
        f'<text x="{label_x}" y="{label_y}" class="sans" fill="#F3F5F7" font-size="{label_size}" font-weight="650">'
        f'{html.escape(tool.label)}</text></g>'
    )


def desktop(paths: dict[str, str]) -> str:
    classes = ("row-a", "row-b", "row-c")
    rows: list[str] = []
    for row_index, (group, tools) in enumerate(GROUPS):
        y = 39 + row_index * 94
        items = [
            icon(
                tool,
                paths,
                x=248 + item_index * 250,
                y=y,
                scale=1.5,
                delay=0.16 + row_index * 0.12 + item_index * 0.04,
                label_size=17,
            )
            for item_index, tool in enumerate(tools)
        ]
        rows.append(
            f'<g class="{classes[row_index]}">'
            f'<text x="48" y="{y + 27}" class="mono" fill="#808995" font-size="14" font-weight="750" letter-spacing="1.4">{group}</text>'
            + "".join(items)
            + "</g>"
        )

    return f'''<svg width="1280" height="310" viewBox="0 0 1280 310" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
  <title id="title">Mert Efe Kurt's toolchain</title>
  <desc id="desc">Python, FastAPI, Pydantic, JavaScript, pytest, Ruff, GitHub Actions, SQLite, Gemini, Model Context Protocol, R, and Swift.</desc>
{shared_style()}
  <rect width="1280" height="310" fill="#0D1014"/>
  <path d="M48 113H1232M48 207H1232" stroke="#2A3038"/>
  {''.join(rows)}
</svg>
'''


def mobile(paths: dict[str, str]) -> str:
    classes = ("row-a", "row-b", "row-c")
    rows: list[str] = []
    for row_index, (group, tools) in enumerate(GROUPS):
        top = 42 + row_index * 220
        items: list[str] = []
        for item_index, tool in enumerate(tools):
            column = item_index % 2
            row = item_index // 2
            items.append(
                icon(
                    tool,
                    paths,
                    x=44 + column * 356,
                    y=top + 50 + row * 76,
                    scale=1.75,
                    delay=0.16 + row_index * 0.12 + item_index * 0.04,
                    label_size=24,
                )
            )
        rows.append(
            f'<g class="{classes[row_index]}">'
            f'<text x="44" y="{top + 18}" class="mono" fill="#808995" font-size="20" font-weight="750" letter-spacing="1.5">{group}</text>'
            + "".join(items)
            + "</g>"
        )

    return f'''<svg width="760" height="680" viewBox="0 0 760 680" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
  <title id="title">Mert Efe Kurt's toolchain</title>
  <desc id="desc">Python, FastAPI, Pydantic, JavaScript, pytest, Ruff, GitHub Actions, SQLite, Gemini, Model Context Protocol, R, and Swift.</desc>
{shared_style()}
  <rect width="760" height="680" fill="#0D1014"/>
  <path d="M44 221H716M44 441H716" stroke="#2A3038"/>
  {''.join(rows)}
</svg>
'''


def main() -> None:
    paths = {
        tool.slug: icon_path(tool.slug)
        for _, tools in GROUPS
        for tool in tools
    }
    (ASSETS / "toolchain.svg").write_text(desktop(paths), encoding="utf-8")
    (ASSETS / "toolchain-mobile.svg").write_text(mobile(paths), encoding="utf-8")


if __name__ == "__main__":
    main()
