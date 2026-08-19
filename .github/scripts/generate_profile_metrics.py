from __future__ import annotations

import html
import json
import os
import urllib.request
from collections import Counter
from pathlib import Path


USERNAME = "mertefekurt"
API_ROOT = "https://api.github.com"
ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets"
ACCENT = "#C8FF45"


def get_json(path: str):
    request = urllib.request.Request(f"{API_ROOT}{path}")
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    request.add_header("User-Agent", "mertefekurt-profile-readme")
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def get_repositories() -> list[dict]:
    repositories: list[dict] = []
    page = 1
    while True:
        batch = get_json(
            f"/users/{USERNAME}/repos?type=owner&sort=full_name&per_page=100&page={page}"
        )
        repositories.extend(batch)
        if len(batch) < 100:
            return repositories
        page += 1


def language_breakdown(repositories: list[dict]) -> list[tuple[str, int]]:
    totals: Counter[str] = Counter()
    for repository in repositories:
        if repository.get("fork") or repository.get("archived"):
            continue
        if repository.get("language"):
            totals[repository["language"]] += 1

    total_repositories = sum(totals.values())
    if not total_repositories:
        return [("No data", 100)]

    top = totals.most_common(4)
    percentages = [(name, round(value * 100 / total_repositories)) for name, value in top]
    used = sum(percent for _, percent in percentages)
    if len(totals) > 4:
        percentages.append(("Other", max(0, 100 - used)))
    elif percentages:
        name, value = percentages[-1]
        percentages[-1] = (name, value + (100 - used))
    return [(name, percent) for name, percent in percentages if percent > 0]


def proof_data(profile: dict) -> tuple[int, int, int]:
    cloud_prs = get_json(
        "/search/issues?q=repo:muratcan-ates/cloudsentinel+is:pr+is:merged+author:mertefekurt"
    )["total_count"]
    contributors = get_json("/repos/emirselengil/YZTA-AI-Hackathon-Team215/contributors")
    kobi_commits = next(
        (item["contributions"] for item in contributors if item["login"] == USERNAME),
        0,
    )
    return int(cloud_prs), int(kobi_commits), int(profile["public_repos"])


def style() -> str:
    return """
  <style>
    .sans { font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif; }
    .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
    @media (prefers-reduced-motion: no-preference) {
      .metric-a { animation: metric-in .7s .1s cubic-bezier(.16,1,.3,1) both; }
      .metric-b { animation: metric-in .7s .22s cubic-bezier(.16,1,.3,1) both; }
      .metric-c { animation: metric-in .7s .34s cubic-bezier(.16,1,.3,1) both; }
      .segment { animation: segment-in .9s var(--delay) cubic-bezier(.16,1,.3,1) both; transform-origin: left; }
    }
    @media (prefers-reduced-motion: reduce) {
      .metric-a, .metric-b, .metric-c, .segment { opacity: 1; transform: none; }
    }
    @keyframes metric-in {
      from { opacity: 0; transform: translateY(14px); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes segment-in {
      from { opacity: 0; transform: scaleX(0); }
      to { opacity: 1; transform: scaleX(1); }
    }
  </style>
"""


def language_segments(languages: list[tuple[str, int]], *, x: int, y: int, width: int) -> str:
    opacity = [1, 0.72, 0.5, 0.34, 0.2]
    cursor = x
    used_width = 0
    parts: list[str] = []
    for index, (name, percent) in enumerate(languages):
        segment_width = (
            width - used_width
            if index == len(languages) - 1
            else round(width * percent / 100)
        )
        segment_width = max(2, segment_width)
        parts.append(
            f'<g transform="translate({cursor} {y})"><line class="segment" '
            f'style="--delay:{0.54 + index * 0.1:.2f}s" x1="0" y1="0" '
            f'x2="{segment_width}" y2="0" stroke="{ACCENT}" stroke-opacity="{opacity[min(index, 4)]}" '
            'stroke-width="9"/></g>'
        )
        cursor += segment_width
        used_width += segment_width
    return "\n    ".join(parts)


def language_labels(languages: list[tuple[str, int]], *, x: int, y: int, gap: int, font_size: int) -> str:
    parts: list[str] = []
    for index, (name, percent) in enumerate(languages):
        safe_name = html.escape(name.upper())
        parts.append(
            f'<text x="{x + index * gap}" y="{y}" class="mono" fill="#A8B0BA" '
            f'font-size="{font_size}" font-weight="700">{safe_name} <tspan fill="#F3F5F7">{percent}%</tspan></text>'
        )
    return "\n  ".join(parts)


def desktop(proof: tuple[int, int, int], languages: list[tuple[str, int]]) -> str:
    cloud_prs, kobi_commits, repo_count = proof
    segments = language_segments(languages, x=48, y=224, width=1184)
    labels = language_labels(languages, x=48, y=266, gap=215, font_size=14)
    return f'''<svg width="1280" height="292" viewBox="0 0 1280 292" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
  <title id="title">Verified GitHub work by Mert Efe Kurt</title>
  <desc id="desc">Merged team pull requests, team-project commits, public repository count, and primary repository languages generated from the GitHub API.</desc>
{style()}
  <rect width="1280" height="292" fill="#0D1014"/>
  <path d="M426 48V177M846 48V177" stroke="#2A3038"/>

  <g class="metric-a">
    <text x="48" y="118" class="mono" fill="#F3F5F7" font-size="68" font-weight="800">{cloud_prs}</text>
    <text x="48" y="157" class="sans" fill="#A8B0BA" font-size="16">merged CloudSentinel PRs</text>
  </g>
  <g class="metric-b">
    <text x="468" y="118" class="mono" fill="#F3F5F7" font-size="68" font-weight="800">{kobi_commits}</text>
    <text x="468" y="157" class="sans" fill="#A8B0BA" font-size="16">KOBİ Ops AI commits</text>
  </g>
  <g class="metric-c">
    <text x="888" y="118" class="mono" fill="#F3F5F7" font-size="68" font-weight="800">{repo_count}</text>
    <text x="888" y="157" class="sans" fill="#A8B0BA" font-size="16">public repositories</text>
  </g>

  <text x="48" y="202" class="mono" fill="#737D88" font-size="12" font-weight="700" letter-spacing="1.2">PRIMARY LANGUAGE BY REPOSITORY</text>
  {segments}
  {labels}
</svg>
'''


def mobile(proof: tuple[int, int, int], languages: list[tuple[str, int]]) -> str:
    cloud_prs, kobi_commits, repo_count = proof
    segments = language_segments(languages, x=44, y=484, width=672)
    label_rows = []
    for index, (name, percent) in enumerate(languages):
        x = 44 + (index % 2) * 342
        y = 536 + (index // 2) * 38
        label_rows.append(
            f'<text x="{x}" y="{y}" class="mono" fill="#A8B0BA" font-size="18" font-weight="700">'
            f'{html.escape(name.upper())} <tspan fill="#F3F5F7">{percent}%</tspan></text>'
        )
    labels = "\n  ".join(label_rows)
    return f'''<svg width="760" height="620" viewBox="0 0 760 620" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
  <title id="title">Verified GitHub work by Mert Efe Kurt</title>
  <desc id="desc">Merged team pull requests, team-project commits, public repository count, and primary repository languages generated from the GitHub API.</desc>
{style()}
  <rect width="760" height="620" fill="#0D1014"/>
  <path d="M44 184H716M44 398H716" stroke="#2A3038"/>

  <g class="metric-a">
    <text x="44" y="126" class="mono" fill="#F3F5F7" font-size="78" font-weight="800">{cloud_prs}</text>
    <text x="230" y="101" class="sans" fill="#A8B0BA" font-size="24">merged CloudSentinel</text>
    <text x="230" y="132" class="sans" fill="#A8B0BA" font-size="24">pull requests</text>
  </g>
  <g class="metric-b">
    <text x="44" y="330" class="mono" fill="#F3F5F7" font-size="78" font-weight="800">{kobi_commits}</text>
    <text x="230" y="305" class="sans" fill="#A8B0BA" font-size="24">KOBİ Ops AI</text>
    <text x="230" y="336" class="sans" fill="#A8B0BA" font-size="24">commits</text>
  </g>
  <g class="metric-c">
    <text x="44" y="442" class="mono" fill="#F3F5F7" font-size="24" font-weight="800">{repo_count} PUBLIC REPOSITORIES</text>
  </g>

  <text x="44" y="468" class="mono" fill="#737D88" font-size="16" font-weight="700">PRIMARY LANGUAGE BY REPOSITORY</text>
  {segments}
  {labels}
</svg>
'''


def main() -> None:
    profile = get_json(f"/users/{USERNAME}")
    repositories = get_repositories()
    languages = language_breakdown(repositories)
    proof = proof_data(profile)
    (ASSETS / "profile-metrics.svg").write_text(desktop(proof, languages), encoding="utf-8")
    (ASSETS / "profile-metrics-mobile.svg").write_text(mobile(proof, languages), encoding="utf-8")


if __name__ == "__main__":
    main()
