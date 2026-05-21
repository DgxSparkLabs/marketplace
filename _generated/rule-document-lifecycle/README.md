# document-lifecycle

Three-tier documentation: rules, reference, history — no sprawl

## Install

```bash
# Project-level (current directory)
document-lifecycle/install.sh

# Global (all projects)
document-lifecycle/install.sh --global

# Specific format
document-lifecycle/install.sh --format windsurf
document-lifecycle/install.sh --format cursor
```

## What it does

Enforces a strict three-tier documentation structure — rules in AGENTS.md, current state in HANDOFF.md, history in CHANGELOG.md — eliminating doc sprawl, duplication, and staleness.

## See also

- [blast-radius](../blast-radius/) — estimate change scope before coding
- [verify-your-work](../verify-your-work/) — prove correctness, don't assume it
