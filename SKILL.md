---
name: github-search
description: Search GitHub for mature public implementations, compare fit by stack, license, and activity, optionally clone up to 3 strong candidates, and propose a reuse plan with source attribution. Use for requests like "find similar repos", "compare OSS options", "search GitHub for a mature implementation", "找类似仓库", "找成熟实现", and "先参考开源实现". Skip docs-only questions, purely local fixes, or tasks limited to editing one named repository.
---

# GitHub Search

## Overview

Use GitHub-first repository research when existing public implementations can improve engineering speed or quality. Default behavior: define the search brief, shortlist strong candidates, collect standardized metadata, compare them in a compact table, and clone at most 3 repos only when there is a clear reuse case.

## Trigger / Skip

Use this skill when the user asks to:

- search GitHub for similar repos or mature implementations
- compare open-source options by stack, stars, recent activity, or license
- inspect README, repo layout, or reusable modules before building
- 找类似仓库、找成熟实现、先参考开源实现、按 star / 最近更新 / 语言筛选

Skip this skill when:

- the task is docs-only
- the task is a purely local fix and the current repo already has enough context
- the user already named the exact repo and only wants edits or explanation inside it
- the user explicitly forbids external GitHub research

## Search Brief Gate

Before searching, confirm or explicitly infer:

- problem to solve
- target stack
- runtime
- deployment model
- license floor or license sensitivity
- what counts as reusable output

Then choose the minimum viable path:

- compare only if the user mainly wants options
- clone and analyze only if there is at least one strong reuse candidate

Read [references/query-patterns.md](references/query-patterns.md) when you need concrete query syntax examples.

## Bounded Workflow

1. Search GitHub MCP first with 2-4 materially different query variants. Prefer repository search, then README or root file inspection.
2. Build a shortlist of 3-5 candidates. If GitHub MCP is unavailable, fall back to authenticated `gh` or the bundled metadata script's REST fallback.
3. For every shortlisted repo, collect standardized metadata before ranking:
   - stars
   - absolute last activity date
   - license
   - primary language or stack clues
   - README presence and preview
   - top-level files and directories
4. Use `scripts/collect_repo_metadata.py` for deterministic metadata collection.
5. Produce a compact comparison table before cloning.
6. Clone at most 3 strong candidates into `/Users/yrpy/Desktop/github-search` with `scripts/clone_or_update_repos.sh`.
7. Analyze cloned repos locally and propose deliberate reuse with repo and file attribution.

If no candidate clears the evaluation gates, stop and return `Reference only` or `Reject` instead of forcing a weak clone.

## Evaluation Gates

A candidate must be compared on all 6 fields:

- stack fit
- absolute last activity date
- license
- README or examples quality
- reusable surface
- coupling or integration risk

Default reject or downgrade rules:

- no license
- clearly stale without explicit justification
- toy demo or tutorial-only repo
- wrong stack for the target
- strong product or platform lock-in that blocks reuse

Use absolute dates in the comparison table, not vague labels like `recent` or `active`.

Read [references/evaluation-checklist.md](references/evaluation-checklist.md) for the scoring rubric and gate details.

## Output Contract

Unless the user asks for another format, return:

1. search brief
2. candidate comparison table
3. top repos to clone, with one-line reasons
4. local analysis summary for cloned repos
5. reuse plan with source repo and file attribution
6. risks, license notes, and what was intentionally not reused

Read [references/output-template.md](references/output-template.md) when you need a reusable response skeleton.
