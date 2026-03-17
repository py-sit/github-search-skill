#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Clone or update GitHub repositories into ~/Desktop/github-search.

Usage:
  clone_or_update_repos.sh [--target-root PATH] [--depth N] <repo> [<repo> ...]

Repo formats:
  owner/repo
  https://github.com/owner/repo
  https://github.com/owner/repo.git
  git@github.com:owner/repo.git
EOF
}

target_root="${HOME}/Desktop/github-search"
depth="1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target-root)
      target_root="$2"
      shift 2
      ;;
    --depth)
      depth="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
    *)
      break
      ;;
  esac
done

if [[ $# -lt 1 ]]; then
  usage >&2
  exit 1
fi

mkdir -p "$target_root"

parse_repo() {
  local ref="$1"
  if [[ "$ref" =~ ^https://github\.com/([^/]+)/([^/]+?)(\.git)?/?$ ]]; then
    echo "${BASH_REMATCH[1]} ${BASH_REMATCH[2]}"
    return 0
  fi

  if [[ "$ref" =~ ^git@github\.com:([^/]+)/([^/]+?)(\.git)?$ ]]; then
    echo "${BASH_REMATCH[1]} ${BASH_REMATCH[2]}"
    return 0
  fi

  if [[ "$ref" =~ ^([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)$ ]]; then
    echo "${BASH_REMATCH[1]} ${BASH_REMATCH[2]}"
    return 0
  fi

  return 1
}

status_code=0

for ref in "$@"; do
  if ! parsed="$(parse_repo "$ref")"; then
    echo "ERROR ${ref} :: unsupported repo reference" >&2
    status_code=1
    continue
  fi

  owner="${parsed%% *}"
  repo="${parsed##* }"
  url="https://github.com/${owner}/${repo}.git"
  dest="${target_root}/${owner}__${repo}"

  if [[ -e "$dest" && ! -d "$dest/.git" ]]; then
    echo "SKIPPED ${dest} :: path exists but is not a git repository"
    status_code=1
    continue
  fi

  if [[ ! -e "$dest" ]]; then
    if git clone --depth "$depth" "$url" "$dest"; then
      echo "CLONED ${dest} :: ${url}"
    else
      echo "CLONE-FAILED ${dest} :: ${url}" >&2
      status_code=1
    fi
    continue
  fi

  if ! git -C "$dest" fetch --depth "$depth" origin; then
    echo "UPDATE-FAILED ${dest} :: fetch failed" >&2
    status_code=1
    continue
  fi

  default_ref="$(git -C "$dest" symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null || true)"
  if [[ -z "$default_ref" ]]; then
    default_ref="origin/main"
  fi

  if ! git -C "$dest" reset --hard "$default_ref"; then
    echo "UPDATE-FAILED ${dest} :: reset failed (${default_ref})" >&2
    status_code=1
    continue
  fi

  if ! git -C "$dest" clean -fd; then
    echo "UPDATE-FAILED ${dest} :: clean failed" >&2
    status_code=1
    continue
  fi

  echo "UPDATED ${dest} :: ${default_ref}"
done

exit "$status_code"
