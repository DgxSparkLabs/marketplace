# Cross-Platform Install + Content Verification — Ground Truth (May 2026)

**Date**: 2026-05-24
**Status**: Verification complete; no changes proposed yet.
**Source artifacts** (all in this directory):
- [[cursor.md]] — Cursor IDE + CLI research (WebFetch evidence, May 2026 only)
- [[empirical_act_verification.md]] — act-based hermetic verification of 18 install/enumeration claims
- [[reproduce.ps1]] — full reproduction script
- `workflows/verify-{codex,gemini,cursor,claude}.yml` — verification scaffolds (not in `.github/workflows/`)
- `logs/*.log` and `logs/<claim-id>.txt` — per-claim evidence

Plus supporting context:
- `docs/EMPIRICAL_CLI_FINDINGS/` — May 22 baseline (Devin + Windsurf empirical, Codex/Gemini blocked at the time)

---

## Per-platform install story (what's true today)

| Platform | Marketplace registration | Per-plugin install | Content (skill) auto-discovery | Gap to native GitHub install |
|----------|---------------------------|--------------------|--------------------------------|------------------------------|
| **Claude Code** | PASS — `claude plugin marketplace add ./` (CL1) | PASS — `claude plugin install <p>@<m> --scope project` (CL2) + `list` shows it (CL3) | N/A — installs explicitly | None — fully working today |
| **Codex** | PASS local (C1), PASS GitHub shortform WITH `--ref feat/claude-plugin-compliance` (C3), FAIL shortform without `--ref` (C2) | **FAIL** — `codex plugin add skill-example@dgxsparklabs-marketplace` errors `missing or invalid plugin.json` (C5) | Reads our marketplace.json fine; enumerates all 81 plugins (C4) | (a) Default branch (`main`) doesn't have manifest at root that Codex accepts → C2 fails. PR #1 merge to main would fix C2. (b) Per-plugin manifest format mismatch — `.claude-plugin/plugin.json` not accepted; exact required path unconfirmed (C7 partial) |
| **Gemini** | PASS local (`./.gemini/` G1), **FAIL GitHub URL** (G2), FAIL even with `--ref` (G3) | PASS via local install (G5 = listed, G6 = skills discoverable). No remote-install path verified. | PASS at runtime — auto-discovers `.gemini/skills/` from cwd | `gemini-extension.json` is at `.gemini/gemini-extension.json` but Gemini expects it at **repo root** for GitHub-URL install |
| **Cursor IDE** | Via Dashboard team-marketplace import (admin) or `/add-plugin` in editor chat | IDE-only; no CLI install command | Reads `.agents/skills/`, `.cursor/skills/`, `.claude/skills/`, `.codex/skills/` natively | None as a *feature*; we just need a `.cursor-plugin/marketplace.json` if we want team-marketplace import to work (we don't have one) |
| **Cursor CLI (`agent`)** | N/A — CLI has no plugin commands | N/A | Implicit via `~/.cursor/cli-config.json` + rules paths | `--plugin-dir <path>` flag exists for runtime injection; no install/list subcommands |
| **Windsurf** | No CLI exists | N/A | Auto-discovers `.windsurf/skills/<name>/SKILL.md` AND `.agents/skills/<name>/SKILL.md` per official docs | We emit neither — 26 skills are invisible to Windsurf users today |
| **Devin** | No marketplace; clone-only | N/A | Auto-discovers `.devin/skills/` + `.agents/skills/` (confirmed by `devin skills paths` in May 22 empirical) | None — current story works; `.agents/skills/` could retire `.devin/skills/` mirror |

---

## Cross-cutting findings

### Finding 1: The `.agents/` directory is a real convergence — but only for content, not for marketplaces

Confirmed (each from a primary doc with fetch date in source artifacts):

- **Windsurf** reads `.agents/skills/<name>/SKILL.md` (project) and `~/.agents/skills/<name>/SKILL.md` (user). [docs.windsurf.com/windsurf/cascade/skills, 2026-05-24]
- **Cursor** reads `.agents/skills/<name>/SKILL.md` as primary project-level skill path. [cursor.com/docs/context/skills, 2026-05-24]
- **Devin** reads `.agents/skills/` at project scope. [`devin skills paths` empirical, 2026-05-22]
- **Codex marketplace** lookup includes `.agents/plugins/marketplace.json` as a canonical path per docs [developers.openai.com/codex/plugins/build, 2026-05-24] — but the act test (C3) showed `.claude-plugin/marketplace.json` works fine for registration too (legacy-compatible).

For **plugin marketplaces** (not skills), there is no `.agents/` convergence. Each platform uses its own path:
- Claude → `.claude-plugin/marketplace.json` + `.claude-plugin/plugin.json`
- Codex → either `.agents/plugins/marketplace.json` (canonical) or `.claude-plugin/marketplace.json` (legacy)
- Cursor → `.cursor-plugin/marketplace.json` (Cursor team-import expects this at repo root)

### Finding 2: My prior local probe of Codex was wrong about enumeration

In an earlier sub-step of this investigation I claimed `codex plugin list` returned ZERO of our plugins after `codex plugin marketplace add .` succeeded. The hermetic act run **refutes** this:

> `Marketplace 'dgxsparklabs-marketplace'`
> `/mnt/c/Users/devic/source/marketplace/.claude-plugin/marketplace.json`
> `... skill-example@dgxsparklabs-marketplace not installed ...`
> `... bundle-skill-all@dgxsparklabs-marketplace not installed ...`
> `... C4_FOUND=YES`

All 81 plugins are listed. The local probe was in a polluted state (possibly registered against a stale path before the latest generator run). Lesson: hermetic > host.

### Finding 3: The actual install gap is the per-plugin manifest, not the marketplace manifest

Codex enumerates fine (C4) but `codex plugin add` fails (C5) with `missing or invalid plugin.json`. The marketplace-level manifest (`.claude-plugin/marketplace.json`) is accepted by Codex as legacy-compatible. The per-plugin manifest (`.claude-plugin/plugin.json` inside each plugin's subdirectory) is NOT — Codex needs a `plugin.json` at some location it accepts (exact path remains unconfirmed by the act run; likely `.codex-plugin/plugin.json` per the WebFetch docs but not verified live).

### Finding 4: Gemini's two GitHub-install codepaths have different failure modes

- **`gemini extensions install <github-url>`** fails because `gemini-extension.json` is expected at the cloned repo root (`/tmp/gemini-ext.../gemini-extension.json`), not in a subdirectory. There is no `--path` option on `extensions install` to redirect this. (G2, G3)
- **`gemini skills install <github-url> --path _generated/skill-example`** correctly navigates to the sub-path but then fails with "No valid skills found … Ensure a SKILL.md file exists with valid frontmatter." The `--path` IS recognized; remote-install validation rejects our SKILL.md frontmatter format for unknown reasons. (G4)

Notably, the same skill installs and is discoverable when installed via the local extension path (G5, G6) — so the SKILL.md format isn't intrinsically broken; Gemini's remote-skill-install validation is stricter than its local-extension-install validation.

### Finding 5: Cursor CLI binary IS `agent` — prior empirical doc was wrong

The May 22 doc said "no CLI exists." Verified false: `agent --version` returns `2026.05.20-2b5dd59`. Binary at `~/.local/bin/agent` (symlink) and `~/.local/share/cursor-agent/versions/<v>/cursor-agent` (real). Prior CI failure was a `$PATH` issue. (CU1, CU2)

The `agent` CLI has NO `plugin install`, `plugin list`, `marketplace add`, or `add-plugin` subcommand. Plugin install in Cursor is editor-only or admin-Dashboard-only. The CLI does expose `--plugin-dir <path>` for runtime injection of a local plugin dir — useful for testing, not for installation. (CU3)

---

## What changed our understanding

Compared to the original research-agent report (pre-verification):

| Original claim | Actually true? |
|----------------|----------------|
| "Codex GitHub shortform works like Claude" | Half-true — works WITH `--ref`; fails without (because default branch doesn't have a manifest Codex accepts at root yet) |
| "Codex enumeration silently fails" | WRONG — enumeration works; only per-plugin install fails |
| "Codex requires `.codex-plugin/plugin.json`" | Likely true per WebFetch docs but live tests only confirmed "current per-plugin layout fails"; exact required path unconfirmed |
| "Gemini supports GitHub URL install" | Half-true — the command is real and accepts URLs, but our manifest layout makes install fail |
| "Cursor has no CLI" | WRONG — binary `agent` exists, just doesn't have plugin commands |
| "Cursor reads `.agents/skills/`" | CONFIRMED via docs |
| "Cursor reads `.agents/plugins/`" | WRONG — Cursor uses `.cursor-plugin/marketplace.json` |
| "Windsurf reads `.windsurf/skills/` and `.agents/skills/`" | CONFIRMED via official docs |
| "Our compat-marketplace-add.yml Codex job proves the integration works" | WRONG — it only proves registration; never tested enumeration or install |

---

## Open questions worth resolving before any code changes

1. **Exact Codex per-plugin manifest path** — `.codex-plugin/plugin.json`? Plain `plugin.json` at plugin root? Could be resolved by creating a tiny test plugin matching the OpenAI docs spec and running `codex plugin add` against it via act.
2. **Whether Gemini's `gemini-extension.json` at the repo root fixes G2/G3** — likely yes; one-shot test: add the file, re-run G2 via act, observe.
3. **Why G4 fails on remote skill install** — is it the frontmatter? a missing pointer in our SKILL.md? Worth a focused probe; not a blocker.
4. **Whether PR #1 merging to main would let C2 pass** without any other change — yes per analysis; `--ref` is only required because default branch (main) lacks the manifest. Untested but follows directly from C3 PASS + C2 FAIL on same shortform.

---

## What's NOT in this synthesis (deliberately deferred)

- **Change proposals.** Per direction: "after we have all the information... we will discuss changes." This document is the ground truth; the change discussion follows.
- **Implementation plans.** Same reason.
- **Re-running compat-*.yml in production CI** with the new assertions discovered here. Would require updating `.github/workflows/`; that's a change discussion item.

---

## How to extend this verification

If new claims need verification:
1. Add a step to the appropriate `workflows/verify-*.yml` with `continue-on-error: true`.
2. Re-run `act` per the reproduce.ps1 commands; logs land in `logs/`.
3. Extract a per-claim snippet to `logs/<ID>.txt` with claim text, status, key evidence, and analysis.
4. Append the row to the table in `empirical_act_verification.md`.
5. Update the corresponding row(s) in this SUMMARY.md.
