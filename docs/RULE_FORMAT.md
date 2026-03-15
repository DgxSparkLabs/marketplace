# Rule Format Reference

Rules are always-on instructions that activate automatically in every agent session. Unlike skills (which must be invoked), rules are loaded at session start and stay active throughout.

This marketplace distributes rules in multiple formats to support different AI agent tools.

---

## Rule Directory Structure

```
my-rule/
├── rule.md             # Required — rule content in plain Markdown (AGENTS.md format)
├── README.md           # Required — documentation with install instructions
├── install.sh          # Required — install script supporting all formats
└── formats/            # Required — tool-specific rule files
    ├── windsurf.md     # Windsurf format (trigger: always_on)
    └── cursor.md       # Cursor format (alwaysApply: true)
```

---

## rule.md (base format)

The `rule.md` file contains the rule content in plain Markdown with no frontmatter. This is the universal format used by `AGENTS.md` and `CLAUDE.md`, which load rules as raw Markdown.

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

## Install Script

Every rule must include an `install.sh` script that handles installation for all supported formats. The script should:

1. Accept `--global` flag for global installation
2. Accept `--format <name>` to install a specific format only
3. Default to installing the `agents` format (AGENTS.md)
4. Be idempotent — check if the rule is already installed before appending
5. Print what was installed and where

Use `no-ai-credit/install.sh` as the reference implementation.

---

## Writing Effective Rules

- **Be concise.** Rules consume context in every session. Keep them focused.
- **Be specific.** "Use pnpm" is better than "use the right package manager."
- **Use NEVER/ALWAYS.** Clear absolutes are easier for agents to follow than nuanced guidelines.
- **List what to check.** Give the agent concrete patterns to scan for.
- **No code execution.** Rules are passive instructions, not scripts. If you need to run code, make it a skill instead.
