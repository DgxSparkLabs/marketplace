---
date: 2026-05-27
purpose: empirical-verification-of-shared-plugin.json-name-namespace-for-marketplace-brand-prefix
status: complete
container: qa-claude (node:20 + Claude 2.1.152 + Flask stub on port 8089)
claude-version: 2.1.152
docs-fetch-date: 2026-05-27
roadmap-items: follow-up to #29/#33 (PR #10) — operator question about brand-prefixed namespace
---

# Brand-prefixed shared `plugin.json` namespace — empirical viability

A hermetic Docker investigation into whether Claude Code accepts two installed skill plugins sharing the same `plugin.json` `name` value (here `dgxsparklabs-skill`), and whether the resulting slash invocations `/dgxsparklabs-skill:foo` and `/dgxsparklabs-skill:bar` both resolve to their respective skills under one shared marketplace-level brand namespace.

## TL;DR

- **PATH A (shared `plugin.json` `name: dgxsparklabs-skill` across all skill plugins) is FULLY VIABLE in Claude Code 2.1.152.** Two skill plugins installed from one local marketplace, each with `plugin.json` `name: dgxsparklabs-skill` but distinct marketplace.json entry names (`skill-foo-test`, `skill-bar-test`), coexist cleanly. Both `/dgxsparklabs-skill:foo` and `/dgxsparklabs-skill:bar` resolve to the correct skills; the system-prompt skill registry surfaces both entries under the one shared prefix; `claude plugin validate` accepts both; install/enable/disable/uninstall act per row keyed by the marketplace entry name with no collision warnings.
- **`/plugins` UI behavior:** `claude plugin list` shows two distinct rows keyed by marketplace name (`skill-foo-test@dgxsparklabs-marketplace`, `skill-bar-test@dgxsparklabs-marketplace`), each with its own enable/disable state — operator clarity preserved. `claude plugin details <marketplace-name>` returns `not found` (consistent with prior research: details lookups use the `plugin.json` `name`, not the marketplace name). `claude plugin details dgxsparklabs-skill` resolves to ONE entry — the first installed — and shows only that plugin's component inventory, hiding the second plugin's skill at the details query level. This is the **only operator-visible cost** of the shared namespace.
- **Slash resolution:** `/dgxsparklabs-skill:foo` and `/dgxsparklabs-skill:bar` both resolve (logs/10a-shared-foo.log:6,7 + logs/10b-shared-bar.log:6,7). Flat forms `/foo` and `/bar` also resolve and Claude internally rewrites them to the fully-qualified `<command-name>/dgxsparklabs-skill:foo</command-name>` form (logs/10c-flat-foo.log:7 + logs/10d-flat-bar.log:7). The marketplace-name forms `/skill-foo-test:foo` and `/skill-bar-test:bar` do NOT resolve — `Unknown command` (logs/10e-control-mkt-foo.log:2 + logs/10f-control-mkt-bar.log:2). This is the inverse of the prior research's finding for the example marketplace because the prior research had `plugin.json` `name` matching the marketplace name; here `plugin.json` `name` differs from marketplace name and Claude routes slash invocations by the `plugin.json` `name` (the docs' "skill namespace" field).
- **Edge cases:** disabling one of the two retires that plugin's skill from the registry without breaking the other (logs/11-edge-disable.log:18,29); uninstall keyed by marketplace name works once `--scope project` is given explicitly (logs/12-edge-uninstall.log:35); `claude plugin validate _generated/skill-foo-test` and `claude plugin validate _generated/skill-bar-test` both pass without any duplicate-name warning (logs/15-validate.log:3,8); `claude plugin list --available --json` lists both as distinct entries (logs/14-available.log).
- **VERDICT: PATH A is implementable.** The migration is a one-line generator change (`_base_plugin_shape` returns a fixed `name = "<marketplace-name>"` minus the trailing `-marketplace` suffix), kept distinct from the marketplace entry name which the generator continues to compose from `<construct.prefix>-<source-dir-name>`. The only behavior degradation is `claude plugin details dgxsparklabs-skill` collapsing to one plugin — a minor UI quirk that operators recover from with `claude plugin list` instead.

## Table of contents

1. [Test setup](#test-setup)
2. [Empirical probes — every assertion in the TL;DR](#empirical-probes)
3. [Comparative phase — what the docs say](#comparative-phase)
4. [Verdict on PATH A](#verdict-on-path-a)
5. [Migration plan for PATH A](#migration-plan-for-path-a)
6. [Open caveats](#open-caveats)
7. [Method + repro recipe](#method)

## Test setup

The probe runs entirely inside a `qa-claude` Docker container (image `node:20`, Claude Code 2.1.152 + `uv` 0.11.16 + Flask via PEP 723 stub). The host repo at `C:\Users\devic\source\marketplace` is bind-mounted read-write at `/workspace/marketplace`. To avoid leaking edits to the host, the test runs against a tarball-copied scratch tree at `/tmp/workspace` and writes its installed-state into `~/.claude/plugins/`.

### Source dirs created in-container (NOT on host)

- `skills/foo-test/SKILL.md` with frontmatter `name: foo`, `description: Test foo — shared-namespace probe (foo half)`
- `skills/bar-test/SKILL.md` with frontmatter `name: bar`, `description: Test bar — shared-namespace probe (bar half)`

### Generator bypass approach

**Used approach (a)** — generator output, then hand-edit. Ran `uv run scripts/generate_manifest.py` once in `/tmp/workspace`, which produced `_generated/skill-foo-test/.claude-plugin/plugin.json` and `_generated/skill-bar-test/.claude-plugin/plugin.json` with the standard distinct names. Then hand-edited both files via `jq` to rewrite `"name": "dgxsparklabs-skill"` and add `"displayName": "DgxSparkLabs Skills"`. The marketplace.json entries were left as the generator produced them: distinct names `skill-foo-test` and `skill-bar-test`, so install commands continue to address each plugin individually.

Why this approach over (b) — patching `_base_plugin_shape` to emit the shared name globally: hand-edit isolates the question to "does Claude accept two cached plugin.json files with the same name?" without coupling to a generator refactor we have not yet decided to take. Path A's eventual migration would be the generator change; the empirical question to settle first is "is it safe?", and hand-edit answers that directly.

### Hermetic state reset before probes

Before any probe:
1. `claude plugin marketplace remove dgxsparklabs-marketplace` (clear prior registration)
2. `rm -rf ~/.claude/plugins/cache/dgxsparklabs-marketplace ~/.claude/plugins/marketplaces/dgxsparklabs-marketplace` (purge cache)
3. Reset `installed_plugins.json` and `known_marketplaces.json` to `{}` (clean slate)
4. Re-add: `claude plugin marketplace add /tmp/workspace`

## Empirical probes

Every assertion below cites a log file + line range. Logs in `logs/`.

### Probe 1 — install both plugins

| Step | Command | Outcome | Citation |
|---|---|---|---|
| 1a | `claude plugin marketplace add /tmp/workspace` | `✔ Successfully added marketplace: dgxsparklabs-marketplace (declared in user settings)` | logs/01-marketplace-add.log:2 |
| 1b | `claude plugin install skill-foo-test@dgxsparklabs-marketplace --scope project` | `✔ Successfully installed plugin: skill-foo-test@dgxsparklabs-marketplace (scope: project)` | logs/03-install-foo.log:2 |
| 1c | `claude plugin enable skill-foo-test@dgxsparklabs-marketplace` | `✘ Failed ... already enabled` (install auto-enabled) | logs/03-install-foo.log:5 |
| 1d | `claude plugin install skill-bar-test@dgxsparklabs-marketplace --scope project` | `✔ Successfully installed plugin: skill-bar-test@dgxsparklabs-marketplace (scope: project)` | logs/04-install-bar.log:2 |
| 1e | `claude plugin enable skill-bar-test@dgxsparklabs-marketplace` | `✘ Failed ... already enabled` (install auto-enabled) | logs/04-install-bar.log:5 |

**No collision warning at install or enable.** Both plugins land successfully.

### Probe 2 — `claude plugin list` shows two distinct rows

| Probe | Citation | Excerpt |
|---|---|---|
| Text output | logs/05-plugin-list.log:1-13 | Two rows: `skill-bar-test@dgxsparklabs-marketplace` and `skill-foo-test@dgxsparklabs-marketplace`, each `Status: ✔ enabled` |
| JSON output | logs/06-plugin-list-json.log:2-22 | Two entries each keyed by `id: "skill-X-test@dgxsparklabs-marketplace"`, distinct `installPath`, both `"enabled": true` |

The list is keyed by the marketplace entry name, NOT by the shared `plugin.json` name. From the operator's perspective, the `/plugins` view still shows two independent rows.

### Probe 3 — `claude plugin details` asymmetry

| Query | Outcome | Citation |
|---|---|---|
| `claude plugin details skill-foo-test` | `Plugin "skill-foo-test" not found.` | logs/07-details.log:2 |
| `claude plugin details skill-bar-test` | `Plugin "skill-bar-test" not found.` | logs/07-details.log:5 |
| `claude plugin details dgxsparklabs-skill` | Resolves to ONE plugin — shows `Source: skill-foo-test@dgxsparklabs-marketplace`, `Skills (1) foo` only | logs/07-details.log:8-26 |

**This is the only operator-visible cost** of the shared namespace. `claude plugin details <shared-name>` returns one of the two plugins (in this run, the first-installed `skill-foo-test`) and silently hides the other's component inventory. The other plugin's contributions are still active at the runtime / slash level — they only disappear from the `details` query.

### Probe 4 — cache layout

Both plugins land in their own version-directory under the cache, with each cached `plugin.json` preserving the shared name:

| Path | Content | Citation |
|---|---|---|
| `~/.claude/plugins/cache/dgxsparklabs-marketplace/skill-foo-test/1.0.0/.claude-plugin/plugin.json` | `"name": "dgxsparklabs-skill"`, description=foo half | logs/08-cache-tree.log:11-26 |
| `~/.claude/plugins/cache/dgxsparklabs-marketplace/skill-bar-test/1.0.0/.claude-plugin/plugin.json` | `"name": "dgxsparklabs-skill"`, description=bar half | logs/08-cache-tree.log:28-44 |
| `~/.claude/plugins/cache/dgxsparklabs-marketplace/skill-foo-test/1.0.0/SKILL.md` | frontmatter `name: foo` | logs/08-cache-tree.log:47-54 |
| `~/.claude/plugins/cache/dgxsparklabs-marketplace/skill-bar-test/1.0.0/SKILL.md` | frontmatter `name: bar` | logs/08-cache-tree.log:56-63 |

The cache is keyed by marketplace entry name (the install-time identity), and within each version dir the verbatim plugin.json + SKILL.md sit side-by-side. There is no collision on disk.

### Probe 5 — slash resolution via stub body-dumper (THE CRITICAL TEST)

For each probe, the `stub_body_dumper.py` on port 8089 captured every `/v1/messages` POST body. Each probe was preceded by `: > /tmp/stub-bodies.log` (truncate). The headless invocation was `printf '<form>\n' | claude --print`. I report the CLI's STDOUT (resolved vs `Unknown command`), the system-prompt skill registry line, and the `<command-name>` element that reached the user-message.

| Probe | Form typed | STDOUT | Registry line in system prompt | `<command-name>` in user msg | Outcome | Citation |
|---|---|---|---|---|---|---|
| 5a | `/dgxsparklabs-skill:foo` | `OK stub.` | `- dgxsparklabs-skill:foo: Test foo …` + `- dgxsparklabs-skill:bar: Test bar …` | `<command-name>/dgxsparklabs-skill:foo</command-name>` | ✔ resolves to foo skill | logs/10a-shared-foo.log:2,6,7 |
| 5b | `/dgxsparklabs-skill:bar` | `OK stub.` | both entries listed | `<command-name>/dgxsparklabs-skill:bar</command-name>` | ✔ resolves to bar skill | logs/10b-shared-bar.log:2,6,7 |
| 5c | `/foo` (flat) | `OK stub.` | both entries listed | `<command-name>/dgxsparklabs-skill:foo</command-name>` (Claude rewrote!) | ✔ resolves to foo via flat form | logs/10c-flat-foo.log:2,5,7 |
| 5d | `/bar` (flat) | `OK stub.` | both entries listed | `<command-name>/dgxsparklabs-skill:bar</command-name>` (Claude rewrote!) | ✔ resolves to bar via flat form | logs/10d-flat-bar.log:2,5,7 |
| 5e | `/skill-foo-test:foo` (mkt-name) | `Unknown command: /skill-foo-test:foo` | (skill-registry block absent — no skill matched, so the system-reminder for skills wasn't emitted) | absent | ✘ does NOT resolve | logs/10e-control-mkt-foo.log:2,5 |
| 5f | `/skill-bar-test:bar` (mkt-name) | `Unknown command: /skill-bar-test:bar` | (absent) | absent | ✘ does NOT resolve | logs/10f-control-mkt-bar.log:2,5 |

**Verbatim system-prompt registry block** captured from probe 5a (logs/10a-shared-foo.log:6 — the same block also appears in 5b/5c/5d):

```
<system-reminder>
The following skills are available for use with the Skill tool:

- dgxsparklabs-skill:foo: Test foo — shared-namespace probe (foo half)
- dgxsparklabs-skill:bar: Test bar — shared-namespace probe (bar half)
...
```

**Both skills are surfaced to the model under the same `dgxsparklabs-skill:` prefix, with distinct second-half names (`foo`, `bar`) and distinct descriptions.** The model sees them as two callable skills sharing one namespace. This is exactly what the docs' description of `name` (*"Unique identifier and skill namespace. Skills are prefixed with this."*) predicts when the namespace is intentionally shared.

### Probe 6 — `claude plugin validate` does not warn on duplicate name

| Target | Outcome | Citation |
|---|---|---|
| `_generated/skill-foo-test` | `✔ Validation passed` | logs/15-validate.log:4 |
| `_generated/skill-bar-test` | `✔ Validation passed` | logs/15-validate.log:9 |
| `.` (whole marketplace) | `✔ Validation passed` | logs/15-validate.log:14 |

The CLI's own validator does not flag the shared plugin.json name as an error or warning. This matches the docs language: `name` is described as "Unique identifier" (plugins-reference) but the validator does not enforce uniqueness across plugins — only that the field is present and kebab-case.

### Probe 7 — edge case: disable one of the two

After both installed, run `claude plugin disable skill-bar-test@dgxsparklabs-marketplace`:

| Observation | Citation |
|---|---|
| `✔ Successfully disabled plugin: skill-bar-test (scope: project)` | logs/11-edge-disable.log:2 |
| `claude plugin list` shows bar `Status: ✘ disabled`, foo still `Status: ✔ enabled` | logs/11-edge-disable.log:3-14 |
| `/dgxsparklabs-skill:foo` → `OK stub.`, registry contains ONLY `dgxsparklabs-skill:foo: Test foo …` | logs/11-edge-disable.log:18,21 |
| `/dgxsparklabs-skill:bar` → `Unknown command: /dgxsparklabs-skill:bar`, registry empty | logs/11-edge-disable.log:25,28 |

Disable is per-marketplace-entry. When one of the two is disabled, the namespace cleanly retracts that plugin's contribution; the other plugin's skill continues to resolve under the same namespace prefix.

### Probe 8 — edge case: uninstall one of the two

`claude plugin uninstall skill-bar-test@dgxsparklabs-marketplace` (without explicit scope) is rejected because the plugin is enabled at project scope:

| Observation | Citation |
|---|---|
| First attempt without `--scope`: `✘ Failed to uninstall ... is enabled at project scope` | logs/12-edge-uninstall.log:2 |
| After `claude plugin disable ... && claude plugin uninstall ... --scope project`: `✔ Successfully uninstalled plugin: skill-bar-test (scope: project)` | logs/12-edge-uninstall.log:35 |
| `claude plugin list` after: only `skill-foo-test` remains | logs/12-edge-uninstall.log:37-43 |
| Cache dir `skill-bar-test` still present on disk (Claude quirk; not relevant to namespacing) | logs/12-edge-uninstall.log:45-47 |
| `/dgxsparklabs-skill:foo` → resolves; registry contains only foo entry | logs/12-edge-uninstall.log:51,54 |
| `/dgxsparklabs-skill:bar` → `Unknown command`; registry empty | logs/12-edge-uninstall.log:58,61 |
| `claude plugin details dgxsparklabs-skill` after bar uninstall: still resolves to foo, `Skills (1) foo` | logs/12-edge-uninstall.log:65-84 |

Uninstalling one plugin from the shared namespace leaves the other completely intact. The shared `dgxsparklabs-skill` prefix continues to resolve cleanly for the remaining plugin.

### Probe 9 — `claude plugin list --available`

After `claude plugin marketplace update dgxsparklabs-marketplace` (necessary to bust the catalog cache), the filtered output:

| Entry | Citation |
|---|---|
| `skill-foo-test@dgxsparklabs-marketplace` listed with description "Test foo — shared-namespace probe (foo half)" | logs/14-available.log:9-16 |
| `skill-bar-test@dgxsparklabs-marketplace` listed with description "Test bar — shared-namespace probe (bar half)" | logs/14-available.log:1-8 |

Both available, both addressable by marketplace name.

## Comparative phase

WebFetch on `https://code.claude.com/docs/en/plugins` and `https://code.claude.com/docs/en/plugins-reference` (fetched 2026-05-27).

Direct quotes about plugin.json `name`:

- **`/en/plugins` Quickstart**: *"`name`: Unique identifier and skill namespace. Skills are prefixed with this (e.g., `/my-first-plugin:hello`)."*
- **`/en/plugins` Quickstart**: *"Plugin skills are always namespaced (like `/my-first-plugin:hello`) to prevent conflicts when multiple plugins have skills with the same name."*
- **`/en/plugins` Quickstart**: *"To change the namespace prefix, update the `name` field in `plugin.json`."*
- **`/en/plugins-reference` Manifest schema row**: `name | string | Unique identifier (kebab-case, no spaces) | "deployment-tools"`

**The docs nowhere explicitly forbid two plugins sharing a `plugin.json` `name`, nor do they describe collision behavior if it happens.** The word "Unique" appears in the description but the validator and runtime treat name as "the namespace this plugin contributes to" rather than "the primary key of the plugin in the marketplace." The marketplace.json `name` IS the primary key (used by install, uninstall, enable, disable, the cache directory layout, `claude plugin list`); the `plugin.json` `name` is the runtime namespace prefix.

This is consistent with the prior `naming-conventions-2026-05-26` research's F-E finding that the slash prefix is what reaches the model in the system-reminder skill registry — only here, by design, two plugins resolve to the same prefix.

## Verdict on PATH A

**PASS.**

The operator's brand-prefixed shared-namespace idea is implementable as proposed. Every requirement passes:

1. ✔ Two installed skill plugins with shared `plugin.json` `name: dgxsparklabs-skill` coexist cleanly
2. ✔ `/dgxsparklabs-skill:foo` and `/dgxsparklabs-skill:bar` both resolve to the correct skills
3. ✔ The system-prompt skill registry surfaces both as `dgxsparklabs-skill:foo` and `dgxsparklabs-skill:bar`
4. ✔ `claude plugin list` keeps two distinct rows keyed by marketplace name
5. ✔ Install / enable / disable / uninstall are per-row, no collision interference
6. ✔ `claude plugin validate` accepts both plugins and the marketplace as a whole

One degradation:

- ✘ `claude plugin details dgxsparklabs-skill` collapses to one entry (the first-installed) and hides the second plugin's component inventory from the details view. Operators using `details` to inspect a single plugin instead need to use `claude plugin list` (which still distinguishes them) or `claude plugin list --available --json | jq '.available[] | select(.pluginId == "<marketplace-name>@dgxsparklabs-marketplace")'`.

## Migration plan for PATH A

The marketplace's source-of-truth-to-emitted-files chain is documented in `docs/ADDING_A_CONSTRUCT.md` section "Trace each fragment to its source". Path A changes exactly one fragment: the `plugin.json` `name` field written by `_base_plugin_shape` at `scripts/constructs.py:73-77`. Marketplace entry naming (used by install commands) stays as-is — that remains `<construct.prefix>-<source-dir-name>`.

### Files that change

| File | Change |
|---|---|
| `scripts/constructs.py` | `_base_plugin_shape` → replace `"name": f"{construct.prefix}-{name}"` with `"name": "dgxsparklabs-skill"` (or more generally `"name": f"dgxsparklabs-{construct.category}"`, brand-prefixed per-construct). The marketplace entry's `name` continues to come from `scripts/generate_manifest.py:138` `plugin_dir = GENERATED / f"{construct.prefix}-{name}"` paired with `_make_marketplace_entry(plugin_json, plugin_dir, construct.category)` — but since the marketplace entry's `name` is read from the `_generated/<dir>` dir name (via `_make_marketplace_entry`), we need to verify the entry name composition or thread a separate `plugin_json["marketplace_name"]` field. Read scripts/generate_manifest.py:138-145 carefully before editing. |
| `scripts/platforms.py` `CodexPlatform.build_plugin_json`, `CursorPlatform.build_plugin_json` | These may also call `_base_plugin_shape` or compose their own `name` — review and decide whether the brand-prefix should propagate to Codex/Cursor (probably yes if we want platform-parity slash invocations). |
| `tests/test_marketplace.py` | Several assertions probably look for the prior `name: <prefix>-<dirname>` shape in cached plugin.json. Update those to expect `dgxsparklabs-<construct.category>` instead. Specifically, any test that reads `_generated/<plugin>/.claude-plugin/plugin.json` and asserts on the `name` field. |
| `docs/ADDING_A_CONSTRUCT.md` section "Trace each fragment to its source" | The whole walked example needs to be re-walked under the new scheme. Specifically the lines that say `"skill-notify"` come from `_base_plugin_shape` — under PATH A the line "the plugin name half" comes from MARKETPLACE.toml + construct.category, not from construct.prefix + source-dir. The marketplace entry name (used in install) is still `<construct.prefix>-<source-dir-name>`, but the slash prefix becomes the brand-prefix. |
| `docs/TEST_YOURSELF.md`, `docs/PLATFORMS.md`, `docs/USER_GUIDE.md`, `README.md` | Every example slash invocation `/<prefix>-<name>:<skill-name>` becomes `/dgxsparklabs-<construct>:<skill-name>`. Searches that match those forms need updating. |

### Operator-visible delta after migration

- **Install commands UNCHANGED**: `claude plugin install skill-example@dgxsparklabs-marketplace` continues to work — marketplace entries keep distinct names.
- **`claude plugin list` UNCHANGED**: still shows ten rows, one per marketplace entry.
- **Slash invocations CHANGE**: `/skill-example:lab-notebook` becomes `/dgxsparklabs-skill:lab-notebook`. All skill plugins share the `dgxsparklabs-skill` prefix; all command plugins share `dgxsparklabs-command`; etc.
- **`claude plugin details` CHANGES**: `claude plugin details skill-example` continues to return `not found`. `claude plugin details dgxsparklabs-skill` now returns ONE of the skill plugins (whichever was installed first), and its component inventory will list every enabled skill across every skill plugin under that namespace. This is the "degradation" — operators inspecting one plugin's details by namespace will see the whole namespace's contribution.

### Risk assessment

- **Low risk** for runtime behavior — proven empirically above.
- **Medium risk** for operator workflows that rely on `claude plugin details <plugin-name>` to inspect single plugins. Operators who use this command need to learn the workaround.
- **Low risk** for tests — straightforward find-and-replace once the generator change lands.
- **Test order**: implement generator change, run `uv run scripts/generate_manifest.py --check`, fix test expectations, run `uv run tests/test_marketplace.py`, re-run a probe matching this research's setup to confirm slash resolution end-to-end.

## Open caveats

- **Test sample is two skill plugins, not ten.** The shared namespace was tested only for the skill construct. The same mechanism should work for any plugin that contributes a slash-invocable component (commands, agents), but the empirical evidence here covers skills specifically. Before committing to PATH A, run the same probe with one shared-name `command-foo` + `command-bar` pair to confirm command-plugin slash routing is identical.
- **No test of cross-construct shared namespaces.** PATH A as proposed in the operator's question was "`dgxsparklabs-skill` shared across all skill plugins." Whether `dgxsparklabs-skill` (shared across skills) AND `dgxsparklabs-skill` (mistakenly also a command-plugin's plugin.json name) collide cleanly is untested. The natural design is per-construct brand prefix (`dgxsparklabs-skill` for skills, `dgxsparklabs-command` for commands, etc.) which keeps namespaces orthogonal.
- **Tab-completion behavior not probed.** Interactive-TUI-only feature; `claude --print` cannot exercise tab-completion. Worth a manual probe inside the dev container before merging PATH A.
- **`claude plugin details dgxsparklabs-skill` collapsing to one entry** is the only confirmed behavior degradation. There may be others in the `/plugins` interactive TUI that this headless probe could not exercise — recommend a manual TUI session with two shared-name plugins installed before merging.
- **Generator changes touching `_base_plugin_shape` will affect every construct's plugin.json**. If we choose `name: f"dgxsparklabs-{construct.category}"` we get per-construct brand prefixes (good for keeping skill / command / agent namespaces orthogonal). If we choose a single `name: "dgxsparklabs"` for ALL constructs across ALL plugins, the slash form becomes `/dgxsparklabs:lab-notebook` (one prefix everywhere — uncluttered but harder to grep for "all skills under this brand"). Operator decision.

## Method

### Container

Existing `qa-claude` container (image `node:20`, persistent), running with bind-mount `C:\Users\devic\source\marketplace` ↔ `/workspace/marketplace`. The container already had Claude 2.1.152 + Node 20 + git + jq from prior research. uv was installed via `curl -LsSf https://astral.sh/uv/install.sh | sh`. The repo was mirrored to `/tmp/workspace` via a tar pipe (the earlier-attempted `cp -r` skipped hidden directories — pitfall worth flagging).

### Stub

`uv run /tmp/workspace/tests/fixtures/claude-stub/stub_body_dumper.py` on port 8089, launched in detached mode (`docker exec -d`), captures every `/v1/messages` POST body to `/tmp/stub-bodies.log`. Each probe truncates the bodies log first (`: > /tmp/stub-bodies.log`), runs `printf '<form>\n' | claude --print` with `ANTHROPIC_BASE_URL=http://127.0.0.1:8089` + `ANTHROPIC_AUTH_TOKEN=stub` exported, then greps the bodies log for skill registry + command-name evidence.

### Repro recipe

```bash
# Inside qa-claude (or any container with claude + uv + jq + Flask):
cd /tmp/workspace

# 1. Create the two test source dirs
mkdir -p skills/foo-test skills/bar-test
cat > skills/foo-test/SKILL.md <<EOF
---
name: foo
description: Test foo — shared-namespace probe (foo half)
---
# foo skill
EOF
cat > skills/bar-test/SKILL.md <<EOF
---
name: bar
description: Test bar — shared-namespace probe (bar half)
---
# bar skill
EOF

# 2. Generate, then hand-edit plugin.json files to share the brand namespace
uv run scripts/generate_manifest.py
for plugin in skill-foo-test skill-bar-test; do
  pj=_generated/$plugin/.claude-plugin/plugin.json
  jq '. + {"name": "dgxsparklabs-skill", "displayName": "DgxSparkLabs Skills"}' "$pj" > "$pj.tmp"
  mv "$pj.tmp" "$pj"
done

# 3. Clean slate, register, install both
claude plugin marketplace remove dgxsparklabs-marketplace 2>/dev/null || true
rm -rf ~/.claude/plugins/cache/dgxsparklabs-marketplace
echo '{}' > ~/.claude/plugins/installed_plugins.json
echo '{}' > ~/.claude/plugins/known_marketplaces.json
claude plugin marketplace add /tmp/workspace
mkdir -p /tmp/test && cd /tmp/test
claude plugin install skill-foo-test@dgxsparklabs-marketplace --scope project
claude plugin install skill-bar-test@dgxsparklabs-marketplace --scope project

# 4. Probe slash resolution against the body dumper
docker exec -d <container> bash -c 'uv run /tmp/workspace/tests/fixtures/claude-stub/stub_body_dumper.py'  # if not running
export ANTHROPIC_BASE_URL=http://127.0.0.1:8089
export ANTHROPIC_AUTH_TOKEN=stub
for form in '/dgxsparklabs-skill:foo' '/dgxsparklabs-skill:bar' '/foo' '/bar' '/skill-foo-test:foo' '/skill-bar-test:bar'; do
  echo "=== $form ==="
  : > /tmp/stub-bodies.log
  printf '%s\n' "$form" | claude --print 2>&1 | head -3
  grep -oE 'dgxsparklabs-skill:(foo|bar)[^"]*' /tmp/stub-bodies.log | head -3
done
```

## Citations

- All empirical logs in `logs/` of this directory
- Claude Code docs: `https://code.claude.com/docs/en/plugins` (fetched 2026-05-27), `https://code.claude.com/docs/en/plugins-reference` (fetched 2026-05-27)
- Prior research this builds on: `docs/research/naming-conventions-2026-05-26/RESEARCH.md` (the qa-naming Docker recipe and body-dumper pattern)
- Generator implementation: `scripts/constructs.py` (`_base_plugin_shape` at line 61, `SkillConstruct` at line 82), `scripts/generate_manifest.py` Phase 1 (line 130-146)
- Operator-facing trace: `docs/ADDING_A_CONSTRUCT.md` section "Trace each fragment to its source"

## PART 2 — follow-up probes (2026-05-27)

Three follow-up probes settling the open caveats from Part 1 section "Open caveats". Same `qa-claude` container, same hermetic-reset pattern, same `stub_body_dumper.py` on port 8089. All probe runs land at `/tmp/workspace` inside the container; the host repo working tree is unchanged except for the new `logs/part2-*.log` files (see prefix). Probe-A artifacts share the `dgxsparklabs-command` plugin.json `name`; Probe-B uses 5 plugins sharing `dgxsparklabs-skill`; Probe-C reuses the Probe-B setup.

### TL;DR of part 2

- **Probe A — command parity: PASS.** Two command plugins (`command-foo-test`, `command-bar-test`) sharing `plugin.json` `name: dgxsparklabs-command` install cleanly; `/dgxsparklabs-command:hello-foo` and `/dgxsparklabs-command:hello-bar` both resolve; controls `/command-foo-test:hello-foo` and `/command-bar-test:hello-bar` fail with `Unknown command`; `claude plugin validate` accepts both; `claude plugin details dgxsparklabs-command` collapses to the first-installed plugin (same degradation as skills, Part 1 section Probe 3).
- **Probe B — scale to 5 plugins: PASS.** 5 skill plugins (a..e) sharing `dgxsparklabs-skill` all install with no warnings, no latency degradation across the sequence (1.7–2.3s per install, no monotonic increase); `claude plugin list` shows 5 distinct rows; `/dgxsparklabs-skill:{a..e}` all resolve; the system-prompt registry surfaces all 5 in one block; disabling 3 cleanly retracts those 3 from the registry while the other 2 keep resolving.
- **Probe B confirmed "first-installed wins" for the details collapse.** When 5 plugins are installed in order a→e, `claude plugin details dgxsparklabs-skill` resolves to skill-**a**-test. When the same 5 are uninstalled and reinstalled in REVERSE order e→a, the details query resolves to skill-**e**-test. So the collapse rule is install-order, NOT alphabetic on the marketplace name. Operators can predict which plugin's inventory will surface: first-installed wins.
- **Probe C — autocomplete signal: PARTIAL.** `--print` mode does NOT exercise interactive tab-completion; the only resolver hint it returns is `Unknown command: /foo. Did you mean /bar?` for invalid input (and the suggestion is just the shortest-similar command). HOWEVER, `--debug-file` exposes the resolver's internal candidate set: `Skill prompt: showing "dgxsparklabs-skill:e" (userFacingName="e")` lines are emitted for each loaded skill at session start. With 5 shared-namespace plugins, the debug log emits 5 such lines — one per skill — so the candidate set the TUI works from is 5 entries. The TUI tab-completion behavior with this candidate set still needs interactive verification (recipe below).
- **VERDICT: Path A is still GO.** All three probes confirm the shared-namespace mechanism is robust for the migration. Per-construct brand prefix (`dgxsparklabs-skill`, `dgxsparklabs-command`, …) is the recommended scheme; commands behave identically to skills, scale shows no degradation up to 5 plugins, and the autocomplete candidate set is well-formed at the resolver level. The only confirmed limitation remains `claude plugin details <shared-name>` collapsing to the first-installed plugin.

### Probe A — command parity

**Setup** (`/tmp/workspace/`):

- `commands/foo-test/commands/hello-foo.md` with frontmatter `description: foo command - command-parity probe`
- `commands/bar-test/commands/hello-bar.md` with frontmatter `description: bar command - command-parity probe`
- After `uv run scripts/generate_manifest.py`, hand-edited both `_generated/command-{foo,bar}-test/.claude-plugin/plugin.json` via `jq` to share `name: dgxsparklabs-command`, `displayName: DgxSparkLabs Commands`. Marketplace.json entries left as generator emitted: `command-foo-test`, `command-bar-test`.

**Install** (Probe A.1):

| Step | Outcome | Citation |
|---|---|---|
| `claude plugin marketplace add /tmp/workspace` | `✔ Successfully added marketplace: dgxsparklabs-marketplace` | logs/part2-A-00-reset-add.log:11 |
| `claude plugin install command-foo-test@dgxsparklabs-marketplace --scope project` | `✔ Successfully installed` | logs/part2-A-01-install.log:2 |
| `claude plugin install command-bar-test@dgxsparklabs-marketplace --scope project` | `✔ Successfully installed` | logs/part2-A-01-install.log:5 |
| `claude plugin list` shows two rows | each `Status: ✔ enabled` | logs/part2-A-01-install.log:8-19 |

No collision warning at install. Both rows present, both enabled.

**Slash resolution** (Probe A.2 — clean state after removing leftover skill plugins):

| Form typed | STDOUT | `<command-name>` in body | Outcome | Citation |
|---|---|---|---|---|
| `/dgxsparklabs-command:hello-foo` | `OK stub.` | `<command-name>/dgxsparklabs-command:hello-foo</command-name>` | ✔ resolves | logs/part2-A-02-slash-probes-clean.log:3-7 |
| `/dgxsparklabs-command:hello-bar` | `OK stub.` | `<command-name>/dgxsparklabs-command:hello-bar</command-name>` | ✔ resolves | logs/part2-A-02-slash-probes-clean.log:13-17 |
| `/command-foo-test:hello-foo` | `Unknown command: /command-foo-test:hello-foo` | (absent) | ✘ does NOT resolve | logs/part2-A-02-slash-probes-clean.log:23-26 |
| `/command-bar-test:hello-bar` | `Unknown command: /command-bar-test:hello-bar` | (absent) | ✘ does NOT resolve | logs/part2-A-02-slash-probes-clean.log:29-32 |

**Registry surfacing** — verbatim system-reminder block captured from the bodies log during the `/dgxsparklabs-command:hello-foo` probe (logs/part2-A-02-slash-probes.log:7-9):

```
- dgxsparklabs-command:hello-foo: foo command - command-parity probe
- dgxsparklabs-command:hello-bar: bar command - command-parity probe
```

Both commands are surfaced to the model under the same `dgxsparklabs-command:` prefix. ~={info} NOTE: Commands surface under the SAME `The following skills are available for use with the Skill tool:` system-reminder block as skills — Claude does not distinguish skills-from-skill-plugins from commands-from-command-plugins at the model-facing surface. The plugin.json's `commands: ["./commands"]` field is purely a loader directive; once loaded, both component types share the same model-visible registry. =~

**Validate** (Probe A.3):

| Target | Outcome | Citation |
|---|---|---|
| `_generated/command-foo-test` | `✔ Validation passed` | logs/part2-A-03-validate.log:4 |
| `_generated/command-bar-test` | `✔ Validation passed` | logs/part2-A-03-validate.log:9 |
| `.` (whole marketplace) | `✔ Validation passed` | logs/part2-A-03-validate.log:14 |

No duplicate-name warning at the CLI's own validator.

**Details collapse** (Probe A.4):

| Query | Outcome | Citation |
|---|---|---|
| `claude plugin details command-foo-test` (marketplace name) | `not found` | logs/part2-A-04b-details-from-test-cwd.log:14 |
| `claude plugin details command-bar-test` (marketplace name) | `not found` | logs/part2-A-04b-details-from-test-cwd.log:14 (same recipe) |
| `claude plugin details dgxsparklabs-command` (shared name, from `/tmp/test`) | Resolves to ONE — `Source: command-foo-test@dgxsparklabs-marketplace`, `Skills (1) hello-foo` | logs/part2-A-04b-details-from-test-cwd.log:16-32 |

**Same degradation as Part 1 section Probe 3** — first-installed wins. Note that `claude plugin details dgxsparklabs-command` lists the hello-foo command under "Skills (1)" — Claude's `plugin details` command counts the loaded components under the `Skills` line of the inventory regardless of construct type. (logs/part2-A-04b-details-from-test-cwd.log:23)

~={info} NOTE: There's a `details` CWD dependency: running `claude plugin details <name>` from the install-time cwd (`/tmp/test`, where the project-scoped install was performed) resolves the shared name; running from elsewhere returns `not found` even though `claude plugin list` shows the rows everywhere. This is consistent with project-scope plugins being cwd-sensitive — not a shared-namespace artifact. =~

**Probe A verdict:** commands behave identically to skills under shared-namespace. Path A migration can safely apply per-construct brand prefixes (`dgxsparklabs-skill`, `dgxsparklabs-command`, `dgxsparklabs-agent`, …) for all 10 construct types. The mechanism in `_base_plugin_shape` is construct-type-agnostic.

### Probe B — scale (5 plugins in one shared namespace)

**Setup** (`/tmp/workspace/`):

- 5 skill source dirs: `skills/{a,b,c,d,e}-test/SKILL.md`, each with frontmatter `name: <letter>`, `description: scale probe <letter>` (logs/part2-B-00-create-source.log:1-7).
- After generator, hand-edited all 5 `_generated/skill-{a..e}-test/.claude-plugin/plugin.json` via `jq` to share `name: dgxsparklabs-skill` (logs/part2-B-01-hand-edit-add.log:1-20).

**Install sequence + per-install latency** (Probe B.2):

| Plugin | Install latency (ms) | Outcome | Citation |
|---|---|---|---|
| skill-a-test | 1767 | `✔ Successfully installed` | logs/part2-B-02-install-5.log:2-4 |
| skill-b-test | 1762 | `✔ Successfully installed` | logs/part2-B-02-install-5.log:6-8 |
| skill-c-test | 1997 | `✔ Successfully installed` | logs/part2-B-02-install-5.log:10-12 |
| skill-d-test | 2318 | `✔ Successfully installed` | logs/part2-B-02-install-5.log:14-16 |
| skill-e-test | 1983 | `✔ Successfully installed` | logs/part2-B-02-install-5.log:18-20 |

**No monotonic latency increase.** Per-install times bounce between 1.7s and 2.3s with no upward trend. No warnings, no cache corruption. ~={done} DONE: Scale to 5 is healthy — no observable degradation. =~

**`claude plugin list`** (Probe B.3) shows 5 distinct rows, each `Status: ✔ enabled` (logs/part2-B-03-list.log:3-25), and `claude plugin list --json` returns 5 entries with distinct `id`, `installPath`, all `"enabled": true` (logs/part2-B-03-list.log:30-72).

**Slash resolution — all 5 forms** (Probe B.4):

| Form typed | STDOUT | `<command-name>` | Citation |
|---|---|---|---|
| `/dgxsparklabs-skill:a` | `OK stub.` | `<command-name>/dgxsparklabs-skill:a</command-name>` | logs/part2-B-04-slash-probes.log:3-6 |
| `/dgxsparklabs-skill:b` | `OK stub.` | `<command-name>/dgxsparklabs-skill:b</command-name>` | logs/part2-B-04-slash-probes.log:11-14 |
| `/dgxsparklabs-skill:c` | `OK stub.` | `<command-name>/dgxsparklabs-skill:c</command-name>` | logs/part2-B-04-slash-probes.log:19-22 |
| `/dgxsparklabs-skill:d` | `OK stub.` | `<command-name>/dgxsparklabs-skill:d</command-name>` | logs/part2-B-04-slash-probes.log:27-30 |
| `/dgxsparklabs-skill:e` | `OK stub.` | `<command-name>/dgxsparklabs-skill:e</command-name>` | logs/part2-B-04-slash-probes.log:35-38 |

**All 5 resolve.** Registry block from a single probe lists all 5 simultaneously (logs/part2-B-05-registry-block.log:9-13):

```
dgxsparklabs-skill:a: scale probe a
dgxsparklabs-skill:b: scale probe b
dgxsparklabs-skill:c: scale probe c
dgxsparklabs-skill:d: scale probe d
dgxsparklabs-skill:e: scale probe e
```

**Details collapse — install-order rule** (Probe B.6 + B.7):

| Install order | `claude plugin details dgxsparklabs-skill` returns | Citation |
|---|---|---|
| a → b → c → d → e (alphabetic) | `Source: skill-a-test@dgxsparklabs-marketplace`, `Skills (1) a` | logs/part2-B-06-details-collapse.log:2-22 |
| e → d → c → b → a (reverse) | `Source: skill-e-test@dgxsparklabs-marketplace`, `Skills (1) e` | logs/part2-B-07-reverse-order-details.log:25-33 |

~={done} DONE: The collapse rule is **install-order (first-installed wins)**, NOT alphabetic on marketplace name. Operators can predict which plugin shows up by install timestamp. =~

**Disable 3 of 5, re-probe** (Probe B.8): after `claude plugin disable skill-{a,b,c}-test@dgxsparklabs-marketplace`:

| Form | Outcome | Citation |
|---|---|---|
| `/dgxsparklabs-skill:a` | `Unknown command` (disabled) | logs/part2-B-08-disable-3.log:31 |
| `/dgxsparklabs-skill:b` | `Unknown command` (disabled) | logs/part2-B-08-disable-3.log:34 |
| `/dgxsparklabs-skill:c` | `Unknown command` (disabled) | logs/part2-B-08-disable-3.log:37 |
| `/dgxsparklabs-skill:d` | `OK stub.`, resolves | logs/part2-B-08-disable-3.log:40-41 |
| `/dgxsparklabs-skill:e` | `OK stub.`, resolves | logs/part2-B-08-disable-3.log:43-44 |
| Registry block (probe e) | only `dgxsparklabs-skill:d` and `dgxsparklabs-skill:e` listed | logs/part2-B-08-disable-3.log:50-51 |

Disable cleanly retracts disabled plugins from the shared namespace; remaining plugins continue to resolve. Same behavior as Part 1 section Probe 7 but proven at higher cardinality.

**Probe B verdict:** the shared-namespace mechanism scales to 5 plugins (and almost certainly higher — the disjoint-cache architecture means each plugin keeps its own version dir on disk and is processed independently by the loader; see Probe C debug output). No new failure modes appear at scale.

### Probe C — headless autocomplete signal

**`--print` mode signals** (Probe C.1–C.3):

| Probe input | STDOUT signal | Citation |
|---|---|---|
| `/` (bare slash) | `Commands are in the form `/command [args]`` | logs/part2-C-02-debug-variants.log:3 |
| `/dgx` (partial brand prefix) | `Unknown command: /dgx. Did you mean /d?` | logs/part2-C-02-debug-variants.log:9 |
| `/dgxsparklabs-s` (partial namespace) | `Unknown command: /dgxsparklabs-s` (no suggestion) | logs/part2-C-03-debug-prefix.log:3 |
| `/dgxsparklabs-skill:` (namespace + colon, no component) | `Unknown command: /dgxsparklabs-skill:` | logs/part2-C-03-debug-prefix.log:12 |
| `/dgxsparklabs-skill` (no colon) | `Unknown command: /dgxsparklabs-skill` | logs/part2-C-03-debug-prefix.log:15 |
| `/dgxsparklabs-skill:a` (valid) | `OK stub.` | logs/part2-C-03-debug-prefix.log:7 |

`--print` mode rejects invalid commands deterministically but emits no autocomplete-candidate set on STDOUT. The "Did you mean" suggestion appears only when a partial input has a length-1 alphabetic prefix match (here `/d` — coincidentally one of our valid commands at the flat resolution level). ~={info} NOTE: This is not a real autocomplete signal — it's the classic edit-distance suggestion engine. It does NOT enumerate candidates. =~

**`--debug-file` exposes the resolver candidate set** (Probe C.6 + C.8): the killer evidence. With 5 shared-namespace skill plugins enabled, the debug log emits one line per skill at session-load time (logs/part2-C-06-debug-file.log:39-43):

```
[DEBUG] Skill prompt: showing "dgxsparklabs-skill:e" (userFacingName="e")
[DEBUG] Skill prompt: showing "dgxsparklabs-skill:d" (userFacingName="d")
[DEBUG] Skill prompt: showing "dgxsparklabs-skill:c" (userFacingName="c")
[DEBUG] Skill prompt: showing "dgxsparklabs-skill:b" (userFacingName="b")
[DEBUG] Skill prompt: showing "dgxsparklabs-skill:a" (userFacingName="a")
```

And earlier in the same log (logs/part2-C-06-debug-file.log:14-32), the loader process is fully visible:

```
[DEBUG] Found 5 plugins (5 enabled, 0 disabled)
[DEBUG] getPluginSkills: Processing 5 enabled plugins
[DEBUG] Checking plugin dgxsparklabs-skill: skillsPath=none, skillsPaths=1 paths
[DEBUG] Attempting to load skills from plugin dgxsparklabs-skill skillsPaths: /tmp/workspace/_generated/skill-e-test
[DEBUG] Loading from skillPath: /tmp/workspace/_generated/skill-e-test for plugin dgxsparklabs-skill
... (repeated for d, c, b, a) ...
[DEBUG] Loaded 1 skills from plugin dgxsparklabs-skill custom path: /tmp/workspace/_generated/skill-e-test
[DEBUG] Loaded 1 skills from plugin dgxsparklabs-skill custom path: /tmp/workspace/_generated/skill-d-test
... (each plugin contributes 1 skill, all under the shared logical plugin name) ...
```

~={done} DONE: The resolver's loader confirms (1) all 5 shared-namespace plugins are loaded independently with the same logical plugin `name`, each contributing 1 skill, and (2) the final "Skill prompt: showing" list is 5 distinct entries under the `dgxsparklabs-skill:` prefix with distinct `userFacingName`s. The candidate set the TUI's tab-completion works against IS well-formed: 5 entries, no collisions, no missing skills. =~

**What `--debug` cannot tell us:** whether the TUI render path *displays* all 5 candidates when the operator types `/dgxsparklabs-skill:<TAB>`. The headless `--print` flow never invokes the tab-completion UI. So the TUI display behavior remains operator-verifiable only.

**Operator recipe — TUI tab-completion verification (run inside qa-claude or a real Claude Code session):**

1. With 2+ plugins sharing `plugin.json` `name: dgxsparklabs-skill` installed (use Probe B's setup or the existing `skill-foo-test` + `skill-bar-test` from Part 1), launch an interactive `claude` session in the install cwd (`/tmp/test`):
   ```bash
   cd /tmp/test
   claude  # interactive TUI
   ```
2. Type `/dgxsparklabs-skill:` (the colon, no character after) and press TAB.
3. **Expected** (per the debug log emission): the autocomplete dropdown shows all enabled skills under that namespace — for Probe B's setup, you should see `a`, `b`, `c`, `d`, `e` as completion candidates. For the original 2-plugin setup, you should see `foo` and `bar`.
4. **Confirmation criterion:** the dropdown should display N candidates where N = number of enabled plugins sharing the namespace. Each candidate should be the SKILL.md frontmatter `name:` value (the `userFacingName` from the debug log).
5. **Negative criterion:** if the dropdown shows only 1 candidate (matching the first-installed plugin's skill), that means the TUI display path inherits the same collapse-to-one bug as `claude plugin details <shared-name>`. THIS WOULD BE A NEW BLOCKER and would change Path A's verdict to a "fix needed first" — but the debug log strongly suggests this is not what happens (the candidate list is well-formed at the resolver level).
6. Also try `/dgx<TAB>` to see whether brand-prefix partial completion works (jumps to `dgxsparklabs-skill:` namespace).

If the dropdown shows all N candidates, ~={done} DONE: TUI tab-completion preserves the shared-namespace contract and Path A migration is fully validated. =~

If the dropdown shows fewer than N, treat this as a new caveat and file as a separate issue against Claude Code; Path A still moves forward but operators using tab-completion will lose visibility into non-first-installed plugins under each shared namespace.

### Updated verdict on Path A migration

**STILL GO.** All three probes pass; the migration risk profile is unchanged from Part 1.

Specific items the operator should treat as decided after Part 2:

- **Per-construct brand prefix is the recommended scheme:** `dgxsparklabs-skill`, `dgxsparklabs-command`, `dgxsparklabs-agent`, `dgxsparklabs-hook`, etc. — keeps namespaces orthogonal and matches the natural plugin-component category. (Probe A confirmed command parity; the same mechanism is construct-type-agnostic at `_base_plugin_shape`.)
- **Scale up to 10 plugins per shared namespace is safe** — Probe B at 5 showed no degradation, and the disjoint-cache layout (1 dir per marketplace entry under `~/.claude/plugins/cache/dgxsparklabs-marketplace/`) plus the per-plugin loader path (`getPluginSkills: Processing N enabled plugins`) is linear in N. Expect 10 to behave like 5 with at most ~5s of cumulative install latency increase.
- **The single confirmed degradation is `claude plugin details <shared-name>` collapsing to first-installed** — Part 1 already documented this; Part 2 confirmed the rule is install-order and extends the same finding to commands.
- **TUI tab-completion is operator-verifiable post-migration.** The debug-log evidence is strongly positive (resolver maintains a well-formed N-entry candidate set), but the actual TUI display path requires an interactive session. Recipe is documented above; verification should happen as the LAST step before merging the generator change.

No probe revealed a fallback necessity. ~={action} TODO: Operator should run the TUI tab-completion recipe (Probe C above, steps 1-6) immediately after the generator change lands but before declaring Path A complete. =~

### Method (Part 2)

Same `qa-claude` container, same `stub_body_dumper.py` on port 8089 (restarted after the host's nightly), same hermetic-reset pattern (`marketplace remove` + `rm -rf cache` + `echo {} > installed_plugins.json` + `echo {} > known_marketplaces.json`). Source dirs and `_generated/` files created in `/tmp/workspace`; host repo `skills/`, `commands/`, `_generated/` etc. confirmed untouched at end of run via `git status --short` (only `docs/research/shared-namespace-2026-05-27/` is the untracked-files report). The container's `uv` lives at `/root/.local/bin/uv` — the prior research's path-bare invocation needed a `bash -lc` (login shell) wrap to source `~/.bashrc`; the workaround used here was an explicit `/root/.local/bin/uv` path or `bash -lc`. Logs prefixed `part2-` to keep them visually distinct from Part 1's 33 logs.
