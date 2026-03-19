# Repo Evaluation Checklist

Use this rubric before any clone step. Every shortlisted repo must be compared on the same six fields.

## Required comparison fields

- stack fit
- absolute last activity date
- license
- README or examples quality
- reusable surface
- coupling or integration risk

Do not write vague labels like `recent` or `active`. Always output the actual date.

## Hard gates

Default to `Reject` or `Reference only` when any of these is true:

- no license
- last meaningful activity is clearly stale for the target use case and there is no explicit justification
- toy demo, tutorial-only repo, or mostly generated code
- wrong stack for the target task
- strong product, vendor, or platform lock-in that makes reuse unrealistic

For staleness, use the current date when evaluating and explain the risk in plain language.

## Fast scoring

Score each field from 1 to 5:

- stack fit: same problem and compatible stack, or only adjacent
- activity: healthy maintenance, or outdated and risky
- license: clearly reusable, or unclear or restrictive
- docs quality: README, setup, and examples are trustworthy, or thin
- reusable surface: isolated modules or patterns exist, or code is monolithic
- integration risk: adaptation cost is low, or coupling is high

## Signals

Strong signals:

- clear README with setup, architecture, and examples
- recent commits or releases
- tests, examples, or demo apps
- modular structure with obvious reusable boundaries
- popularity that makes sense for the niche

Weak signals:

- screenshots with little code
- very old last meaningful update
- no license or unclear license
- monolithic structure with poor separation
- heavy vendor coupling or hidden hosted dependencies
- large amounts of generated code without explanation

## Recommendation labels

Use one of these labels in the final summary:

- `Direct dependency`
- `Partial reuse`
- `Reference only`
- `Reject`
