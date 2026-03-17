# Repo Evaluation Checklist

Use this rubric when multiple GitHub repos look relevant and you need a sharper ranking.

## Fast scoring

Score each repo from 1 to 5 on:

- Problem fit: Does it solve the same problem or only a nearby one?
- Maintenance: Is it recently updated and clearly still alive?
- Extraction value: Can useful modules be reused without importing the whole repo?
- Code quality: Are structure, naming, tests, and docs good enough to trust?
- Integration cost: How hard will it be to adapt to the current stack?
- License safety: Is reuse compatible with the current task?

## Strong signals

- Clear README with setup, architecture, and examples
- Recent commits or releases
- Tests, examples, or demo apps
- Modular structure with obvious reusable boundaries
- Popularity that matches the niche; small niches do not always need huge stars

## Weak signals

- Mostly screenshots with little code
- Last meaningful update is very old
- No license or unclear license
- Monolithic code with poor separation
- Heavy vendor coupling or hidden hosted dependencies
- Generated or copied code with little explanation

## Reuse recommendation labels

Use one of these labels in your summary:

- Direct dependency: Good candidate to add as a package or service dependency
- Partial reuse: Good source for isolated modules, prompts, schemas, or patterns
- Reference only: Useful for ideas or architecture, not for direct code reuse
- Reject: Not worth cloning or reusing
