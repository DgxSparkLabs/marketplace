---
date: 2026-05-26
purpose: empirical-naming-convention-research-and-migration-plan
status: complete
container: qa-naming (node:20)
claude-version: 2.1.150
docs-fetch-date: 2026-05-26
roadmap-items: 29, 33
---

# Plugin Naming Conventions — Empirical Research and Recommendation

A hermetic Docker investigation of what strings the Claude CLI actually displays and accepts for each of our 10 example plugins, compared against Anthropic's documented and observed-in-the-wild conventions, with a concrete migration plan validated by a proof-of-concept rename inside the same container.

## TL;DR

- **The operator's premise — that Claude displays "doubled" names like `example-skill` after typing `skill-example` — is FALSE for the current state of the repo.** The generator (`scripts/generate_manifest.py`) already rewrites every `_generated/<plugin>/.claude-plugin/plugin.json` `name` to match the marketplace name. Claude only ever sees `skill-example`, never `example-skill`. The mismatch lives in the *source* `<construct>/example/.claude-plugin/plugin.json` files (logs/13-cached-names.log:24-34 vs logs/13-cached-names.log:5-15) and surfaces only when the operator runs `claude plugin tag` against the source path (logs/17-tag-checks.log:2-7) or reads source files directly.
- **The real awkwardness is the doubled component name: `/skill-example:example-skill`** (marketplace-name : SKILL.md-name). This IS what the operator types and IS the canonical invocation form. Both halves contain the substring "skill" + "example". The empirical fix is renaming the SKILL.md frontmatter `name:` to a semantic value like `lab-notebook`, yielding `/skill-example:lab-notebook` (logs/18-rename-proof.log:2-3).
- **Recommended scheme: B+** — align marketplace.json `name` AND source `<construct>/example/.claude-plugin/plugin.json` `name` to `<construct>-example`, AND rename the SKILL.md / agent / command-file / output-style / theme component names from `example-<construct>` to a single semantic word (`lab-notebook`, `notebook-reviewer`, `hello`, etc.). This eliminates doubling in the slash form, makes `claude plugin tag` on the source path agree with the marketplace entry, follows Anthropic's `displayName`/component-name conventions, and preserves construct-grouped catalog browsability.
- **Proof of concept ran inside the container**: after applying B+ to `skill-example`, the canonical invocation `/skill-example:lab-notebook weather` resolves (logs/18-rename-proof.log:2-3), the bare `/lab-notebook weather` form also resolves (logs/18-rename-proof.log:5-6), the old `/skill-example:example-skill` form fails with `Unknown command` (logs/18-rename-proof.log:8-9), and the system-prompt skill registry sent to the model contains `skill-example:lab-notebook: <description>` (logs/stub-bodies-excerpt.log:2-3) — clean and unambiguous.

## Table of contents

1. [Empirical findings per construct](#empirical-findings-per-construct)
2. [Anthropic's own naming conventions](#anthropics-own-naming-conventions)
3. [Five-scheme comparison](#five-scheme-comparison)
4. [Recommended scheme — B+](#recommended-scheme--b-component-rename)
5. [Migration plan](#migration-plan)
6. [Proof-of-concept evidence](#proof-of-concept-evidence)
7. [Method](#method)
8. [Open questions and caveats](#open-questions-and-caveats)
9. [Citations](#citations)

## Empirical findings per construct

All findings captured inside `qa-naming` (node:20 + Claude 2.1.150 + Flask stub on port 8088/8089). Raw logs in `logs/`.

### Master cross-cutting findings (apply to all constructs)

| # | Finding | Evidence |
|---|---|---|
| F-A | The generator rewrites `plugin.json` `name` from source to marketplace value. Cached `~/.claude/plugins/cache/dgxsparklabs-marketplace/<plugin>/<version>/.claude-plugin/plugin.json` always has `name: <construct>-example` (matching marketplace.json), even though source `<construct>/example/.claude-plugin/plugin.json` says `name: example-<construct>`. | `logs/13-cached-names.log:1-15` (cached forms) vs `logs/13-cached-names.log:36-46` (source forms) |
| F-B | `claude plugin list` (text and `--json`) keys plugins by the marketplace name only. The `plugin.json` source `name` field is never displayed at the CLI. | `logs/04-plugin-list.log:1-50`, `logs/05-plugin-list-json.log:1-30` |
| F-C | `claude plugin details <name>` requires the marketplace name AND the plugin must be enabled. The `plugin.json` source name (`example-skill` etc.) fails with `Plugin "<name>" not found.` Every construct except `mcp-example` (already aligned) shows this asymmetry. | `logs/07-details.log:23, 50, 76, 100, 124, 148, 172, 196` (each "Plugin "example-X" not found" line) |
| F-D | `claude plugin enable/disable` requires the `plugin@marketplace` qualified form and uses the marketplace name. The bare marketplace name (without `@dgxsparklabs-marketplace`) errors with `Plugin "<name>" not found in any editable settings scope. Use plugin@marketplace format.` | `logs/06-enable-all.log:1-27` (errors) vs `logs/06-enable-qualified.log:1-9` (success) |
| F-E | The slash-command namespace prefix is the **marketplace name**, not the `plugin.json` `name`. Claude's docs say *"To change the namespace prefix, update the `name` field in `plugin.json`"* (`code.claude.com/docs/en/plugins`, fetched 2026-05-26) — but because the install-time rewrite ignores the source `name`, the prefix in practice equals the marketplace name. The system prompt skill-registry confirms: `skill-example:example-skill: <description>` is what reaches the model (pre-rename). | `logs/stub-bodies.log` line `text: "<system-reminder>\nThe following skills are available...skill-example:example-skill: Reference example..."` |
| F-F | Forms that do NOT resolve (despite what doc and prior research suggested): `/<plugin.json-name>:<skill-name>` (e.g. `/example-skill:example-skill`) is `Unknown command`; `/<marketplace-name>` alone (no colon, e.g. `/skill-example`) is `Unknown command`. | `logs/11-slash-matrix.log:5-7, 19-21` |
| F-G | Forms that DO resolve: `/<marketplace-name>:<skill-name>` (canonical, e.g. `/skill-example:example-skill`) AND the bare `/<skill-name>` flat form (e.g. `/example-skill`) both round-trip OK from a stub session. The flat form is documented at `code.claude.com/docs/en/skills` (fetched 2026-05-26) as the standalone-skills shortform; it works for plugin skills too. | `logs/11-slash-matrix.log:3-4, 13-15` |
| F-H | `claude plugin tag --dry-run` against the SOURCE path (`skills/example/`) reads the source `plugin.json` name and would create the tag `example-skill--v1.0.0`. Against `_generated/skill-example/` it finds the marketplace entry and creates `skill-example--v1.0.0`. The two disagree — confirming that for the release-tag workflow, source and marketplace name MUST align. | `logs/17-tag-checks.log:2-9, 11-19` |
| F-I | `rule-example` does not appear in the Claude marketplace listing (consistent with the 2026-05-26 rule deprecation in `ClaudeCodePlatform.supports`). `claude plugin install rule-example@dgxsparklabs-marketplace` errors with `Plugin "rule-example" not found in marketplace`. | `logs/03-install-all.log:24-26` |
| F-J | The five new findings above contradict `docs/TEST_YOURSELF.md:286-302` which claims the "After install, `/plugins` shows" column is `example-skill` (Example Skill) etc. After installation, the displayed name is `skill-example`, full stop. The TEST_YOURSELF "doubled-name visibility" bug described in `docs/ROADMAP.md` item #33 is overstated — the only place the `example-<construct>` form leaks is `claude plugin tag` on the source path. | `logs/04-plugin-list.log:1-50` |

### Per-construct strings (current state)

For each construct, ten data points are captured: marketplace.json `name`, source `plugin.json` `name`, generated `_generated/<x>/.claude-plugin/plugin.json` `name`, displayed in `claude plugin list`, displayed in `claude plugin details <marketplace-name>`, displayed in `claude plugin details <plugin.json-name>`, component name(s), canonical slash form that resolved, flat slash form, registry-line in system prompt.

| Construct | marketplace.json `name` | source `plugin.json` `name` | `_generated/` `name` | `claude plugin list` row | `details <mkt-name>` | `details <plugin.json-name>` | component name | canonical slash | flat slash | system-prompt registry line |
|---|---|---|---|---|---|---|---|---|---|---|
| skill | `skill-example` | `example-skill` | `skill-example` | `skill-example@dgxsparklabs-marketplace` | OK | NOT FOUND | `example-skill` (SKILL.md frontmatter) | `/skill-example:example-skill` ✓ | `/example-skill` ✓ | `skill-example:example-skill: <desc>` |
| sub-agent | `agent-example` | `example-agent` | `agent-example` | `agent-example@dgxsparklabs-marketplace` | OK | NOT FOUND | `notebook-reviewer` (agent file `name:`) | not via slash — `/agents` picker | n/a | `agent-example:notebook-reviewer: <desc>` (in stub bodies) |
| command | `command-example` | `example-command` | `command-example` | `command-example@dgxsparklabs-marketplace` | OK | NOT FOUND | `hello` (filename `hello.md`) | `/command-example:hello` ✓ | n/a (commands don't have flat form) | `command-example:hello: <desc>` |
| hook | `hook-example` | `example-hook` | `hook-example` | `hook-example@dgxsparklabs-marketplace` | OK | NOT FOUND | (six event names; not slash-invoked) | passive — no slash | n/a | not in slash registry; visible in `details` "Hooks (6) SessionStart, UserPromptSubmit, …" |
| MCP | `mcp-example` | `mcp-example` | `mcp-example` | `mcp-example@dgxsparklabs-marketplace` | OK | OK (only one where both names agree) | `example` (MCP server key in mcp-config.json) | tool-call `mcp__mcp-example__example__<tool>` | n/a | not in skill registry; `/mcp` shows `plugin:mcp-example:example` |
| LSP | `lsp-example` | `example-lsp` | `lsp-example` | `lsp-example@dgxsparklabs-marketplace` | OK | NOT FOUND | (none — schema-only example) | auto-attaches by extension | n/a | n/a |
| monitor | `monitor-example` | `example-monitor` | `monitor-example` | `monitor-example@dgxsparklabs-marketplace` | OK | NOT FOUND | `example-disk` (per monitors.json) | passive — fires on condition | n/a | n/a |
| output-style | `output-style-example` | `example-output-style` | `output-style-example` | `output-style-example@dgxsparklabs-marketplace` | OK | NOT FOUND | `Lab Notebook Voice` (frontmatter `name:` — human-readable) | `/output-style Lab Notebook Voice` (interactive only — slash returns `Unknown command: /output-style` in `--print` mode) | n/a | n/a |
| theme | `theme-example` | `example-theme` | `theme-example` | `theme-example@dgxsparklabs-marketplace` | OK | NOT FOUND | `Lab Notebook` (themes/*.json `name:`) | `/theme Lab Notebook` (`isn't available in this environment` in `--print`) | n/a | n/a |
| rule | (not in Claude marketplace) | `example-rule` | (not emitted to Claude) | (not present) | NOT FOUND | NOT FOUND | n/a | n/a | n/a | n/a |

Citations to logs:

- All `claude plugin list` rows: `logs/04-plugin-list.log:1-50` and `logs/05-plugin-list-json.log:1-50`
- `plugin details <marketplace-name>` for all nine: `logs/07-details.log:5-21, 28-44, 53-69, 80-92, 103-118, 126-140, 152-166, 175-189, 199-212`
- `plugin details <plugin.json-name>` NOT FOUND lines: `logs/07-details.log:23, 50, 76, 100, 124, 148, 172, 196` (mcp at `logs/07-details.log:128-140` shows OK because source and marketplace both say `mcp-example`)
- Slash matrix for skill+command: `logs/11-slash-matrix.log:1-39`
- Output-style and theme slash failures in headless: `logs/15-output-style-theme.log:2-7`

### Selected raw quotes (canonical evidence)

**`logs/04-plugin-list.log:1-50`** — full `claude plugin list` after installing all 9 (rule absent):

```
Installed plugins:

  ❯ agent-example@dgxsparklabs-marketplace
    Version: 1.0.0
    Scope: project
    Status: ✔ enabled

  ❯ command-example@dgxsparklabs-marketplace
    ...
```

(no entry contains `example-<construct>`, confirming F-J)

**`logs/11-slash-matrix.log:3-21`** — slash invocations exercising stub:

```
------ INPUT: /skill-example:example-skill weather ------
OK stub.
    bodies registry mentions:
agent-example:notebook-reviewer
command-example:hello
plugin:skill
skill-example:example-skill
------ INPUT: /example-skill:example-skill weather ------
Unknown command: /example-skill:example-skill
    bodies registry mentions:
------ INPUT: /example-skill weather ------
OK stub.
...
------ INPUT: /skill-example weather ------
Unknown command: /skill-example
```

(canonical and flat-skill-name forms work; doubled-with-plugin.json-name form fails; bare marketplace name without colon fails)

**`logs/17-tag-checks.log:2-19`** — `claude plugin tag` reveals the source vs marketplace disagreement:

```
=== tag --dry-run on skills/example (source - misaligned) ===
Plugin:  example-skill
Version: 1.0.0 (from plugin.json)
Tag:     example-skill--v1.0.0

✔ Dry run — would create tag example-skill--v1.0.0 at HEAD in /tmp/workspace
  git -C /tmp/workspace tag -a example-skill--v1.0.0 -m "example-skill 1.0.0"

=== tag --dry-run on _generated/skill-example (regenerated - aligned because rewritten) ===
Plugin:  skill-example
Version: 1.0.0 (from plugin.json)
Marketplace entry: plugins[17] in /tmp/workspace/.claude-plugin/marketplace.json (version: 1.0.0)
Tag:     skill-example--v1.0.0
```

The `claude plugin tag` help text says *"validating that plugin.json and any enclosing marketplace entry agree"* (`logs/16-validate-paths.log:14-15`). Anthropic's own tooling expects alignment. We violate it in `<construct>/example/` sources.

## Anthropic's own naming conventions

### Documented (code.claude.com/docs/en)

Fetched 2026-05-26.

**`/en/plugins`** — Quickstart example: `name: "my-first-plugin"`, skills file at `skills/hello/SKILL.md`, invocation `/my-first-plugin:hello`. Note the convention: plugin name is `<topic>-<noun>` semantic (`my-first-plugin`), skill name is a verb (`hello`). The `name` field is described as *"Unique identifier and skill namespace. Skills are prefixed with this (e.g., `/my-first-plugin:hello`)."* and the only constraint stated is "kebab-case, no spaces."

**`/en/plugins-reference`** — Manifest schema row: `name: string, Unique identifier (kebab-case, no spaces), Example: "deployment-tools"`. Component-namespacing example: *"the agent `agent-creator` for the plugin with name `plugin-dev` will appear as `plugin-dev:agent-creator`"* — again `<topic>-<noun>` plugin name, `<noun>-<noun>` agent name; no `agent-` prefix on the plugin name.

**`/en/plugin-marketplaces`** — Walkthrough example: plugin name `quality-review-plugin`, marketplace name `my-plugins`, plugin's skill `quality-review`, invocation `/quality-review-plugin:quality-review`. (Anthropic's own example has the doubled-word problem — they call this acceptable; we can do better with `B+`.) Schema row for the per-plugin entry: `name: string, Plugin identifier (kebab-case, no spaces). This is public-facing: users see it when installing.` Schema row for marketplace name: `name: string, Marketplace identifier (kebab-case, no spaces). This is public-facing: users see it when installing plugins (for example, /plugin install my-tool@your-marketplace).`

`displayName` (since 2.1.143): *"Human-readable name shown in UI surfaces. Falls back to `name` when omitted. May contain spaces and any casing. Not used for namespacing or lookup."* This is the field for friendly capitalization — `name` is the identifier, `displayName` is the label.

**`strict` mode** (`/en/plugin-marketplaces#strict-mode`): default `true` means `plugin.json` is the authority. Confirms F-A is technically a violation — Anthropic expects `plugin.json` to win, not be silently rewritten. Our generator does this because the marketplace entry is what users `install` against, but if we ever set `strict: false` we would need the marketplace entry to be self-sufficient.

### Observed in Anthropic's two public marketplaces

Snapshot via `curl` 2026-05-26:

- **`anthropics/claude-plugins-official`** — 203 plugins. Patterns:
  - ~80% are single semantic names: `airtable`, `figma`, `stripe`, `linear`, `mongodb`, `slack`, `notion`, `vercel`, `playwright`.
  - **LSP plugins consistently use `<language>-lsp` SUFFIX**: `clangd-lsp`, `csharp-lsp`, `gopls-lsp`, `jdtls-lsp`, `kotlin-lsp`, `liquid-lsp`, `lua-lsp`, `php-lsp`, `pyright-lsp`, `ruby-lsp`, `rust-analyzer-lsp`, `swift-lsp`, `typescript-lsp` (13 LSP plugins, all suffix). This is the only systematic construct-suffix.
  - **Output styles use `-output-style` SUFFIX**: `explanatory-output-style`, `learning-output-style`.
  - **Skill bundles use `-skills` plural SUFFIX**: `apollo-skills`, `circle-skills`, `forge-skills`, `huggingface-skills`, `netlify-skills`, `togetherai-skills`, `youdotcom-agent-skills`.
  - **No plugin uses a `<construct>-<thing>` PREFIX** for the type-of-construct meaning. `skill-creator` and `commit-commands` are semantic (a skill-creator IS a creator-of-skills), not type-tags.

- **`anthropics/claude-plugins-community`** — 1715 plugins. Statistical breakdown computed from `/tmp/community.json` 2026-05-26:
  - Construct PREFIX form (`skill-*`, `agent-*`, `mcp-*`, etc.): **3.0% total** (51 plugins). `agent-* = 16`, `skill-* = 11`, `mcp-* = 9`, `plugin-* = 2`. Manual inspection: `agent-advisor`, `agent-archive`, `agent-discover` — most are semantic (agent FOR advising, agent FOR archiving), not type-tags.
  - Construct SUFFIX form (`*-skill`, `*-mcp`, etc.): **7.2% total** (124 plugins). `*-plugin = 44`, `*-skill = 33`, `*-mcp = 23`, `*-lsp = 14`, `*-agent = 9`.
  - **Vast majority (89%) use single semantic names** with no construct tag — exactly the Anthropic-official idiom.

### What Anthropic does that we don't

| Convention | Anthropic | DgxSparkLabs marketplace |
|---|---|---|
| `plugin.json` `name` matches marketplace.json `name` | YES (every entry, both files maintained in lockstep) | NO except `mcp-example` |
| `displayName` for human-readable label | NOT widely used in official (`displayName=(none)` for 203/203 plugins, `logs/...official-pluginnames` listing) — they keep names short enough to be readable as-is | We use `displayName` in source `plugin.json` (`"Example Skill"`, etc.) but the generator strips it before emitting `_generated/`, so it never reaches Claude |
| Single semantic name | YES (80%+ of official) | NO — we use `<construct>-example` |
| Construct SUFFIX where used | `-lsp`, `-output-style`, `-skills` (suffix at end) | We use `<construct>-` prefix (`skill-example`, `command-example`) — opposite direction |
| Component name distinct from plugin name | YES (Anthropic: `quality-review-plugin` contains `quality-review`; `commit-commands` contains `commit`) | YES for command (`hello`) and agent (`notebook-reviewer`), NO for skill (`example-skill` doubles `example`) |

## Five-scheme comparison

For all 10 example plugins, what the operator types at install + what Claude displays + what the slash invocation looks like:

### Legend

- `mp` = marketplace.json `name` (what operator types after `claude plugin install`)
- `pj` = source `<construct>/example/.claude-plugin/plugin.json` `name`
- `co` = component name (skill `name:`, agent `name:`, command file stem, output-style `name:`, theme `name:`)
- `display` = what `claude plugin list` shows in the row header
- `slash` = canonical resolved slash form (empirically — those that say `OK stub` in `logs/11-slash-matrix.log`)

### Scheme A — Status quo (current)

| Construct | mp | pj | co | display | slash | issue |
|---|---|---|---|---|---|---|
| skill | `skill-example` | `example-skill` | `example-skill` | `skill-example` | `/skill-example:example-skill` | "example" repeats; `pj`/`mp` mismatch; `claude plugin tag` against source produces wrong tag |
| sub-agent | `agent-example` | `example-agent` | `notebook-reviewer` | `agent-example` | `agent-example:notebook-reviewer` (picker) | `pj`/`mp` mismatch only — component name is already good |
| command | `command-example` | `example-command` | `hello` | `command-example` | `/command-example:hello` | `pj`/`mp` mismatch only — component name is already good |
| hook | `hook-example` | `example-hook` | (event names) | `hook-example` | (passive) | `pj`/`mp` mismatch only |
| mcp | `mcp-example` | `mcp-example` | `example` | `mcp-example` | `mcp__mcp-example__example__<tool>` | (already scheme B per `4d4818b`) |
| lsp | `lsp-example` | `example-lsp` | (none) | `lsp-example` | (auto-attach) | `pj`/`mp` mismatch only |
| monitor | `monitor-example` | `example-monitor` | `example-disk` | `monitor-example` | (passive) | `pj`/`mp` mismatch; component name has redundant "example" |
| output-style | `output-style-example` | `example-output-style` | `Lab Notebook Voice` | `output-style-example` | `/output-style Lab Notebook Voice` | `pj`/`mp` mismatch only |
| theme | `theme-example` | `example-theme` | `Lab Notebook` | `theme-example` | `/theme Lab Notebook` | `pj`/`mp` mismatch only |

### Scheme B — Align `pj` to `mp`, keep components as-is

Apply the `mcp-example` precedent (commit `4d4818b`) to the other 9.

| Construct | mp | pj | co | display | slash |
|---|---|---|---|---|---|
| skill | `skill-example` | `skill-example` | `example-skill` (unchanged) | `skill-example` | `/skill-example:example-skill` (still doubled) |
| sub-agent | `agent-example` | `agent-example` | `notebook-reviewer` | `agent-example` | `agent-example:notebook-reviewer` ✓ |
| command | `command-example` | `command-example` | `hello` | `command-example` | `/command-example:hello` ✓ |
| hook | `hook-example` | `hook-example` | (events) | `hook-example` | (passive) ✓ |
| mcp | `mcp-example` | `mcp-example` | `example` | `mcp-example` | `mcp__mcp-example__example__<tool>` ✓ |
| lsp | `lsp-example` | `lsp-example` | (none) | `lsp-example` | (auto) ✓ |
| monitor | `monitor-example` | `monitor-example` | `example-disk` | `monitor-example` | (passive) |
| output-style | `output-style-example` | `output-style-example` | `Lab Notebook Voice` | `output-style-example` | `/output-style Lab Notebook Voice` ✓ |
| theme | `theme-example` | `theme-example` | `Lab Notebook` | `theme-example` | `/theme Lab Notebook` ✓ |

**Pros**: minimal source change; `claude plugin tag` against source agrees with marketplace; matches roadmap #28 mcp precedent.
**Con**: skill `/skill-example:example-skill` still doubles the word "example".

### Scheme B+ — Scheme B + component rename (RECOMMENDED)

Align `pj` to `mp` AND rename component names that contain `example-<construct>` to a single semantic word.

| Construct | mp | pj | co | display | slash |
|---|---|---|---|---|---|
| skill | `skill-example` | `skill-example` | `lab-notebook` | `skill-example` | `/skill-example:lab-notebook` ✓ (proven, `logs/18-rename-proof.log:2-3`) |
| sub-agent | `agent-example` | `agent-example` | `notebook-reviewer` (already clean) | `agent-example` | `agent-example:notebook-reviewer` ✓ |
| command | `command-example` | `command-example` | `hello` (already clean) | `command-example` | `/command-example:hello` ✓ |
| hook | `hook-example` | `hook-example` | (six event names, no rename needed) | `hook-example` | (passive) ✓ |
| mcp | `mcp-example` | `mcp-example` | `example` (already aligned) | `mcp-example` | `mcp__mcp-example__example__<tool>` ✓ |
| lsp | `lsp-example` | `lsp-example` | (n/a) | `lsp-example` | (auto) ✓ |
| monitor | `monitor-example` | `monitor-example` | `disk-usage` (rename from `example-disk`) | `monitor-example` | (passive) ✓ |
| output-style | `output-style-example` | `output-style-example` | `Lab Notebook Voice` (already clean) | `output-style-example` | `/output-style Lab Notebook Voice` ✓ |
| theme | `theme-example` | `theme-example` | `Lab Notebook` (already clean) | `theme-example` | `/theme Lab Notebook` ✓ |

**Pros**: zero doubled words anywhere; canonical slash form is short and semantic; matches Anthropic's `quality-review-plugin:quality-review` precedent (theirs is doubled, ours is cleaner); preserves construct-grouped catalog browsability; `claude plugin tag` source path agrees with marketplace.
**Con**: requires touching the SKILL.md frontmatter and the monitor config — two extra files vs Scheme B.

### Scheme C — Drop construct prefix on `pj`

Marketplace stays `<construct>-example`, `pj` becomes a semantic word.

| Construct | mp | pj | co | display | slash |
|---|---|---|---|---|---|
| skill | `skill-example` | `lab-notebook` | `status` | `skill-example` | `/skill-example:status` |
| sub-agent | `agent-example` | `notebook` | `reviewer` | `agent-example` | `agent-example:reviewer` |

**Con**: re-introduces `pj`/`mp` mismatch; doesn't fix the `claude plugin tag` source-path problem. Equivalent to Scheme A for that issue.

### Scheme D — Single semantic name end-to-end (Anthropic idiom)

| Construct | mp | pj | co | display | slash |
|---|---|---|---|---|---|
| skill | `lab-notebook` | `lab-notebook` | `status` | `lab-notebook` | `/lab-notebook:status` |
| sub-agent | `notebook-reviewer` | `notebook-reviewer` | `review` | `notebook-reviewer` | `notebook-reviewer:review` |
| command | `notebook-header` | `notebook-header` | `today` | `notebook-header` | `/notebook-header:today` |
| ...etc | (10 unrelated names) | | | | |

**Pros**: most consistent with Anthropic's 1700-plugin community + 200-plugin official idiom; shortest slash forms; cleanest display.
**Con**: loses construct-grouped browsability — a new user can't `claude plugin list --json --available | grep ^skill-` to see all skill examples. The repo's purpose is example-per-construct; the prefix is load-bearing for discoverability. This is the right scheme for *real* plugins (post-1.0 content add) but not for the example bundle.

### Scheme F — Topic-themed (Anthropic LSP idiom flipped to prefix)

Marketplace `<construct>-<topic>` where `<topic>` is the example's theme.

| Construct | mp | pj | co | display | slash |
|---|---|---|---|---|---|
| skill | `skill-lab-notebook` | `skill-lab-notebook` | `status` | `skill-lab-notebook` | `/skill-lab-notebook:status` |
| sub-agent | `agent-lab-notebook` | `agent-lab-notebook` | `reviewer` | `agent-lab-notebook` | `agent-lab-notebook:reviewer` |

**Pros**: preserves construct prefix; ties all examples to the lab-notebook theme.
**Con**: marketplace name is two-segment; longer to type; less idiomatic. The "example" suffix in B+ flags reference-purpose more cleanly than "lab-notebook" suffix (which sounds like a real plugin).

## Recommended scheme — B+ (component rename)

### The three criteria

1. **Operator types fewest awkward characters**: Scheme D wins on raw length; B+ is a close second. C and F are longer. A and B doubled-word slash forms are longer to read.
2. **Claude displays cleanest strings**: B+ ties with D for zero-doubling; both beat A/B (skill still doubles "example") and F (long names).
3. **Marketplace browsability** (a new user can find the example for each construct type): A, B, B+, C, F all have the `<construct>-example` prefix → identical here. D loses badly because the 10 examples scatter alphabetically.

**B+ is the only scheme that wins ALL three criteria for our specific "examples bundle" use case.** For when real production plugins return (roadmap #16+), D is the right scheme — but that's a separate decision.

### Why B+ over plain B

The only construct still producing a "doubled" slash form under plain B is **skill** (`/skill-example:example-skill`). Renaming the SKILL.md `name:` to `lab-notebook` costs one line in `skills/example/SKILL.md` and produces `/skill-example:lab-notebook`. Two other components have minor redundancy (`example-disk` monitor, `example-skill` skill) — fixing those is one line each. Total touched: ~3 source lines vs 9 plugin.json files in B.

### One downside the proof-of-concept exposed

After re-installing, the plugin landed `disabled` until explicit `claude plugin enable skill-example@dgxsparklabs-marketplace` (logs/18 onward). This is a **separate orthogonal observation** — installation does NOT auto-enable on this codepath. Probably unrelated to naming but worth flagging for the QA arc.

## Migration plan

Apply Scheme B+ in this order. All changes are to source files under `<construct>/example/`; the generator regenerates `_generated/` automatically.

### Phase 1 — Align `pj` to `mp` for the 8 misaligned plugins (Scheme B portion)

For each of `agents`, `commands`, `hooks`, `lsp-servers`, `monitors`, `output-styles`, `themes` (and `rules` if rule emission ever returns to Claude):

```diff
# <construct>/example/.claude-plugin/plugin.json
- "name": "example-<construct>",
+ "name": "<construct>-example",
- "homepage": "https://github.com/DgxSparkLabs/marketplace/tree/main/examples/example-<construct>",
+ "homepage": "https://github.com/DgxSparkLabs/marketplace/tree/main/<construct>/example",
```

Skill is the master example below.

### Phase 2 — Rename redundant component names (Scheme B+ portion)

Only two files actually need it:

```diff
# skills/example/SKILL.md
---
- name: example-skill
+ name: lab-notebook
  description: ...
```

```diff
# monitors/example/monitors/monitors.json — rename "example-disk" to "disk-usage"
[
  {
-   "name": "example-disk",
+   "name": "disk-usage",
    "command": "df -h .",
    ...
  }
]
```

The other 7 components (`notebook-reviewer`, `hello`, `example` MCP server key, `Lab Notebook Voice`, `Lab Notebook`, six hook events, LSP n/a) are already clean.

### Phase 3 — Update docs that quote slash invocations

Search-and-replace across `docs/TEST_YOURSELF.md` (lines 290, 293 cells), `docs/PLATFORMS.md`, `docs/USER_GUIDE.md` (if present), and any README:

- `/example-skill:example-skill` → `/skill-example:lab-notebook`
- `/example-command:hello` → `/command-example:hello`
- `example-agent` (in `/plugins` shows column) → `agent-example`
- ... etc per the empirical table above

Then update the "After install, /plugins shows" column in TEST_YOURSELF.md lines 290-299 to remove all `example-<construct>` references — they were never accurate (F-J).

### Phase 4 — Verify

In a fresh Docker container (matching the qa-naming recipe):

1. `uv run scripts/generate_manifest.py --check` (drift gate)
2. `uv run tests/test_marketplace.py`
3. `claude plugin marketplace add ./ && claude plugin install skill-example@dgxsparklabs-marketplace && claude plugin enable skill-example@dgxsparklabs-marketplace`
4. With stub on 8089: `printf '/skill-example:lab-notebook weather\n' | claude --print` → OK stub
5. `claude plugin tag --dry-run skills/example/` → should print `Plugin: skill-example` (not `example-skill`)

### Before/after for the two highest-traffic example plugins

#### skill-example

**Before** (`skills/example/SKILL.md:1-5` + `skills/example/.claude-plugin/plugin.json:1-3`):

```
---
name: example-skill
description: Reference example. Echoes back...
---
```
```json
{
  "name": "example-skill",
  ...
```

**After**:

```
---
name: lab-notebook
description: Reference example. Echoes back...
---
```
```json
{
  "name": "skill-example",
  ...
```

Operator-visible delta:
- Install: `claude plugin install skill-example@dgxsparklabs-marketplace --scope project` (unchanged)
- `/plugins` row: `skill-example@dgxsparklabs-marketplace` (unchanged — generator already does this)
- Slash: was `/skill-example:example-skill` (doubled), now `/skill-example:lab-notebook` ✓ (proven `logs/18-rename-proof.log:2-3`)
- `claude plugin tag skills/example/` now produces `skill-example--v1.0.0` (was `example-skill--v1.0.0`), matching the marketplace entry

#### agent-example

**Before** (`agents/example/.claude-plugin/plugin.json:1-3`):

```json
{
  "name": "example-agent",
  ...
```

**After**:

```json
{
  "name": "agent-example",
  ...
```

`agents/example/agents/notebook-reviewer.md` frontmatter `name: notebook-reviewer` UNCHANGED (already semantic).

Operator-visible delta:
- Install: `claude plugin install agent-example@dgxsparklabs-marketplace --scope project` (unchanged)
- `/agents` picker row: `agent-example:notebook-reviewer` (unchanged)
- `claude plugin tag agents/example/` now produces `agent-example--v1.0.0`

## Proof-of-concept evidence

Inside `qa-naming` container, on a scratch in-container copy at `/tmp/workspace` (NOT pushed to git, NOT touching the host marketplace), I:

1. Edited `skills/example/SKILL.md` frontmatter `name: example-skill` → `name: lab-notebook`.
2. Edited `skills/example/.claude-plugin/plugin.json` `"name": "example-skill"` → `"name": "skill-example"`.
3. Ran `uv run scripts/generate_manifest.py` — clean regenerate (`logs/18-rename-proof.log` precursors).
4. Reinstalled the plugin: `claude plugin marketplace remove dgxsparklabs-marketplace && claude plugin marketplace add ./ && claude plugin install skill-example@dgxsparklabs-marketplace --scope project && claude plugin enable skill-example@dgxsparklabs-marketplace`.
5. Verified `claude plugin details skill-example` shows `Skills (1) lab-notebook` (the cached SKILL.md `name:` is `lab-notebook`).
6. Verified the three slash forms:
   - `/skill-example:lab-notebook weather` → OK stub (resolved, command-name element confirms canonical form)
   - `/lab-notebook weather` → OK stub (flat skill-name form also works)
   - `/skill-example:example-skill weather` → Unknown command (old form correctly retired)
7. Verified the system-prompt skill registry sent to the stub contains exactly one entry: `skill-example:lab-notebook: <description>` (no doubled words, no `example-skill` anywhere).

Citations:

- Pre-rename source: `logs/13-cached-names.log:36-46` shows source `name=example-skill`
- Rename action: edits described in section above (in-container only, not committed)
- Post-rename details: `logs/18-rename-proof.log:1-15` — full slash matrix and registry inspection
- Skill registry: `logs/stub-bodies-excerpt.log:2-9` — registry entry + command-name element + command-args

## Method

### Container setup

```powershell
docker run -d --name qa-naming -v "${PWD}:/workspace/marketplace:ro" node:20 sleep 7200
docker exec qa-naming bash -c '
  apt-get update -qq && apt-get install -y -qq python3-pip python3-flask git curl
  npm install -g @anthropic-ai/claude-code
  cp -r /workspace/marketplace /tmp/workspace
'
```

Read-only mount of the host repo + writable copy at `/tmp/workspace` so any in-container changes (the proof-of-concept rename) cannot accidentally leak to the host.

### Stub setup

Both `tests/fixtures/claude-stub/stub.py` (port 8088) and `stub_body_dumper.py` (port 8089). Body dumper captures the full request body — including the system prompt's skill registry block — to `/tmp/stub-bodies.log` for forensic grep.

### Per-construct probe script

```bash
for pair in "skill:skill-example:example-skill" ...; do
  cons=${pair%%:*}; rest=${pair#*:}
  marketplace_name=${rest%%:*}; pluginjson_name=${rest##*:}
  claude plugin details $marketplace_name >> details.log
  claude plugin details $pluginjson_name >> details.log
done
```

Plus per-slash-form invocation captured via `printf '/<form>\n' | claude --print` against the body-dumper.

### Limitations

- Output-style and theme slash forms can only be exercised interactively — `claude --print` reports `Unknown command: /output-style` and `/theme isn't available in this environment` (`logs/15-output-style-theme.log:2,5`). The display strings (cached plugin.json + plugin list) are still empirically captured.
- The proof-of-concept rename only validates `skill-example`. The same logic applies to the other 7 construct examples but only one was tested end-to-end. The migration plan above lists each as a one-line edit.

## Open questions and caveats

- **Why does `--print` install land disabled?** Post-install state was `Status: ✘ disabled` until explicit `claude plugin enable <name>@<marketplace>` (`logs/19-renamed-registry.log` precursors). This is orthogonal to naming but worth a side-investigation; suspected interaction between `claude plugin install --scope project` and the no-config-loaded codepath.
- **Why does the doc claim `plugin.json` `name` is the namespace prefix when empirically the marketplace name is?** Two possibilities: (a) the doc is correct and our generator's name-rewrite is the divergence; (b) the doc is outdated and Claude actually uses the marketplace name throughout. The cached plugin.json post-install (`logs/12-validate-mcp-settings.log:25-35` shows cached `name=theme-example`) suggests Claude reads the cached plugin.json, which IS the marketplace name due to generator rewrite — so the doc is technically right but the field user-visible-in-source isn't what reaches Claude. After Scheme B+ migration this distinction becomes moot because source and cached agree.
- **Why does Anthropic's own `quality-review-plugin` example double the word "quality-review"?** Their idiom in `/en/plugin-marketplaces` walkthrough doubles intentionally to teach the namespacing rule. They're modeling namespace-explicitness, not aesthetic minimalism. Scheme B+ improves on their teaching example for our use case.
- **Should the `displayName` field be set?** Currently the generator strips it before emit (no `displayName` in any cached or `_generated/` plugin.json — confirmed `logs/13-cached-names.log:1-15` cached forms have no displayName field). Anthropic's official marketplace also doesn't use displayName widely (203/203 show `displayName=(none)` in raw `marketplace.json`). Skipping is fine. If we want friendly capitalization later, set `displayName` in marketplace.json entries.

## Citations

### Anthropic documentation (fetched 2026-05-26)

- `code.claude.com/docs/en/plugins` — namespacing convention, `<my-first-plugin>:<hello>` example, "To change the namespace prefix, update the `name` field in `plugin.json`."
- `code.claude.com/docs/en/plugins-reference` — manifest schema `name: string, Unique identifier (kebab-case, no spaces), Example: "deployment-tools"`, agent-namespacing example `plugin-dev:agent-creator`
- `code.claude.com/docs/en/plugin-marketplaces` — marketplace schema with per-plugin `name` field, `displayName` (2.1.143+), `strict` mode, walkthrough using `quality-review-plugin:quality-review`
- `code.claude.com/docs/en/skills` — plugin-skill namespacing rule, standalone vs plugin skill names table

### Anthropic example marketplaces (snapshot 2026-05-26)

- `github.com/anthropics/claude-plugins-official` `/.claude-plugin/marketplace.json` — 203 plugins, single-semantic naming dominant, `-lsp` / `-output-style` / `-skills` suffixes for type-tagged subsets
- `github.com/anthropics/claude-plugins-community` `/.claude-plugin/marketplace.json` — 1715 plugins, 89% single-semantic, 7% suffix, 3% prefix

### Empirical logs in this research

All paths relative to `docs/research/naming-conventions-2026-05-26/logs/`:

- `01-marketplace-add.log` — `claude plugin marketplace add ./` output
- `02-marketplace-list.log` — registered marketplace listing
- `03-install-all.log` — bulk install of 10 example plugins (rule fails as expected)
- `04-plugin-list.log` — `claude plugin list` after install (9 enabled)
- `05-plugin-list-json.log` — `--json` machine-readable form
- `06-enable-all.log` — bare-name enable fails (use plugin@marketplace format)
- `06-enable-qualified.log` — qualified-form enable succeeds
- `07-details.log` — `claude plugin details` for both name forms across 9 constructs
- `08-slash-forms.log` — first-pass slash form probe (4 cases)
- `09-skill-forms.log` — focused skill slash form matrix
- `11-slash-matrix.log` — complete slash matrix for skill + command
- `12-validate-mcp-settings.log` — `claude plugin validate`, `claude mcp list`, cached plugin.json layout
- `13-cached-names.log` — cached vs `_generated/` vs source `plugin.json` `name` fields side-by-side
- `15-output-style-theme.log` — `/output-style` and `/theme` invocations (both fail in `--print`)
- `16-validate-paths.log` — validate on `_generated/` vs source, `plugin tag --help`
- `17-tag-checks.log` — `claude plugin tag --dry-run` against source vs `_generated/` (proves alignment matters)
- `18-rename-proof.log` — post-rename slash invocation matrix (proof-of-concept)
- `19-renamed-registry.log` — renamed-skill registry mention check
- `plugin-list-json-post-rename.log` — `--json` form after the rename
- `stub-bodies-excerpt.log` — trimmed excerpt of the system-prompt skill registry + command-name element after rename
- `stub-bodies.log` — full request bodies (239 KB; cited line-ranges via grep above)
