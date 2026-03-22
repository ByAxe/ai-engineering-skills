#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import subprocess
import tempfile
from pathlib import Path


def run(*args: str, capture_output: bool = True) -> str:
    completed = subprocess.run(
        args,
        check=True,
        text=True,
        capture_output=capture_output,
    )
    return completed.stdout.strip() if capture_output else ""


def release_exists(repo: str, tag: str) -> bool:
    completed = subprocess.run(
        ["gh", "release", "view", tag, "--repo", repo, "--json", "tagName"],
        text=True,
        capture_output=True,
    )
    return completed.returncode == 0


def ensure_release(repo: str, pr_number: int, tag: str, assets: list[Path]) -> None:
    title = f"PR {pr_number} demo assets"
    notes = f"Temporary demo assets for PR #{pr_number}."
    asset_args = [str(asset) for asset in assets]

    if release_exists(repo, tag):
        run(
            "gh",
            "release",
            "upload",
            tag,
            *asset_args,
            "--clobber",
            "--repo",
            repo,
            capture_output=False,
        )
        return

    run(
        "gh",
        "release",
        "create",
        tag,
        *asset_args,
        "--repo",
        repo,
        "--title",
        title,
        "--notes",
        notes,
        "--prerelease",
        "--latest=false",
        capture_output=False,
    )


def build_demo_section(repo: str, tag: str, gif_name: str, mp4_name: str, title: str) -> str:
    base = f"https://github.com/{repo}/releases/download/{tag}"
    gif_url = f"{base}/{gif_name}"
    mp4_url = f"{base}/{mp4_name}"
    return (
        "## Demo\n"
        f"![{title}]({gif_url})\n\n"
        f"[MP4 download]({mp4_url})\n"
    )


def update_pr_body(repo: str, pr_number: int, demo_section: str) -> None:
    body = run("gh", "pr", "view", str(pr_number), "--repo", repo, "--json", "body", "--jq", ".body")
    pattern = re.compile(r"^## Demo\n.*?(?=^## |\Z)", re.DOTALL | re.MULTILINE)
    if pattern.search(body):
        updated_body = pattern.sub(demo_section + "\n", body, count=1)
    else:
        updated_body = demo_section + "\n\n" + body if body else demo_section

    with tempfile.NamedTemporaryFile("w", delete=False) as handle:
        handle.write(updated_body)
        body_path = Path(handle.name)

    try:
        run(
            "gh",
            "pr",
            "edit",
            str(pr_number),
            "--repo",
            repo,
            "--body-file",
            str(body_path),
            capture_output=False,
        )
    finally:
        body_path.unlink(missing_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload PR demo assets to a GitHub prerelease and patch the PR body Demo section.",
    )
    parser.add_argument("--repo", required=True, help="owner/repo")
    parser.add_argument("--pr", required=True, type=int, help="Pull request number")
    parser.add_argument("--gif", required=True, type=Path, help="Path to the GIF preview")
    parser.add_argument("--mp4", required=True, type=Path, help="Path to the MP4 download")
    parser.add_argument("--title", default="Feature demo", help="Alt text/title for the demo section")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for asset in (args.gif, args.mp4):
        if not asset.is_file():
            raise SystemExit(f"Asset not found: {asset}")

    tag = f"pr-{args.pr}-demo-assets"
    ensure_release(args.repo, args.pr, tag, [args.gif, args.mp4])
    demo_section = build_demo_section(
        repo=args.repo,
        tag=tag,
        gif_name=args.gif.name,
        mp4_name=args.mp4.name,
        title=args.title,
    )
    update_pr_body(args.repo, args.pr, demo_section)
    print(f"Updated PR #{args.pr} demo section using release tag {tag}.")


if __name__ == "__main__":
    main()
