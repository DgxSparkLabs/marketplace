---
date: 2026-05-25
purpose: hands-on QA verification of all 6 supported platforms + the `agents` CLI, per construct × per platform
audience: operator-qa
status: live
---

# Test Yourself — Platform QA Walkthrough

A step-by-step verification guide for an operator to confirm the DgxSparkLabs marketplace works end-to-end on each of the six supported platforms plus the cross-platform `agents` CLI. Each section is independent — work through all of them, or pick the platforms you actually use.

> **2026-05-30 single/multi scope (updated for `cd7a7d8`).** *Every* Claude-supported construct now ships a **`-single`** (solo: the simplest possible plugin of that type) and a **`-multi`** (several components in one plugin) reference plugin, and all source dirs moved under **`src/`**. Hooks ship as **9 per-event plugins + 1 `-multi`**. Marketplace total: **27** entries (26 individuals + `bundle-examples`). The Claude reference card and cells below cover both layouts; empirically captured 2026-05-30 (CLI 2.1.157) — examples:
>
> - `/dgxsparklabs-skill-example-multi:notebook` · `:status` — two skills in the multi-skill plugin (`src/skills/example-multi/`)
> - `/dgxsparklabs-skill-example-single:hello` — the only skill in the solo plugin (`src/skills/example-single/`)
> - `/dgxsparklabs-command-example-multi:hello` · `:goodbye` · `:ping` — three commands in one plugin
>
> Non-Claude per-construct cells (Cursor IDE/CLI, Codex, Gemini, Windsurf, Devin, `.agents/` shim) are still written for the solo layout only and have **not** been re-cascaded for the `cd7a7d8` single/multi expansion or the `src/` move — treat those sections as stale pending ROADMAP #37-#42.

This is a hand-holding document. If something below looks obvious, that's intentional — the goal is that someone who has never touched these tools can follow it without guessing.

**Round-2 expansion (2026-05-25)**: this revision was expanded from "a handful of exemplary cells" to **a full construct × platform grid**. Every construct type that a platform supports is exercised by a hands-on test. The 🐛 / ✅ callouts from the 2026-05-25 QA pass are preserved.

---

## Outline — jump to any test

Sections are numbered sequentially: `N` is a part, `N.M` a subsection, `N.M.K` one specific test. **Track progress** by the deepest number you've finished (e.g. "done through **4.8.6**"). Links are Obsidian-style (they jump in Obsidian; on GitHub they render but do not navigate).

- [1. How to use this guide](#1.%20How%20to%20use%20this%20guide)
- [2. Master verification matrix](#2.%20Master%20verification%20matrix)
- [3. Prerequisites (one-time host setup)](#3.%20Prerequisites%20%28one-time%20host%20setup%29)
  - [3.1 Docker Desktop (required for hermetic path)](#3.1%20Docker%20Desktop%20%28required%20for%20hermetic%20path%29)
  - [3.2 Node.js 18+ (required for Claude / Codex / Gemini CLIs)](#3.2%20Node.js%2018+%20%28required%20for%20Claude%20/%20Codex%20/%20Gemini%20CLIs%29)
  - [3.3 WSL or Git Bash (only needed for Devin native install)](#3.3%20WSL%20or%20Git%20Bash%20%28only%20needed%20for%20Devin%20native%20install%29)
  - [3.4 Docker hermetic-session primer](#3.4%20Docker%20hermetic-session%20primer)
  - [3.5 Three install sources — choose remote-main, remote-branch, or local-clone](#3.5%20Three%20install%20sources%20—%20choose%20remote-main,%20remote-branch,%20or%20local-clone)
  - [3.6 Repository state](#3.6%20Repository%20state)
  - [3.7 Example plugins used as canonical test items](#3.7%20Example%20plugins%20used%20as%20canonical%20test%20items)
- [4. Claude Code](#4.%20Claude%20Code)
  - [4.1 Setup option A — Dev Container (recommended)](#4.1%20Setup%20option%20A%20—%20Dev%20Container%20%28recommended%29)
  - [4.2 Setup option B — Docker (manual, hermetic)](#4.2%20Setup%20option%20B%20—%20Docker%20%28manual,%20hermetic%29)
  - [4.3 Setup option C — Native](#4.3%20Setup%20option%20C%20—%20Native)
  - [4.4 Auth](#4.4%20Auth)
  - [4.5 Hermetic Claude session (no auth required)](#4.5%20Hermetic%20Claude%20session%20%28no%20auth%20required%29)
  - [4.6 Marketplace registration](#4.6%20Marketplace%20registration)
  - [4.7 Claude construct reference card — exact strings to type and expect](#4.7%20Claude%20construct%20reference%20card%20—%20exact%20strings%20to%20type%20and%20expect)
  - [4.8 Per-construct verification](#4.8%20Per-construct%20verification)
    - [4.8.0 Day-to-day usage and the rookie operator guide](#4.8.0%20Day-to-day%20usage%20and%20the%20rookie%20operator%20guide)
      - [4.8.0.1 Rookie operator guide — set up the container and run every construct test through tmux](#4.8.0.1%20Rookie%20operator%20guide%20—%20set%20up%20the%20container%20and%20run%20every%20construct%20test%20through%20tmux)
    - [4.8.1 Skill — `skill-example-multi`](#4.8.1%20Skill%20—%20`skill-example-multi`)
    - [4.8.2 Rule — N/A for Claude (retired 2026-05-26)](#4.8.2%20Rule%20—%20N/A%20for%20Claude%20%28retired%202026-05-26%29)
    - [4.8.3 Sub-agent — `agent-example-multi`](#4.8.3%20Sub-agent%20—%20`agent-example-multi`)
    - [4.8.4 Command — `command-example-multi`](#4.8.4%20Command%20—%20`command-example-multi`)
    - [4.8.5 Hook — `hook-example-multi`](#4.8.5%20Hook%20—%20`hook-example-multi`)
    - [4.8.6 MCP server — `mcp-example-multi`](#4.8.6%20MCP%20server%20—%20`mcp-example-multi`)
    - [4.8.7 LSP server — `lsp-example-multi`](#4.8.7%20LSP%20server%20—%20`lsp-example-multi`)
    - [4.8.8 Monitor — `monitor-example-multi`](#4.8.8%20Monitor%20—%20`monitor-example-multi`)
    - [4.8.9 Output style — `output-style-example-multi`](#4.8.9%20Output%20style%20—%20`output-style-example-multi`)
    - [4.8.10 Theme — `theme-example-multi`](#4.8.10%20Theme%20—%20`theme-example-multi`)
  - [4.9 Headless and hermetic alternative path (no-auth validations and the original refactor arcs)](#4.9%20Headless%20and%20hermetic%20alternative%20path%20%28no-auth%20validations%20and%20the%20original%20refactor%20arcs%29)
    - [4.9.1 Claude validation 1 — marketplace description (F1)](#4.9.1%20Claude%20validation%201%20—%20marketplace%20description%20%28F1%29)
    - [4.9.2 Claude validation 2 — lsp-example schema (F2)](#4.9.2%20Claude%20validation%202%20—%20lsp-example%20schema%20%28F2%29)
    - [4.9.3 Claude validation 3 — monitor-example shape (F3)](#4.9.3%20Claude%20validation%203%20—%20monitor-example%20shape%20%28F3%29)
    - [4.9.4 Claude validation 4 — theme-example distinctiveness (F4)](#4.9.4%20Claude%20validation%204%20—%20theme-example%20distinctiveness%20%28F4%29)
    - [4.9.5 Claude validation 5a — UserPromptSubmit hook firing (F5)](#4.9.5%20Claude%20validation%205a%20—%20UserPromptSubmit%20hook%20firing%20%28F5%29)
    - [4.9.6 Claude validation 5b — SessionStart hook firing (F5)](#4.9.6%20Claude%20validation%205b%20—%20SessionStart%20hook%20firing%20%28F5%29)
    - [4.9.7 Claude validation 5c — PreToolUse hook with matcher (F5)](#4.9.7%20Claude%20validation%205c%20—%20PreToolUse%20hook%20with%20matcher%20%28F5%29)
    - [4.9.8 Claude validation 5d — PostToolUse hook firing (F5)](#4.9.8%20Claude%20validation%205d%20—%20PostToolUse%20hook%20firing%20%28F5%29)
    - [4.9.9 Claude validation 5e — Stop hook firing (F5)](#4.9.9%20Claude%20validation%205e%20—%20Stop%20hook%20firing%20%28F5%29)
    - [4.9.10 Claude validation 5f — SessionEnd hook firing (F5)](#4.9.10%20Claude%20validation%205f%20—%20SessionEnd%20hook%20firing%20%28F5%29)
    - [4.9.11 Claude validation 6 — mcp-example uv prerequisite (F6)](#4.9.11%20Claude%20validation%206%20—%20mcp-example%20uv%20prerequisite%20%28F6%29)
    - [4.9.12 Claude validation 7a — skill slash command namespacing (F7)](#4.9.12%20Claude%20validation%207a%20—%20skill%20slash%20command%20namespacing%20%28F7%29)
    - [4.9.13 Claude validation 7b — agent namespacing (F7)](#4.9.13%20Claude%20validation%207b%20—%20agent%20namespacing%20%28F7%29)
    - [4.9.14 Claude validation 7c — MCP tool namespacing (F7)](#4.9.14%20Claude%20validation%207c%20—%20MCP%20tool%20namespacing%20%28F7%29)
    - [4.9.15 Claude validation 8 — rule deprecation (F8)](#4.9.15%20Claude%20validation%208%20—%20rule%20deprecation%20%28F8%29)
    - [4.9.16 Claude validation 9 — output style applied (F9)](#4.9.16%20Claude%20validation%209%20—%20output%20style%20applied%20%28F9%29)
  - [4.10 Cleanup](#4.10%20Cleanup)
- [5. Codex](#5.%20Codex)
  - [5.1 Setup option A — Docker (hermetic)](#5.1%20Setup%20option%20A%20—%20Docker%20%28hermetic%29)
  - [5.2 Setup option B — Native](#5.2%20Setup%20option%20B%20—%20Native)
  - [5.3 Auth](#5.3%20Auth)
  - [5.4 Marketplace registration](#5.4%20Marketplace%20registration)
  - [5.5 Per-construct verification](#5.5%20Per-construct%20verification)
    - [5.5.1 Skill — `skill-example`](#5.5.1%20Skill%20—%20`skill-example`)
    - [5.5.2 Sub-agent — `agent-example`](#5.5.2%20Sub-agent%20—%20`agent-example`)
    - [5.5.3 Hook — `hook-example`](#5.5.3%20Hook%20—%20`hook-example`)
    - [5.5.4 MCP server — `mcp-example`](#5.5.4%20MCP%20server%20—%20`mcp-example`)
    - [5.5.5 Rule (no native install, file-discovery only) — `rule-example`](#5.5.5%20Rule%20%28no%20native%20install,%20file-discovery%20only%29%20—%20`rule-example`)
  - [5.6 Specifically for THIS refactor](#5.6%20Specifically%20for%20THIS%20refactor)
  - [5.7 Cleanup](#5.7%20Cleanup)
- [6. Gemini](#6.%20Gemini)
  - [6.1 Setup option A — Docker (hermetic)](#6.1%20Setup%20option%20A%20—%20Docker%20%28hermetic%29)
  - [6.2 Setup option B — Native](#6.2%20Setup%20option%20B%20—%20Native)
  - [6.3 Auth](#6.3%20Auth)
  - [6.4 Extension install](#6.4%20Extension%20install)
  - [6.5 Per-construct verification](#6.5%20Per-construct%20verification)
    - [6.5.1 Skill — `skill-example`](#6.5.1%20Skill%20—%20`skill-example`)
    - [6.5.2 Sub-agent — `agent-example`](#6.5.2%20Sub-agent%20—%20`agent-example`)
    - [6.5.3 Hook — `hook-example`](#6.5.3%20Hook%20—%20`hook-example`)
  - [6.6 Specifically for THIS refactor](#6.6%20Specifically%20for%20THIS%20refactor)
  - [6.7 Cleanup](#6.7%20Cleanup)
- [7. Cursor (IDE + CLI)](#7.%20Cursor%20%28IDE%20+%20CLI%29)
  - [7.1 Cursor IDE](#7.1%20Cursor%20IDE)
    - [7.1.1 Marketplace registration paths](#7.1.1%20Marketplace%20registration%20paths)
    - [7.1.2 Per-construct verification (IDE)](#7.1.2%20Per-construct%20verification%20%28IDE%29)
  - [7.2 Cursor CLI (`agent` binary)](#7.2%20Cursor%20CLI%20%28`agent`%20binary%29)
    - [7.2.1 Setup](#7.2.1%20Setup)
    - [7.2.2 Per-construct verification (CLI)](#7.2.2%20Per-construct%20verification%20%28CLI%29)
  - [7.3 Specifically for THIS refactor](#7.3%20Specifically%20for%20THIS%20refactor)
  - [7.4 Cleanup](#7.4%20Cleanup)
- [8. Windsurf](#8.%20Windsurf)
  - [8.1 Setup](#8.1%20Setup)
  - [8.2 Populating the workspace](#8.2%20Populating%20the%20workspace)
  - [8.3 Per-construct verification](#8.3%20Per-construct%20verification)
    - [8.3.1 Skill — `skill-example` (read via `.agents/skills/`)](#8.3.1%20Skill%20—%20`skill-example`%20%28read%20via%20`.agents/skills/`%29)
    - [8.3.2 Rule — `rule-example`](#8.3.2%20Rule%20—%20`rule-example`)
    - [8.3.3 Hook — `hook-example`](#8.3.3%20Hook%20—%20`hook-example`)
  - [8.4 Specifically for THIS refactor](#8.4%20Specifically%20for%20THIS%20refactor)
  - [8.5 Cleanup](#8.5%20Cleanup)
- [9. Devin](#9.%20Devin)
  - [9.1 Setup option A — Docker (hermetic)](#9.1%20Setup%20option%20A%20—%20Docker%20%28hermetic%29)
  - [9.2 Setup option B — Native (WSL or Git Bash)](#9.2%20Setup%20option%20B%20—%20Native%20%28WSL%20or%20Git%20Bash%29)
  - [9.3 Auth](#9.3%20Auth)
  - [9.4 Populating the workspace](#9.4%20Populating%20the%20workspace)
  - [9.5 Per-construct verification](#9.5%20Per-construct%20verification)
    - [9.5.1 Skill — `skill-example` (read via `.agents/skills/`)](#9.5.1%20Skill%20—%20`skill-example`%20%28read%20via%20`.agents/skills/`%29)
    - [9.5.2 Rule — `rule-example` (read via `.windsurf/rules/`, `.cursor/rules/`)](#9.5.2%20Rule%20—%20`rule-example`%20%28read%20via%20`.windsurf/rules/`,%20`.cursor/rules/`%29)
    - [9.5.3 MCP — Devin-managed (no marketplace-emitted Devin MCP config)](#9.5.3%20MCP%20—%20Devin-managed%20%28no%20marketplace-emitted%20Devin%20MCP%20config%29)
  - [9.6 Specifically for THIS refactor](#9.6%20Specifically%20for%20THIS%20refactor)
  - [9.7 Cleanup](#9.7%20Cleanup)
- [10. `agents` CLI (the new cross-platform shim)](#10.%20`agents`%20CLI%20%28the%20new%20cross-platform%20shim%29)
  - [10.1 Setup option A — Docker (hermetic)](#10.1%20Setup%20option%20A%20—%20Docker%20%28hermetic%29)
  - [10.2 Setup option B — Native (Windows PowerShell)](#10.2%20Setup%20option%20B%20—%20Native%20%28Windows%20PowerShell%29)
  - [10.3 Auth](#10.3%20Auth)
  - [10.4 CLI surface verification](#10.4%20CLI%20surface%20verification)
  - [10.5 Per-construct install verification](#10.5%20Per-construct%20install%20verification)
    - [10.5.1 Skill — `skill-example`](#10.5.1%20Skill%20—%20`skill-example`)
    - [10.5.2 Rule — `rule-example`](#10.5.2%20Rule%20—%20`rule-example`)
    - [10.5.3 Sub-agent — `agent-example`](#10.5.3%20Sub-agent%20—%20`agent-example`)
    - [10.5.4 Command — `command-example`](#10.5.4%20Command%20—%20`command-example`)
    - [10.5.5 Hook — `hook-example`](#10.5.5%20Hook%20—%20`hook-example`)
    - [10.5.6 MCP — `mcp-example`](#10.5.6%20MCP%20—%20`mcp-example`)
    - [10.5.7 LSP — `lsp-example` (forward-looking)](#10.5.7%20LSP%20—%20`lsp-example`%20%28forward-looking%29)
    - [10.5.8 Monitor — `monitor-example` (forward-looking)](#10.5.8%20Monitor%20—%20`monitor-example`%20%28forward-looking%29)
    - [10.5.9 Output style — `output-style-example` (forward-looking)](#10.5.9%20Output%20style%20—%20`output-style-example`%20%28forward-looking%29)
    - [10.5.10 Theme — `theme-example` (forward-looking)](#10.5.10%20Theme%20—%20`theme-example`%20%28forward-looking%29)
  - [10.6 Scope and flag verification](#10.6%20Scope%20and%20flag%20verification)
    - [10.6.1 `--scope user` (writes to `~/.agents/` only per D-6)](#10.6.1%20`--scope%20user`%20%28writes%20to%20`~/.agents/`%20only%20per%20D-6%29)
    - [10.6.2 `--scope user` + `--agents-only` for sub-agent](#10.6.2%20`--scope%20user`%20+%20`--agents-only`%20for%20sub-agent)
    - [10.6.3 `agents list` (installed, not available)](#10.6.3%20`agents%20list`%20%28installed,%20not%20available%29)
    - [10.6.4 `agents uninstall` cleans both per-platform AND `.agents/` paths](#10.6.4%20`agents%20uninstall`%20cleans%20both%20per-platform%20AND%20`.agents/`%20paths)
  - [10.7 Specifically for THIS refactor](#10.7%20Specifically%20for%20THIS%20refactor)
  - [10.8 Cleanup](#10.8%20Cleanup)
- [11. Master teardown](#11.%20Master%20teardown)
- [12. Reporting findings](#12.%20Reporting%20findings)
- [13. Quick reference table](#13.%20Quick%20reference%20table)
- [14. Known issues surfaced by QA (2026-05-25)](#14.%20Known%20issues%20surfaced%20by%20QA%20%282026-05-25%29)
  - [14.1 🐛 Codex sub-agents not discovered](#14.1%20🐛%20Codex%20sub-agents%20not%20discovered)
  - [14.2 🐛 Gemini sub-agents not discovered](#14.2%20🐛%20Gemini%20sub-agents%20not%20discovered)
  - [14.3 🐛 Cursor skill popup mangled metadata](#14.3%20🐛%20Cursor%20skill%20popup%20mangled%20metadata)
  - [14.4 ✅ Cursor sub-agent (positive finding)](#14.4%20✅%20Cursor%20sub-agent%20%28positive%20finding%29)
  - [14.5 Documentation/process improvements adopted in this doc revision](#14.5%20Documentation/process%20improvements%20adopted%20in%20this%20doc%20revision)
- [15. Discrepancies and unknowns flagged during doc expansion](#15.%20Discrepancies%20and%20unknowns%20flagged%20during%20doc%20expansion)
  - [15.1 Discrepancies between source documents](#15.1%20Discrepancies%20between%20source%20documents)
  - [15.2 Unknown verification methods (gaps for the next research round)](#15.2%20Unknown%20verification%20methods%20%28gaps%20for%20the%20next%20research%20round%29)

## 1. How to use this guide

Each platform section has the same shape:

1. **What we're verifying** — one-paragraph statement of intent
2. **Setup option A: Docker (hermetic)** — for clean, throwaway testing
3. **Setup option B: Native (your machine)** — if you already use the tool
4. **Auth (if needed)** — flagged clearly so you know when login is required
5. **Per-construct verification** — one hands-on test per construct the platform supports
6. **Specifically for THIS refactor** — what's NEW in 2026-05 that's worth testing harder
7. **Cleanup** — return to a clean state, no artifacts left behind

Check off `[ ]` boxes as you go. Anything that deviates from "Expected" is something to report back.

> **Hands-on, not file-existence.** Every test step asks the operator to run a command and observe a behavior — invoke a skill, dispatch a sub-agent, fire a hook, list installed plugins. File-existence checks (`ls`, `cat`, `test -f`) may appear as a DIAGNOSTIC step AFTER a hands-on test fails, never as the primary verification. A file on disk that no platform consumes is a stranded artifact, not a working integration.

---

## 2. Master verification matrix

This matrix is the index. Each cell tells you what to expect in the per-platform sections below.

- **TEST** — the platform emits and consumes this construct; QA covers it with a hands-on test in this doc.
- **TEST¹/TEST²/etc.** — TEST with a footnote (caveat, known bug, or pending QA).
- **N/A** — the platform doesn't support this construct (per its `supports` set in `scripts/platforms.py` and the per-platform "What constructs it supports" tables in `docs/PLATFORMS.md`).
- **CLAUDE-ONLY** — for lsp / monitor / output-style / theme, only Claude consumes these constructs; other platforms have no concept and no test path.

|                 | Claude  | Codex   | Gemini  | Cursor IDE | Cursor CLI | Windsurf | Devin   | `agents` CLI |
|---              |---      |---      |---      |---         |---         |---       |---      |---           |
| skill           | TEST    | TEST    | TEST    | TEST¹      | TEST²      | TEST     | TEST    | TEST         |
| rule            | N/A³    | N/A⁴    | N/A⁵    | TEST       | TEST²      | TEST     | TEST⁶   | TEST         |
| agent           | TEST    | TEST⁷   | TEST⁸   | TEST ✅⁹   | TEST²      | N/A      | N/A     | TEST         |
| command         | TEST    | N/A     | N/A¹⁰   | TEST¹¹     | TEST²      | N/A      | N/A     | TEST¹²       |
| hook            | TEST    | TEST    | TEST¹³  | TEST¹¹     | TEST²      | TEST¹⁴   | N/A     | TEST         |
| mcp             | TEST    | TEST    | N/A¹⁵   | TEST¹¹     | TEST²      | N/A      | TEST¹⁶  | TEST         |
| lsp             | TEST    | CLAUDE-ONLY | CLAUDE-ONLY | CLAUDE-ONLY | CLAUDE-ONLY | CLAUDE-ONLY | CLAUDE-ONLY | TEST¹²    |
| monitor         | TEST    | CLAUDE-ONLY | CLAUDE-ONLY | CLAUDE-ONLY | CLAUDE-ONLY | CLAUDE-ONLY | CLAUDE-ONLY | TEST¹²    |
| output-style    | TEST    | CLAUDE-ONLY | CLAUDE-ONLY | CLAUDE-ONLY | CLAUDE-ONLY | CLAUDE-ONLY | CLAUDE-ONLY | TEST¹²    |
| theme           | TEST    | CLAUDE-ONLY | CLAUDE-ONLY | CLAUDE-ONLY | CLAUDE-ONLY | CLAUDE-ONLY | CLAUDE-ONLY | TEST¹²    |

**Footnotes**:

1. Cursor IDE skill popup is **🐛 KNOWN BUG (2026-05-25 QA)** — install works, but the popup's metadata fields are mangled. See the bug callout in the Cursor section. Per `docs/PLATFORMS.md` Cursor section, skill discovery uses `.agents/skills/` (the cross-platform convergence path).
2. Cursor CLI (`agent` binary) has **no plugin install commands** per `docs/PLATFORMS.md` Cursor section. The CLI reads from `.agents/skills/`, `.cursor/rules/`, `.cursor/agents/`, and `.cursor-plugin/plugin.json` pointers natively — populate those by running the `agents` CLI (cross-platform) and verify the Cursor CLI sees them. Hands-on test path is "install via `agents` CLI → open repo with `agent` → ask CLI to use construct".
3. **Rules are NOT a Claude plugin component** as of 2026-05-26 (per `code.claude.com/docs/en/plugins-reference#plugin-components-reference`, fetched 2026-05-26). Claude consumes rules via its memory subsystem at `.claude/rules/*.md` (project) and `~/.claude/rules/*.md` (user). `RuleConstruct` has been removed from `ClaudeCodePlatform.supports`; no `rule-<name>` plugins are surfaced to Claude. To use a rule with Claude, symlink or copy `rules/<name>/rule.md` into `.claude/rules/<name>.md`. See `docs/USER_GUIDE.md` Claude section + the new Claude validation 8 below for the post-deprecation check.
4. Per `docs/PLATFORMS.md` Codex "What constructs it supports": Codex reads rules from `AGENTS.md`, `.cursor/rules/*.md`, `.windsurf/rules/*.md` directly — no separate Codex rule install. **Verification method: open Codex in the marketplace clone and confirm rule context is reflected in behavior.**
5. Per `docs/PLATFORMS.md` Gemini "What constructs it supports": rule context comes from `GEMINI.md` and `AGENTS.md`, not a Gemini-native rule install.
6. Devin reads rules from `.cursor/rules/`, `.windsurf/rules/`, `.cursorrules`, and `AGENTS.md` per `devin rules paths` (per `docs/PLATFORMS.md` Devin section). Verification is via `devin rules list`.
7. Codex sub-agents — **🐛 KNOWN BUG (2026-05-25 QA)**: `.codex/agents/<name>.toml` is emitted but Codex's sub-agent loader doesn't surface our sub-agent. See bug callout in Codex section.
8. Gemini sub-agents — **🐛 KNOWN BUG (2026-05-25 QA)**: `.gemini/agents/<name>.md` is emitted but Gemini's agent loader doesn't surface our sub-agent. See bug callout in Gemini section.
9. Cursor IDE sub-agent — **✅ KNOWN GOOD (2026-05-25 QA)**: `/notebook-reviewer` dropdown displays correctly. See positive-finding callout in Cursor section.
10. Per `docs/PLATFORMS.md` Gemini section, Gemini commands exist natively as TOML but we do not emit them today (deferred, per round-2 capabilities scan U6). Marked N/A here.
11. Per `docs/PLATFORMS.md` Cursor "What constructs it supports" table: Cursor commands / hooks / MCP are "manifest-only" — surfaced via per-plugin `.cursor-plugin/plugin.json` pointer fields, auto-discovered. **Verification method UNKNOWN for command/hook/MCP enumeration commands inside Cursor — see follow-up.**
12. The `agents` CLI surface is the cross-platform shim — `agents install <name>` should land at `.agents/<type>/<name>/` (project) or `~/.agents/<type>/<name>/` (user). For construct types that no platform reads from `.agents/<type>/` natively (per `docs/research/platform-feature-routing/RECOMMENDATION.md` adoption matrix), the test is "the CLI emits to the right path" — downstream consumption is a forward-looking property.
13. Gemini hooks emit at `.gemini/hooks/hooks.json`. **Verification method UNKNOWN** — Gemini has no documented hooks-list command. Best signal today is file presence + valid JSON. See follow-up.
14. Windsurf hooks emit at `.windsurf/hooks.json`. **Verification method UNKNOWN** — Windsurf has no CLI; hook invocation depends on triggering Cascade events. See follow-up.
15. Per `docs/PLATFORMS.md` Gemini section, Gemini's MCP support is CLI-managed via `gemini mcp add`, not extension-installed. Not in our emission scope.
16. Devin MCP — `devin mcp list`/`get`/`add` are CLI-managed (per `docs/PLATFORMS.md` Devin "Discovery commands"). Marketplace currently does not emit a Devin-native MCP config; verification is "Devin's MCP surface works alongside our marketplace install".

**TEST cell count**: 53 hands-on test cells across the grid (vs 4-5 in the prior revision). N/A and CLAUDE-ONLY cells are skipped intentionally.

**Construct support sources**:
- `scripts/platforms.py` — each Platform class's `supports` set is the ground truth.
- `docs/PLATFORMS.md` per-platform "What constructs it supports" tables — the readable cross-reference.
- `docs/ARCHITECTURE.md` "The seven platform classes" — the architecture-level overview.

---

## 3. Prerequisites (one-time host setup)

### 3.1 Docker Desktop (required for hermetic path)

```powershell
# Windows
winget install Docker.DockerDesktop
# Then launch Docker Desktop from Start Menu and let it finish first-run setup
docker --version
docker run --rm hello-world      # should print "Hello from Docker!"
```

If you'd rather skip Docker and test natively for everything, that's fine — just use Setup option B in each section.

### 3.2 Node.js 18+ (required for Claude / Codex / Gemini CLIs)

```powershell
winget install OpenJS.NodeJS.LTS
node --version       # expected: v18.x or higher
npm --version
```

### 3.3 WSL or Git Bash (only needed for Devin native install)

If you don't already have WSL:

```powershell
wsl --install
# Reboot when prompted
```

Otherwise, Git Bash from `git-scm.com` works for Devin's installer too.

### 3.4 Docker hermetic-session primer

Every hermetic section in this doc uses one of two patterns:

**One-shot** (no persistence, auto-clean):
```powershell
docker run --rm -it IMAGE bash -c "your-commands-here"
```

**Multi-step** (you want to interact inside the container):
```powershell
docker run -it --name qa-test IMAGE bash
# ... do stuff inside ...
exit
docker rm -f qa-test         # explicit cleanup
```

The `--rm` flag in the one-shot form auto-removes the container when the command exits. The multi-step form requires manual `docker rm -f`. The final "Master teardown" section at the bottom lists every container name we use, so you can clean them up in one sweep.

### 3.5 Three install sources — choose remote-main, remote-branch, or local-clone

This doc was originally written assuming "install from `DgxSparkLabs/marketplace` on default branch." That works fine for smoke-testing the released marketplace, but it is **useless for pre-merge PR verification** — `main` doesn't yet have the fixes a still-open PR introduces. To make this guide usable for testing in-flight PRs, every per-platform section documents THREE install sources where the platform supports them.

| Mode | What it tests | When to use |
|---|---|---|
| Remote `main` | The state of `main` on GitHub | Smoke-test of released marketplace |
| Remote branch ref | A specific branch on GitHub (e.g., `main`) | Pre-merge PR verification — needs the platform's `--ref` flag |
| Local clone | The exact bytes in your working tree | Most reliable for unmerged PRs, hands-on debugging |

Platform-by-platform support:

| Platform | Remote main | Remote `--ref <branch>` | Local clone |
|---|:--:|:--:|:--:|
| Claude Code | ✅ | partial† | ✅ |
| Codex | ✅ | ✅ | ✅ |
| Gemini | ✅ | ✅ | ✅ |
| Cursor IDE | ✅ (Dashboard / `/add-plugin`) | partial (Dashboard supports branch; `/add-plugin` form untested) | ✅ (open local dir in editor) |
| Cursor CLI | n/a — no plugin install | n/a | ✅ (reads workspace files) |
| Windsurf | n/a — no CLI | n/a | ✅ (clone + open in IDE) |
| Devin | n/a — no marketplace | n/a | ✅ (clone + `devin skills list`) |
| `agents` CLI | ✅ via curl/irm one-liner | ✅ via `AGENTS_REF` env var | ✅ (`bash install.sh` from local checkout) |

**Legend**:
- ✅ — verified working in this repo's evidence (act/CI logs or per-platform reference docs).
- **partial** — the platform has SOME branch-ref capability but it's either undocumented (Cursor `/add-plugin`) or absent from the CLI surface (Claude — clone-first is the workaround).
- **n/a** — the platform has no marketplace registration step at all; it reads from the workspace filesystem, so "branch selection" is "which branch you cloned."

**Canonical example branch throughout this doc**: `main`. Where you see that branch ref below, substitute your PR's branch when testing an in-flight change.

**Docker setup pattern when testing a PR branch**: every per-platform Docker setup below clones `main` into `/workspace/marketplace` inside the container by default; pass `--branch <pr-branch>` to `git clone` to test a specific PR.

> **Per-platform PR references**: many cells below still reference "PR #5" as the canonical example. PR #5 (cross-platform emission bug fixes) merged into `main` on 2026-05-26 — the references are historical context for *what is being verified*, not instructions to clone PR #5. Newer arcs (PR #6 Claude QA, PR #8 hermetic stub, PR #9 minimal-stable, PR #10 naming alignment) are reflected per-section where they touched that platform's behavior.

### 3.6 Repository state

Make sure you're on a recent `main` of `DgxSparkLabs/marketplace`:

```powershell
cd C:\Users\devic\source\marketplace
git fetch origin
git checkout main
git pull
git log --oneline -1        # expected: a86cb86 or newer
```

### 3.7 Example plugins used as canonical test items

Throughout the per-construct tests below, these plugin names are used as the standard examples — they all exist in `_generated/` after the generator runs:

| Construct | Plugin name(s) | Source dir(s) (under `src/` since `cd7a7d8`) |
|---|---|---|
| skill | `skill-example-single` · `skill-example-multi` | `src/skills/example-single/` · `src/skills/example-multi/` |
| rule | `rule-example` (not a Claude plugin — see F8) | `src/rules/example/` |
| agent (sub-agent) | `agent-example-single` · `agent-example-multi` | `src/agents/example-single/` · `src/agents/example-multi/` |
| command | `command-example-single` · `command-example-multi` | `src/commands/example-single/` · `src/commands/example-multi/` |
| hook | `hook-example-<event>` (×9) · `hook-example-multi` | `src/hooks/example-<event>/` · `src/hooks/example-multi/` |
| mcp | `mcp-example-single` · `mcp-example-multi` | `src/mcp-servers/example-single/` · `src/mcp-servers/example-multi/` |
| lsp | `lsp-example-single` · `lsp-example-multi` | `src/lsp-servers/example-single/` · `src/lsp-servers/example-multi/` |
| monitor | `monitor-example-single` · `monitor-example-multi` | `src/monitors/example-single/` · `src/monitors/example-multi/` |
| output-style | `output-style-example-single` · `output-style-example-multi` | `src/output-styles/example-single/` · `src/output-styles/example-multi/` |
| theme | `theme-example-single` · `theme-example-multi` | `src/themes/example-single/` · `src/themes/example-multi/` |

---

## 4. Claude Code

**What we're verifying**: marketplace registration + per-construct install for the **9 construct types** Claude supports (`ClaudeCodePlatform.supports` per `docs/PLATFORMS.md` Claude "What constructs it supports" — `RuleConstruct` was removed 2026-05-26 because rules are not a Claude plugin component per `code.claude.com/docs/en/plugins-reference#plugin-components-reference`). This is also the verification surface for the 2026-05-26 Claude QA fixes (marketplace description, LSP / monitor / theme / hook example fixes, `uv` prereq doc, rule emission retirement) — see the validation list below.

### 4.1 Setup option A — Dev Container (recommended)

The repo ships `.devcontainer/` with everything pre-wired — Claude CLI, Node 20, Python 3.12, `uv`, Flask (for the hermetic stub), `git`, `gh`, plus VS Code extensions. See `.devcontainer/README.md` for the full inventory.

```text
1. Install Docker Desktop + the VS Code "Dev Containers" extension.
2. Open the repo in VS Code -> "Reopen in Container" when prompted.
3. First build runs .devcontainer/post-create.sh and prints what's installed + next steps.
4. Open a terminal inside VS Code (Ctrl+`). Run `claude` to sign in.
```

Forwarded ports: 8088 (F5 sentinel stub) and 8089 (F7/F9 body-dumper stub). Claude config persists across rebuilds via a named docker volume scoped to this repo's container ID.

### 4.2 Setup option B — Docker (manual, hermetic)

Use this when you want a one-off container without the dev container's VS Code integration — e.g., scripting the QA pass or testing on a host without VS Code. The pattern below bind-mounts your current working directory into the container, so whatever branch you have checked out on the host is what the container tests — no `git clone` step needed.

From the marketplace repo root on the host (PowerShell):

```powershell
docker run --rm -it --name qa-claude `
  -v "${PWD}:/workspace/marketplace" `
  -w /workspace/marketplace `
  node:20 bash
```

Or POSIX bash:

```bash
docker run --rm -it --name qa-claude \
  -v "$PWD:/workspace/marketplace" \
  -w /workspace/marketplace \
  node:20 bash
```

The `--rm` flag auto-removes the container on exit. `-w` lands you in the mounted dir. Once inside, install the three things `node:20` doesn't ship with:

```bash
# 1. Claude CLI
npm install -g @anthropic-ai/claude-code
claude --version

# 2. uv (Python tool for the marketplace generator + the hermetic stub)
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv --version
```

That's the entire prep. **No separate Flask install** — the hermetic stub uses PEP 723 inline metadata, so `uv run tests/fixtures/claude-stub/stub.py` fetches Flask into an ephemeral env on first invocation. To test a specific PR branch, check it out on the host (`git checkout <branch>`) before running the `docker run`; the container sees the host's working tree live.

### 4.3 Setup option C — Native

```powershell
npm install -g @anthropic-ai/claude-code
claude --version
```

### 4.4 Auth

Marketplace registration, listing, and install are auth-free (verified by `act`-based CI). `claude auth login` is only required if you actually use Claude for chat — not for the QA flow here.

### 4.5 Hermetic Claude session (no auth required)

For verifying F5 / F7 / F9 in CI or on a host with no Anthropic account, run Claude against a local stub server that returns Anthropic-shape responses. Hooks fire before the API call, slash commands resolve client-side, and output-style content appears verbatim in the request body — all three become observable from the stub's access log + captured bodies + sentinel files. F4 (theme visual distinctness) still requires interactive auth because it's a TTY paint operation with no observable in the request stream.

Inside the container after installing Claude (the dev container already has `uv` ready):

```bash
# 1. Pick which stub to run. Both are self-bootstrapping PEP 723 scripts —
#    `uv run` fetches Flask into an ephemeral env on first invocation, no
#    separate `pip install` or apt package needed.
#    Use stub.py for F5 (sentinel files are the observable).
#    Use stub_body_dumper.py for F7 / F9 (request bodies need grepping).
uv run tests/fixtures/claude-stub/stub.py > /tmp/stub-server.log 2>&1 &
sleep 1   # wait for Flask to bind

# 2. Point Claude at the stub.
export ANTHROPIC_BASE_URL=http://127.0.0.1:8088
export ANTHROPIC_AUTH_TOKEN=stub            # any non-empty value works
export API_TIMEOUT_MS=20000                 # fail fast on stub bugs
```

Now any `claude` invocation routes through the stub. Each affected validation below has a "Hermetic verification" sub-step you can use in place of the interactive-auth step. The stub's source + per-env-var details live at `tests/fixtures/claude-stub/README.md`. CI runs the same recipe in `.github/workflows/compat-headless-claude.yml`.

> **Alternative: dockerized stub with bind-mounted logs.** If you want captured request bodies on your host filesystem (so you can `grep` them from outside the container), or if you're orchestrating multiple containers, build the stub as its own Docker image and have qa-claude join its network namespace. See `tests/fixtures/claude-stub/README.md` section "Docker workflow" for the two-`docker run` recipe. Trade-off: an extra `docker build` step up front, but the captured bodies stream to `./.stub-logs/stub-bodies.log` on the host where you can `tail -f` them live without ever exec'ing into the container.

### 4.6 Marketplace registration

Use the `claude` CLI directly — these commands are scriptable and work in headless containers (the equivalent `/plugin ...` slash commands require the interactive Claude session UI).

- [ ] Step 1: Register the marketplace. Pick ONE of:
  - **Remote `main`**:
    ```bash
    claude plugin marketplace add DgxSparkLabs/marketplace
    ```
  - **Remote PR branch** — Claude's `plugin marketplace add` has **no documented `--ref` flag** per `docs/PLATFORMS.md` Claude "Known gaps". To test a PR branch, clone it locally first then use the local-clone form below.
  - **Local clone** (recommended for testing in-flight changes — tests exactly the bytes at `/workspace/marketplace`):
    ```bash
    claude plugin marketplace add /workspace/marketplace
    ```
  - **Expected (remote-main and local-clone)**: "Successfully added marketplace 'dgxsparklabs-marketplace'" (or similar).
- [ ] Step 2: list registered marketplaces:
  ```bash
  claude plugin marketplace list
  ```
  **Expected**: `dgxsparklabs-marketplace` appears in the output.
- [ ] Step 3: enumerate available plugins from this marketplace specifically (filtering by `marketplaceName` avoids dumping every globally-known plugin):
  ```bash
	MARKETPLACE="dgxsparklabs-marketplace"
	
	claude plugin list --json --available > /tmp/plugins.json 2>/tmp/claude.err
	
	jq --arg mp "$MARKETPLACE" '
	  [.. | objects | select(.marketplaceName? == $mp)]
	' /tmp/plugins.json
  ```
  **Expected**: JSON array of **27** plugins — **26 Claude-supported individuals + 1 cross-construct catalog bundle** `bundle-examples`. The 26 individuals are: 8 construct types (skill / command / agent / mcp / lsp / monitor / output-style / theme) × `{-single, -multi}` = 16, plus the hook family = 9 per-event plugins (`hook-example-userpromptsubmit` … `hook-example-precompact`) + 1 `hook-example-multi` = 10. Rule individuals are excluded per F8. Empirically verified 2026-05-30 against `claude` CLI 2.1.157: this enumeration returns exactly 27. If you see **10**, you are on a pre-`cd7a7d8` checkout (the symmetric single/multi expansion had not landed).

- [ ] Step 4 — **install auto-enables (CLI ≥ 2.1.157); the old "enable-after-install" gotcha is REVERSED**. Verified 2026-05-30 against `claude` 2.1.157: `claude plugin install <plugin>@dgxsparklabs-marketplace --scope project` lands the plugin **already enabled** — it writes `"enabledPlugins": { "<plugin>@dgxsparklabs-marketplace": true }` straight into `<project>/.claude/settings.json`. Running a separate `claude plugin enable …` afterward now *errors* with `Plugin "<…>" is already enabled`. (Older CLIs ≤ the 2026-05-26 research baseline landed plugins disabled and required an explicit enable; that is no longer true.) The per-construct cells below keep an **Enable** step for back-compat with older CLIs — on 2.1.157 it is a harmless no-op that prints "already enabled"; treat that as PASS, not failure.
  - **Scope is cwd-relative.** Because `--scope project` writes enablement into the *current directory's* `.claude/settings.json`, `claude plugin list` only shows `✔ enabled` when run **from the same project dir** you installed in. Run it from elsewhere and the same plugins read back `✘ disabled` — that is correct scope behavior, not a regression. This is the new single most likely cause of "I installed it but `list` says disabled."

### 4.7 Claude construct reference card — exact strings to type and expect

This table is the cheat sheet for the per-construct cells below. As of `cd7a7d8`, every Claude-supported construct ships **two reference plugins** — a `-single` (solo: one component, the simplest possible plugin of that type) and a `-multi` (several components in one plugin) — so QA exercises both layouts. Hooks are the exception: they ship as **9 per-event plugins + 1 `-multi`** covering all nine events.

> **Namespace model — Path A was reverted (`649b398`).** The earlier "shared brand namespace" (`/dgxsparklabs-skill:` as one entry point for every skill) is **gone**. Each plugin now has its **own** slash namespace equal to its `plugin.json` `name`, which is `dgxsparklabs-<install-name>`. So the install name `skill-example-multi` → slash namespace `dgxsparklabs-skill-example-multi` → invoked as `/dgxsparklabs-skill-example-multi:<component>`. Ignore any lingering reference to `docs/research/shared-namespace-2026-05-27/` for invocation strings — that approach is no longer shipped.

Two decoupled names per plugin: the **install name** (`skill-example-multi`, what you type at `claude plugin install`) lives in `marketplace.json`; the **slash namespace** (`dgxsparklabs-skill-example-multi`) is the `plugin.json` `name`. The **component** suffix after the `:` is the construct's own internal name (skill/agent/output-style frontmatter `name:`, command filename stem, MCP server key, etc.).

Install pattern for every row: `claude plugin install <install-name>@dgxsparklabs-marketplace --scope project` (auto-enables — see Step 4). Slash namespace for every row = `dgxsparklabs-<install-name>`. ✅ marks invocation strings empirically captured in the 2026-05-30 hermetic QA (request-body inspection / sentinel files); ◦ marks per-spec behavior an operator is the first to confirm interactively.

| Construct · variant   | Install name                   | Invoke (component(s) after the `:`)                                                                 | Expected behavior                                                                 |
|---                    |---                             |---                                                                                                  |---                                                                                |
| skill · single        | `skill-example-single`         | ✅ `/dgxsparklabs-skill-example-single:hello`                                                        | Solo plugin (SKILL.md at plugin root). Prints a minimal greeting + UTC timestamp. |
| skill · multi         | `skill-example-multi`          | ✅ `/dgxsparklabs-skill-example-multi:notebook [topic]` · `:status`                                  | `notebook` → lab-notebook status block; `status` → `df -h .` + UTC timestamp.     |
| command · single      | `command-example-single`       | ✅ `/dgxsparklabs-command-example-single:hello`                                                      | Prints a lab-notebook header for today's UTC date.                                |
| command · multi       | `command-example-multi`        | ✅ `/dgxsparklabs-command-example-multi:hello` · `:goodbye` · `:ping`                                | `hello` → header; `goodbye` → closing footer; `ping` → "pong" + UTC.              |
| agent · single        | `agent-example-single`         | ◦ `/agents` → select `dgxsparklabs-agent-example-single:notebook-reviewer`                          | Sub-agent dispatched as a skeptical peer reviewer of a lab-notebook entry.        |
| agent · multi         | `agent-example-multi`          | ✅ `/agents` → `dgxsparklabs-agent-example-multi:notebook-reviewer` · `:summarizer` · `:validator`   | Three sub-agents in one plugin; pick any from the picker. Live-verified (4.8.3).  |
| hook · per-event (×9) | `hook-example-<event>`         | passive — fires its one event                                                                       | Writes `/tmp/hook-fired-<event>.log`. One plugin per event (`…-userpromptsubmit` … `…-precompact`). |
| hook · multi          | `hook-example-multi`           | passive — fires all nine events                                                                     | ✅ each sentinel `/tmp/hook-fired-<event>.log` holds a marker + the full JSON payload (stdin). All 9 live-verified; see 4.8.5. |
| mcp · single          | `mcp-example-single`           | ◦ model-called tool, server key `example` (confirm `mcp__…` name via `claude --debug`)              | Claude can fetch URLs via the wrapped server. Requires `uv` on PATH.              |
| mcp · multi           | `mcp-example-multi`            | ✅ model-called tools, server keys `fetch` · `filesystem` · `sequential-thinking`                    | Three MCP servers in one plugin (each behind a logging proxy). Requires `uv`. Live-verified (4.8.6). |
| lsp · single / multi  | `lsp-example-single` / `-multi`| ✅ (multi) auto-attaches by file extension (`.md`, `.py`) | **single** → external `marksman` (install separately). **multi** → bundled `example_lsp.py` (markdown+python, only `uv` needed) — a real stdlib LSP: diagnostics + symbols + go-to-definition + hover + references. Multi live-verified; see 4.8.7. |
| monitor · single      | `monitor-example-single`       | ◦ passive — runs `disk-usage` at session start                                                      | `df -h .` output once per session.                                                |
| monitor · multi       | `monitor-example-multi`        | ✅ passive — `disk-usage` · `memory-usage` · `git-status`                                             | Three monitors in one plugin, each runs at session start (output prefixed `[monitor:<name>]`). Live-verified (4.8.8). |
| output-style · single | `output-style-example-single`  | ◦ `/config` → **Output style** (no `/output-style` command in 2.1.159)                              | Replies adopt measured, citation-focused prose. Persists namespaced to project `.claude/settings.local.json` `"outputStyle"`. |
| output-style · multi  | `output-style-example-multi`   | ✅ `/config` → **Output style** → pick `dgxsparklabs-output-style-example-multi:{Lab Notebook Voice,Concise Engineer,Tutoring}` | Three selectable styles in one plugin. Verified live 2026-06-01 (4.8.9).          |
| theme · single        | `theme-example-single`         | ◦ `/theme` picker → `Lab Notebook`                                                                  | Terminal flips to the Lab Notebook palette. F4 interactive cell.                  |
| theme · multi         | `theme-example-multi`          | ✅ `/theme` picker: `Lab Notebook` · `Nord` · `Solarized Dark` (persists `custom:dgxsparklabs-theme-example-multi:<stem>` to user settings) | Three selectable themes in one plugin. Verified live 2026-06-01 (4.8.10).         |
| rule                  | N/A (not a Claude plugin component since 2026-05-26) | rule applies passively (no slash)                                              | See Claude validation 8.                                                          |

**Reading the slash columns**: the namespace before the `:` is the **plugin's own** `plugin.json` `name` = `dgxsparklabs-<install-name>` (e.g. `dgxsparklabs-skill-example-multi`) — one namespace per plugin, not shared across a construct type. The suffix after the `:` is the component's own name from inside the plugin: for skill it's the SKILL.md frontmatter `name:` (`notebook`, `status`, `hello`); for sub-agent the agent-file frontmatter `name:` (`notebook-reviewer`, …); for command the filename stem (`hello`, `goodbye`, `ping`); for MCP the server key in the mcp config. The 2026-05-30 hermetic capture shows the resolved form verbatim in the request body, e.g. `<command-name>/dgxsparklabs-command-example-multi:hello</command-name>`. Output-style and theme are **global selectors**, not plugin-namespaced slashes, and their invocation surface differs in CLI 2.1.159 (verified live 2026-06-01): **theme** uses the `/theme` picker; **output style** has **no** `/output-style` command and is set under `/config` → Output style. In the selectors the plugin entries appear namespaced (`dgxsparklabs-output-style-example-multi:Lab Notebook Voice`; `custom:dgxsparklabs-theme-example-multi:lab-notebook`).

**After-install enable step**: on CLI ≥ 2.1.157 install auto-enables (Step 4), so the explicit `Enable` step in each cell below is a back-compat no-op that prints `already enabled` — that output is PASS. The 2026-05-30 hermetic run confirms behaviorally: hooks fired after a bare `install` with no separate enable.

**Interactive vs headless**: many Claude slash commands require an interactive TTY session and return `Unknown command` or `isn't available in this environment` when invoked via `claude --print` (headless). Cells below flag this per-construct. Specifically: `/mcp`, `/agents`, `/theme`, and `/config` (where Output style lives) are all interactive-TUI-only — they error or no-op under `claude --print`. (Note: there is no `/output-style` command in 2.1.159; older logs referencing `/output-style <name>` predate this build. See `docs/research/naming-conventions-2026-05-26/logs/15-output-style-theme.log:2-7` for the historical capture, and 4.8.9–4.8.10 for the live 2026-06-01 mechanics.)

**Where do the names come from?** Two decoupled names per plugin. The **install** name (`skill-example-multi`, what you type at `claude plugin install`) is `<construct.prefix>-<source-dir-name>`, where the source dir now lives under `src/<construct>/` (e.g. `src/skills/example-multi/`) — sources moved into `src/` in `cd7a7d8`. The **slash** namespace is the `plugin.json` `name` = `dgxsparklabs-<install-name>` (per-plugin; the shared `dgxsparklabs-<category>` of Path A was reverted in `649b398`). The **component** name (`notebook`, `status`, `hello`) is the SKILL.md frontmatter `name:` field (operator-authored, e.g. `src/skills/example-multi/skills/notebook/SKILL.md`). See [`ADDING_A_CONSTRUCT.md`](./ADDING_A_CONSTRUCT.md) for the full byte-by-byte breakdown.

### 4.8 Per-construct verification

Each test installs ONE plugin of the construct type, then invokes it. Per-construct cleanup is folded into the master cleanup block at the end.

> **Provenance of the "what you'll see" captures.** Every `▶` block below was captured **live** in container `qa-claude`, CLI `2.1.159`, on 2026-06-01. The container's default model **varied by session** — some captures are Haiku 4.5, some Opus 4.8 (e.g. the `SessionStart` payload in 4.8.5 records `"model":"claude-opus-4-8"`) — so the per-cell stamps just say "verified live 2026-06-01" and point here rather than naming a model. The live tmux path (4.8.0 + these cells) is the **primary** verification method; the headless/hermetic stub path (4.9) is a no-auth **alternative**.

> **These are "debug examples" — every construct surfaces its own inputs (added 2026-06-01).** For a new author, the most valuable thing to see is *exactly what data Claude hands your construct*. So each example now logs/echoes its inputs, and the proof signal for each is the input it reveals — not the model's prose. Where to look per construct:
>
> | Construct | How it surfaces its input | Where you see it |
> |---|---|---|
> | hook | reads the hook JSON payload from **stdin** (`p="$(cat)"`) | `/tmp/hook-fired-<event>.log` — marker line + full payload (tool_name, tool_input, cwd, session_id…) |
> | mcp | bundled `mcp_logging_proxy.py` tees JSON-RPC both ways | `/tmp/mcp_proxy_<server>.log` — `->` requests / `<-` responses |
> | lsp | always-error marker + message log (the original debug example) | `${TMPDIR}/example_lsp.log` + the `(example-lsp)` diagnostic |
> | command / skill | echoes a `[command:<name>] args=[$ARGUMENTS]` / `[skill:<name>] …` debug line | first line of the rendered output |
> | sub-agent | instructed to begin its reply with a verbatim `[agent-input]` block | the agent's first output block |
> | monitor | each command prefixes its output with `[monitor:<name>]` | the session-start context the model recites |
>
> **The pattern to copy when writing your own debug construct:** find where the host hands you data (stdin for hooks, stdio JSON-RPC for MCP, `$ARGUMENTS` for commands/skills, the delegated task for agents) and echo it verbatim to a log or to the output *before* doing the real work. Then you are debugging against ground truth, not guessing. The cells below were partly captured before this change landed; the input-surfacing line is additive (it precedes the documented output).

#### 4.8.0 Day-to-day usage and the rookie operator guide

Two different audiences read this section. **First**, the everyday-usage table (4.8.0) tells a *human user* how they actually invoke each construct during normal work. **Then**, the rookie-operator guide (4.8.0.1) tells an *AI agent* exactly how to set up the container and drive each construct through tmux to verify it — every command, every expected output, no guessing.

**Three summaries, three jobs — don't confuse them:** the **reference card** (4.7) is the install-and-invoke matrix (install names, exact slash strings, ✅/◦ verification status); the **day-to-day table** just below is the human-usage view; the **per-construct cells** (4.8.1–4.8.10) are the deep dives with live captures. The per-construct cells are numbered in historical order (skill=1, rule=2, agent=3, command=4, …), **not** difficulty order — the rookie guide below runs them easiest-first (command → skill → sub-agent → hook → mcp → monitor → output-style → theme → lsp), which is the order to follow.

**Day-to-day usage — how you actually invoke each construct** (the `dgxsparklabs-…-example-multi` plugins; install names in cell 4.8's reference card):

| Construct | What it is | How you use it day-to-day | What you see |
|---|---|---|---|
| **command** | a reusable slash prompt | type `/dgxsparklabs-command-example-multi:hello` (also `:goodbye`, `:ping`), Enter | a rendered markdown block, preceded by the debug line `[command:hello] args=[…]` |
| **skill** | a model-invoked capability (`SKILL.md`) | type `/dgxsparklabs-skill-example-multi:notebook <topic>` (also `:status`); or just describe a task its `description` matches and Claude auto-loads it | the skill's output block, preceded by `[skill:notebook] args=[<topic>]` |
| **sub-agent** | a separate agent with its own context + tools | ask in plain English ("use the …:summarizer subagent to summarize X"), or open `/agents` to view/manage them | a nested `…:summarizer(…)` task + a `Done (N tool use…)` line (expand with `ctrl+o`) |
| **hook** | a shell command bound to a lifecycle event | nothing — it fires automatically (session start, prompt submit, tool use, compaction, exit, …) | usually invisible; effects are side-effects (sentinel files written, a context line injected) |
| **mcp** | external tool servers | nothing to invoke directly — ask naturally ("fetch https://…") and Claude calls the `mcp__…` tool; `/mcp` shows server status | a tool-permission prompt, then a `Called plugin:…:<server>` line + the result |
| **monitor** | a shell command run once at session start | nothing — runs automatically when the session opens; its stdout is added to Claude's context | usually nothing in the UI; the model may mention it (e.g. `[monitor:disk-usage]` data) |
| **output-style** | a system-prompt voice preset | `/config` → **Output style** → pick one (**no `/output-style` command** in 2.1.159) | replies adopt the new voice; persists in project `.claude/settings.local.json` |
| **theme** | a terminal colour palette | `/theme` → pick one from the picker | colours change immediately; persists in user `~/.claude/settings.json` |
| **lsp** | a language server feeding diagnostics + navigation | nothing to invoke — **edit** a matching file and diagnostics auto-attach; ask "list the symbols / go to definition" for navigation | `⎿ Found N new diagnostic issue` after an edit; `(example-lsp)`-tagged diagnostics |

Passive constructs (**hook**, **monitor**, **lsp**) are never "invoked" — they react to what you're already doing. Active constructs (**command**, **skill**, **sub-agent**, **mcp** tools, **output-style**, **theme**) you trigger explicitly.

##### 4.8.0.1 Rookie operator guide — set up the container and run every construct test through tmux

*You are an AI agent verifying these constructs. You are NOT a human at a keyboard: Claude runs **inside a Docker container, inside a tmux session**, and you drive it by injecting keystrokes from the host with `docker exec <container> tmux …` and reading the screen back with `capture-pane`. This guide is **self-contained** — Part 0 teaches the exact docker + tmux primitives, then Parts A–C use only those, so you never have to guess a command. (Cell 4.8.7's "Driving this through tmux as an automated agent" guide has extra LSP-specific depth, but you do not need it to follow this.) Every command and output below was captured live 2026-06-01 in container `qa-claude`, CLI 2.1.159. Replace `qa-claude` everywhere with the real container name from step 0.2.*

**▶ Lessons from the cold-read test — read this FIRST (the six things that actually trip rookies)**

On 2026-06-02 we ran a controlled experiment: nine fresh agents, each with zero prior context, each verified ONE construct using only this guide. **All nine constructs PASSED** — the constructs are solid. But the agents independently hit the same handful of snags. Here they are with the fix and exact commands, so you don't rediscover them the hard way:

1. **Grey "ghost-suggestion" text is NOT your input, and `C-u` does NOT remove it.** After almost every turn the input box shows dimmed grey text — an autocomplete hint from session history (e.g. `explore the lsptest directory`, `git init`). It will not submit on its own and it does not corrupt your next command. `C-u` clears any *real typed* characters but leaves the grey hint on screen; it only disappears once you type a fresh command over it. **Do not fight it** — 8 of 9 agents wasted tool calls pressing `C-u`/`Escape` at it. Just send your command (the `-l` text overwrites the line):
   ```bash
   docker exec qa-claude tmux send-keys -t 0:0.0 -l '/dgxsparklabs-command-example-multi:hello'
   docker exec qa-claude tmux send-keys -t 0:0.0 Enter
   ```

2. **`capture-pane | tail -n N` lies — pull scrollback, and for file-based proofs read the FILE.** A freshly split pane or a chatty turn pushes the block you want above the visible tail, so `tail -n 8` comes back blank or clipped (this bit the skill, hook, theme, and lsp testers). Always widen with `-S` and, when the proof is a file (hook sentinels, mcp proxy log, lsp input log), read the file directly instead of the screen:
   ```bash
   docker exec qa-claude tmux capture-pane -p -t 0:0.0 -S -30 | tail -n 20   # not just `| tail -n 8`
   docker exec qa-claude bash -lc 'cat /tmp/hook-fired-pretooluse.log'        # the proof is the file, not the pane
   ```

3. **Make persistence/sentinel proofs CAUSAL — establish a control first.** The container is NOT a clean slate between runs: theme/output-style may already hold the value you are about to set, and `SessionStart`/`Stop` hooks fire at launch *before* you do anything. Grepping the value or listing sentinels then "passes" without your action having caused it. Reset first:
   ```bash
   docker exec qa-claude bash -lc 'rm -f /tmp/hook-fired-*.log'   # hooks: the rm IS the control, not cleanup
   # theme: in /theme, first select "Dark mode", confirm settings.json reads "dark",
   #        THEN select the plugin theme — now the flip dark → custom:… is one you caused.
   ```

4. **The container clock can lag the host — match the SHAPE of the output, not the literal date.** Captured timestamps read `2026-06-01…` from the container's `date -u`, and the doc's frozen samples use that same date. Do not diff dates character-for-character (you will false-match by luck or false-fail tomorrow); the date was never the thing under test.

5. **A capable model (Opus 4.x) narrates a LOT unprompted — that prose is not proof.** Before you send anything you will often see the model recite the session-start monitor data, muse about a bug it spotted by reading, and propose "Next:" steps. That is the model reading its own context, NOT your construct firing. For every construct, trust the *real signal* — the `(example-lsp)` source tag, the `Called plugin:…` line, the sentinel file, the settings write — and never the model's description. (The LSP tester watched the model propose `pyflakes` as if no language server existed.)

6. **TUI menus open on a default tab/row you must navigate FROM — they are not where you think.** `/agents` opens on the **Running** tab, which says `No subagents are currently running` — that is NOT failure; press `Left` once to reach the **Agents** tab where the plugin agents live. In `/config` and `/theme` the highlight starts on the *currently active* item, so the number of `Down` presses is state-dependent — capture the `❯` row first, then compute the delta; never hardcode "press Down N times".

**Part 0 — the docker + tmux mechanics you use at every step.** There are only eight; every later command is built from these. If you have never driven tmux from outside before, read this part slowly — it is the whole game.

**0.1 — Run a shell command inside the container.** Your tools run on the *host*. To run something *inside* the container, wrap it in `docker exec <container> bash -lc '<command>'`:
```bash
docker exec qa-claude bash -lc 'ls /workspace'
```

**0.2 — Find the container and the tmux session.**
```bash
docker ps --format '{{.Names}}\t{{.Status}}'        # → the running container, e.g. "qa-claude  Up 2 hours"
docker exec qa-claude tmux ls                        # → "0: 1 windows (attached)"  — the session is NAMED "0"
docker exec qa-claude tmux list-panes -t 0:0 -F '#{pane_index} cmd=#{pane_current_command}'
```
If `tmux ls` says "no server running on …", create a session first: `docker exec qa-claude tmux new-session -d -s 0`.

**0.3 — Pane addressing is `session:window.pane`.** The session is named `0`, so `0:0.0` = session 0, window 0, **pane 0** (left); `0:0.1` = **pane 1** (right). After a horizontal split the original keeps index `0`; the new pane is index `1`. You pass these as `-t 0:0.0` / `-t 0:0.1` to every `send-keys` and `capture-pane`.

**0.4 — Send keystrokes (THE most important rule).** Send the *text* with `-l` (literal), then send `Enter` as a **separate** call. Never combine them:
```bash
docker exec qa-claude tmux send-keys -t 0:0.0 -l 'some text'   # types the text into pane 0 (does NOT submit)
docker exec qa-claude tmux send-keys -t 0:0.0 Enter            # presses Return — a key NAME, so NO -l
```
- `-l` types the string verbatim. **Without `-l`, tmux interprets words as key *names*.** So special keys are sent WITHOUT `-l`: `Enter`, `Up`, `Down`, `Escape`, `Tab`, `Space`, `C-c` (Ctrl-C, interrupt), `C-u` (clear the input line), `C-o` (expand a collapsed block).
- ⚠ **Putting text and `Enter` in one `-l` call literally types the word "Enter" and never submits** — the single most common mistake.

**0.5 — Read a pane** with `capture-pane -p` (prints the visible screen). Add `-S -<n>` to include scrollback when output scrolled off the top:
```bash
docker exec qa-claude tmux capture-pane -p -t 0:0.0            # current screen
docker exec qa-claude tmux capture-pane -p -t 0:0.0 -S -25     # + 25 lines of history
```
**Blank capture?** The command didn't land or Claude exited. Diagnose with `list-panes` (0.2): if pane 0 shows `bash` when you expected `claude`/`node`, your launch failed (almost always a bad `cd` — a pane's cwd/`$HOME` differs from a `docker exec bash -lc` shell, so **use absolute paths**).

**0.6 — Always `sleep` before capturing.** Keystrokes are async and the model needs time. Rules of thumb: TUI boot ≈ 15 s; a permission dialog appears ≈ 6–9 s after an edit/tool prompt; a full model turn ≈ 6–20 s. Capture too early and you read a half-rendered screen and wrongly conclude it failed. Also: a follow-up prompt **won't submit while the model is busy** (a spinner like `✻ Brewed for 7s` is showing) — wait for the idle `❯` prompt. (Ignore any dimmed grey ghost-suggestion text in the input box — it is a cosmetic autocomplete hint, not input, and `C-u` does NOT remove it; see lesson 1 above. `C-u` only clears *real* typed characters.)

**0.7 — Answer Claude's interactive dialogs.** They block until answered; each is a menu with one highlighted row. `Enter` accepts the highlighted row (usually "Yes" / option 1); `Down`/`Up` move the highlight; `Escape` cancels. Examples you will hit below: "Trust this folder?" → `Enter`; an edit dialog → `Enter` (=Yes, one edit) or `Down` then `Enter` (=allow all edits this session); a tool-permission dialog → `Enter`.

**0.8 — Windows / Git-Bash hosts only: bare-slash commands.** A bare `/word` slash (`/mcp`, `/theme`, `/config`, `/agents`, `/exit`) sent through a Git-Bash host is rewritten to a Windows path before it reaches the container, so Claude receives garbage. Prefix those `send-keys` calls with `MSYS_NO_PATHCONV=1` (shown inline below). Namespaced slashes (`/dgxsparklabs-…:hello`) are immune — the `:` disables the conversion. On Linux/macOS hosts, ignore this and drop the prefix. See `PITFALLS.md`.

**Part A — one-time setup (~2 min).** Each step shows the command and the real output to expect. Every command uses only the Part 0 primitives.

1. **Find the container** (its hostname varies; it gets recreated):
   ```bash
   docker ps --format '{{.Names}}\t{{.Status}}'
   # → qa-claude   Up 2 hours
   ```
2. **Create an absolute scratch dir** (a pane's cwd/`$HOME` can differ from a `docker exec bash -lc` shell — always use absolute paths):
   ```bash
   docker exec qa-claude bash -lc 'mkdir -p /workspace/lsptest && cd /workspace/lsptest && pwd'
   # → /workspace/lsptest
   ```
3. **Install all nine `example-multi` plugins** into that project scope (install auto-enables on CLI ≥2.1.157):
   ```bash
   docker exec qa-claude bash -lc 'cd /workspace/lsptest && for p in command skill agent hook mcp monitor output-style theme lsp; do claude plugin install ${p}-example-multi@dgxsparklabs-marketplace --scope project 2>&1 | tail -n1; done'
   # → nine lines, each: ✔ Successfully installed plugin: <p>-example-multi@dgxsparklabs-marketplace (scope: project)
   ```
4. **Confirm enabled:**
   ```bash
   docker exec qa-claude bash -lc 'cd /workspace/lsptest && claude plugin list 2>&1 | grep -E "@dgxsparklabs|Status:" | paste - -'
   # → every row shows ✔ enabled  (a few plugins list twice — cosmetic quirk, still enabled)
   ```
5. **(Only if you want a live log tail — i.e. for LSP) split tmux into two panes** (left = Claude, right = a shell for tailing logs). Targets are `0:0.0` (left) and `0:0.1` (right). **For command/skill/sub-agent/output-style/theme there is nothing to tail — skip this and use the single pane.** For hooks/MCP/LSP you *can* tail in a second pane, but reading the log file directly (`cat`/`grep`) works just as well, so this split is optional for everything except the LSP two-pane walkthrough (4.8.7):
   ```bash
   docker exec qa-claude tmux split-window -h -t 0:0
   docker exec qa-claude tmux list-panes -t 0:0 -F '#{pane_index} #{pane_current_command}'
   # → 0 bash   /   1 bash
   ```
   (Step 3 installs all nine plugins for convenience; if you are verifying only ONE construct you may install just that plugin — `claude plugin install <construct>-example-multi@dgxsparklabs-marketplace --scope project` — they are independent.)
6. **Launch Claude in the left pane** (plain `claude`, absolute `cd`), then wait and read:
   ```bash
   docker exec qa-claude tmux send-keys -t 0:0.0 -l 'cd /workspace/lsptest && claude'
   docker exec qa-claude tmux send-keys -t 0:0.0 Enter
   sleep 16
   docker exec qa-claude tmux capture-pane -p -t 0:0.0 | tail -n 14
   ```
   - If you see **"Do you want to trust the files in this folder?"**, press `Enter` (Yes is highlighted): `docker exec qa-claude tmux send-keys -t 0:0.0 Enter`. If the path was trusted earlier you skip straight to the prompt.
   - When ready you'll see an empty `❯` prompt and `? for shortcuts`. Because **monitors** are installed, the model usually narrates the session-start monitor reports first, e.g. a line mentioning `[monitor:git-status] … this isn't a git repo`. That narration is itself live proof the monitor construct fired.

**Part B — run each construct (this order; easiest first).** Always `sleep` before capturing (TUI boot ≈ 15 s; a permission dialog appears ≈ 6–9 s after an edit/tool prompt; a model turn ≈ 6–20 s). Capturing too early reads a half-rendered screen.

1. **command** — visible slash output:
   ```bash
   MSYS_NO_PATHCONV=1 docker exec qa-claude tmux send-keys -t 0:0.0 -l '/dgxsparklabs-command-example-multi:hello'
   docker exec qa-claude tmux send-keys -t 0:0.0 Enter
   sleep 6
   docker exec qa-claude tmux capture-pane -p -t 0:0.0 | tail -n 10
   ```
   Expect (the `[command:hello]` line is the debug echo — it shows the raw args, empty here):
   ```text
     Ran 1 shell command
   ● [command:hello] args=[]
     # Lab Notebook — 2026-06-01
     ## Entries
     - [ ] (add entries here)
   ```
   Full detail (`:ping`, `:goodbye`, the autocomplete dropdown): cell 4.8.4.

2. **skill** — pass a topic argument:
   ```bash
   MSYS_NO_PATHCONV=1 docker exec qa-claude tmux send-keys -t 0:0.0 -l '/dgxsparklabs-skill-example-multi:notebook rookie-onboarding'
   docker exec qa-claude tmux send-keys -t 0:0.0 Enter
   sleep 7
   docker exec qa-claude tmux capture-pane -p -t 0:0.0 -S -18 | tail -n 12
   ```
   Expect the debug line carrying your argument, then the block:
   ```text
   ● [skill:notebook] args=[rookie-onboarding]
     [Lab Notebook] Status update on "rookie-onboarding"
     - Time: 2026-06-01T20:22:45Z
     - Status: in-progress
     - Next checkpoint: …
   ```
   Full detail (`:status`, the bare-label dropdown quirk): cell 4.8.1.

3. **sub-agent** — make a file, then dispatch:
   ```bash
   docker exec qa-claude bash -lc 'printf "# Demo\nA short note for the rookie onboarding agent test.\n" > /workspace/lsptest/demo-note.md'
   docker exec qa-claude tmux send-keys -t 0:0.0 -l 'Use the dgxsparklabs-agent-example-multi:summarizer subagent to summarize demo-note.md. Do not ask questions.'
   docker exec qa-claude tmux send-keys -t 0:0.0 Enter
   sleep 14
   docker exec qa-claude tmux capture-pane -p -t 0:0.0 | tail -n 12
   ```
   Expect the namespaced task header + a `Done` line (top-level proof it ran in its own context):
   ```text
   ● dgxsparklabs-agent-example-multi:summarizer(Summarize demo-note.md)
     ⎿  Done (1 tool use · 3.4k tokens · 7s)
   ● The summarizer subagent reviewed demo-note.md. Here's its summary: …
   ```
   The namespaced task header + the `Done` line are the proof — they always appear. The agent's prompt also asks it to echo its received task (`[agent-input]`), but that is model-dependent and **often skipped**, and it is collapsed under the `Done` line; `ctrl+o` (`send-keys … C-o`) toggles the whole transcript verbose but may reveal no echo at all. Don't treat the echo as a pass criterion. Full detail + caveats: cell 4.8.3.

4. **hook** — sentinel files, NO chat output (the most important debug construct). The `rm` below is the *control*, not cleanup: `SessionStart`/`Stop`/`SubagentStop`/`UserPromptSubmit` already fired at launch, so you must clear first to isolate THIS edit's events. One edit+approve fires **six**: `UserPromptSubmit` → `PreToolUse` → `Notification` (the permission dialog) → `PostToolUse` → `Stop` → `SubagentStop` (expect ~6 sentinel files after, not 5):
   ```bash
   docker exec qa-claude bash -lc 'rm -f /tmp/hook-fired-*.log'   # the control: isolates this edit's events
   docker exec qa-claude tmux send-keys -t 0:0.0 -l 'Use the Edit tool to append the line # hooktest as the last line of demo-note.md. Do not ask questions, just make the edit.'
   docker exec qa-claude tmux send-keys -t 0:0.0 Enter
   sleep 8
   docker exec qa-claude tmux capture-pane -p -t 0:0.0 -S -20 | tail -n 16   # the edit dialog is ~14 lines tall; -n 8 clips it
   docker exec qa-claude tmux send-keys -t 0:0.0 Enter                 # approve (option 1, Yes)
   sleep 6
   docker exec qa-claude bash -lc 'cat /tmp/hook-fired-pretooluse.log'   # read the FILE, not the screen
   ```
   Expect a marker line + the full JSON payload — note the real `tool_name` (the whole point of the debug hook):
   ```text
   2026-06-01T20:01:56Z preToolUse fired
   {"session_id":"…","cwd":"/workspace/lsptest","hook_event_name":"PreToolUse","tool_name":"Edit","tool_input":{"file_path":".../demo-note.md","old_string":"…","new_string":"…"},"tool_use_id":"toolu_…"}
   ```
   Full 9-event sequence (incl. `/compact` → `PreCompact` and `/exit` → `SessionEnd`): cell 4.8.5.

5. **mcp** — a server running behind the logging proxy. The servers spawn at session start, so their proxy logs already exist; then make a tool call:
   ```bash
   docker exec qa-claude bash -lc 'ls /tmp/mcp_proxy_*.log'    # → mcp_proxy_fetch.log, mcp_proxy_filesystem.log, mcp_proxy_sequential-thinking.log
   docker exec qa-claude tmux send-keys -t 0:0.0 -l 'Use the fetch MCP tool to retrieve https://example.com and show me just the page title. Do not ask questions.'
   docker exec qa-claude tmux send-keys -t 0:0.0 Enter
   sleep 6
   docker exec qa-claude tmux capture-pane -p -t 0:0.0 | tail -n 8     # expect a tool-permission dialog
   docker exec qa-claude tmux send-keys -t 0:0.0 Enter                 # approve
   sleep 14   # COLD CACHE: first-ever run downloads the server via uvx/npx — the call can take ~34s.
              # If no "Called plugin:…:fetch" line yet, sleep 20 more and re-capture BEFORE judging it failed.
   docker exec qa-claude tmux capture-pane -p -t 0:0.0 -S -16 | tail -n 8   # expect: Called plugin:…:fetch + "Example Domain"
   docker exec qa-claude bash -lc 'grep tools/call /tmp/mcp_proxy_fetch.log | tail -n1'   # the proxy-log line is the real proof
   ```
   The proxy-log line is the debug proof — the verbatim JSON-RPC request with the URL argument: `[fetch] -> {"method":"tools/call","params":{"name":"fetch","arguments":{"url":"https://example.com"},…}}`. Full detail (incl. the upstream `filesystem`/`zod` failure): cell 4.8.6.

6. **monitor** — session-start context (already fired at launch). Probe it, but **forbid tool use** or the model just runs `df` itself and proves nothing:
   ```bash
   docker exec qa-claude tmux send-keys -t 0:0.0 -l 'Without running any tool or command, quote verbatim any session-start monitor or observation context you were given. If you received none, say exactly: NO MONITOR CONTEXT.'
   docker exec qa-claude tmux send-keys -t 0:0.0 Enter
   sleep 8
   docker exec qa-claude tmux capture-pane -p -t 0:0.0 -S -20 | tail -n 16
   ```
   Expect the model to recite three monitors, each prefixed `[monitor:disk-usage]` / `[monitor:memory-usage]` / `[monitor:git-status]`. Full detail: cell 4.8.8.

7. **output-style** — set via `/config` (there is **no** `/output-style` command). Drive the config panel:
   ```bash
   MSYS_NO_PATHCONV=1 docker exec qa-claude tmux send-keys -t 0:0.0 -l '/config'
   docker exec qa-claude tmux send-keys -t 0:0.0 Enter ; sleep 3
   docker exec qa-claude tmux send-keys -t 0:0.0 -l 'output style' ; sleep 1   # filter to the row
   docker exec qa-claude tmux send-keys -t 0:0.0 Enter ; sleep 1               # select the row
   docker exec qa-claude tmux send-keys -t 0:0.0 Space ; sleep 1               # open the style list
   docker exec qa-claude tmux capture-pane -p -t 0:0.0 | tail -n 16            # see items incl. dgxsparklabs-output-style-example-multi:Lab Notebook Voice
   # navigate to the plugin style: send `Down` N times, then `Enter` to confirm, then `Escape` `Escape` to leave /config
   ```
   Proof = the persisted value:
   ```bash
   docker exec qa-claude bash -lc 'cat /workspace/lsptest/.claude/settings.local.json'
   # → {"outputStyle":"dgxsparklabs-output-style-example-multi:Lab Notebook Voice"}
   ```
   Full detail: cell 4.8.9.

8. **theme** — the `/theme` picker (this one IS a real command):
   ```bash
   MSYS_NO_PATHCONV=1 docker exec qa-claude tmux send-keys -t 0:0.0 -l '/theme'
   docker exec qa-claude tmux send-keys -t 0:0.0 Enter ; sleep 2
   docker exec qa-claude tmux capture-pane -p -t 0:0.0 | tail -n 16   # items 8–10: Lab Notebook / Nord / Solarized Dark (from dgxsparklabs-theme-example-multi)
   # the highlight starts on the CURRENTLY ACTIVE theme, so capture the `❯` row first and compute N — don't guess.
   # CAUSAL CONTROL: the container may already hold this theme from a prior run. First select "2. Dark mode",
   # confirm settings.json reads "dark", THEN re-open /theme and select the plugin theme — now the flip is YOURS.
   # send `Down` N times to the plugin theme, then `Enter` to apply
   ```
   Proof (note: **user** scope, not project):
   ```bash
   docker exec qa-claude bash -lc 'grep -i theme ~/.claude/settings.json'
   # → "theme": "custom:dgxsparklabs-theme-example-multi:lab-notebook"
   ```
   Full detail: cell 4.8.10.

9. **lsp** — diagnostics on edit. The full two-pane walkthrough (with the input log tail) is cell 4.8.7. Quick version: `printf 'def add(a,b):\n    return a+b\n\nprint(undefined_var)\n' > calc.py` in the scratch dir, ask Claude to *edit* it (a Read won't attach the LSP), then ask "List verbatim the language-server diagnostics for calc.py." Expect `undefined name 'undefined_var' (example-lsp)` plus the always-on `example-lsp marker` line.

**Part C — teardown** (this is the quick *per-session* reset — close the Claude session, the extra pane, and the scratch/log files. To also **uninstall the plugins** from the marketplace, run the full cleanup block in 4.10):
```bash
MSYS_NO_PATHCONV=1 docker exec qa-claude tmux send-keys -t 0:0.0 -l '/exit'
docker exec qa-claude tmux send-keys -t 0:0.0 Enter
docker exec qa-claude tmux kill-pane -t 0:0.1     # close the right pane (ignore error if you never used it)
docker exec qa-claude bash -lc 'rm -rf /workspace/lsptest /tmp/hook-fired-*.log /tmp/mcp_proxy_*.log'
```

#### 4.8.1 Skill — `skill-example-multi`

*(a `skill-example-single` sibling — one solo `hello` skill — is covered in the reference card above)*

- [ ] **Install** (run in host shell or container shell):
  ```bash
  claude plugin install skill-example-multi@dgxsparklabs-marketplace --scope project
  ```
- [ ] **Enable** (on CLI ≥2.1.157 install already enabled the plugin, so this prints `already enabled` — that is PASS, not failure):
  ```bash
  claude plugin enable skill-example-multi@dgxsparklabs-marketplace
  ```
- [ ] **Verify in `/plugins`**: row labeled `skill-example-multi@dgxsparklabs-marketplace`, status `✔ enabled`. (Enablement is project-scoped — `/plugins` and `claude plugin list` show `✔ enabled` only when run from the project dir you installed in; from elsewhere the same plugin reads `✘ disabled`, which is correct scope behavior.)
- [ ] **Invoke** (canonical namespaced form; type in an interactive `claude` session):
  ```text
  /dgxsparklabs-skill-example-multi:notebook weather
  ```
  The multi plugin ships two skills — `notebook` and `status`. Only the namespaced `/dgxsparklabs-skill-example-multi:<component>` form is verified to resolve; there is no bare flat form.
- [ ] **Expected visible output**: a markdown block formatted as a lab-notebook status entry — header with the topic, current UTC timestamp, and the skill's canned body text per `src/skills/example-multi/skills/notebook/SKILL.md`.
- [ ] **Slash-dropdown check**: typing `/dgxsparklabs-skill-example-multi:` triggers autocomplete. Note the **display quirk** confirmed live (below): the dropdown labels the rows by their **bare component name** (`/notebook`, `/status`) — not the full namespaced path the way commands do — each tagged `(dgxsparklabs-skill-example-multi)` with its frontmatter description. The verified-resolving invocation is still the full `/dgxsparklabs-skill-example-multi:<component>` form.

**▶ What you'll see in the session — verified live 2026-06-01 (see the provenance note under 4.8)**

Both skills were driven through a live interactive `claude` in tmux. Each runs `date -u …` for the timestamp (so you see a `Ran 1 shell command` line) and prints a fixed block matching its `SKILL.md`. Verbatim captures:

Each skill also prints a `[skill:<name>] args=[$ARGUMENTS]` debug line first (added in the 2026-06-01 debug-example sweep — re-verified live in a fresh session):

- **`/dgxsparklabs-skill-example-multi:notebook rookie-onboarding`** (the trailing text is the `$ARGUMENTS` topic):
  ```text
    Ran 1 shell command

  ● [skill:notebook] args=[rookie-onboarding]

    [Lab Notebook] Status update on "rookie-onboarding"
    - Time: 2026-06-01T20:22:45Z
    - Status: in-progress
    - Next checkpoint: Complete environment setup and run first build/test to confirm the toolchain works
  ```
- **`/dgxsparklabs-skill-example-multi:status`** (`df -h .` of the cwd + UTC stamp):
  ```text
  ● [skill:status] args=[]

    [Status] 2026-06-01T19:14:11Z
    Filesystem      Size  Used Avail Use% Mounted on
    overlay        1007G   12G  944G   2% /
  ```

**Autocomplete dropdown (live capture).** After typing `/dgxsparklabs-skill-example-multi:`:
```text
  /status                                  (dgxsparklabs-skill-example-multi) Prints disk usage of the
                                           current working directory plus a UTC timestamp. A second s…
  /notebook                                (dgxsparklabs-skill-example-multi) Echoes back a formatted
                                           lab-notebook-style status message. Shows how to write a SK…
```
The rows read as bare `/status` / `/notebook` (vs. commands, which list the full `/dgxsparklabs-command-…:hello`). The namespace is still shown in the parenthetical tag, and the full namespaced string is what was invoked and resolved.

**Reproduction (human, in the tmux Claude pane):** type the full `/dgxsparklabs-skill-example-multi:notebook <topic>` (or `:status`) and press Enter. The skill bodies are explicit, so Haiku shells out for the timestamp and prints the block with no clarifying question.

**Gotcha:** the invocation echoes as a normal `❯` prompt line and then `Ran 1 shell command` — there is **no** distinct "Skill: notebook" banner. The proof is the rendered block (and its `[Lab Notebook]` / `[Status]` sentinel text), not a skill-loaded announcement.

- [ ] **Failure signals**: (a) no `skill-example-multi` entry in `/plugins` → install path broken; (b) `/dgxsparklabs-skill-example-multi:notebook` returns "Unknown command" → src/ reorg didn't propagate or SKILL.md `name:` field changed; (c) slash resolves but body is empty → SKILL.md frontmatter parse error.
- [ ] **Diagnostic**:
  ```bash
  claude plugin details dgxsparklabs-skill-example-multi
  ls ~/.claude/plugins/cache/dgxsparklabs-marketplace/skill-example-multi/
  ```

#### 4.8.2 Rule — N/A for Claude (retired 2026-05-26)

- [ ] **No Claude plugin install path for rules.** Per `code.claude.com/docs/en/plugins-reference#plugin-components-reference` (fetched 2026-05-26), rules are not a Claude plugin component — they live in Claude's memory subsystem. There are 0 `rule-*` plugins in the Claude marketplace listing (confirmed — see Claude validation 8).
- [ ] **Manual install (filesystem)** — POSIX:
  ```bash
  mkdir -p .claude/rules
  cp src/rules/example/rule.md .claude/rules/example.md
  ```
  PowerShell:
  ```powershell
  New-Item -ItemType Directory -Force .claude/rules
  Copy-Item src/rules/example/rule.md .claude/rules/example.md
  ```
- [ ] **Verify**:
  ```bash
  diff src/rules/example/rule.md .claude/rules/example.md
  ```
- [ ] **Invoke**: rules are passive — no slash command. Start a `claude` session in the project; the rule's guidance becomes part of every system prompt.
- [ ] **Expected observable**: Claude's responses reflect the rule (e.g., the example rule's `When you are not sure, ask for confirmation` directive surfaces as cautious counterquestions in ambiguous cases).
- [ ] See Claude validation 8 below to confirm no `rule-*` plugins surface in Claude's marketplace listing post-deprecation.

#### 4.8.3 Sub-agent — `agent-example-multi`

*(invocation requires interactive Claude session — `/agents` is TUI-only; an `agent-example-single` sibling with the solo `notebook-reviewer` agent is in the reference card)*

- [ ] **Install**:
  ```bash
  claude plugin install agent-example-multi@dgxsparklabs-marketplace --scope project
  ```
- [ ] **Enable** (on CLI ≥2.1.157 install already enabled the plugin, so this prints `already enabled` — that is PASS, not failure):
  ```bash
  claude plugin enable agent-example-multi@dgxsparklabs-marketplace
  ```
- [ ] **Verify in `/plugins`**: row labeled `agent-example-multi@dgxsparklabs-marketplace`, status `✔ enabled`.
- [ ] **Invoke (interactive only)** — TTY picker, no headless equivalent per F7b. In a real `claude` session:
  ```text
  /agents
  ```
  Then select `dgxsparklabs-agent-example-multi:notebook-reviewer` from the picker. The multi plugin ships three agents — `notebook-reviewer`, `summarizer`, `validator`.
- [ ] **Expected**: `/agents` lists all three plugin agents under a **Plugin agents** group, namespaced `dgxsparklabs-agent-example-multi:<name>`. Dispatching one routes a task to that sub-agent's own context/toolset. Empirically captured live (below).

**▶ What you'll see in the session — verified live 2026-06-01 (see the provenance note under 4.8)**

The `/agents` picker is a TUI; the agents were both **listed** and one was **dispatched** to confirm it actually runs.

**1. The picker.** `/agents` (a bare slash — `MSYS_NO_PATHCONV=1` on Windows) opens on the **Running** tab, which shows `No subagents are currently running` — this is NOT a failure (a cold-read tester nearly flagged it as one, since it matches failure-signal (b)). Press **`Left` once** to switch to the **Agents** tab. There, all three plugin agents appear under *Plugin agents*, separate from the built-ins:
```text
   Agents  Running   Library

     Create new agent

     Plugin agents
     dgxsparklabs-agent-example-multi:notebook-reviewer · inherit
     dgxsparklabs-agent-example-multi:summarizer · inherit
     dgxsparklabs-agent-example-multi:validator · inherit

     Built-in agents (always available)
     claude · inherit
     …
   ←/→ to switch · ↑/↓ to navigate · Enter to select · Esc to close
```

**2. A real dispatch.** Closing the picker (`Esc`) and prompting *"Use the dgxsparklabs-agent-example-multi:summarizer subagent to summarize the file demo-note.md. Do not ask questions."* produces a nested sub-agent task with its own tool calls, then a completion line:
```text
● dgxsparklabs-agent-example-multi:summarizer(Summarize demo-note.md)
  ⎿  Read(demo-note.md)
  ⎿  Done (1 tool use · 3.4k tokens · 9s)

● Here's the summary of demo-note.md:
  TL;DR
  A short note documenting a tmux-based verification session for marketplace constructs. …
```
The runtime signal is the **namespaced task header** `dgxsparklabs-agent-example-multi:summarizer(…)` and the `Done (N tool use · … · Ns)` line — proof the sub-agent ran in its own context, not the main loop. While it runs, the bottom status tracker shows a second row (`◯ dgxsparklabs-agent-exam…  Summarize demo-note.md  7s`).

**Debug-example note — the `[agent-input]` echo is the WEAKEST debug channel; do not rely on it.** As of the 2026-06-01 sweep each agent's prompt asks it to begin its reply by quoting, verbatim, the task it was handed (a `[agent-input]` echo). **But this is model-compliance-dependent and frequently does not happen** — a cold-read tester on 2026-06-02 found the summarizer skipped the echo entirely and jumped straight to its `## TL;DR`. Two corrections to earlier wording:
> - **`ctrl+o` is a global "show detailed transcript" toggle, NOT a per-block expand.** Sending `docker exec qa-claude tmux send-keys -t 0:0.0 C-o` re-renders the *whole* transcript verbosely; it does not "open" just the sub-agent's collapsed block. The footer confirms it: `Showing detailed transcript · ctrl+o to toggle`.
> - **You may see no `[agent-input]` at all** — when the model skips it there is nothing to find, collapsed or expanded. Do not hunt for it as a pass criterion.
>
> The reliable, model-independent proof of the sub-agent construct remains the **namespaced task header** (`dgxsparklabs-agent-example-multi:summarizer(…)`) plus the **`Done (N tool use · … · Ns)`** line — those always appear and show it ran in its own context. Treat `[agent-input]` as a nice-to-have, not a verification gate. (Unlike hooks/MCP, a model-based construct can only *echo* its input into its own output, which it may decline to do — there is no file to fall back on.)

**Gotcha — Windows MSYS path mangling eats bare slash commands.** Sending `/agents` to tmux through a Windows (Git-Bash/MSYS) shell rewrites the argument to `C:/Program Files/Git/agents`, so the session receives a **path**, not the slash command (it then asks "what should I do with this path?"). Namespaced slashes like `/dgxsparklabs-command-…:hello` survive because the `:` makes MSYS treat the string as a path-list and skip conversion; a bare `/word` does not. **Fix:** prefix the send-keys command with `MSYS_NO_PATHCONV=1` (or drive tmux from PowerShell, which doesn't convert). This applies to every bare-slash TUI construct: `/agents`, `/mcp`, `/output-style`, `/theme`. See `PITFALLS.md`.

- [ ] **Failure signals**: (a) no `agent-example-multi` entry in `/plugins` → install path broken; (b) `/agents` picker has no *Plugin agents* group → agent loader broken or frontmatter `name:` mismatch; (c) dispatch succeeds but no namespaced task header / `Done` line → sub-agent context not switching (regression of PR #5 fixes).
- [ ] **Diagnostic**:
  ```bash
  claude plugin details dgxsparklabs-agent-example-multi | grep -F notebook-reviewer
  ```

#### 4.8.4 Command — `command-example-multi`

*(a `command-example-single` sibling with the solo `hello` command is in the reference card)*

- [ ] **Install**:
  ```bash
  claude plugin install command-example-multi@dgxsparklabs-marketplace --scope project
  ```
- [ ] **Enable** (on CLI ≥2.1.157 install already enabled the plugin, so this prints `already enabled` — that is PASS, not failure):
  ```bash
  claude plugin enable command-example-multi@dgxsparklabs-marketplace
  ```
- [ ] **Verify in `/plugins`**: row labeled `command-example-multi@dgxsparklabs-marketplace`, status `✔ enabled`.
- [ ] **Invoke** (in any `claude` session — works in `--print` too). The multi plugin ships three commands — `hello`, `goodbye`, `ping`:
  ```text
  /dgxsparklabs-command-example-multi:hello
  ```
- [ ] **Expected visible output**: Claude runs the command's one `date` shell-out (the session shows a `Ran 1 shell command` line) and prints a markdown block. The exact shape comes from `src/commands/example-multi/commands/hello.md` — substitute today's UTC date for `<DATE>`:
  ```markdown
  # Lab Notebook — <DATE>

  ## Entries

  - [ ] (add entries here)
  ```

**▶ What you'll see in the session — verified live 2026-06-01 (see the provenance note under 4.8)**

All three commands in this plugin were driven through a live interactive `claude` in tmux. Each is a tiny prompt that runs `date -u …` once (hence the `Ran 1 shell command` line), prints a `[command:<name>] args=[$ARGUMENTS]` debug line (added in the 2026-06-01 debug-example sweep — re-verified live), then a fixed block. Verbatim captures:

- **`/dgxsparklabs-command-example-multi:hello`**
  ```text
    Ran 1 shell command

  ● [command:hello] args=[]

    # Lab Notebook — 2026-06-01

    ## Entries

    - [ ] (add entries here)
  ```
- **`/dgxsparklabs-command-example-multi:ping extra-args-here`** (the trailing text is `$ARGUMENTS`)
  ```text
    Ran 1 shell command

  ● [command:ping] args=[extra-args-here]

    pong @ 2026-06-01T20:05:04Z
  ```
- **`/dgxsparklabs-command-example-multi:goodbye`**
  ```text
    Ran 1 shell command

  ● [command:goodbye] args=[]

    ---
    **Session closed at 2026-06-01T19:10:06Z**

    Next checkpoint: (set one)
  ```

**Autocomplete dropdown (the live slash-dropdown check).** Typing `/dgxsparklabs-command-example-multi:` (no Enter) renders a picker; the captured frame:
```text
  /dgxsparklabs-command-example-multi:he…  (dgxsparklabs-command-example-multi) Prints a formatted
                                           lab-notebook header for today's UTC date.
  /dgxsparklabs-command-example-multi:go…  (dgxsparklabs-command-example-multi) Prints a formatted
                                           lab-notebook closing footer with a UTC timestamp.
```
Each row is tagged with the plugin's own namespace `(dgxsparklabs-command-example-multi)` — confirming the per-plugin (not shared) namespace model.

**Reproduction (human, in the tmux Claude pane):** type each slash string and press Enter. Because the command bodies are explicit ("print this exact block"), Haiku runs the `date` shell-out and prints the block with no clarifying question.

**Gotchas observed:**
- **Ghost-suggestion Enter trap.** After running one command, Claude Code may show the *previous* slash string as a dimmed autosuggestion in an otherwise-empty input. Pressing Enter on that ghost does **nothing** (it is not committed input). Fix: clear the line (`Ctrl+U`) and *type* the next command fresh so it becomes real input, then Enter. (Driving via tmux: `send-keys C-u`, then `send-keys -l '<slash>'`, then a separate `send-keys Enter`.)
- **Enable scope.** `claude plugin enable command-example-multi@dgxsparklabs-marketplace` (run for back-compat) reports `scope: user` even though the original install was `--scope project`. Harmless here — the command resolves either way — but don't be surprised by the scope mismatch in the message.
- **Don't trust the model's prose as proof.** The signal is the rendered block above (and the `Ran 1 shell command` line), not Claude saying it ran — a chat reply alone is not verification.

- [ ] **Slash-dropdown check**: typing `/dgxsparklabs-command-example-multi:` triggers autocomplete; you should see `/dgxsparklabs-command-example-multi:hello` (and `:goodbye`, `:ping`) with description "Prints a formatted lab-notebook header for today's UTC date." Only the namespaced form is verified to resolve — a hermetic run captured `<command-name>/dgxsparklabs-command-example-multi:hello</command-name>` in the request body. There is no bare flat form. (Live dropdown capture in the **▶ What you'll see** block above.)
- [ ] **Failure signals**: (a) no `command-example-multi` entry in `/plugins` → install broken; (b) `/dgxsparklabs-command-example-multi:hello` returns "Unknown command" → src/ reorg didn't propagate, OR a command file rename didn't propagate; (c) command runs but output is wrong shape → command file edited locally — re-check against `src/commands/example-multi/commands/hello.md`.

#### 4.8.5 Hook — `hook-example-multi`

*(covers all 9 events in one plugin; there are also 9 single-event plugins `hook-example-<event>` in the reference card, one per event)*

- [ ] **Install**:
  ```bash
  claude plugin install hook-example-multi@dgxsparklabs-marketplace --scope project
  ```
- [ ] **Enable** (on CLI ≥2.1.157 install already enabled the plugin, so this prints `already enabled` — that is PASS, not failure):
  ```bash
  claude plugin enable hook-example-multi@dgxsparklabs-marketplace
  ```
- [ ] **Verify in `/plugins`**: row labeled `hook-example-multi@dgxsparklabs-marketplace`, status `✔ enabled`.
- [ ] **Invoke**: hooks are passive — they fire on Claude events. Per `src/hooks/example-multi/hooks/hooks.json`, all 9 events have handlers, each writing a `/tmp/hook-fired-<event>.log` sentinel:
  - `userpromptsubmit`: type any prompt and press Enter.
  - `sessionstart`: open a fresh `claude` session.
  - `pretooluse` / `posttooluse`: type `edit README.md and add a blank line at the bottom` — both fire on the resulting `Write`/`Edit` tool call (matcher is `Write|Edit`).
  - `stop`: send the response that completes a turn.
  - `subagentstop`: complete a sub-agent turn.
  - `sessionend`: type `/exit` or press `Ctrl+D`.
  - `notification`: trigger a Claude notification (e.g. a permission prompt).
  - `precompact`: trigger a context compaction.
- [ ] **Check sentinels** (run in a separate shell) — POSIX:
  ```bash
  ls /tmp/hook-fired-*.log
  ```
  PowerShell on Windows:
  ```powershell
  Get-ChildItem $env:TEMP\hook-fired-*.log
  ```
  Expect one file per event triggered (e.g. `/tmp/hook-fired-sessionstart.log`, `/tmp/hook-fired-userpromptsubmit.log`, …, `/tmp/hook-fired-precompact.log`). Note the order in the filename is `hook-fired-<event>`.

**▶ What you'll see in the session — verified live 2026-06-01, all 9 events (see the provenance note under 4.8)**

Hooks produce **no chat output** — the proof is the sentinel files, not anything Claude says. Starting from a cleared `/tmp` (`rm -f /tmp/hook-fired-*.log`), a single short run fired all nine. The sequence that triggers everything:

1. **Restart `claude`** → fires `SessionStart`.
2. **Submit an edit prompt** — verbatim: *"Use the Edit tool to append the line # hook-test as the last line of clean.py. Do not ask questions, just make the edit."* and **approve the permission dialog** → fires `UserPromptSubmit`, `PreToolUse`, then the permission prompt itself fires `Notification`, then `PostToolUse`, `Stop`, and `SubagentStop`.
3. **Run `/compact`** → fires `PreCompact` (and re-fires `SessionStart`/`SubagentStop` as the session re-primes).
4. **Type `/exit`** → fires `SessionEnd`.

`ls /tmp/hook-fired-*.log` shows 9 files = 9 events. **These are debug-grade hooks: each sentinel now contains a timestamped marker line FOLLOWED BY the full JSON payload Claude sent that event** (read from stdin via `p="$(cat)"`). Verified live 2026-06-01 with the updated plugin — e.g. `cat /tmp/hook-fired-sessionstart.log`:
```text
2026-06-01T20:01:20Z sessionStart fired
{"session_id":"daf177ea-…","transcript_path":"…/daf177ea….jsonl","cwd":"/workspace/lsptest","hook_event_name":"SessionStart","source":"startup","model":"claude-opus-4-8[1m]"}
```
and `cat /tmp/hook-fired-pretooluse.log` after an edit (note the real `tool_name` and full `tool_input` — the thing the old env-var version could not see):
```text
2026-06-01T20:01:56Z preToolUse fired
{"session_id":"daf177ea-…","cwd":"/workspace/lsptest","permission_mode":"default","hook_event_name":"PreToolUse","tool_name":"Edit","tool_input":{"file_path":"/workspace/lsptest/clean.py","old_string":"# hook-test","new_string":"# hook-test\n# debug-test","replace_all":false},"tool_use_id":"toolu_01Wst…"}
```
The `UserPromptSubmit` handler additionally injects `[Lab Notebook context: timestamp=…]` into the prompt (stdout), separate from the file log.

**Gotchas observed live:**
- **Read the payload from stdin, NOT `${CLAUDE_TOOL_NAME}`.** An earlier version of this example read `${CLAUDE_TOOL_NAME:-unknown}` from the environment and always logged `unknown` — CLI 2.1.159 does not populate that env var. The fix (now shipped): `p="$(cat)"` captures the hook's stdin JSON, which carries `tool_name`, `tool_input`, `cwd`, `session_id`, etc. If you write your own hook and see `unknown`/empty where a tool name should be, you're reading the env instead of stdin.
- **`Notification` fires from the edit-permission prompt.** You don't need a special action to exercise it — any approval dialog counts.
- **`/compact` re-fires `SessionStart`** (and `SubagentStop`); you'll see a second timestamped line appended to those sentinels. Multiple firings are expected — sentinels append, they don't overwrite.
- **Exit with `/exit`, not Ctrl+C, to fire `SessionEnd` reliably.** In this tmux/CLI combo a double `Ctrl+C` did **not** terminate the session (the pane stayed on `claude`); `/exit` + Enter did, and only then did `hook-fired-sessionend.log` appear. (Both `/compact` and `/exit` are bare-slash commands — when driving via tmux from Windows, send them with `MSYS_NO_PATHCONV=1`; see the sub-agent cell's gotcha and `PITFALLS.md`.)

- [ ] **Failure signals**: (a) sentinel file missing for a triggered event → that hook didn't fire; (b) sentinel has the marker line but no JSON payload after it → the handler isn't reading stdin (`p="$(cat)"`) — it may be reading a `CLAUDE_TOOL_NAME` env var that isn't populated; (c) `pretooluse`/`posttooluse` payload shows no `tool_name` → wrong event matcher or a malformed payload.
- [ ] For the headless/no-auth reproduction of each event, see the alternative-path cells 4.9.5–4.9.10 (kept for CI; 4.8.5 here is authoritative for shipped behavior).

#### 4.8.6 MCP server — `mcp-example-multi`

*(connection check and tool-call verification both require interactive Claude session; an `mcp-example-single` sibling with the solo `example` server is in the reference card)*

- [ ] **Prerequisite**: `uv` must be installed and on PATH (the dev container has it; manual setups need to install). POSIX:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
  PowerShell:
  ```powershell
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- [ ] **Install**:
  ```bash
  claude plugin install mcp-example-multi@dgxsparklabs-marketplace --scope project
  ```
- [ ] **Enable** (on CLI ≥2.1.157 install already enabled the plugin, so this prints `already enabled` — that is PASS, not failure):
  ```bash
  claude plugin enable mcp-example-multi@dgxsparklabs-marketplace
  ```
- [ ] **Verify in `/plugins`**: row labeled `mcp-example-multi@dgxsparklabs-marketplace`, status `✔ enabled`.
- [ ] **Verify in `/mcp` (interactive only)**: in a real `claude` session type:
  ```text
  /mcp
  ```
  The multi plugin ships three servers — keys `fetch`, `filesystem`, `sequential-thinking` (per `src/mcp-servers/example-multi/mcp-config.json`). The `fetch` server should appear with status `✓ Connected` (assuming `uv` present). If `uv` is missing, you'll see `plugin:dgxsparklabs-mcp-example-multi:fetch: uvx mcp-server-fetch - ✗ Failed to connect`. `npx`-backed servers (`filesystem`, `sequential-thinking`) need Node on PATH. `/mcp` is a TUI command; it cannot be exercised under `claude --print`.
- [ ] **Exercise the tool (interactive)**: tools are model-called, not user-typed. Ask Claude:
  ```text
  fetch https://example.com and summarize the contents
  ```
  Watch the tool name in `claude --debug` output.
- [ ] **Expected tool name**: `mcp__dgxsparklabs-mcp-example-multi__fetch__fetch` (hook-matcher form) or `plugin:dgxsparklabs-mcp-example-multi:fetch` (CLI display form).

**▶ What you'll see in the session — verified live 2026-06-01 (see the provenance note under 4.8)**

**1. `/mcp` connection status.** After a session restart (give servers ~10s to download/spawn on first run), `/mcp` lists all three plugin servers, namespaced `plugin:dgxsparklabs-mcp-example-multi:<key>`:
```text
   Manage MCP servers
   3 servers

     Built-in MCPs (always available)
   ❯ plugin:dgxsparklabs-mcp-example-multi:fetch · ✔ connected · 1 tool
     plugin:dgxsparklabs-mcp-example-multi:filesystem · ✘ failed
     plugin:dgxsparklabs-mcp-example-multi:sequential-thinking · ✔ connected · 1 tool
```
`fetch` (uvx) and `sequential-thinking` (npx) connect; **`filesystem` fails in this image** — see the gotcha below. 2 of 3 connecting is enough to prove the construct loads and spawns servers; the failure is upstream, not a plugin-config defect.

**2. A real tool call.** Tools are *model-called*, not user-typed. Prompting *"Use the fetch MCP tool … to retrieve https://example.com and show me just the page title. Do not ask questions."* triggers a tool-permission dialog naming the server's own tool ("Fetches a URL from the internet…"); approve it, and:
```text
❯ Use the fetch MCP tool … to retrieve https://example.com and show me just the page title.

  Called plugin:dgxsparklabs-mcp-example-multi:fetch

● The page title is: Example Domain
```
The runtime signal is the `Called plugin:dgxsparklabs-mcp-example-multi:fetch` line (the CLI display form of the tool) plus a correct result — proof the MCP server actually executed, not that Claude described fetching.

**Second observation channel — the JSON-RPC proxy log (debug-grade example).** Each server in this plugin runs behind the bundled `mcp_logging_proxy.py`, which tees the wire traffic to `/tmp/mcp_proxy_<server>.log`. Tail it (`tail -f /tmp/mcp_proxy_fetch.log`) to watch the entire exchange — verified live 2026-06-01:
```text
[fetch] ## proxy start -> uvx mcp-server-fetch
[fetch] -> {"method":"initialize","params":{"protocolVersion":"2025-11-25",…,"clientInfo":{"name":"claude-code","version":"2.1.159",…}},"jsonrpc":"2.0","id":0}
[fetch] <- {"jsonrpc":"2.0","id":0,"result":{…,"serverInfo":{"name":"mcp-fetch","version":"1.27.2"}}}
[fetch] -> {"method":"tools/list","jsonrpc":"2.0","id":1}
[fetch] <- {"jsonrpc":"2.0","id":1,"result":{"tools":[{"name":"fetch",…}]}}
[fetch] -> {"method":"tools/call","params":{"name":"fetch","arguments":{"url":"https://example.com"},…},"id":3}
[fetch] <- {"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"Contents of https://example.com/:…"}],"isError":false}}
```
`->` is client→server, `<-` is server→client. This is the MCP analog of the LSP input log: you see the `initialize` handshake, the advertised tool schemas, and every `tools/call` with its arguments and result — exactly what you need when debugging your own server. The proxy only forwards bytes, so it can't corrupt the protocol.

**Gotchas observed live:**
- **`filesystem` server fails: `ERR_MODULE_NOT_FOUND` for `zod`.** Running its command by hand — `npx -y @modelcontextprotocol/server-filesystem /tmp` — throws `Cannot find package '…/_npx/<hash>/node_modules/zod/index.js'`. This is an **upstream npx/packaging bug** in `@modelcontextprotocol/server-filesystem` (its `zod` dependency isn't resolved in the npx cache), unrelated to this plugin's `mcp-config.json`. `sequential-thinking` is also npx-based and connects fine, so it's package-specific, not a Node/npx/network problem. Workarounds: clear the npx cache (`rm -rf ~/.npm/_npx`) and retry, or pin a known-good server version in `mcp-config.json`.
- **First-run latency.** `uvx`/`npx` download the servers on first launch; `/mcp` may show a server as still-connecting for several seconds. The `fetch` call above took ~34s end-to-end on a cold cache. Re-check `/mcp` after a beat before calling it a failure.
- **`/mcp` is a bare-slash TUI command** — drive it through tmux with `MSYS_NO_PATHCONV=1` from Windows, and it returns an error under `claude --print`.

- [ ] **Failure signals**: (a) `/mcp` shows `✗ Failed to connect` with `uvx mcp-server-fetch` → `uv` not installed; (b) `/mcp` empty → server config not loaded — check `~/.claude/plugins/cache/dgxsparklabs-marketplace/mcp-example-multi/mcp-config.json` post-install; (c) tool invocation but model says "no fetch tool" → src/ reorg didn't propagate to MCP plugin; (d) `filesystem` shows `✘ failed` while others connect → the upstream `zod` resolution bug above, not your config.

#### 4.8.7 LSP server — `lsp-example-multi`

*(an `lsp-example-single` sibling points at an external `marksman` binary — the "real production server" reference. This multi plugin instead ships **two bundled, self-contained language servers** (`markdown` + `python`) that run `example_lsp.py` from inside the plugin — a real, dependency-free LSP (the Python side parses with the stdlib `ast`) providing **diagnostics, document symbols, go-to-definition, hover, and references**. No language toolchain to install, only `uv` on PATH.)*

> **There is no "LSP tab" in Claude Code 2.1.** LSP status is observable only via `claude --debug` (load + protocol events) and the `/plugin` Errors tab (launch failures). An LSP server is a child process Claude forks **lazily** when a matching file is opened/**edited**, using the **PATH of the shell that launched `claude`**. Claude auto-feeds `publishDiagnostics` to the model after each edit and reaches symbols / definition / hover / references through its **LSP tool**; it never calls `textDocument/formatting`.

- [ ] **Prerequisite — just `uv`** (the servers are bundled; no marksman/pyright/rust-analyzer to install). It must be on the PATH of the shell that launches `claude`:
  ```bash
  which uv || curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- [ ] **Install + enable** (auto-enables on CLI ≥2.1.157; a separate `enable` prints `already enabled` = PASS):
  ```bash
  claude plugin install lsp-example-multi@dgxsparklabs-marketplace --scope project
  ```
> **`--debug` is OPTIONAL and conflicts with the live walkthrough below — don't lead with it.** The two `--debug` steps in this checklist (this one and the watcher in Step 2) are a *secondary* way to see Claude's own load-time confirmation. But `claude --debug` **exits immediately in many headless containers** (see the walkthrough's traps), so a cold-read agent following this top-to-bottom hits a dead end. **The primary, reliable verification needs no `--debug`:** launch plain `claude`, edit a file, and read the two observability channels — the in-chat `(example-lsp)` diagnostic and the server's own log at `/tmp/example_lsp.log`. If you want the load-time confirmation anyway and `--debug` runs in your container, it prints the lines below; otherwise skip straight to "Invoke — EDIT the file".
- [ ] **(Optional) Verify the plugin LOADED the servers** — if `claude --debug` works in your container, read `~/.claude/debug/<session>.txt`. Expect:
  ```text
  Loaded 2 LSP server(s) from plugin: dgxsparklabs-lsp-example-multi
  Registered diagnostics handler for plugin:dgxsparklabs-lsp-example-multi:{markdown,python}
  LSP server manager initialized successfully
  ```
  Seeing these = the marketplace's LSP plugin is wired correctly. (If `--debug` exits immediately, skip this — the two channels below are the real pass.)
- [ ] **Invoke — EDIT the file, do NOT just read it.** Claude Code attaches the LSP (sends `textDocument/didOpen`) only when Claude **edits/writes** a file, never on a Read (CC docs: diagnostics fire "after each file edit"; see [anthropics/claude-code#16804](https://github.com/anthropics/claude-code/issues/16804)). **Step 1** — create the buggy file (shell):
  ```bash
  printf 'def add(a, b):\n    return a + b\n\nprint(undefined_var)\n' > calc.py   # 'undefined_var' is never defined
  ```
  **Step 2** — in a second shell, start the watcher (leave it running):
  ```bash
  tail -f ~/.claude/debug/<session>.txt | grep --line-buffered -iE 'lsp server|publishdiagnostics|received diagnostics'
  ```
  **Step 3** — in the `claude` session, type this prompt **exactly** (the explicit wording stops the model asking what to add):
  ```text
  Use the Edit tool to append the comment line # lsp test as the last line of calc.py. Do not ask questions, just make the edit.
  ```
  **Step 4** — accept the edit at the prompt: press Enter (selects `1. Yes`).
- [ ] **Expected (PASS)** — the watcher prints these (the server starts lazily on the first matching edit):
  ```text
  Starting LSP server instance: plugin:dgxsparklabs-lsp-example-multi:python
  [LSP PROTOCOL …:python] Received notification 'textDocument/publishDiagnostics'.
  Received diagnostics from plugin:…:python: 2 diagnostic(s) for file:///…/calc.py
  ```
  The `N diagnostic(s)` line (always ≥1 — the always-on marker guarantees it) is the proof. Diagnostics attach to the model's **next** turn — type this prompt **exactly** to surface it:
  ```text
  List verbatim the language-server diagnostics shown to you for calc.py, with line numbers.
  ```
  **Expected reply** (verified live 2026-06-01): this example ships with `--always-error`, so you get **two** diagnostics, both tagged `(example-lsp)` — a guaranteed marker (`example-lsp marker — file analyzed …`) **plus** the real finding `undefined name 'undefined_var'` on the `print(undefined_var)` line. The marker means `⎿ Found N new diagnostic issue` appears on **every** edit, even a clean file — so you can confirm the LSP fired without even needing a bug in the file.
- [ ] **Second observation channel — the input log.** The server also appends every LSP message it receives to a file. Tail it to watch the client→server wire traffic live (`initialize` → `didOpen` → `didChange` → `didSave`). **Note (verified live 2026-06-02, CLI 2.1.159):** the `didChange` is **full-sync** — `contentChanges` carries the **whole document** as `{"text": "…"}` with **no `range` key**, e.g. `[0004] textDocument/didChange {…,"contentChanges":[{"text":"x = 1\ny = 2\nz = 3\nw = 4\n"}]}`. Do not go hunting for an incremental `range` field — this CLI version does not send one. (The server's `apply_change()` still handles both forms defensively.):
  ```bash
  tail -f "${TMPDIR:-/tmp}/example_lsp.log"
  ```
  You'll see `initialize`, `textDocument/didOpen`, `textDocument/didChange`, … appended as they arrive — direct proof the server is being driven.
- [ ] **(Optional) navigation features** — type either prompt **exactly**:
  ```text
  Use the LSP to list the symbols defined in calc.py.
  ```
  ```text
  Use the LSP go-to-definition to tell me which line the function add is defined on.
  ```
  **Expected:** the symbols list includes `add`; the definition resolves to the `def add(a, b):` line. (The model calls its LSP tool, which `example_lsp` answers.)
- [ ] **Watch `Received diagnostics … N diagnostic(s)`, not `Checking registry - N pending`** — the `pending` counter is a brief pre-attach queue depth that almost always polls as `0` even on success. Because this example uses `--always-error`, every analyzed file yields ≥1 diagnostic — so `0 diagnostic(s)` / `Skipping empty diagnostics` means the server **didn't run at all** (check `uv`/PATH and the `/plugin` Errors tab), not that the file is clean.
- [ ] **⚠️ Two traps**: (a) a **Read won't trigger it** — only an Edit/Write does. (b) a capable model *describes* the bug from its own reading even when the LSP never ran — a chat reply is **not** proof. Trust the `Received diagnostics … N diagnostic(s)` debug line + the `example-lsp` source tag.
- [ ] **Failure signals**: no `Starting LSP server instance: …:python` after an edit → (a) `uv` not on the launch shell's PATH (`which uv`); (b) `/plugin` → `lsp-example-multi` → **Errors tab** shows a spawn error; (c) stale install — `claude plugin uninstall lsp-example-multi@dgxsparklabs-marketplace`, reinstall, `/reload-plugins`. If it starts but logs `0 diagnostic(s)`, drive `example_lsp.py` directly over stdio (`initialize` → `didOpen` → `didChange`) to isolate server vs. client. **The server must maintain its own document buffer regardless of sync mode:** on CLI 2.1.159 the observed `didChange` is full-document (no `range`), but earlier CLI versions sent incremental (range + fragment) — the original bug was a handler that assumed one shape. `apply_change()` handles both.

**▶ Full live walkthrough — watch the LSP work in a two-pane tmux**

This reproduces the whole thing end-to-end: you watch `example_lsp` work through **both** observability
channels at once — the **always-on marker** (in the Claude chat) and the **input log** (every LSP message
the server receives). Verified live 2026-06-01. Total time ~3 minutes.

> **Read this first — five things that WILL trip you, and the fix for each** (each one cost a debugging
> detour during the first run):
>
> 1. **`claude --debug` exits immediately** in some headless containers — it prints `Resume this session
>    with: claude --resume …` and quits. **Fix:** launch plain `claude`. You don't need `--debug` here;
>    the input log is the *server's* own log, not Claude's debug log, so both channels work without it.
> 2. **`~` / `cd ~/test` can point at a directory that doesn't exist** (fresh containers vary; one shell's
>    `$HOME` ≠ another's working dir). **Fix:** create and use an **absolute** path, e.g. `/workspace/lsptest`.
> 3. **First launch, Claude asks to *trust the folder*.** **Fix:** answer `1. Yes` (Enter) — nothing happens
>    until you do.
> 4. **The log file doesn't exist until the server first runs**, so `tail` errors with `cannot open … No
>    such file`. **Fix:** use `tail -F` (capital F) — it waits and auto-attaches when the first edit creates
>    the file.
> 5. **The diagnostic lands one message LATE.** After Claude edits a file you see `Done.` and *nothing* —
>    the diagnostic attaches to your **next** turn. **Fix:** send one more prompt; then it appears.

**Step 1 — two panes.** In the container, in tmux, split the window side-by-side: press **`Ctrl-b`** then
**`%`**. Left pane = Claude, right pane = the log watcher.

**Step 2 — RIGHT pane: follow the server's input log.**
```bash
tail -n0 -F "${TMPDIR:-/tmp}/example_lsp.log"
```
Expected: it prints `tail: cannot open … No such file or directory` and waits. That's correct — the server
hasn't started yet (gotcha #4).

**Step 3 — LEFT pane: prereqs, install, launch.** Use absolute paths (gotcha #2); `uv` must be on PATH.
```bash
which uv || curl -LsSf https://astral.sh/uv/install.sh | sh
mkdir -p /workspace/lsptest && cd /workspace/lsptest
claude plugin install lsp-example-multi@dgxsparklabs-marketplace --scope project   # auto-enables
printf 'x = 1\n' > clean.py                                                          # a file with NO bug
claude                                                                               # plain claude, NOT --debug (gotcha #1)
```
Answer **`1. Yes`** to "trust this folder" (gotcha #3).

**Step 4 — edit the clean file.** In Claude, type this prompt **exactly**:
```text
Use the Edit tool to append the comment line # ping as the last line of clean.py. Do not ask questions, just make the edit.
```
Accept the edit (Enter / `1. Yes`). **Watch the RIGHT pane** — the log now fills with live wire traffic:
```text
=== example_lsp started (lang=python, always_error=True, pid=…) ===
[0001] initialize             {… "name": "Claude Code", "version": "2.1.x" …}
[0002] initialized            {}
[0003] textDocument/didOpen   {… "uri": ".../clean.py", "text": "x = 1\n# ping\n"}
```
That is **Channel 2**: you are watching Claude Code talk to your language server.

**Step 5 — surface the always-on marker (Channel 1).** Send one more message (gotcha #5) — type **exactly**:
```text
List verbatim the language-server diagnostics shown to you for clean.py, with line numbers.
```
**Expected** — even though `clean.py` has no bug:
```text
⎿  Found 1 new diagnostic issue in 1 file (ctrl+o to expand)
⚠ [Line 1:1] example-lsp marker — file analyzed (always-on; event #N) (example-lsp)
```
The `(example-lsp)` source tag = it came from your server, not the model guessing. The marker appears on
*every* file, so you always get visible proof the LSP ran — no bug required.

**Step 6 (optional) — a second edit shows `didChange`/`didSave`.** Type `Append the line # pong to clean.py
using the Edit tool.` and watch the RIGHT pane add `[0004] textDocument/didChange …` and `[0005]
textDocument/didSave …`. (This is the message family whose mishandling caused the historical
incremental-`didChange` bug — now you can see its exact shape on the wire.)

**Result:** two independent pulses confirm the server is alive — a marker in the chat (Channel 1) and every
message in the log (Channel 2). Edit any `.py`/`.md` through Claude and both react.

**▶ Driving this through tmux as an automated agent — exact mechanics**

*The generic docker + tmux mechanics — finding the container, pane addressing, the `-l`-then-`Enter` rule, `capture-pane`, the sleep discipline, answering dialogs, and the Windows `MSYS_NO_PATHCONV=1` slash gotcha — are taught once in **4.8.0 Part 0**. Read that first if you have not. This section adds only the two things that are **LSP-specific**: the second pane tailing the server's input log, and the fact that an LSP diagnostic attaches one turn late. Replace `qa-claude` with the real container name.*

**1. LSP-specific setup — a second pane tailing the server's input log.** Split the window and start the tail in the right pane (`0:0.1`):
```bash
docker exec qa-claude tmux split-window -h -t 0:0                                    # right pane becomes 0:0.1
docker exec qa-claude tmux send-keys -t 0:0.1 -l 'tail -n0 -F /tmp/example_lsp.log'  # the server's OWN input log
docker exec qa-claude tmux send-keys -t 0:0.1 Enter
```
Use `tail -F` (capital F): the log file does not exist until the server first runs, and `-F` waits and auto-attaches when the first edit creates it. Launch `claude` in the left pane (`0:0.0`) exactly as in 4.8.0 Part A step 6.

**2. The canonical one-cycle loop** (edit → accept → one more message → observe both panes):
```bash
docker exec qa-claude tmux send-keys -t 0:0.0 -l 'Use the Edit tool to append the comment line # ping as the last line of clean.py. Do not ask questions, just make the edit.'
docker exec qa-claude tmux send-keys -t 0:0.0 Enter
sleep 9
docker exec qa-claude tmux capture-pane -t 0:0.0 -p | tail -8     # expect the "Do you want to make this edit?" dialog
docker exec qa-claude tmux send-keys -t 0:0.0 Enter               # accept the edit
sleep 8
docker exec qa-claude tmux send-keys -t 0:0.0 -l 'List verbatim the language-server diagnostics shown to you for clean.py, with line numbers.'
docker exec qa-claude tmux send-keys -t 0:0.0 Enter              # the diagnostic attaches to THIS (next) turn
sleep 22
docker exec qa-claude tmux capture-pane -t 0:0.0 -p | tail -12    # LEFT: expect "… example-lsp marker … (example-lsp)"
docker exec qa-claude tmux capture-pane -t 0:0.1 -p | tail -8     # RIGHT: expect the [0001] initialize … [0003] didOpen log
```

**3. Remaining LSP-specific agent traps.**
- A follow-up prompt **won't submit while the model is busy** — if a spinner like `✻ Brewed for 7s` is showing, your `Enter` is ignored. Wait until idle, then send.
- The input box shows grey **ghost-suggestion** text that is NOT what you typed; if unsure, send `C-u` (clear line) before typing.
- **Do not drive with `claude --debug`** — it can exit immediately in headless containers. Plain `claude` stays interactive; you don't need `--debug` (the input log is the *server's* log).
- After `pkill -f claude` to restart, the pane drops to `bash`; relaunch `claude` with `send-keys` and `sleep` before reading.

#### 4.8.8 Monitor — `monitor-example-multi`

*(a `monitor-example-single` sibling with the solo `disk-usage` monitor is in the reference card)*

- [ ] **Install**:
  ```bash
  claude plugin install monitor-example-multi@dgxsparklabs-marketplace --scope project
  ```
- [ ] **Enable** (on CLI ≥2.1.157 install already enabled the plugin, so this prints `already enabled` — that is PASS, not failure):
  ```bash
  claude plugin enable monitor-example-multi@dgxsparklabs-marketplace
  ```
- [ ] **Verify in `/plugins`**: row labeled `monitor-example-multi@dgxsparklabs-marketplace`, status `✔ enabled`.
- [ ] **Verify in `/plugin` Monitors tab (interactive)**: three monitors listed — `disk-usage`, `memory-usage`, `git-status`.
- [ ] **Invoke**: monitors are passive — `disk-usage` runs `df -h .` once at session start per `src/monitors/example-multi/monitors/monitors.json`. Start a fresh `claude` session.
- [ ] **Probe the monitor output** (interactive) — ask Claude:
  ```text
  what's our current disk usage?
  ```
- [ ] **Expected**: at session start, all three monitors run and their stdout is injected into the model's context as session-start observations (the model labels them "monitor events" with task IDs). Empirically captured live (below).

**▶ What you'll see in the session — verified live 2026-06-01 (see the provenance note under 4.8)**

**Monitors emit no monitor-authored chat line** — the command output is *injected into the model's context* at session start, not printed to the UI by the construct itself. **But beware the opposite surprise (cold-read tester, Opus 4.8):** a capable model often *spontaneously narrates* that injected context at boot — full `[monitor:*]` quotes plus a summary table and "everything looks healthy" — before you prompt anything. That boot narration is the model reading its context, and it already half-proves the construct fired; do not be thrown that a construct billed as "no visible output" fills the screen at launch. The clean, model-independent proof is still the recital probe below, and you must **forbid tool use** or the model will just run `df` itself (which would prove nothing). Verbatim probe (first prompt of a fresh session):
```text
Without running any tool or command, quote verbatim any session-start monitor or observation context you were given (disk usage, memory, git status). If you received none, say exactly: NO MONITOR CONTEXT.
```
The model's reply — all three monitors fired, each output prefixed with its `[monitor:<name>]` marker (the debug-example self-announce). Re-verified live 2026-06-01 in a freshly rebuilt session:
```text
● I received three session-start monitor observations. Quoted verbatim:

  [monitor:disk-usage]
  overlay        1007G   12G  944G   2% /

  [monitor:memory-usage]
  total        used        free      shared  buff/cache   available
  Mem:            15Gi       2.2Gi        11Gi       1.8Mi       2.4Gi        13Gi

  [monitor:git-status]
  not a git repo
```
`disk-usage` = `echo '[monitor:disk-usage]'; df -h . | tail -n +2`; `memory-usage` = `… free -h | head -2`; `git-status` = `… git status --short || echo 'not a git repo'` (correctly reporting `/workspace/lsptest` is not a git repo). The `[monitor:<name>]` prefix is what makes the silently-injected context identifiable — at session start you may also see the model narrate these unprompted (e.g. "Monitor … stream ended"), which is itself live proof they fired.

**Gotchas observed live:**
- **No chat surface, no `/plugin` "Monitors tab" was needed.** The construct is verified by the *recited context*, not by any panel. Don't expect a banner at session start.
- **Forbid tool use in the probe.** "What's our disk usage?" alone is **not** proof — a capable model just calls `Bash`/`df` and answers, whether or not the monitor ran. The `Without running any tool …` framing is what isolates the monitor's injected context. (This is the same "verify the real signal, not the prose" trap as elsewhere.)
- **`plugin.json` carries no `monitors` key**, yet the monitors load — the CLI auto-discovers `monitors/monitors.json`. So a "valid" install with an empty recital means the JSON didn't parse, not that the key is missing.

- [ ] **Failure signals**: (a) no `monitor-example-multi` entry in `/plugins` → install broken; (b) the recital returns `NO MONITOR CONTEXT` → monitor loader didn't run or `monitors.json` schema mismatch (regression of F3); (c) a monitor missing from the recital → rename/reorg didn't propagate post-regenerate.

#### 4.8.9 Output style — `output-style-example-multi`

*(invocation requires interactive Claude session via `/config` — there is **no** `/output-style` slash command in CLI 2.1.159 (see live findings below); an `output-style-example-single` sibling with just `Lab Notebook Voice` is in the reference card)*

- [ ] **Install**:
  ```bash
  claude plugin install output-style-example-multi@dgxsparklabs-marketplace --scope project
  ```
- [ ] **Enable** (on CLI ≥2.1.157 install already enabled the plugin, so this prints `already enabled` — that is PASS, not failure):
  ```bash
  claude plugin enable output-style-example-multi@dgxsparklabs-marketplace
  ```
- [ ] **Verify in `/plugins`**: row labeled `output-style-example-multi@dgxsparklabs-marketplace`, status `✔ enabled`.
- [ ] **Invoke (interactive only, via `/config`)** — in a real `claude` session, open the config panel and set the style:
  1. Type `/config` and Enter.
  2. Type `output style` to filter to the **Output style** row, Enter to select it.
  3. Press **Space** to open the style list, navigate with `↑/↓`, **Enter** to select. **The write to `settings.local.json` lands on THIS list-Enter** — you are then returned to the row (footer now reads `Enter to save · Esc to cancel`); that outer Enter/Esc only closes the panel and does **not** revert the change. So verify persistence right after the list-Enter, and don't worry that Esc would undo it (it won't). (A cold-read tester was unsure whether the change had committed at this exact step.)
  The plugin's three styles appear in that list, namespaced `dgxsparklabs-output-style-example-multi:<Name>` — `Lab Notebook Voice`, `Concise Engineer`, `Tutoring` — alongside the built-ins (`Default`, `Proactive`, `Explanatory`, `Learning`). **There is no `/output-style` slash command in CLI 2.1.159** (typing it shows "No commands match").
- [ ] **Verify persistence** — POSIX:
  ```bash
  cat .claude/settings.local.json
  ```
  PowerShell:
  ```powershell
  Get-Content .claude/settings.local.json
  ```
  Expect the **namespaced** value `"outputStyle": "dgxsparklabs-output-style-example-multi:Lab Notebook Voice"` (NOT the bare `"Lab Notebook Voice"` older docs implied).

**▶ What you'll see in the session — verified live 2026-06-01 (see the provenance note under 4.8)**

In this build, output styles are **not** a slash command — they're a setting under `/config`. `/output-style` / `/style` both return "No commands match". The flow and signals:

**1. The selector** (`/config` → filter `output style` → Enter → Space). The plugin styles are registered as items 5–7:
```text
   ❯ 1. Default ✔
     2. Proactive
     3. Explanatory
     4. Learning
     5. dgxsparklabs-output-style-example-multi:Concise Engineer   Terse, action-oriented engineering voice…
     6. dgxsparklabs-output-style-example-multi:Lab Notebook Voice Writes responses in a measured, citation-focused…
     7. dgxsparklabs-output-style-example-multi:Tutoring           Patient teaching voice…
   Enter to confirm · Esc to cancel
```

**2. The persistence signal (the proof).** Selecting #6 and confirming writes the namespaced id to the **project** settings file (`/workspace/lsptest/.claude/settings.local.json`):
```json
{
  "outputStyle": "dgxsparklabs-output-style-example-multi:Lab Notebook Voice"
}
```
and the `/config` row updates to `Output style → dgxsparklabs-output-style-example-multi:Lab Notebook…`. That settings write (captured immediately after selection) is the construct's real signal. Note the scope: output style lands in **project** `.claude/settings.local.json`, whereas theme lands in **user** `~/.claude/settings.json` (see 4.8.10) — and `settings.local.json` was observed reset to `{}` on a later unrelated restart, so treat the post-selection write as the proof, not long-term durability.

**3. Behavior change.** Subsequent replies adopt the style's voice (per `…/output-styles/lab-notebook-voice.md`). Note a *trivial* prompt won't showcase it — "what is 2+2" just returns "2 plus 2 equals 4." regardless. To see the voice, ask something substantive ("summarize what you just did") and look for measured, citation-focused prose.

**Gotchas observed live:**
- **No `/output-style` command exists** in 2.1.159 — use `/config`. Older docs (and the `--print` research log) referenced a `/output-style <name>` slash that this build does not have.
- **The persisted value is namespaced** (`dgxsparklabs-output-style-example-multi:Lab Notebook Voice`), not the bare frontmatter `name:`. A failure check expecting bare `"Lab Notebook Voice"` would false-negative.
- **Queued-slash trap.** If you fire `/config` while the model is mid-turn (e.g. still emitting the session-start monitor reports), it's *queued as literal text* and comes back as `Unknown command: /config`. Wait for an idle `❯` prompt before sending TUI slashes.
- **`/config` is a bare-slash TUI command** — drive via tmux with `MSYS_NO_PATHCONV=1` from Windows.
- **Failure signals**: (a) no `output-style-example-multi` in `/plugins` → install broken; (b) plugin styles absent from the `/config` list → frontmatter `name:` not exposed; (c) selection made but `settings.local.json` has no `outputStyle` → persistence broken.
- [ ] For the headless/no-auth reproduction, see the alternative-path cell 4.9.16 (this live cell is authoritative for the persisted value and the `/config` mechanics).

#### 4.8.10 Theme — `theme-example-multi`

*(invocation requires interactive Claude session — `/theme` returns `isn't available in this environment` in `--print`; a `theme-example-single` sibling with just `Lab Notebook` is in the reference card)*

- [ ] **Install**:
  ```bash
  claude plugin install theme-example-multi@dgxsparklabs-marketplace --scope project
  ```
- [ ] **Enable** (on CLI ≥2.1.157 install already enabled the plugin, so this prints `already enabled` — that is PASS, not failure):
  ```bash
  claude plugin enable theme-example-multi@dgxsparklabs-marketplace
  ```
- [ ] **Verify in `/plugins`**: row labeled `theme-example-multi@dgxsparklabs-marketplace`, status `✔ enabled`.
- [ ] **Invoke (interactive only)** — unlike output style, `/theme` **is** a real slash command in CLI 2.1.159 ("Change the theme"). In a real `claude` session type `/theme` (no argument) to open the picker, navigate with `↑/↓`, and `Enter` to apply. The multi plugin ships three themes — `Lab Notebook`, `Nord`, `Solarized Dark` — appearing in the picker tagged `(from dgxsparklabs-theme-example-multi)`. `/theme` returns `isn't available in this environment` under `claude --print`.
- [ ] **Expected visible output**: an immediate confirmation `⎿ Using custom theme "Lab Notebook"` and the terminal colors flip to the Lab Notebook palette — solarized-light-ish: background `#fdf6e3`, foreground `#586e75`, Claude messages `#268bd2`, errors `#dc322f`. No `/clear` needed.
- [ ] **Persistence check (format CONFIRMED 2026-06-01)**:
  ```bash
  grep -i theme ~/.claude/settings.json
  ```
  Expect (note theme persists to **user** scope, not project): `"theme": "custom:dgxsparklabs-theme-example-multi:lab-notebook"` — i.e. `custom:<plugin-name>:<theme-file-stem>`.

**▶ What you'll see in the session — verified live 2026-06-01 (see the provenance note under 4.8)**

`/theme` opens a picker (no argument needed). The three plugin themes appear as items 8–10, each tagged with the plugin, and a live code-preview pane shows the syntax colors:
```text
   Theme
   Choose the text style that looks best with your terminal

   ❯ 1.  Auto (match terminal) ✔
     2.  Dark mode
     …
     8.  Lab Notebook (from dgxsparklabs-theme-example-multi)
     9.  Nord (from dgxsparklabs-theme-example-multi)
     10. Solarized Dark (from dgxsparklabs-theme-example-multi)
     11. New custom theme…
   Enter to select · Esc to cancel
```
Selecting **8. Lab Notebook** and pressing Enter yields the confirmation line `⎿ Using custom theme "Lab Notebook"` and writes the theme id to **user** settings `~/.claude/settings.json`:
```json
"theme": "custom:dgxsparklabs-theme-example-multi:lab-notebook"
```
That settings write + the confirmation line are the verifiable signals (the literal background-color flip is real but doesn't survive a plain-text `capture-pane -p`, which strips ANSI — use `capture-pane -e` if you need to assert on color codes).

**Gotchas observed live:**
- **Theme has a slash command; output style does not.** `/theme` works directly; the analogous output-style setting is only reachable via `/config` (see 4.8.9). Don't assume symmetry between the two constructs.
- **Theme persists to user scope** (`~/.claude/settings.json`), not the project `settings.local.json` where output style lands. The persisted id is `custom:<plugin-name>:<theme-file-stem>` (`lab-notebook`, the JSON filename stem — not the human `name:` "Lab Notebook").
- **`/theme` is a bare-slash TUI command** — drive via tmux with `MSYS_NO_PATHCONV=1` from Windows; and wait for an idle `❯` (a queued `/theme` during the monitor-report turn comes back as unknown).
- **Visual assertion is the one thing tmux text-capture can't show.** The confirmation line and the settings write stand in for "eyes on screen"; for true color verification a human or `capture-pane -e` is required (this was historically the F4 interactive-only cell).
- **Failure signals**: (a) no `theme-example-multi` in `/plugins` → install broken; (b) the three themes absent from the `/theme` picker → theme JSON `name`/loader mismatch; (c) selection made but `~/.claude/settings.json` has no `custom:dgxsparklabs-theme-example-multi:*` theme → persistence broken.

### 4.9 Headless and hermetic alternative path (no-auth validations and the original refactor arcs)

> **This section is the ALTERNATIVE path, not the primary one.** The primary, recommended way to verify every construct is the **live interactive tmux** path in 4.8 (start at 4.8.0). Use this 4.9 section instead when you **cannot run an authenticated interactive session** — e.g. in CI, or with no API key — because it drives Claude headlessly (`claude --print`) against a local stub and checks request bodies / sentinel files. Several cells here are now **superseded by their live 4.8 counterpart** (noted inline with a pointer); they are kept because the headless reproduction is still useful for automation. Where a 4.9 cell and its 4.8 cell disagree on a detail, **4.8 is authoritative** (it reflects the current shipped behavior, including the 2026-06-01 debug-example sweep).

These validations trace to three landed arcs (findings F1–F9):

1. **Arc 1 (PR #6, 2026-05-26)** — 6 example-plugin bugs fixed (marketplace description, LSP/monitor/theme schemas, hook coverage, MCP uv prereq) + Claude rule emission retired. Source research: `docs/archive/claude-qa-2026-05-26/RESEARCH.md`.
2. **Arc 2 (PR #8, 2026-05-26)** — hermetic Claude stub at `tests/fixtures/claude-stub/` enables F5/F7/F9 to verify without auth; F4 (visual theme) still interactive-only. Source research: `docs/archive/claude-headless-qa-2026-05-26/RESEARCH.md`.
3. **Arc 3 (PR #10, 2026-05-26)** — mcp-example name alignment + Scheme B+ across all 9 other example plugins + 2 component renames. Source research: `docs/research/naming-conventions-2026-05-26/RESEARCH.md`.

Each cell is operator-runnable ("do X, observe Y"); the hermetic variant needs the stub from 4.5 running.

#### 4.9.1 Claude validation 1 — marketplace description (F1)

- [ ] **Action** — from the marketplace repo root:
  ```bash
  claude plugin validate ./
  ```
  (or add `--strict` if your CLI version supports the flag)
- [ ] **Expected**: exit code 0; output contains `Validation passed` (verified — 27 plugins total, 0 `rule-*` plugins); the previously-seen `description: No marketplace description provided` warning is GONE.
- [ ] **CI gate**: `.github/workflows/compat-validate.yml` runs this on every PR and fails the build if ANY warning or error appears.

#### 4.9.2 Claude validation 2 — lsp-example schema (F2)

- [ ] **Action** (`enable` prints `already enabled` on CLI ≥2.1.157 — that is PASS):
  ```bash
  claude plugin install lsp-example-multi@dgxsparklabs-marketplace --scope project
  claude plugin enable lsp-example-multi@dgxsparklabs-marketplace
  ```
  Then open or edit a `.md` file in a project with the plugin enabled.
- [ ] **Expected**: Claude surfaces `marksman` diagnostics (e.g., broken-link or heading warnings) inline; `/plugin` Errors tab shows no LSP errors. Pre-fix the `/plugin` Errors tab would show three validator errors complaining about `lspServers.command`, `lspServers.extensionToLanguage`, and `unrecognized_keys: ["example-markdown"]` (per F2 symptom block).

#### 4.9.3 Claude validation 3 — monitor-example shape (F3)

- [ ] **Action** (`enable` prints `already enabled` on CLI ≥2.1.157 — that is PASS):
  ```bash
  claude plugin install monitor-example-multi@dgxsparklabs-marketplace --scope project
  claude plugin enable monitor-example-multi@dgxsparklabs-marketplace
  claude
  ```
  Watch the bottom-status / notification panel during the first 30 seconds.
- [ ] **Expected**: a notification appears with the `df -h .` disk usage summary, sourced from the `disk-usage` monitor. Pre-fix `/plugin` Errors tab would show `Failed to load monitors ... expected array, received object`.

#### 4.9.4 Claude validation 4 — theme-example distinctiveness (F4)

- [ ] **Action** — install + enable (`enable` prints `already enabled` on CLI ≥2.1.157 — that is PASS):
  ```bash
  claude plugin install theme-example-multi@dgxsparklabs-marketplace --scope project
  claude plugin enable theme-example-multi@dgxsparklabs-marketplace
  ```
  Then in a `claude` session:
  ```text
  /theme
  ```
  Pick **Lab Notebook**, confirm with Enter.
- [ ] **Expected**: terminal visibly switches to a light/paper-toned palette (foreground darkens, background lightens). Compare to the default dark theme — the Lab Notebook entry should be obviously distinct.
- [ ] **Persistence check**:
  ```bash
  cat ~/.claude/settings.json | grep theme
  ```
  Should show `custom:theme-example-multi:lab-notebook` per `code.claude.com/docs/en/plugins-reference#themes` (operator confirms exact format — see F4 caveat above).

#### 4.9.5 Claude validation 5a — UserPromptSubmit hook firing (F5)

> **Applies to all six hook cells (4.9.5–4.9.10).** Since the 2026-06-01 debug-example sweep, each sentinel `/tmp/hook-fired-<event>.log` contains the timestamped marker line (`<ts> <event> fired`) **followed by the full JSON payload Claude sent that event** (read from stdin). The `test -s …` / `tail …` checks below assert on the marker line and still pass unchanged; for the payload schema and the live 9-event walkthrough, **4.8.5 is authoritative**. (The old `${CLAUDE_TOOL_NAME}` env-var approach was a bug — the tool name lives in the stdin JSON.)

- [ ] **Hermetic verification** (run the stub session above first; install `hook-example-multi`):
  ```bash
  rm -f /tmp/hook-fired-userpromptsubmit.log
  echo "say hello" | claude --print
  test -s /tmp/hook-fired-userpromptsubmit.log && echo PASS
  ```
- [ ] **Expected (hermetic)**: CONFIRMED 2026-05-30 against the stub — exit 0; the sentinel file exists and contains a `<UTC-ISO-timestamp> userPromptSubmit fired` line.
- [ ] **Interactive**: with `hook-example` installed + enabled, submit any prompt in a `claude` session. In another terminal:
  ```bash
  tail /tmp/hook-fired-userpromptsubmit.log
  ```
- [ ] **Expected**: a new line in the form `<UTC-ISO-timestamp> userPromptSubmit fired` (the hook command writes the sentinel). The injected `[Lab Notebook context: timestamp=...]` line goes into Claude's prompt context — not visible at the operator terminal by design; `claude --debug` reveals it.

#### 4.9.6 Claude validation 5b — SessionStart hook firing (F5)

- [ ] **Hermetic verification**:
  ```bash
  rm -f /tmp/hook-fired-sessionstart.log
  echo "say hello" | claude --print
  test -s /tmp/hook-fired-sessionstart.log && echo PASS
  ```
- [ ] **Expected (hermetic)**: CONFIRMED 2026-05-30 against the stub — exit 0; sentinel contains a `sessionStart fired` line. A fresh `claude --print` invocation is a fresh session, so SessionStart fires.
- [ ] **Interactive**: restart `claude` in the project (exit + re-enter, or open a new session). In another terminal:
  ```bash
  tail /tmp/hook-fired-sessionstart.log
  ```
- [ ] **Expected**: a new line with the session-start timestamp.

#### 4.9.7 Claude validation 5c — PreToolUse hook with matcher (F5)

- [ ] **Hermetic verification (partial)**: PreToolUse only fires when Claude returns a `tool_use` content block. The default `stub.py` returns text-only, so this hook does NOT fire under hermetic — extending the stub to emit a canned `Edit` tool_use block is future work. Use the interactive step for now.
- [ ] **Interactive** — in the session, type this prompt exactly:
  ```text
  edit README.md and add a blank line at the bottom
  ```
  In another terminal:
  ```bash
  tail /tmp/hook-fired-pretooluse.log
  ```
- [ ] **Expected**: a line like `<UTC-ISO-timestamp> preToolUse Edit` (or `preToolUse Write`). The matcher `Write|Edit` in `hooks.json` gates which tool calls trigger this hook.

#### 4.9.8 Claude validation 5d — PostToolUse hook firing (F5)

- [ ] **Hermetic verification (partial)**: same caveat as 5c — needs the stub to return a `tool_use` block. Use the interactive step.
- [ ] **Interactive**: same edit as 5c. After the tool call completes:
  ```bash
  tail /tmp/hook-fired-posttooluse.log
  ```
- [ ] **Expected**: mirror line right after the PreToolUse entry (`<ts> postToolUse Edit` or `postToolUse Write`).

#### 4.9.9 Claude validation 5e — Stop hook firing (F5)

- [ ] **Hermetic verification**:
  ```bash
  rm -f /tmp/hook-fired-stop.log
  echo "say hello" | claude --print
  test -s /tmp/hook-fired-stop.log && echo PASS
  ```
- [ ] **Expected (hermetic)**: CONFIRMED 2026-05-30 against the stub — exit 0; sentinel contains a `stop fired` line. Stop fires at the end of every assistant turn, including the single stub turn.
- [ ] **Interactive**: ask Claude any question and wait for the response to complete. Then:
  ```bash
  tail /tmp/hook-fired-stop.log
  ```
- [ ] **Expected**: a new line per assistant turn.

#### 4.9.10 Claude validation 5f — SessionEnd hook firing (F5)

- [ ] **Hermetic verification**:
  ```bash
  rm -f /tmp/hook-fired-sessionend.log
  echo "say hello" | claude --print
  test -s /tmp/hook-fired-sessionend.log && echo PASS
  ```
- [ ] **Expected (hermetic)**: CONFIRMED 2026-05-30 against the stub — exit 0; sentinel contains a `sessionEnd fired` line. `claude --print` exits the session after one turn, so SessionEnd fires.
- [ ] **Interactive**: exit the Claude session (`/exit` or `Ctrl+D`). Then in a separate shell:
  ```bash
  tail /tmp/hook-fired-sessionend.log
  ```
- [ ] **Expected**: a final line with the session-end timestamp.

#### 4.9.11 Claude validation 6 — mcp-example uv prerequisite (F6)

- [ ] **Action** — on a fresh host (no `uv` installed) (`enable` prints `already enabled` on CLI ≥2.1.157 — that is PASS):
  ```bash
  claude plugin install mcp-example-multi@dgxsparklabs-marketplace --scope project
  claude plugin enable mcp-example-multi@dgxsparklabs-marketplace
  claude
  ```
  Then in the session, type exactly: `fetch https://example.com and summarize the response`. Check `/plugin` Errors tab.
- [ ] **Pre-install-uv expected**: error in `/plugin` Errors tab — `plugin:dgxsparklabs-mcp-example-multi:fetch: uvx mcp-server-fetch - ✗ Failed to connect` (because `uvx` is not on PATH).
- [ ] **Then install uv** — POSIX:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
  PowerShell:
  ```powershell
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
  Restart the Claude session.
- [ ] **Post-install-uv expected**: `/plugin` shows `plugin:dgxsparklabs-mcp-example-multi:fetch: uvx mcp-server-fetch - ✓ Connected`. The fix is the README documenting this prereq (see `src/mcp-servers/example-multi/README.md`).

#### 4.9.12 Claude validation 7a — skill slash command namespacing (F7)

- [ ] **Hermetic verification** — with `command-example-multi` installed + enabled and the body-dumper stub running on port 8089:
  ```bash
  export ANTHROPIC_BASE_URL=http://127.0.0.1:8089
  echo "/dgxsparklabs-command-example-multi:hello" | claude --print
  grep -F "dgxsparklabs-command-example-multi:hello" /tmp/stub-bodies.log
  ```
- [ ] **Expected (hermetic)**: CONFIRMED 2026-05-30 — grep matches; the captured request body contained `<command-name>/dgxsparklabs-command-example-multi:hello</command-name>`, proving Claude resolved the per-plugin namespace client-side. (Skills resolve under the same `/dgxsparklabs-<plugin>:<component>` convention.)
- [ ] **Interactive**: with `skill-example-multi` installed, in a real `claude` session type:
  ```text
  /
  ```
  And read the autocomplete dropdown entry.
- [ ] **Expected**: the entry resolves to `/dgxsparklabs-skill-example-multi:notebook` (the UI may show a shorter label, but the actual invocation is the namespaced form). Per `code.claude.com/docs/en/plugins` (2026-05-26): *"Plugin skills are always namespaced (like `/my-first-plugin:hello`) to prevent conflicts..."* Only the per-plugin namespaced form is verified to resolve — there is no bare flat form.

#### 4.9.13 Claude validation 7b — agent namespacing (F7)

- [ ] **Hermetic verification (partial)**: `/agents` is an interactive TUI command — there is no headless equivalent. The 7a hermetic check exercises the same client-side resolver code path, so a green 7a is strong evidence the namespacing infrastructure works for agents too. Use the interactive step for the agent-specific surface.
- [ ] **Interactive**: with `agent-example-multi` installed + enabled, in a `claude` session type:
  ```text
  /agents
  ```
- [ ] **Expected**: the entry appears as `dgxsparklabs-agent-example-multi:notebook-reviewer` (no `/` prefix — the colon-namespaced form is what `/agents` displays).

#### 4.9.14 Claude validation 7c — MCP tool namespacing (F7)

- [ ] **Hermetic verification (partial)**: same as 7b — `mcp__*` tool names only appear once Claude returns a `tool_use` block; the default stub doesn't. Future work to extend the stub. Use the interactive step.
- [ ] **Interactive**: with `mcp-example-multi` installed + enabled, ask Claude:
  ```text
  fetch https://example.com
  ```
  Watch the tool name in `claude --debug` output.
- [ ] **Expected**: tool name appears as `mcp__dgxsparklabs-mcp-example-multi__fetch__fetch` (the hook-matcher form) or `plugin:dgxsparklabs-mcp-example-multi:fetch` (the CLI display form). Both are documented per `code.claude.com/docs/en/hooks` and `code.claude.com/docs/en/plugins-reference`.

#### 4.9.15 Claude validation 8 — rule deprecation (F8)

- [ ] **Action**:
  ```bash
  claude plugin list --available --json | jq '.available | map(.name) | map(select(startswith("rule-"))) | length'
  ```
- [ ] **Expected**: `0` — CONFIRMED 2026-05-30; no `rule-*` plugins are surfaced to Claude after the 2026-05-26 deprecation. Additionally, Claude-side bundle cascade: `bundle-quality-rules`, `bundle-workflow-rules`, `bundle-documentation-rules`, `bundle-environment-rules`, `bundle-notifications-rules`, and `bundle-rule-all` are also gone (their dependencies are no longer valid Claude plugins). They remain available to Cursor / Codex / Gemini / Windsurf.

#### 4.9.16 Claude validation 9 — output style applied (F9)
- [ ] **Hermetic verification** (use `stub_body_dumper.py` on port 8089, `ANTHROPIC_BASE_URL=http://127.0.0.1:8089`): with `output-style-example-multi` installed, the simplest injection path is `--append-system-prompt`:
  ```bash
  rm -f /tmp/stub-bodies.log
  claude --print --append-system-prompt "$(cat src/output-styles/example-multi/output-styles/lab-notebook-voice.md)" "explain F9"
  grep -F "Lab Notebook Voice" /tmp/stub-bodies.log
  grep -F "Next:" /tmp/stub-bodies.log
  ```
- [ ] **Expected (hermetic)**: both greps match — the output-style content reaches the `system[]` array of the captured request body verbatim, which is the proof the style would be applied if a real model were behind the stub. The persistence-vs-application distinction (`/config` selection vs `--append-system-prompt` injection) can be tested separately by setting `outputStyle` in settings and re-running.
- [ ] **Action (interactive)**: with `output-style-example-multi` installed, type `/config` in a `claude` session, navigate to **Output style**, pick "Lab Notebook Voice", and confirm.
- [ ] **Persistence check**: `cat .claude/settings.local.json | jq .outputStyle` returns the **namespaced** value `"dgxsparklabs-output-style-example-multi:Lab Notebook Voice"` (NOT the bare `"Lab Notebook Voice"`). See 4.8.9 — that live cell is authoritative for the `/config` mechanics and the persisted value.
- [ ] **Apply**: type `/clear` to force a fresh session that re-reads the system prompt.
- [ ] **Behavioral check**: ask Claude: *"Explain what the `_base_plugin_shape` function in `scripts/constructs.py` does."*
- [ ] **Expected response markers** (from the SKILL.md spec): plain factual sentences citing file paths and line numbers; no hedging language unless flagged as uncertainty; the response ends with one line tagged `Next:` proposing the immediate next checkable step. The `Next:` line is the cleanest binary signal — present means active, absent means not.
- [ ] **A/B compare**: in a separate clean session, set `outputStyle: "Default"`, ask the same question — observe no `Next:` line and more conversational tone.

### 4.10 Cleanup

This is the **full** cleanup: it uninstalls every plugin from the marketplace. For a quick *per-session* reset that only closes the session and removes scratch/log files (without uninstalling), use Part C of the rookie guide (4.8.0.1).

```bash
# Uninstall every individual plugin currently installed from this marketplace,
# whatever set you exercised (-single, -multi, per-event hooks, etc.):
for p in $(claude plugin list 2>/dev/null | grep -oE '[a-z-]+@dgxsparklabs-marketplace' | cut -d@ -f1 | sort -u); do
  claude plugin uninstall "$p" --scope project
done
claude plugin marketplace remove dgxsparklabs-marketplace
```

If hermetic (option A):
```powershell
docker rm -f qa-claude
```

---

## 5. Codex

**What we're verifying**: marketplace registration + per-construct install for the four constructs Codex supports per `CodexPlatform.supports` and `docs/PLATFORMS.md` Codex "What constructs it supports": **skill, mcp, hook, sub-agent**. Codex also reads rule context from `AGENTS.md` and the Cursor/Windsurf rule mirrors. **New in 2026-05-25**: sub-agent emission as `.codex/agents/<name>.toml` (markdown→TOML converter) AND Phase 5.5 emits `.agents/plugins/marketplace.json` as Codex's canonical marketplace path.

### 5.1 Setup option A — Docker (hermetic)

```powershell
docker run -it --name qa-codex node:20 bash
```

Inside the container (`node:20` has `git` pre-installed):
```bash
# Install Codex CLI
npm install -g @openai/codex
codex --version

# Clone the PR branch for testing PR #5:
git clone --branch main https://github.com/DgxSparkLabs/marketplace.git /workspace/marketplace
cd /workspace/marketplace

# (To test against main instead: --branch main or omit --branch.)
```

### 5.2 Setup option B — Native

```powershell
npm install -g @openai/codex
codex --version
```

### 5.3 Auth

```bash
codex auth login         # OpenAI account; opens browser
```

Marketplace registration and `codex plugin list` are auth-free; `codex plugin add` typically requires auth.

### 5.4 Marketplace registration

- [ ] Step 1: Register the marketplace. Pick ONE of:
  - **Remote `main`** (smoke test only — NOT for PR #5 verification; pre-fix `main` will trigger the C2 failure mode per `docs/PLATFORMS.md` Codex "Known gaps"):
    ```bash
    codex plugin marketplace add DgxSparkLabs/marketplace
    ```
  - **Remote PR branch** (recommended remote path — `--ref` is verified working per `docs/PLATFORMS.md` Codex "From GitHub (specific branch)" and `docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification.md` C3):
    ```bash
    codex plugin marketplace add DgxSparkLabs/marketplace --ref main
    ```
  - **Local clone** (most reliable — tests exactly the bytes at `/workspace/marketplace`):
    ```bash
    codex plugin marketplace add /workspace/marketplace
    ```
  - **Expected (all three modes)**: marketplace registered under name `dgxsparklabs-marketplace`.

- [ ] Step 2: `codex plugin marketplace list`
  - **Expected**: a row showing `dgxsparklabs-marketplace` with a ROOT path. The ROOT should point at `.agents/plugins/marketplace.json` inside Codex's marketplace cache — that confirms Phase 5.5's canonical-path emission works.
  - **Example expected output**:
    ```
    MARKETPLACE               ROOT
    dgxsparklabs-marketplace  /root/.codex/.tmp/marketplaces/dgxsparklabs-marketplace
    openai-curated            /root/.codex/.tmp/plugins
    ```

- [ ] Step 3: `codex plugin list`
  - **Expected**: lists all marketplace plugins (skills, rules, agents, bundles, etc.); should NOT be empty. STATUS column shows `not installed` for any you haven't `codex plugin add`-ed yet.

### 5.5 Per-construct verification

#### 5.5.1 Skill — `skill-example`
- [ ] **Install**: `codex plugin add skill-example@dgxsparklabs-marketplace`
- [ ] **Hands-on invocation**: open a Codex session and ask it to use the skill:
  ```bash
  codex
  > use the example skill to send a test notification
  ```
- [ ] **Expected**: Codex recognizes the skill and invokes it (or describes how it would). Codex surfaces skills via the per-plugin `.codex-plugin/plugin.json` pointing at `./skills/`.
- [ ] **Diagnostic (only if hands-on fails)**: `codex plugin list | grep -F "skill-example"` shows STATUS = `installed`.

#### 5.5.2 Sub-agent — `agent-example`
- [ ] **Install**: `codex plugin add agent-example@dgxsparklabs-marketplace`
  - **Expected**: install command succeeds.
- [ ] **Hands-on invocation** — open a Codex session and ask:
  ```bash
  codex
  > what subagents do we have available?
  ```
- [ ] **Expected**: `notebook-reviewer` (our sub-agent from `agent-example`) appears in the list alongside Codex's built-ins (`default`, `explorer`, `worker`).
- [ ] **🐛 KNOWN BUG (2026-05-25 QA)**: Codex does NOT currently surface our sub-agent. It lists only its three built-ins. The `.codex/agents/notebook-reviewer.toml` file emission is on disk (verified via `codex plugin list` ROOT path), but Codex's subagent loader isn't picking it up. Likely cause: TOML schema mismatch between what our `scripts/converters/md_to_toml.py` produces and what Codex expects. Needs investigation before this refactor's Codex sub-agent emission can claim "working." See "Known issues surfaced by QA" below.

#### 5.5.3 Hook — `hook-example`
- [ ] **Install**: `codex plugin add hook-example@dgxsparklabs-marketplace`
- [ ] **Hands-on invocation**: trigger the hook's bound event inside a `codex` session (whichever event the hook subscribes to in `hooks/example/hooks/hooks.json`).
- [ ] **Expected**: hook fires its configured action. The per-plugin manifest emits `"hooks": "./hooks/hooks.json"` per `CodexPlatform.build_plugin_json`.
- [ ] **Verification method UNKNOWN** for Codex hook enumeration — Codex has no `codex hooks list` command captured in our docs. Hook firing is the only observable. See follow-up.

#### 5.5.4 MCP server — `mcp-example`
- [ ] **Install**: `codex plugin add mcp-example@dgxsparklabs-marketplace`
- [ ] **Hands-on invocation**: in a `codex` session, list MCP tools or invoke one of the example MCP's tools.
  ```bash
  codex mcp list
  ```
- [ ] **Expected**: `mcp-example` (or its server name) appears in the MCP server list, OR Codex exposes the MCP's tools in-session.
- [ ] **Note**: Codex also accepts manually-added MCP servers via `codex mcp add` — verify our plugin-installed MCP is enumerated separately from any test MCPs added by hand.

#### 5.5.5 Rule (no native install, file-discovery only) — `rule-example`
- [ ] **Setup**: this is N/A as a Codex-native install path. Codex reads rules from `AGENTS.md`, `.cursor/rules/*.md`, `.windsurf/rules/*.md` natively. Verify by opening Codex inside the workspace you cloned in setup:
  ```bash
  cd /workspace/marketplace   # already on main from setup
  codex
  > what rules currently apply to your behavior?
  ```
- [ ] **Expected**: Codex describes rules from `.cursor/rules/` and `.windsurf/rules/` as active context (the rule mirrors are present after `uv run scripts/generate_manifest.py`).
- [ ] **Verification method UNKNOWN** — Codex has no documented "list active rules" command; this is qualitative. See follow-up.

### 5.6 Specifically for THIS refactor

The whole `.codex/agents/<name>.toml` path is new. If the hands-on sub-agent test shows `notebook-reviewer` is invisible to Codex, that confirms the known bug above. If it DOES surface (i.e., the bug got fixed), update this doc.

Phase 5.5's `.agents/plugins/marketplace.json` is also new — Step 2 of marketplace registration is the verification (the ROOT path).

### 5.7 Cleanup

```bash
codex plugin remove skill-example@dgxsparklabs-marketplace
codex plugin remove agent-example@dgxsparklabs-marketplace
codex plugin remove hook-example@dgxsparklabs-marketplace
codex plugin remove mcp-example@dgxsparklabs-marketplace
codex plugin marketplace remove dgxsparklabs-marketplace
```

If hermetic:
```powershell
docker rm -f qa-codex
```

---

## 6. Gemini

**What we're verifying**: extension install from GitHub URL, plus per-construct verification for the three constructs Gemini supports per `GeminiPlatform.supports` and `docs/PLATFORMS.md` Gemini "What constructs it supports": **skill, sub-agent, hook**. **New in 2026-05-25**: sub-agent emission at `.gemini/agents/<name>.md` AND hook emission at `.gemini/hooks/hooks.json`.

### 6.1 Setup option A — Docker (hermetic)

```powershell
docker run -it --name qa-gemini node:20 bash
```

Inside the container (`node:20` has `git` pre-installed):
```bash
# Install Gemini CLI
npm install -g @google/gemini-cli
gemini --version

# Clone the PR branch for testing PR #5:
git clone --branch main https://github.com/DgxSparkLabs/marketplace.git /workspace/marketplace
cd /workspace/marketplace

# (To test against main instead: --branch main or omit --branch.)
```

### 6.2 Setup option B — Native

```powershell
npm install -g @google/gemini-cli
gemini --version
```

### 6.3 Auth

```bash
gemini auth login        # Google OAuth; needs browser
```

### 6.4 Extension install

- [ ] Step 1: Install the marketplace extension. Pick ONE of:
  - **Remote `main`** (smoke test only — NOT for PR #5 verification, since `main` doesn't yet have the Gemini hook/sub-agent fixes):
    ```bash
    echo "y" | gemini extensions install https://github.com/DgxSparkLabs/marketplace --consent
    ```
  - **Remote PR branch** (recommended remote path — `--ref` is verified working per `docs/PLATFORMS.md` Gemini "From GitHub (specific branch)"; CI uses this same pattern via `compat-extension.yml`):
    ```bash
    echo "y" | gemini extensions install https://github.com/DgxSparkLabs/marketplace --ref main --consent
    ```
  - **Local clone** (most reliable — tests exactly the bytes at `/workspace/marketplace`):
    ```bash
    echo "y" | gemini extensions install /workspace/marketplace --consent
    ```
  - **Expected (all three modes)**: extension installs successfully; success message printed.
  - **Note**: the original remote-main path was the G2 path in the verification logs — broken pre-Phase-5, fixed by root-level `gemini-extension.json` emission.

- [ ] Step 2: `gemini extensions list 2>&1`
  - **Expected**: dgxsparklabs marketplace extension appears
  - **Note**: the `2>&1` is required — Gemini writes extension list to stderr (a quirk we verified empirically; see `docs/PLATFORMS.md` Gemini "Known gaps")

### 6.5 Per-construct verification

#### 6.5.1 Skill — `skill-example`
- [ ] **Install**: covered by the extension install above (Gemini installs all skills as part of the extension).
- [ ] **Hands-on invocation**: in a `gemini` session, ask Gemini to invoke the skill:
  ```bash
  gemini
  > use the example skill to send a test
  ```
- [ ] **Expected**: Gemini recognizes the skill and executes it (or asks for needed params).
- [ ] **Diagnostic**: `gemini skills list --all 2>&1 | grep -F example` matches.

#### 6.5.2 Sub-agent — `agent-example`
- [ ] **Install**: covered by the extension install above.
- [ ] **Hands-on invocation**: open a Gemini session and check the agents list:
  ```bash
  gemini
  > /agents
  ```
- [ ] **Expected**: under "Local Agents", you should see `notebook-reviewer` (our sub-agent) alongside Gemini's built-ins (`codebase_investigator`, `cli_help`, `generalist`).
- [ ] **🐛 KNOWN BUG (2026-05-25 QA)**: Gemini does NOT currently surface our sub-agent in `/agents`. It shows only its three built-ins. The file is on disk at `~/.gemini/extensions/dgxsparklabs-marketplace/agents/notebook-reviewer.md` (you can confirm with `ls ~/.gemini/extensions/*/agents/`). The extension installs cleanly and skills are recognized (skill test above works), but Gemini's agent loader isn't picking up our `.md` agent file. Likely cause: file location or frontmatter mismatch. See "Known issues surfaced by QA" below.
- [ ] **Disk-level sanity check** (use this AFTER the hands-on `/agents` test as a diagnostic, to confirm the bug isn't "we didn't ship the file"):
  ```bash
  ls ~/.gemini/extensions/*/agents/ 2>/dev/null
  cat ~/.gemini/extensions/*/agents/notebook-reviewer.md 2>/dev/null | head -20
  ```

#### 6.5.3 Hook — `hook-example`
- [ ] **Install**: covered by the extension install above.
- [ ] **Hands-on invocation**: trigger the hook's bound event inside a `gemini` session (whichever Cascade-style or session event the hook subscribes to in `hooks/example/hooks/hooks.json`).
- [ ] **Expected**: hook executes its action.
- [ ] **🛑 Verification method UNKNOWN**: Gemini has no documented hooks-list command (per `docs/PLATFORMS.md` Gemini "Discovery commands" — there's `mcp list` but no `hooks list`). File presence + JSON validity is the minimum signal until Gemini exposes a hooks-list command. See follow-up.
- [ ] **Diagnostic**:
  ```bash
  ls ~/.gemini/extensions/*/hooks/ 2>/dev/null
  cat ~/.gemini/extensions/*/hooks/hooks.json 2>/dev/null
  ```
  - **Expected**: `hooks.json` file present and contains valid JSON

### 6.6 Specifically for THIS refactor

Sub-agent and hook emission to Gemini is new. The `/agents` hands-on test (NOT just file existence) is the only way to verify the platform actually loads what we ship. The file-existence check is diagnostic — useful only if the hands-on test fails. The hook hands-on test is currently bottlenecked by no hooks-list command — flag this as a verification-gap to research.

### 6.7 Cleanup

```bash
gemini extensions uninstall DgxSparkLabs__marketplace
# (name shown by `gemini extensions list 2>&1` is the canonical form)
```

If hermetic:
```powershell
docker rm -f qa-gemini
```

---

## 7. Cursor (IDE + CLI)

Cursor has two distinct surfaces — the **IDE** (GUI, in-editor `/add-plugin`) and the **CLI** (binary name is `agent`, no plugin install commands). Per the locked D-9 decision and `docs/PLATFORMS.md` Cursor "Discovery commands" + "Known gaps", both surfaces share the same `CursorPlatform` emission (`.cursor/rules/`, `.cursor/agents/`, per-plugin `.cursor-plugin/plugin.json`). The IDE installs via UI gesture; the CLI consumes from filesystem only.

**What we're verifying**: per-construct install on the IDE side for **rule, skill, sub-agent, command, hook, MCP** (`CursorPlatform.supports`), plus filesystem-discovery verification on the CLI side (populated either by Dashboard import, a `/add-plugin` in the IDE, or — on the CLI — by the `agents` cross-platform CLI).

### 7.1 Cursor IDE

**Docker is NOT applicable** — Cursor IDE is a GUI, not headless.

Native install:
- Download installer from `cursor.com/download`
- Run the Windows installer, complete first-run setup
- Sign in via the app's UI

#### 7.1.1 Marketplace registration paths

**Three install sources are possible for Cursor IDE**, varying by surface (in-editor `/add-plugin` vs Dashboard team-marketplace import) and source (remote main / remote branch / local clone). For PR #5 verification, **the local-clone path is the most reliable** because it tests the exact bytes of the PR (the hook + skill-manifest fixes in this PR write to `.cursor/*.json` and `.cursor/rules/`, both of which Cursor IDE picks up from a locally-opened workspace).

- [ ] **Path A — In-editor `/add-plugin` (remote)**:
  - Open any test repo in Cursor (a scratch dir is fine)
  - **Remote `main`**: in Cursor's chat panel, run `/add-plugin <plugin-name>@https://github.com/DgxSparkLabs/marketplace` — see per-construct tests below.
  - **Remote PR branch (UNTESTED)**: the form `/add-plugin <plugin-name>@https://github.com/DgxSparkLabs/marketplace?ref=main` MAY work but is not documented in Cursor's published docs and not verified in this repo's evidence. If you can confirm or refute it, please report — see the open-questions section at the bottom of this doc.
  - **❗ Do NOT use the naked-URL form** (`/add-plugin https://github.com/DgxSparkLabs/marketplace`). It sends Cursor's chat agent into a research spiral — it goes off investigating the repo instead of installing. The `<plugin-name>@<url>` form goes straight to the install UI without involving the chat agent.

- [ ] **Path B — Dashboard team-marketplace import** (admin path; verify once):
  - Visit `cursor.com/dashboard` → Settings → Plugins → Import
  - **Remote `main`**: paste `https://github.com/DgxSparkLabs/marketplace` and save
  - **Remote PR branch**: the Dashboard UI exposes a branch selector — pick `main` (per `docs/PLATFORMS.md` Cursor "From GitHub (specific branch)": "Branch selection happens in the dashboard").
  - **Expected**: marketplace appears in the team marketplace list, all Cursor-supported plugins enumerated.

- [ ] **Path C — Local clone** (recommended for PR #5 verification):
  - On the host (Cursor IDE is GUI, so Docker doesn't apply), clone the PR branch:
    ```powershell
    git clone --branch main https://github.com/DgxSparkLabs/marketplace.git C:\Users\devic\source\marketplace-pr5
    ```
  - Open `C:\Users\devic\source\marketplace-pr5` in Cursor (File → Open Folder).
  - Cursor picks up `.cursor/rules/*.md`, `.cursor/agents/*.md`, `.cursor/hooks.json`, `.cursor/mcp.json`, and per-plugin `.cursor-plugin/plugin.json` files from the opened workspace. This is the path that exercises THIS PR's hook + skill-manifest fixes most directly — no marketplace registration needed; Cursor reads workspace files natively.

#### 7.1.2 Per-construct verification (IDE)

##### Skill — `skill-example`
- [ ] **Install**: in Cursor chat panel, run `/add-plugin skill-example@https://github.com/DgxSparkLabs/marketplace`
- [ ] **Hands-on invocation**: type `/example` in Cursor.
- [ ] **Expected**: clean popup showing skill name and description; selecting it invokes the skill.
- [ ] **🐛 KNOWN BUG (2026-05-25 QA)**: The skill popup displays mangled metadata. Instead of clean description text, you see something like:
  ```
  /1.0.0
  Send a Telegram notification with a task summary
  a86cb86dfd62f99475408fc984e334af0475029b
  Send a Telegram notification with a task summary
  ```
  The version, commit SHA, and duplicated description appear in slots Cursor expects different fields in. Likely cause: our `.cursor-plugin/plugin.json` populates fields Cursor's display layer renders in unexpected positions. Skill is functional (install succeeds, settings.json populated correctly), just the popup metadata is mis-rendered. See "Known issues surfaced by QA" below.

##### Rule — `rule-example`
- [ ] **Install**: `/add-plugin rule-example@https://github.com/DgxSparkLabs/marketplace`
- [ ] **Hands-on invocation**: open the Cursor chat panel and ask "what rules are currently in effect?", or attempt an action the rule constrains.
- [ ] **Expected**: Cursor's reply reflects the rule's framing (the example rule should make Cursor qualify plans with explicit example consideration). Rule is read from `.cursor/rules/example.md` (the `CursorPlatform.emit` Rule branch copies `formats/cursor.md` → `.cursor/rules/<name>.md`).

##### Sub-agent — `agent-example`
- [ ] **Install**: `/add-plugin agent-example@https://github.com/DgxSparkLabs/marketplace`
- [ ] **Hands-on invocation**: in Cursor, type `/notebook-reviewer`.
- [ ] **Expected**: sub-agent dropdown appears with the correct description ("Reviews a lab notebook entry as a skeptical peer reviewer...").
- [ ] **✅ KNOWN GOOD (2026-05-25 QA)**: This works correctly. Cursor's sub-agent format matches what we emit at `.cursor/agents/notebook-reviewer.md`. This is the load-bearing positive finding — Cursor accepts our format, so the Codex and Gemini sub-agent bugs are platform-specific format-mismatches, not a "we shipped a uniformly broken format" issue.

##### Command — `command-example`
- [ ] **Install**: `/add-plugin command-example@https://github.com/DgxSparkLabs/marketplace`
- [ ] **Hands-on invocation**: type the command's slash form (per `commands/example/commands/<name>.md` frontmatter).
- [ ] **Expected**: command appears in Cursor's command palette / slash dropdown; invocation runs the command body.
- [ ] **Verification method UNKNOWN**: Cursor has no documented "list registered commands" enumeration command per `docs/PLATFORMS.md` Cursor section. Per-plugin `.cursor-plugin/plugin.json` emits `"commands": "./commands/"` and Cursor "auto-discovers from default subdirs inside an installed plugin" — but the visible-to-operator surface depends on what Cursor renders. See follow-up.

##### Hook — `hook-example`
- [ ] **Install**: `/add-plugin hook-example@https://github.com/DgxSparkLabs/marketplace`
- [ ] **Hands-on invocation**: trigger the hook's bound event (whichever event the hook subscribes to in `hooks/example/hooks/hooks.json`).
- [ ] **Expected**: hook fires its configured action.
- [ ] **Diagnostic**: `.cursor/hooks.json` (project) or `~/.cursor/hooks.json` (user) shows the hook entry. Per-plugin `.cursor-plugin/plugin.json` emits `"hooks": "./hooks/hooks.json"`.
- [ ] **Verification method UNKNOWN**: Cursor's hook-list surface isn't documented. See follow-up.

##### MCP server — `mcp-example`
- [ ] **Install**: `/add-plugin mcp-example@https://github.com/DgxSparkLabs/marketplace`
- [ ] **Hands-on invocation**: open Cursor's MCP server UI (Settings → MCP Servers) or use one of the MCP's tools in-chat.
- [ ] **Expected**: `mcp-example` (or its server name) appears in the MCP server list, AND Cursor's chat agent has access to its tools.
- [ ] **Diagnostic**: `.cursor/mcp.json` shows the server entry; per-plugin manifest passes through `"mcpServers": <value-from-source-plugin.json>`.

### 7.2 Cursor CLI (`agent` binary)

**What we're verifying**: Cursor CLI (the `agent` binary) consumes from filesystem only — there's no `agent plugin install`, no marketplace registration command (per `docs/PLATFORMS.md` Cursor "Known gaps"). Populate `.agents/` and `.cursor/` paths via the cross-platform `agents` CLI, then verify the Cursor CLI sees them.

Because the CLI reads only workspace files, **"branch selection" reduces to "which branch you cloned."** There is no remote-main vs remote-branch distinction for the CLI — clone the branch you want to test and open it.

#### 7.2.1 Setup

```bash
# macOS/Linux/WSL
curl https://cursor.com/install -fsS | bash

# Windows PowerShell
irm 'https://cursor.com/install?win32=true' | iex

# Verify
agent --version    # expected: e.g., 2026.05.20-2b5dd59

# For PR #5 verification, clone the PR branch and cd into it:
git clone --branch main https://github.com/DgxSparkLabs/marketplace.git /workspace/marketplace
cd /workspace/marketplace
```

#### 7.2.2 Per-construct verification (CLI)

Use the `agents` cross-platform CLI to populate the project's `.agents/` and (where applicable) `.cursor/` dirs — those are what the Cursor CLI reads.

Set up a scratch project:
```bash
mkdir scratch-cursor-cli && cd scratch-cursor-cli
agents install skill-example --scope project    # populates .agents/skills/example/
agents install rule-example --scope project        # populates .cursor/rules/ (per-platform spray)
agents install agent-example --scope project            # populates .cursor/agents/notebook-reviewer.md
agents install command-example --scope project
agents install hook-example --scope project
agents install mcp-example --scope project
```

##### Skill — `skill-example`
- [ ] **Hands-on invocation**: open the scratch dir with the Cursor CLI:
  ```bash
  agent
  > use the example skill
  ```
- [ ] **Expected**: the CLI's agent discovers the skill from `.agents/skills/example/SKILL.md` (per `docs/PLATFORMS.md` Cursor "Discovery paths" — `.agents/skills/<name>/SKILL.md` is the primary path).

##### Rule — `rule-example`
- [ ] **Hands-on invocation**: with the CLI in the scratch dir, ask the agent for an action the rule should affect.
- [ ] **Expected**: rule from `.cursor/rules/example.md` is in effect — the agent's response reflects the rule's framing.

##### Sub-agent — `agent-example`
- [ ] **Hands-on invocation**: in the CLI, dispatch the sub-agent (the CLI's mechanism for invoking workspace agents — refer to `agent --help` for the exact slash form, or use `agent agent <name>` if that subcommand exists).
- [ ] **Expected**: sub-agent from `.cursor/agents/notebook-reviewer.md` is invocable.
- [ ] **Verification method UNKNOWN**: per `docs/PLATFORMS.md` Cursor "Discovery commands" the CLI lacks a documented agent-dispatch command. See follow-up.

##### Command — `command-example`
- [ ] **Hands-on invocation**: with the CLI, attempt to invoke the command.
- [ ] **Expected**: command from `_generated/command-example/commands/` is invocable.
- [ ] **Verification method UNKNOWN**: same as for the IDE — no enumeration command. The CLI's `agent --help` lists `generate-rule` but no plugin-command surface. See follow-up.

##### Hook — `hook-example`
- [ ] **Hands-on invocation**: trigger the hook's bound event during a CLI session.
- [ ] **Expected**: hook fires.
- [ ] **Verification method UNKNOWN**: CLI hook surface not documented. See follow-up.

##### MCP server — `mcp-example`
- [ ] **Hands-on invocation**: `agent mcp` (per `agent --help` from `logs/CU3.txt`).
- [ ] **Expected**: `mcp-example` listed; tools invocable from a CLI session.

### 7.3 Specifically for THIS refactor

Cursor IDE gained FOUR new construct types this refactor (sub-agents, commands, hooks, MCP). Sub-agent has a positive confirmation; the other three have UNKNOWN verification methods because Cursor's enumeration surface for these isn't documented.

The Cursor CLI per-construct tests are a forward-looking shape — the CLI's verification methods aren't fully mapped yet. UNKNOWN cells should fuel the next research round.

### 7.4 Cleanup

Uninstall each plugin via Cursor IDE's UI:
- Settings → Plugins → click each → Remove
- Remove the marketplace from Settings → Plugins → Import list

For the CLI scratch project:
```bash
cd .. && rm -rf scratch-cursor-cli
```

---

## 8. Windsurf

**What we're verifying**: rule + hook discovery, plus skill auto-discovery from `.agents/skills/`. Per `WindsurfPlatform.supports` and `docs/PLATFORMS.md` Windsurf "What constructs it supports": **rule, hook**, and skills via the `.agents/skills/` cross-platform path. **New in 2026-05-25**: hook emission at `.windsurf/hooks.json`.

### 8.1 Setup

**Docker NOT applicable** — Windsurf is GUI-only, no CLI exists.

Native install:
- Download from `codeium.com/windsurf` → run the Windows installer
- Sign in via the app's UI (Codeium account)

### 8.2 Populating the workspace

Windsurf reads from the filesystem only — no install command, no marketplace registration. "Branch selection" reduces to "which branch you cloned." Either:

1. **Clone the PR branch** (recommended for PR #5 verification — this is what tests THIS PR's hook fixes at `.windsurf/hooks.json`):
   ```bash
   git clone --branch main https://github.com/DgxSparkLabs/marketplace.git C:\Users\devic\source\marketplace-pr5
   ```
   Open the clone in Windsurf (File → Open Folder).

2. **Clone main** (smoke test only — NOT useful for PR #5 verification because the hook event-name fixes haven't landed):
   ```bash
   git clone https://github.com/DgxSparkLabs/marketplace
   ```

3. **Scratch dir + `agents` CLI** (works for both, depends on which branch the `agents` CLI was installed from — see Platform 7 for `AGENTS_REF`):
   ```bash
   mkdir scratch-windsurf && cd scratch-windsurf
   agents install rule-example --scope project
   agents install hook-example --scope project
   agents install skill-example --scope project
   ```
   Open `scratch-windsurf` in Windsurf.

### 8.3 Per-construct verification

#### 8.3.1 Skill — `skill-example` (read via `.agents/skills/`)
- [ ] **Hands-on invocation**: in Windsurf, open Cascade and type `@skill-example`.
- [ ] **Expected**: Cascade recognizes the `@skill-X` syntax and uses the skill — auto-discovered from `.agents/skills/example/SKILL.md` per `docs/PLATFORMS.md` Windsurf "Discovery paths".
- [ ] **Alternative hands-on**: ask Cascade "list the skills you have available" — `example` should appear.

#### 8.3.2 Rule — `rule-example`
- [ ] **Hands-on invocation**: ask Cascade for an action the rule should affect (e.g., a refactor where example reasoning would change the recommendation).
- [ ] **Expected**: Cascade's reply reflects the rule's framing. Rule discovered from `.windsurf/rules/example.md` (with the required `trigger:` frontmatter — `always_on` for `example` per the source `rule.md`).
- [ ] **Diagnostic**: confirm `.windsurf/rules/example.md` exists in the workspace.

#### 8.3.3 Hook — `hook-example`
- [ ] **Hands-on invocation**: trigger the hook's bound Cascade event (per `hooks/example/hooks/hooks.json`'s event subscription).
- [ ] **Expected**: hook fires its configured action.
- [ ] **🛑 Verification method UNKNOWN**: Windsurf has no CLI to enumerate registered hooks. Per `docs/PLATFORMS.md` Windsurf "Known gaps", verification today is qualitative — observe the side effect or check Cascade behavior. See follow-up.
- [ ] **Diagnostic**: `.windsurf/hooks.json` present at the workspace root (Windsurf-specific path — no `hooks/` subdir, unlike Gemini).

### 8.4 Specifically for THIS refactor

Hook emission to `.windsurf/hooks.json` is new in 2026-05-25. With no Windsurf CLI for introspection, the only verification path is "trigger the event and observe behavior change" — which depends on the example hook being interactive enough to observe. This is a known coverage gap, not a bug in the emission itself.

### 8.5 Cleanup

Nothing to uninstall on the platform side — Windsurf reads from the repo's filesystem. Close the project to "uninstall." If you used a scratch dir:
```bash
cd .. && rm -rf scratch-windsurf
```

---

## 9. Devin

**What we're verifying**: skill discovery from `.agents/skills/`, rule discovery from `.windsurf/rules/` + `.cursor/rules/` (per `DevinPlatform.supports = {SkillConstruct}` and `docs/PLATFORMS.md` Devin "What constructs it supports" + "Discovery paths"), and MCP CLI surface. **New in 2026-05-25**: `.devin/skills/` mirror retired (now uses `.agents/skills/`).

### 9.1 Setup option A — Docker (hermetic)

```powershell
docker run -it --name qa-devin ubuntu:24.04 bash
```

Inside (Devin's installer needs `curl` and POSIX; `ubuntu:24.04` ships without curl/git so `apt install` is required):
```bash
apt update && apt install -y curl git
curl -fsSL https://cli.devin.ai/install.sh | bash || true
# Add devin to PATH if installer doesn't:
export PATH="$HOME/.local/bin:$PATH"
devin --version

# Clone the PR branch for testing PR #5:
git clone --branch main https://github.com/DgxSparkLabs/marketplace.git /workspace/marketplace
cd /workspace/marketplace

# (To test against main instead: --branch main or omit --branch.)
```

### 9.2 Setup option B — Native (WSL or Git Bash)

```bash
# Inside WSL or Git Bash:
curl -fsSL https://cli.devin.ai/install.sh | bash || true
devin --version
```

### 9.3 Auth

```bash
devin auth login         # Codeium/Windsurf login; opens browser
```

(Discovery commands are auth-free; `auth login` is only needed for actual Devin agent sessions.)

### 9.4 Populating the workspace

For Docker setup: already done above by the `git clone --branch` step. Just confirm you're in the clone:
```bash
cd /workspace/marketplace && pwd
```

For native setup (WSL/Git Bash), clone the branch you want to test:
```bash
git clone --branch main https://github.com/DgxSparkLabs/marketplace.git ~/marketplace-pr5 && cd ~/marketplace-pr5
# Or: omit --branch main to clone main for a smoke test.
```

### 9.5 Per-construct verification

#### 9.5.1 Skill — `skill-example` (read via `.agents/skills/`)
- [ ] **Hands-on invocation**: `devin skills list`
- [ ] **Expected**: lists 27 skills from `.agents/skills/` (since `.devin/skills/` was retired this round). `example` is one of them. Output format per `docs/PLATFORMS.md` Devin "Discovery commands": `/<slash-command> [triggers] (path) - description`.
- [ ] **Hands-on (dispatching the skill)**: in a `devin` session, ask Devin to use the skill.
- [ ] **Diagnostic**: `devin skills paths` should mention `.agents/skills/` AND `~/.agents/skills/` (user scope) — `.devin/skills/` should be ABSENT (the legacy mirror was retired per D-1).
- [ ] **Hands-on (show)**: `devin skills show example` — prints the skill body.

#### 9.5.2 Rule — `rule-example` (read via `.windsurf/rules/`, `.cursor/rules/`)
- [ ] **Hands-on invocation**: `devin rules list`
- [ ] **Expected**: rules listed with provider tags (`Cursor`, `Windsurf`, `Standard`) per `docs/PLATFORMS.md` Devin "Discovery commands". `example` appears tagged with both `Cursor` and `Windsurf` (it's mirrored to both `.cursor/rules/example.md` and `.windsurf/rules/example.md`).
- [ ] **Diagnostic**: `devin rules paths` lists `.windsurf/rules/*.md`, `.cursorrules`, `.cursor/rules/*.md`.
- [ ] **Hands-on (show)**: `devin rules show example` — prints the rule body.

#### 9.5.3 MCP — Devin-managed (no marketplace-emitted Devin MCP config)
- [ ] **Hands-on invocation**: `devin mcp list`
- [ ] **Expected**: empty-state `No MCP servers configured` (or any MCPs you've manually added). The marketplace does not emit a Devin-native MCP config today; this test is "Devin's MCP surface still works alongside our marketplace clone."
- [ ] **Optional**: `devin mcp add example -- uvx mcp-server-fetch && devin mcp list | grep -i example`
- [ ] **Expected**: manual add + grep both succeed.

### 9.6 Specifically for THIS refactor

The `.devin/skills/` mirror was retired. If `devin skills list` returns ZERO skills, the `.agents/skills/` fallback isn't working as expected (regression). Also confirm `.devin/skills/` is ABSENT in the workspace tree (`ls -la .devin/` should show no `skills/` subdir).

### 9.7 Cleanup

If hermetic:
```powershell
docker rm -f qa-devin
```

If native:
- `devin auth logout` if you want to clear creds
- Delete the scratch clone

---

## 10. `agents` CLI (the new cross-platform shim)

**What we're verifying**: the new `agents` CLI installs cleanly, has the documented subcommand surface, respects `--scope project|user`, and the `--agents-only` flag actually restricts emission to `.agents/`. Per construct, the CLI should emit to `.agents/<construct>/<name>/` (project) or `~/.agents/<construct>/<name>/` (user).

### 10.1 Setup option A — Docker (hermetic)

```powershell
docker run -it --name qa-agents ubuntu:24.04 bash
```

Inside (`ubuntu:24.04` ships without curl/python3/git, so install them first):
```bash
apt update && apt install -y curl python3 git
```

Then install the `agents` CLI. Pick ONE of the four paths below:

```bash
# Path 1 — Remote main (smoke test only — NOT for PR #5 verification):
curl -fsSL https://raw.githubusercontent.com/DgxSparkLabs/marketplace/main/install.sh | bash

# Path 2 — Remote PR branch via curl URL path segment (fetches install.sh from the branch):
curl -fsSL https://raw.githubusercontent.com/DgxSparkLabs/marketplace/main/install.sh | bash

# Path 3 — Remote PR branch via AGENTS_REF env var (install.sh from main, but clones the marketplace from the branch — see install.sh: `REF="${AGENTS_REF:-main}"`):
AGENTS_REF=main curl -fsSL https://raw.githubusercontent.com/DgxSparkLabs/marketplace/main/install.sh | bash

# Path 4 — Local clone (most reliable — tests exactly the bytes at /workspace/marketplace):
git clone --branch main https://github.com/DgxSparkLabs/marketplace.git /workspace/marketplace
cd /workspace/marketplace && bash install.sh
```

Then:
```bash
export PATH="$HOME/.local/bin:$PATH"
agents --version
```

**`install.sh` env-var surface** (from `install.sh` itself):
- `AGENTS_REF` — marketplace branch to clone (default `main`). Use this to install from a PR branch.
- `AGENTS_MARKETPLACE_URL` — override the repo URL (default `https://github.com/DgxSparkLabs/marketplace`). Useful for testing forks.
- `AGENTS_DEST` — override the wrapper install path (default `~/.local/bin/agents`).
- `AGENTS_LIB` — override the library install path (default `~/.local/share/agents`).
- `AGENTS_PYTHON` — override the Python interpreter (default: first of `python3`, `python` on PATH).

`install.ps1` (Windows) supports the same env vars (`$env:AGENTS_REF`, `$env:AGENTS_MARKETPLACE_URL`, etc.) per its header comment.

### 10.2 Setup option B — Native (Windows PowerShell)

```powershell
# Path 1 — Remote main:
irm https://raw.githubusercontent.com/DgxSparkLabs/marketplace/main/install.ps1 | iex

# Path 2 — Remote PR branch via AGENTS_REF env var:
$env:AGENTS_REF = 'main'
irm https://raw.githubusercontent.com/DgxSparkLabs/marketplace/main/install.ps1 | iex

# Path 3 — Local clone (most reliable):
git clone --branch main https://github.com/DgxSparkLabs/marketplace.git C:\Users\devic\source\marketplace-pr5
Set-Location C:\Users\devic\source\marketplace-pr5
powershell -ExecutionPolicy Bypass -File .\install.ps1

agents --version
```

**Expected**: a version string (e.g., `agents 0.1.0`). If `agents` is not recognized: the wrapper's install path (`$env:LOCALAPPDATA\agents\bin\agents.ps1` on Windows, `~/.local/bin/agents` on POSIX) didn't get added to `$PATH`. That's a real UX bug — flag it.

### 10.3 Auth

None. The `agents` CLI clones the marketplace via git; no platform auth required.

### 10.4 CLI surface verification

Set up a scratch project:
```bash
mkdir scratch-agents-cli && cd scratch-agents-cli
```

- [ ] **List available**:
  ```bash
  agents list --available
  ```
  - **Expected**: readable list of plugins. Note whether output is grouped, paginated, scannable.

- [ ] **Info on a plugin**:
  ```bash
  agents info skill-example
  ```
  - **Expected**: metadata (description, version, source, author)

- [ ] **`--help` surface**:
  ```bash
  agents --help
  agents install --help
  ```
  - **Expected**: clear, complete help text — every documented flag mentioned.

### 10.5 Per-construct install verification

For every supported construct, install and verify the on-disk landing path. The matrix's TEST¹² cells live here — construct types for which `agents` is the emit surface but no platform reads `.agents/<type>/` natively (yet) are still tested for correct emission.

#### 10.5.1 Skill — `skill-example`
- [ ] **Project install**: `agents install skill-example --scope project`
- [ ] **Verify path**:
  ```bash
  test -d .agents/skills/example && echo "agents YES"   # expected: agents YES
  test -f .agents/skills/example/SKILL.md && echo "skill YES"   # expected: skill YES
  ```
- [ ] **Hands-on (Cursor CLI or Windsurf consumes)**: the SKILL.md at `.agents/skills/example/` is what Cursor CLI and Windsurf read — see those platforms' per-construct sections for the consumption test.
- [ ] **Per-platform spray** (default): `ls .cursor/skills/example/ 2>/dev/null` may also exist if the CLI sprays to per-platform paths; verify it matches the expected default scope.

#### 10.5.2 Rule — `rule-example`
- [ ] **Project install (strict `.agents/` only)**: `agents install rule-example --scope project --agents-only`
- [ ] **Verify**:
  ```bash
  test -f .agents/rules/example.md && echo "agents YES"   # expected: agents YES
  test -f .cursor/rules/example.md && echo "cursor YES"   # expected: NOTHING (no output) — --agents-only blocks per-platform spray
  test -f .windsurf/rules/example.md && echo "windsurf YES"   # expected: NOTHING
  ```
- [ ] **Hands-on**: the `.agents/rules/example.md` is forward-looking per `docs/PLATFORMS.md` "Per-platform manifest paths" + `docs/ARCHITECTURE.md` AgentsPlatform notes — no platform reads it natively today, but emission must be correct.

#### 10.5.3 Sub-agent — `agent-example`
- [ ] **Project install**: `agents install agent-example --scope project`
- [ ] **Verify**:
  ```bash
  test -d .agents/agents/agent-example && echo "agents YES"   # expected: agents YES (if CLI emits to .agents/agents/)
  ```
- [ ] **Note**: per `docs/research/platform-feature-routing/RECOMMENDATION.md` adoption matrix, `.agents/agents/` is UNVERIFIED across all platforms — no platform reads it natively today. The CLI test is "emission lands at the right path." Consumption is via per-platform mirrors (`.cursor/agents/`, `.codex/agents/`, `.gemini/agents/`).
- [ ] **Per-platform spray**: `ls .cursor/agents/notebook-reviewer.md` should exist (default-scope spray), and that file IS consumed by Cursor IDE.

#### 10.5.4 Command — `command-example`
- [ ] **Project install**: `agents install command-example --scope project`
- [ ] **Verify**:
  ```bash
  test -d .agents/commands/command-example && echo "agents YES"   # expected: agents YES
  ```
- [ ] **Note**: only Cursor (manifest-only) and Claude consume commands today. The `.agents/commands/` emission is forward-looking.

#### 10.5.5 Hook — `hook-example`
- [ ] **Project install**: `agents install hook-example --scope project`
- [ ] **Verify**:
  ```bash
  test -d .agents/hooks/hook-example && echo "agents YES"   # expected: agents YES
  ```
- [ ] **Per-platform spray**: `.cursor/hooks.json`, `.windsurf/hooks.json`, `.gemini/hooks/hooks.json` may also exist depending on what the CLI sprays under default scope.

#### 10.5.6 MCP — `mcp-example`
- [ ] **Project install**: `agents install mcp-example --scope project`
- [ ] **Verify**:
  ```bash
  test -d .agents/mcp-servers/mcp-example && echo "agents YES"   # expected: agents YES
  ```
- [ ] **Per-platform spray**: `.cursor/mcp.json` should also exist; Claude's plugin install handles the MCP wiring via the per-plugin manifest.

#### 10.5.7 LSP — `lsp-example` (forward-looking)
- [ ] **Project install**: `agents install lsp-example --scope project`
- [ ] **Verify**:
  ```bash
  test -d .agents/lsp-servers/lsp-example && echo "agents YES"   # expected: agents YES
  ```
- [ ] **Note**: only Claude consumes LSP today. The `.agents/lsp-servers/` emission is forward-looking.

#### 10.5.8 Monitor — `monitor-example` (forward-looking)
- [ ] **Project install**: `agents install monitor-example --scope project`
- [ ] **Verify**:
  ```bash
  test -d .agents/monitors/monitor-example && echo "agents YES"
  ```
- [ ] **Note**: Claude-only consumer.

#### 10.5.9 Output style — `output-style-example` (forward-looking)
- [ ] **Project install**: `agents install output-style-example --scope project`
- [ ] **Verify**:
  ```bash
  test -d .agents/output-styles/output-style-example && echo "agents YES"
  ```
- [ ] **Note**: Claude-only consumer.

#### 10.5.10 Theme — `theme-example` (forward-looking)
- [ ] **Project install**: `agents install theme-example --scope project`
- [ ] **Verify**:
  ```bash
  test -d .agents/themes/theme-example && echo "agents YES"
  ```
- [ ] **Note**: Claude-only consumer.

### 10.6 Scope and flag verification

#### 10.6.1 `--scope user` (writes to `~/.agents/` only per D-6)
- [ ] **Install**: `agents install rule-example --scope user`
- [ ] **Verify**:
  ```bash
  test -f "$HOME/.agents/rules/example.md" && echo "user YES"     # expected: user YES
  test -f "./.agents/rules/example.md" && echo "project YES"      # expected: NOTHING (user scope writes ONLY to ~/.agents/)
  ```

#### 10.6.2 `--scope user` + `--agents-only` for sub-agent
- [ ] **Install**: `agents install agent-example --scope user --agents-only`
- [ ] **Verify**:
  ```bash
  test -d "$HOME/.agents/agents/agent-example" && echo "user YES"     # expected: user YES
  test -d "./.agents/agents/agent-example" && echo "project YES"      # expected: NOTHING
  test -f "$HOME/.cursor/agents/notebook-reviewer.md" && echo "user cursor YES"   # expected: NOTHING (--agents-only)
  ```

#### 10.6.3 `agents list` (installed, not available)
- [ ] **Hands-on**: `agents list`
- [ ] **Expected**: shows all the installs from the per-construct tests above; distinguishes project vs user scope clearly.

#### 10.6.4 `agents uninstall` cleans both per-platform AND `.agents/` paths
- [ ] **Uninstall**: `agents uninstall skill-example --scope project`
- [ ] **Verify**:
  ```bash
  test -d .agents/skills/example && echo "still there"     # expected: NOTHING
  test -d .cursor/skills/example && echo "still there"     # expected: NOTHING
  ```

### 10.7 Specifically for THIS refactor

The CLI is brand new. Watch for:
- PATH not updated after install → UX bug
- Unclear error messages on bad input → polish issue
- Default scope (project) not surprising → matches D-13 Option C
- `--agents-only` actually skips per-platform paths → tests D-13 strict mode
- Constructs the CLI doesn't yet support (if any) → flag as scope gap

### 10.8 Cleanup

```bash
# Inside container:
agents uninstall rule-example --scope project
agents uninstall agent-example --scope project
agents uninstall command-example --scope project
agents uninstall hook-example --scope project
agents uninstall mcp-example --scope project
agents uninstall lsp-example --scope project
agents uninstall monitor-example --scope project
agents uninstall output-style-example --scope project
agents uninstall theme-example --scope project
# user-scope cleanup
agents uninstall rule-example --scope user
agents uninstall agent-example --scope user
exit
```

Then on host:
```powershell
docker rm -f qa-agents        # if hermetic
```

Native uninstall of the `agents` CLI:
```powershell
# Windows
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\agents"
# Then remove the PATH entry if installer added one — check $env:Path
```

```bash
# POSIX
rm ~/.local/bin/agents
rm -rf ~/.local/lib/agents_cli   # if installer placed lib here
```

---

## 11. Master teardown

If you ran any of the hermetic Docker paths, clean them all at once:

```powershell
docker rm -f qa-claude qa-codex qa-gemini qa-devin qa-agents 2>$null
docker image prune -f
```

Verify nothing's left:
```powershell
docker ps -a | Select-String "qa-"
# expected: no output
```

**Note on in-container clones**: if you used the `git clone --branch main ... /workspace/marketplace` step inside the containers, those clones live entirely inside each container's writable layer. `docker rm -f` removes the container AND its writable layer in one shot — no separate cleanup step needed for the clones. (Confirm with `docker ps -a` after teardown — nothing labelled `qa-*` should remain, and the clones go with them.)

Native platforms (Cursor IDE / Windsurf IDE / native CLI installs) — uninstall via their respective uninstall flows or simply leave installed if you use them day-to-day. If you made native local clones (e.g., `C:\Users\devic\source\marketplace-pr5` for Cursor IDE or Windsurf), delete those directories when you're done:

```powershell
Remove-Item -Recurse -Force C:\Users\devic\source\marketplace-pr5
```

---

## 12. Reporting findings

When you're done (or if something breaks mid-flow), capture:

1. **Which platform(s)** you tested and via which path (hermetic / native)
2. **Which cells in the matrix passed** as expected — useful to confirm what works
3. **Which cells failed** — and what you saw vs what was expected
4. **Which cells were UNKNOWN-method** — operator's notes on how they tried to verify, even if the method wasn't documented. These notes feed the next research round.
5. **Anything that felt wrong even if it "worked"** — confusing output, unclear errors, ambiguous flags, missing help text

A short report is fine — even a one-line summary per platform like "Cursor: agent + command + hook + MCP all visible in UI ✓; Gemini hook not auto-discovered ✗" is genuinely useful. With the expanded matrix, the per-cell granularity makes it easier to report a partial pass ("8/10 Claude cells PASS, lsp and monitor UNKNOWN-method").

If you'd prefer, file findings as GitHub issues against `DgxSparkLabs/marketplace` (one per finding so they can be triaged independently).

---

## 13. Quick reference table

Assumes `/workspace/marketplace` is the clone path (Docker setups in each platform's section produce this). For the local-install column, "clone first" means the `git clone --branch main ... /workspace/marketplace` step has already run.

| Platform | Native install | Docker base image | Local install command (from `/workspace/marketplace`) | New emissions this refactor |
|---|---|---|---|---|
| Claude Code | `npm install -g @anthropic-ai/claude-code` | `node:20` | `claude plugin marketplace add /workspace/marketplace` | none — regression check (all 10 constructs) |
| Codex | `npm install -g @openai/codex` | `node:20` | `codex plugin marketplace add /workspace/marketplace` | sub-agents (`.codex/agents/*.toml`), `.agents/plugins/marketplace.json` |
| Gemini | `npm install -g @google/gemini-cli` | `node:20` | `echo "y" \| gemini extensions install /workspace/marketplace --consent` | sub-agents (`.gemini/agents/`), hooks (`.gemini/hooks/hooks.json`) |
| Cursor IDE | `cursor.com/download` (GUI) | N/A (GUI) | open `/workspace/marketplace` (or host equivalent) in Cursor → File → Open Folder | sub-agents, commands, hooks, MCP (4 new!) |
| Cursor CLI | `curl https://cursor.com/install -fsS \| bash` / `irm 'https://cursor.com/install?win32=true' \| iex` | N/A | `cd /workspace/marketplace && agent` | reads same paths as IDE; consumption via filesystem |
| Windsurf | `codeium.com/windsurf` (GUI) | N/A (GUI) | open `/workspace/marketplace` (or host equivalent) in Windsurf → File → Open Folder | hooks (`.windsurf/hooks.json`) |
| Devin | `curl -fsSL https://cli.devin.ai/install.sh \| bash` (WSL on Windows) | `ubuntu:24.04` | `cd /workspace/marketplace && devin skills list` | `.devin/skills/` retired (now uses `.agents/skills/`) |
| `agents` CLI | `irm .../install.ps1 \| iex` (Win) / `curl ... \| bash` (POSIX) | `ubuntu:24.04` | `cd /workspace/marketplace && bash install.sh` | entire CLI is new |

Remote-branch quick reference (where supported):

| Platform | Remote-branch install command |
|---|---|
| Claude Code | not supported — use local clone |
| Codex | `codex plugin marketplace add DgxSparkLabs/marketplace --ref main` |
| Gemini | `echo "y" \| gemini extensions install https://github.com/DgxSparkLabs/marketplace --ref main --consent` |
| Cursor IDE | Dashboard branch picker (UI); `/add-plugin <name>@<url>?ref=<branch>` form untested |
| Cursor CLI | n/a — clone the branch and open |
| Windsurf | n/a — clone the branch and open |
| Devin | n/a — clone the branch and open |
| `agents` CLI | `AGENTS_REF=main curl -fsSL https://raw.githubusercontent.com/DgxSparkLabs/marketplace/main/install.sh \| bash` |

---

*Maintain this doc alongside platform changes. If a platform's install method changes or a new emission lands, update the relevant section and the master matrix. The doc is canonical only if it stays accurate.*

---

## 14. Known issues surfaced by QA (2026-05-25)

Discovered during the first hands-on QA pass of this doc. All three are real and reproducible.

### 14.1 🐛 Codex sub-agents not discovered

- **Symptom**: `codex plugin add agent-example@dgxsparklabs-marketplace` reports success; `codex plugin marketplace list` shows our marketplace; but `codex` interactive session lists only built-in subagents (`default`, `explorer`, `worker`) — not our `notebook-reviewer`.
- **State on disk**: `.codex/agents/notebook-reviewer.toml` emission exists per `scripts/converters/md_to_toml.py` (verified by `codex plugin list` ROOT column pointing at the canonical `.agents/plugins/marketplace.json`).
- **Hypothesis**: TOML schema produced by our converter doesn't match what Codex's subagent loader expects. Compare a working Codex-native subagent TOML (if available in Codex docs) against what we emit.
- **Scope to investigate**: `scripts/converters/md_to_toml.py` + Codex sub-agent docs at `developers.openai.com/codex/subagents/` (compare field names).

### 14.2 🐛 Gemini sub-agents not discovered

- **Symptom**: `gemini extensions install` succeeds; `gemini extensions list 2>&1` and `gemini skills list --all 2>&1` both show our content correctly (all 27 skills enumerated); but `/agents` in an interactive `gemini` session shows only built-ins (`codebase_investigator`, `cli_help`, `generalist`) — not our `notebook-reviewer`.
- **State on disk**: `~/.gemini/extensions/dgxsparklabs-marketplace/agents/notebook-reviewer.md` exists with valid frontmatter.
- **Hypothesis**: Either the file location inside the extension is wrong (Gemini may expect `agents/<name>/agent.md` not `agents/<name>.md`), or the frontmatter is missing a required field, or Gemini's agent loader is gated on a `gemini-extension.json` declaration we don't emit.
- **Scope to investigate**: `GeminiPlatform.emit` in `scripts/platforms.py` + Gemini extension reference docs at `geminicli.com/docs/extensions/reference/` (specifically the sub-agents section).

### 14.3 🐛 Cursor skill popup mangled metadata

- **Symptom**: After `/add-plugin skill-example@<url>` succeeds, typing `/example` (the skill's invocation name) in Cursor shows a popup with mangled fields — version string, commit SHA, and the description duplicated, instead of a clean description-only popup. (Originally observed during 2026-05-25 QA with `skill-telegram-notify` / `/telegram`; symptom reproduces with the example fixture.)
- **State on disk**: `.cursor/settings.json` is populated correctly with the plugin entry. The actual install path works.
- **Hypothesis**: Our `.cursor-plugin/plugin.json` for skills populates fields that Cursor's display layer renders in unexpected slots. Compare against a working Cursor-native skill plugin's manifest.
- **Scope to investigate**: `CursorPlatform.build_plugin_json` for SkillConstruct in `scripts/platforms.py` + Cursor plugin manifest reference at `cursor.com/docs/reference/plugins`.

### 14.4 ✅ Cursor sub-agent (positive finding)

- **Symptom**: `/add-plugin agent-example@<url>` then `/notebook-reviewer` in Cursor → clean popup with correct description. Sub-agent invocation works as designed.
- **Implication**: Cursor's sub-agent format DOES match what we emit (`.cursor/agents/<name>.md` with YAML frontmatter). The Codex and Gemini bugs above are NOT a "we shipped a uniformly broken format" issue — Cursor accepts it. The other two platforms have format-or-discovery mismatches specific to each.

### 14.5 Documentation/process improvements adopted in this doc revision

- **Claude verification uses `claude plugin ...` CLI form** (not `/plugin ...` slash commands), because the slash commands require the interactive Claude UI; the CLI is scriptable and works in headless containers.
- **Codex verification uses `codex plugin marketplace list`** (not `cat ~/.codex/config.toml | grep`), because the list command is the source of truth for what Codex actually registered.
- **Codex Step 4's clone+cat was deleted** as hollow verification (it inspected a file without invoking Codex — proved nothing about Codex's recognition of the path).
- **Hands-on subagent invocation** added for both Codex and Gemini (`codex` then ask for available subagents; `gemini` then `/agents`) because file-existence checks miss the discovery-loading bugs above.
- **Cursor `/add-plugin` uses `<name>@<url>` form** (not naked URL) because the naked URL triggers Cursor's chat agent into research-spiral mode instead of going to the install UI.
- **Round-2 (2026-05-25)**: per-construct grid expansion. Every cell in the master matrix has either a hands-on test, a documented N/A justification, or an UNKNOWN-method flag for follow-up research.

---

## 15. Discrepancies and unknowns flagged during doc expansion

Surfaced while building the per-construct grid from `docs/PLATFORMS.md` + `docs/ARCHITECTURE.md` + `scripts/platforms.py`. Not for resolution in this doc — these are follow-up items.

### 15.1 Discrepancies between source documents

- **`docs/PLATFORMS.md` Codex "What constructs it supports" table** lists `mcp: yes` with note "manifest emits `mcpServers`", but `docs/ARCHITECTURE.md` "The seven platform classes" row for `CodexPlatform` only lists "skill, mcp, hook, agent". Both agree on MCP, but PLATFORMS.md's note "no per-plugin MCP install command" suggests the consumption pattern is qualitatively different from skill — the matrix marks MCP as TEST but the operator should expect `codex mcp list` to be the only enumeration surface for Codex MCP, distinct from how skills are listed via `codex plugin list`.
- **`docs/PLATFORMS.md` Cursor "What constructs it supports"** marks command/hook/mcp as "manifest-only" (auto-discovered, no Phase 3 mirror) per `CursorPlatform.emit`. The CursorPlatform code at `scripts/platforms.py:283-308` confirms this — Command/Hook have no mirror branch. But `docs/PLATFORMS.md` doesn't document an enumeration surface for these inside Cursor, leaving the verification method UNKNOWN. Flag for follow-up.
- **Devin `supports` discrepancy**: `DevinPlatform.supports = {SkillConstruct}` per `scripts/platforms.py:386`, but `docs/PLATFORMS.md` Devin "What constructs it supports" lists rule and mcp as `yes (via Cursor/Windsurf mirrors)` and `yes` (CLI-managed). The `supports` set is "what gets a per-plugin Devin manifest emitted" — not "what Devin reads." The matrix treats this with footnote 6 (rule) and 16 (mcp); the operator should be aware these are read-via-other-mirrors, not Devin-native plugin install.

### 15.2 Unknown verification methods (gaps for the next research round)

These are cells in the matrix marked TEST but where no clean hands-on verification command is documented for the platform:

- **Claude lsp / monitor / output-style / theme** — example plugins exist, but `lsp-example` etc. may not configure a real language/event, making the "Expected" observation unreliable. Hands-on test is best-effort; full coverage may require richer example plugins.
- **Codex hook enumeration** — no `codex hooks list` command captured in our docs. Hook firing is the only observable.
- **Codex rule activation surface** — no documented "list active rules" command. Rule presence is verified via filesystem; rule effect is qualitative.
- **Gemini hook enumeration** — no `gemini hooks list` command. File presence + JSON validity is the minimum signal.
- **Cursor IDE command / hook enumeration** — Cursor has no documented "list registered commands/hooks" surface for plugin-installed constructs.
- **Cursor CLI agent / command / hook dispatch** — `agent --help` (per `logs/CU3.txt`) lists `mcp`, `models`, `generate-rule`, but no plugin-construct subcommand.
- **Windsurf hook trigger** — no CLI for introspection; verification is "observe Cascade-triggered side effect."
- **`agents` CLI per-platform spray default behavior** — the per-construct project-scope tests assume the CLI's default mode sprays to `.cursor/`, `.windsurf/`, etc. alongside `.agents/`. The exact spray policy per construct type isn't fully documented; verify empirically.
- **Cursor `/add-plugin` with `?ref=<branch>` query parameter** — undocumented in Cursor's published docs; not verified in this repo's evidence. If you try `/add-plugin <name>@https://github.com/DgxSparkLabs/marketplace?ref=main` in Cursor and observe whether it installs from the branch or silently falls back to default, report your finding. The Dashboard team-marketplace import flow has a separate branch-selector UI per `docs/PLATFORMS.md` Cursor "From GitHub (specific branch)" — that path is the verified one.

These gaps suggest the next research pass should focus on:
1. Per-platform enumeration commands for each construct type (especially Cursor command/hook/MCP listing, Codex hooks listing, Gemini hooks listing).
2. The `agents` CLI's default spray policy per construct type.
3. Whether `lsp-example`, `monitor-example`, `output-style-example`, `theme-example` example plugins are configured for observable end-to-end testing or are illustrative-only.
