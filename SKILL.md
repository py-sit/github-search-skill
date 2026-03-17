---
name: github-search
description: GitHub-first repository research and code reuse workflow for engineering problems. Use when the user asks to search GitHub, find similar open-source repos, 找类似开源项目, 找成熟实现, 比较开源方案, 参考现成仓库, filter by stars or recent activity or language, inspect README or directory structure, clone promising repos, or reuse helpful code before building from scratch. Also prefer this skill when a coding task could benefit from existing public implementations and the user did not forbid external research. Skip for purely local fixes with enough context, docs-only questions, or exact-repo edit requests with no discovery need.
---

# GitHub Search

## Overview

Prefer GitHub MCP as the first external research step for implementation-oriented problems. Search broadly enough to find strong candidates, compare them in a compact table, clone the most promising repos into `/Users/yrpy/Desktop/github-search`, then inspect the cloned code locally before reusing anything.

Default behavior: if the task may benefit from an existing public implementation and the user did not forbid external research, use this skill before designing from scratch.

Skip the GitHub-first step only when the user explicitly forbids GitHub search, the task is purely local and already has the needed code, the question is documentation-only, or the user already named the exact repo to use and only wants edits or explanation inside that repo.

Common trigger phrases include:

- "search GitHub for this"
- "find similar repos"
- "compare open-source options"
- "look for a mature implementation"
- "找类似仓库"
- "找可复用组件"
- "先参考开源实现"
- "按 star / 最近更新 / 语言筛选"
- "拉 README 和目录结构"

## Workflow

### 1. Define the search brief

- Extract the problem to solve, target stack, runtime, deployment model, and what counts as a useful repo.
- Build 3-6 search queries:
  - a broad problem query
  - a stack-specific query
  - an architecture or subsystem query
  - a template or boilerplate query when relevant

Example query shapes for GitHub search syntax:

```text
"openai compatible api gateway" stars:>=100 pushed:>=2024-01-01 language:Go archived:false
"wechat mini program llm" stars:>=20 pushed:>=2024-01-01 language:TypeScript archived:false
"billing platform" stars:>=50 pushed:>=2023-01-01 archived:false
```

### 2. Search with GitHub MCP first

- Prefer GitHub MCP repository search before generic web search whenever existing code could help.
- Use `search_repositories` to discover repos.
- Use `get_file_contents` to pull `README.md` and top-level directory listings.
- Use `search_code` only after a repo shortlist exists and you need to find specific files or patterns.
- Search with at least 2 materially different query variants unless the user already narrowed the target tightly.
- Filter with GitHub search syntax when possible:
  - `stars:>=N`
  - `pushed:>=YYYY-MM-DD`
  - `language:TypeScript`
  - `archived:false`
  - `topic:<name>` when useful

If GitHub MCP is unavailable or insufficient:

- Fall back to `gh` CLI if it is installed and authenticated.
- If neither GitHub MCP nor authenticated `gh` is available, say so explicitly and avoid pretending a GitHub search was completed.

### 3. Inspect candidate fit

- Pull `README.md` with GitHub MCP for each promising repo.
- Inspect the top-level directory structure with GitHub MCP when directory listing is available; otherwise clone early and inspect locally.
- Check key files when relevant:
  - `README.md`
  - `LICENSE`
  - `package.json`
  - `pnpm-workspace.yaml`
  - `pyproject.toml`
  - `requirements.txt`
  - `go.mod`
  - `Cargo.toml`
  - `docker-compose.yml`
  - `src/`, `packages/`, `apps/`, `server/`, `backend/`, `examples/`, `docs/`
- Reject repos that are abandoned, toy demos, the wrong stack, tightly coupled to another product, or license-incompatible.

### 4. Output a candidate comparison table

Always produce a compact comparison table before cloning. Use this shape:

| Repo | Why relevant | Stack | Stars | Recent activity | Reuse targets | Risks |
| --- | --- | --- | ---: | --- | --- | --- |

- Prefer 3-6 repos in the table.
- Rank the candidates.
- Clearly call out the top 1-3 repos worth cloning.

### 5. Clone the winners into the desktop workspace

- Ensure `/Users/yrpy/Desktop/github-search` exists.
- Clone only the top 1-3 promising repos unless the user explicitly asks for more.
- Use the bundled script `scripts/clone_or_update_repos.sh` to clone or update repos under stable folder names. Resolve it relative to the skill directory, for example: `$CODEX_HOME/skills/github-search/scripts/clone_or_update_repos.sh`.
- Use shallow clones by default.

Examples:

```bash
bash "$CODEX_HOME/skills/github-search/scripts/clone_or_update_repos.sh" openai/openai-cookbook
bash "$CODEX_HOME/skills/github-search/scripts/clone_or_update_repos.sh" https://github.com/vercel/ai.git open-webui/open-webui
```

### 6. Run full local analysis on cloned repos

After cloning, inspect the repos locally instead of relying only on remote metadata.

- Prefer `rg --files`, `rg -n`, `find`, README, manifests, tests, examples, and entrypoints.
- Identify concrete reuse opportunities:
  - isolated utilities
  - API clients
  - prompts and schemas
  - UI components
  - parsers
  - storage layers
  - deployment templates
  - test patterns
- Prefer extracting minimal components or patterns over copying an entire repository.

### 7. Reuse code deliberately

- State which repo and file contributed each reused idea or component.
- Check `LICENSE` before substantial reuse.
- Prefer adaptation over verbatim copying.
- Avoid importing secrets, telemetry config, or environment-specific glue without understanding it.
- Treat searched repos as inputs to engineering judgment, not automatic truth.

## Output contract

Unless the user explicitly asks for a different format, structure the deliverable in this order:

1. Search brief
2. Candidate comparison table
3. Top repos to clone, with a one-line reason for each
4. Local analysis summary for cloned repos
5. Reuse plan with source repo and file attribution
6. Risks, license notes, and what was intentionally not reused

If no repo is strong enough, say that clearly and return a reject-or-reference-only recommendation instead of forcing a weak clone.

## Local analysis checklist

When inspecting a cloned repo, answer these questions:

- What problem does this repo actually solve?
- Which files are the real entrypoints?
- Which modules are reusable with minimal adaptation?
- Which parts are tightly coupled and not worth importing?
- Is the repo more useful as inspiration, partial reuse, or a direct dependency?
- What license or integration risk exists?

Read [references/evaluation-checklist.md](references/evaluation-checklist.md) when you need a reusable scoring rubric.
