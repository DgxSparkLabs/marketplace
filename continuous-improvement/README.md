# continuous-improvement

An always-on rule that gives AI agents a structured seven-phase workflow for finding, planning, validating, implementing, testing, documenting, and self-reviewing codebase improvements. Synthesized from Google's code review practices, Nielsen's usability heuristics, and refactoring.guru patterns.

Unlike a skill (which must be invoked), this is a **rule** — it activates automatically in every session with no user action needed.

## Quick Install

```bash
git clone https://github.com/ForkYoraiLevi/marketplace.git /tmp/marketplace

# Install into current project (all agent formats)
/tmp/marketplace/continuous-improvement/install.sh

# Install globally (all projects, all agent formats)
/tmp/marketplace/continuous-improvement/install.sh --global

# Install for a specific tool only
/tmp/marketplace/continuous-improvement/install.sh --format windsurf
/tmp/marketplace/continuous-improvement/install.sh --format cursor
/tmp/marketplace/continuous-improvement/install.sh --format claude
/tmp/marketplace/continuous-improvement/install.sh --format agents
```

## Manual Install

Copy the appropriate format file to your project or global config:

### AGENTS.md (universal)

Append the contents of `rule.md` to your project's `AGENTS.md`:

```bash
cat continuous-improvement/rule.md >> AGENTS.md
```

### Windsurf

```bash
mkdir -p .windsurf/rules
cp continuous-improvement/formats/windsurf.md .windsurf/rules/continuous-improvement.md
```

### Cursor

```bash
mkdir -p .cursor/rules
cp continuous-improvement/formats/cursor.md .cursor/rules/continuous-improvement.md
```

### Claude Code

Append the contents of `rule.md` to your `CLAUDE.md`:

```bash
cat continuous-improvement/rule.md >> CLAUDE.md
```

## What it enforces

The rule defines a mandatory seven-phase workflow when an agent is asked to improve a codebase:

1. **Discovery** — Systematically audit for code smells, error handling gaps, edge cases, security weaknesses, usability friction, missing tests, documentation gaps, performance issues, and inconsistencies
2. **Planning** — Organize findings by category and priority, present the plan before implementing
3. **Validation** — Verify assumptions by reproducing problems, reading git history, and checking conventions before changing anything
4. **Implementation** — Make minimal, convention-following changes one at a time, applying UX heuristics and defensive programming principles
5. **Testing** — Write regression tests, run the full suite, verify edge cases, and confirm zero new warnings
6. **Documentation** — Update docs alongside code, write clear commit messages, document new patterns
7. **Self-Review** — Critically evaluate your own work: would you approve this in a code review? Fix anything that falls short before declaring done.

## Sources

The rule content is synthesized from established software engineering practices:

- [Google Engineering Practices — What to Look For in Code Review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- [Nielsen Norman Group — 10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)
- [Refactoring Guru — Refactoring Catalog](https://refactoring.guru/refactoring/catalog)
- Defensive programming and continuous improvement (Kaizen) principles

## How it works

This is a **rule**, not a skill. Rules are loaded automatically at session start and stay active for the entire session. No invocation needed.

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/continuous-improvement.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/continuous-improvement.md` | `alwaysApply: true` |
| Claude Code | `CLAUDE.md` (appended) | Always on |
