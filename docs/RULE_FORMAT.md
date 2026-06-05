# Rule Format Reference

Rules are always-on instructions that activate automatically in every agent session. Unlike skills (which must be invoked), rules are loaded at session start and stay active throughout.

This marketplace distributes rules in multiple formats to support different AI agent tools.

---

## Rule Directory Structure (source — `src/rules/<name>/`)

```
my-rule/
├── rule.md             # Required — rule content in plain Markdown (AGENTS.md format)
├── README.md           # Required — documentation with install instructions
└── formats/            # Optional — per-platform rule files; the generator falls back to rule.md if absent
    ├── windsurf.md     # Windsurf format (trigger: always_on)
    └── cursor.md       # Cursor format (alwaysApply: true)
```

The generator (`scripts/generate_manifest.py`) copies `rule.md` into `_generated/rule-<name>/rules/<name>.md` so the per-platform Cursor/Codex manifests can point at it. Rules are **not** a Claude plugin component, so no `plugin.json` or `activate.sh` is emitted — on Claude Code you copy the rule into `.claude/rules/` yourself (see Installation Mechanism below). See [[ADDING_A_CONSTRUCT]] for the workflow (the single contributor walkthrough covers rules along with the other 9 construct types).

---

## rule.md (base format)

The `rule.md` file contains the rule content in plain Markdown with no frontmatter. This is the universal format used by `AGENTS.md`, which loads rules as raw Markdown.

```markdown
## My Rule Title

- Rule instruction one
- Rule instruction two
```

This file is the single source of truth. The format-specific files in `formats/` wrap the same content with tool-specific frontmatter.

---

## Format-Specific Files

### Windsurf (`formats/windsurf.md`)

Windsurf reads rules from `.windsurf/rules/*.md`. Rules must include frontmatter:

```markdown
---
trigger: always_on
description: "Short description of the rule"
---

Rule content here...
```

**Trigger values:**
| Value | Behavior |
|-------|----------|
| `always_on` | Active in every session (use this for rules) |
| `glob` | Active when working with files matching a glob pattern |
| `model_decision` | Agent decides when to apply based on description |
| `manual` | Only active when user explicitly triggers it |

For glob-activated rules, add a `globs` field:
```yaml
---
trigger: glob
description: "TypeScript style rules"
globs: "**/*.{ts,tsx}"
---
```

### Cursor (`formats/cursor.md`)

Cursor reads rules from `.cursor/rules/*.md`. Rules use frontmatter:

```markdown
---
description: "Short description of the rule"
alwaysApply: true
---

Rule content here...
```

**Activation behavior:**
| Configuration | Behavior |
|--------------|----------|
| `alwaysApply: true` | Always active (use this for rules) |
| `globs` specified | Active when working with matching files |
| `description` only | Agent decides when to apply |
| None of the above | User must invoke manually |

### AGENTS.md

This file uses plain Markdown with no frontmatter. Content is always active. To install a rule, append the contents of `rule.md` to the existing file:

```bash
cat rule.md >> AGENTS.md
```

---

## Installation Mechanism

Rules are **not** a Claude plugin component — Claude's plugin manifest has no `rules` field; rules are a memory feature (see `code.claude.com/docs/en/memory#organize-rules-with-claude-rules`). A rule is therefore **not** installed via `/plugin install`. On Claude Code:

1. Copy `src/rules/<name>/rule.md` into `~/.claude/rules/<name>.md` (user scope) or `.claude/rules/<name>.md` (project scope).
2. Claude Code loads `.claude/rules/*.md` automatically at session start.

The generator copies `rule.md` into `_generated/rule-<name>/rules/<name>.md` so the per-platform Cursor/Codex manifests can point at it — but it emits **no** Claude `plugin.json` or `activate.sh` for rules. Contributors editing `src/rules/<name>/rule.md` do not write or maintain install scripts.

For non-Claude-Code platforms (Cursor, Windsurf, Devin), the generator produces auto-committed mirrors:

- `.cursor/rules/<name>.md` — from `src/rules/<name>/formats/cursor.md` (or `src/rules/<name>/rule.md` if there's no `formats/`)
- `.windsurf/rules/<name>.md` — from `src/rules/<name>/formats/windsurf.md` (or `src/rules/<name>/rule.md` if there's no `formats/`)
- `.agents/rules/<name>.md` — raw `rule.md`, forward-looking convergence (per D-12, 2026-05-25). No platform reads `.agents/rules/` today, but Cursor 2.7+ and Windsurf 2.0 are credible adopters.

Devin reads rules from `.cursor/rules/` natively (no separate `.devin/rules/` mirror is emitted).

Users `git clone` the repo and point their tool at the matching directory.

---

## Writing Effective Rules

- **Be concise.** Rules consume context in every session. Keep them focused.
- **Be specific.** "Use pnpm" is better than "use the right package manager."
- **Use NEVER/ALWAYS.** Clear absolutes are easier for agents to follow than nuanced guidelines.
- **List what to check.** Give the agent concrete patterns to scan for.
- **No code execution.** Rules are passive instructions, not scripts. If you need to run code, make it a skill instead.
