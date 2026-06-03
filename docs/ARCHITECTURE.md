---
date: 2026-05-24
purpose: generator architecture, protocols, generation phases
status: live
---

# Architecture

The generator turns canonical source content (skills, rules, ...) into platform-native install artifacts using a strategy pattern. Two protocols — `Construct` and `Platform` — encapsulate per-type and per-platform behavior; a thin orchestrator in `scripts/generate_manifest.py` runs nine phases (numbered 1, 1.5, 2a, 2b, 3, 4, 4.5, 5, 6) to produce per-platform manifests and mirrors. Mirror hygiene is built in via shared `shutil.copytree` ignore patterns. This document is the canonical reference for the protocols, the phases, and the contracts they uphold. For per-platform install behavior, see [[PLATFORMS]].

## How to read this document

Start with the section that matches what you want to do:

- **Adding a new construct type** (a new plugin kind like `skill` or `rule`): jump to *The two protocols → Construct*, then *How to extend → Adding a new construct type*.
- **Adding a new platform** (a new emission target like Claude or Codex): jump to *The two protocols → Platform*, then *The seven platform classes* and *How to extend → Adding a new platform*.
- **Understanding why an output file exists**: read *The six generation phases* end-to-end; each phase output is annotated with its trigger.
- **Debugging a stray file in the wrong directory**: jump to *Mirror hygiene*.
- **Writing CI assertions**: read *The `supports` gate*, then cross-check against the CI tables in [[PLATFORMS]].
- **Just trying to orient**: read *The two protocols* and *Things worth knowing*, in that order.

## The two protocols

### Construct

`scripts/constructs.py:38-56` defines the `Construct` protocol with two methods and three attributes:

```python
@runtime_checkable
class Construct(Protocol):
    prefix: str               # e.g., "skill"
    source_directory: Path    # e.g., Path("skills/") — relative to repo root
    category: str             # marketplace.json category tag

    def build_plugin_json(self, name: str) -> dict:
        """Build the plugin.json content dict. Pure — no I/O."""

    def emit(self, name: str, target_dir: Path) -> None:
        """Write the full plugin to target_dir: copy source, generate
        construct-specific artifacts (e.g., activate.sh for rules), and
        write .claude-plugin/plugin.json. Does ALL I/O for this instance."""
```

Ten concrete implementations live in the same file: `SkillConstruct`, `RuleConstruct`, `CommandConstruct`, `AgentConstruct`, `HookConstruct`, `MCPConstruct`, `LSPConstruct`, `MonitorConstruct`, `OutputStyleConstruct`, `ThemeConstruct`. Each knows where its source content lives and how to build its plugin.json shape. The `CONSTRUCTS` registry (a `dict[str, Construct]`) is the single source of truth.

For the user-facing reference table of all 10 construct types, see [[CONSTRUCT_TYPES]].

### Platform

`scripts/platforms.py:64-82` defines the `Platform` protocol:

```python
class Platform(Protocol):
    name: str                       # e.g., "codex"
    mirror_directory: Path | None   # None for ClaudeCode (no separate mirror)
    supports: set[type[Construct]]  # CLASSES of supported constructs

    def emit(self, construct: Construct, name: str) -> None:
        """Emit the mirror for this construct instance under mirror_directory."""

    def build_plugin_json(self, construct: Construct, name: str) -> dict:
        """Produce the per-platform per-plugin manifest dict (no I/O).
        Called by generator Phase 1.5 for each (plugin, platform) pair where
        type(construct) in self.supports. Return {} to skip emission."""
```

`build_plugin_json` is the mechanism for emitting per-plugin native manifests at `_generated/<plugin>/.<platform>-plugin/plugin.json` only where the platform actually hosts that construct type. Seven concrete implementations live in `scripts/platforms.py`; the `PLATFORMS` registry at `scripts/platforms.py:344-352` is the single source of truth.

## How to extend

### Adding a new construct type

Pick a `prefix` (e.g., `widget`) and a source directory (e.g., `widgets/`). Then:

1. **Add the class** in `scripts/constructs.py`. Implement `build_plugin_json(name) -> dict` (returns the dict that becomes `.claude-plugin/plugin.json`) and `emit(name, target_dir)` (writes the plugin directory to disk — copy source, generate any per-construct artifacts, call `write_plugin_json(target_dir, self.build_plugin_json(name))`).
2. **Register it** by adding an instance to the `CONSTRUCTS` dict at the bottom of `scripts/constructs.py`.
3. **Declare platform support** in `scripts/platforms.py`: add the construct class to each platform's `supports` set where it should be hosted. Phase 1.5 picks it up automatically.
4. **Add per-platform manifest logic** in any `Platform.build_plugin_json` that needs it (e.g., Codex emits `"widgets": "./widgets/"` pointer for skill-like constructs).
5. **Write tests** in `tests/test_marketplace.py` — the test suite iterates `CONSTRUCTS.values()` uniformly, so most coverage falls out for free. Add a specific test if your construct has unusual emission logic.
6. **Add walkthrough lines** in [[ADDING_A_CONSTRUCT]] and a row in [[CONSTRUCT_TYPES]].
7. **Regenerate** with `uv run scripts/generate_manifest.py`, inspect `_generated/widget-*/`, and verify the new directories appear.

You do NOT need to modify `generate_manifest.py` — the orchestrator iterates the registries.

### Adding a new platform

Pick a `name` (e.g., `myide`) and a mirror directory (e.g., `.myide/`, or `None` if the platform installs explicitly without a mirror). Then:

1. **Add the class** in `scripts/platforms.py`. Implement `emit(construct, name)` (writes mirrored content to `self.mirror_directory`, using `shutil.copytree(..., ignore=_COPY_IGNORE)`) and `build_plugin_json(construct, name)` (returns the per-platform per-plugin manifest dict, or `{}` to skip).
2. **Declare `supports`** as a set of construct classes — only these get per-plugin manifests and mirror content.
3. **Register it** by adding an entry to the `PLATFORMS` dict at the bottom of `scripts/platforms.py`.
4. **Wire any platform-level emissions** that don't fit the per-plugin pattern (e.g., `GeminiPlatform.emit_extension_manifest` writes the repo-level `gemini-extension.json` from Phase 4; see also Phase 4.5 root copy and Phase 6 root `.cursor-plugin/marketplace.json`).
5. **Add a section in [[PLATFORMS]]** with install path, discovery commands, supports table, CI assertions, and known gaps.
6. **Add a `compat-<construct>.yml` job** in `.github/workflows/` for each construct your platform supports — install the marketplace, run an introspection command, grep for the expected substring.
7. **Regenerate** and verify `_generated/<plugin>/.myide-plugin/plugin.json` appears for supported constructs only.

Phase 1.5 (per-plugin manifests), Phase 3 (mirror generation), and the `supports` gate require no changes — adding the platform class is enough.

### Modifying generation phases

Phases run sequentially in `main()` at `scripts/generate_manifest.py:110-244`. Reasons to touch them:

- **Add a new phase**: when an emission has no logical home in the existing phases. Example: Phase 4.5 was added to copy `gemini-extension.json` to the repo root because `gemini extensions install <github-url>` looks for it there, not in `.gemini/`. Number the new phase with `.5` to preserve readability of the original five-phase design.
- **Extend an existing phase**: when adding behavior that fits the phase's purpose. Example: if a new platform needs a repo-root manifest similar to Cursor's, extend Phase 6 (or copy the pattern into a new sibling phase).
- **Don't touch Phase 1 / 2a / 3 / 5**: these are the load-bearing core. Phase 1 emits per-plugin Claude manifests; 2a emits catalog bundles; 3 wipes and re-emits all mirrors; 5 writes the aggregated `.claude-plugin/marketplace.json`. Adding new behavior at these layers risks breaking the `supports` gate or the in-memory marketplace aggregation. (Phase 2b — per-construct catch-all bundles — was retired 2026-05-27.)

Phases interact through two shared structures: `marketplace_entries: list[dict]` (Phase 1/2a/2b append; Phase 5 writes) and `individual_plugins: list[tuple[Path, Construct, str]]` (Phase 1 populates; Phase 1.5 and Phase 6 iterate).

## The seven platform classes

| Class | File:line | `supports` | Mirror dir | Why it exists |
|---|---|---|---|---|
| `ClaudeCodePlatform` | `scripts/platforms.py:102-139` | 9 of 10 constructs (RuleConstruct intentionally excluded per `code.claude.com/docs/en/plugins-reference#plugin-components-reference`, 2026-05-26 — rules are a memory feature, not a plugin component) | none (no separate mirror) | Canonical platform; `marketplace.json` + per-plugin `.claude-plugin/plugin.json` are written by main flow. `build_plugin_json` delegates to the construct so Claude schema stays a single source of truth. |
| `CodexPlatform` | `scripts/platforms.py:128-191` | skill, mcp, hook, agent | `.codex/` | Codex reuses our `.claude-plugin/marketplace.json` (legacy-compatible). Emits `.codex-plugin/plugin.json` per supported plugin. Skill mirror retired (D-1, 2026-05-25); only `.codex/agents/<n>.toml` is emitted to the mirror dir (sub-agent TOML converted from Claude-style markdown via `scripts/converters/md_to_toml.py`). |
| `GeminiPlatform` | `scripts/platforms.py:194-256` | skill, agent, hook | `.gemini/` | Mirrors skills to `.gemini/skills/`, sub-agents to `.gemini/agents/<n>.md`, and hooks to `.gemini/hooks/hooks.json` (per Gemini extensions reference, 2026-05-25). Emits the repo-level `.gemini/gemini-extension.json` via `emit_extension_manifest` (Phase 4). Returns `{}` from `build_plugin_json` — Gemini's install unit is extensions, not plugins. |
| `CursorPlatform` | `scripts/platforms.py:259-330` | rule, skill, agent, command, hook, mcp | `.cursor/` | Emits `.cursor/rules/<name>.md` from per-rule format files and `.cursor/agents/<n>.md` for workspace-level sub-agents (Cursor 2.4 schema). Command/Hook/MCP are surfaced via per-plugin `.cursor-plugin/plugin.json` pointer fields (auto-discovered by Cursor). Skills served from `.agents/` — no `.cursor/skills/`. |
| `WindsurfPlatform` | `scripts/platforms.py:333-370` | rule, hook | `.windsurf/` | Emits `.windsurf/rules/<name>.md` with `trigger:` frontmatter and `.windsurf/hooks.json` (per Windsurf Cascade hooks docs, 2026-05-25). No CLI exists; `build_plugin_json` returns `{}`. |
| `DevinPlatform` | `scripts/platforms.py:373-394` | skill | `None` | Devin reads rules from `.cursor/rules/` natively and skills from `.agents/skills/` (verified Q-B1, 2026-05-25). Skill mirror retired (D-1); `mirror_directory` is `None` so Phase 3 skips it. `supports` keeps `SkillConstruct` so a future per-plugin Devin manifest schema can plug in via Phase 1.5 without code changes. |
| `AgentsPlatform` | `scripts/platforms.py:397-442` | skill, rule | `.agents/` | The `.agents/skills/<name>/SKILL.md` path is read natively by Windsurf, Cursor, AND Devin — a true cross-platform skill convergence. Also emits `.agents/rules/<name>.md` as forward-looking convergence (D-12, 2026-05-25). Implemented as a proper Platform class (not a special-case step) for symmetry. Hosts content only — `build_plugin_json` returns `{}`. |

## The six generation phases

```
        source content (skills/, rules/, commands/, ...)
                            │
                            ▼
            ┌───────────────────────────────┐
            │ Phase 1: per-plugin Claude    │  → _generated/<prefix>-<name>/
            │   plugin.json + content       │      .claude-plugin/plugin.json
            └───────────────┬───────────────┘
                            │ (marketplace_entries + individual_plugins lists)
                            ▼
            ┌───────────────────────────────┐
            │ Phase 1.5: per-platform       │  → _generated/<plugin>/
            │   per-plugin manifests        │      .codex-plugin/plugin.json
            │   (gated on supports)         │      .cursor-plugin/plugin.json
            └───────────────┬───────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │ Phase 2a: catalog bundles     │  → _generated/bundle-<name>/
            └───────────────┬───────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │ Phase 2b: (retired 2026-05-27)│  per-construct catch-alls removed
            └───────────────┬───────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │ Phase 3: mirror generation    │  → .codex/, .gemini/, .cursor/,
            │   (wipe, then emit per supports) │   .windsurf/, .devin/, .agents/
            └───────────────┬───────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │ Phase 4: gemini-extension     │  → .gemini/gemini-extension.json
            └───────────────┬───────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │ Phase 4.5: root-level copy    │  → gemini-extension.json (root)
            └───────────────┬───────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │ Phase 5: aggregated marketplace │ → .claude-plugin/marketplace.json
            └───────────────┬───────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │ Phase 6: cursor team-import   │  → .cursor-plugin/marketplace.json
            │   root manifest               │
            └───────────────────────────────┘
```

The orchestrator at `scripts/generate_manifest.py:110-244` runs the following phases in order:

| Phase | What it does | File:line | Output |
|---|---|---|---|
| **1** | Individual construct plugins. For each construct × source instance, call `construct.build_plugin_json(name)` and `construct.emit(name, plugin_dir)` to write `_generated/<prefix>-<name>/`. Collects in-memory marketplace entries. | `scripts/generate_manifest.py:121-131` | `_generated/<prefix>-<name>/.claude-plugin/plugin.json` per source instance |
| **1.5** | Per-platform per-plugin manifests. For each `(plugin, platform)` pair where `type(construct) in platform.supports`, call `platform.build_plugin_json(construct, name)` and write `_generated/<plugin>/.<platform>-plugin/plugin.json`. Empty `{}` returns are skipped. Claude is skipped (already done by Phase 1). | `scripts/generate_manifest.py:133-153` | `_generated/<plugin>/.codex-plugin/plugin.json` + `.cursor-plugin/plugin.json` where supported |
| **2a** | Catalog bundles. Load `catalog.toml [bundle.*]` blocks, resolve member references, emit `_generated/bundle-<name>/` per bundle. | `scripts/generate_manifest.py:155-162` | `_generated/bundle-<name>/.claude-plugin/plugin.json` per catalog bundle |
| **2b** | **Retired 2026-05-27**. Previously emitted `bundle-<prefix>-all` per Claude-supported construct; removed because they doubled the marketplace listing without curation value. The phase header is preserved in `scripts/generate_manifest.py` for archaeology. | — | — |
| **3** | Cross-platform mirrors. Wipe all `platform.mirror_directory` roots, then for each platform call `platform.emit(construct, name)` for every supported `(construct, name)`. Includes `AgentsPlatform` populating `.agents/skills/`. | `scripts/generate_manifest.py:182-196` | `.codex/`, `.gemini/`, `.cursor/`, `.windsurf/`, `.devin/`, `.agents/` populated |
| **4** | Gemini extension manifest. Call `GeminiPlatform.emit_extension_manifest()` to write `.gemini/gemini-extension.json`. | `scripts/generate_manifest.py:198-200` | `.gemini/gemini-extension.json` |
| **4.5** | Root-level `gemini-extension.json` copy. `gemini extensions install <github-url>` clones the repo and expects the manifest at the repo root, not inside `.gemini/`. Copy the Phase-4 output to the root. | `scripts/generate_manifest.py:202-209` | `gemini-extension.json` at repo root |
| **5** | Top-level `marketplace.json`. Aggregate the in-memory marketplace entries collected during Phase 1+2 and write `.claude-plugin/marketplace.json`. Entries are sorted by `(category, name)` for deterministic diffs. Built from in-memory data so the `category` field survives even though it's not stored in individual plugin.json files. | `scripts/generate_manifest.py:211-212` | `.claude-plugin/marketplace.json` |
| **5.5** | Codex canonical marketplace path. Copy `.claude-plugin/marketplace.json` byte-identical to `.agents/plugins/marketplace.json` — the path documented at developers.openai.com/codex/plugins/build (2026-05-25). Both paths remain valid; we serve both. | `scripts/generate_manifest.py:219-226` | `.agents/plugins/marketplace.json` |
| **6** | Root-level `.cursor-plugin/marketplace.json`. Cursor team-marketplace import expects a multi-plugin manifest at the repo root listing all Cursor-supported plugins. | `scripts/generate_manifest.py:228-250` | `.cursor-plugin/marketplace.json` at repo root |

After Phase 6, the generator prints a one-line summary of category counts and per-platform manifest counts.

## The `supports` gate

One architectural rule ties everything together: **per-plugin native manifest emission is gated on `type(construct) in platform.supports`**.

The gate appears in two places:

- **Phase 1.5** at `scripts/generate_manifest.py:139-153` — emits `_generated/<plugin>/.<platform>-plugin/plugin.json` only where the gate passes
- **Phase 3** at `scripts/generate_manifest.py:188-196` — emits the mirror directory contents only for supported constructs

The consequence: a `_generated/theme-example/` directory will have `.claude-plugin/plugin.json` (Claude supports themes) but NOT `.codex-plugin/plugin.json` (Codex doesn't include `ThemeConstruct` in its `supports`). The on-disk layout encodes which platforms can host which constructs — no fiction, no per-platform manifests for things the platform can't use.

Two follow-on properties fall out for free:

- Adding a new construct type requires defining `supports` membership ONCE per platform; per-plugin manifest emission falls out automatically. No drift.
- Adding a new platform requires implementing `build_plugin_json` and declaring `supports`; the generator's Phase 1.5 picks it up with no additional wiring.

## Mirror hygiene

When `Platform.emit` copies source content into a mirror directory, it must exclude per-platform manifest directories so they don't bleed across mirrors. A single shared `shutil.ignore_patterns` constant is reused by every Platform's `emit`:

```python
# scripts/platforms.py:58-61
_COPY_IGNORE = shutil.ignore_patterns(
    "__pycache__", "*.pyc",
    ".claude-plugin", ".codex-plugin", ".cursor-plugin",
)
```

Excluded items, and why each exclusion exists:

| Pattern | Why excluded |
|---|---|
| `__pycache__`, `*.pyc` | Python byte-cache artifacts have no business in a generated mirror; they'd vary by runner and cause spurious drift. |
| `.claude-plugin` | Per-plugin Claude manifest dir. Belongs only in `_generated/<plugin>/`, not in `.codex/skills/<name>/` etc. |
| `.codex-plugin` | Per-plugin Codex manifest dir. Must not appear inside any other platform's mirror. |
| `.cursor-plugin` | Per-plugin Cursor manifest dir. Same reason. |

Phase 3 also wipes every `platform.mirror_directory` before re-emitting (`scripts/generate_manifest.py:184-186`), so stale content from earlier runs cannot survive a regeneration.

## Things worth knowing

| Behavior | Why it matters here |
|---|---|
| **Claude Code plugin dependencies auto-install.** Installing `bundle-examples` installs every dep. The install output reports `(+ N dependencies: ...)`. Uninstalling the bundle does NOT auto-remove its deps — they orphan and persist until `claude plugin prune --scope <scope> -y`. | The domain-bundle architecture is dep-only plugins with no inlined content. Auto-install is what makes multi-member bundles usable in practice. |
| **`claude plugin validate <path>` enforces kebab-case for Claude.ai marketplace sync.** Mixed-case names load locally but fail sync; the validator warns. `homepage` and `repository` fields are tolerated with an "Unknown field" warning — kept anyway for documentation. | Naming convention enforced repository-wide: hyphens throughout, no underscores. |
| **Bundle references depend at install time; no transitive flattening.** A bundle's `dependencies` field lists its members directly; installing the bundle installs the deps in one transaction. Removing a member from the bundle does not retroactively un-install it from machines that installed the bundle. | Lets bundles compose cleanly without the generator needing to compute closure or maintain a graph. |
| **The Construct Protocol is `@runtime_checkable` but concrete classes do NOT inherit from Protocol.** Structural typing works at static-check time; isinstance dispatches on concrete classes. | Means `isinstance(obj, Construct)` works for duck-typed Construct-shaped objects, while keeping the inheritance graph flat. |
| **Per-construct catch-all bundles retired 2026-05-27.** Phase 2b previously emitted `bundle-<prefix>-all` per Claude-supported construct. Removed because they doubled marketplace entries without adding curation. The reserved-name check in `load_bundles` is also gone. | The catalog can now use any name, including the old `<prefix>-all` form, without collision. |

## References

- `scripts/platforms.py:64-352` — Platform protocol + 7 Platform classes + registry
- `scripts/constructs.py:38-56` — Construct protocol; 10 Construct classes follow
- `scripts/generate_manifest.py:110-244` — `main()`, the nine-phase orchestrator
- `scripts/bundles.py` — `Bundle` dataclass + `load_bundles`
- `scripts/utils.py` — shared helpers (`scan_source_dir`, `_marketplace_*`, `write_plugin_json`)
- [[CONSTRUCT_TYPES]] — 10-construct reference table
- [[RULE_FORMAT]] — rule install workaround (`activate.sh`)
- [[SKILL_FORMAT]] — SKILL.md format spec
- [[ADDING_A_CONSTRUCT]] — primary contributor walkthrough
- [[PLATFORMS]] — per-platform install/support reference
- [[CONTRIBUTING]] — how to add things and test
- [[INVESTIGATION_PLUGIN_DEPENDENCIES]] — dependency-auto-install proof + bonus findings

---

*Last updated: 2026-05-24.*
