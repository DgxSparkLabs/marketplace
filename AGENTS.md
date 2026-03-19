# Agent Instructions

This is a skills and rules marketplace. Not a software project — no build system, no package manager.

**New here?** Read `docs/ONBOARDING.md` for a 3-minute orientation. For market intelligence, start with `research/KNOWLEDGE_BASE.md`.

Skills live under `skills/` and rules under `rules/`.
- Has `SKILL.md` → skill
- Has `rule.md` + `install.sh` → rule

## Layout

```
marketplace/
├── catalog.toml                # TUI installer configuration (platforms, families, MCP)
├── docs/
│   ├── SKILL_FORMAT.md         # Full SKILL.md spec
│   └── RULE_FORMAT.md          # Full rule spec
├── _template/                  # Starter for new skills
├── rules/
│   └── no-ai-credit/           # Reference rule
├── skills/
│   └── send-email/             # Reference skill
└── ...
```

## Adding a Skill

Use `_template/` as a starter. Full spec in `docs/SKILL_FORMAT.md`.

```
my-skill/
├── SKILL.md            # Required
├── README.md           # Required
├── scripts/            # Optional
├── setup.sh            # Optional — prerequisite installer
└── references/         # Optional
```

- Python scripts must use PEP 723 inline metadata (`uv run` with zero install)
- Always set `allowed-tools` to minimum needed
- Update the **Skills** table in root `README.md` (alphabetical)

## Adding a Rule

Use `rules/no-ai-credit/` as a reference. Full spec in `docs/RULE_FORMAT.md`.

```
my-rule/
├── rule.md             # Required — plain Markdown, no frontmatter
├── README.md           # Required
├── install.sh          # Required — supports --global and --format
└── formats/
    ├── windsurf.md     # trigger: always_on
    └── cursor.md       # alwaysApply: true
```

- Copy and adapt `rules/no-ai-credit/install.sh`
- Update the **Rules** table in root `README.md` (alphabetical)

## Conventions

- Directory names: **kebab-case**
- Script filenames: **snake_case** for Python, **kebab-case** allowed for shell scripts
- Python scripts: PEP 723, runnable via `uv run`
- Shell scripts: shebang + `set -euo pipefail`
- Never commit secrets
- Do not add project-level config (`pyproject.toml`, `package.json`, etc.) at root
- Do not mix skill and rule formats in one directory

## Testing

Run the test suite to validate all skills, rules, and install scripts:

```
uv run tests/test_marketplace.py        # all tests
uv run tests/test_marketplace.py -v     # verbose
uv run tests/test_marketplace.py -k rule  # only rule tests
```

The test suite checks: directory structure, YAML frontmatter, catalog consistency, PEP 723 metadata, shell script safety, install script behavior (--help, --global, idempotency), format file content parity, and secret scanning. Always run the tests before submitting changes.

Run the CI workflow locally with [act](https://github.com/nektos/act) and podman:

```
./tests/run-ci-local.sh          # run the full GitHub Actions workflow locally
./tests/run-ci-local.sh -n       # dry-run (no container)
```

## Marketplace Testing

Always run `uv run tests/test_marketplace.py` before declaring done.

## Research Directory

The `research/` directory contains 90+ files across 12 research rounds. Read `research/README.md` before modifying any research file.

**Critical rules:**

- **Canonical files** are the top-level `.md` files in `research/` (e.g., `arxiv_findings.md`, `github_findings.md`, `SUMMARY_AND_CONCLUSIONS.md`). These represent carefully consolidated findings across all rounds.
- **Never wholesale-rewrite a canonical file.** Merge new findings incrementally into the existing structure. Rewrites lose data — past attempts dropped 21 arXiv papers and 38 GitHub repos.
- **Archival rounds** live in `research/skill-marketplaces-N/`. These are raw research data, not authoritative. New rounds go in `skill-marketplaces-N+1/`.
- **Verify before citing.** Star counts and repo existence must be checked against live sources before adding to canonical files. Prior rounds contain unverified data.
- **Raw artifacts are gitignored.** Scrape dumps, notebook outputs, and batch results are excluded. Only curated analysis files are committed.
- **Note provenance.** When adding a data point, note which research round or source it came from.
- See `research/TASKS.md` for the current maintenance backlog.

## No AI Credit

Never attribute work to yourself or to any AI agent, tool, or assistant. This applies to every artifact you produce or modify.

- NEVER add "Co-Authored-By" lines referencing any AI agent or bot in git commits.
- NEVER add "Generated with", "Created by", "Built with", "Powered by", or similar AI attribution to git commits, PRs, code comments, documentation, READMEs, changelogs, or any other output.
- NEVER add badges, links, sections, or footnotes crediting an AI tool or agent.
- NEVER add file headers or authorship lines that reference an AI tool.
- NEVER include `noreply@` email addresses associated with AI bots in commits.
- Git commit messages must contain only the actual change description — no agent attribution of any kind.

Before completing any task, scan your output for:
- "Co-Authored-By" lines referencing any AI or bot
- "Generated with" / "Created by" / "Built with" / "Powered by" followed by an AI tool name
- Any mention of an AI agent name as an author or contributor
- Badges or links that credit an AI tool
- `noreply@` email addresses associated with AI bots

If any of these are present, remove them before finishing. No exceptions.

## Writing Rules — Keep Them Concise

Rules consume agent context in every session. Verbose rules dilute attention and waste context budget.

- **Aim for actionable checklists, not documentation.** If a rule reads like an essay, it's too long.
- **Every line should be an instruction the agent can act on.** Remove explanations of *why* — agents need *what* and *when*.
- **Consolidate** — 5 crisp bullet points beat 40 lines of prose.
- Rules installed to multiple targets appear multiple times in agent context. Use `--format agents` to install to a single target.

## Blast Radius

Before making any change, estimate its blast radius — how many files it touches, how complex the diff will be, and how hard it is to revert.

- **Estimate first:** How many files? (>5 = break it up.) How complex? Can you revert cleanly?
- **Small atomic changes.** One commit = one purpose. Each independently revertable.
- **State your approach** in one sentence before coding. List files you expect to modify.
- **If >2x longer than expected**, STOP and reassess. Do not push through.
- **Simple > clever.** Do not build abstractions for one-time problems. When in doubt, do less.
- **Know your limits.** If the scope exceeds what fits in context, say so. Don't guess.

## Pitfalls Discipline

Maintain a `PITFALLS.md` file in every project. This is the knowledge base of things that went wrong and how they were fixed.

### Before complex work

- Check `PITFALLS.md` for entries related to the area you're touching.
- Search git log for relevant fixes: `git log --oneline --grep="<keyword>"`.
- If a past pitfall is relevant, factor it into your approach before writing code.

### After fixing a bug

- Add an entry: **symptom** (what you observed), **cause** (root cause), **fix** (what resolved it), **commit** (reference).
- Keep entries concise — 2-4 lines each.

### Promotion

- If a pitfall recurs across projects, promote it to a global rule in `AGENTS.md`.
- If a pitfall can be prevented structurally (test, hook, validation), add the guardrail and note it in the entry.

## Prior Art

Before building anything non-trivial, search for existing solutions first.

1. **In the codebase** — check for existing utilities, helpers, patterns.
2. **In dependencies** — check package.json/Cargo.toml/requirements.txt before adding anything new.
3. **On the web** — use `duckduckgo-search` skill for established packages and patterns.
4. **On GitHub** — use `github-search` skill for repos with stars, license, and freshness info.

**Evaluate:** maintenance status, adoption, scope fit, license, security.

**Always report** what you found: "Found X, reusing it" or "Searched for X, nothing suitable, building custom."

## Verification Ladder

Build automated verification at multiple layers. Set up test infrastructure before feature code.

### Layers
0. **Compile** — zero warnings (`-Wall -Wextra` or equivalent)
1. **Unit** — each function/API works correctly (PASS/FAIL/SKIP)
2. **Integration** — multiple functions compose correctly
3. **Performance** — baselines in machine-readable file, warn on >50% regression
4. **End-to-end** — real application smoke test, automated

### Principles
- Every test proves three things: correct **outcome**, correct **mechanism**, clean **side effects**.
- Test the negative path — invalid inputs must produce clean errors, not crashes.
- Distinguish PASS, FAIL, and SKIP — environment problems are SKIPs, not FAILs.
- Automate the most important check first.
- Pre-commit: build must succeed. Pre-push: fast test subset must pass.

## Verify Your Work

Test everything you create before declaring done. Do not assume correctness — prove it.

- **Run the code.** If it produces output, inspect it. If it has side effects, confirm they occurred.
- **Prove three things:** correct outcome, correct mechanism (went through the intended path), clean side effects (no leaks, no stale state).
- **Test the negative path.** Invalid inputs must produce clean errors, not crashes.
- **Be autonomous.** Exhaust all approaches before asking the user for help.
- **Pause for what only the user can provide** — API keys, OAuth, credentials, policy decisions.
- **State what was tested** and what remains untested. Never say "should work."

## Document Lifecycle

Every project has exactly three documentation tiers. No more.

- **Tier 1: Rules** (`AGENTS.md`) — conventions, testing requirements, critical rules. Max 200 lines. No changelogs or history.
- **Tier 2: Reference** (`HANDOFF.md`) — current state, how to build/test, what's next. Updated in-place after every behavior-changing commit.
- **Tier 3: History** (`CHANGELOG.md`) — what changed and when. Append-only.

### Rules
- Never create a document to flag that another is stale — fix the stale one.
- Never duplicate information across tiers.
- If a document has no owner or update trigger, delete it.
- After every behavior-changing commit, `HANDOFF.md` must be accurate.

## Document Progress

For tasks with 3+ steps or 2+ files, write progress to disk. Context compacts and sessions end — files survive.

- **Before starting:** Plan what you'll do in the todo list.
- **After each step:** Mark the todo complete. Update `HANDOFF.md` if behavior changed. Commit.
- **Do NOT rely on conversation memory.** The todo list and `HANDOFF.md` are your memory.
- Never create append-only logs that grow unboundedly. `HANDOFF.md` is edited in-place to reflect current state. History goes in `CHANGELOG.md`.

## Continuous Improvement

When asked to improve or harden a codebase, follow these phases in order:

1. **Discovery** — Audit for code smells, error handling gaps, edge cases, security issues, missing tests, docs gaps, performance problems. Use tools to verify — never guess. List findings with file path, line number, and severity.
2. **Planning** — Group by category, rank by impact, present plan before implementing. One change per commit. Flag anything that could break existing behavior.
3. **Validation** — Confirm each problem exists. Check existing tests. Read git history for context. Do not refactor based on speculation.
4. **Implementation** — Match existing conventions. One change at a time. Simple > clever. Do not over-engineer or rewrite working code without a discovered reason.
5. **Testing** — Write/update tests for every change. Run full suite after each group. Test happy path AND failure modes.
6. **Documentation** — Update docs where behavior changed. Clear commit messages.
7. **Self-review** — Would you approve this in code review? If unsure, fix it or flag it.

## Improve the Process

The task is never just the task. Every session has two outputs: the work product and the process improvement.

### Before finishing a session:
- **Did you hit friction?** Fix the system — add a check, update a doc, improve a script. Don't just work around it.
- **Did you make a mistake?** Add a guardrail — a test, a hook, a validation — so the next agent can't repeat it.
- **Did you discover something useful?** Write it where it'll be found — HANDOFF.md, AGENTS.md, a tool. Not in conversation.
- **Are the rules wrong?** Fix them. The methodology is code. It has bugs. Ship fixes.

### What this looks like:
- Spent 20 minutes debugging an environment issue? Add it to the pre-flight checklist.
- Forgot to update HANDOFF.md? Add a pre-commit check for it.
- Found an undocumented behavior? Add it to HANDOFF.md, not a progress log.
- A test didn't catch a regression? Write the test that would have.

### Why:
Each session that improves the process makes the next session easier. This compounds. A project that improves its workflow every session gets faster over time, not just bigger.

## Session Resilience

You don't have memory. These files do. Everything you learn this session is lost when it ends.

- **Treat every session as your last.** Write state to disk continuously, not just at the end.
- **HANDOFF.md is your memory.** After every meaningful change, update it with current state, what works, what's next.
- **PITFALLS.md captures lessons.** When you fix a bug or discover non-obvious behavior, write it down: symptom, cause, fix.
- **CHANGELOG.md tracks history.** One paragraph per milestone. Append-only.
- **The todo list is your plan.** If it's not in the list, it doesn't exist. If context compacts, the list survives.
- **Never assume the next agent has context.** Write as if someone with zero knowledge will continue your work.
- **The question isn't "did I complete the task?"** — it's "would the next agent thank me for how I left this project?"

## Stay Motivated

The todo list is the definition of completeness. Before stopping, check it.

### "Done" means ALL of these:
- All todo items completed
- Tests pass
- Changes committed
- `HANDOFF.md` accurate

### Before stopping:
- Pending todo items? **Keep working.**
- Finished one step? **Start the next.**
- Hit an error? **Debug it.**
- About to ask a question you could answer by searching? **Search first.**

### If unsure whether you're done:
Invoke `/motivation` — it checks git, HANDOFF.md, build, and tests, then reports what's objectively incomplete.

## Task Formation

### Decompose First

When you receive a request, break it down before coding:

1. **Identify goals** — what are we trying to achieve and why? State the intent, not just the action.
2. **Break into tasks** — each goal becomes actionable tasks with concrete steps.
3. **Write it in the todo list** — the list is the plan. If it's not in the list, it doesn't exist.
4. **Order by dependency** — what must happen first? What's parallel?

Every goal has a "why." Every task has a "done" condition.

### Writing Tasks

- **Define "done"** as one concrete command with one observable outcome before writing any code.
- **Reference code by name, not line number.** "After the declaration of `g_handle_map`" not "after line ~2113."
- **Every task has a pass condition** written before work starts — a specific, verifiable check.
- **Dependency graphs are explicit.** If B depends on A, draw it.
- **Tasks are sized for one session.** If it can't be completed, tested, and committed in one sitting, break it down.

### The Commit Loop
1. State what you're changing in one sentence
2. Write or update the test
3. Make the change
4. Run the test — if it fails, go back to 3
5. Run the full fast suite
6. Update `HANDOFF.md` if behavior changed
7. Commit

## Python UV

ALWAYS use `uv`. NEVER use `pip`, `pip install`, `virtualenv`, `venv`, `pyenv`, `conda`, or `poetry`.

- **Scripts:** PEP 723 inline metadata + `uv run script.py`
- **Projects:** `uv init`, `uv add`, `uv sync`, `uv run`
- **Virtualenvs:** `uv venv` (never `python -m venv`)
- **Global tools:** `uv tool install` (never `pip install --user` or `pipx`)
- If an existing project uses pip/requirements.txt, follow its conventions — do not migrate without asking.
