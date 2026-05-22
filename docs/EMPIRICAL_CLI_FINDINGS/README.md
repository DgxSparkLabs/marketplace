# Empirical CLI Findings

This directory contains empirical, CI-backed discovery of AI coding assistant CLI surfaces as of May 2026.

**Method:** Each platform has a dedicated GitHub Actions workflow under `.github/workflows/explore-<platform>.yml`.
Commands are run in CI without any API keys or auth. Exit codes, output, and stderr are captured.
Findings are updated after each CI run iteration.

## Platforms

| Platform | CLI Package | Install Method | Auth-free commands found | Status |
|----------|-------------|----------------|--------------------------|--------|
| Codex | `@openai/codex` | npm | TBD | run 1 pending |
| Gemini | `@google/gemini-cli` | npm | TBD | run 1 pending |
| Cursor | unknown | curl / npm? | TBD | run 1 pending |
| Windsurf | unknown | unknown | TBD | run 1 pending |
| Devin | `cli.devin.ai/install.sh` | curl | TBD | run 1 pending |

## Per-platform findings docs

- [codex.md](codex.md)
- [gemini.md](gemini.md)
- [cursor.md](cursor.md)
- [windsurf.md](windsurf.md)
- [devin.md](devin.md)

_This README is updated after each iteration pass._
