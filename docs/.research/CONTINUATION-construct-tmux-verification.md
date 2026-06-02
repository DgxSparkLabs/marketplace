---
date: 2026-06-01
status: live
purpose: continuation prompt — prove every marketplace construct works via live interactive Claude in the container's tmux, the way the LSP was proven
audience: the next session / a cold-start agent
---

# CONTINUATION — Live-tmux verification of all marketplace constructs

> Read this cold and continue. The LSP construct is the finished template; do the same for the rest.

## MISSION
Prove every marketplace construct works end-to-end by driving a **live interactive** Claude CLI inside the
container's tmux (the way the LSP was already proven), observe what the human **sees in the session**, then
document each in `docs/TEST_YOURSELF.md` with: (a) "what you'll see in the session", (b) a verbatim
reproduction (human steps), and (c) any gotchas. Repeat the LSP success pattern for: **command, skill,
sub-agent, hook, mcp, monitor, output-style, theme**.

## WHAT'S ALREADY DONE (the LSP, as the template)
- Built a REAL stdlib language server: `src/lsp-servers/example-multi/example_lsp.py` (Python via `ast` +
  Markdown): diagnostics, documentSymbol, definition, hover, references.
- Added observability: `--always-error` (a guaranteed marker diagnostic on EVERY file) + input logging to
  `${TMPDIR:-/tmp}/example_lsp.log`. Enabled in `lsp-config.json`.
- Fixed a real bug: the server must apply **incremental** `didChange` (keep the buffer), not assume
  full-document — `apply_change()`.
- Demonstrated LIVE in the container tmux (2 panes: Claude | `tail -F` log). The always-on marker appeared
  on a clean file + the input log streamed `initialize`/`didOpen`/`didChange`/`didSave`.
- Fully documented in `docs/TEST_YOURSELF.md` cell **4.8.7**, including a human "▶ Full live walkthrough —
  two-pane tmux" and an "▶ Driving this through tmux as an automated agent — exact mechanics" guide (§0–§9).
  **READ cell 4.8.7's agent guide FIRST — it is the canonical tmux operator reference; do not re-derive it.**

## ENVIRONMENT / SETUP FACTS
- Container name: `qa-claude` (hostname varies, e.g. `0c43182b8b60` — it gets recreated). Find it with
  `docker ps`. Repo is bind-mounted at `/workspace/marketplace`. `HOME=/root`.
- **USE ABSOLUTE PATHS** (a pane's cwd/`$HOME` can differ from a `docker exec bash -lc` shell). Scratch dir:
  `/workspace/lsptest` (`mkdir -p`).
- `uv` is installed (`/root/.local/bin/uv`). `claude` CLI 2.1.159, model Haiku 4.5.
- Install a construct's plugin (from `/workspace/lsptest`):
  `claude plugin install <install-name>@dgxsparklabs-marketplace --scope project`  (auto-enables on 2.1.157+).
- Launch **plain `claude`** (NOT `claude --debug` — it exits immediately headless). Answer the "trust this
  folder" prompt with Enter (`1. Yes`).

## THE PER-CONSTRUCT METHOD
For each construct: (1) install+enable in `/workspace/lsptest`; (2) launch claude in the left tmux pane;
(3) invoke it via the EXACT slash/tool string; (4) capture what shows in the session; (5) write the "what you
see" + reproduction into the matching `TEST_YOURSELF` cell. Exact install names, slash namespaces, and
component names are in cell **1.7** ("Claude construct reference card") and cells **1.8.1–1.8.10**.

| Construct | invoke (exact) | notes |
|---|---|---|
| command (multi) | `/dgxsparklabs-command-example-multi:hello` (also `:goodbye`, `:ping`) | renders a markdown block; easiest, do FIRST |
| skill (multi) | `/dgxsparklabs-skill-example-multi:notebook` (also `:status`); single `:hello` | |
| sub-agent | `/agents` → pick `dgxsparklabs-agent-example-multi:notebook-reviewer` (`:summarizer`, `:validator`) | INTERACTIVE/TUI-only |
| hook | `hook-example-multi` (9 events) → sentinels `/tmp/hook-fired-<event>.log` | trigger by editing a file / new session |
| mcp | `mcp-example-multi` (servers `fetch`/`filesystem`/`sequential-thinking`) | needs uv/uvx; `/mcp` TUI-only; tool is model-called |
| monitor | `monitor-example-multi` (`disk-usage`/`memory-usage`/`git-status`) | runs at session start |
| output-style | `/output-style "Lab Notebook Voice"` (also `Concise Engineer`, `Tutoring`) | TUI-only |
| theme | `/theme "Lab Notebook"` (also `Nord`, `Solarized Dark`) | TUI-only, visual |

## KEY LEARNINGS TO CARRY (verify via real signals, not the model's prose)
- A capable model **describes** behavior even when the construct didn't fire — a chat reply is NOT proof.
  Find the construct's real signal (a rendered slash output, a sentinel file, a settings.json change, a debug
  line).
- `/agents`, `/mcp`, `/output-style`, `/theme` are interactive-TUI-only (error under `--print`).
- Namespace model: per-plugin slash namespace = `plugin.json` `name` = `dgxsparklabs-<install-name>` (NOT a
  shared namespace — "Path A" was reverted).
- Install auto-enables (CLI ≥2.1.157); enablement is cwd/project-scoped.
- Diagnostics/attachments can land **one turn late** (true for LSP; watch for similar async surfacing).

## DOC CONVENTIONS (must follow)
- `TEST_YOURSELF.md` uses PURE NUMERIC numbering (`1`, `1.1`, `1.1.1` — no letters).
- Links are Obsidian-style (encode only space/paren; never put `:` in a heading). See `VAULT-RULES.md` +
  `PITFALLS.md`.
- EVERY tester action must be a VERBATIM copy-paste prompt/command — no "ask Claude to…" improvisation (the
  prompt must be explicit enough that Haiku just does it, with no clarifying question).
- After ANY source change: `uv run scripts/generate_manifest.py`, then `uv run tests/test_marketplace.py` +
  `tests/test_schema_fitness.py` + `--check` (drift).
- New gotchas → `PITFALLS.md`.

## FLAGS / DO NOT TOUCH
- Branch: `chore/housekeeping-and-roadmap`. The LSP work + these doc additions are **UNCOMMITTED**. Do not
  commit without the user's explicit go + branch choice.
- `git status` shows STRAY non-LSP modified files NOT from this work — `CHANGELOG.md`, `scripts/utils.py`,
  `src/MARKETPLACE.toml`, `docs/archive/.../IMPLEMENTATION_PLAN.md`, `docs/research/.../RESEARCH.md`,
  `docs/.research/`. **DO NOT sweep these into a commit; ask first.**
- Task-list items #9–12 ("gist") are leaked from another context — ignore.

## FIRST STEPS
1. Read `docs/TEST_YOURSELF.md` cell 4.8.7 (agent tmux guide) + cell 1.7 (reference card).
2. Confirm container: `docker ps`; `docker exec qa-claude tmux ls`; `tmux list-panes -t 0:0 -F …`.
3. Start with **command** (easiest, visible slash output): install `command-example-multi`, launch claude in
   `/workspace/lsptest`, run `/dgxsparklabs-command-example-multi:hello`, capture the rendered output,
   document "what you see" + reproduction in cell **1.8.4**.
4. Proceed through the other constructs; document each; keep tests/drift green.
