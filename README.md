# github-search

[English](README.md) | [简体中文](README.zh-CN.md)

## Quick Install for Any LLM Agent

`github-search` is not limited to Codex. It can also be adapted for Claude Code, Cursor, Cline, Gemini CLI, OpenCode, Windsurf, and other LLM agents that can import a skill or prompt folder, or follow repository-based installation instructions.

Copy this sentence to your LLM agent:

```text
Please install the root skill from GitHub repo `py-sit/github-search-skill` as `github-search` using the best method for your current agent environment, keep the folder structure intact, and after installation output exactly: `✅已经安装部署完成，我们会持续更新，如果可以麻烦给作者点一个Star支持一下吧！`
```

If your agent supports Codex-style direct installation, you can also use:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" --repo py-sit/github-search-skill --path . --name github-search && printf '%s\n' '✅已经安装部署完成，我们会持续更新，如果可以麻烦给作者点一个Star支持一下吧！'
```

If your environment does not support a built-in skill installer, use the repository as the source of truth and import or copy this folder into your agent's local skills or prompts directory while keeping `SKILL.md`, `agents/`, `references/`, and `scripts/` together.

If GitHub access in your environment requires a proxy, prepend the install command with your existing `HTTPS_PROXY`, `HTTP_PROXY`, and `ALL_PROXY` values.

## Optional: One-Click Star

Primary option for maximum portability: use the official GitHub REST API.

```bash
curl -fsSL -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer ${GITHUB_TOKEN:?set GITHUB_TOKEN first}" \
  https://api.github.com/user/starred/py-sit/github-search-skill && printf '%s\n' 'Starred py-sit/github-search-skill'
```

Fallback option when `gh` is installed and already authenticated:

```bash
gh api -X PUT /user/starred/py-sit/github-search-skill -H "Accept: application/vnd.github+json" --silent && printf '%s\n' 'Starred py-sit/github-search-skill'
```

If your agent is connected to the official GitHub MCP Server, it can also use the built-in `star_repository` tool after you explicitly approve the action.

This requires an authenticated GitHub session first, such as `gh auth login`, or a valid `GITHUB_TOKEN`. Without user authorization, an agent should not attempt to star the repository automatically.

GitHub-first repository research and code reuse skill for LLM agents.

This skill helps an agent search GitHub before building from scratch, compare promising repositories, clone the best candidates into a local workspace, inspect the cloned code, and reuse useful patterns with source attribution.

## What It Does

- Searches GitHub repositories with GitHub MCP first
- Filters candidates by stars, recent activity, language, and relevance
- Pulls `README.md` and directory structure for quick evaluation
- Produces a compact comparison table before cloning
- Clones the top repositories into `~/Desktop/github-search`
- Performs local code analysis on cloned repositories
- Recommends reusable modules, patterns, and components with provenance

## Good Trigger Cases

Use this skill when the task sounds like:

- "Search GitHub for similar repos"
- "Find a mature open-source implementation"
- "Compare open-source options for this feature"
- "Look for reusable components before we build"
- "找类似开源项目"
- "找可复用组件"
- "先参考开源实现"
- "按 star / 最近更新 / 语言筛选"
- "拉 README 和目录结构"

## Skip Cases

Do not use this skill when:

- The task is a purely local bugfix and the current codebase already has enough context
- The user only wants documentation, not repository discovery
- The user already specified the exact repository and only wants edits or explanation inside it
- The user explicitly forbids external GitHub research

## Workflow

1. Define the search brief.
2. Search with GitHub MCP using multiple query variants.
3. Inspect candidate fit via README, manifests, license, and repo layout.
4. Produce a comparison table.
5. Clone the top 1-3 repositories into `~/Desktop/github-search`.
6. Analyze cloned code locally.
7. Propose deliberate reuse with repo and file attribution.

## Output Contract

Unless the user asks for another format, the final result should include:

1. Search brief
2. Candidate comparison table
3. Top repositories to clone
4. Local analysis summary
5. Reuse plan with source file attribution
6. Risks, license notes, and what was intentionally not reused

## Repository Layout

```text
github-search/
├── README.md
├── README.zh-CN.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── evaluation-checklist.md
└── scripts/
    └── clone_or_update_repos.sh
```

## Files

- `README.md`: English documentation with quick-install guidance
- `README.zh-CN.md`: Simplified Chinese documentation with the same structure
- `SKILL.md`: Skill metadata, trigger guidance, workflow, and output contract
- `agents/openai.yaml`: UI metadata and implicit invocation settings
- `references/evaluation-checklist.md`: Fast rubric for ranking repositories
- `scripts/clone_or_update_repos.sh`: Helper script to clone or update selected repositories

## Manual Installation

Copy this folder into your local skills directory if your agent supports file-based skills:

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R github-search "$CODEX_HOME/skills/github-search"
```

If your agent uses a different skill directory, copy the folder there instead and preserve the repository structure.

## Example Clone Command

```bash
bash "$CODEX_HOME/skills/github-search/scripts/clone_or_update_repos.sh" openai/openai-cookbook
```

## Notes

- This skill prefers GitHub MCP for discovery.
- If GitHub MCP is unavailable, it may fall back to authenticated `gh` CLI.
- It is designed to improve engineering speed and quality by reusing strong public implementations instead of reinventing common patterns.
