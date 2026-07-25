# Task for w1 — naming/UX investigation (issue #19, questions 1+2)

## WHY (the reason this matters)
The repo (C:\Users\devic\source\marketplace, GitHub DgxSparkLabs/marketplace) is being scoped
down to a skills-only, Claude-Code-only template marketplace that people fork (umbrella issue
#18). Naming and user interaction are a first-class design value: every future expansion is
gated on issue #19's naming/UX standard. Your findings feed two later PRs: CI naming
validation (PR 3) and the README "make it yours" fork checklist (PR 4). The manager is
executing code PRs in the main working tree in parallel — that is why you work in your own
worktree and deliver to GitHub, not to the repo files.

## Read first (you have no session context)
- HANDOFF.md + PITFALLS.md (repo root) — mandatory per project rules
- docs/LESSONS.md — especially lesson 7 (brand identity derives from src/MARKETPLACE.toml
  via `brand = marketplace_name.removesuffix("-marketplace")` in scripts/constructs.py) and
  lesson 5 (probe the live CLI, don't trust docs; record `claude --version`)
- Issue #19 body: gh issue view 19 -R DgxSparkLabs/marketplace

## HOW (steps and constraints)
1. Do NOT touch the main working tree — the manager is branching/deleting in it. Make your
   own read-only worktree: `git worktree add ../marketplace-w1-research main` and work there.
2. Trace the name-resolution chain in code (cite file:line): src/MARKETPLACE.toml →
   scripts/constructs.py brand derivation → plugin.json `name` fields →
   .claude-plugin/marketplace.json entries → what `claude plugin marketplace add` and
   `/plugin install <name>@<marketplace>` actually key on. Note which names come from the
   GitHub repo slug vs MARKETPLACE.toml vs the skill folder name vs SKILL.md frontmatter.
3. Probe the live CLI where possible (`claude --version`, `claude plugin --help`,
   marketplace add of the local checkout) — record version next to each behavioral claim.
   Cross-check https://code.claude.com/docs/en/plugin-marketplaces and /docs/en/skills.
4. Answer #19 Q1 (install-command surface: exact commands, full resolution chain) and Q2
   (scoped-name surface in-session: `<plugin>:<skill>`, typeahead, collisions). Also list,
   as input to Q3, every place the brand/owner appears that a forker would need to change.
5. When done: `git worktree remove ../marketplace-w1-research`.

## WHAT (deliverable shape)
A single comment posted on issue #19 (`gh issue comment 19 -R DgxSparkLabs/marketplace
--body-file <your-draft>`) with sections: "Q1 — name-resolution chain" (with file:line
citations + CLI version), "Q2 — scoped-name surfaces", "Input to Q3 — fork-rename
inventory", "Open unknowns". Evidence over opinion; label judgment as judgment.

## Report back
Append to .agent-mail/to-manager.md: `- [HH:MM] (w1) done — #19 comment posted <URL>`.
If blocked: `- [HH:MM] (w1) blocked — <exact thing you need>` and wait.
