# Query Patterns

Use this reference only when you need concrete search syntax examples. Keep the main skill flow short and deterministic.

## Query design rules

- Start from the problem, then narrow by stack or subsystem.
- Use 2-4 materially different queries by default.
- Prefer repository search before code search.
- Add filters only when they improve precision:
  - `stars:>=N`
  - `pushed:>=YYYY-MM-DD`
  - `language:<name>`
  - `archived:false`
  - `topic:<name>`

## Recommended query shapes

Use a mix of these patterns:

- broad problem query
- stack-specific query
- architecture or subsystem query
- template or boilerplate query when relevant

Examples:

```text
"openai compatible api gateway" stars:>=100 pushed:>=2024-01-01 language:Go archived:false
"wechat mini program llm" stars:>=20 pushed:>=2024-01-01 language:TypeScript archived:false
"billing platform" stars:>=50 pushed:>=2023-01-01 archived:false
```

## Stop conditions

- Stop after 3-5 credible candidates if they already cover the problem space well.
- Do not keep broadening queries just to fill a table.
- If no strong candidate emerges, say so and return `Reference only` or `Reject`.
