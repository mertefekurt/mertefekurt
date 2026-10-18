"""Refresh short, template-heavy public READMEs without touching rich ones.

Run from the profile repository with an authenticated ``gh`` session. The
script only rewrites README files that are short or contain the old filler
copy, and uses the repository's own description, command examples, and file
map as source material.
"""
from __future__ import annotations

import base64
import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPOS_FILE = Path("/tmp/mertefekurt-public.json")
SKIP = {"mertefekurt"}


def gh(*args: str, input_data: str | None = None) -> dict | str:
    result = subprocess.run(
        ["gh", *args], input=input_data, text=True, capture_output=True, check=True
    )
    return result.stdout


def get_repo(name: str) -> dict:
    return json.loads(gh("api", f"repos/mertefekurt/{name}"))


def get_readme(name: str) -> tuple[str, str, str]:
    data = json.loads(gh("api", f"repos/mertefekurt/{name}/readme"))
    content = base64.b64decode(data["content"]).decode("utf-8")
    return content, data["sha"], data.get("path", "README.md")


def get_project_description(name: str, fallback: str) -> str:
    """Use the package's own description when GitHub metadata is empty."""
    try:
        raw = gh(
            "api",
            f"repos/mertefekurt/{name}/contents/pyproject.toml",
            "-H",
            "Accept: application/vnd.github.raw+json",
        )
    except subprocess.CalledProcessError:
        return fallback
    match = re.search(r"^description\s*=\s*[\"'](.+?)[\"']\s*$", raw, re.MULTILINE)
    return match.group(1).strip() if match else fallback


def clean_title(name: str) -> str:
    return re.sub(r"[-_]", " ", name).title().replace("Api", "API").replace("Ai", "AI")


def first_shell_block(readme: str) -> str | None:
    match = re.search(r"```(?:bash|sh|shell)\n(.*?)```", readme, re.DOTALL | re.IGNORECASE)
    if not match:
        return None
    lines = [line.rstrip() for line in match.group(1).strip().splitlines()]
    lines = [line for line in lines if line and not line.startswith("#")]
    return "\n".join(lines[:8]) if lines else None


def text_file_map(readme: str) -> str | None:
    match = re.search(r"```text\n(.*?)```", readme, re.DOTALL | re.IGNORECASE)
    if not match:
        return None
    return match.group(1).strip()


def render(repo: dict, readme: str) -> str:
    name = repo["name"]
    title = clean_title(name)
    language = (repo.get("language") or (repo.get("primaryLanguage") or {}).get("name") or "")
    description = get_project_description(name, repo.get("description") or "")
    if not description:
        description = f"A focused {language or 'software'} project from Mert Efe Kurt."
    command = first_shell_block(readme)
    if not command:
        command = f"git clone https://github.com/mertefekurt/{name}.git\ncd {name}"
        if language == "Python":
            command += '\npython -m pip install -e ".[dev]"'
    file_map = text_file_map(readme)
    lines = [
        f"# {title}",
        "",
        f"![{title} cover](assets/readme-cover.svg)",
        "",
        description,
        "",
    ]
    if language:
        lines += [f"`{language}`", ""]
    lines += ["## Start here", "", "```bash", command, "```", ""]
    if file_map:
        lines += ["## Project map", "", "```text", file_map, "```", ""]
    lines += [
        "## Repository",
        "",
        f"[Open the source on GitHub →](https://github.com/mertefekurt/{name})",
        "",
        "[MIT License](LICENSE)" if repo.get("license") else "",
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def should_refresh(readme: str) -> bool:
    filler = (
        "small, inspectable",
        "shortest path from clone to result",
        "developer tool tool",
    )
    return len(readme) < 900 or any(phrase in readme.lower() for phrase in filler)


def refresh(name: str) -> tuple[str, bool, str]:
    repo = get_repo(name)
    try:
        readme, sha, path = get_readme(name)
    except subprocess.CalledProcessError:
        return name, False, "no README"
    if not should_refresh(readme):
        return name, False, "kept rich README"
    new_readme = render(repo, readme)
    payload = json.dumps(
        {
            "message": "docs: refine project README",
            "content": base64.b64encode(new_readme.encode()).decode(),
            "sha": sha,
            "branch": repo["default_branch"],
        }
    )
    gh("api", f"repos/mertefekurt/{name}/contents/{path}", "--method", "PUT", "--input", "-", input_data=payload)
    return name, True, "refreshed"


def main() -> None:
    repos = json.loads(REPOS_FILE.read_text())
    names = [repo["name"] for repo in repos if repo["name"] not in SKIP]
    with ThreadPoolExecutor(max_workers=8) as pool:
        for name, changed, status in pool.map(refresh, names):
            print(f"{'UPDATED' if changed else 'KEPT':7} {name}: {status}")


if __name__ == "__main__":
    main()
