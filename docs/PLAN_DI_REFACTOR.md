# Plan: Dependency-Injection Refactor of the Marketplace Generator

**Status:** v3 — incorporates the 14 findings from the reviewer critique (3 BLOCKERS, 6 IMPORTANTs, 5 NICE) + user-driven structural improvements (code-generated catch-all bundles, example-directory rename, test-list categorization)
**Original draft:** session 2026-05-23
**Reviewer critique (full text of every BLOCKER/IMPORTANT/NICE):** `docs/PLAN_DI_REFACTOR_CRITIQUE.md`
**Branch:** `feat/claude-plugin-compliance`
**Estimated effort:** 10-15 hours of focused agent time (bumped from initial 6-10 per reviewer's added scope from BLOCKERS 2-3)

---

## TL;DR

Replace the current per-construct generator code with a strategy-pattern architecture:

- 10 Construct classes in `scripts/constructs.py` (each implements `build_plugin_json` + `emit`)
- 6 Platform classes in `scripts/platforms.py`
- 1 Bundle module in `scripts/bundles.py`
- 1 Utils module in `scripts/utils.py` (shared helpers like `scan_source_dir`)
- ~100-line generator main flow in `scripts/generate_manifest.py`
- Tiny `catalog.toml` containing ONLY bundle definitions

**Also:** rename all 10 example directories from `example-<construct>` to just `example` (removes redundancy now that prefixes are uniform). Update tests and compat workflows that reference old example names.

Resolves 9 of 11 quiet asymmetries. End state: every future construct or platform addition is a single typed Python class.

---

## Changes From v1 (Reviewer-Driven)

Each row's "Source" column references a specific finding in [`docs/PLAN_DI_REFACTOR_CRITIQUE.md`](./PLAN_DI_REFACTOR_CRITIQUE.md) — that file has the full text of every BLOCKER/IMPORTANT/NICE. The brief in-line description after the label here is enough to understand the change without flipping; the critique doc has empirical evidence and suggested resolutions if you need more.

| Change | Source (label — what the finding said) |
|--------|----------------------------------------|
| Construct protocol now has `build_plugin_json` + `emit` (not just `build_plugin_json`) | BLOCKER 2 — skills need `shutil.copytree` of the source tree into the plugin dir; v1 sketch only returned a dict, so generated plugins would have been empty. Plus IMPORTANT 4 — RuleConstruct's full emit (activate.sh + rules/ subdir + README copy) was missing from the sketch |
| Generated plugin layout uses `_generated/<name>/.claude-plugin/plugin.json` (not `_generated/<name>/plugin.json`) | BLOCKER 1 — Claude Code reads plugin manifests from the `.claude-plugin/` subdir; the v1 path would have made the marketplace uninstallable |
| marketplace.json built from in-memory entries during Phase 1/2, not re-read from filesystem | BLOCKER 3 — `category` field exists only in marketplace.json (not individual plugin.json), so reconstructing entries from disk would have lost it |
| `category` field tracked per construct/bundle and carried into marketplace.json | BLOCKER 3 — same root cause as above; explicit tracking ensures the field survives |
| `supports: set[type[Construct]]` typed consistently (classes, not instances) | IMPORTANT 1 — v1's `ClaudeCodePlatform.supports = set(CONSTRUCTS.values())` used instances while the protocol said classes; would have broken `isinstance(c, construct_cls)` dispatch |
| BundleMember fields renamed: `kind`→`ref_type` ("plugin"/"bundle"), `construct`→`prefix` | IMPORTANT 2 — v1's `kind` collided with "construct type" meaning, making the schema confusing |
| Tests to DELETE explicitly listed | IMPORTANT 3 — 5 tests in `TestConfigFiles` assert on the OLD catalog schema; implementing agent needed an explicit deletion list to avoid leaving stale assertions |
| RuleConstruct sketch shows full emit (activate.sh + rules/ subdir + README copy) | IMPORTANT 4 + OQ-12 — the current generator does these but v1's sketch returned only `_base_plugin_shape`, hiding the real complexity; OQ-12 nailed down the generated rule directory structure |
| New `scripts/utils.py` module added; `scan_source_dir` lives there | IMPORTANT 5 — v1 had `_scan_source_dir` in `generate_manifest.py` but called from `bundles.py` — circular import |
| Bundle validation rejects `members + members_from_construct` together | IMPORTANT 6 — v1's silent precedence ("`members_from_construct` wins") would have silently mis-catalogued. Note: moot in v3 since `members_from_construct` was later removed entirely, but the validation pattern remains |
| `test_plugin_count` computed, not hardcoded | NICE 1 — v1's hardcoded `== 81` would have failed immediately after the refactor (count changes) and on every future content addition |
| `_load_plugin_json` cached for MCP/Theme | NICE 2 — `description_for` reads plugin.json, `build_plugin_json` reads it again; harmless but wasteful — cache it |
| MCP/Theme `plugin.json` path-vs-dict: pass through path strings as-is | NICE 3 — `example-mcp/.claude-plugin/plugin.json` stores `"mcpServers": "./mcp-config.json"` (a path, not a dict); v1 sketch tried to access `["mcpServers"]` as a dict, which would have copied the literal path string instead of the server config |
| `@runtime_checkable` on Construct Protocol | NICE 4 — without it, `isinstance(c, Construct)` fails at runtime; concrete classes don't explicitly inherit from Protocol with structural subtyping |
| `_check_drift()` skeleton added | NICE 5 — v1 referenced `_check_drift()` but provided no implementation hint; the existing `check_drift()` calls `write_all()` then diffs, which the implementing agent needs to replicate |
| Examples renamed: `example-<construct>` → just `example` (resolves OQ-11) | User decision — the duplication (`skills/example-skill/`) was redundant once prefixing is uniform; new naming: `skill-example`, `rule-example`, etc. |
| Compat workflow updates IN SCOPE (mainly `compat-mcp.yml`) | OQ-11 follow-on — `compat-mcp.yml` installs `example-mcp@dgxsparklabs-marketplace` (current name); after refactor + rename it becomes `mcp-example@dgxsparklabs-marketplace`. Workflow assertions must update or CI breaks |
| **Catch-all bundles generated by code (NOT declared in catalog.toml)** | **User decision (v3)** — catch-alls have zero user-configurable content (always "every member of construct X"), so configuration files have nothing useful to encode. Generator owns the reserved namespace |
| **`members_from_construct` field removed entirely; catalog is purely declarative** | **Follows from catch-alls-in-code** — once catch-alls aren't catalog-declared, the field has no callers; removing it eliminates a phantom config option |
| **Reserved bundle names (`<prefix>-all`): catalog cannot define** | **Validation introduced to prevent collision with code-generated catch-alls** — without this, a catalog `[bundle.skill-all]` would silently collide with the generator's auto-emitted `bundle-skill-all` |
| **New High Level Test List section added** | **User request** — explicit checklist of every test that should exist after refactor, with category and one-line purpose |
| **Migration concerns relaxed: feature branch, no published users; rename freely** | **User decision** — PR #1 hasn't merged, no external users have hardcoded install commands, so internal renames don't need migration notes |

---

## Goal

Replace the asymmetric, special-cased generator codebase with a typed, polymorphic architecture where:

1. Each construct type is a Python class implementing the `Construct` protocol with `build_plugin_json` (for marketplace.json metadata) + `emit` (for filesystem output)
2. Each platform is a Python class implementing the `Platform` protocol
3. `catalog.toml` contains ONLY bundle definitions
4. Generator main flow is a tiny dispatch loop over typed registries

This collapses ~15 special-case generator functions into ~6 generic ones, eliminates ~9 quiet asymmetries documented in the architecture discussion, and makes the marketplace structurally honest: configuration files contain only configuration; behavior lives in code.

---

## Scope

### In scope

- Refactor `scripts/generate_manifest.py` into modular files:
  - `scripts/constructs.py` — 10 Construct classes
  - `scripts/platforms.py` — 6 Platform classes
  - `scripts/bundles.py` — bundle resolution from catalog
  - `scripts/utils.py` — shared helpers (`scan_source_dir`, `_load_plugin_json`, `_to_json`, `_frontmatter`, `_marketplace_*`)
  - `scripts/generate_manifest.py` — entry point (~100 lines)
- Reduce `catalog.toml` to bundle definitions only
- **Rename 10 example directories** from `example-<construct>` to `example`
- Add per-construct catch-all bundles (`bundle.skill-all`, ..., one per construct)
- Migrate existing skill and rule domain bundles to the new `[bundle.*]` schema
- Consolidate 11 `docs/ADDING_*.md` files into 1 parameterized `docs/ADDING_A_CONSTRUCT.md`
- Update `tests/test_marketplace.py` to iterate uniformly + delete 5 stale tests + add orphan-detection test
- **Update compat workflows that reference old example plugin names** (primarily `compat-mcp.yml`; audit all)
- Audit other docs/tests for hardcoded plugin names from the example rename
- Hyphenate any remaining underscored TOML keys (audit confirms minimal work)
- Update PR #1 description to reflect new architecture + example renames
- Verify CI green across all 10 compat workflows + the existing CI workflow
- Produce a refactor report (`docs/DI_REFACTOR_REPORT.md`)

### Out of scope

- Adding new construct types
- Adding new platforms (the 6 we have cover the empirical landscape)
- Modifying Claude Code's plugin spec or contracts
- Adding new real (non-example) skills/rules/etc.
- Removing the `activate.sh` symlink workaround for rules (Claude Code limitation)
- Changes to `MARKETPLACE.toml` identity fields (owner/version/license)
- Changes to compat workflow ASSERTIONS or structure (only hardcoded plugin name references update)
- Changes to Wave 4 settings (codex/gemini stay `continue-on-error: false`)
- Touching the `archive/cli-empirical-discovery` git tag

---

## Background

This refactor builds on prior planning and validation. See:

- [`PLATFORM_INSPECTION_CATALOG.md`](./PLATFORM_INSPECTION_CATALOG.md) — empirical CLI behavior per platform; canonical source for inspection commands, expected outputs, match modes
- [`PLATFORM_VALIDATION_CICD_PLAN.md`](./PLATFORM_VALIDATION_CICD_PLAN.md) — 20 locked decisions for validation CI; this refactor must not contradict any of them
- [`INVESTIGATION_PLUGIN_DEPENDENCIES.md`](./INVESTIGATION_PLUGIN_DEPENDENCIES.md) — empirical proof of recursive dep auto-install; load-bearing for [decision #5](#locked-decisions) (bundle reference semantics)
- [`RESTRUCTURE_REPORT.md`](./RESTRUCTURE_REPORT.md) — Option D examples-in-native-folders restructuring (already landed in PR #1)
- [`ORG_POLICY_INVESTIGATION.md`](./ORG_POLICY_INVESTIGATION.md) — root-cause analysis of the transient install block (May 22, 2026)
- [`EMPIRICAL_CLI_FINDINGS/`](./EMPIRICAL_CLI_FINDINGS/) — raw exploration notes per platform (codex, cursor, devin, gemini, windsurf)
- [`PLAN_DI_REFACTOR_CRITIQUE.md`](./PLAN_DI_REFACTOR_CRITIQUE.md) — the v1 reviewer critique that drove the v3 updates in this plan; cross-referenced from [Changes From v1](#changes-from-v1-reviewer-driven)

**Architectural drift the v1 plan corrected:** catalog-as-DSL trending toward `description_source = "frontmatter:SKILL.md"`. v1 inverted: behavior in code (typed Construct classes), configuration in TOML (bundle definitions only).

**Why v2:** reviewer pass (`docs/PLAN_DI_REFACTOR_CRITIQUE.md`) caught three implementation-breaking blockers and surfaced 8 additional issues. Architecture survived (sound); code sketches and edge-cases needed correction.

**Asymmetries this refactor dissolves:**

| Letter | Asymmetry | Resolution |
|--------|-----------|-----------|
| A | Examples filtered out then re-included via `gen_example_bundles()` | First-class bundle members; one code path |
| B | `gen_skill_bundles()` / `gen_rule_bundles()` as separate functions | One generic bundle generator |
| C | Skills/rules privileged in tests | Tests iterate `CONSTRUCTS.values()` uniformly |
| D | `rules-all` exists; `skills-all` doesn't | `bundle.<construct>-all` for every construct |
| E | Naming uses both `_` and `-` | Hyphens throughout |
| F | 11 near-duplicate ADDING_*.md docs | One parameterized doc + per-construct quick reference |
| G | description field placement varies | Each Construct class knows where its description lives |
| H | Mirror generation only for skills/rules | `Platform.supports` declares which constructs each platform mirrors |
| K | Plugin.json field variation per construct | Each Construct class builds its own plugin.json shape |

Asymmetries I (rules need activate.sh — Claude Code limitation) and J (compat workflows differ per construct — necessary platform asymmetry) are external constraints not fixable here.

---

## Locked Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | `catalog.toml` contains ONLY `[bundle.*]` blocks | Constructs and platforms have stable behavior, not configuration |
| 2 | Constructs defined as Python classes implementing `Construct` protocol | Polymorphism handles plugin.json variation natively |
| 3 | Platforms defined as Python classes implementing `Platform` protocol | Per-platform quirks encapsulated; `supports` declares constructs |
| 4 | Examples are first-class members of their bundles (no special-case code) | Resolves asymmetry A |
| 5 | Bundle reference semantics: depend at install time (no transitive flattening) | Empirically verified; simpler generator; preserves bundle structure |
| 6 | Bundle generated plugin name: `bundle-<name>` universally | Predictable convention |
| 7 | Bundle members syntax: `plugin-prefix:name` or `bundle:name` | Single member syntax (e.g., `skill:telegram-notify`, `bundle:communication-skills`) |
| 8 | ~~Per-construct catch-all bundles via `members_from_construct = "<prefix>"`~~ **SUPERSEDED by decisions #23–#24**: catch-alls are now code-generated (Phase 2b of the generator), NOT catalog-declared; `members_from_construct` is removed from the schema entirely | Original rationale: auto-populated uniform pattern. Superseded reasoning: catch-alls have zero user-configurable content, so config files have nothing useful to encode |
| 9 | Underscored TOML keys → hyphens | Single naming convention |
| 10 | 11 ADDING_*.md docs → 1 parameterized doc + reference table | Reduce duplication |
| 11 | Construct descriptions extracted by Construct class | Behavior in code, not config strings |
| 12 | Migration approach: single feature commit | Refactor changes everything atomically |
| 13 | Verify CI green before final push | Empirical safety net |
| 14 | Bundle descriptions optional; fallback enumerates member names | Don't block on description writing |
| **15** | **Construct protocol has TWO methods: `build_plugin_json(name)` returns dict + `emit(name, target_dir)` writes filesystem** | **Resolves BLOCKER 2: skill copytree, rule activate.sh, etc. need filesystem ops separate from dict construction** |
| **16** | **Generated plugin path: `_generated/<prefix>-<name>/.claude-plugin/plugin.json`** | **Resolves BLOCKER 1: Claude Code reads from `.claude-plugin/` subdir** |
| **17** | **`marketplace.json` aggregation: entries built in-memory during Phase 1/2; NOT re-read from filesystem** | **Resolves BLOCKER 3: `category` field survives; all required fields present** |
| **18** | **Example directories renamed from `example-<construct>` to `example`** | **Resolves OQ-11: removes redundancy now that prefixes are uniform; plugin name `skill-example` clearer than `skill-example-skill`** |
| **19** | **Compat workflows referencing old example plugin names are IN SCOPE for this refactor** | **Resolves OQ-11 follow-on: `compat-mcp.yml` references `example-mcp` → must become `mcp-example`** |
| **20** | **Bundle with both `members` and `members_from_construct` raises ValueError at load time** | **Resolves IMPORTANT 6: prevent silent mis-cataloging** |
| **21** | **Construct Protocol decorated with `@runtime_checkable`; concrete classes do NOT inherit from Protocol** | **Resolves NICE 4: structural typing works at static check time; isinstance dispatches on concrete classes** |
| **22** | **Tests to DELETE explicitly listed (see Test Redesign section)** | **Resolves IMPORTANT 3: implementing agent doesn't leave stale tests** |
| **23** | **Per-construct catch-all bundles (`bundle-<prefix>-all`) generated by code, NOT declared in catalog.toml** | **They have zero user configuration — every catch-all is "every member of construct X." Code is the right home for derivation logic.** |
| **24** | **`members_from_construct` field removed from Bundle dataclass and catalog schema** | **Was only used by catch-alls; since catch-alls are code-generated, the field is dead. Catalog becomes purely declarative.** |
| **25** | **Reserved bundle names: `<prefix>-all` for each construct prefix; `load_bundles` raises ValueError if catalog tries to define one** | **Prevents collision with auto-generated catch-alls. Provides clear error if user tries.** |

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│ Source content (humans edit)                                     │
│ skills/<name>/, rules/<name>/, commands/<name>/, ...             │
│ Examples renamed to <construct>/example/                         │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             │ scanned via Utils.scan_source_dir
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│ Construct registry (scripts/constructs.py)                       │
│ CONSTRUCTS: dict[str, Construct]                                 │
│                                                                  │
│ Skill → build_plugin_json + emit (copytree + write .claude-plugin/plugin.json) │
│ Rule  → build_plugin_json + emit (rules/<name>.md + activate.sh + .claude-plugin/plugin.json) │
│ MCP   → build_plugin_json + emit (copytree + .claude-plugin/plugin.json with mcpServers path) │
│ ... 10 total                                                     │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             │ Phase 1+2 generate plugins + collect entries
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│ Bundle resolution (scripts/bundles.py)                           │
│ catalog.toml [bundle.*] entries → resolved dependency lists      │
│ Members: "plugin-prefix:name" or "bundle:name"                   │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│ Output 1: Claude Code marketplace                                │
│ _generated/<prefix>-<name>/.claude-plugin/plugin.json (one per   │
│   construct instance) + _generated/bundle-<name>/.claude-plugin/ │
│   plugin.json (one per bundle) + .claude-plugin/marketplace.json │
│   (manifest aggregated from in-memory entries)                   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ Platform registry (scripts/platforms.py)                         │
│ PLATFORMS: dict[str, Platform]                                   │
│                                                                  │
│ ClaudeCode → no mirror (marketplace.json IS output)              │
│ Codex      → .codex/skills/                                      │
│ Gemini     → .gemini/skills/, .gemini/gemini-extension.json      │
│ Cursor     → .cursor/rules/                                      │
│ Windsurf   → .windsurf/rules/                                    │
│ Devin      → .devin/skills/, .devin/rules/                       │
└──────────────────────────────────────────────────────────────────┘
```

---

## Platform Requirements

What each target platform expects to find in our marketplace to detect and install plugins correctly, and what the generator must emit to satisfy it. For empirical findings (exact CLI commands, exit codes, error modes, edge cases), see [`PLATFORM_INSPECTION_CATALOG.md`](./PLATFORM_INSPECTION_CATALOG.md) and the raw exploration notes under [`EMPIRICAL_CLI_FINDINGS/`](./EMPIRICAL_CLI_FINDINGS/) — this table is the architectural summary that drives the Platform classes designed in the [Code Design](#code-design) section.

| Platform | What it reads | What the generator emits | Install path / detection |
|----------|---------------|--------------------------|--------------------------|
| Claude Code | `.claude-plugin/marketplace.json` (top-level manifest) + per-plugin `.claude-plugin/plugin.json` for individual + bundle plugins | Top-level `.claude-plugin/marketplace.json` (aggregated in Phase 5); `_generated/<prefix>-<name>/.claude-plugin/plugin.json` per individual plugin; `_generated/bundle-<name>/.claude-plugin/plugin.json` per bundle / catch-all | `/plugin marketplace add DgxSparkLabs/marketplace` then `/plugin install <name>@dgxsparklabs-marketplace` |
| Codex | Same `.claude-plugin/marketplace.json` we emit for Claude Code — Codex consumes our manifest directly; registration recorded in `~/.codex/config.toml` | No additional emission beyond what Claude Code needs (Codex reuses our marketplace) | `codex plugin marketplace add ./` then `codex plugin install <name>@dgxsparklabs-marketplace` |
| Gemini | `.gemini/gemini-extension.json` (extension manifest — `name` + `version` required, `description` recommended); per-skill content at `.gemini/skills/<name>/` | `.gemini/gemini-extension.json` (fields populated from `MARKETPLACE.toml`); `.gemini/skills/<name>/` mirror per skill (full source copy) | `gemini extensions install ./.gemini/` AND/OR `gemini skills install ./.gemini/skills/<name>` |
| Cursor | `.cursor/rules/<name>.md` (front-matter + body); no install command — Cursor IDE detects files on workspace open | `.cursor/rules/<name>.md` per rule (transformed from `rules/<name>/rule.md` source) | Clone repo + open in Cursor IDE (no headless install path) |
| Windsurf | `.windsurf/rules/<name>.md` (Cursor-compatible rule format); no install command | `.windsurf/rules/<name>.md` per rule (same format as Cursor) | Clone repo + open in Windsurf IDE (no headless install path) |
| Devin | Rules: `.cursor/rules/*.md` and `.windsurf/rules/*.md` (verified via `devin rules paths` — Devin reads from these directories natively; see [`EMPIRICAL_CLI_FINDINGS/devin.md`](./EMPIRICAL_CLI_FINDINGS/devin.md)). Skills: `.devin/skills/<name>/` (Devin-native skills location) | `.devin/skills/<name>/` mirror per skill (Devin reads this); rule support comes from the `.cursor/` and `.windsurf/` mirrors emitted for those platforms (no separate `.devin/rules/` emission — Devin reads the Cursor/Windsurf paths directly) | Clone repo; Devin's `devin skills list` and `devin rules list` auto-detect content at session start |

For each platform there's a corresponding Platform class in `scripts/platforms.py` (see [Code Design > Platform Protocol](#platform-protocol)) that encapsulates this knowledge. Adding a new platform = writing a new Platform class + entry in the `PLATFORMS` registry — no catalog or generator-loop changes needed.

Two platforms (Cursor, Windsurf) have no install command at all; they're file-detection-only. Three platforms (Claude Code, Codex, Gemini) have headless CLI install paths exercised in the [External E2E compat workflows](#external-e2e-compat-workflows-in-githubworkflowscompat-yml). Devin straddles: no install command per se, but `devin skills list` / `devin rules list` provide CLI-introspectable verification post-clone.

---

## Code Design

### Construct Protocol

```python
# scripts/constructs.py
from typing import Protocol, runtime_checkable
from pathlib import Path

@runtime_checkable
class Construct(Protocol):
    """A Claude Code plugin construct type (skill, rule, command, ...)."""
    prefix: str                  # e.g., "skill"
    source_directory: Path       # e.g., Path("skills/")
    category: str                # marketplace.json category tag (often == prefix)

    def build_plugin_json(self, name: str) -> dict:
        """Build the plugin.json content (for marketplace.json aggregation).
        Pure function — no I/O."""
        ...

    def emit(self, name: str, target_dir: Path) -> None:
        """Write the FULL plugin to target_dir: copy source content,
        generate construct-specific artifacts (e.g., activate.sh for rules),
        and write .claude-plugin/plugin.json. Does ALL I/O for this construct
        instance."""
        ...
```

### Helper Functions (in scripts/utils.py)

```python
# scripts/utils.py
import json
import shutil
from pathlib import Path
from functools import cache

GENERATED = Path("_generated/")
MARKETPLACE_JSON = Path(".claude-plugin/marketplace.json")
CATALOG = Path("catalog.toml")


def scan_source_dir(source_dir: Path) -> list[str]:
    """List instance names in a source directory."""
    if not source_dir.exists():
        return []
    return sorted(d.name for d in source_dir.iterdir() if d.is_dir())


@cache
def _load_plugin_json(path: Path) -> dict:
    """Cached read of a plugin.json file."""
    return json.loads(path.read_text())


def _frontmatter(path: Path) -> dict:
    """Parse YAML frontmatter from a markdown file."""
    text = path.read_text()
    # Standard YAML frontmatter parser
    ...


def _to_json(obj: dict) -> str:
    """Pretty-print JSON with consistent formatting."""
    return json.dumps(obj, indent=2) + "\n"


def _marketplace_version() -> str:
    """Read version from MARKETPLACE.toml."""
    ...


def _marketplace_author() -> dict:
    """Build author dict from MARKETPLACE.toml."""
    ...


def _marketplace_name() -> str:
    """Read marketplace name from MARKETPLACE.toml."""
    ...


def _marketplace_description() -> str:
    """Read marketplace description from MARKETPLACE.toml.
    Used by GeminiPlatform.emit_extension_manifest() for the
    .gemini/gemini-extension.json file."""
    ...


def write_plugin_json(target_dir: Path, plugin_json: dict) -> None:
    """Write plugin.json under target_dir/.claude-plugin/plugin.json.
    Creates the .claude-plugin/ subdir if missing."""
    plugin_subdir = target_dir / ".claude-plugin"
    plugin_subdir.mkdir(parents=True, exist_ok=True)
    (plugin_subdir / "plugin.json").write_text(_to_json(plugin_json))
```

### Sample Construct Implementations

```python
# scripts/constructs.py (continued)

from utils import (
    _frontmatter, _load_plugin_json, _marketplace_version,
    _marketplace_author, write_plugin_json,
)

def _base_plugin_shape(construct: Construct, name: str) -> dict:
    """Common plugin.json fields shared by all constructs."""
    return {
        "name": f"{construct.prefix}-{name}",
        "version": _marketplace_version(),
        "author": _marketplace_author(),
    }


class SkillConstruct:
    prefix = "skill"
    source_directory = Path("skills/")
    category = "skill"

    def build_plugin_json(self, name):
        base = _base_plugin_shape(self, name)
        base["description"] = _frontmatter(
            self.source_directory / name / "SKILL.md"
        )["description"]
        base["skills"] = ["./"]  # Claude Code skill plugins reference content at plugin root
        return base

    def emit(self, name, target_dir):
        # Skills copy the entire source tree (SKILL.md, scripts/, references/, etc.)
        shutil.copytree(self.source_directory / name, target_dir, dirs_exist_ok=True)
        # Then place plugin.json under .claude-plugin/
        write_plugin_json(target_dir, self.build_plugin_json(name))


ACTIVATE_SH_TEMPLATE = """#!/usr/bin/env bash
set -euo pipefail
# Symlink (or copy on Windows) {name}.md into ~/.claude/rules/
# ... existing template body ...
"""

class RuleConstruct:
    prefix = "rule"
    source_directory = Path("rules/")
    category = "rule"

    def build_plugin_json(self, name):
        base = _base_plugin_shape(self, name)
        base["description"] = (
            f"Always-on rule: {name}. Install, then run activate.sh to symlink "
            f"the rule into ~/.claude/rules/"
        )
        base["keywords"] = ["rule", name]
        return base

    def emit(self, name, target_dir):
        # Rules: copy rule.md into rules/<name>.md subdir (not the plugin root)
        rules_subdir = target_dir / "rules"
        rules_subdir.mkdir(parents=True, exist_ok=True)
        shutil.copy(self.source_directory / name / "rule.md", rules_subdir / f"{name}.md")

        # Copy README.md if present
        readme = self.source_directory / name / "README.md"
        if readme.exists():
            shutil.copy(readme, target_dir / "README.md")

        # Generate activate.sh from template
        activate_path = target_dir / "activate.sh"
        activate_path.write_text(ACTIVATE_SH_TEMPLATE.format(name=name))
        activate_path.chmod(0o755)

        # Write plugin.json under .claude-plugin/
        write_plugin_json(target_dir, self.build_plugin_json(name))


class MCPConstruct:
    prefix = "mcp"
    source_directory = Path("mcp-servers/")
    category = "mcp"

    def build_plugin_json(self, name):
        base = _base_plugin_shape(self, name)
        # Read description and mcpServers from the source .claude-plugin/plugin.json
        source_plugin_json = _load_plugin_json(
            self.source_directory / name / ".claude-plugin" / "plugin.json"
        )
        base["description"] = source_plugin_json["description"]
        # mcpServers may be a path string (e.g., "./mcp-config.json") or an inline dict;
        # pass through whatever the source has — Claude Code spec accepts both
        base["mcpServers"] = source_plugin_json["mcpServers"]
        return base

    def emit(self, name, target_dir):
        # Copy entire source tree (includes mcp-config.json, scripts, etc.)
        shutil.copytree(self.source_directory / name, target_dir, dirs_exist_ok=True)
        # Overwrite the .claude-plugin/plugin.json with our computed version
        # (in case generated name differs from source plugin.json's name field)
        write_plugin_json(target_dir, self.build_plugin_json(name))


class ThemeConstruct:
    prefix = "theme"
    source_directory = Path("themes/")
    category = "theme"

    def build_plugin_json(self, name):
        base = _base_plugin_shape(self, name)
        source_plugin_json = _load_plugin_json(
            self.source_directory / name / ".claude-plugin" / "plugin.json"
        )
        base["description"] = source_plugin_json["description"]
        # experimental.themes path string passes through
        base.setdefault("experimental", {})["themes"] = (
            source_plugin_json["experimental"]["themes"]
        )
        return base

    def emit(self, name, target_dir):
        shutil.copytree(self.source_directory / name, target_dir, dirs_exist_ok=True)
        write_plugin_json(target_dir, self.build_plugin_json(name))


# ... 6 more Construct classes for command, agent, hook, lsp, monitor, output-style
# Each follows the same pattern: build_plugin_json reads source plugin.json (or frontmatter
# for command/agent/output-style) and includes construct-specific fields; emit does
# copytree + write_plugin_json.


# Registry — single source of truth, code-defined
CONSTRUCTS: dict[str, Construct] = {
    "skill":         SkillConstruct(),
    "rule":          RuleConstruct(),
    "command":       CommandConstruct(),
    "agent":         AgentConstruct(),
    "hook":          HookConstruct(),
    "mcp":           MCPConstruct(),
    "lsp":           LSPConstruct(),
    "monitor":       MonitorConstruct(),
    "output-style":  OutputStyleConstruct(),
    "theme":         ThemeConstruct(),
}
```

### Platform Protocol

```python
# scripts/platforms.py
from typing import Protocol
from pathlib import Path
from constructs import Construct, SkillConstruct, RuleConstruct, MCPConstruct, ...

class Platform(Protocol):
    """An AI coding platform we generate config/mirror outputs for."""
    name: str                                    # e.g., "codex"
    mirror_directory: Path | None                # None for ClaudeCode
    supports: set[type[Construct]]               # CLASSES of supported constructs

    def emit(self, construct: Construct, name: str) -> None:
        """Emit the mirror for this construct instance under mirror_directory."""
        ...
```

### Sample Platform Implementations

```python
class ClaudeCodePlatform:
    """Canonical platform — no separate mirror."""
    name = "claude-code"
    mirror_directory = None
    supports = {SkillConstruct, RuleConstruct, CommandConstruct, AgentConstruct,
                HookConstruct, MCPConstruct, LSPConstruct, MonitorConstruct,
                OutputStyleConstruct, ThemeConstruct}

    def emit(self, construct, name):
        pass  # no-op; .claude-plugin/marketplace.json is written by main flow


class CodexPlatform:
    name = "codex"
    mirror_directory = Path(".codex/")
    supports = {SkillConstruct}

    def emit(self, construct, name):
        dst = self.mirror_directory / "skills" / name
        shutil.copytree(construct.source_directory / name, dst, dirs_exist_ok=True)


class GeminiPlatform:
    name = "gemini"
    mirror_directory = Path(".gemini/")
    supports = {SkillConstruct}

    def emit(self, construct, name):
        dst = self.mirror_directory / "skills" / name
        shutil.copytree(construct.source_directory / name, dst, dirs_exist_ok=True)

    def emit_extension_manifest(self):
        """Single repo-level file; called separately by generator main."""
        manifest = {
            "name": _marketplace_name(),
            "version": _marketplace_version(),
            "description": _marketplace_description(),
        }
        (self.mirror_directory / "gemini-extension.json").write_text(_to_json(manifest))


# ... CursorPlatform, WindsurfPlatform, DevinPlatform follow similar patterns


PLATFORMS: dict[str, Platform] = {
    "claude-code":  ClaudeCodePlatform(),
    "codex":        CodexPlatform(),
    "gemini":       GeminiPlatform(),
    "cursor":       CursorPlatform(),
    "windsurf":     WindsurfPlatform(),
    "devin":        DevinPlatform(),
}
```

### Bundle Schema

```python
# scripts/bundles.py
from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True)
class BundleMember:
    ref_type: Literal["plugin", "bundle"]   # what kind of thing is being referenced
    prefix: str | None                        # construct prefix if ref_type=="plugin", else None
    name: str                                 # plugin instance name OR bundle name

    @classmethod
    def from_str(cls, s: str) -> "BundleMember":
        """Parse 'skill:telegram-notify' or 'bundle:communication-skills'."""
        left, right = s.split(":", 1)
        if left == "bundle":
            return cls(ref_type="bundle", prefix=None, name=right)
        return cls(ref_type="plugin", prefix=left, name=right)


@dataclass(frozen=True)
class Bundle:
    name: str
    description: str | None
    members: list[BundleMember]

    @property
    def category(self) -> str:
        """marketplace.json category for bundle plugins."""
        return "bundle"

    def generated_plugin_name(self) -> str:
        return f"bundle-{self.name}"

    def resolve_dependencies(self, constructs: dict[str, Construct]) -> list[str]:
        """Returns list of plugin names this bundle's plugin.json depends on."""
        return [
            f"{m.prefix}-{m.name}" if m.ref_type == "plugin"
            else f"bundle-{m.name}"
            for m in self.members
        ]


def _reserved_bundle_names(constructs: dict[str, Construct]) -> set[str]:
    """Names the generator owns and refuses to let catalog define."""
    return {f"{c.prefix}-all" for c in constructs.values()}


def load_bundles(catalog_path: Path, constructs: dict[str, Construct]) -> list[Bundle]:
    """Parse catalog.toml [bundle.*] blocks. Validates schema.

    Raises ValueError if a bundle's name collides with a reserved
    (code-generated catch-all) name, or if bundle has an unknown field.
    """
    import tomllib
    data = tomllib.loads(catalog_path.read_text())
    reserved = _reserved_bundle_names(constructs)
    bundles = []
    for name, spec in data.get("bundle", {}).items():
        # Decision #25: reject names that collide with auto-generated catch-alls
        if name in reserved:
            raise ValueError(
                f"Bundle '{name}' uses a reserved name (auto-generated catch-all). "
                f"Catalog cannot define '<construct>-all' bundles; they are emitted "
                f"by the generator directly. Reserved names: {sorted(reserved)}"
            )

        members_raw = spec.get("members", [])
        if not members_raw:
            raise ValueError(
                f"Bundle '{name}': must specify 'members' (a list of plugin or bundle "
                f"references like 'skill:foo' or 'bundle:bar')."
            )

        members = [BundleMember.from_str(m) for m in members_raw]
        bundles.append(Bundle(
            name=name,
            description=spec.get("description"),
            members=members,
        ))
    return bundles


def build_bundle_plugin_json(bundle: Bundle, deps: list[str]) -> dict:
    """Build the plugin.json content for a bundle (dep-only plugin)."""
    description = bundle.description or _auto_description(deps)
    return {
        "name": bundle.generated_plugin_name(),
        "version": _marketplace_version(),
        "description": description,
        "author": _marketplace_author(),
        "dependencies": deps,
    }


def _auto_description(deps: list[str]) -> str:
    """Fallback description when bundle has none in catalog."""
    if len(deps) <= 3:
        return f"Bundle containing: {', '.join(deps)}"
    return f"Bundle containing {len(deps)} items: {', '.join(deps[:3])}, ..."
```

---

## Catalog Schema (After)

```toml
# catalog.toml — bundle definitions ONLY

# ─── Skill domain bundles (migrated from [skill_domain.*]) ───────

[bundle.communication-skills]
description = "Messaging and notification skills"
members = ["skill:telegram-notify", "skill:slack-post", "skill:discord-webhook"]

[bundle.development-skills]
description = "Development tooling and analysis skills"
members = ["skill:blast-radius", "skill:code-health-audit", "skill:act-runner"]

# ... 6 more migrated skill domain bundles

# ─── Rule domain bundles (migrated from [rule_domain.*]) ─────────

[bundle.trust-rules]
description = "Trust and verification rules"
members = ["rule:no-ai-credit", "rule:verify-before-claim"]

# ... 4 more migrated rule domain bundles

# ─── Per-construct catch-all bundles are NOT declared here ───────
#
# Decision #23: bundle-<prefix>-all (skill-all, rule-all, ..., theme-all)
# is generated by the code (Phase 2b of generate_manifest.py), not
# declared in catalog.toml. They have no user-configurable content —
# every catch-all is "every member of that construct" — so configuration
# files have nothing useful to contribute. The generator owns the 10
# reserved names and emits the bundles directly.
#
# To install all skills: `/plugin install bundle-skill-all@dgxsparklabs-marketplace`
# To install all rules:  `/plugin install bundle-rule-all@dgxsparklabs-marketplace`
# (and so on for all 10 construct prefixes)
#
# Decision #25: load_bundles raises ValueError if catalog tries to
# define a reserved name (e.g., [bundle.skill-all] in catalog.toml fails).

# ─── Cross-construct examples bundle ─────────────────────────────

[bundle.examples]
description = "Reference examples — install to study every construct type"
members = [
  "skill:example",         "rule:example",
  "command:example",       "agent:example",
  "hook:example",          "mcp:example",
  "lsp:example",           "monitor:example",
  "output-style:example",  "theme:example",
]

# Note: example directory names changed from 'example-<construct>' to 'example'
# during this refactor (decision #18). Plugin names: skill-example, rule-example, etc.
```

---

## Source Structure (Updated For Example Rename)

```
skills/<name>/                    — real skill content + skills/example/
rules/<name>/                     — real rule content + rules/example/
commands/<name>/                  — commands/example/ (only example today)
agents/<name>/                    — agents/example/
hooks/<name>/                     — hooks/example/
mcp-servers/<name>/               — mcp-servers/example/
lsp-servers/<name>/               — lsp-servers/example/
monitors/<name>/                  — monitors/example/
output-styles/<name>/             — output-styles/example/
themes/<name>/                    — themes/example/
```

**Renaming step is part of the refactor's first phase** — see Migration Path.

---

## Generator Algorithm

```python
# scripts/generate_manifest.py — entry point, ≤100 lines

import sys
import json
from pathlib import Path
from constructs import CONSTRUCTS
from platforms import PLATFORMS, ClaudeCodePlatform, GeminiPlatform
from bundles import load_bundles, build_bundle_plugin_json, _auto_description
from utils import (
    GENERATED, MARKETPLACE_JSON, CATALOG, scan_source_dir, _to_json,
    _marketplace_name, _marketplace_author, _marketplace_version,
    _marketplace_description, write_plugin_json,
)


def _make_marketplace_entry(plugin_json: dict, plugin_dir: Path, category: str) -> dict:
    """Build a marketplace.json entry from an in-memory plugin.json dict."""
    return {
        "name": plugin_json["name"],
        "source": f"./{plugin_dir}",
        "description": plugin_json["description"],
        "version": plugin_json["version"],
        "author": plugin_json["author"],
        "category": category,
    }


def _write_marketplace_json(entries: list[dict]) -> None:
    """Write the top-level marketplace.json from in-memory entries.
    Sorted by category, then name (matches current behavior)."""
    entries.sort(key=lambda e: (e["category"], e["name"]))
    manifest = {
        "name": _marketplace_name(),
        "owner": _marketplace_author(),
        "plugins": entries,
    }
    MARKETPLACE_JSON.write_text(_to_json(manifest))


def _emit_bundle_plugin(
    name: str, description: str, deps: list[str], category: str = "bundle"
) -> dict:
    """Write a single bundle plugin under _generated/bundle-<name>/.
    Returns the marketplace.json entry for aggregation.

    Note: takes name+description+deps directly (not a Bundle object) so it
    can be shared by Phase 2a (catalog bundles) and Phase 2b (code-generated
    catch-alls — which have no Bundle object). Phase 2a callers should
    resolve the description fallback via `bundle.description or _auto_description(deps)`
    before passing here."""
    plugin_name = f"bundle-{name}"
    plugin_json = {
        "name": plugin_name,
        "version": _marketplace_version(),
        "description": description,
        "author": _marketplace_author(),
        "dependencies": deps,
    }
    plugin_dir = GENERATED / plugin_name
    plugin_dir.mkdir(parents=True, exist_ok=True)
    write_plugin_json(plugin_dir, plugin_json)
    return _make_marketplace_entry(plugin_json, plugin_dir, category)


def main():
    marketplace_entries: list[dict] = []

    # Phase 1: Individual construct plugins
    for construct in CONSTRUCTS.values():
        for name in scan_source_dir(construct.source_directory):
            plugin_json = construct.build_plugin_json(name)
            plugin_dir = GENERATED / f"{construct.prefix}-{name}"
            plugin_dir.mkdir(parents=True, exist_ok=True)
            construct.emit(name, plugin_dir)
            marketplace_entries.append(
                _make_marketplace_entry(plugin_json, plugin_dir, construct.category)
            )

    # Phase 2a: User-declared bundle plugins (from catalog.toml)
    bundles = load_bundles(CATALOG, CONSTRUCTS)
    for bundle in bundles:
        deps = bundle.resolve_dependencies(CONSTRUCTS)
        description = bundle.description or _auto_description(deps)
        marketplace_entries.append(
            _emit_bundle_plugin(bundle.name, description, deps)
        )

    # Phase 2b: Code-generated catch-all bundles (decision #23)
    #   For each construct, emit `bundle-<prefix>-all` whose deps are every
    #   instance of that construct. Skip if a construct has no source instances.
    for construct in CONSTRUCTS.values():
        deps = [
            f"{construct.prefix}-{n}"
            for n in scan_source_dir(construct.source_directory)
        ]
        if not deps:
            continue
        marketplace_entries.append(
            _emit_bundle_plugin(
                name=f"{construct.prefix}-all",
                description=f"Every {construct.prefix} in the marketplace",
                deps=deps,
            )
        )

    # Phase 3: Cross-platform mirrors
    for platform in PLATFORMS.values():
        if platform.mirror_directory is None:
            continue
        for construct_cls in platform.supports:
            construct = next(c for c in CONSTRUCTS.values() if isinstance(c, construct_cls))
            for name in scan_source_dir(construct.source_directory):
                platform.emit(construct, name)

    # Phase 4: Platform-specific repo-level emissions
    PLATFORMS["gemini"].emit_extension_manifest()

    # Phase 5: Top-level marketplace.json (from collected entries)
    _write_marketplace_json(marketplace_entries)


def _check_drift():
    """Snapshot _generated/ + mirrors + marketplace.json, regenerate, diff.
    Exit 0 if identical; exit 1 if drift detected."""
    import tempfile, subprocess
    # Snapshot current state to a temp dir
    # Run main()
    # Diff the snapshot against new state
    # Report any drift
    # (Mirrors current check_drift() in generate_manifest.py)
    ...


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(_check_drift())
    main()
```

---

## Test Redesign

### Tests to DELETE

The following tests in the current `tests/test_marketplace.py` assert on the OLD catalog schema and MUST be removed:

1. `TestConfigFiles.test_catalog_toml_parses` (asserts `"construct" in cat` and `"skill_domain" in cat`)
2. `TestConfigFiles.test_catalog_has_all_ten_construct_types` (asserts on `[construct.*]`)
3. `TestConfigFiles.test_catalog_has_examples_domain_for_each_construct` (iterates `[construct.*]`)
4. `TestConfigFiles.test_examples_domain_members_exist_in_source_dirs` (iterates `[<>_domain.examples]`)
5. `TestConfigFiles.test_every_skill_in_one_domain` (iterates `[skill_domain.*]`)
6. `TestConfigFiles.test_every_rule_in_one_domain` (iterates `[rule_domain.*]`)

### Tests to ADD

```python
class TestSourceLayout(unittest.TestCase):
    def test_construct_source_dirs_exist(self):
        for construct_id, construct in CONSTRUCTS.items():
            with self.subTest(construct=construct_id):
                self.assertTrue(construct.source_directory.exists())

    def test_examples_present_per_construct(self):
        # Each construct's source dir contains an 'example' subdir
        for construct_id, construct in CONSTRUCTS.items():
            with self.subTest(construct=construct_id):
                self.assertTrue((construct.source_directory / "example").exists())

    def test_instance_names_kebab_case(self):
        # Generic check applied to every construct's source instances —
        # replaces the per-construct test_skill_names_kebab_case + test_rule_names_kebab_case
        import re
        kebab = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
        for construct_id, construct in CONSTRUCTS.items():
            for name in scan_source_dir(construct.source_directory):
                with self.subTest(construct=construct_id, name=name):
                    self.assertRegex(name, kebab,
                                     f"{construct_id}/{name}: not kebab-case; derived plugin name would be invalid")


class TestGeneratedPlugins(unittest.TestCase):
    def test_all_plugins_at_correct_path(self):
        # Single uniform check: iterate marketplace.json's plugins array
        # and verify each entry's source resolves to a real .claude-plugin/plugin.json.
        # Replaces the separate individual + bundle path-check tests.
        manifest = json.loads(MARKETPLACE_JSON.read_text())
        for entry in manifest["plugins"]:
            plugin_path = Path(entry["source"]) / ".claude-plugin" / "plugin.json"
            with self.subTest(plugin=entry["name"]):
                self.assertTrue(plugin_path.exists(),
                                f"{entry['name']}: source {entry['source']} has no .claude-plugin/plugin.json")

    def test_all_plugins_parse_and_have_required_fields(self):
        # Single uniform check: every plugin.json parses + has common required fields;
        # bundles additionally have `dependencies`. Replaces individual + bundle field-check tests.
        manifest = json.loads(MARKETPLACE_JSON.read_text())
        common_required = {"name", "description", "version", "author"}
        for entry in manifest["plugins"]:
            plugin_path = Path(entry["source"]) / ".claude-plugin" / "plugin.json"
            with self.subTest(plugin=entry["name"]):
                data = json.loads(plugin_path.read_text())
                self.assertTrue(common_required.issubset(data.keys()),
                                f"{entry['name']}: missing common fields {common_required - data.keys()}")
                if entry["category"] == "bundle":
                    self.assertIn("dependencies", data,
                                  f"{entry['name']}: bundle missing 'dependencies' field")

    def test_bundle_dependencies_resolve_to_real_plugins(self):
        # Note: load_bundles signature requires (catalog_path, constructs) per decision #25
        for bundle in load_bundles(CATALOG, CONSTRUCTS):
            deps = bundle.resolve_dependencies(CONSTRUCTS)
            for dep_name in deps:
                with self.subTest(bundle=bundle.name, dep=dep_name):
                    self.assertTrue(Path(f"_generated/{dep_name}/.claude-plugin/plugin.json").exists())

    def test_individual_plugin_name_matches_prefix_and_source(self):
        for construct in CONSTRUCTS.values():
            for name in scan_source_dir(construct.source_directory):
                plugin_path = Path(f"_generated/{construct.prefix}-{name}/.claude-plugin/plugin.json")
                with self.subTest(plugin=plugin_path):
                    data = json.loads(plugin_path.read_text())
                    self.assertEqual(data["name"], f"{construct.prefix}-{name}")


class TestNoOrphanedConstructs(unittest.TestCase):
    """Sanity smoke test that every construct instance appears in at least
    one bundle — catalog OR code-generated catch-all. Per the user's "loose"
    semantic choice: catch-alls always include every instance by design, so
    this test is technically always-pass after a correct generator run. Its
    value is as a wiring check: it fails fast if CONSTRUCTS, scan_source_dir,
    catch-all emission, or marketplace.json aggregation are mis-configured.
    For catching catalog-maintenance lapses (someone adds a skill but
    forgets to add it to any domain bundle), see test_marketplace_lists_all_expected_plugins."""
    def test_every_construct_in_at_least_one_bundle(self):
        all_bundle_deps: set[str] = set()
        # Catalog bundles
        for bundle in load_bundles(CATALOG, CONSTRUCTS):
            all_bundle_deps.update(bundle.resolve_dependencies(CONSTRUCTS))
        # Code-generated catch-alls (decision #23)
        for construct in CONSTRUCTS.values():
            all_bundle_deps.update(
                f"{construct.prefix}-{n}" for n in scan_source_dir(construct.source_directory)
            )
        # Every instance must be in the union
        for construct in CONSTRUCTS.values():
            for name in scan_source_dir(construct.source_directory):
                plugin_name = f"{construct.prefix}-{name}"
                with self.subTest(plugin=plugin_name):
                    self.assertIn(plugin_name, all_bundle_deps,
                                  f"{plugin_name} is not in any bundle (catalog or catch-all)")


class TestBundleValidation(unittest.TestCase):
    def test_bundle_cannot_use_reserved_catchall_name(self):
        # Validates decision #25: catalog cannot define bundle-<prefix>-all names
        import tempfile
        bad_catalog = """
[bundle.skill-all]
members = ["skill:foo"]
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
            f.write(bad_catalog)
            f.flush()
            with self.assertRaises(ValueError):
                load_bundles(Path(f.name), CONSTRUCTS)

    def test_bundle_requires_members(self):
        # Validates that a bundle entry without 'members' is rejected
        import tempfile
        bad_catalog = """
[bundle.empty]
description = "no members listed"
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
            f.write(bad_catalog)
            f.flush()
            with self.assertRaises(ValueError):
                load_bundles(Path(f.name), CONSTRUCTS)


class TestConstructRegistry(unittest.TestCase):
    """Validates CONSTRUCTS registry invariants — pure unit tests on
    the dict in scripts/constructs.py, no filesystem dependency."""
    def test_all_prefixes_unique(self):
        # Coverage gap 1: prevents two construct classes from colliding on
        # the prefix (which would produce duplicate plugin names like skill-foo).
        prefixes = [c.prefix for c in CONSTRUCTS.values()]
        self.assertEqual(len(prefixes), len(set(prefixes)),
                         f"Duplicate prefixes in CONSTRUCTS: {[p for p in prefixes if prefixes.count(p) > 1]}")

    def test_all_prefixes_kebab_case(self):
        import re
        kebab = re.compile(r"^[a-z]+(-[a-z]+)*$")
        for construct_id, construct in CONSTRUCTS.items():
            with self.subTest(construct=construct_id):
                self.assertRegex(construct.prefix, kebab,
                                 f"{construct_id}: prefix '{construct.prefix}' is not kebab-case")


class TestPlatformMirrors(unittest.TestCase):
    """Validates that each platform's mirror directory contains the
    expected files for the constructs it declares it supports.
    Coverage gap 2: replaces the previous `...` body with concrete per-platform
    layout assertions. Adding a new platform = adding a branch here."""
    def test_codex_skills_mirror(self):
        codex = PLATFORMS["codex"]
        if SkillConstruct not in codex.supports:
            self.skipTest("Codex does not declare skill support")
        skill = next(c for c in CONSTRUCTS.values() if isinstance(c, SkillConstruct))
        for name in scan_source_dir(skill.source_directory):
            with self.subTest(skill=name):
                # Codex mirror layout: .codex/skills/<name>/ with SKILL.md present
                self.assertTrue((codex.mirror_directory / "skills" / name / "SKILL.md").exists())

    def test_gemini_skills_mirror_and_extension_manifest(self):
        gemini = PLATFORMS["gemini"]
        skill = next(c for c in CONSTRUCTS.values() if isinstance(c, SkillConstruct))
        for name in scan_source_dir(skill.source_directory):
            with self.subTest(skill=name):
                self.assertTrue((gemini.mirror_directory / "skills" / name / "SKILL.md").exists())
        # Repo-level extension manifest (Phase 4 emission)
        manifest_path = gemini.mirror_directory / "gemini-extension.json"
        self.assertTrue(manifest_path.exists())
        manifest = json.loads(manifest_path.read_text())
        for required in ("name", "version", "description"):
            self.assertIn(required, manifest)

    def test_cursor_rules_mirror(self):
        cursor = PLATFORMS["cursor"]
        rule = next(c for c in CONSTRUCTS.values() if isinstance(c, RuleConstruct))
        for name in scan_source_dir(rule.source_directory):
            with self.subTest(rule=name):
                self.assertTrue((cursor.mirror_directory / "rules" / f"{name}.md").exists())

    def test_windsurf_rules_mirror(self):
        windsurf = PLATFORMS["windsurf"]
        rule = next(c for c in CONSTRUCTS.values() if isinstance(c, RuleConstruct))
        for name in scan_source_dir(rule.source_directory):
            with self.subTest(rule=name):
                self.assertTrue((windsurf.mirror_directory / "rules" / f"{name}.md").exists())

    def test_devin_skills_mirror(self):
        # Devin reads rules from .cursor/ and .windsurf/ (verified empirically per
        # docs/EMPIRICAL_CLI_FINDINGS/devin.md); we emit a Devin-native skills mirror only.
        devin = PLATFORMS["devin"]
        skill = next(c for c in CONSTRUCTS.values() if isinstance(c, SkillConstruct))
        for name in scan_source_dir(skill.source_directory):
            with self.subTest(skill=name):
                self.assertTrue((devin.mirror_directory / "skills" / name / "SKILL.md").exists())


class TestCatchAllBundles(unittest.TestCase):
    """Validates decision #23: code-generated bundle-<prefix>-all per construct."""
    def test_catchall_present_for_each_construct_with_sources(self):
        for construct in CONSTRUCTS.values():
            sources = scan_source_dir(construct.source_directory)
            catchall_path = Path(f"_generated/bundle-{construct.prefix}-all/.claude-plugin/plugin.json")
            with self.subTest(construct=construct.prefix):
                if sources:
                    self.assertTrue(catchall_path.exists(),
                                    f"Catch-all missing for {construct.prefix} (sources present)")
                else:
                    self.assertFalse(catchall_path.exists(),
                                     f"Catch-all should be skipped for {construct.prefix} (no sources)")

    def test_catchall_deps_match_all_sources(self):
        for construct in CONSTRUCTS.values():
            sources = scan_source_dir(construct.source_directory)
            if not sources:
                continue
            catchall = json.loads(
                Path(f"_generated/bundle-{construct.prefix}-all/.claude-plugin/plugin.json").read_text()
            )
            expected = {f"{construct.prefix}-{n}" for n in sources}
            with self.subTest(construct=construct.prefix):
                self.assertEqual(set(catchall["dependencies"]), expected)


class TestPluginCount(unittest.TestCase):
    """Replaces hardcoded test_plugin_count == 81."""
    def test_marketplace_count_matches_expected_formula(self):
        # Formula:
        #   = sum(individual construct instances)
        #   + len(user-declared bundles from catalog)
        #   + count of constructs that have at least one source (one catch-all each)
        manifest = json.loads(MARKETPLACE_JSON.read_text())
        individuals = sum(
            len(scan_source_dir(c.source_directory)) for c in CONSTRUCTS.values()
        )
        catalog_bundles = len(load_bundles(CATALOG, CONSTRUCTS))
        catchalls = sum(
            1 for c in CONSTRUCTS.values() if scan_source_dir(c.source_directory)
        )
        expected = individuals + catalog_bundles + catchalls
        self.assertEqual(len(manifest["plugins"]), expected)


class TestPlatformMirrors(unittest.TestCase):
    def test_platform_mirrors_present_for_supported_constructs(self):
        for platform_id, platform in PLATFORMS.items():
            if platform.mirror_directory is None:
                continue
            with self.subTest(platform=platform_id):
                self.assertTrue(platform.mirror_directory.exists())
                for construct_cls in platform.supports:
                    construct = next(
                        c for c in CONSTRUCTS.values() if isinstance(c, construct_cls)
                    )
                    for name in scan_source_dir(construct.source_directory):
                        # Each platform's mirror should contain entries for every source
                        # under each supported construct. Specific layout per platform:
                        # Codex: .codex/skills/<name>/
                        # Gemini: .gemini/skills/<name>/
                        # Cursor: .cursor/rules/<name>.md
                        # Windsurf: .windsurf/rules/<name>.md
                        # Devin: .devin/skills/<name>/ or .devin/rules/<name>.md
                        ...  # Specific assertions per platform; reviewer can verify per-platform layout assumptions


class TestNoSecrets(unittest.TestCase):
    # ... unchanged from current
    ...


class TestGeneratorDrift(unittest.TestCase):
    def test_check_succeeds(self):
        result = subprocess.run(
            [..., "uv", "run", "scripts/generate_manifest.py", "--check"],
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0)
```

---

## High Level Test List

The complete test surface in the final state. Each row: what's being verified, by what mechanism, the category (unit/contract/integration/E2E), why it matters. Implementing agent uses this as a checklist; reviewer uses it to spot coverage gaps.

### Test Categories

| Category        | Definition                                                                                                                                                                 | Speed    | Reliability                       | Examples in this project                                                                                           |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Unit**        | Pure function tests. No filesystem reads of project state, no subprocesses. Operate on fixtures or in-memory inputs.                                                       | <10ms    | Very high                         | `load_bundles` with bad fixtures; `BundleMember.from_str` parsing                                                  |
| **Contract**    | Verifies an artifact (generated file, source file, repo layout) conforms to an external schema or convention. Reads files but doesn't compose components.                  | 10-100ms | High                              | plugin.json schema; marketplace.json schema; naming conventions; gemini-extension.json shape                       |
| **Integration** | Tests multiple components working together — the generator's outputs in the context of the catalog + source tree. Asserts on state produced by running the full generator. | 100ms-1s | High (until source/catalog drift) | "every catalog bundle resolves to real plugin files"; "catch-all deps match every source"; aggregation correctness |
| **E2E**         | Invokes the full pipeline via subprocess, or invokes real external CLIs against generated outputs.                                                                         | 1-30s+   | Medium (CLI dependencies)         | `--check` drift detection; 10 compat-*.yml workflows installing plugins via `claude plugin install`                |

### Distribution

- **5 unit tests** (`load_bundles` validation + member-syntax parser + `CONSTRUCTS` registry invariants — prefix uniqueness and kebab-case)
- **10 contract tests** (plugin.json + marketplace.json + Gemini extension manifest + repo layout + naming conventions + no-secrets policy)
- **8 integration tests** (generator + catalog composition + per-platform mirrors + bundle resolution) — TestPlatformMirrors split into per-platform methods (Codex, Gemini, Cursor, Windsurf, Devin) for granularity; counted as one test class with multiple methods
- **1 E2E test in `tests/test_marketplace.py`** (drift detection via subprocess invocation of the generator)
- **10 E2E workflows externally** (`.github/workflows/compat-*.yml` — install plugins via real CLIs on each platform)

This project's test mix skews integration-heavy because the primary artifact IS a generator. Pure unit tests are minimal because there's little "library code" to test in isolation — the catalog parser and member-syntax validator are about it. The E2E surface mostly lives outside `test_marketplace.py` in the compat workflows, where we exercise the marketplace against real CLIs. Uniform iteration over the construct registry (rather than per-construct named tests like `test_skill_*` + `test_rule_*`) keeps the test count flat as content grows — adding a 27th skill or a new construct type doesn't require a new test class.

---

### Source layout tests (`TestSourceLayout`)

| Category | Test | What it verifies |
|----------|------|------------------|
| Contract | `test_construct_source_dirs_exist` | Each of the 10 source directories exists, so the generator can iterate and emit plugins for every construct |
| Contract | `test_examples_present_per_construct` | Each construct has an `example/` subdir, ensuring the contributor template referenced by `ADDING_A_CONSTRUCT.md` is always present |
| Contract | `test_instance_names_kebab_case` | Every instance name across every construct (`skills/<name>/`, `rules/<name>/`, `commands/<name>/`, ... all 10) follows kebab-case, so the derived plugin names (`<prefix>-<source_name>`) are valid |

### Generated plugin tests (`TestGeneratedPlugins`)

| Category | Test | What it verifies |
|----------|------|------------------|
| Integration | `test_all_plugins_at_correct_path` | Every plugin listed in marketplace.json — individual constructs, catalog bundles, and code-generated catch-alls alike — has its manifest at `_generated/<name>/.claude-plugin/plugin.json`. Single uniform check: iterate the marketplace.json `plugins` array, assert each entry's `source` resolves to a manifest file. Wrong path = uninstallable marketplace |
| Contract | `test_all_plugins_parse_and_have_required_fields` | Every plugin.json file (individual + bundle + catch-all) parses as valid JSON and carries the common required fields (name, description, version, author); bundle plugins additionally have `dependencies`. Single uniform iteration over marketplace.json's `plugins` array, with conditional logic only for the bundle-specific `dependencies` field |
| Integration | `test_bundle_dependencies_resolve_to_real_plugins` | Every bundle's `dependencies` resolves to a real plugin file — Claude Code installs deps recursively at install time, so any missing dep would fail the install |
| Contract | `test_individual_plugin_name_matches_prefix_and_source` | Each plugin's `name` follows the `<prefix>-<source_name>` convention (`skill-foo`, `mcp-bar`, etc.), keeping plugin identifiers predictable across the marketplace |

### Catch-all bundle tests (`TestCatchAllBundles`)

Validates the code-generated "every member of construct X" bundles (`bundle-skill-all`, `bundle-rule-all`, etc.). These bundles are emitted by the generator, NOT declared in `catalog.toml`, because their content is purely derivative — every catch-all is "every instance of one construct," which has no user-configurable choice.

| Category | Test | What it verifies |
|----------|------|------------------|
| Integration | `test_catchall_deps_match_all_sources` | Each catch-all bundle's `dependencies` equal exactly the set of every instance of that construct, honoring the "everything of this construct" semantic |
| Integration | `test_catchall_present_for_each_construct_with_sources` | `bundle-<prefix>-all` is emitted iff the construct has at least one source — present when sources exist, skipped when the construct has zero contributions (an empty bundle would have no purpose) |

### Platform mirror tests (`TestPlatformMirrors`)

| Category | Test | What it verifies |
|----------|------|------------------|
| Contract | `test_gemini_extension_manifest_exists_and_parses` | `.gemini/gemini-extension.json` is valid JSON with required fields, satisfying Gemini's extension manifest spec |
| Integration | `test_platform_mirrors_present_for_supported_constructs` | Each platform's mirror dir is populated for the constructs it declares it `supports` — each Platform class lists which Construct types it handles (e.g., Codex supports skills only, Devin supports skills + rules), so cross-platform users see content for their CLI |

### Marketplace.json tests (`TestMarketplaceJson`)

| Category | Test | What it verifies |
|----------|------|------------------|
| Contract | `test_marketplace_entries_have_required_fields` | Each marketplace.json entry has name/source/description/version/author/category — entries are built from in-memory data during Phase 1/2 (NOT re-read from filesystem), so the `category` tag survives even though it's not stored in individual plugin.json files |
| Contract | `test_marketplace_entries_sorted_by_category_then_name` | Entries are sorted by category then name, producing stable diffs between regenerations |
| Contract | `test_marketplace_json_exists_and_parses` | Top-level `.claude-plugin/marketplace.json` parses as valid JSON; Claude Code loads this file directly |
| Integration | `test_marketplace_lists_all_expected_plugins` | The marketplace.json `plugins` array contains exactly the expected set: every (construct, source) individual + every catalog bundle (Phase 2a) + every code-generated catch-all (Phase 2b). Set equality — a missing entry means an orphaned plugin in `_generated/`; an extra entry means a phantom listing |

### Orphan detection (`TestNoOrphanedConstructs`)

| Category | Test | What it verifies |
|----------|------|------------------|
| Integration | `test_every_construct_in_at_least_one_bundle` | Every individual plugin appears in at least one bundle (catalog or catch-all), preventing orphan content that exists in `_generated/` but isn't reachable via any installable group; replaces the deleted `test_every_skill_in_one_domain` |

### Bundle validation (`TestBundleValidation`)

Validates `load_bundles` rejects bad catalog entries at parse time, preventing silent mis-cataloging.

| Category | Test | What it verifies |
|----------|------|------------------|
| Unit | `test_bundle_cannot_use_reserved_catchall_name` | `load_bundles` raises `ValueError` if catalog tries to define a `<prefix>-all` name — those names are owned by the code-generated catch-all emit phase, so a catalog declaration would silently collide with the generator's own output |
| Unit | `test_bundle_member_syntax_validated` | `BundleMember.from_str` raises `ValueError` on malformed members; only `<kind>:<name>` syntax is accepted |
| Unit | `test_bundle_requires_members` | A bundle without a `members` field raises `ValueError`, preventing silent empty bundles |

### Plugin count test (`TestPluginCount`)

| Category | Test | What it verifies |
|----------|------|------------------|
| Integration | `test_marketplace_count_matches_expected_formula` | Manifest plugin count equals `individuals + catalog_bundles + catchalls` — replaces the brittle hardcoded `== 81` and self-adjusts as content changes |

### Secret scan (`TestNoSecrets`) — unchanged

| Category | Test | What it verifies |
|----------|------|------------------|
| Contract | `test_no_secrets_in_tracked_files` | No tracked file contains API key / credential patterns; enforces the "no committed secrets" repo policy |

### Drift check (`TestGeneratorDrift`)

| Category | Test | What it verifies |
|----------|------|------------------|
| E2E | `test_check_succeeds` | `scripts/generate_manifest.py --check` exits 0, detecting any committed `_generated/` content that's drifted from current sources |

### External E2E (compat workflows in `.github/workflows/compat-*.yml`)

Not part of `tests/test_marketplace.py` but part of the verification surface. They invoke real CLIs (Claude Code, Codex, Gemini, Devin) against the generated marketplace.

| Category | Workflow | What it verifies |
|----------|----------|------------------|
| E2E | `compat-agent.yml` | Agent plugins install via `claude plugin install` and the sub-agent registers in Claude Code |
| E2E | `compat-command.yml` | Command plugins install and the slash command registers in Claude Code |
| E2E | `compat-extension.yml` | Gemini extension validates, installs, and appears in `gemini extensions list` |
| E2E | `compat-hook.yml` | Hook plugin installs and `hooks.json` registers correctly in Claude Code |
| E2E | `compat-marketplace-add.yml` | `claude plugin marketplace add` and `codex plugin marketplace add` register the marketplace correctly |
| E2E | `compat-mcp.yml` | MCP plugin installs and the `mcpServers` field is registered; Devin/Codex/Gemini equivalents also verified |
| E2E | `compat-monitor.yml` | Monitor plugin installs and `experimental.monitors` registers in Claude Code |
| E2E | `compat-output-style.yml` | Output-style plugin installs and `experimental.outputStyles` registers in Claude Code |
| (none) | `compat-rule.yml` does not exist | Rules aren't installable per a Claude Code limitation; rule format is covered only by the Contract + Integration tiers |
| E2E | `compat-skill.yml` | Skill plugins install via `claude plugin install` and appear in `claude plugin list` (also tested for Devin, Codex, Gemini) |
| E2E | `compat-theme.yml` | Theme plugin installs and `experimental.themes` registers in Claude Code |

### Final Distribution Summary

| Category | Count in `test_marketplace.py` | Count externally | Total |
|----------|-------------------------------|------------------|-------|
| Unit | 5 | 0 | 5 |
| Contract | 10 | 0 | 10 |
| Integration | 8 (TestPlatformMirrors split into 5 per-platform methods) | 0 | 8 |
| E2E | 1 | 10 (compat workflows) | 11 |

24 explicit assertions in `test_marketplace.py`, ~80+ subtest-level assertions through iteration over `CONSTRUCTS.values()`, `PLATFORMS.values()`, and bundle lists. Subtest count scales with content; explicit-test count stays flat. The bulk of E2E coverage lives in CI workflows where real platform CLIs are actually invoked — the unit-test file's E2E is bounded to drift detection.

**Coverage assessment:** Each layer of the architecture has at least one test category guarding it. Unit covers the parser. Contract covers the schemas (plugin.json, marketplace.json, gemini-extension.json, naming conventions). Integration covers the generator-as-composer. E2E covers the real install path. No layer is untested.

---

## Documentation Changes

Delete 11 files: `docs/ADDING_A_SKILL.md`, `docs/ADDING_A_RULE.md`, ..., `docs/ADDING_A_THEME.md`, `docs/ADDING_A_DOMAIN_BUNDLE.md`.

Create `docs/ADDING_A_CONSTRUCT.md`:

```markdown
# Adding A New Plugin (Skill, Rule, Command, ...)

The marketplace supports 10 plugin construct types. The contribution
workflow is identical for each.

## Per-construct quick reference

| Construct     | Source folder    | Example template          | Description location  |
|---------------|------------------|---------------------------|------------------------|
| skill         | skills/          | skills/example/           | SKILL.md frontmatter   |
| rule          | rules/           | rules/example/            | (auto-generated)       |
| command       | commands/        | commands/example/         | command.md frontmatter |
| agent         | agents/          | agents/example/           | agent.md frontmatter   |
| hook          | hooks/           | hooks/example/            | hooks.json description |
| mcp           | mcp-servers/     | mcp-servers/example/      | plugin.json            |
| lsp           | lsp-servers/     | lsp-servers/example/      | plugin.json            |
| monitor       | monitors/        | monitors/example/         | plugin.json            |
| output-style  | output-styles/   | output-styles/example/    | plugin.json            |
| theme         | themes/          | themes/example/           | plugin.json            |

## Steps

1. Copy the example template:
   `cp -r <source-folder>/example/ <source-folder>/<your-name>/`
2. Edit the copied content per the construct's convention
3. Add to a bundle in catalog.toml (existing or new `[bundle.<your-domain>-<construct>]`)
4. Regenerate: `uv run scripts/generate_manifest.py`
5. Test: `uv run tests/test_marketplace.py`
6. Commit

## Adding a new bundle

(See "Bundle Schema" section of the architecture doc for full reference.)
```

Update `docs/CONSTRUCT_TYPES.md` to a concise reference table.

---

## Migration Path

Single feature commit. Sequence:

1. **Rename 10 example directories** using `git mv`:
   - `git mv skills/example-skill skills/example`
   - `git mv rules/example-rule rules/example`
   - ... 8 more
2. Write `scripts/utils.py` (helpers: `scan_source_dir`, `_load_plugin_json`, `_frontmatter`, `_marketplace_*`, `_to_json`, `write_plugin_json`)
3. Write `scripts/constructs.py` (10 Construct classes + registry)
4. Write `scripts/platforms.py` (6 Platform classes + registry)
5. Write `scripts/bundles.py` (Bundle dataclass + loader with validation)
6. Rewrite `scripts/generate_manifest.py` to use the new modules
7. Rewrite `catalog.toml`:
   - Delete all `[construct.*]` blocks
   - Delete all `[skill_domain.*]` and `[rule_domain.*]` blocks
   - Add migrated `[bundle.*]` entries (skill/rule domains → `bundle.<domain>-<construct>`)
   - Add `[bundle.examples]` cross-construct bundle
   - NOTE: Do NOT add `[bundle.<construct>-all]` entries — those are
     code-generated per decision #23. The generator's Phase 2b emits
     them automatically.
8. Rewrite `tests/test_marketplace.py`:
   - DELETE the 6 tests listed above
   - ADD the new uniform-iteration tests
9. Audit compat workflows for hardcoded example plugin names:
   - `compat-mcp.yml`: `example-mcp` → `mcp-example`
   - Other workflows: grep for any `@dgxsparklabs-marketplace` install command referencing example names; update accordingly
10. Audit other docs/scripts for hardcoded plugin names:
    - `docs/ADDING_*.md` (being replaced anyway)
    - `README.md` example install commands
    - Any catalog references using old domain names
11. Consolidate 11 `docs/ADDING_*.md` files into `docs/ADDING_A_CONSTRUCT.md`
12. Update `docs/CONSTRUCT_TYPES.md`
13. Update `docs/RESUME_HERE.md` to reflect new architecture
14. Run `uv run scripts/generate_manifest.py` to regenerate everything
15. Run `uv run tests/test_marketplace.py`; iterate until green
16. Run `uv run scripts/generate_manifest.py --check` (drift check)
17. Commit (single commit, conventional message)
18. Push
19. Watch CI; verify all 10 compat workflows + CI green
20. Update PR #1 description to reflect new architecture + example renames
21. Write `docs/DI_REFACTOR_REPORT.md`
22. Commit + push the report

---

## Validation Strategy

### Behavioral parity (with expected breaking changes documented)

| Aspect | Before refactor | After refactor | Change type |
|--------|----------------|---------------|-------------|
| Individual plugin name (real construct) | `skill-telegram-notify` | `skill-telegram-notify` | Unchanged |
| Individual plugin name (example) | `example-mcp` | `mcp-example` | **Renamed** (compat workflows updated; decisions #18+#19) |
| Bundle plugin name | `skills-communication` | `bundle-communication-skills` | **Renamed** |
| Bundle plugin name | `rules-all` | `bundle-rule-all` | **Renamed** |
| Plugin source path | `./_generated/skill-telegram-notify` | `./_generated/skill-telegram-notify` | Unchanged |
| Plugin.json location | `.claude-plugin/plugin.json` | `.claude-plugin/plugin.json` | Unchanged (decision #16 preserves existing) |
| Mirror directory contents | `.codex/skills/<name>/` | `.codex/skills/<name>/` | Unchanged |
| Compat workflow grep targets (real plugins) | `skill-telegram-notify` etc. | Same names | Unchanged |
| Compat workflow grep targets (example plugins) | `example-mcp` | `mcp-example` | **Updated in compat-*.yml** |

### Snapshot diff approach

1. Before starting: capture `jq '.plugins[].name' .claude-plugin/marketplace.json | sort > /tmp/plugins-before.txt`
2. After regenerating: capture the same to `/tmp/plugins-after.txt`
3. Diff: only the documented renames should appear

### CI verification

All 10 compat workflows + the pre-existing CI workflow MUST pass on the pushed commit. Specifically verify:
- `compat-mcp` succeeds with the new `mcp-example` install command (post-update)
- Other compat workflows succeed without modification (real construct names unchanged)
- `compat-extension` validates `.gemini/gemini-extension.json` correctly
- Drift check clean: `uv run scripts/generate_manifest.py --check`

---

## Risks

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|------------|--------|-----------|
| R1 | Bundle/example renames break user install commands documented elsewhere | High | Medium | PR description and CHANGELOG document the renames; users running old install commands hit "plugin not found" with a clear error |
| R2 | Test count changes confusingly | Low | Low | Computed test (NICE 1 fix); no hardcoded count |
| R3 | Compat workflows reference renamed plugin names | High | High (CI breaks) | Audit ALL compat workflows in step 9; explicitly update each occurrence |
| R4 | Future contributor confused by code-defined constructs vs catalog bundles | Low | Low | Doc the split in CONSTRUCT_TYPES.md and ADDING_A_CONSTRUCT.md |
| R5 | Python version requirements (Protocol, match, dataclass) | Low | Low | PEP 723 header already specifies `requires-python = ">=3.11"`; all features supported |
| R6 | A construct with no real sources is awkward edge case | Low | Low | Phase 2b's `if not deps: continue` skips catch-all emission when a construct has zero sources. A construct with only the example (e.g., commands/example/ today) is valid and produces a single-member catch-all (`bundle-command-all` with dep `command-example`) |
| R7 | Bundle description fallback is ambiguous | Low | Low | `_auto_description` enumerates first 3 members + count |
| R8 | Reviewer finds blockers we missed in v2 | Medium | High | Plan goes to second reviewer (per user decision) before implementation |
| R9 | Generator semantic drift undetected | Medium | High | Snapshot diff + drift check + CI; in-memory marketplace.json aggregation (decision #17) preserves `category` |
| R10 | Single-commit migration loses atomicity if any phase fails | Low | Medium | Each phase tests before next; commits stay local until full green |
| R11 | `_generated/` tree diff is enormous on commit | High | Low | Expected; agent should not panic at 100+ file diff |
| R12 | Example rename breaks more than just compat-mcp.yml | Medium | Medium | Step 9 audits ALL compat workflows for hardcoded names |
| R13 | `@runtime_checkable` on Protocol affects performance subtly | Very low | Very low | Acceptable cost for static-type benefits |

---

## Resolved Open Questions

Previous OQ-1 through OQ-10 from v1, plus newly identified OQ-11 and OQ-12, all resolved:

| OQ | Question | Resolution |
|----|----------|-----------|
| 1 | Plugin version source | Use `_marketplace_version()` from MARKETPLACE.toml uniformly |
| 2 | Bundle plugin version source | Same |
| 3 | Empty catch-all bundles | Valid; a bundle with one dep is fine |
| 4 | Description fallback format | `"Bundle containing: X, Y, Z"` or `"Bundle containing N items: X, Y, Z, ..."` for >3 |
| 5 | Test parallelism | No (current scale) |
| 6 | Protocol typing | `@runtime_checkable` decoration (decision #21) |
| 7 | Python version | 3.11+ (already in PEP 723 header) |
| 8 | Plugin entry points | Out of scope; future capability |
| 9 | Catalog backward compat | Hard-fail with clear error: `ValueError("OLD catalog schema detected. The DI refactor requires bundles-only catalog. See docs/PLAN_DI_REFACTOR.md")` |
| 10 | `source` field in marketplace.json | `./_generated/<prefix>-<name>` for all entries (uniform) |
| **11** | Example naming conflict | **Resolved: examples renamed `example-<construct>` → just `example`; compat workflows updated (decisions #18+#19)** |
| **12** | Generated rule structure | **Resolved: `_generated/rule-<name>/rules/<name>.md` + `_generated/rule-<name>/activate.sh` + `_generated/rule-<name>/README.md` (if source has one) + `_generated/rule-<name>/.claude-plugin/plugin.json`. Specified in `RuleConstruct.emit()` sketch.** |

---

## Success Criteria

The refactor is complete when:

- [ ] `scripts/generate_manifest.py` is ≤ 100 lines
- [ ] All construct dispatch logic lives in `scripts/constructs.py`
- [ ] All platform dispatch logic lives in `scripts/platforms.py`
- [ ] Bundle resolution lives in `scripts/bundles.py`
- [ ] Shared helpers live in `scripts/utils.py`
- [ ] `catalog.toml` contains only `[bundle.*]` blocks
- [ ] All 10 construct types defined as Python classes
- [ ] All 6 platforms defined as Python classes
- [ ] All example directories renamed from `example-<construct>` to `example`
- [ ] All existing skill/rule sources still produce installable plugins (snapshot diff)
- [ ] All 10 per-construct catch-all bundles exist as generated artifacts in `_generated/bundle-<prefix>-all/` (code-emitted per decision #23, NOT declared in catalog)
- [ ] `catalog.toml` contains NO `[bundle.<construct>-all]` entries (decisions #23+#25)
- [ ] `load_bundles` rejects catalog entries using reserved names
- [ ] All existing domain-style bundles migrated to `bundle.<domain>-<construct>` naming
- [ ] `bundle.examples` cross-construct bundle exists
- [ ] All compat workflows referencing old example names updated
- [ ] 11 ADDING docs consolidated to 1
- [ ] Stale tests deleted (the 6 listed in Test Redesign)
- [ ] New uniform-iteration tests added; ≥50 assertions
- [ ] `test_no_orphaned_constructs` ensures every instance is in at least one bundle
- [ ] Bundle validation rejects reserved catch-all names (catalog cannot define `[bundle.<prefix>-all]`; per decision #25 those names are code-owned)
- [ ] `CONSTRUCTS` registry: all 10 prefixes are unique + kebab-case (TestConstructRegistry)
- [ ] `test_plugin_count` is computed, not hardcoded
- [ ] Drift check clean
- [ ] All 10 compat workflows + CI workflow green on the pushed commit
- [ ] PR #1 description updated
- [ ] Refactor report committed (`docs/DI_REFACTOR_REPORT.md`)

---

## Estimated Effort

10-15 hours (bumped from the initial 6-10 estimate). The bump accounts for implementation surface the v1 plan had under-counted: skills/rules need source-tree copy + activate.sh generation (originally hidden in the BLOCKER 2 / IMPORTANT 4 sketches), marketplace.json needs in-memory aggregation logic (BLOCKER 3), and the test suite needs ~15 new assertions beyond the existing 40.

- Constructs + Platforms + Utils classes: 3-4 hours (10 construct classes with emit() bodies + 6 platform classes + shared helpers)
- Generator rewrite + catalog migration: 2-3 hours
- Example renames + compat workflow updates: 1 hour
- Test rewrite (delete + add + verify): 2-3 hours
- Docs consolidation: 1 hour
- Verification + CI cycles: 1-2 hours
- Report writing: 30 min

---

## What Reviewer (v2) Should Look For

The plan has been updated to address all v1 reviewer findings. The v2 reviewer's job:

1. **Verify the fixes** — does each documented "Change From v1" actually appear correctly in the body?
2. **New regressions** — did any plan edit introduce a new inconsistency?
3. **Example rename edge cases** — what's specific to the rename that could break (compat workflow audit completeness, doc references, hardcoded names elsewhere)?
4. **Test coverage gaps** — does the new test suite cover what the old one did + the new orphan check?
5. **Architectural consistency** — does the build_plugin_json / emit split hold cleanly across all 10 constructs, or are there constructs where this is awkward?
6. **Empirical correctness** — do the code sketches match what the existing generator actually does (modulo the intentional architectural change)?

Output to `docs/PLAN_DI_REFACTOR_CRITIQUE_V2.md`. Same severity categories.
