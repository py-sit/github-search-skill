#!/usr/bin/env python3
"""Collect standardized metadata for shortlisted GitHub repositories."""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


REPO_PATTERNS = (
    re.compile(r"^https://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$"),
    re.compile(r"^git@github\.com:([^/]+)/([^/]+?)(?:\.git)?$"),
    re.compile(r"^([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)$"),
)


@dataclass(frozen=True)
class RepoRef:
    owner: str
    repo: str
    raw: str

    @property
    def full_name(self) -> str:
        return f"{self.owner}/{self.repo}"


def parse_repo_ref(value: str) -> RepoRef:
    for pattern in REPO_PATTERNS:
        match = pattern.match(value)
        if match:
            return RepoRef(owner=match.group(1), repo=match.group(2), raw=value)
    raise ValueError(f"unsupported repo reference: {value}")


def gh_ready() -> bool:
    if shutil.which("gh") is None:
        return False
    result = subprocess.run(
        ["gh", "auth", "status"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def run_gh_api(path: str) -> Any:
    result = subprocess.run(
        ["gh", "api", "-H", "Accept: application/vnd.github+json", path],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or "unknown gh api error"
        raise RuntimeError(stderr)
    return json.loads(result.stdout)


def rest_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-search-skill/1.0",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def run_rest_api(path: str) -> Any:
    if shutil.which("curl") is not None:
        command = [
            "curl",
            "-fsSL",
            "--max-time",
            "30",
            "-H",
            "Accept: application/vnd.github+json",
            "-H",
            "User-Agent: github-search-skill/1.0",
        ]
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if token:
            command.extend(["-H", f"Authorization: Bearer {token}"])
        command.append(f"https://api.github.com{path}")
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            stderr = result.stderr.strip() or "curl request failed"
            raise RuntimeError(stderr)
        return json.loads(result.stdout)

    request = urllib.request.Request(
        f"https://api.github.com{path}",
        headers=rest_headers(),
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace").strip()
        detail = body or exc.reason
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(str(exc.reason)) from exc


def github_api(path: str, prefer_gh: bool) -> tuple[Any, str]:
    if prefer_gh:
        try:
            return run_gh_api(path), "gh"
        except RuntimeError:
            pass
    return run_rest_api(path), "rest"


def optional_github_api(path: str, prefer_gh: bool) -> tuple[Any | None, str]:
    try:
        return github_api(path, prefer_gh)
    except RuntimeError:
        return None, "missing"


def decode_readme(raw: str | None) -> str:
    if not raw:
        return ""
    decoded = base64.b64decode(raw).decode("utf-8", errors="replace")
    lines = [line.rstrip() for line in decoded.splitlines()]
    preview_lines: list[str] = []
    for line in lines:
        if not line.strip() and not preview_lines:
            continue
        preview_lines.append(line)
        if len(preview_lines) >= 40:
            break
    preview = "\n".join(preview_lines).strip()
    return preview[:2000]


def collect_repo_metadata(repo_ref: RepoRef, prefer_gh: bool) -> dict[str, Any]:
    repo_payload, source = github_api(f"/repos/{repo_ref.full_name}", prefer_gh)
    contents_payload, contents_source = github_api(
        f"/repos/{repo_ref.full_name}/contents", prefer_gh
    )
    readme_payload, readme_source = optional_github_api(
        f"/repos/{repo_ref.full_name}/readme", prefer_gh
    )

    entries = contents_payload if isinstance(contents_payload, list) else []
    top_level_dirs = sorted(item["name"] for item in entries if item.get("type") == "dir")
    top_level_files = sorted(item["name"] for item in entries if item.get("type") == "file")

    return {
        "input": repo_ref.raw,
        "repo": repo_ref.full_name,
        "source": {
            "repo": source,
            "contents": contents_source,
            "readme": readme_source,
        },
        "html_url": repo_payload.get("html_url"),
        "description": repo_payload.get("description"),
        "stars": repo_payload.get("stargazers_count"),
        "forks": repo_payload.get("forks_count"),
        "watchers": repo_payload.get("subscribers_count"),
        "language": repo_payload.get("language"),
        "topics": repo_payload.get("topics") or [],
        "default_branch": repo_payload.get("default_branch"),
        "license": (repo_payload.get("license") or {}).get("spdx_id")
        or (repo_payload.get("license") or {}).get("name"),
        "archived": repo_payload.get("archived", False),
        "pushed_at": repo_payload.get("pushed_at"),
        "updated_at": repo_payload.get("updated_at"),
        "top_level_dirs": top_level_dirs,
        "top_level_files": top_level_files,
        "readme": {
            "present": bool(readme_payload),
            "path": readme_payload.get("path") if readme_payload else None,
            "preview": decode_readme(readme_payload.get("content")) if readme_payload else "",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect standardized metadata for shortlisted GitHub repositories."
    )
    parser.add_argument("repos", nargs="+", help="Repo refs like owner/repo or GitHub URLs")
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation level (default: 2)",
    )
    args = parser.parse_args()

    prefer_gh = gh_ready()
    results: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []

    for raw_ref in args.repos:
        try:
            repo_ref = parse_repo_ref(raw_ref)
        except ValueError as exc:
            errors.append({"input": raw_ref, "error": str(exc)})
            continue

        try:
            results.append(collect_repo_metadata(repo_ref, prefer_gh))
        except Exception as exc:  # noqa: BLE001
            errors.append({"input": raw_ref, "repo": repo_ref.full_name, "error": str(exc)})

    payload = {
        "repos": results,
        "errors": errors,
        "used_gh": prefer_gh,
    }
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=args.indent)
    sys.stdout.write("\n")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
