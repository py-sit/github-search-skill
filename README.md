# github-search

GitHub-first repository research and code reuse skill for Codex.

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
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── evaluation-checklist.md
└── scripts/
    └── clone_or_update_repos.sh
```

## Files

- `SKILL.md`: Skill metadata, trigger guidance, workflow, and output contract
- `agents/openai.yaml`: UI metadata and implicit invocation settings
- `references/evaluation-checklist.md`: Fast rubric for ranking repositories
- `scripts/clone_or_update_repos.sh`: Helper script to clone or update selected repositories

## Installation

Copy this folder into your Codex skills directory:

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R github-search "$CODEX_HOME/skills/github-search"
```

If Codex is already running, restart it so the new skill metadata is reloaded.

## Example Clone Command

```bash
bash "$CODEX_HOME/skills/github-search/scripts/clone_or_update_repos.sh" openai/openai-cookbook
```

## Notes

- This skill prefers GitHub MCP for discovery.
- If GitHub MCP is unavailable, it may fall back to authenticated `gh` CLI.
- It is designed to improve engineering speed and quality by reusing strong public implementations instead of reinventing common patterns.
