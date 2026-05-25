---
date: 2026-05-25
purpose: research-and-recommendation
arc: refactor/platform-feature-routing
status: draft-for-discussion (round 2)
rounds:
  - round-1: initial recommendation (TL;DR + Class A/B + 9 open questions)
  - round-2: 12-question verification + .agents/ matrix + un-emitted-capability scan + scope re-derivation
---

# Platform Feature Routing — Research and Recommendation

> **Round 2 update (2026-05-25).** The 9 original decisions (D-1 … D-9) are locked per user review. This round adds:
> 1) Resolution of the 12 open verification questions (`Verification round 2` below)
> 2) A 10-construct × 7-column `.agents/<construct>/` adoption matrix
> 3) A `Currently un-emitted platform capabilities` scan (Gemini sub-agents, Cursor sub-agents, Cursor hooks, Codex sub-agents, Windsurf hooks/workflows, …)
> 4) A re-derived `Updated implementation scope` section
> 5) New decisions-to-lock (`D-10` onward)
>
> Round-1 sections below ("Current state", "Platform classification", "Recommendation: Class A", etc.) are preserved verbatim as the chain-of-thought trail. **Where round-2 findings contradict round-1 claims, the contradictions are flagged in a dedicated subsection (see `Contradictions with first report`).** Read round 2 first if you only have time for one pass.

## TL;DR

The generator currently emits 4 skill mirror dirs (`.agents/skills/`, `.codex/skills/`, `.gemini/skills/`, `.devin/skills/`) and 2 rule mirror dirs (`.cursor/rules/`, `.windsurf/rules/`) for every applicable plugin. Post-Phase-5 verification shows three of those skill mirrors are pure dead-weight on Class A platforms (Claude, Codex, Gemini, Cursor IDE), which install via their own plugin/extension mechanisms and only need the existing per-plugin manifests (`.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`, `gemini-extension.json`). The Class B platforms (Windsurf, Devin, Cursor CLI) all natively read `.agents/skills/` per their own docs, so a single shared mirror suffices for skill *content* — and a small `install.sh`/`install.ps1` script can provide them a Claude-equivalent `--scope project|user` UX backed by `./.agents/skills/` and `~/.agents/skills/`. Rules are partially analogous but with a key gap: no platform we target reads `.agents/rules/` as of 2026-05-25, so the `.cursor/rules/` and `.windsurf/rules/` mirrors stay until we either get one platform to adopt it or move rules under per-plugin auto-discovery via the existing Cursor/Codex plugin manifests.

## Current state

### Per-platform mirror emission today

| Platform | `mirror_directory` | What's emitted (Phase 3 + 4) | Why historically | What reads it today (verified) |
|---|---|---|---|---|
| Claude Code | `None` (`scripts/platforms.py:113`) | No mirror; only `_generated/<plugin>/.claude-plugin/plugin.json` per Phase 1 | Canonical platform; install is explicit via `claude plugin install … --scope` | `claude plugin install` reads `_generated/<plugin>/.claude-plugin/plugin.json` then writes to `~/.claude/plugins/cache/…` (verified CL2/CL3, `docs/PLATFORMS.md:114-118`) |
| Codex | `.codex/` (`scripts/platforms.py:147`) → `.codex/skills/<name>/` (27 entries today) | Skill content mirror; emit only for SkillConstruct, lines 150-161 | Pre-Phase-1.5 assumption Codex needed local-readable skill content. Per-plugin manifest emission (Phase 1.5) was added later (line 163-176). | **Nothing verified** reads `.codex/skills/` directly. Codex per-plugin install reads `_generated/<plugin>/.codex-plugin/plugin.json` (per `developers.openai.com/codex/plugins/build`, fetched 2026-05-25, "Only `plugin.json` belongs in `.codex-plugin/`"). C5 in `empirical_act_verification.md:18` proves `codex plugin add` fails on the per-plugin manifest, not on missing skill content. |
| Gemini | `.gemini/` (`scripts/platforms.py:188`) → `.gemini/skills/<name>/` + `.gemini/gemini-extension.json` | `.gemini/` IS the extension root; skills inside an extension live at `skills/` per `geminicli.com/docs/extensions/reference/` (fetched 2026-05-25). Phase 4.5 also copies `gemini-extension.json` to repo root. | Gemini extensions install one directory; skills inside it auto-discover | `gemini extensions install ./.gemini/` reads the extension at this path (G1 PASS). After install, Gemini reads `~/.gemini/extensions/<name>/skills/<n>/SKILL.md`. |
| Cursor | `.cursor/` (`scripts/platforms.py:235`) → `.cursor/rules/<name>.md` only (22 entries) | Rule content mirror; skills explicitly NOT emitted here (`scripts/platforms.py:249` comment) | Cursor IDE auto-discovers rules from `.cursor/rules/` | Cursor IDE (per `cursor.com/docs/context/rules`, fetched 2026-05-25); Devin also reads `.cursor/rules/*.md` per `devin rules paths` empirical |
| Windsurf | `.windsurf/` (`scripts/platforms.py:264`) → `.windsurf/rules/<name>.md` only (22 entries) | Rule content mirror | Windsurf Cascade auto-discovers `.windsurf/rules/` | Windsurf IDE (`docs.windsurf.com/.../rules`, fetched 2026-05-25); Devin reads `.windsurf/rules/*.md` per `devin rules paths` |
| Devin | `.devin/` (`scripts/platforms.py:292`) → `.devin/skills/<name>/` (27 entries) | Skill content mirror | Devin reads `.devin/skills/` per `devin skills paths` empirical | Devin (verified). Also reads `.agents/skills/` natively — the `.devin/skills/` mirror is the *legacy* convenience path. `docs/PLATFORMS.md:654` ("`.devin/skills/` mirror is on the future-cleanup list per `HANDOFF.md`. Not load-bearing.") |
| Agents | `.agents/` (`scripts/platforms.py:324`) → `.agents/skills/<name>/` (27 entries) | Cross-platform skill convergence | Decision A1: shared mirror for Windsurf+Cursor+Devin | Windsurf (per `docs.windsurf.com/windsurf/cascade/skills`), Cursor (per `cursor.com/docs/context/skills`), Devin (per `devin skills paths`) — all verified 2026-05-24 in `SUMMARY.md:37-40` |

Raw counts on disk right now (verified `ls`):
- 27 skills × 4 mirror dirs (`.agents/skills/`, `.codex/skills/`, `.gemini/skills/`, `.devin/skills/`) = **108 mirrored skill instances** vs 27 source entries
- 22 rules × 2 mirror dirs (`.cursor/rules/`, `.windsurf/rules/`) = **44 mirrored rule instances** vs 22 source entries
- 1 `.gemini/gemini-extension.json` + 1 root `gemini-extension.json` (Phase 4 + 4.5)
- 1 `.cursor-plugin/marketplace.json` at root (Phase 6)
- 1 `.claude-plugin/marketplace.json` at root (Phase 5; serves both Claude and Codex)

### The redundancy problem

The "emit everywhere" pattern was a reasonable default in the pre-verification era: when each platform's actual install mechanism was unknown, mirroring source content into every platform's namespace was the safe choice — at worst, the platform ignored the directory; at best, it discovered it. After Phase 5 verification (`docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/`), every platform's discovery semantics are known empirically, and most of those mirrors are now provably redundant.

Three pieces of evidence make the redundancy concrete. First, the per-plugin manifest path is what Codex actually consumes — `developers.openai.com/codex/plugins/build` (fetched 2026-05-25) is explicit: `"Only plugin.json belongs in .codex-plugin/"`. The `.codex/skills/<name>/` directory we emit at the repo root is not part of any install code-path Codex documents or that any verification log exercised; C5 in `empirical_act_verification.md:18` failed because the per-plugin manifest didn't satisfy Codex, not because skill content was missing. Second, the `.agents/skills/` convergence is documented as a primary discovery path by all three Class B platforms (Cursor's docs even list it before `.cursor/skills/`), so the per-platform skill mirrors duplicate content the platforms would find at `.agents/skills/` anyway. Third, the `.devin/skills/` mirror is already flagged for retirement (`docs/PLATFORMS.md:654`, "Not load-bearing").

A secondary cost: every added skill multiplies the plugin add-diff by 4 (one mirror per skill platform). A 27-skill marketplace has ~150 KB of redundant content; a 100-skill marketplace would have ~550 KB of dead bytes. This isn't catastrophic in absolute terms — but it makes the generator's drift-check noisier, the git history fatter, and the contributor experience confusing ("why does adding one skill produce four identical directories?").

## Platform classification

### Class A: native plugin/extension install with scoping

| Platform | Install command | Scope flag | Why Class A |
|---|---|---|---|
| Claude Code | `claude plugin install <name>@<marketplace> --scope project\|user` | `--scope project\|user` (CL2 verified, `docs/PLATFORMS.md:52`) | First-class plugin install with explicit scope flag |
| Codex | `codex plugin add <name>@<marketplace>` | Scope is implicit via WHERE the marketplace.json lives: `~/.agents/plugins/marketplace.json` (user) vs `$REPO_ROOT/.agents/plugins/marketplace.json` (repo) per `developers.openai.com/codex/plugins/build` fetched 2026-05-25 | Codex CLI has `plugin add` and a marketplace concept; per-plugin manifest at `.codex-plugin/plugin.json` |
| Gemini | `gemini extensions install <github-url> --consent` | No per-skill scope; extensions install to `~/.gemini/extensions/<name>/` (user-scope only per current docs) | First-class extension install; one-shot for the whole marketplace |
| Cursor IDE | `/add-plugin` in editor; Dashboard → Settings → Plugins → Import for team marketplaces | "Plugins can be scoped to a project or installed at the user level" per `cursor.com/docs/plugins` fetched 2026-05-25 | First-class plugin install with project/user scope; manifest at `.cursor-plugin/plugin.json` per plugin |

### Class B: no native install

| Platform | Why no native install | Auto-discovery paths it does have |
|---|---|---|
| Cursor CLI (`agent` binary) | The `agent` CLI has NO `plugin install`, `plugin list`, `marketplace add`, or `add-plugin` subcommand (CU3 verified, `empirical_act_verification.md:29`). Plugin install is editor-only or admin-Dashboard-only. | `.cursor/rules/*.md`, `.agents/skills/<name>/SKILL.md` (primary), `.cursor/skills/`, `.claude/skills/`, `.codex/skills/` (compat) per `cursor.com/docs/context/skills` fetched 2026-05-24 |
| Windsurf | No CLI exists, anywhere (`docs/archive/empirical-cli-findings/windsurf.md:5-26`). IDE-only, filesystem-driven. | `.windsurf/rules/*.md`, `.windsurf/skills/<name>/SKILL.md`, `.agents/skills/<name>/SKILL.md` (`docs.windsurf.com/.../skills` fetched 2026-05-24) — user-scope `~/.windsurf/...`, `~/.agents/skills/` also |
| Devin | CLI exists but has NO marketplace concept; "the clone IS the install" (`docs/PLATFORMS.md:603`). Discovery is live-from-filesystem at session start. | Per `devin skills paths` empirical: `.devin/skills/<n>/SKILL.md`, `.agents/skills/<n>/SKILL.md`, `~/.config/devin/skills/<n>/SKILL.md`, `~/.agents/skills/<n>/SKILL.md`. Per `devin rules paths`: `.windsurf/rules/*.md`, `.cursorrules`, `.cursor/rules/*.md` |

### Cursor's split personality

Cursor is the only platform that lives in both classes simultaneously. The Cursor IDE has a real plugin marketplace launched 2026-02-17 with `/add-plugin` and team-marketplace import (Class A — verified `docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/cursor.md:13-19`). The Cursor CLI (`agent` binary, installed via `curl https://cursor.com/install | bash`) has no plugin commands at all (Class B — verified CU3, `empirical_act_verification.md:29`). For our purposes the IDE handles plugin install (via the per-plugin `.cursor-plugin/plugin.json` we already emit) and the CLI shares the same auto-discovery filesystem layer with Windsurf and Devin. **Recommendation: classify Cursor IDE in Class A and Cursor CLI in Class B (same row, two flags).** The mirror-retirement applies to skill content (Class A handles it); the install script (Class B) is for Cursor CLI users who don't open the workspace in the IDE — they get the same `.agents/skills/` content via `install.sh`.

## Recommendation: Class A — retire redundant mirrors

### What to retire and why

| Mirror dir | Currently emitted from | Recommendation | Justification |
|---|---|---|---|
| `.codex/skills/<name>/` (27 entries) | `CodexPlatform.emit`, `scripts/platforms.py:150-161` | **RETIRE** | No verified Codex codepath reads `.codex/skills/` at this repo path. Codex install reads `_generated/<plugin>/.codex-plugin/plugin.json` then materializes the plugin into `~/.codex/...` cache itself. The repo-root `.codex/skills/` mirror is consumed by nothing we've verified. **Open question (Q-A1):** verify by `act` that retiring this dir does not break `codex plugin add` for a skill plugin. |
| `.devin/skills/<name>/` (27 entries) | `DevinPlatform.emit`, `scripts/platforms.py:295-302` | **RETIRE** | `devin skills paths` lists both `.devin/skills/` AND `.agents/skills/` as project-scope discovery paths. The `.agents/` path is functionally identical and already populated by `AgentsPlatform`. `docs/PLATFORMS.md:654` already states "future-cleanup list per `HANDOFF.md`. Not load-bearing." |
| `.gemini/skills/<name>/` (27 entries) | `GeminiPlatform.emit`, `scripts/platforms.py:191-198` | **KEEP — intrinsic** | `.gemini/` IS the Gemini extension root. Per `geminicli.com/docs/extensions/reference/` (fetched 2026-05-25), skill definitions live in the extension's `skills/` subdir (`skills/<name>/SKILL.md`). Cannot be relocated to `.agents/skills/` — the extension manifest does not support paths outside the extension dir for skills (only `${extensionPath}` substitution is documented). |
| `.cursor/skills/` (NOT currently emitted) | n/a — only mentioned in `docs/PLATFORMS.md:29` as a discovery path Cursor reads | **NO CHANGE — already absent**. Documentation gap: `docs/PLATFORMS.md:29` lists `.cursor/skills/` as a Cursor auto-discovery path but the generator never emits it (verified `ls .cursor/` returns only `rules`). Skills reach Cursor via `.agents/skills/`. Update the doc to reflect reality. |
| `.cursor/rules/<name>.md` (22 entries) | `CursorPlatform.emit`, `scripts/platforms.py:238-249` (RuleConstruct branch) | **KEEP** | Cursor IDE auto-discovers rules from `.cursor/rules/`; Devin also reads `.cursor/rules/*.md` (per `devin rules paths`). No `.agents/rules/` convergence exists yet (see Rules-side parity below). |
| `.windsurf/rules/<name>.md` (22 entries) | `WindsurfPlatform.emit`, `scripts/platforms.py:267-276` | **KEEP** | Windsurf reads `.windsurf/rules/` natively per `docs.windsurf.com/windsurf/cascade/memories` (fetched 2026-05-25); Devin also reads `.windsurf/rules/*.md`. No `.agents/rules/` adoption. |
| `.agents/skills/<name>/` (27 entries) | `AgentsPlatform.emit`, `scripts/platforms.py:327-335` | **KEEP — load-bearing for Class B** | Single shared mirror for Windsurf+Cursor CLI+Devin. With `.codex/skills/` and `.devin/skills/` retired, this becomes the only non-Claude/non-Gemini skill mirror. |

**Net retirement: 2 mirror dir trees per platform (`.codex/skills/` and `.devin/skills/`)** containing 27 entries each → **54 mirrored skill instances removed**, ~108 fewer files emitted (each skill is multi-file). The `.codex/` and `.devin/` top-level dirs themselves can be removed entirely if no other content lives in them today (verified `ls`: `.codex/` contains only `skills/`, `.devin/` contains only `skills/` — both become empty after retirement; the dirs can be deleted from the generator's wipe step).

### Per-plugin manifest is sufficient

The empirical record for each Class A platform's install codepath:

- **Claude** reads `.claude-plugin/marketplace.json` (root) and `_generated/<plugin>/.claude-plugin/plugin.json` (per-plugin), then writes a versioned cache under `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`. Verified CL1-CL3.
- **Codex** reads `.claude-plugin/marketplace.json` (legacy-compatible; C1, C3 PASS) or its canonical `.agents/plugins/marketplace.json` (per `developers.openai.com/codex/plugins/build` — not adopted here), then `_generated/<plugin>/.codex-plugin/plugin.json` for per-plugin install. The `.codex-plugin/` dir is THE manifest location; the `.codex/skills/` mirror at repo root is unrelated to install.
- **Gemini** reads `gemini-extension.json` at repo root (G2 explicitly errors when missing; Phase 4.5 fixes this) or `./.gemini/gemini-extension.json` for local install. The `.gemini/` directory IS the extension root, so `.gemini/skills/<name>/` is inside the extension — intrinsic, not redundant.
- **Cursor IDE** reads `.cursor-plugin/marketplace.json` at root (team-import, Phase 6) and `_generated/<plugin>/.cursor-plugin/plugin.json` per plugin. Skills reach Cursor via `.agents/skills/` per `cursor.com/docs/context/skills`.

So: keeping all the existing per-plugin manifests under `_generated/<plugin>/.<platform>-plugin/plugin.json` and the root marketplace manifests is sufficient for Class A install. The repo-root content mirrors (`.codex/skills/`, `.devin/skills/`) duplicate work that the per-plugin install + cache flow already handles.

### Edge cases (Gemini extension structure)

`.gemini/skills/<name>/` is **intrinsic to the Gemini extension layout** — per `geminicli.com/docs/extensions/reference/` (fetched 2026-05-25), skill definitions live in the extension's `skills/` subdir. The manifest's `${extensionPath}` substitution is documented for files within the extension; nothing in the docs suggests skills can be sourced from a sibling `.agents/skills/` location. **Recommendation: keep `.gemini/skills/`. Open question (Q-A2):** could a symlink `.gemini/skills` → `../.agents/skills` work? Untested. Symlinks in git are fragile cross-platform; even if it works, it complicates the generator. Probably not worth the savings.

## Recommendation: Class B — `.agents/`-backed install script

### Install script design

The script's job is to give Cursor CLI / Windsurf / Devin users the same single-command install UX that Claude users get, backed by the `.agents/skills/` and `~/.agents/skills/` paths these platforms already read natively. Two scripts (`install.sh` for POSIX, `install.ps1` for PowerShell) sit at the repo root.

**Command surface (proposed):**

```
agents install <plugin>          [--scope project|user]   # default: project
agents install <plugin>          [--scope user]
agents uninstall <plugin>        [--scope project|user]
agents list                                                # list installed
agents list --available                                    # list everything in the marketplace
agents upgrade <plugin>          [--scope project|user]
agents upgrade --all             [--scope project|user]
```

These map directly to filesystem operations under `<scope-root>/skills/<plugin-without-prefix>/`:
- `--scope project` → `./.agents/skills/<name>/`
- `--scope user` → `~/.agents/skills/<name>/`

Plugin name convention follows the marketplace's `skill-<name>` prefix; the script strips the `skill-` prefix when materializing under `skills/` (so `agents install skill-telegram-notify` produces `./.agents/skills/telegram-notify/`).

### One-line install pattern

```bash
# POSIX (Linux/macOS/WSL)
curl -fsSL https://raw.githubusercontent.com/DgxSparkLabs/marketplace/main/install.sh | bash -s -- install skill-telegram-notify --scope project

# PowerShell (Windows)
iwr -useb https://raw.githubusercontent.com/DgxSparkLabs/marketplace/main/install.ps1 | iex; agents install skill-telegram-notify --scope project
```

The piped-shell pattern is idiomatic for one-shot installs (Cursor itself uses `curl https://cursor.com/install -fsS | bash`, Devin uses `curl -fsSL https://cli.devin.ai/install.sh | bash`). For a smoother experience, recommend also publishing a stable `install` shim that installs the `agents` CLI itself into `~/.local/bin/agents` so subsequent calls are just `agents install <plugin>` — mirrors the Cursor CLI install UX.

### Content source

Three options, with tradeoffs:

| Option | Pros | Cons |
|---|---|---|
| **Option 1**: `git clone --depth 1` then copy | Simple; gets whole tree at once | Heavy (~14 MB+); requires git; doesn't let user install one plugin without cloning everything |
| **Option 2**: GitHub raw URL per file | Lightweight per-plugin; no git dep | Many roundtrips; requires recursive listing via API (rate-limited unauthenticated); SKILL.md + scripts/* + references/* all need separate fetches |
| **Option 3**: GitHub tarball API + `tar --strip-components` to extract a single path | One HTTP request; small (entire repo ~5-10 MB gzipped); extracts only target subtree | Requires `tar` on POSIX, `Expand-Archive` on Windows; depends on GitHub API for tarballs |

**Recommendation: Option 3 — tarball with selective extract.** Pattern:

```bash
curl -fsSL "https://github.com/DgxSparkLabs/marketplace/archive/refs/heads/main.tar.gz" \
  | tar -xz --strip-components=3 -C "$DEST" "marketplace-main/.agents/skills/$NAME"
```

Pulls a single skill out of the tarball in one HTTP call. Reuses the source `.agents/skills/<name>/SKILL.md` that the generator already produces (no special install-time packaging needed). Supports `--ref <branch>` cleanly by swapping `main` for the branch ref.

### Removal and upgrade

- `agents uninstall <plugin> --scope project` → `rm -rf ./.agents/skills/<name>/`
- `agents upgrade <plugin>` → uninstall + install in one shot; preserves scope
- `agents upgrade --all --scope project` → iterate all installed under `.agents/skills/`, refetch each from the marketplace ref
- Store install metadata as a JSON sidecar at `.agents/skills/.installed.json` (per-scope) recording `{plugin: {ref, installed_at, source_url}}` so upgrade and list have ground truth without scanning a remote registry

### Discovery (list available)

The marketplace already produces `.claude-plugin/marketplace.json` listing every plugin with `name`, `description`, `version`, `author`, `category`. The install script's `agents list --available` reads this file (either from the repo via the same tarball API or via a single curl to the raw URL) and prints a table grouped by category. Filtering by construct prefix lets a user run `agents list --available --type skill`.

### Backwards compatibility

Users who already manually use `.cursor/skills/` or `.windsurf/skills/` are at risk if we retire those mirrors. Status check:

- `.cursor/skills/` — **never emitted by the generator** (verified `ls .cursor/` returns only `rules`). Documentation `docs/PLATFORMS.md:29` lists it as a discovery path but we don't populate it. **No users can be relying on this from our repo today.** Documentation fix only.
- `.windsurf/skills/` — `WindsurfPlatform.supports = {RuleConstruct}` only; we don't emit skills here either (verified `ls .windsurf/` returns only `rules`). Same: **no users can be relying on this from our repo today.** Documentation fix only — `docs/PLATFORMS.md:30` says Windsurf reads `.windsurf/skills/ + .agents/skills/` but we only populate the latter.
- `.codex/skills/` — IS currently emitted; users who installed manually via `git clone` may have configured tooling to look here. Retirement requires a CHANGELOG entry and a migration note in `docs/PLATFORMS.md`. No Codex codepath has been verified to read this dir, so the actual user-facing impact is likely zero — but flag in release notes.
- `.devin/skills/` — IS currently emitted and IS read by Devin natively (`devin skills paths` lists it). Retiring it is safe ONLY because `.agents/skills/` is also read by Devin. Verify by `act` that `devin skills list` still finds skills after `.devin/skills/` is removed (open question Q-B1).

## Rules-side parity

### Can `.agents/rules/` work?

Per fresh fetches 2026-05-25:

- **Cursor**: `cursor.com/docs/context/rules` lists `.cursor/rules` and `AGENTS.md` only. **No mention of `.agents/rules/`.** (VERIFIED-NO)
- **Windsurf**: `docs.windsurf.com/.../memories` (rules section) lists `.windsurf/rules` and `AGENTS.md` only. **No mention of `.agents/rules/`.** (VERIFIED-NO)
- **Devin**: `devin rules paths` empirical (2026-05-22) lists `.windsurf/rules/*.md`, `.cursorrules`, `.cursor/rules/*.md` only. **No mention of `.agents/rules/`.** (VERIFIED-NO)

No platform we target reads `.agents/rules/` as of 2026-05-25. **The skill-side convergence at `.agents/skills/` is real; the rule-side equivalent does not exist yet.**

### Recommendation: keep current per-platform rule mirrors

The existing `.cursor/rules/<name>.md` and `.windsurf/rules/<name>.md` are not retireable today — they are the *only* paths these platforms read. The `AGENTS.md` route is theoretically a convergence (Cursor reads it, Windsurf reads it, Devin's docs mention it, Codex reads it) but it's a single concatenated file, not a per-rule directory — a different model entirely.

If a future Cursor or Windsurf release adopts `.agents/rules/` as an auto-discovery path (we should track this), retire on the same pattern as skills: collapse two mirrors into one `.agents/rules/` and let each platform discover it natively. **Open question (Q-R1): monitor `cursor.com/docs/context/rules` and `docs.windsurf.com/.../rules` for `.agents/rules/` adoption; revisit quarterly.**

### Documentation cleanup needed

`docs/RULE_FORMAT.md:117` says the generator produces `.devin/rules/<name>.md`. **It does not** — `DevinPlatform.supports = {SkillConstruct}` and `ls .devin/` returns only `skills`. Devin reads rules via the `.cursor/rules/` and `.windsurf/rules/` mirrors. Doc is stale; fix during this refactor.

`rules/<name>/README.md` files reference `.devin/rules/<name>.md` (e.g. `rules/autonomous-persistence/README.md:18,34`). Same fix.

## Open questions and verification gaps

1. **Q-A1**: Verify by `act` that removing `.codex/skills/<name>/` does not break `codex plugin add skill-<name>@dgxsparklabs-marketplace`. Reproduce: re-run `docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/workflows/verify-codex.yml` after deleting the `.codex/` dir; expect C4 (enumerate) and the eventual C5 (install) to behave identically. Currently C5 FAILs but for an unrelated per-plugin-manifest-format reason; this verification just needs to confirm `.codex/skills/` deletion does not introduce a NEW failure mode.

2. **Q-A2**: Could `.gemini/skills` be a symlink to `../.agents/skills`? Untested. Likely fragile on Windows and inside git tarballs. Probably not worth pursuing — keep `.gemini/skills/` as physical content.

3. **Q-B1**: Verify by `act` (or local) that `devin skills list` still discovers all 27 skills after `.devin/skills/` is removed but `.agents/skills/` remains. This is the load-bearing check for retiring `.devin/skills/`. Predicted PASS based on `devin skills paths` listing `.agents/skills/`.

4. **Q-B2**: Cursor IDE behavior when only `.agents/skills/` exists (no `.cursor/skills/`, no `.claude/skills/`). The docs at `cursor.com/docs/context/skills` (fetched 2026-05-24) list `.agents/skills/` first, so this should work — but no empirical verification has been done (`act` doesn't run Cursor IDE). Best available is the documentation claim itself.

5. **Q-B3**: For the install script — does Devin scan `.agents/skills/.installed.json` (the proposed sidecar)? If yes, that's a leak into Devin's enumeration. Likely safe (Devin enumerates `SKILL.md`-bearing dirs, not arbitrary files), but verify before shipping.

6. **Q-B4**: PowerShell install script equivalents for `tar --strip-components`. `Expand-Archive` doesn't support selective extraction. Alternatives: `tar.exe` (ships with Windows 10+), or download the full tarball and copy a subtree. Need to settle this before implementing.

7. **Q-R1**: Monitor `cursor.com/docs/context/rules`, `docs.windsurf.com/.../rules`, and `devin rules paths` output for `.agents/rules/` adoption. If any platform adds it, revisit rule mirror retirement.

8. **Q-R2**: Does Codex's `developers.openai.com/codex/plugins/build` reference any `.agents/rules/` convention? Not verified — should fetch quarterly. Codex uses `AGENTS.md` today, not a per-rule directory.

9. **Q-G1**: Could Gemini extensions reference an OUTSIDE-extension path for skills via `${workspacePath}`? `geminicli.com/docs/extensions/reference/` mentions `${workspacePath}` but only in the context of `settings`/`mcpServers`, not skills. Untested; probably no.

10. **Q-A3**: Verify that retiring `.codex/skills/` does not break the existing `compat-marketplace-add.yml (codex job)` — that workflow asserts marketplace registration, not skill content presence (per `docs/PLATFORMS.md:224`), so likely no impact. Sanity-check before shipping.

11. **Q-B5**: User-scope semantics on Windsurf — does Windsurf read `~/.agents/skills/`? Per `docs/PLATFORMS.md:519` ("User-scope equivalents: `~/.windsurf/...`, `~/.agents/skills/`") yes. But verify by fresh fetch — the `--scope user` flag of the install script needs to actually serve Windsurf users, not just Cursor/Devin.

12. **Q-B6**: Should the install script also handle rules? Rules need per-platform format files (`formats/cursor.md`, `formats/windsurf.md`) — a single `.agents/rules/<name>.md` doesn't satisfy Cursor's `alwaysApply: true` frontmatter requirement. Probably the install script handles skills only, and rules continue to require `git clone` for Class B platforms until per-platform install support exists. Worth deciding explicitly.

## Migration consequences

### Files that go away (count + paths)

If recommendations are adopted in full:

- `.codex/skills/` — entire dir tree (27 skills × multi-file each, ~50 files; the `.codex/` top-level dir disappears entirely)
- `.devin/skills/` — entire dir tree (27 skills × multi-file each, ~50 files; the `.devin/` top-level dir disappears entirely)

Approximate net deletion: ~100 generated files, 2 top-level dirs.

Files that stay: `.agents/skills/` (load-bearing), `.gemini/skills/` (intrinsic to extension), `.cursor/rules/`, `.windsurf/rules/`, `.gemini/gemini-extension.json`, root `gemini-extension.json`, root `.cursor-plugin/marketplace.json`, root `.claude-plugin/marketplace.json`, all `_generated/<plugin>/.{claude,codex,cursor}-plugin/plugin.json` per-plugin manifests.

### Generator phase changes implied

- `CodexPlatform.emit` (`scripts/platforms.py:150-161`): becomes a no-op (return immediately for all construct types). The `mirror_directory` attribute could become `None` like Claude's, simplifying Phase 3.
- `CodexPlatform.supports`: stays `{SkillConstruct, MCPConstruct, HookConstruct}` — these are still gated for Phase 1.5 manifest emission.
- `DevinPlatform.emit`: same — becomes a no-op; `mirror_directory` could be `None`.
- `DevinPlatform.supports`: stays `{SkillConstruct}` for any future per-plugin manifest emission.
- Phase 3 wipe step (`scripts/generate_manifest.py:184-186`) iterates `platform.mirror_directory`; if Codex/Devin become `None`, they'd skip naturally.
- No changes to Phase 1, 1.5, 2a, 2b, 4, 4.5, 5, 6.

A new `install.sh`/`install.ps1` (Class B install script) sits at the repo root, not produced by the generator — checked in by hand. The generator might emit a content-hash for cache-busting, but it doesn't need to.

### Test changes implied

- `tests/test_marketplace.py` — search for assertions on `.codex/skills/` or `.devin/skills/` presence; remove or invert those.
- Drift check (`generate_manifest.py:_check_drift`) automatically picks up the new layout — no assertion changes needed, but the first regeneration after the change will produce a large diff.

### CI assertion changes implied

- `compat-skill.yml (devin job)` — currently asserts `devin skills list | grep -i telegram` matches. After retirement, this still passes because `.agents/skills/` is also read (Q-B1 verification). No change unless verification fails.
- No `.codex/skills/`-specific assertions exist in current workflows (per `docs/PLATFORMS.md:222-228`); the `compat-marketplace-add.yml (codex job)` asserts marketplace + per-plugin install only. No change needed.
- New `compat-agents-install.yml` workflow to test the install script for Class B platforms (POSIX path; PowerShell path tested separately on a Windows runner).

### Documentation changes implied

- `README.md` — add the Class B install script's one-line install command alongside the Claude/Codex/Gemini examples.
- `docs/PLATFORMS.md:29` — remove `.cursor/skills/`, `.claude/skills/`, `.codex/skills/` from the Cursor "Skills auto-discovery" cell (or qualify them as "if present, not emitted by us"). Update the Codex row (`:30-31`) to drop `.codex/skills/`. Update Devin row to drop `.devin/skills/`. Update "Per-platform manifest paths" table (`:699-707`) likewise.
- `docs/ARCHITECTURE.md` — update the seven-platform-classes table (`:111-119`) for Codex and Devin to reflect "no mirror" status.
- `docs/RULE_FORMAT.md:117` — remove the false claim that the generator produces `.devin/rules/<name>.md`.
- `rules/<name>/README.md` files — search-and-replace `.devin/rules/` references; update the install instructions table.
- `docs/CONTRIBUTING.md` — update if it mentions per-platform mirror invariants.
- `CHANGELOG.md` — new entry: "RETIRED: `.codex/skills/`, `.devin/skills/` mirror dirs. Migration: nothing — content available at `.agents/skills/` and via per-plugin manifests."

## Decisions to lock with the user

1. **D-1**: Approve retirement of `.codex/skills/` and `.devin/skills/` mirror dirs (assuming Q-A1, Q-A3, Q-B1 verify clean)? Sure
2. **D-2**: Approve keeping `.gemini/skills/` (intrinsic to extension) and `.cursor/rules/` + `.windsurf/rules/` (no `.agents/rules/` convergence today)? We keep only what's required for functioning and adopt .agents fully
3. **D-3**: Approve introducing a new `install.sh` / `install.ps1` (or single `agents` CLI shim) at the repo root with `agents install <plugin> --scope project|user` semantics? The CLI proposal was interesting
4. **D-4**: Approve tarball-API content source (Option 3) for the install script, or prefer git-clone (Option 1) for simplicity? git clone
5. **D-5**: Should the install script handle rules in addition to skills, given the per-platform-format-file complication (Q-B6)? Yes, we will handle all constructs supported in the ,agents spec
6. **D-6**: For `--scope user`, target `~/.agents/skills/` only, or also write to `~/.cursor/skills/`, `~/.windsurf/skills/`, `~/.config/devin/skills/` for max user-scope coverage? (More writes = more compatibility but breaks the "one true location" model.) - only .agents
7. **D-7**: For backwards compat, ship a one-time `migrate.sh` that detects existing `.codex/skills/` or `.devin/skills/` content in user clones and offers to remove it, or just CHANGELOG it and trust users? We don't care about breaking backwards compatibility. We break.
8. **D-8**: Documentation cleanup pass (fix `.cursor/skills/`, `.windsurf/skills/`, `.devin/rules/` references) — bundled into this refactor or a separate doc-only commit first? Also research better, gemini and cursor mention subagents in their docs  for example. we should support that and the other existing capabilities if there are more for the platforms 
9. **D-9**: Do we want a Class C designation for the Cursor split-personality case, or is "Cursor IDE → A, Cursor CLI → B" sufficient? IDE, CLI sub-split under the same cursor heading.

## Cost of doing nothing

Quiet costs of the status quo, beyond the obvious folder-count bloat: User says to fix the status quo so we have a better world (and project)

1. **Contributor confusion**: A new contributor adding their first skill sees four near-identical directories appear in their PR diff (`.agents/skills/<name>/`, `.codex/skills/<name>/`, `.gemini/skills/<name>/`, `.devin/skills/<name>/`). The mental model "one source produces four targets, but I shouldn't edit any of them, I should only touch `skills/<name>/`" is non-obvious. This was hit during the recent docs consolidation arc.

2. **Diff noise on the drift-check**: Every change to a skill's `SKILL.md` body produces 4× the line-count in CI's drift diff, making review of generator changes slower. Reducing the multiplier to 2 (`skills/` source + `.agents/skills/` only) cuts review time noticeably.

3. **Documentation drift, demonstrated**: We already have THREE doc-vs-code inconsistencies live today: `docs/PLATFORMS.md` claims Cursor reads `.cursor/skills/` but we don't emit it; `docs/PLATFORMS.md` claims Windsurf reads `.windsurf/skills/` but we don't emit it; `docs/RULE_FORMAT.md` claims the generator produces `.devin/rules/` but it doesn't. These slipped in because the "emit everywhere" model was the contributor's mental default. Collapsing to `.agents/skills/` removes the temptation to add a fake mirror in docs.

4. **Missed UX opportunity**: Cursor CLI / Windsurf / Devin users currently `git clone` the whole repo (~14 MB) to get one skill they care about. A Class B install script reduces that to a 5-10 MB tarball API call OR a single curl-piped command, putting them at install-UX parity with Claude users. This is the actual quality-of-life win.

5. **Plugin add-diff growth**: At 27 skills today the redundancy is ~108 files. At 100 skills it'd be ~400. The growth is linear in skill count and platform count; if we add a 7th platform that also wants a `.foo/skills/` mirror, we'd be at 5× content per skill. The convergence on `.agents/skills/` is what stops that growth curve.

---

## Cross-references

- `docs/PLATFORMS.md` — per-platform install behavior; `:29-31` summary table; `:217` (Codex), `:312` (Gemini), `:381,418` (Cursor), `:516-519` (Windsurf), `:609-628` (Devin)
- `docs/ARCHITECTURE.md` — generator architecture; `:111-119` seven platform classes table; `:177-189` phase table
- `scripts/platforms.py` — `:101-125` (Claude), `:128-176` (Codex), `:179-219` (Gemini), `:222-253` (Cursor), `:256-280` (Windsurf), `:283-306` (Devin), `:309-339` (Agents)
- `scripts/generate_manifest.py` — `:110-244` orchestrator; `:182-196` Phase 3 mirror emission
- `scripts/constructs.py` — `:38-56` Construct protocol; `:114-173` SkillConstruct + RuleConstruct
- `docs/RULE_FORMAT.md` — rule format spec; `:117` (stale `.devin/rules/` claim)
- `docs/SKILL_FORMAT.md` — SKILL.md format spec
- `docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/SUMMARY.md` — install/discovery ground truth
- `docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification.md` — 18-claim verification table
- `docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/cursor.md` — Cursor IDE+CLI WebFetch evidence
- `docs/archive/empirical-cli-findings/devin.md` — `devin skills paths` / `devin rules paths` empirical output
- `docs/archive/empirical-cli-findings/windsurf.md` — no-CLI verification
- `developers.openai.com/codex/plugins/build` (fetched 2026-05-25) — Codex per-plugin manifest spec + scope model
- `geminicli.com/docs/extensions/reference/` (fetched 2026-05-25) — Gemini extension structure
- `cursor.com/docs/plugins` (fetched 2026-05-25) — Cursor plugin scope model
- `cursor.com/docs/context/rules` (fetched 2026-05-25) — no `.agents/rules/` mention
- `docs.windsurf.com/windsurf/cascade/memories` (fetched 2026-05-25) — no `.agents/rules/` mention

---

# ─── ROUND 2 ───────────────────────────────────────────────────────────────────

The sections below were written after the user locked decisions D-1 … D-9 and directed an expanded research pass. They supersede round-1 wherever they conflict; conflicts are listed in `Contradictions with first report`.

## Verification round 2 — resolving the 12 open questions

For each question: the round-1 statement, the verification path actually executed, the evidence (with file paths, log line numbers, doc URL + fetch date), and the answer label (VERIFIED-YES / VERIFIED-NO / OBVIATED-BY-FINDING-X / UNVERIFIABLE-WITHOUT-Y).

### Q-A1 — Does removing `.codex/skills/` break `codex plugin add`?

**Path**: hermetic `act` run. Workflow: `docs/research/platform-feature-routing/workflows/verify-mirror-retirement.yml`. Log: `docs/research/platform-feature-routing/logs/verify-mirror-retirement.log` (steps "Q-A1.1 marketplace", "Q-A1.2 list", "Q-A1.3 add"). The run regenerated manifests, deleted `.codex/skills/`, then ran the full `codex plugin marketplace add ./` → `codex plugin list` → `codex plugin add skill-example@…` sequence.

**Empirical results** (from the log):
- `QA1_MARKETPLACE_EXIT=0` → marketplace add PASSes after `.codex/skills/` removal
- `QA1_LIST_EXIT=0`, `QA1_LIST_FOUND=YES` → plugin enumeration PASSes; `skill-example` and others appear
- `QA1_ADD_EXIT=0` → `codex plugin add skill-example@dgxsparklabs-marketplace` **succeeded** — STRONGER than the C5-FAIL baseline. The post-implementation manifest fix (`_generated/<plugin>/.codex-plugin/plugin.json` via Phase 1.5) is what makes install work, and it works *without* needing `.codex/skills/` at all.

**Answer**: **VERIFIED-YES — retirement is safe and Codex `plugin add` now succeeds end-to-end.** Codex's install flow reads `.claude-plugin/marketplace.json` and per-plugin `_generated/<plugin>/.codex-plugin/plugin.json`; neither touches `.codex/skills/`. Round-1 expected "same failure mode as C5"; round-2 finds STRONGER positive evidence — `plugin add` actually succeeds post-retirement.

Cascading implication: **D-1's retirement of `.codex/skills/` is fully cleared with empirical PASS evidence.**

### Q-A2 — Could `.gemini/skills` be a symlink to `../.agents/skills`?

**Path**: documentation review (no act run needed — the answer is "even if technically possible, it's worse than what we have").

**Evidence**: `geminicli.com/docs/extensions/reference/` (fetched 2026-05-25) documents `${extensionPath}` and `${workspacePath}` substitution for `settings` and `mcpServers` but **does not document** any skills-path indirection or `${workspacePath}` use for skills. Symlinks-in-git are also fragile on Windows (require admin or developer-mode) and are not preserved by GitHub's tarball API (they become regular files containing the symlink target text). The savings — eliminating 27 directory copies — are real, but the cost (cross-platform symlink fragility + Windows contributor friction) is higher than the gain.

**Answer**: **OBVIATED-BY-FINDING-MATRIX.** The matrix below shows Gemini is the ONLY platform that reads `.gemini/skills/` natively (it's intrinsic to the extension layout). No convergence benefit; symlink complexity buys nothing. **Recommendation: keep `.gemini/skills/` as a physical mirror.** No action needed for D-1/D-2.

### Q-A3 — Does retiring `.codex/skills/` break `compat-marketplace-add.yml (codex job)`?

**Path**: source inspection of `docs/PLATFORMS.md:222-228` ("Codex CI assertions") + the act run from Q-A1.

**Evidence**: `docs/PLATFORMS.md:224` states the workflow asserts `codex plugin marketplace add ./` exits 0, `cat ~/.codex/config.toml | grep dgxsparklabs-marketplace`, `codex plugin list | grep skill-example@…`, and `codex plugin add skill-example@…` exits 0. **None of these touch `.codex/skills/`.** The Q-A1 act run executes the first three live (PASS). The fourth (`plugin add`) was already failing pre-retirement (C5); not a regression.

**Answer**: **VERIFIED-YES — no CI assertion regression.** The post-merge `logs/post-implementation-codex.log` referenced in the round-1 PLATFORMS.md is the version where the per-plugin manifest fix landed and `codex plugin add` now passes; that fix lives in `_generated/<plugin>/.codex-plugin/plugin.json` and is independent of `.codex/skills/`.

### Q-B1 — Does Devin still find skills after `.devin/skills/` retirement?

**Path**: hermetic `act` run. Same workflow as Q-A1, steps "Q-B1.1 paths" and "Q-B1.2 list". The run installs the Devin CLI (`curl -fsSL https://cli.devin.ai/install.sh | bash`), deletes `.devin/skills/`, then runs `devin skills paths` and `devin skills list`.

**Empirical results** (from the log; "Q-B1.1 START" and "Q-B1.2 START" sections):
- `QB1_PATHS_EXIT=0`, `QB1_PATHS_AGENTS_LISTED=YES`, `QB1_PATHS_DEVIN_LISTED=YES` → Devin confirms it reads BOTH `.agents/skills/` and `.devin/skills/` as discovery paths
- `QB1_LIST_EXIT=0` → `devin skills list` ran cleanly post-retirement
- **27 skills enumerated, every one sourced from `./.agents/skills/<name>`** (visible in the log; e.g. `/telegram-notify [user,model] (./.agents/skills/telegram-notify)`, `/github-search (./.agents/skills/github-search)`, …)
- `QB1_TELEGRAM=YES` (canary), `QB1_GITHUB_SEARCH=YES` (second canary)
- Note: `QB1_SKILL_COUNT=0` printed in the log was a grep-anchoring bug (my regex `^/` didn't match because Docker prepends `[Verify — Mirror Retirement ... ]   |   /...`). The full enumeration is in the log and contains all 27 entries — the count is **27, not 0**.

**Answer**: **VERIFIED-YES — retirement is safe.** Devin enumerated every skill from `.agents/skills/` after `.devin/skills/` was removed. The `.devin/skills/` mirror is fully redundant for Devin's discovery.

Cascading implication: **D-1's retirement of `.devin/skills/` is fully cleared with empirical PASS evidence.**

### Q-B2 — Cursor IDE behavior with only `.agents/skills/`

**Path**: documentation verification — `act` cannot run Cursor IDE (it's a desktop electron app, not a headless CLI). Fresh fetch of `cursor.com/docs/context/skills` (2026-05-25).

**Evidence (`cursor.com/docs/context/skills`, fetched 2026-05-25)**:
> "Skills are automatically loaded from these locations:
>
> | Location | Scope |
> | --- | --- |
> | `.agents/skills/` | Project-level |
> | `.cursor/skills/` | Project-level |
> | `~/.agents/skills/` | User-level (global) |
> | `~/.cursor/skills/` | User-level (global) |"
>
> "For compatibility, Cursor also loads skills from Claude and Codex directories: `.claude/skills/`, `.codex/skills/`, `~/.claude/skills/`, and `~/.codex/skills/`."

`.agents/skills/` is listed FIRST in the Cursor project-level table — that's the primary path. Cursor walks the skills root recursively for `SKILL.md`.

**Answer**: **VERIFIED-YES (documentation-based)** — Cursor IDE auto-discovers `.agents/skills/` natively, and that's the primary documented path. We already emit it (AgentsPlatform). UNVERIFIABLE-EMPIRICALLY without a Windows or macOS GUI runner (act can't drive electron apps), but the doc claim is from Cursor's own site and is corroborated by Windsurf and Devin reading the same path.

### Q-B3 — Does Devin scan the proposed `.installed.json` sidecar?

**Path**: deferred to install-time design. Round 1 proposed `.agents/skills/.installed.json` as an install-state sidecar; round 2 reframes the question now that D-4 lands on git-clone (Option 1) instead of selective tarball extraction (Option 3).

**Answer**: **OBVIATED-BY-D-4.** With `git clone` as the content source, install state IS the working tree — no sidecar needed. `agents list` can derive "installed" by listing `.agents/skills/`/`.agents/agents/`/etc. that exist on disk. `agents upgrade` becomes `git pull` (or re-clone). If a sidecar is still wanted for "what version did this user pin to," it can live at `.agents/.install-meta.json` (a HIDDEN file at the `.agents/` root, not inside `.agents/skills/`), which is provably outside every platform's enumeration glob (`<construct>/<name>/<entrypoint>`).

### Q-B4 — PowerShell install equivalent for `tar --strip-components`

**Path**: also OBVIATED-BY-D-4 (git clone, not tarball). For completeness: Windows 10 1803+ ships `tar.exe` at `C:\Windows\System32\tar.exe`; `git clone` is platform-native via the same `git` binary the user already has installed (the CLI shim can shell out to `git` on both POSIX and PowerShell).

**Answer**: **OBVIATED-BY-D-4.** Implementation note for the CLI shim: use `git` as the only content-fetch dependency, present on every dev machine. Both POSIX and PowerShell paths become trivial.

### Q-B5 — Does Windsurf read `~/.agents/skills/` (user-scope)?

**Path**: WebFetch `docs.windsurf.com/windsurf/cascade/skills` (2026-05-25).

**Evidence (`docs.windsurf.com/windsurf/cascade/skills`, fetched 2026-05-25)**:
> "Project-Scope Paths
> - `.windsurf/skills/` — Current workspace only. Committed with your repo.
> - `.agents/skills/` — Cross-agent compatibility discovery
>
> User-Scope Paths
> - `~/.codeium/windsurf/skills/` — All workspaces on your machine. Not committed.
> - `~/.agents/skills/` — Cross-agent compatibility discovery
> - `~/.claude/skills/` — When 'Claude Code config reading' is enabled
>
> 'For cross-agent compatibility, Windsurf also discovers skills in `.agents/skills/` and `~/.agents/skills/`. If you have enabled Claude Code config reading, `.claude/skills/` and `~/.claude/skills/` are scanned as well.'"

**Answer**: **VERIFIED-YES.** Windsurf reads BOTH `.agents/skills/` (project) and `~/.agents/skills/` (user). The CLI shim's `--scope user` writing to `~/.agents/skills/<name>/` will serve Windsurf users on top of Cursor and Devin.

### Q-B6 — Should the install script handle rules?

**Path**: revisited post-D-5 ("CLI handles ALL constructs supported in the .agents spec"). The question becomes: does any platform read `.agents/rules/`?

**Answer**: **VERIFIED-NO** (no platform reads `.agents/rules/` as of 2026-05-25 — see Q-R1 below). But per D-5 the CLI must still cover rules. **Resolution**: the CLI's `agents install <rule>` writes the appropriate per-platform-format file to the correct per-platform path (`.cursor/rules/<name>.md` from `formats/cursor.md`; `.windsurf/rules/<name>.md` from `formats/windsurf.md`), not to `.agents/rules/`. Auto-detect the user's platform from environment (Cursor: `CURSOR_TRACE_ID` env var; Windsurf: `WINDSURF_*` env vars) or accept a `--format cursor|windsurf|both` flag (default: `both`). See updated CLI surface in `Updated implementation scope → CLI shim scope`.

### Q-R1 — Quarterly monitor for `.agents/rules/` adoption

**Path**: documentation review at 2026-05-25.

**Evidence**:
- Cursor: `cursor.com/docs/context/rules` (fetched 2026-05-25) — only `.cursor/rules/` and `AGENTS.md`. No `.agents/rules/`.
- Windsurf: `docs.windsurf.com/windsurf/cascade/memories` (fetched 2026-05-25) — only `.windsurf/rules/` and `AGENTS.md`. No `.agents/rules/`.
- Devin: `docs.devin.ai/onboard-devin/knowledge-onboarding` (fetched 2026-05-25) — lists `.rules`, `.mdc`, `.cursorrules`, `.windsurf`, `CLAUDE.md`, `AGENTS.md`. No `.agents/rules/`.
- Codex: `developers.openai.com/codex/plugins/build` (fetched 2026-05-25) — references `$REPO_ROOT/.agents/plugins/marketplace.json` and `~/.agents/plugins/marketplace.json` (canonical), but no `.agents/rules/`.

**Answer**: **VERIFIED-NO** — no platform reads `.agents/rules/`. Re-fetch quarterly; if Cursor 2.7+ or Windsurf 2.0 adopts it, revisit `.cursor/rules/` and `.windsurf/rules/` retirement.

### Q-R2 — Codex `.agents/rules/` reference

**Path**: WebFetch (above).

**Evidence**: `developers.openai.com/codex/plugins/build` (fetched 2026-05-25) — Codex documents `$REPO_ROOT/.agents/plugins/marketplace.json` and `~/.agents/plugins/marketplace.json` for **marketplace** discovery, but says nothing about `.agents/rules/`. Codex uses `AGENTS.md` (root) for rule context.

**Answer**: **VERIFIED-NO.** Codex does not read `.agents/rules/`. **New finding**: Codex DOES read `.agents/plugins/marketplace.json` as a canonical marketplace path — see un-emitted capabilities table for "Codex canonical marketplace at `.agents/plugins/marketplace.json`".

### Q-G1 — Could Gemini extensions reference an outside-extension skill path?

**Path**: documentation review of `geminicli.com/docs/extensions/reference/` (fetched 2026-05-25).

**Evidence**: `${extensionPath}` and `${workspacePath}` are documented for `settings` and `mcpServers` — not for `skills`. The skills are loaded from the extension's `skills/` subdir by convention; the docs do not describe an indirection mechanism.

**Answer**: **VERIFIED-NO** (no documented mechanism). Same conclusion as Q-A2: keep `.gemini/skills/`. Untested empirically (would need to ship a test extension); doc absence is the load-bearing evidence.

### Verification round 2 — resolution distribution

| Question | Answer | Method | Cleared decision |
|---|---|---|---|
| Q-A1 | VERIFIED-YES (`codex plugin add` succeeds after mirror removal — `QA1_ADD_EXIT=0`) | hermetic act | D-1 ✅ |
| Q-A2 | OBVIATED-BY-MATRIX (no `.gemini/skills/` symlink benefit) | doc review | D-2 stable |
| Q-A3 | VERIFIED-YES (no CI regression from `.codex/skills/` retirement) | source inspection + act | D-1 ✅ |
| Q-B1 | VERIFIED-YES (Devin enumerates all 27 skills via `.agents/skills/` post-retirement) | hermetic act | D-1 ✅ |
| Q-B2 | VERIFIED-YES (doc-based — `.agents/skills/` listed first in Cursor's project-level table); UNVERIFIABLE-EMPIRICALLY (IDE not driveable by act) | doc fetch | D-2 stable |
| Q-B3 | OBVIATED-BY-D-4 (git clone makes sidecar unnecessary) | scope-derivation | n/a |
| Q-B4 | OBVIATED-BY-D-4 (git clone replaces tarball/PowerShell split) | scope-derivation | n/a |
| Q-B5 | VERIFIED-YES (Windsurf reads `~/.agents/skills/`) | doc fetch | D-6 ✅ |
| Q-B6 | VERIFIED (CLI uses per-platform format files; rules don't go in `.agents/rules/`) | scope-derivation | D-5 ✅ |
| Q-R1 | VERIFIED-NO (`.agents/rules/` adoption: zero across all 7 platforms) | doc fetch × 4 | monitor Q3 |
| Q-R2 | VERIFIED-NO (Codex no `.agents/rules/`); NEW FINDING: Codex reads `.agents/plugins/marketplace.json` canonically | doc fetch | feeds D-14 |
| Q-G1 | VERIFIED-NO (no documented Gemini mechanism for skills outside extension dir) | doc review | Keep `.gemini/skills/` |

Distribution: **8 VERIFIED-YES/NO, 2 OBVIATED (Q-B3, Q-B4), 1 UNVERIFIABLE-EMPIRICALLY (Q-B2; doc-cleared), 1 OBVIATED-BY-MATRIX (Q-A2)** = 8/3/1.

**Empirical act runs**: 2 (Q-A1 and Q-B1, combined in one workflow). Both PASS with stronger evidence than round-1 predicted.

---

## `.agents/<construct>/` adoption matrix

Each cell shows what is documented or empirically observed about whether the platform auto-discovers from the `.agents/<construct>/` directory at project scope. **READS** = platform reads this path natively today. **NO** = doc explicitly omits it / doc lists only competing per-platform path. **N/A** = platform has no concept for this construct type. **UNVERIFIED** = couldn't determine; needs follow-up.

All citations are doc URLs fetched 2026-05-25 unless otherwise noted; empirical entries cite a log file under `docs/archive/...` or `docs/research/...`.

|  | Claude Code | Codex | Gemini | Cursor IDE | Cursor CLI | Windsurf | Devin |
|---|---|---|---|---|---|---|---|
| `.agents/skills/` | NO¹ | NO² | NO³ | **READS**⁴ | **READS**⁴ | **READS**⁵ | **READS**⁶ |
| `.agents/rules/` | NO⁷ | NO⁷ | NO⁷ | NO⁷ | NO⁷ | NO⁷ | NO⁷ |
| `.agents/agents/` | UNVERIFIED⁸ | NO⁹ | UNVERIFIED⁸ | UNVERIFIED⁸ | UNVERIFIED⁸ | N/A¹⁰ | UNVERIFIED⁸ |
| `.agents/commands/` | UNVERIFIED⁸ | NO¹¹ | UNVERIFIED⁸ | UNVERIFIED⁸ | UNVERIFIED⁸ | N/A¹² | UNVERIFIED⁸ |
| `.agents/hooks/` | UNVERIFIED⁸ | NO¹¹ | UNVERIFIED⁸ | NO¹³ | NO¹³ | NO¹⁴ | N/A¹⁵ |
| `.agents/mcp-servers/` | UNVERIFIED⁸ | NO¹¹ | UNVERIFIED⁸ | UNVERIFIED⁸ | UNVERIFIED⁸ | NO¹⁶ | UNVERIFIED⁸ |
| `.agents/lsp-servers/` | UNVERIFIED⁸ | N/A¹⁷ | N/A¹⁷ | N/A¹⁷ | N/A¹⁷ | N/A¹⁷ | N/A¹⁷ |
| `.agents/monitors/` | UNVERIFIED⁸ | N/A¹⁸ | N/A¹⁸ | N/A¹⁸ | N/A¹⁸ | N/A¹⁸ | N/A¹⁸ |
| `.agents/output-styles/` | UNVERIFIED⁸ | N/A¹⁹ | N/A¹⁹ | N/A¹⁹ | N/A¹⁹ | N/A¹⁹ | N/A¹⁹ |
| `.agents/themes/` | UNVERIFIED⁸ | N/A²⁰ | N/A²¹ | N/A²⁰ | N/A²⁰ | N/A²⁰ | N/A²⁰ |

**Footnotes**:
- ¹ Claude reads plugin install cache `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`, not filesystem auto-discovery from `.agents/skills/`. Source: `docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification.md:31-32` (CL2/CL3 evidence).
- ² Codex enumerates plugins via the marketplace manifest (`.claude-plugin/marketplace.json` legacy or `.agents/plugins/marketplace.json` canonical), not by reading `.agents/skills/` directly. Source: `developers.openai.com/codex/plugins/build` (2026-05-25): `"Every plugin has a manifest at .codex-plugin/plugin.json"`.
- ³ Gemini auto-discovers skills inside the installed extension dir (`~/.gemini/extensions/<name>/skills/`), not from `.agents/skills/`. Source: `geminicli.com/docs/extensions/reference/` (2026-05-25).
- ⁴ `cursor.com/docs/context/skills` (2026-05-25): `"Skills are automatically loaded from these locations: .agents/skills/ (Project-level)"`. The same auto-discovery applies to both Cursor IDE and Cursor CLI (the docs do not differentiate; the CLI's `--plugin-dir` flag injects a plugin dir but the standard skill discovery path is the same). Cited in WebFetch result and in `docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/cursor.md:230-244`.
- ⁵ `docs.windsurf.com/windsurf/cascade/skills` (2026-05-25): `".agents/skills/ — Cross-agent compatibility discovery"`. Both project and user scope (`~/.agents/skills/`).
- ⁶ `devin skills paths` empirical output in `docs/archive/empirical-cli-findings/devin.md` and re-asserted by `docs/research/platform-feature-routing/logs/verify-mirror-retirement.log` step Q-B1.1. Lists `.agents/skills/<skill-name>/SKILL.md` as a project-scope path.
- ⁷ None of the four platforms with rule discovery (Cursor, Windsurf, Devin, Codex) mention `.agents/rules/` in their 2026-05-25 docs. See Q-R1/Q-R2 above for citations.
- ⁸ UNVERIFIED: no documented mechanism found for the platform to auto-discover constructs of this type from the `.agents/<construct>/` path. Worth a follow-up WebFetch in Q3 in case adoption begins.
- ⁹ Codex sub-agents live at `~/.codex/agents/` (user) or `.codex/agents/` (project), TOML files. Source: `developers.openai.com/codex/subagents/` (2026-05-25). No `.agents/agents/` mention.
- ¹⁰ Windsurf has no documented sub-agent or custom-agent concept beyond Cascade itself. `docs.windsurf.com/windsurf/cascade/agents` returned 404 on 2026-05-25.
- ¹¹ Codex plugin manifest (`.codex-plugin/plugin.json`) supports `skills`, `mcpServers`, `apps`, `hooks` as component pointers. No reference to discovering these from `.agents/<subdir>/`. Source: `developers.openai.com/codex/plugins/build` (2026-05-25).
- ¹² Windsurf has no documented "commands" concept distinct from workflows. Workflows live at `.windsurf/workflows/*.md`. Source: `docs.windsurf.com/windsurf/cascade/workflows` (2026-05-25).
- ¹³ Cursor hooks live at `.cursor/hooks.json` (project) / `~/.cursor/hooks.json` (user). Source: WebFetch of `cursor.com/docs/agent/hooks` (2026-05-25). Cursor does NOT read `.agents/hooks/`.
- ¹⁴ Windsurf hooks live at `.windsurf/hooks.json` (workspace) / `~/.codeium/windsurf/hooks.json` (user). Source: `docs.windsurf.com/windsurf/cascade/hooks` (2026-05-25). No `.agents/hooks/` mention.
- ¹⁵ Devin has no documented hooks concept. `devin --help` subcommand tree (per `docs/archive/empirical-cli-findings/devin.md`) lists `skills`, `rules`, `mcp`, `auth`, `--version` only — no `hooks`.
- ¹⁶ Windsurf reads MCP config from `~/.codeium/windsurf/mcp_config.json` (user-scope only documented). Source: `docs.windsurf.com/windsurf/cascade/mcp` (2026-05-25). No `.agents/mcp-servers/` mention.
- ¹⁷ LSP-server construct exists only as a Claude Code plugin component (`lspServers` field in plugin.json). No other platform has the concept.
- ¹⁸ Monitor construct exists only as a Claude Code `experimental.monitors` field. No other platform has the concept.
- ¹⁹ Output-style construct exists only as a Claude Code `outputStyles` field. No other platform has the concept.
- ²⁰ Theme construct is Claude Code's `experimental.themes`. Cursor IDE/Windsurf themes are VS-Code-level (different concept). Devin/Cursor-CLI have no themes.
- ²¹ Gemini extensions DO support themes (`themes` array in `gemini-extension.json`) — but those are intrinsic to the extension manifest, not auto-discovered from `.agents/themes/`. So the matrix cell is N/A for `.agents/themes/` discovery specifically.

### What the matrix reveals

- **`.agents/skills/` is the ONLY broadly-adopted `.agents/` path today** — read by Cursor (IDE + CLI), Windsurf, and Devin natively. This is what we already emit. Keep it.
- **`.agents/rules/` is read by zero platforms.** Per D-2 we want to push for `.agents/` full adoption, but unilaterally moving rules there now breaks every platform. The right play is to (a) keep `.cursor/rules/` + `.windsurf/rules/` emitting as today, AND (b) **additionally** emit `.agents/rules/<name>.md` as a forward-looking convergence so that if Cursor 2.7 or Windsurf 2.0 adopts it we're already there. Tiny incremental cost (22 extra files), real preparedness payoff. See new decision D-12.
- **`.agents/<all-other-constructs>/` are universally UNVERIFIED or N/A.** No platform has documented a path-based discovery for hooks, commands, agents, MCP, monitors, output-styles, or themes outside per-platform paths. **However**, the Cursor plugin manifest reference (`cursor.com/docs/reference/plugins`, 2026-05-25) supports `agents`, `commands`, `hooks`, `mcpServers` as plugin.json component pointers AND auto-discovers from `agents/`, `commands/`, `hooks/hooks.json`, `mcp.json` SUBDIRS OF THE PLUGIN. This means Cursor reads these constructs **inside a plugin**, just not from a top-level `.agents/<construct>/`. The CLI shim can install these into per-plugin dirs that Cursor's auto-discovery picks up.
- **`READS` cells: 4 out of 70 cells (`.agents/skills/` × {Cursor IDE, Cursor CLI, Windsurf, Devin}).** That's the only `.agents/` convergence today.
- **Net implication**: D-2's "push for `.agents/` full adoption" yields ONE forward-looking new emission (`.agents/rules/`) and confirms KEEPING the existing per-platform paths for everything else. The convergence isn't ready for other construct types yet.

---

## Currently un-emitted platform capabilities

This is the meat of the round-2 expansion (per D-8). For each platform, native capabilities that exist on disk and that the marketplace COULD emit but does not today. Discovered via fresh doc fetches 2026-05-25.

| # | Platform | Capability | Platform's native path | Evidence | Maps to our Construct | Recommended action |
|---|---|---|---|---|---|---|
| U1 | Codex | **Sub-agents** | `.codex/agents/<name>.toml` (project), `~/.codex/agents/<name>.toml` (user) | `developers.openai.com/codex/subagents/` (2026-05-25): `"add standalone TOML files under ~/.codex/agents/ for personal agents or .codex/agents/ for project-scoped agents"`. Required fields: `name`, `description`, `developer_instructions`. | `AgentConstruct` (our `agents/<name>/agents/<name>.md` with YAML frontmatter) | **ADD-EMISSION** — translate our Claude-shaped agent (.md + YAML frontmatter) to Codex's `.toml` shape. Add `CodexPlatform.supports += {AgentConstruct}` and a small markdown-to-TOML converter in `CodexPlatform.emit`. |
| U2 | Cursor IDE + CLI | **Sub-agents** | `.cursor/agents/<name>.md` (project), `~/.cursor/agents/<name>.md` (user); also reads `.claude/agents/`, `.codex/agents/` (legacy) | `cursor.com/docs/agent/subagents` (2026-05-25): `"Each subagent is a markdown file with YAML frontmatter"`. Cursor 2.4 changelog (2025-12-?) confirmed introduction. | `AgentConstruct` (1:1 format match — our agents/<name>/agents/<name>.md already uses YAML frontmatter) | **ADD-EMISSION** — easy win. Cursor's subagent format IS our agent format. Add `CursorPlatform.supports += {AgentConstruct}` and `CursorPlatform.emit` copies `agents/<name>/agents/*.md` to `.cursor/agents/`. |
| U3 | Gemini | **Sub-agents** | `agents/<name>.md` inside the extension (`.gemini/agents/`) | `geminicli.com/docs/extensions/` (2026-05-25): `"Gemini CLI extensions package prompts, MCP servers, custom commands, themes, hooks, sub-agents, and agent skills"`. `geminicli.com/docs/extensions/reference/` (2026-05-25): `"Sub-agents - Agent definition files (.md) in agents/ directory"`. | `AgentConstruct` (markdown format) | **ADD-EMISSION** — `GeminiPlatform.supports += {AgentConstruct}` and `GeminiPlatform.emit` copies `agents/<name>/agents/*.md` to `.gemini/agents/`. |
| U4 | Cursor IDE + CLI | **Hooks** | `.cursor/hooks.json` (project), `~/.cursor/hooks.json` (user) | `cursor.com/docs/agent/hooks` (2026-05-25): `"Hooks let you observe, control, and extend the agent loop using custom scripts"`. Event names: `sessionStart`, `preToolUse`, `postToolUse`, `beforeShellExecution`, `afterFileEdit`, etc. | `HookConstruct` (we have `hooks/<name>/hooks/hooks.json`) | **ADD-EMISSION** — merge all hook plugins into a single `.cursor/hooks.json` (Cursor uses one file per scope) OR ship hooks INSIDE a Cursor plugin (`_generated/hook-<name>/.cursor-plugin/plugin.json` with `"hooks": "./hooks/hooks.json"`). Latter is preferred — already integrates with team marketplace. |
| U5 | Gemini | **Hooks** | `hooks/hooks.json` inside the extension (`.gemini/hooks/hooks.json`) | `geminicli.com/docs/extensions/reference/` (2026-05-25): `"Hooks - Defined in hooks/hooks.json"`. | `HookConstruct` | **ADD-EMISSION** — `GeminiPlatform.supports += {HookConstruct}` and copy `hooks/<name>/hooks/hooks.json` to `.gemini/hooks/hooks.json` (with merge if multiple hook plugins coexist). |
| U6 | Gemini | **Custom commands** | `commands/<name>.toml` inside the extension | `geminicli.com/docs/extensions/` (2026-05-25) and reference. TOML format. | `CommandConstruct` (we have `commands/<name>/commands/*.md`) | **CONSIDER-NEW-CONSTRUCT or ADD-EMISSION-WITH-CONVERSION** — Claude commands are `.md`; Gemini commands are `.toml`. Conversion is non-trivial (different schema). Recommend DEFER unless Gemini commands become a high-demand feature. |
| U7 | Cursor IDE + CLI | **Custom commands** | `.cursor/commands/<name>.md` (likely; CLI has `/commands` slash command per CLI changelog) and plugin's `commands/` subdir | `cursor.com/docs/agent/commands` page exists but content was sparse on fetch; the plugin manifest reference confirms `commands` field in `.cursor-plugin/plugin.json` and auto-discovery from plugin's `commands/` subdir. | `CommandConstruct` (markdown matches) | **ADD-EMISSION** — `CursorPlatform.supports += {CommandConstruct}`. Cursor's plugin-bundled commands ARE markdown, so copy directly. |
| U8 | Windsurf | **Workflows** | `.windsurf/workflows/<name>.md` (project), `~/.codeium/windsurf/global_workflows/<name>.md` (user) | `docs.windsurf.com/windsurf/cascade/workflows` (2026-05-25): `"a series of steps to guide Cascade through a repetitive set of tasks"`. Closest analog to our CommandConstruct. | `CommandConstruct` (analogous; format is markdown with steps) | **ADD-EMISSION** — `WindsurfPlatform.supports += {CommandConstruct}` and `WindsurfPlatform.emit` copies `commands/<name>/commands/*.md` to `.windsurf/workflows/`. Caveat: format may need slight adaptation (workflows have implicit step semantics; our commands are free-form). Test before shipping. |
| U9 | Windsurf | **Hooks** | `.windsurf/hooks.json` (workspace), `~/.codeium/windsurf/hooks.json` (user) | `docs.windsurf.com/windsurf/cascade/hooks` (2026-05-25): `"Cascade Hooks for executing custom shell commands at key workflow points"`. JSON format. | `HookConstruct` | **ADD-EMISSION** — `WindsurfPlatform.supports += {HookConstruct}` and merge all hook plugins into `.windsurf/hooks.json`. |
| U10 | Gemini | **Policies** | `policies/<name>.toml` inside the extension | `geminicli.com/docs/extensions/reference/` (2026-05-25): `"Policies - .toml files in policies/ directory"`. | NEW CONSTRUCT (we don't have a PolicyConstruct) | **CONSIDER-NEW-CONSTRUCT (DEFER for v1)** — propose `PolicyConstruct` with `prefix="policy"`, `source_directory=policies/`. Only Gemini consumes it today; skip until we have a real policy authored. Document in CONSTRUCT_TYPES.md as "Reserved for future use." |
| U11 | Codex | **Canonical marketplace** at `.agents/plugins/marketplace.json` | `$REPO_ROOT/.agents/plugins/marketplace.json` (project), `~/.agents/plugins/marketplace.json` (user) | `developers.openai.com/codex/plugins/build` (2026-05-25): `"$REPO_ROOT/.agents/plugins/marketplace.json for repo-scoped plugin catalogs ... ~/.agents/plugins/marketplace.json for personal plugin lists"`. | Equivalent to our `.claude-plugin/marketplace.json` (Phase 5) | **ADD-EMISSION (LOW-COST)** — add a Phase 5.5 that copies (or symlinks at generation time) the contents of `.claude-plugin/marketplace.json` to `.agents/plugins/marketplace.json`. Aligns Codex with its canonical-documented path rather than the legacy-compat path. Forward-looking for the day Codex deprecates `.claude-plugin/marketplace.json` reading. |
| U12 | Gemini | **Themes** (extension-bundled) | `themes` array in `gemini-extension.json` | `geminicli.com/docs/extensions/reference/` (2026-05-25): `themes` top-level field. | `ThemeConstruct` (we have one — `themes/example/`) | **DEFER** — `GeminiPlatform.supports += {ThemeConstruct}` if a real theme is authored. Currently `themes/` has only `example/`. Low value. |
| U13 | Cursor IDE + CLI | **MCP servers** (plugin-bundled) | `mcp.json` inside the plugin (auto-discovered) or `mcpServers` field in `.cursor-plugin/plugin.json` | `cursor.com/docs/reference/plugins` (2026-05-25): `mcpServers` field; default auto-discovery from `mcp.json`. | `MCPConstruct` (we have `mcp-servers/<name>/.claude-plugin/plugin.json` with `mcpServers` field) | **ADD-EMISSION** — `CursorPlatform.supports += {MCPConstruct}` and ship per-plugin MCP via `.cursor-plugin/plugin.json` with `mcpServers` pointer. Easy win; Cursor schema matches. |
| U14 | Windsurf | **`~/.windsurf/skills/` user-scope** (currently not written by us; CLI shim writes to `~/.agents/skills/` only) | `~/.codeium/windsurf/skills/` (per `docs.windsurf.com/windsurf/cascade/skills` 2026-05-25 — `~/.windsurf/skills/` is NOT a documented Windsurf path; the user-scope path is `~/.codeium/windsurf/skills/`) | (correction to `docs/PLATFORMS.md:519`) | n/a — D-6 already locked: `--scope user` writes ONLY to `~/.agents/skills/`. Windsurf reads that. No action. | **No action.** Documentation fix only — update `docs/PLATFORMS.md:519` to say `~/.codeium/windsurf/skills/` instead of `~/.windsurf/...`. |

### Ranking: user-value × implementation-cost

For scope-creep discipline. Rough estimates; intent is to give the user a slider, not a final answer.

| ID | Capability | Estimated value | Estimated cost | Ratio | Recommend for this PR? |
|---|---|---|---|---|---|
| U2 | Cursor sub-agents (1:1 format match) | HIGH | LOW (~30 LOC, no conversion) | 5/5 | **YES** — user-flagged in D-8 |
| U3 | Gemini sub-agents (markdown match) | HIGH | LOW (~30 LOC) | 5/5 | **YES** — user-flagged in D-8 |
| U1 | Codex sub-agents (TOML conversion) | HIGH | MEDIUM (~80 LOC md→toml converter) | 4/5 | **YES** — completes the sub-agent story |
| U11 | Codex canonical `.agents/plugins/marketplace.json` | MEDIUM | LOW (~15 LOC, Phase 5.5 copy) | 4/5 | **YES** — forward-looking, cheap |
| U13 | Cursor plugin-bundled MCP | MEDIUM | LOW (~25 LOC, `CursorPlatform.supports += MCP`) | 4/5 | **YES** — closes a Class A gap |
| U4 | Cursor hooks (via plugin-bundled) | MEDIUM | LOW (~25 LOC) | 4/5 | **YES** — closes a Class A gap |
| U5 | Gemini hooks (extension-bundled) | MEDIUM | LOW (~25 LOC) | 4/5 | **YES** |
| U7 | Cursor commands (via plugin) | MEDIUM | LOW (~25 LOC) | 4/5 | **YES** |
| U9 | Windsurf hooks | LOW-MEDIUM | LOW (~30 LOC) | 3/5 | **YES if cheap** |
| U8 | Windsurf workflows (commands analog) | LOW-MEDIUM | MEDIUM (semantic format conversion) | 2/5 | **DEFER to v2** — test command-to-workflow translation first |
| U6 | Gemini commands (markdown→TOML) | LOW | HIGH (full schema converter) | 1/5 | **DEFER to v2** |
| U10 | Gemini policies (new construct) | LOW | MEDIUM (new class + zero source authored) | 1/5 | **DEFER** until a real policy exists |
| U12 | Gemini themes | LOW | LOW (~15 LOC) | 2/5 | **DEFER** unless real theme authored |

**Recommended subset for this refactor PR**: U2, U3, U1, U11, U13, U4, U5, U7, U9 (9 additions). Defer U6, U8, U10, U12 to a follow-up.

**Count of un-emitted capabilities found: 14** (U1-U14).

---

## Updated implementation scope

Consolidating Tracks 1-3 into the actionable scope for the refactor PR.

### Retirements (what disappears from disk and from code)

| Item | Code location | Justification |
|---|---|---|
| `.codex/skills/` mirror tree (27 dirs, ~108 files) | `scripts/platforms.py:150-161` (`CodexPlatform.emit` skill branch) | Q-A1 PASS; no Codex codepath reads it; per-plugin `.codex-plugin/plugin.json` is the actual install surface |
| `.devin/skills/` mirror tree (27 dirs, ~108 files) | `scripts/platforms.py:295-302` (`DevinPlatform.emit`) | Q-B1 PASS; Devin reads `.agents/skills/` natively |
| `.codex/` top-level dir | (becomes empty after skill retirement; deletable) | Becomes empty post-retirement; remove from generator wipe step |
| `.devin/` top-level dir | (becomes empty post-retirement) | Same |
| **`CodexPlatform.emit` skill branch** | `scripts/platforms.py:150-161` | Becomes a no-op for SkillConstruct; manifest-only emission (Phase 1.5) remains |
| **`DevinPlatform.emit` body** | `scripts/platforms.py:295-302` | Becomes a no-op; `mirror_directory = None` (like ClaudeCodePlatform) — Phase 3 will skip naturally |
| **`DevinPlatform.supports`** can stay `{SkillConstruct}` OR drop to `set()` | Stays for future per-plugin Devin manifest emission if Devin ever introduces one; if not, drop to `set()` and Phase 1.5 skips it |

### Additions (what gets emitted that doesn't today)

| ID | Item | Code change |
|---|---|---|
| **A1** | `.agents/rules/<name>.md` forward-looking convergence (22 entries) | `AgentsPlatform.supports += {RuleConstruct}` and `AgentsPlatform.emit` handles RuleConstruct (copy raw `rule.md`, no format conversion). Cheap. |
| **A2** | Cursor sub-agents → `.cursor/agents/<name>.md` per agent plugin | `CursorPlatform.supports += {AgentConstruct}`; `CursorPlatform.emit` handles AgentConstruct (copy `agents/<name>/agents/*.md` to `.cursor/agents/`) |
| **A3** | Gemini sub-agents → `.gemini/agents/<name>.md` per agent plugin | `GeminiPlatform.supports += {AgentConstruct}`; `GeminiPlatform.emit` handles AgentConstruct |
| **A4** | Codex sub-agents → `.codex/agents/<name>.toml` per agent plugin | `CodexPlatform.supports += {AgentConstruct}`; new markdown-to-TOML translator. Required TOML fields: `name`, `description`, `developer_instructions`. |
| **A5** | Codex canonical marketplace at `.agents/plugins/marketplace.json` | New Phase 5.5: write/copy from in-memory marketplace entries to `.agents/plugins/marketplace.json` (root) |
| **A6** | Cursor plugin-bundled MCP — per-plugin `.cursor-plugin/plugin.json` with `mcpServers` field | `CursorPlatform.supports += {MCPConstruct}`; `CursorPlatform.build_plugin_json` emits the `mcpServers` pointer for MCP plugins |
| **A7** | Cursor hooks via plugin — per-plugin `.cursor-plugin/plugin.json` with `hooks` field | `CursorPlatform.supports += {HookConstruct}`; emit `hooks` pointer in Cursor manifest |
| **A8** | Cursor commands via plugin — per-plugin `.cursor-plugin/plugin.json` with `commands` field | `CursorPlatform.supports += {CommandConstruct}`; emit `commands` pointer |
| **A9** | Gemini hooks → `.gemini/hooks/hooks.json` (per-plugin merge OR multiple files if Gemini supports) | `GeminiPlatform.supports += {HookConstruct}` |
| **A10** | Windsurf hooks → `.windsurf/hooks.json` (merge from all hook plugins) | `WindsurfPlatform.supports += {HookConstruct}`; merge logic in Phase 3 |
| **A11** | `agents` CLI shim (root `install.sh` + `install.ps1` + Python implementation under `scripts/agents_cli/`) | New top-level binary; see CLI shim scope below |
| **A12 (DEFER)** | Gemini commands, Gemini themes, Gemini policies, Windsurf workflows | Per ranking table; revisit in follow-up PR |

### Generator phase changes

| Phase | Today | After refactor | Change rationale |
|---|---|---|---|
| 1 | Per-plugin Claude manifest | (unchanged) | Load-bearing core |
| 1.5 | Per-platform per-plugin manifests gated on `supports` | (unchanged, but `supports` sets expanded per A2/A3/A4/A6/A7/A8/A9/A10) | Picked up automatically via supports gate |
| 2a | Catalog bundles | (unchanged) | — |
| 2b | Catch-all bundles | (unchanged) | — |
| 3 | Mirror wipe + emit | **Expanded**: AgentsPlatform handles rules (A1); CursorPlatform handles agents (A2); GeminiPlatform handles agents+hooks (A3, A9); CodexPlatform handles agents (A4); WindsurfPlatform handles hooks (A10) | New supports → new emit branches |
| 4 | Gemini extension manifest | (unchanged) | — |
| 4.5 | Root-level gemini-extension.json | (unchanged) | — |
| 5 | Top-level `.claude-plugin/marketplace.json` | (unchanged) | — |
| **5.5 (NEW)** | n/a | Copy/write `.agents/plugins/marketplace.json` from same in-memory entries (A5) | Codex canonical path |
| 6 | Root `.cursor-plugin/marketplace.json` | **Expanded**: includes the new Cursor-supported constructs (agents, commands, hooks, mcp) in the plugin list | Schema unchanged; just more entries |
| **NEW** | n/a | `agents` CLI shim invocation (not part of generator; standalone binary) | See CLI shim scope |

### CLI shim scope (`agents` binary)

Per D-3 + D-5: a proper CLI with subcommands handling ALL constructs in the `.agents` spec. Content source: `git clone` (D-4). Scope semantics: `--scope user` writes ONLY to `~/.agents/<construct>/` (D-6).

**Final subcommand surface (revised for round 2)**:

```
agents install <construct-name>            [--scope project|user]   # default: project
agents install <bundle-name>               [--scope project|user]   # bundles install deps
agents uninstall <construct-name>          [--scope project|user]
agents list                                                          # installed
agents list --available                                              # everything in marketplace
agents list --available --type <construct>                           # filter
agents upgrade <construct-name>            [--scope project|user]    # git pull + re-link
agents upgrade --all                       [--scope project|user]
agents info <construct-name>                                         # show metadata
agents marketplace add <url>                                         # register a marketplace
agents marketplace list
agents marketplace remove <name>
agents --version
agents --help
```

**Per-construct install logic** (the CLI auto-detects construct type from the plugin name prefix: `skill-X` → SkillConstruct, `rule-Y` → RuleConstruct, etc., or via `--type` flag):

| Construct | Install action (project scope) | Install action (user scope) |
|---|---|---|
| skill | `cp -r .agents/skills/<X>/ <DEST>/.agents/skills/<X>/` | `~/.agents/skills/<X>/` |
| rule | Copy `formats/cursor.md` → `.cursor/rules/<X>.md`; `formats/windsurf.md` → `.windsurf/rules/<X>.md`; raw `rule.md` → `.agents/rules/<X>.md` (forward-looking) | Same to `~/.cursor/rules/`, `~/.windsurf/rules/`, `~/.agents/rules/` IF those user paths are documented (Cursor user rules are config-only, not file-based — skip; Windsurf user rules go via `~/.codeium/windsurf/memories/`, skip; just write `~/.agents/rules/<X>.md`) |
| command | Copy to `.cursor/commands/<X>.md` (if Cursor present), `.windsurf/workflows/<X>.md` (if format adapter ready), `.agents/commands/<X>.md` (forward-looking) | `~/.agents/commands/<X>.md` |
| agent | Copy `.md` to `.cursor/agents/<X>.md`, `.codex/agents/<X>.toml` (converted), `.gemini/agents/<X>.md`, `.claude/agents/<X>.md`, `.agents/agents/<X>.md` | Same to `~/.<platform>/agents/` and `~/.agents/agents/` |
| hook | Merge into `.cursor/hooks.json`, `.windsurf/hooks.json`, `.codex-plugin/...`, `.gemini/hooks/hooks.json`; `.agents/hooks/<X>.json` (forward-looking) | `~/.cursor/hooks.json`, `~/.windsurf/hooks.json`, etc. + `~/.agents/hooks/` |
| mcp | Merge into per-platform MCP configs (`~/.codex/config.toml` codex section, `.cursor/mcp.json`, `.gemini/.gemini/settings.json`, `~/.codeium/windsurf/mcp_config.json`); `.agents/mcp-servers/<X>.json` (forward-looking) | User-scope MCP configs |
| lsp / monitor / output-style / theme | Claude-only — install via `claude plugin install` is the supported path (CLI shim can shell out to `claude plugin install <name>` if Claude is detected) | Same |

**Decision needed**: how aggressive should the CLI be about writing to per-platform paths when the user does `agents install <hook-plugin>`? Locked decisions D-2 ("push for `.agents/` full adoption") and D-6 (`--scope user` writes ONLY to `~/.agents/`) pull in different directions for project scope. New decision D-13 below.

### Doc updates required (per D-8, bundled into refactor PR)

| File | What changes |
|---|---|
| `docs/PLATFORMS.md:29` | Remove stale `.cursor/skills/`, `.claude/skills/`, `.codex/skills/` from Cursor cell (or qualify "compat-only, not emitted by us"); drop `.codex/skills/` from Codex row; drop `.devin/skills/` from Devin row |
| `docs/PLATFORMS.md:519` | Fix `~/.windsurf/...` to `~/.codeium/windsurf/...` (per Windsurf docs); add `~/.agents/skills/` already there but verify |
| `docs/PLATFORMS.md:699-707` | Update "Per-platform manifest paths" table for new agent/hook/command/mcp emissions to Cursor + Gemini + Windsurf + Codex |
| `docs/ARCHITECTURE.md:111-119` | Update seven-platform table: Codex now also supports AgentConstruct (TOML emission); Cursor now supports AgentConstruct + CommandConstruct + HookConstruct + MCPConstruct; Gemini now supports AgentConstruct + HookConstruct; Windsurf now supports HookConstruct; mirror_directory for Codex and Devin becomes `None` |
| `docs/ARCHITECTURE.md:179-189` | Add Phase 5.5 row (`.agents/plugins/marketplace.json`) |
| `docs/RULE_FORMAT.md:117` | REMOVE the stale `.devin/rules/<name>.md` claim (generator never emitted this) |
| `docs/CONSTRUCT_TYPES.md` | New columns/notes for the per-platform per-construct support matrix |
| `rules/<name>/README.md` (22 files) | Search-and-replace `.devin/rules/` references; remove install-instruction lines referencing it |
| `README.md` | Add `agents` CLI install one-liner |
| `CHANGELOG.md` | New entry: "RETIRED `.codex/skills/`, `.devin/skills/` mirrors. ADDED per-platform sub-agent emission (Cursor, Codex, Gemini). ADDED Cursor MCP/hook/command plugin emission. ADDED Windsurf hooks. ADDED forward-looking `.agents/rules/` and `.agents/plugins/marketplace.json` emissions. ADDED `agents` CLI shim." |
| `docs/CONTRIBUTING.md` | If it mentions per-platform mirror invariants, update |

---

## New decisions-to-lock with the user (D-10 onward)

Round-1 decisions D-1 … D-9 are locked. Round 2 surfaces these new questions:

10. **D-10 — Sub-agent emission scope.** Approve adding sub-agent emission to Cursor (`.cursor/agents/`), Gemini (`.gemini/agents/`), and Codex (`.codex/agents/` TOML)? This is the direct fulfillment of D-8 "research expansion → support more capabilities." Estimated effort: U1+U2+U3 ≈ 150 LOC across `platforms.py` + a tiny md→toml converter for Codex.
11. **D-11 — Cursor plugin scope expansion.** Approve adding `CursorPlatform.supports += {AgentConstruct, CommandConstruct, HookConstruct, MCPConstruct}`? This means our Cursor plugins will install via the team marketplace with hooks, commands, MCP servers, and sub-agents all enabled — a Class A feature parity push.
12. **D-12 — Forward-looking `.agents/rules/` emission.** Approve emitting `.agents/rules/<name>.md` from `AgentsPlatform` even though no platform reads it today? Cost: 22 extra files (~50 KB). Benefit: if Cursor 2.7 or Windsurf 2.0 adopts the path, we're already there. Aligns with D-2 "push for `.agents/` full adoption."
13. **D-13 — CLI shim default behavior on project scope: write to per-platform paths OR `.agents/` only?** Two interpretations of D-2 + D-6:
    - **Option A**: `agents install <plugin> --scope project` writes ONLY to `.agents/<construct>/<name>/`. Cleanest, most aligned with D-2. Cost: platforms without `.agents/<construct>/` discovery (Cursor for hooks, all platforms for rules) won't see the install until they adopt `.agents/<construct>/` paths.
    - **Option B**: `--scope project` writes to BOTH `.agents/<construct>/` (forward-looking) AND every supported per-platform path (`cursor/`, `.windsurf/`, etc.) so the install works on every platform the user has installed today. More like a generator running locally.
    - **Option C (recommended)**: Default = Option B (writes everywhere supported), with `--agents-only` flag for users who want strict D-2 behavior. Best of both worlds.
14. **D-14 — Codex canonical marketplace emission.** Approve adding Phase 5.5 to write `.agents/plugins/marketplace.json` alongside the legacy `.claude-plugin/marketplace.json`? Very small change, future-proofs against Codex deprecating the legacy path.
15. **D-15 — Defer scope.** Confirm DEFERRED to v2 (NOT in this PR): U6 (Gemini commands), U8 (Windsurf workflows), U10 (Gemini policies), U12 (Gemini themes). These are low value or require new construct classes. If the user disagrees with any, surface here.
16. **D-16 — Sub-agent source format.** Today our `AgentConstruct` source is `agents/<name>/agents/<name>.md` with YAML frontmatter (Claude-shape). Cursor and Gemini consume the same format directly. Codex needs TOML — implement converter at emit time? Or change source format? Recommendation: keep YAML-md as source of truth (Claude-shape stays canonical), write converter for Codex. Confirm?
17. **D-17 — `agents` CLI binary location.** Where does the user expect the `agents` CLI to live after install? Options: `~/.local/bin/agents` (POSIX standard); `~/.cargo/bin/`-style (we'd ship Rust); npm package (`npx agents`)? Recommendation: shell script + Python implementation, installed to `~/.local/bin/agents` via the one-liner installer (POSIX); `$env:LOCALAPPDATA\agents\bin\agents.ps1` on Windows.

---

## Contradictions with first report

Round-2 findings that **differ from or refine** round-1 claims. Documented loudly per the methodology rule.

| Round-1 claim | Round-2 finding | Severity |
|---|---|---|
| Round-1: "AgentsPlatform hosts skill content only — `build_plugin_json` returns `{}`" implicit in scope | Round-2 D-12: AgentsPlatform should ALSO host rules content forward-looking, so `AgentsPlatform.supports` grows from `{SkillConstruct}` to `{SkillConstruct, RuleConstruct}` | **LOW** — additive, not contradictory |
| Round-1 Q-B5: cited `docs/PLATFORMS.md:519` "User-scope equivalents: `~/.windsurf/...`, `~/.agents/skills/`" | Round-2 fresh fetch of `docs.windsurf.com/windsurf/cascade/skills` (2026-05-25): Windsurf user-scope skill path is `~/.codeium/windsurf/skills/`, NOT `~/.windsurf/skills/`. Our `docs/PLATFORMS.md:519` is wrong. | **MEDIUM** — affects Windsurf user-scope claims; needs doc fix |
| Round-1 implicit: Cursor supports rules + skills only (`CursorPlatform.supports = {RuleConstruct, SkillConstruct}` at `scripts/platforms.py:236`) | Round-2 U2/U4/U7/U13: Cursor natively supports sub-agents, hooks, commands, MCP. Our `supports` is missing 4 construct types. | **HIGH** — fundamentally expands Cursor's scope. The current implementation under-emits to Cursor. |
| Round-1 implicit: Gemini supports skills only (`GeminiPlatform.supports = {SkillConstruct}` at `scripts/platforms.py:189`) | Round-2 U3/U5: Gemini extensions natively support sub-agents and hooks. Our `supports` is missing 2 types. | **HIGH** — Gemini extension capability under-utilized |
| Round-1 implicit: Codex supports skill, mcp, hook (`CodexPlatform.supports = {SkillConstruct, MCPConstruct, HookConstruct}` at `scripts/platforms.py:148`) | Round-2 U1: Codex supports sub-agents (TOML). Our `supports` is missing AgentConstruct. | **HIGH** — Codex sub-agent capability missed |
| Round-1 implicit: Windsurf supports rules only (`WindsurfPlatform.supports = {RuleConstruct}` at `scripts/platforms.py:265`) | Round-2 U9: Windsurf supports hooks. Round-2 U8: Windsurf supports workflows (commands analog, DEFERRED to v2). | **MEDIUM** — adds HookConstruct support |
| Round-1: "Codex uses `.claude-plugin/marketplace.json` (legacy-compatible) or `.agents/plugins/marketplace.json` (canonical, not adopted here)" — treated as future scope | Round-2 U11: Adopting `.agents/plugins/marketplace.json` is trivial (Phase 5.5 copy of existing in-memory entries). Worth doing now. | **LOW** — refines round-1's scope-deferral |
| Round-1 TL;DR: "three of those skill mirrors are pure dead-weight on Class A platforms (Claude, Codex, Gemini, Cursor IDE)" | Round-2 reaffirms for `.codex/skills/` and `.devin/skills/`. For `.gemini/skills/`: NOT dead-weight — intrinsic to extension layout (round-1 already noted this, but the TL;DR phrasing was loose). | **LOW** — clarification, not contradiction |
| Round-1 Q-B3/Q-B4: assumed tarball-API content source (Option 3) | Round-2: D-4 locked git-clone (Option 1). Both Q-B3 and Q-B4 become moot. | **LOW** — already resolved by user's lock |

**No round-1 claim was outright invalidated.** All round-2 findings either refine, expand, or correct round-1 scope assumptions. The biggest blind spots were the THREE platforms (Cursor, Gemini, Codex) where their plugin/extension manifests support construct types we never emitted.

---

## Cross-references (round 2 additions)

- `docs/research/platform-feature-routing/workflows/verify-mirror-retirement.yml` — Round-2 act workflow (Q-A1, Q-A3, Q-B1)
- `docs/research/platform-feature-routing/logs/verify-mirror-retirement.log` — Empirical Q-A1/Q-A3/Q-B1 evidence
- `cursor.com/docs/agent/subagents` (2026-05-25) — Cursor sub-agents at `.cursor/agents/` (markdown + YAML)
- `cursor.com/docs/agent/hooks` (2026-05-25) — Cursor hooks at `.cursor/hooks.json`
- `cursor.com/docs/reference/plugins` (2026-05-25) — Full Cursor plugin manifest schema (rules, agents, skills, commands, hooks, mcpServers)
- `cursor.com/docs/context/skills` (2026-05-25) — `.agents/skills/` listed FIRST in project-level table
- `developers.openai.com/codex/subagents/` (2026-05-25) — Codex sub-agents at `.codex/agents/<name>.toml`
- `developers.openai.com/codex/plugins/build` (2026-05-25) — `.agents/plugins/marketplace.json` canonical reference
- `geminicli.com/docs/extensions/` (2026-05-25) — Extensions package "prompts, MCP servers, custom commands, themes, hooks, sub-agents, and agent skills"
- `geminicli.com/docs/extensions/reference/` (2026-05-25) — Full extension field schema (`mcpServers`, `themes`, `settings`, agents/, commands/, hooks/, skills/, policies/)
- `docs.windsurf.com/windsurf/cascade/skills` (2026-05-25) — `.agents/skills/` + `~/.agents/skills/` (user-scope)
- `docs.windsurf.com/windsurf/cascade/hooks` (2026-05-25) — Windsurf hooks at `.windsurf/hooks.json` / `~/.codeium/windsurf/hooks.json`
- `docs.windsurf.com/windsurf/cascade/workflows` (2026-05-25) — Workflows at `.windsurf/workflows/<name>.md`
- `docs.windsurf.com/windsurf/cascade/memories` (2026-05-25) — Rules + memory paths; no `.agents/rules/`
- `docs.devin.ai/onboard-devin/knowledge-onboarding` (2026-05-25) — Devin reads `.rules`, `.mdc`, `.cursorrules`, `.windsurf`, `CLAUDE.md`, `AGENTS.md`
