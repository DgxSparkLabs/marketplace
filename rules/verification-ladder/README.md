# verification-ladder

Five-layer automated testing: compile, unit, integration, perf, e2e

## Install

```bash
# Project-level (current directory)
verification-ladder/install.sh

# Global (all projects)
verification-ladder/install.sh --global

# Specific format
verification-ladder/install.sh --format windsurf
verification-ladder/install.sh --format cursor
```

## What it does

Establishes a five-layer automated verification strategy — from compile-time warnings through end-to-end smoke tests — ensuring test infrastructure is built before feature code.

## See also

- [blast-radius](../blast-radius/) — estimate change scope before coding
- [verify-your-work](../verify-your-work/) — prove correctness, don't assume it
