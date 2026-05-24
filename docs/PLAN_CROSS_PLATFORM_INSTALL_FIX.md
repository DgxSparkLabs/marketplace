# Plan: Cross-Platform Native Install Compliance (May 2026)

**Status**: v2 — decisions A1, B2, C1, Q2 LOCKED 2026-05-24. Implementation pending.
**Date**: 2026-05-24
**Branch policy**: Continue on `feat/claude-plugin-compliance` (Q2 LOCKED). Same branch as PR #1; scope expands.
**Ground truth**: [[VERIFICATION_2026-05/SUMMARY]] · [[VERIFICATION_2026-05/empirical_act_verification]] · [[VERIFICATION_2026-05/cursor]]
**Prior architecture**: [[PLAN_DI_REFACTOR]] (the DI refactor's 25 locked decisions are the foundation this plan extends, not replaces)

---

## High-Level Overview

### What we set out to verify and what we found

The README described install commands like `git clone` + IDE-open or `gemini extensions install ./.gemini/` as the *canonical* install paths for non-Claude platforms. User instinct: those are workarounds; native marketplace-equivalent installs must exist. Verification confirmed the instinct — every non-Claude platform DOES have a native install mechanism (or strongly equivalent) — but the verification also surfaced that **most of them silently fail against our current generator output** because we're emitting Claude-shaped manifests into platform-shaped paths.

### The eight issues, ranked by user impact

| # | Issue | Visible to user as | Affects |
|---|-------|---------------------|---------|
| 1 | Codex per-plugin install fails | `codex plugin add skill-X` errors `missing or invalid plugin.json` | Every Codex user trying to install one of our 81 plugins |
| 2 | Codex GitHub shortform fails without `--ref` | `codex plugin marketplace add DgxSparkLabs/marketplace` errors `marketplace root does not contain a supported manifest` | Codex users following standard install instructions |
| 3 | Gemini GitHub URL install fails | `gemini extensions install https://github.com/DgxSparkLabs/marketplace --consent` errors `Configuration file not found … gemini-extension.json` | Gemini users wanting one-command install |
| 4 | Windsurf can't see our skills | 26 skills invisible in Cascade; only rules are picked up | Every Windsurf user |
| 5 | No Cursor team-marketplace manifest | Admin paste-GitHub-URL flow fails — there's no `.cursor-plugin/marketplace.json` for Cursor to parse | Cursor 2.6+ teams trying to import our marketplace |
| 6 | Compat CI assertions are shallow | Green CI doesn't mean the integration works; issues 1, 3, 4 went undetected for weeks | Maintainers — false confidence |
| 7 | Skill content 4x duplicated on disk | `.codex/skills/`, `.gemini/skills/`, `.devin/skills/` all byte-identical copies of `skills/` | Repo size, generator runtime |
| 8 | `.claude-plugin/` leaking into mirror dirs | `.claude-plugin/plugin.json` accidentally copied into `.codex/skills/example/` etc. | Cleanliness; potential confusion for platforms |

### The shape of the fix

Three orthogonal additions to the generator + two CI improvements:

1. **`AgentsPlatform`** — new Platform class emitting `.agents/skills/<name>/SKILL.md` (serves Windsurf and Devin natively per official docs; positions us on the cross-platform convergence path)
2. **Per-plugin native manifests** — emit `.codex-plugin/plugin.json` and `.cursor-plugin/plugin.json` alongside the existing `.claude-plugin/plugin.json` in each `_generated/<plugin>/` directory (resolves Codex install, enables Cursor team-import)
3. **Root-level extension/marketplace manifests** — emit `gemini-extension.json` at repo root (resolves Gemini GitHub URL install) and `.cursor-plugin/marketplace.json` at repo root (enables Cursor team-import)
4. **CI assertion depth** — extend `.github/workflows/compat-marketplace-add.yml` Codex job with the missing `codex plugin list | grep` and `codex plugin install` assertions; extend `compat-extension.yml` with the GitHub-URL install variant
5. **Mirror dir hygiene** — fix `shutil.copytree` calls in the existing `Codex/Gemini/DevinPlatform.emit` methods to exclude `.claude-plugin/` from copies

### Recommended sequencing (4 phases)

| Phase | Scope | Why this order |
|-------|-------|----------------|
| **P1 — CI assertions first** | Extend compat-*.yml with the missing assertions (issue #6). Run; let them fail loudly against current generator output. | Establishes the trip-wire that proves the fixes work and prevents regressions. Failing CI is the spec for P2/P3. |
| **P2 — Generator additions** | Add `AgentsPlatform`; emit per-plugin Codex + Cursor manifests; emit root-level `gemini-extension.json` + `.cursor-plugin/marketplace.json`; fix mirror dir hygiene. | Resolves issues 1, 3, 4, 5, 7, 8 in one coherent change. P1's assertions will go green when this lands. |
| **P3 — README rewrite** | Replace the workaround install instructions with verified-working native commands per platform. Cite the act run logs as evidence. | Now the README documents what actually works; users can copy-paste and it executes. |
| **P4 — Merge PR #1** | Issue #2 (Codex shortform without `--ref`) auto-resolves once main has the manifest. | Last because it's free; merging is the trigger. |

### Effort estimate (very rough)

| Phase | Estimate | Confidence |
|-------|----------|------------|
| P1 (CI assertions) | 1-2 hours | High — workflows already exist; we copy verification scaffolds in |
| P2 (generator additions) | 4-6 hours | Medium — touches 4 new emit paths + 2 hygiene fixes; well-scoped per the DI architecture |
| P3 (README rewrite) | 1-2 hours | High — verified commands already on disk in `empirical_act_verification.md` |
| P4 (merge) | 5 minutes | Trivial |
| **Total** | **6-10 hours** | Medium overall |

### What this plan does NOT do

- **Does not change the DI refactor decisions.** All 25 locked decisions from [[PLAN_DI_REFACTOR]] stand. We're adding new Platforms and new emit paths within the existing Construct/Platform protocol.
- **Does not change Claude Code integration.** Claude install is fully working per CL1/CL2/CL3 verification; we touch only `.claude-plugin/`'s neighbors, never `.claude-plugin/` itself.
- **Does not delete `.codex/`, `.gemini/`, `.devin/` mirror dirs.** Some content (skills) could collapse to `.agents/skills/`, but the platforms also have platform-specific bits. Conservative call: keep the mirrors, add `.agents/`. Revisit consolidation as a separate plan if useful.
- **Does not adopt the `.agents/plugins/marketplace.json` canonical path for Codex.** Codex accepts `.claude-plugin/marketplace.json` legacy-compatibly per docs AND per C1/C3 act tests. The canonical path is nicer-but-not-needed. Leave for a future cleanup.

---

## Deep Dive

### Issue 1: Codex per-plugin install fails (`missing or invalid plugin.json`)

**Evidence**
- C5 (act-verified): `codex plugin add skill-example@dgxsparklabs-marketplace` after successful marketplace registration returns:
  > `Error: missing or invalid plugin.json`
  > `Caused by: missing or invalid plugin.json`
- Log: `docs/VERIFICATION_2026-05/logs/C5.txt`, `logs/verify-codex-run.log:386-400`

**Root cause**
Each `_generated/<plugin>/` directory contains `.claude-plugin/plugin.json` (Claude Code's per-plugin manifest, inside a subdirectory). Codex's `plugin add` doesn't recognize that path. WebFetch evidence from `developers.openai.com/codex/plugins/build` (fetched 2026-05-24) says Codex expects `.codex-plugin/plugin.json` per plugin with required fields `name`, `version`, `description` and optional component pointers like `skills: "./skills/"`. The exact required path was not pinned down by C7 (the error doesn't print a path) but the WebFetch docs are explicit.

**Proposed solution (per locked Decision B2)**
Extend the Platform protocol with `build_plugin_json(construct, name) -> dict` (symmetric with the existing `Construct.build_plugin_json(name) -> dict`). Add `CodexPlatform.build_plugin_json` implementation. A new generator Phase 1.5 (after Phase 1 individual plugins) iterates `(plugin × platform)` and writes per-platform per-plugin manifests gated on `platform.supports`:

```python
# In CodexPlatform:
def build_plugin_json(self, construct: Construct, name: str) -> dict:
    full_name = f"{construct.prefix}-{name}"
    manifest = {
        "name": full_name,
        "version": "1.0.0",
        "description": _description_from_source(construct, name),
    }
    # Per-construct pointers (Codex schema)
    if isinstance(construct, SkillConstruct):
        manifest["skills"] = "./skills/"
    elif isinstance(construct, McpConstruct):
        manifest["mcpServers"] = "./mcp.json"
    elif isinstance(construct, HookConstruct):
        manifest["hooks"] = "./hooks/hooks.json"
    # ... per-construct
    return manifest

# In generator Phase 1.5 (gated emission):
for plugin in all_generated_plugins:
    construct_type = type(plugin.construct)
    for platform in PLATFORMS:
        if construct_type in platform.supports:  # B2 gate
            manifest = platform.build_plugin_json(plugin.construct, plugin.name)
            target = plugin.dir / f".{platform.name}-plugin" / "plugin.json"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(manifest, indent=2))
```

Emit only to plugins where `type(construct) in CodexPlatform.supports`. For example, if `CodexPlatform.supports = {SkillConstruct, McpConstruct, RuleConstruct, HookConstruct}`, then `_generated/skill-example/.codex-plugin/plugin.json` is emitted but `_generated/theme-example/.codex-plugin/plugin.json` is NOT.

**Alternatives considered**
- **A. Symlink `.claude-plugin/plugin.json` → `.codex-plugin/plugin.json`** — would fail because schema is different (Claude uses `pluginType`/Claude-specific fields; Codex uses `policy`/component pointers). Rejected.
- **B. Emit only `.codex-plugin/plugin.json`, retire `.claude-plugin/plugin.json`** — breaks Claude install. Rejected.
- **C. Emit a single "universal" plugin.json that both accept** — no such schema exists; the platforms diverge intentionally. Rejected.

**Recommendation**: emit both side-by-side. Each platform reads its own; they coexist without conflict.

**Trade-offs**
- (+) Resolves the install failure cleanly
- (+) Follows the DI refactor's "per-platform emit" pattern; small, localized change
- (-) Each plugin dir grows from one manifest to two (then three with Cursor — see Issue 5)
- (-) The exact required Codex schema is still partly inferred from docs; will need a small focused act test against a known-good Codex plugin to pin down required fields

---

### Issue 2: Codex GitHub shortform fails without `--ref`

**Evidence**
- C2 (act-verified): `codex plugin marketplace add DgxSparkLabs/marketplace` (no ref) fails with:
  > `Error: invalid marketplace file …: marketplace root does not contain a supported manifest`
- C3 (act-verified): same command WITH `--ref feat/claude-plugin-compliance` PASSES
- Logs: `logs/C2.txt`, `logs/C3.txt`

**Root cause**
Without `--ref`, Codex clones the GitHub default branch. Our default branch is `main`. Main does not yet have the DI-refactor manifests because PR #1 has not merged. The feature branch does. So the install works against the branch with manifests and fails against the branch without.

**Proposed solution**
**Do nothing in code.** Issue auto-resolves the moment PR #1 lands on main. Plan P4 (merge) is the fix.

Until then, document the workaround in P3 (README): users on Codex add `--ref feat/claude-plugin-compliance` explicitly during the pre-merge window. After merge, drop that note.

**Alternatives considered**
- **A. Cherry-pick the manifest files to main as a fast-follow** — pollutes main with partial state; the rest of the DI refactor would still need to land in a follow-up commit. Reject.
- **B. Hold all other fixes until PR #1 merges, then re-test** — too sequential; loses parallelism.

**Recommendation**: include in P4 as a passive resolution.

---

### Issue 3: Gemini GitHub URL install fails (`Configuration file not found at <tmp>/gemini-extension.json`)

**Evidence**
- G2 (act-verified): `gemini extensions install https://github.com/DgxSparkLabs/marketplace --consent` fails with `Configuration file not found at /tmp/gemini-extensionOunyeo/gemini-extension.json`
- G3 (act-verified): same with `--ref feat/claude-plugin-compliance` — same error
- G1 (act-verified, baseline): `gemini extensions install ./.gemini/ --consent` PASSES (because that points directly at the directory containing the manifest)
- Logs: `logs/G2.txt`, `logs/G3.txt`, `logs/G1.txt`

**Root cause**
Gemini's `extensions install` clones the GitHub repo to a temp dir and then looks for `gemini-extension.json` at the cloned repo ROOT. We store it at `.gemini/gemini-extension.json` (a subdirectory). Gemini has no `--path` option on `extensions install` to redirect the lookup (verified by `gemini extensions install --help`).

**Proposed solution**
Emit `gemini-extension.json` at **repo root** in addition to `.gemini/gemini-extension.json`. The two are identical content; the root copy enables `gemini extensions install https://github.com/…`, the `.gemini/` copy maintains the local install path (`gemini extensions install ./.gemini/ --consent`).

Generator change: add a step at the end of `GeminiPlatform.emit` (or as a top-level generator step) that copies `.gemini/gemini-extension.json` to the repo root.

**Alternatives considered**
- **A. Move `gemini-extension.json` to repo root, remove from `.gemini/`** — would break the local-install path our existing CI uses. Reject.
- **B. Use `gemini extensions link <path>` instead** — `link` is for development-mode dynamic loading, not user installs. Wrong abstraction.
- **C. Restructure repo so `.gemini/` IS the repo root** — radical, breaks Claude-first design. Reject.

**Recommendation**: write `gemini-extension.json` at both `.gemini/gemini-extension.json` and repo root. Net: one extra small file at repo root, two install paths work.

**Trade-offs**
- (+) Resolves the URL install failure
- (+) Single line of `shutil.copy` in the generator
- (-) Adds a top-level file to the repo (one more thing visible at root); annotate clearly in README that this exists for Gemini install only

---

### Issue 4: Windsurf can't see our skills

**Evidence**
- Research (WebFetch from `docs.windsurf.com/windsurf/cascade/skills`, 2026-05-24): "Skills are automatically loaded from `.windsurf/skills/<name>/SKILL.md`. Windsurf also discovers skills in `.agents/skills/` and `~/.agents/skills/`."
- Local inspection of generator: `WindsurfPlatform.supports = {RuleConstruct}` only — no `SkillConstruct`.
- Consequence: 26 skills in `skills/` are invisible to Windsurf users; only the 21 rules show up.

**Proposed solution (preferred)**
Add a new `AgentsPlatform` class emitting `.agents/skills/<name>/<files>` in the existing `_generated/` → mirror pattern. Both Windsurf and Devin read `.agents/skills/` natively (verified). Cursor reads it too (per `cursor.com/docs/context/skills`). So one Platform emission serves three platforms at the runtime level.

```python
@dataclass
class AgentsPlatform:
    name: str = "agents"
    mirror_dir: Path = Path(".agents")
    supports: set[type[Construct]] = field(default_factory=lambda: {SkillConstruct})

    def emit(self, construct: Construct, name: str, source_dir: Path):
        if isinstance(construct, SkillConstruct):
            target = self.mirror_dir / "skills" / name
            shutil.copytree(source_dir, target, ignore=shutil.ignore_patterns(".claude-plugin", "*.pyc"))
```

**Alternative considered**
- **A. Add `SkillConstruct` to `WindsurfPlatform.supports` and emit `.windsurf/skills/`** — works for Windsurf but doesn't help Devin or position us on the `.agents/` convergence. Strictly worse than the `AgentsPlatform` option.

**Recommendation**: `AgentsPlatform`. After it lands and `devin skills list` confirms `.agents/skills/` is picked up by Devin, consider retiring `.devin/skills/` emission as a follow-up (decision deferred).

**Trade-offs**
- (+) Resolves Windsurf invisibility
- (+) Sets up future consolidation of `.devin/skills/` → `.agents/skills/`
- (+) Aligns with the broader ecosystem convergence per multiple platform docs
- (-) Adds another mirror dir; net repo size increases until we collapse the Devin mirror later

---

### Issue 5: No Cursor team-marketplace manifest (`.cursor-plugin/marketplace.json`)

**Evidence**
- Research (WebFetch from `cursor.com/docs/plugins`, 2026-05-24): Cursor team marketplaces import a GitHub repo URL via Dashboard. The repo must have `.cursor-plugin/marketplace.json` listing all plugins (per `github.com/cursor/plugins` README).
- Local inspection: no `.cursor-plugin/` directory exists in the repo.
- Per-plugin: Cursor expects `<plugin>/.cursor-plugin/plugin.json` with `name` required, everything else optional and auto-discovered.

**Proposed solution (per locked Decision B2)**
Extend the existing `CursorPlatform` class with `build_plugin_json` (Platform protocol extension). The generator's new Phase 1.5 writes `_generated/<plugin>/.cursor-plugin/plugin.json` per plugin, gated on `type(construct) in CursorPlatform.supports`. Additionally, a top-level generator step writes `.cursor-plugin/marketplace.json` at repo root (multi-plugin list, analogous to `.claude-plugin/marketplace.json`).

```python
# In CursorPlatform (already exists for rules; we add build_plugin_json):
def build_plugin_json(self, construct: Construct, name: str) -> dict:
    full_name = f"{construct.prefix}-{name}"
    # Cursor's manifest is very forgiving — only `name` required.
    # Everything else auto-discovers from default subdirs (skills/, rules/, agents/, ...).
    return {"name": full_name}
```

The per-plugin manifest is essentially trivial — Cursor's schema only requires `name` and auto-discovers components from default subdirectory names. The root-level `marketplace.json` collects every plugin Cursor supports.

**Alternative considered**
- **A. Only emit the root marketplace.json, skip per-plugin manifests** — risk: Cursor's auto-discovery from the plugin source dir might not work for our `_generated/` layout. Conservative call: emit both. Cost is minimal.

**Recommendation**: emit both. Per-plugin manifest is one-line JSON.

**Trade-offs**
- (+) Unlocks Cursor team marketplace import path
- (+) Cleanly extends the existing CursorPlatform pattern
- (-) Adds one more file per plugin (now 3 per-plugin manifests: Claude, Codex, Cursor)
- (-) Cursor team marketplace import is admin-only and requires a Teams/Enterprise plan; not universal user-facing benefit. But it's the **only** native install path for Cursor 2.6+; alternative is "clone and open in IDE" which still works.

---

### Issue 6: Compat CI assertions are shallow (false-confidence in CI)

**Evidence**
- `.github/workflows/compat-marketplace-add.yml` Codex job: only `codex plugin marketplace add ./` + `grep config.toml`. Never checks plugin enumeration (C4) or install (C5).
- `.github/workflows/compat-extension.yml`: only tests local path; never tests GitHub URL install (G2/G3).
- Result: issues 1 and 3 went undetected for weeks despite "green CI."

**Proposed solution**
Promote the verification scaffolds in `docs/VERIFICATION_2026-05/workflows/` to production by merging their new steps into the existing `compat-*.yml`. Specifically:

| Existing workflow | Add these steps |
|-------------------|-----------------|
| `compat-marketplace-add.yml` Codex job | After registration: `codex plugin list \| grep skill-example` (asserts enumeration); `codex plugin add skill-example@dgxsparklabs-marketplace` (asserts install); cleanup `codex plugin remove`. |
| `compat-extension.yml` | New `gemini-github-url-install` job: `gemini extensions install https://github.com/DgxSparkLabs/marketplace --ref ${{ github.ref_name }} --consent`; assert exit 0; cleanup. Runs only on pushes to feature branches and PRs against main (where the ref is known). |
| `compat-marketplace-add.yml` Claude job | After registration: `claude plugin install skill-example@dgxsparklabs-marketplace --scope project`; `claude plugin list \| grep skill-example`. (CL2, CL3 — caught nothing today but prevents future regressions.) |

**Alternative considered**
- **A. Run the verification workflows as-is in CI** — keeps verification separate from production CI; downside is two parallel surfaces to maintain. Reject.

**Recommendation**: fold the new assertions into existing workflows. Keep `docs/VERIFICATION_2026-05/workflows/` as the historical record.

**Trade-offs**
- (+) Trip-wire prevents regression of any fix in P2
- (+) Reuses well-tested act-verified assertions
- (-) Codex install step requires `.codex-plugin/plugin.json` to exist — so P1 (CI) and P2 (generator) become coupled: ship them together or CI goes red

**Sequencing implication**: P1 (CI) and P2 (generator) should land in the same PR, even though they're separate phases. CI changes ALONE would break the build; generator changes alone would have no test. They're a unit.

---

### Issue 7: Skill content 4x duplicated on disk

**Evidence**
- `skills/` (source), `.codex/skills/`, `.gemini/skills/`, `.devin/skills/` all contain byte-identical copies of every skill. No platform-specific transformation.

**Proposed solution**
Add `AgentsPlatform` per Issue 4 → now 5 copies temporarily. Once verified that Devin reads `.agents/skills/` (per official docs + our existing May-22 empirical evidence from `devin skills paths`), retire `.devin/skills/` emission. Net: 4 → 4 (with `.devin/` removed, `.agents/` added).

Codex and Gemini retain their per-platform skill dirs (`.codex/skills/`, `.gemini/skills/`) until/unless their official docs confirm `.agents/skills/` reads at project scope. Today neither is confirmed; conservative call is to keep them.

**Alternative considered**
- **A. Symlinks instead of copies** — fragile on Windows (the generator runs on Windows; symlinks require admin or developer mode).
- **B. Drop `.codex/skills/` and `.gemini/skills/` immediately, assume `.agents/skills/` is read** — risky given current docs. Defer.

**Recommendation**: incremental retirement, starting with `.devin/skills/` after `AgentsPlatform` lands.

**Trade-offs**
- (+) Small first step on consolidation
- (+) Aligned with ecosystem convergence
- (-) Doesn't fully solve duplication; full collapse requires platform docs to catch up

---

### Issue 8: `.claude-plugin/` leaks into mirror dirs

**Evidence**
- `.codex/skills/example/`, `.gemini/skills/example/`, `.devin/skills/example/` each contain a copy of the source's `.claude-plugin/plugin.json` — meaningless on those platforms.
- Caused by `shutil.copytree(skill_source_dir, target)` calls in Platform emit methods that don't ignore `.claude-plugin/`.

**Proposed solution**
Add `.claude-plugin` (and `.codex-plugin`, `.cursor-plugin` once those exist as source-side dirs in `_generated/`) to the `ignore_patterns` of every `shutil.copytree` call in Platform emit methods that are NOT the target platform's own manifest dir.

```python
# In each Platform.emit:
shutil.copytree(
    source_dir, target_dir,
    ignore=shutil.ignore_patterns(
        "__pycache__", "*.pyc",
        ".claude-plugin", ".codex-plugin", ".cursor-plugin",  # cross-platform manifest dirs
    ),
)
```

Each platform's own emit then writes its own manifest after the copytree, ensuring only the right manifest lands in the right place.

**Alternative considered**
- **A. Only ignore `.claude-plugin` (the current leaking case)** — works today but bites us again when we add `.codex-plugin/` and `.cursor-plugin/` per-plugin manifests. Reject in favor of the full pattern.

**Recommendation**: full ignore pattern across all manifest dirs in every Platform emit method.

**Trade-offs**
- (+) Defensive — won't bite us again when new manifest dirs are added
- (+) Two-line change per Platform class
- (-) None

---

## Architectural Decisions To Lock

Before any code change, three decisions need to be made.

### Decision A: Is `.agents/` a Platform or a directory mirror?  →  **LOCKED: A1**

`AgentsPlatform` is a proper Platform class per the DI strategy pattern. Same shape as the other six Platforms: `name`, `mirror_dir`, `supports`, `emit`. Not a hack, not a special-case step.

Considered and rejected: A2 (top-level emit step outside Platform abstraction).

### Decision B: Per-plugin native manifest emission strategy  →  **LOCKED: B2**

Emit per-plugin native manifests **only where the platform supports the construct type**. Gate on `platform.supports`:

```python
# In generator, after Phase 1 (individual plugins generated) — new Phase 1.5:
for plugin in all_generated_plugins:
    construct_type = type(plugin.construct)
    for platform in PLATFORMS:
        if construct_type in platform.supports:
            manifest = platform.build_plugin_json(plugin.construct, plugin.name)
            target = plugin.dir / f".{platform.name}-plugin" / "plugin.json"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(manifest, indent=2))
```

This requires extending the Platform protocol with one new method:

```python
class Platform(Protocol):
    name: str
    mirror_dir: Path
    supports: set[type[Construct]]
    def emit(self, construct: Construct, name: str, source_dir: Path) -> None: ...
    def build_plugin_json(self, construct: Construct, name: str) -> dict: ...  # NEW
```

Why this matters:
- A `_generated/theme-example/` directory will have `.claude-plugin/plugin.json` (Claude supports themes) but NOT `.codex-plugin/plugin.json` (Codex doesn't include `ThemeConstruct` in `supports`). The on-disk layout encodes which platforms can host which constructs — no fiction, no per-platform manifests for things the platform can't use.
- Adding a new construct type requires defining `supports` membership ONCE per platform; per-plugin manifest emission falls out automatically. No drift.
- Adding a new platform requires implementing `build_plugin_json` and declaring `supports`; the generator's Phase 1.5 picks it up with no additional wiring.

Considered and rejected: B1 (emit all three formats unconditionally — would pollute plugin dirs with manifests platforms can't use); B3 (emit only formats CI proves — too slow to bootstrap, hard to reason about).

### Decision C: Sequence CI and generator changes — together or separately?  →  **LOCKED: C1**

CI assertion extensions and generator additions land in the same PR (PR #1 scope expansion). They're a unit because the CI assertions assume the manifest fixes are present.

Considered and rejected: C2 (CI first, deliberately-red CI window); C3 (generator first, retroactive tests).

---

## Recommended Sequencing (concrete)

Assuming all three decisions land per recommendations (A1, B1, C1):

**Phase 1: Platform protocol extension + Generator additions + CI assertions (one PR-worth of work)**
1. **Protocol**: extend `Platform` protocol in `scripts/platforms.py` with `build_plugin_json(construct: Construct, name: str) -> dict`. Document in the docstring that it's called by Phase 1.5 and gated on `supports`.
2. **AgentsPlatform**: add to `scripts/platforms.py`, register in `PLATFORMS`. `supports = {SkillConstruct}`, `mirror_dir = Path(".agents")`, emits `.agents/skills/<name>/`. `build_plugin_json` returns `{}` (Agents doesn't host plugin manifests, only skill content).
3. **CodexPlatform.build_plugin_json**: implement per-construct schema (per Issue 1 sketch). Returns the Codex manifest dict.
4. **CursorPlatform.build_plugin_json**: implement minimal `{"name": full_name}` per Issue 5.
5. **ClaudePlatform.build_plugin_json**: already exists implicitly via `Construct.build_plugin_json(name)` — wrap it for protocol symmetry (or designate Claude as the special case the protocol doesn't apply to; decide during implementation).
6. **Generator Phase 1.5**: new phase after Phase 1, iterates `(plugin × platform)`; gated emission of `_generated/<plugin>/.<platform>-plugin/plugin.json` where `type(construct) in platform.supports`.
7. **Root-level `gemini-extension.json`**: new top-level generator step copies `.gemini/gemini-extension.json` to repo root.
8. **Root-level `.cursor-plugin/marketplace.json`**: new top-level generator step writes the Cursor multi-plugin marketplace manifest.
9. **Mirror dir hygiene**: extend `shutil.copytree` `ignore_patterns` in every Platform emit method to exclude `.claude-plugin`, `.codex-plugin`, `.cursor-plugin`.
10. **CI extensions**: extend `compat-marketplace-add.yml` Codex job with `codex plugin list \| grep skill-example` and `codex plugin add skill-example@dgxsparklabs-marketplace`. Extend Claude job with `claude plugin install` + `claude plugin list`. Add `gemini-github-url-install` job to `compat-extension.yml`.
11. **Tests**: extend `tests/test_marketplace.py` with new assertions covering: per-platform per-plugin manifests exist where gated; root-level `gemini-extension.json` and `.cursor-plugin/marketplace.json` exist; mirror dirs don't contain leaked `.claude-plugin/`. Run full suite.
12. **Verify**: regenerate all manifests; run `act` against verification scaffolds locally to ensure all new assertions go green.

**Phase 2: README rewrite**
1. Replace each per-platform install section with verified-working native commands (citing act log evidence).
2. Drop the "clone and open in IDE" framing where a native install now works.
3. Keep clone-and-open as the fallback for Cursor/Windsurf where no CLI plugin install exists.

**Phase 3: Merge PR #1**
1. Verify CI green on the tip commit.
2. `gh pr merge 1 --merge` (or `--squash`).
3. C2 (Codex shortform without `--ref`) starts passing as soon as main has the manifest.

**Phase 4 (optional, defer): Retire `.devin/skills/`**
1. Verify Devin reads from `.agents/skills/` at project scope via a focused act test (or live `devin skills list` if user wants to run it manually).
2. Remove `SkillConstruct` from `DevinPlatform.supports`.
3. Re-test.

---

## Risk Register

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|------------|--------|------------|
| R1 | Codex's exact required per-plugin manifest path differs from `.codex-plugin/plugin.json` | Medium (WebFetch docs are explicit but live verification didn't pin it down) | High (P2 generator change wouldn't actually fix C5) | Before writing the generator change, run a focused act test: emit a minimal `.codex-plugin/plugin.json` per WebFetch spec, re-run C5 in act, confirm PASS. ~30 min added to P2. |
| R2 | Gemini's GitHub URL install still fails even with root-level `gemini-extension.json` | Low (the error message is explicit about the path) | High (P2 generator change wouldn't fix G2/G3) | Same pattern: focused act test before the full generator change. |
| R3 | The per-plugin Cursor manifest `{"name": "..."}` is too minimal and Cursor rejects it | Low (docs explicitly say `name` is the only required field) | Medium (Cursor team-import flow stays broken) | Add an act test for Cursor team-import path; if cursor.com has no headless way to test that import, accept this as untestable and validate manually post-merge. |
| R4 | Adding `gemini-extension.json` at repo root confuses users / shadows the `.gemini/` copy | Low | Low | Document clearly in README that the root copy exists solely for GitHub-URL install convenience and is byte-identical to `.gemini/gemini-extension.json`. |
| R5 | New CI assertions are flaky in act vs. real GHA | Low | Medium | The verification scaffolds already ran successfully in act; promoting their content to real workflows should behave the same. Watch the first real-GHA run carefully. |
| R6 | Mirror dir hygiene change (Issue 8) breaks something we don't realize depends on `.claude-plugin/` being copied | Low | Low | Run full test suite + check generated diff before committing. Easy to revert. |
| R7 | PR #1 review surface grows from "DI refactor + multi-platform validation" to "DI refactor + multi-platform validation + native install fix" — reviewer fatigue | Medium | Low | Communicate clearly in PR description that each phase is internally coherent; provide this plan as the reading guide. Alternative: ship native install fix as a fast-follow PR (changes recommended sequencing to "merge PR #1 first, then start the fix from a fresh branch"). User decision. |

---

## Open Questions

1. ~~**(Decision A/B/C above)** — locked or alternative?~~ **RESOLVED 2026-05-24**: A1, B2, C1 all locked.
2. ~~**(R7 mitigation)** — keep all P1/P2 on `feat/claude-plugin-compliance` (one big PR) or split?~~ **RESOLVED 2026-05-24**: Same branch `feat/claude-plugin-compliance`; expand PR #1 scope.
3. **(Bonus: Codex `.agents/plugins/marketplace.json` canonical path)** — emit it or rely on legacy-compatible `.claude-plugin/marketplace.json`? Per docs both work; legacy form is verified. Adding canonical form is one extra file. Decision: defer to "do it if cheap" during P1 implementation.
4. **(Bonus: SKILL.md frontmatter for Gemini remote install)** — Issue G4 left unresolved. Worth a focused frontmatter probe to learn what Gemini wants, but not blocking the main plan. Could be a small follow-up.
5. **(Bonus: Cursor `--plugin-dir` flag)** — research surfaced this flag exists on the `agent` CLI for runtime plugin injection. Worth exploring for testing scenarios, but not for end-user install. Defer.
6. **(NEW: ClaudePlatform.build_plugin_json)** — does Claude need an explicit Platform `build_plugin_json` implementation, or does it stay special-cased through `Construct.build_plugin_json`? Decide during implementation; doesn't block.

---

## Cross-References

- [[VERIFICATION_2026-05/SUMMARY]] — ground truth single-page synthesis
- [[VERIFICATION_2026-05/empirical_act_verification]] — full per-claim table with log refs
- [[VERIFICATION_2026-05/cursor]] — Cursor IDE + CLI research
- [[PLAN_DI_REFACTOR]] — the DI architecture this plan extends
- [[PLATFORM_INSPECTION_CATALOG]] — empirical CLI commands catalog
- [[EMPIRICAL_CLI_FINDINGS/README]] — May 22 baseline
- `scripts/platforms.py` — where `AgentsPlatform` would be added
- `scripts/constructs.py` — Construct protocol; no changes expected
- `.github/workflows/compat-marketplace-add.yml` — target for P1 Codex assertion additions
- `.github/workflows/compat-extension.yml` — target for P1 Gemini URL install assertion
- `README.md` — target for P2 rewrite

---

## Status of this plan

**v2 — decisions locked, implementation pending.**

Decisions locked 2026-05-24:
- A1: `AgentsPlatform` as a proper Platform class
- B2: per-plugin native manifests gated on `platform.supports`
- C1: CI assertions + generator additions ship in same PR
- Q2: same branch `feat/claude-plugin-compliance`; expand PR #1 scope

Next step: spawn implementing subagent with this plan as the brief (matching the [[PLAN_DI_REFACTOR]] pattern), or implement directly. Pending user direction.
