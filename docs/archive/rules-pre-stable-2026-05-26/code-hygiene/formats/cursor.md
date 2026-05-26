---
description: "Enforce DRY, single-responsibility, centralized definitions, and human-readable naming"
alwaysApply: true
---
## Code Hygiene

Write code a human can maintain without an AI agent.

- **Search before defining.** Before creating any type, constant, enum, or utility, grep the codebase. Import if found. Refactor to generalize if similar.
- **Centralize definitions and paths.** Types, constants, config shapes, enums, and directory paths live in dedicated files — never inline, never duplicated. One source of truth per concept. Moving a directory should require editing one line.
- **One file, one job.** Each module has a single responsibility. If describing it requires "and," split it. Target ~300 lines max per file.
- **Name for humans.** No `utils`, `helpers`, `misc`, `processData()`. Every file, function, and variable describes its purpose without reading the implementation.
- **Refactor alongside.** When touching code, consolidate nearby duplication in the same change — not as a future task. Delete dead code on sight.
- **Config over code.** If a non-developer needs to change it (data registries, feature toggles, resource lists), it belongs in a config file, not in source code. Derive behavior from existing data structures rather than maintaining parallel mappings.
- **Complete every migration.** Partial reorganizations are worse than none — leftover files look like mistakes. If you organize some files, organize all of them.
- **Maintain `CODEBASE.md`.** Document module boundaries, shared type locations, directory purposes, and key abstractions. Update when architecture changes.
- **Structure directories.** Source in `src/`, documentation in `docs/`, scripts in `scripts/`, configuration in `config/`. Adapt to language conventions.
