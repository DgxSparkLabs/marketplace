---
date: 2026-05-25
purpose: implementation-plan
arc: refactor/platform-feature-routing
status: ready-for-implementation
implementer-input: yes
research-source: ./RECOMMENDATION.md
decisions-locked: D-1 through D-17 (see ./RECOMMENDATION.md round 1 + round 2)
---

# Platform Feature Routing — Implementation Plan

> **Implementer note.** This plan is your primary input. Every meaningful decision is locked here or in [[RECOMMENDATION]] (D-1 … D-17). Where a code sketch appears it is labelled `# sketch` — refine on the way in. Where a line number is cited it was verified against the file at commit `0f2cba7` (branch `feat/claude-plugin-compliance`); re-verify before mass-editing if the branch has moved. The only deliverable from this plan is working code + tests + docs landing on `refactor/platform-feature-routing`. Do not commit until the user reviews; create commits per unit (see [PR strategy](#pr-strategy)).

## TL;DR

This refactor (a) retires two dead skill mirrors (`.codex/skills/`, `.devin/skills/`), (b) expands four platforms' `supports` sets to emit sub-agents / hooks / commands / MCP / rules across Cursor + Gemini + Codex + Windsurf + Agents, (c) adds a new `agents` CLI shim under `scripts/agents_cli/` (POSIX bash + Python), (d) adds Phase 5.5 to emit `.agents/plugins/marketplace.json` (Codex canonical path), and (e) bundles a docs + CHANGELOG sweep. **9 work units, ~12 existing files modified + ~22 new files created, expected test count 52 → ~70 (delta +18), expected commits 10 (one per unit + final docs/CHANGELOG).** The single hardest unit is **Unit 4 (Codex sub-agent emission with markdown→TOML converter)** — the only non-trivial format conversion in the refactor.

## Sequencing — the work order

Units are numbered in execution order. Dependencies are explicit. Units 1, 5, 7, 9 can run in parallel after Unit 0 (no shared files); Units 2-4 share `scripts/platforms.py` and must serialize.

| # | Unit | Covers | D-decisions | Blocks | Blocked by |
|---|---|---|---|---|---|
| 0 | **Retirement** of `.codex/skills/` + `.devin/skills/` mirror branches | (RETIRE rows in scope table) | D-1 | — | — |
| 1 | **AgentsPlatform** gains `RuleConstruct` (forward-looking `.agents/rules/`) | A1 | D-2, D-12 | — | — |
| 2 | **CursorPlatform** `supports` += {Agent, Command, Hook, MCP}; emit branches; Phase 6 picks up extras for free | A2, A6, A7, A8 | D-2, D-10, D-11, D-13 | Unit 7 (CLI), Unit 8 (CI) | Unit 0 |
| 3 | **GeminiPlatform** `supports` += {Agent, Hook}; emit branches | A3, A9 | D-10 | Unit 7, Unit 8 | Unit 0 |
| 4 | **CodexPlatform** `supports` += {Agent}; emit `.codex/agents/<n>.toml`; **md→TOML converter** | A4 | D-10, D-16 | Unit 7, Unit 8 | Unit 0 |
| 5 | **WindsurfPlatform** `supports` += {Hook}; emit `.windsurf/hooks.json` (merge) | A10 | D-10 | Unit 7, Unit 8 | Unit 0 |
| 6 | **Phase 5.5** — emit `.agents/plugins/marketplace.json` | A5 | D-14 | — | Unit 0 |
| 7 | **`agents` CLI shim** under `scripts/agents_cli/` + repo-root `install.sh` / `install.ps1` | A11 | D-3, D-4, D-5, D-6, D-13, D-17 | Unit 8 | Units 2-5 |
| 8 | **CI** — extend `compat-*.yml` for new emissions; add `compat-agents-cli.yml` | (CI assertion changes) | D-13, D-17 | — | Units 2-7 |
| 9 | **Docs + CHANGELOG** sweep | (Doc updates required) | D-7, D-8 | — | All |

**Parallelization green light:** Units 1, 6 are independent of Units 2-5 (different code paths inside `platforms.py` / `generate_manifest.py`). Units 2-5 all edit `scripts/platforms.py` so should land on a single feature branch in serial commits; if fan-out is desired, do Unit 1 + Unit 6 in parallel sub-agents and Units 2-5 sequentially in one sub-agent. Units 7-9 fan out after the generator stabilizes.

---

## Work units (one detailed section per numbered unit)

### Unit 0: Retirement of `.codex/skills/` and `.devin/skills/` mirror branches

**Covers**: D-1 (RETIRE both mirrors), the "Retirements" table in [[RECOMMENDATION]] round 2.
**D-decisions**: D-1, D-7 (clean break).

**Files to edit**:
- `scripts/platforms.py` lines 128-176 (`CodexPlatform`): drop the SkillConstruct branch from `emit` (lines 150-161 collapse to a no-op for SkillConstruct — the `if not isinstance(...): return` guard reverses; new emit short-circuits when only SkillConstruct support remains without a Codex skill mirror); set `mirror_directory: Path | None = None` (currently `REPO_ROOT / ".codex"` at line 147); `SkillConstruct` stays in `supports` because Phase 1.5 still emits `.codex-plugin/plugin.json` for skills via `build_plugin_json` (lines 163-176, unchanged).
- `scripts/platforms.py` lines 283-306 (`DevinPlatform`): set `mirror_directory: Path | None = None` (currently line 292); body of `emit` (lines 295-302) becomes `pass`. `supports = {SkillConstruct}` stays so we can later attach a per-plugin Devin manifest if Devin introduces one; with no mirror_directory Phase 3 skips this platform naturally (`generate_manifest.py:189`).
- `scripts/platforms.py` line 38, line 132 docstring updates: remove references to `.codex/skills/` mirror; update the docstring at lines 128-144 to describe the now manifest-only Codex role.
- `scripts/generate_manifest.py` lines 182-196 (Phase 3 wipe + emit): no functional change required — the `mirror_directory is None` guard at lines 185 + 189 already filters. Add an explanatory comment at line 184 about how Codex / Devin became `None`.
- `tests/test_marketplace.py` lines 211-227 (`test_codex_skills_mirror`): REMOVE outright OR convert to `test_codex_no_mirror_directory` (asserts `PLATFORMS["codex"].mirror_directory is None`).
- `tests/test_marketplace.py` lines 273-286 (`test_devin_skills_mirror`): REMOVE outright OR convert to `test_devin_no_mirror_directory`.
- `tests/test_marketplace.py` line 867 (`TestMirrorHygiene.MIRROR_DIRS_TO_CHECK`): drop `.codex` and `.devin` from the list (those dirs no longer exist).

**New files**: none.

**Filesystem deletions** (the implementer does NOT commit deletions by hand — they fall out of the next generator run because Phase 3 wipes `mirror_directory` roots, but with both set to `None` Phase 3 stops writing them, and the existing dirs need a manual `git rm -r .codex/ .devin/` before commit because Phase 3 only wipes what it owns):
- `.codex/` (entire tree, currently `.codex/skills/<27 dirs>`)
- `.devin/` (entire tree, currently `.devin/skills/<27 dirs>`)

**Detailed change description**:

Both retirements are minimal Python edits that make the platforms manifest-only. The key insight is that `SkillConstruct` remains in both `supports` sets because **Phase 1.5 still needs them** — Codex still emits `_generated/skill-<name>/.codex-plugin/plugin.json` (verified empirically in `logs/post-implementation-codex.log`), and we want to keep that path open for Devin if a per-plugin Devin manifest format ever lands. The retirement only removes the **mirror_directory + Phase-3 skill copy**, not the `supports` declaration.

After the source edit, run `uv run scripts/generate_manifest.py` once locally — it will produce a clean tree with no `.codex/skills/` or `.devin/skills/`. Then `git rm -r .codex/ .devin/` and commit. The drift check (`--check`) will then pass because the snapshot+regenerate sequence will produce identical contents (both empty).

**Verification**:
- Tests modified: `test_codex_skills_mirror` (drop or invert), `test_devin_skills_mirror` (drop or invert), `TestMirrorHygiene.MIRROR_DIRS_TO_CHECK` (remove `.codex`, `.devin`).
- Tests added: `test_codex_no_mirror_directory` (1 assertion), `test_devin_no_mirror_directory` (1 assertion). Net delta: 0 (drop 2, add 2).
- Pytest expected: 52 tests still pass after this unit.
- Drift check: `uv run scripts/generate_manifest.py --check` must exit 0 after regeneration + `git rm -r .codex/ .devin/`.
- Manual verification: `ls .codex/ .devin/ 2>&1` after generation should both report "No such file or directory".

**Commit message** (proposed):
```
refactor(platforms): retire .codex/skills/ and .devin/skills/ mirrors

Codex's plugin install reads _generated/<plugin>/.codex-plugin/plugin.json
directly; the repo-root .codex/skills/ mirror was consumed by nothing
(verified Q-A1 act run). Devin enumerates .agents/skills/ natively
(verified Q-B1) — .devin/skills/ was a redundant copy.

Sets CodexPlatform.mirror_directory and DevinPlatform.mirror_directory
to None; Phase 3 skips them naturally via the existing guard. Skill
support stays in both .supports sets so per-plugin manifest emission
(Phase 1.5) is unchanged for Codex.

Net: removes ~110 generated files (27 skills × 4 mirror artifacts each).

Refs: docs/research/platform-feature-routing/RECOMMENDATION.md D-1
```

---

### Unit 1: AgentsPlatform gains RuleConstruct (forward-looking `.agents/rules/`)

**Covers**: A1 — forward-looking `.agents/rules/<name>.md` emission for 22 rules.
**D-decisions**: D-2 (push for `.agents/` full adoption), D-12 (approve A1 even though zero platforms read it today).

**Files to edit**:
- `scripts/platforms.py` lines 309-339 (`AgentsPlatform`):
  - Line 325: `supports: set[type[Construct]] = {SkillConstruct, RuleConstruct}` (add `RuleConstruct`).
  - Lines 327-335: extend `emit` with a branch for RuleConstruct that copies the raw `rule.md` to `.agents/rules/<name>.md`. Note: the raw `rule.md` has no frontmatter (per `rules/example/rule.md:1-5`), no format conversion needed.
- `tests/test_marketplace.py` add a new test class `TestAgentsRulesMirror` after `TestAgentsMirror` (~line 856): assert `.agents/rules/<name>.md` exists for every rule source (22 assertions via `subTest`).
- `tests/test_marketplace.py` `TestMirrorHygiene.MIRROR_DIRS_TO_CHECK` (line 867): no change (`.agents` already in list).

**New files**: none source-side. Generator output creates `.agents/rules/<22 entries>.md`.

**Detailed change description**:

The `AgentsPlatform.emit` becomes:

```python
# sketch — scripts/platforms.py AgentsPlatform.emit
def emit(self, construct: Construct, name: str) -> None:
    if isinstance(construct, SkillConstruct):
        target = self.mirror_directory / "skills" / name
        shutil.copytree(
            construct.source_directory / name, target,
            dirs_exist_ok=True, ignore=_COPY_IGNORE,
        )
    elif isinstance(construct, RuleConstruct):
        rules_dir = self.mirror_directory / "rules"
        rules_dir.mkdir(parents=True, exist_ok=True)
        # Raw rule.md — no format conversion (per D-12: forward-looking convergence,
        # consumers may adopt their own frontmatter conventions later)
        shutil.copy(construct.source_directory / name / "rule.md",
                    rules_dir / f"{name}.md")
```

No platform reads `.agents/rules/` today (verified Q-R1, Q-R2). This is preparedness, not consumption. Cost: 22 files × ~1 KB = ~22 KB.

**Verification**:
- Tests added: `TestAgentsRulesMirror.test_rules_mirror_exists` (subTests = 22). Net test count delta: +1 class / +1 method (parametrized via subTest, still counts as one pytest method).
- Pytest expected: +1 new passing method.
- Drift check: `uv run scripts/generate_manifest.py --check` exits 0 after regeneration.
- Manual verification: `ls .agents/rules/ | wc -l` returns 22.

**Commit message** (proposed):
```
feat(agents): emit .agents/rules/<name>.md for forward-looking convergence

No platform reads .agents/rules/ as of 2026-05-25 (verified Q-R1/Q-R2),
but Cursor 2.7+ and Windsurf 2.0 are credible adopters. Emit the path
now so we're already there when one of them flips.

Cost: 22 files × ~1 KB. AgentsPlatform.supports now {Skill, Rule}.

Refs: RECOMMENDATION.md D-12 / A1
```

---

### Unit 2: CursorPlatform `supports` += {Agent, Command, Hook, MCP}; emit branches

**Covers**: A2 (Cursor sub-agents to `.cursor/agents/<n>.md`), A6 (Cursor MCP via per-plugin `.cursor-plugin/plugin.json`), A7 (Cursor hooks via per-plugin), A8 (Cursor commands via per-plugin).
**D-decisions**: D-10, D-11 (Cursor scope expansion), D-13 Option C indirectly (CLI default behaviour).

**Files to edit**:
- `scripts/platforms.py` lines 222-253 (`CursorPlatform`):
  - Line 236: `supports: set[type[Construct]] = {RuleConstruct, SkillConstruct, AgentConstruct, CommandConstruct, HookConstruct, MCPConstruct}` (add four).
  - Lines 238-249 (`emit`): extend the existing RuleConstruct branch with a new `AgentConstruct` branch that copies `agents/<name>/agents/*.md` files into `.cursor/agents/`. The other three new types (Command, Hook, MCP) need NO emit branch — they are surfaced purely through the per-plugin `.cursor-plugin/plugin.json` manifest written by Phase 1.5 (Cursor auto-discovers `commands/`, `hooks/hooks.json`, `mcp.json` inside an installed plugin). Skills branch remains absent (served from `.agents/`).
  - Lines 251-253 (`build_plugin_json`): expand to emit pointer fields per construct type per Cursor manifest schema:
    - AgentConstruct: `{"name": ..., "agents": "./agents/"}` (auto-discovered, the field is optional per cursor.com docs but explicit pointer makes intent clear)
    - CommandConstruct: `{"name": ..., "commands": "./commands/"}`
    - HookConstruct: `{"name": ..., "hooks": "./hooks/hooks.json"}`
    - MCPConstruct: `{"name": ..., "mcpServers": ...}` — reuse the loaded source MCPConstruct's `mcpServers` value (mirror the Codex pattern at `platforms.py:172-173`).
- `scripts/generate_manifest.py` lines 214-236 (Phase 6 — root `.cursor-plugin/marketplace.json`): NO code change required. The loop at line 220-225 already filters by `type(construct) in cursor_platform.supports`; growing `supports` automatically grows the cursor team-marketplace entries.
- `tests/test_marketplace.py` lines 596-714 (`TestPerPlatformManifests`): the existing `test_cursor_plugin_json_emitted_for_supported_constructs` is parameterized over `cursor.supports`, so it will start asserting agents/commands/hooks/mcp **automatically** once `supports` grows. Add a NEW class `TestCursorAgentsMirror` (~line 856 alongside TestAgentsMirror): assert `.cursor/agents/<name>.md` exists for every agent source (1 today — the example agent).
- `tests/test_marketplace.py` lines 783-799 (`test_cursor_marketplace_lists_cursor_supported_plugins`): already parameterized — picks up new constructs automatically.

**New files**: none source-side. Generator output adds `.cursor/agents/<name>.md` (1 file today), `.cursor-plugin/plugin.json` for ~28 more plugins (commands + hooks + mcp + agents per-plugin manifests).

**Detailed change description**:

Most of the work is `supports` set growth — Phase 1.5 and Phase 6 do their job automatically once the gate opens. The only emit branch needed is `AgentConstruct` because Cursor reads `.cursor/agents/<name>.md` as a workspace-level file (per `cursor.com/docs/agent/subagents`, 2026-05-25), independent of plugin install. For hooks/commands/MCP, Cursor's plugin manifest schema (per `cursor.com/docs/reference/plugins`) auto-discovers from inside an installed plugin — so just declaring `supports` and emitting the per-plugin manifest is enough.

The new `build_plugin_json` becomes a small switch:

```python
# sketch — scripts/platforms.py CursorPlatform.build_plugin_json
def build_plugin_json(self, construct: Construct, name: str) -> dict:
    base = {"name": f"{construct.prefix}-{name}"}
    if isinstance(construct, AgentConstruct):
        base["agents"] = "./agents/"
    elif isinstance(construct, CommandConstruct):
        base["commands"] = "./commands/"
    elif isinstance(construct, HookConstruct):
        base["hooks"] = "./hooks/hooks.json"
    elif isinstance(construct, MCPConstruct):
        source_pj = _load_plugin_json(
            construct.source_directory / name / ".claude-plugin" / "plugin.json"
        )
        base["mcpServers"] = source_pj["mcpServers"]
    # RuleConstruct + SkillConstruct: name-only minimal manifest (existing behavior)
    return base
```

The new `emit` AgentConstruct branch:

```python
# sketch — scripts/platforms.py CursorPlatform.emit, agent branch
elif isinstance(construct, AgentConstruct):
    agents_dir = self.mirror_directory / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    src_agents = construct.source_directory / name / "agents"
    if src_agents.exists():
        for agent_md in sorted(src_agents.glob("*.md")):
            shutil.copy(agent_md, agents_dir / agent_md.name)
```

Note the agent source layout (`agents/<plugin-name>/agents/*.md`, e.g. `agents/example/agents/notebook-reviewer.md` per `agents/example/agents/notebook-reviewer.md:1-5`) means one agent plugin can contain multiple `.md` sub-agents — copy them all.

**Verification**:
- Tests added: `TestCursorAgentsMirror.test_cursor_agents_mirror_exists` (subTest per agent, +1 method).
- Tests modified: `test_cursor_plugin_json_emitted_for_supported_constructs` (no source change — picks up new types automatically; expected to start failing then passing once emit branches land).
- Pytest expected: +1 method passing; ~28 new subTest cases under existing parameterized methods.
- Drift check: `uv run scripts/generate_manifest.py --check` exits 0.
- Manual verification: `ls .cursor/agents/`, `ls _generated/hook-example/.cursor-plugin/plugin.json`, `ls _generated/mcp-example/.cursor-plugin/plugin.json` all exist; `cat _generated/mcp-example/.cursor-plugin/plugin.json` shows `mcpServers` field.

**Commit message** (proposed):
```
feat(cursor): emit sub-agents + commands + hooks + MCP per Cursor 2.4 schema

Cursor's plugin manifest (cursor.com/docs/reference/plugins, 2026-05-25)
supports agents, commands, hooks, mcpServers fields and auto-discovers
the matching subdirs. We were under-emitting — only rules + skills had
.cursor-plugin/plugin.json.

CursorPlatform.supports gains AgentConstruct, CommandConstruct,
HookConstruct, MCPConstruct. AgentConstruct emits .cursor/agents/<n>.md
directly; the others surface through per-plugin .cursor-plugin/plugin.json
auto-discovery. Phase 6 cursor team-marketplace.json picks up the new
plugins automatically via the supports-set filter.

Refs: RECOMMENDATION.md D-10, D-11 / A2, A6, A7, A8
```

---

### Unit 3: GeminiPlatform `supports` += {Agent, Hook}; emit branches

**Covers**: A3 (Gemini sub-agents to `.gemini/agents/`), A9 (Gemini hooks to `.gemini/hooks/hooks.json`).
**D-decisions**: D-10.

**Files to edit**:
- `scripts/platforms.py` lines 179-219 (`GeminiPlatform`):
  - Line 189: `supports: set[type[Construct]] = {SkillConstruct, AgentConstruct, HookConstruct}` (add two).
  - Lines 191-198 (`emit`): extend with AgentConstruct + HookConstruct branches.
    - Agent: copy `agents/<name>/agents/*.md` → `.gemini/agents/`. Mirror the Cursor agent branch shape (Gemini's extension reference at `geminicli.com/docs/extensions/reference/` documents `Sub-agents - Agent definition files (.md) in agents/ directory`).
    - Hook: copy `hooks/<name>/hooks/hooks.json` → `.gemini/hooks/hooks.json`. **Merge semantics** for multi-hook-plugin coexistence: today there's only one hook plugin (`hooks/example/`) so direct copy works; if a second hook plugin lands, the second `emit` call would overwrite the first. Add a TODO comment in the emit branch noting this constraint, and a follow-up merge implementation when a second hook plugin appears (defer per simplicity).
  - Lines 200-203 (`build_plugin_json`): unchanged — Gemini extensions don't use per-plugin manifests, returns `{}` (per existing comment).

**New files**: none source-side. Generator output adds `.gemini/agents/<n>.md` (1) and `.gemini/hooks/hooks.json` (1).

**Detailed change description**:

Gemini's `.gemini/` directory IS the extension root (per `geminicli.com/docs/extensions/reference/` — see [[RECOMMENDATION]] footnote 3). The skills/, agents/, hooks/ subdirs are all auto-discovered relative to the extension root. This is structurally analogous to the existing `.gemini/skills/<name>/` emission — same pattern, new construct types.

Emit sketch:

```python
# sketch — scripts/platforms.py GeminiPlatform.emit
def emit(self, construct: Construct, name: str) -> None:
    if isinstance(construct, SkillConstruct):
        dst = self.mirror_directory / "skills" / name
        shutil.copytree(construct.source_directory / name, dst,
                        dirs_exist_ok=True, ignore=_COPY_IGNORE)
    elif isinstance(construct, AgentConstruct):
        agents_dir = self.mirror_directory / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        for agent_md in sorted((construct.source_directory / name / "agents").glob("*.md")):
            shutil.copy(agent_md, agents_dir / agent_md.name)
    elif isinstance(construct, HookConstruct):
        # NOTE: with multiple hook plugins, this overwrites. Add merge when 2nd plugin lands.
        hooks_dir = self.mirror_directory / "hooks"
        hooks_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(construct.source_directory / name / "hooks" / "hooks.json",
                    hooks_dir / "hooks.json")
```

**Verification**:
- Tests added: `TestGeminiAgentsMirror.test_gemini_agents_mirror_exists` (+1 method), `TestGeminiHooksMirror.test_gemini_hooks_json_exists` (+1 method). Net delta +2.
- Pytest expected: +2 new passing methods.
- Drift check: must pass.
- Manual verification: `ls .gemini/agents/`, `cat .gemini/hooks/hooks.json` show expected content.

**Commit message** (proposed):
```
feat(gemini): emit sub-agents + hooks under .gemini/ extension root

Gemini extensions ship sub-agents (agents/<n>.md) and hooks
(hooks/hooks.json) inside the extension dir per
geminicli.com/docs/extensions/reference/ (2026-05-25). Previously only
skills/ was emitted.

GeminiPlatform.supports gains AgentConstruct, HookConstruct. Single
hook plugin today — multi-plugin merge deferred until a second lands.

Refs: RECOMMENDATION.md D-10 / A3, A9
```

---

### Unit 4: CodexPlatform `supports` += {Agent}; emit `.codex/agents/<name>.toml` with md→TOML converter

**Covers**: A4 — Codex sub-agents at `.codex/agents/<name>.toml` per `developers.openai.com/codex/subagents/` (2026-05-25).
**D-decisions**: D-10, D-16 (keep YAML-md as canonical source, write TOML converter at emit time).

**Files to edit**:
- `scripts/platforms.py` lines 128-176 (`CodexPlatform`):
  - Line 148: `supports: set[type[Construct]] = {SkillConstruct, MCPConstruct, HookConstruct, AgentConstruct}` (add Agent).
  - Lines 150-161 (`emit`): **restore mirror_directory** (revert Unit 0's `None` for the AgentConstruct case) — wait, conflict resolution: Unit 0 set `mirror_directory = None` so Phase 3 skips Codex entirely. For Unit 4 we need a Codex mirror_directory back. **Resolution**: Set `mirror_directory = REPO_ROOT / ".codex"` (the original value); Unit 0 only meant to retire the **skill** branch, not the whole mirror. Update Unit 0 to NOT change `mirror_directory` — instead, Unit 0 only removes the SkillConstruct case from `emit`. The implementer should merge Unit 0 and Unit 4 mentally before editing: at end of Unit 0 the Codex platform has mirror_directory=`.codex/` with an empty emit (or just a no-op for SkillConstruct), then Unit 4 adds the AgentConstruct branch that creates `.codex/agents/<name>.toml`. **The implementer should re-read this note and apply Units 0 + 4 in a single coherent edit.** Similarly for Devin: stays mirror-less.
  - Lines 150-161: new emit body:

```python
# sketch — scripts/platforms.py CodexPlatform.emit
def emit(self, construct: Construct, name: str) -> None:
    # Skills: no longer mirrored (D-1); manifest-only via Phase 1.5
    if isinstance(construct, AgentConstruct):
        agents_dir = self.mirror_directory / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        from converters.md_to_toml import claude_agent_md_to_codex_toml
        src_agents = construct.source_directory / name / "agents"
        for agent_md in sorted(src_agents.glob("*.md")):
            toml_text = claude_agent_md_to_codex_toml(agent_md.read_text(encoding="utf-8"))
            (agents_dir / f"{agent_md.stem}.toml").write_text(toml_text, encoding="utf-8")
    # MCP, Hook: manifest-only via Phase 1.5 (no mirror content)
```

  - Lines 163-176 (`build_plugin_json`): no change required — AgentConstruct doesn't slot into a per-plugin Codex manifest (Codex sub-agents are TOML files in `.codex/agents/`, separate from plugin install).
- **New file**: `scripts/converters/__init__.py` (empty) and `scripts/converters/md_to_toml.py` containing the converter. See [Codex markdown-to-TOML converter](#codex-markdown-to-toml-converter-per-d-16) section below for the full code sketch.
- `scripts/platforms.py` line 33: add `from converters.md_to_toml import claude_agent_md_to_codex_toml` at the imports OR import inside the emit function (lazy import is cleaner because only one platform uses it).
- `tests/test_marketplace.py` add a new class `TestCodexAgentsMirror`:
  - `test_codex_agents_toml_exists` — `.codex/agents/<name>.toml` exists for every agent source.
  - `test_codex_agents_toml_valid` — parses as TOML, contains required keys `name`, `description`, `developer_instructions`.
  - `test_codex_agents_toml_roundtrip` — given a known input (the example notebook-reviewer agent), the converter produces the expected fields (assert on `name == "notebook-reviewer"`, `description` starts with `"Reviews a lab notebook..."`).
- `tests/test_marketplace.py` add a `TestMdToTomlConverter` class with unit tests for the converter (see [Codex markdown-to-TOML converter](#codex-markdown-to-toml-converter-per-d-16) below for test cases).

**New files**:
- `scripts/converters/__init__.py` — empty.
- `scripts/converters/md_to_toml.py` — the converter module (~80 LOC).

**Detailed change description**:

This is the hardest unit because it introduces the only meaningful format conversion in the refactor. Our `AgentConstruct` source format is a Claude-style markdown file with YAML frontmatter (`agents/<name>/agents/<n>.md`). Codex sub-agents are TOML files with the same semantic content but a different shape.

Source format (verified against `agents/example/agents/notebook-reviewer.md:1-5`):

```markdown
---
name: notebook-reviewer
description: Reviews a lab notebook entry as a skeptical peer reviewer...
tools: Read, Grep, Glob
---

You are a peer reviewer for laboratory notebook entries...
```

Required Codex TOML output (per `developers.openai.com/codex/subagents/`, 2026-05-25 — required fields: `name`, `description`, `developer_instructions`):

```toml
name = "notebook-reviewer"
description = "Reviews a lab notebook entry as a skeptical peer reviewer..."
developer_instructions = """
You are a peer reviewer for laboratory notebook entries...
"""
# tools array if frontmatter had a tools key
tools = ["Read", "Grep", "Glob"]
```

The converter (full sketch in [Codex markdown-to-TOML converter](#codex-markdown-to-toml-converter-per-d-16)) handles: frontmatter parse (reusing `utils._frontmatter` pattern), body extraction, comma-list parsing for `tools`, and TOML serialization with triple-quoted strings for the body. Python 3.11+ ships `tomllib` for read; for **write** we need either `tomli_w` (not in stdlib) or a hand-rolled emitter. Per existing project conventions (no third-party deps, see `scripts/utils.py:22` `import tomllib`), **hand-roll a tiny TOML writer** scoped to the keys we emit. Sketch is below.

**Verification**:
- Tests added: ~4 in `TestCodexAgentsMirror` + ~4 in `TestMdToTomlConverter`. Net delta +8.
- Pytest expected: +8 new passing methods.
- Drift check: must pass.
- Manual verification: `cat .codex/agents/notebook-reviewer.toml` shows the converted TOML; `python -c "import tomllib; tomllib.loads(open('.codex/agents/notebook-reviewer.toml').read())"` parses cleanly.

**Commit message** (proposed):
```
feat(codex): emit Codex sub-agents at .codex/agents/<n>.toml

Codex sub-agents (developers.openai.com/codex/subagents/ 2026-05-25)
live as TOML files. Our canonical source is Claude-style markdown with
YAML frontmatter (D-16); add scripts/converters/md_to_toml.py to
translate at emit time. Source format stays single-truth (D-16); Codex
gets a derived TOML view.

CodexPlatform.supports gains AgentConstruct. Converter handles required
fields (name, description, developer_instructions) plus optional tools[]
from frontmatter.

Refs: RECOMMENDATION.md D-10, D-16 / A4 / U1
```

---

### Unit 5: WindsurfPlatform `supports` += {Hook}; emit `.windsurf/hooks.json`

**Covers**: A10 — Windsurf hooks at `.windsurf/hooks.json` per `docs.windsurf.com/windsurf/cascade/hooks` (2026-05-25).
**D-decisions**: D-10.

**Files to edit**:
- `scripts/platforms.py` lines 256-280 (`WindsurfPlatform`):
  - Line 265: `supports: set[type[Construct]] = {RuleConstruct, HookConstruct}` (add Hook).
  - Lines 267-276 (`emit`): extend with HookConstruct branch — copy `hooks/<name>/hooks/hooks.json` → `.windsurf/hooks.json`. Same single-plugin-today caveat as Gemini (Unit 3); add TODO for merge semantics.
- `tests/test_marketplace.py` add `TestWindsurfHooksMirror.test_windsurf_hooks_json_exists` (+1 method).

**New files**: none source-side. Generator emits `.windsurf/hooks.json` (1).

**Detailed change description**:

Mirrors the Gemini hook approach exactly (Unit 3). Only difference: target path is `.windsurf/hooks.json` (no `hooks/` subdir — Windsurf reads `hooks.json` directly at the workspace root of `.windsurf/`, per the docs).

```python
# sketch — scripts/platforms.py WindsurfPlatform.emit
def emit(self, construct: Construct, name: str) -> None:
    if isinstance(construct, RuleConstruct):
        # existing logic (lines 268-276), unchanged
        ...
    elif isinstance(construct, HookConstruct):
        # NOTE: overwrites on multi-plugin coexistence; add merge when needed
        self.mirror_directory.mkdir(parents=True, exist_ok=True)
        shutil.copy(construct.source_directory / name / "hooks" / "hooks.json",
                    self.mirror_directory / "hooks.json")
```

**Verification**:
- Tests added: 1 method. Net delta +1.
- Pytest expected: +1 passing method.
- Drift check: must pass.
- Manual verification: `cat .windsurf/hooks.json` shows expected content.

**Commit message** (proposed):
```
feat(windsurf): emit .windsurf/hooks.json from HookConstruct

Windsurf reads .windsurf/hooks.json natively per
docs.windsurf.com/windsurf/cascade/hooks (2026-05-25). Mirror our single
hook plugin (hook-example) into the workspace-level file.

WindsurfPlatform.supports gains HookConstruct.

Refs: RECOMMENDATION.md D-10 / A10 / U9
```

---

### Unit 6: Phase 5.5 — emit `.agents/plugins/marketplace.json` (Codex canonical)

**Covers**: A5 — Codex canonical marketplace at `.agents/plugins/marketplace.json`.
**D-decisions**: D-14.

**Files to edit**:
- `scripts/generate_manifest.py` after line 212 (after Phase 5 closes by writing `.claude-plugin/marketplace.json`), insert Phase 5.5:

```python
# sketch — scripts/generate_manifest.py Phase 5.5
# ── Phase 5.5: Codex canonical marketplace at .agents/plugins/marketplace.json ─
# developers.openai.com/codex/plugins/build (2026-05-25) documents this as the
# canonical path. .claude-plugin/marketplace.json remains the legacy-compat path.
# Both files are byte-identical; this is a copy, not a re-emit.
agents_plugins_dir = REPO_ROOT / ".agents" / "plugins"
agents_plugins_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(MARKETPLACE_JSON, agents_plugins_dir / "marketplace.json")
```

- `scripts/generate_manifest.py` lines 9-19 (top-level phase comment): add `5.5 Codex canonical marketplace at .agents/plugins/marketplace.json`.
- `scripts/generate_manifest.py` `_check_drift` function lines 260-269: add `REPO_ROOT / ".agents" / "plugins"` to `root_generated` list so the snapshot includes Phase 5.5 output.
- `tests/test_marketplace.py` add `TestAgentsPluginsMarketplace`:
  - `test_agents_plugins_marketplace_exists` — `.agents/plugins/marketplace.json` exists.
  - `test_agents_plugins_marketplace_byte_identical` — byte-identical to `.claude-plugin/marketplace.json` (per the copy semantics).

**New files**: none source-side. Generator emits `.agents/plugins/marketplace.json` (1).

**Detailed change description**:

Trivial copy step. By keeping both files byte-identical we (a) preserve Codex's legacy compat path, (b) align with Codex's canonical-documented path, (c) make the test trivial. If a future divergence is needed (e.g. Codex stops accepting the legacy schema), this phase can grow into a re-emit; for now copy suffices.

**Verification**:
- Tests added: 2 methods. Net delta +2.
- Pytest expected: +2 passing.
- Drift check: must pass.
- Manual verification: `diff .claude-plugin/marketplace.json .agents/plugins/marketplace.json` shows no diff.

**Commit message** (proposed):
```
feat(generator): add Phase 5.5 emitting .agents/plugins/marketplace.json

Codex documents .agents/plugins/marketplace.json as the canonical
marketplace catalog path (developers.openai.com/codex/plugins/build,
2026-05-25). Currently Codex falls back to .claude-plugin/marketplace.json
(legacy compat). Emit both — copy is byte-identical — so we're ready
when Codex deprecates the legacy path.

New Phase 5.5 in generate_manifest.py main(); drift snapshot extended.

Refs: RECOMMENDATION.md D-14 / A5 / U11
```

---

### Unit 7: `agents` CLI shim — `scripts/agents_cli/` + repo-root installers

**Covers**: A11 — `agents` CLI per D-3 (proper subcommands), D-4 (git clone content), D-5 (all .agents-spec constructs), D-6 (`--scope user` writes only to `~/.agents/`), D-13 Option C (project scope writes everywhere + `--agents-only` flag), D-17 (POSIX install path `~/.local/bin/agents`, Windows `$env:LOCALAPPDATA\agents\bin\agents.ps1`).
**D-decisions**: D-3, D-4, D-5, D-6, D-13, D-17.

**Files to edit**:
- `README.md` lines 24-32 (`GitHub-Direct Install Support` table): add a new row for the `agents` CLI (one-line install + scope). Lines 99-101 (Windsurf block): rewrite to mention `agents install <plugin> --scope project` as a shorthand for the clone-and-open workflow.
- `docs/PLATFORMS.md` lines 547-555 (Windsurf "Install path" section) and 583-585 (Devin "Install path"): add `agents install` example.

**New files** (organized under `scripts/agents_cli/`):
- `scripts/agents_cli/__init__.py` — empty.
- `scripts/agents_cli/main.py` — entry point + argparse dispatcher.
- `scripts/agents_cli/install.py` — install / uninstall / upgrade logic.
- `scripts/agents_cli/list.py` — list / list --available / info logic.
- `scripts/agents_cli/marketplace.py` — marketplace add / remove / list.
- `scripts/agents_cli/constructs/__init__.py` — empty.
- `scripts/agents_cli/constructs/skill.py` — install handler.
- `scripts/agents_cli/constructs/rule.py` — install handler (per-platform format file routing).
- `scripts/agents_cli/constructs/agent.py` — install handler (md + TOML emission for Codex via shared converter).
- `scripts/agents_cli/constructs/hook.py` — install handler (merge into per-platform `.cursor/hooks.json` / `.windsurf/hooks.json` / `.gemini/hooks/hooks.json` plus forward-looking `.agents/hooks/<n>.json`).
- `scripts/agents_cli/constructs/command.py` — install handler.
- `scripts/agents_cli/constructs/mcp.py` — install handler (merge into per-platform MCP configs).
- `scripts/agents_cli/utils/__init__.py` — empty.
- `scripts/agents_cli/utils/git_ops.py` — git clone / ref resolve helpers.
- `scripts/agents_cli/utils/paths.py` — scope → target path resolution per platform.
- Repo root: `install.sh` — POSIX one-liner installer (downloads from raw github, drops `agents` shim into `~/.local/bin/`).
- Repo root: `install.ps1` — PowerShell one-liner installer (drops `agents.ps1` into `$env:LOCALAPPDATA\agents\bin\`).
- Reuse `scripts/converters/md_to_toml.py` (created in Unit 4) for the agent install handler.

**Detailed change description**:

The `agents` CLI is the user-facing shim for Class B platforms (Windsurf, Devin, Cursor CLI) and a convenience wrapper for everyone else. It must implement the exact command surface per D-3 + D-5 + D-13:

```
agents install <plugin>            [--scope project|user] [--agents-only]
agents uninstall <plugin>          [--scope project|user]
agents list
agents list --available            [--type <construct>]
agents upgrade <plugin>            [--scope project|user]
agents upgrade --all               [--scope project|user]
agents info <plugin>
agents marketplace add <url>
agents marketplace list
agents marketplace remove <name>
agents --version
agents --help
```

The `--agents-only` flag (D-13 Option C) toggles strict mode: write only to `.agents/<construct>/` paths, skip per-platform spray.

#### Module layout

```
scripts/agents_cli/
  __init__.py
  main.py                  # entry point + argparse subcommands
  install.py               # install/uninstall/upgrade orchestration
  list.py                  # list/info logic
  marketplace.py           # marketplace add/list/remove
  constructs/
    __init__.py            # plugin-name-prefix → handler mapping
    skill.py
    rule.py
    agent.py
    hook.py
    mcp.py
    command.py
  utils/
    __init__.py
    git_ops.py             # git clone + ref resolve (uses subprocess to call `git`)
    paths.py               # scope-to-path resolution per platform + per construct
```

#### Installer (`install.sh` + `install.ps1`)

The one-liner installers fetch the `agents` shim and drop it into a PATH-visible location, then optionally invoke `agents install <plugin> --scope project`.

`install.sh` (POSIX, sketch):

```bash
# sketch — install.sh
#!/usr/bin/env bash
set -euo pipefail
DEST="${AGENTS_DEST:-$HOME/.local/bin/agents}"
mkdir -p "$(dirname "$DEST")"
# Pull the wrapper script + a tarball of scripts/agents_cli/ at the pinned ref
REF="${AGENTS_REF:-main}"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT
git clone --depth 1 --branch "$REF" \
  https://github.com/DgxSparkLabs/marketplace "$TMPDIR/marketplace"
# Install wrapper that python-execs the package
cat > "$DEST" <<'WRAPPER'
#!/usr/bin/env bash
exec python3 -m agents_cli.main "$@"
WRAPPER
chmod +x "$DEST"
# Move the package into a PYTHONPATH-visible location
INSTALL_LIB="${AGENTS_LIB:-$HOME/.local/share/agents}"
mkdir -p "$INSTALL_LIB"
cp -r "$TMPDIR/marketplace/scripts/agents_cli" "$INSTALL_LIB/agents_cli"
# Persist PYTHONPATH wiring in a small shim
sed -i.bak "s|^exec python3|PYTHONPATH=\"$INSTALL_LIB:\$PYTHONPATH\" exec python3|" "$DEST"
rm -f "$DEST.bak"
echo "Installed 'agents' to $DEST"
if [ "${1:-}" = "install" ]; then exec "$DEST" "$@"; fi
```

`install.ps1` (Windows, sketch):

```powershell
# sketch — install.ps1
$ErrorActionPreference = 'Stop'
$Dest = "$env:LOCALAPPDATA\agents\bin\agents.ps1"
$Lib  = "$env:LOCALAPPDATA\agents\lib"
New-Item -ItemType Directory -Force -Path (Split-Path $Dest) | Out-Null
New-Item -ItemType Directory -Force -Path $Lib | Out-Null
$Ref = if ($env:AGENTS_REF) { $env:AGENTS_REF } else { 'main' }
$Tmp = New-TemporaryFile | ForEach-Object { Remove-Item $_; New-Item -ItemType Directory -Path $_ }
try {
    git clone --depth 1 --branch $Ref https://github.com/DgxSparkLabs/marketplace "$Tmp\marketplace"
    Copy-Item -Recurse -Force "$Tmp\marketplace\scripts\agents_cli" "$Lib\agents_cli"
    @"
`$env:PYTHONPATH = '$Lib;' + `$env:PYTHONPATH
python -m agents_cli.main @args
"@ | Set-Content -Path $Dest -Encoding UTF8
    Write-Host "Installed 'agents' to $Dest"
} finally {
    Remove-Item -Recurse -Force $Tmp
}
```

#### Per-construct install logic (D-13 Option C semantics)

The `agents install <plugin>` command:
1. Resolve construct type from name prefix (`skill-`, `rule-`, `agent-`, `hook-`, `mcp-`, `command-`, `lsp-`, `monitor-`, `output-style-`, `theme-`). Implement in `constructs/__init__.py` as a `PREFIX_TO_HANDLER` dict mapping → module functions.
2. `git clone --depth 1` the marketplace repo (or pull from a cached clone at `~/.cache/agents/marketplace/`) per D-4.
3. Dispatch to the construct handler with `(plugin_name, scope, agents_only)`.

Per-construct destination table (with `--agents-only OFF`, i.e. spray everywhere supported):

| Construct | Project scope writes | User scope writes |
|---|---|---|
| skill | `./.agents/skills/<X>/` | `~/.agents/skills/<X>/` |
| rule | `./.agents/rules/<X>.md` (raw) + `./.cursor/rules/<X>.md` (formats/cursor.md) + `./.windsurf/rules/<X>.md` (formats/windsurf.md) | `~/.agents/rules/<X>.md` only (per D-6 the user-scope is .agents-only) |
| agent | `./.agents/agents/<X>.md` + `./.cursor/agents/<X>.md` + `./.gemini/agents/<X>.md` + `./.codex/agents/<X>.toml` (converted) + `./.claude/agents/<X>.md` | `~/.agents/agents/<X>.md` only |
| hook | `./.agents/hooks/<X>.json` (forward-looking) + merge into `./.cursor/hooks.json` + `./.windsurf/hooks.json` + `./.gemini/hooks/hooks.json` (and `./.codex-plugin/...` if applicable) | `~/.agents/hooks/<X>.json` only |
| mcp | `./.agents/mcp-servers/<X>.json` (forward-looking) + merge into per-platform MCP configs | `~/.agents/mcp-servers/<X>.json` only |
| command | `./.agents/commands/<X>.md` + `./.cursor/commands/<X>.md` | `~/.agents/commands/<X>.md` only |
| lsp / monitor / output-style / theme | Claude-only → if `claude` binary on PATH, shell out to `claude plugin install <plugin>`; otherwise install only `./.agents/<construct>/<X>/` (forward-looking) | Same |

With `--agents-only ON`, **all** writes collapse to the `.agents/<construct>/` path only (matches D-2 strict interpretation).

#### Error handling

| Error | Behavior |
|---|---|
| `--scope` not in {project, user} | Argparse-validated; exit 2 with help. |
| Plugin not found in marketplace | After clone, scan `<repo>/_generated/<plugin>/` — if absent, exit 1 with "Plugin '<plugin>' not found in marketplace. Run `agents list --available`." |
| Write permission denied | Wrap each `mkdir` / `copy` in `try/except OSError`; print path + suggest `--scope user` if project scope failed in a non-writable dir. |
| Network failure on `git clone` | Catch `subprocess.CalledProcessError`; print git's stderr; exit 1. Suggest re-running with `--ref <branch>` or checking network. |
| Construct prefix unknown | Print known prefixes; exit 1. |
| Codex TOML conversion failure | Catch the converter's `ValueError`; print which source file failed and a one-line diagnostic; **continue** the install for other targets (don't fail the whole spray for one bad target). |

#### Tests

`tests/test_agents_cli.py` (new file) — unit + integration tests:
- `TestArgParse` — every documented subcommand parses; bad scope value rejected.
- `TestConstructDispatch` — `skill-X` → skill handler; unknown prefix → error.
- `TestPaths` — scope + construct → expected target path (project + user, with and without `--agents-only`).
- `TestInstallSkillProjectScope` — fixture marketplace, install `skill-example`, assert `.agents/skills/example/SKILL.md` exists.
- `TestInstallRuleAllSpray` — install `rule-example`, assert `.cursor/rules/example.md` + `.windsurf/rules/example.md` + `.agents/rules/example.md` all written.
- `TestAgentsOnlyFlag` — install with `--agents-only`, assert NO per-platform paths written.
- `TestUninstall` — round-trip install + uninstall, assert files removed.
- `TestList` — given a fixture install state, `agents list` enumerates installed plugins.

**Verification**:
- Tests added: ~8 new methods in `tests/test_agents_cli.py`. Net delta +8.
- Pytest expected: +8 new passing.
- Manual verification: `bash install.sh && agents --version` exits 0; `agents install skill-example --scope project` produces `.agents/skills/example/SKILL.md`.

**Commit message** (proposed):
```
feat(cli): add `agents` CLI shim for cross-platform marketplace install

Per D-3 + D-5 + D-13: install/uninstall/list/upgrade/info/marketplace
subcommands; `--scope project|user`; `--agents-only` strict mode (D-13
Option C); git-clone content (D-4); writes only to `~/.agents/` for user
scope (D-6); installed to `~/.local/bin/agents` POSIX / 
`%LOCALAPPDATA%\agents\bin\agents.ps1` Windows (D-17).

Module layout under scripts/agents_cli/: main entry, install/list/
marketplace orchestration, per-construct handlers (skill/rule/agent/
hook/mcp/command), shared utils (git_ops, paths). Reuses
scripts/converters/md_to_toml.py for Codex agent install.

Refs: RECOMMENDATION.md D-3, D-4, D-5, D-6, D-13, D-17 / A11
```

---

### Unit 8: CI — extend `compat-*.yml` and add `compat-agents-cli.yml`

**Covers**: CI assertion changes per RECOMMENDATION.md "CI assertion changes implied" plus D-17 verification.
**D-decisions**: D-13, D-17.

**Files to edit**:
- `.github/workflows/compat-agent.yml` (currently Claude-only per analogy with `compat-hook.yml:1-46`): add a `cursor` job asserting `_generated/agent-example/.cursor-plugin/plugin.json` parses and includes the `agents` field; add a `gemini` job asserting `.gemini/agents/notebook-reviewer.md` exists post-checkout; add a `codex` job asserting `.codex/agents/notebook-reviewer.toml` parses as valid TOML.
- `.github/workflows/compat-hook.yml`: add `cursor`, `gemini`, `windsurf` jobs asserting per-platform hook artifact existence after `uv run scripts/generate_manifest.py`.
- `.github/workflows/compat-command.yml`: add `cursor` job asserting `.cursor-plugin/plugin.json` includes `commands` field.
- `.github/workflows/compat-mcp.yml`: add `cursor` job asserting `.cursor-plugin/plugin.json` includes `mcpServers` field.

**New files**:
- `.github/workflows/compat-agents-cli.yml` — POSIX matrix test (ubuntu-latest) that:
  1. Runs `bash install.sh` from the checkout (with `AGENTS_REF=$GITHUB_HEAD_REF` so the installer pulls the PR's branch).
  2. Verifies `agents --version` exits 0.
  3. Runs `agents install skill-example --scope project` in a temp workdir.
  4. Asserts `./.agents/skills/example/SKILL.md` exists.
  5. Runs `agents uninstall skill-example --scope project`.
  6. Asserts `./.agents/skills/example/` is gone.
  7. (Optional Wave 2) Adds a `windows-latest` job running `install.ps1` + same assertions in PowerShell.

**Detailed change description**:

Each new job mirrors the existing `claude:` job pattern from `compat-marketplace-add.yml:14-51` for structure: `actions/checkout`, `astral-sh/setup-uv`, `uv run scripts/generate_manifest.py`, then platform-specific assertion. For Cursor / Windsurf / Gemini jobs that don't need a CLI install (because the assertions are filesystem-only), skip the platform CLI setup — just `cat`/`grep` the generated artifacts.

For the agents-cli job, the install.sh smoke test is the load-bearing verification. If `AGENTS_REF` doesn't propagate cleanly (e.g. for forked PRs), fall back to `bash install.sh` against `main` and then `agents install skill-example` — the install action will still verify the CLI surface even if it pulls older content.

**Verification**:
- New CI jobs (8-10 jobs across workflows): all must exit 0 on the PR.
- Test for CLI install: covered by `compat-agents-cli.yml` itself.

**Commit message** (proposed):
```
ci: extend compat workflows for new platform emissions + add agents-cli

compat-agent.yml: cursor + gemini + codex assertions for new emissions.
compat-hook.yml: cursor + gemini + windsurf assertions.
compat-command.yml + compat-mcp.yml: cursor assertions.
compat-agents-cli.yml (new): install.sh → agents install/uninstall
round-trip on ubuntu-latest.

Refs: RECOMMENDATION.md "CI assertion changes implied"
```

---

### Unit 9: Documentation + CHANGELOG sweep

**Covers**: D-8 (bundle doc cleanup into refactor) — the full "Doc updates required" table in [[RECOMMENDATION]].
**D-decisions**: D-7 (clean break, no migration helpers), D-8.

**Files to edit**:
- `docs/PLATFORMS.md` line 29 (Cursor row in `At a glance` table): drop `.cursor/skills/`, `.claude/skills/`, `.codex/skills/` from `Skills auto-discovery` cell (replace with `.agents/skills/` only). Line 30 (Windsurf row): drop `.windsurf/skills/` (not emitted by us). Line 31 (Devin row): drop `.devin/skills/`.
- `docs/PLATFORMS.md` lines 197-244 (Codex section): update "What constructs it supports" table (line 203-209) — add `agent: yes` row. Update "Discovery paths it reads" (line 213-218): remove `.codex/skills/<name>/`; add `.codex/agents/<n>.toml`.
- `docs/PLATFORMS.md` lines 414-432 (Cursor section): update "What constructs it supports" — add agent, command, hook, mcp rows. Line 422: update `CursorPlatform.supports = {RuleConstruct, SkillConstruct}` annotation to the new 6-construct set.
- `docs/PLATFORMS.md` lines 505-519 (Windsurf section): add `hook: yes` row; update line 519 from `~/.windsurf/...` to `~/.codeium/windsurf/...` per round-2 finding.
- `docs/PLATFORMS.md` lines 605-628 (Devin section): drop `.devin/skills/`; clarify `.agents/skills/` is now the sole skill path.
- `docs/PLATFORMS.md` lines 699-707 (Per-platform manifest paths table): update Codex/Devin rows (remove their skill mirror columns); update Cursor row (note agents/, hooks via plugin); add Windsurf hook column.
- `docs/ARCHITECTURE.md` lines 111-119 (Seven platform classes table):
  - Codex row: `supports` `{skill, mcp, hook, agent}` (add agent); `mirror_directory` stays `.codex/`; clarify that skill is manifest-only (no mirror branch).
  - Cursor row: `supports` `{rule, skill, agent, command, hook, mcp}`.
  - Gemini row: `supports` `{skill, agent, hook}`.
  - Windsurf row: `supports` `{rule, hook}`.
  - Devin row: `mirror_directory: None`.
  - Agents row: `supports` `{skill, rule}`.
- `docs/ARCHITECTURE.md` lines 179-189 (Phases table): add Phase 5.5 row (between Phase 5 and Phase 6).
- `docs/RULE_FORMAT.md` lines 113-119 (Installation Mechanism — non-Claude-Code platforms list): REMOVE the `.devin/rules/<name>.md` bullet at line 117 entirely (generator never emitted it; per [[RECOMMENDATION]] this is a known stale claim).
- `rules/<name>/README.md` (22 files in `rules/autonomous-persistence/`, `rules/blast-radius/`, etc. — verified via `Glob rules/*/README.md` returning 22 hits): for each file, remove any `.devin/rules/` references; example: `rules/autonomous-persistence/README.md:18` has `nFor other platforms (Devin, Cursor, Windsurf), see the auto-generated mirrors in `.devin/rules/`, `.cursor/rules/`, `.windsurf/rules/` after `git clone`.` — change to drop `.devin/rules/`. (Implementer: search-and-replace `.devin/rules/, ` → `` and `, .devin/rules/` → `` across `rules/*/README.md`.)
- `docs/CONSTRUCT_TYPES.md` (currently a flat 10-row table): add a per-platform support footnote referencing the new emissions; line 19 (theme row) can stay as-is. No major schema change needed.
- `README.md` lines 24-32: add `agents` CLI row to the GitHub-Direct Install Support table. After line 100 (the Windsurf example block ends `Cascade chat`): add a `### Cross-platform: agents CLI` section showing one-liner install + `agents install skill-X`.
- `CHANGELOG.md`: prepend a new dated entry — see [CHANGELOG entry](#changelog-entry-proposed-exact-text) below.

**New files**: none.

**Detailed change description**:

This is a mechanical sweep — every change either deletes a stale claim (per [[RECOMMENDATION]] "Contradictions with first report" table) or adds a one-line mention of a new emission. The implementer should:
1. Read [[RECOMMENDATION]] §"Doc updates required" once as a checklist.
2. Apply each row.
3. Run `uv run scripts/generate_manifest.py --check` to confirm no source-of-truth drift was introduced by the doc edits (shouldn't be possible, but cheap to check).

**Verification**:
- Tests added: 0 (docs).
- Manual verification: `grep -rn ".devin/rules" docs/ rules/` should return 0 hits after the sweep.
- Drift check: must still pass.

**Commit message** (proposed):
```
docs: align platform/construct refs with refactor; CHANGELOG entry

Bundle doc cleanup per D-8. Updates docs/PLATFORMS.md (Cursor/Codex/
Gemini/Windsurf/Devin sections + at-a-glance + per-platform manifest
paths table), docs/ARCHITECTURE.md (seven-platform table + phases),
docs/RULE_FORMAT.md (drop stale .devin/rules/ claim, never emitted),
rules/*/README.md (drop .devin/rules/ refs in 22 READMEs), README.md
(add `agents` CLI section). CHANGELOG entry covers retirements +
additions + new CLI.

Refs: RECOMMENDATION.md D-7, D-8 "Doc updates required"
```

---

## File change inventory (master list)

| File | Units touching it | Lines changed (est.) | Net change |
|---|---|---|---|
| `scripts/platforms.py` | 0, 1, 2, 3, 4, 5 | ~120 LOC modified | +60 LOC, -20 LOC (net +40) |
| `scripts/generate_manifest.py` | 0 (comment), 6, 9 (comment) | ~20 LOC modified | +15 LOC |
| `scripts/utils.py` | (none direct) | 0 | 0 |
| `scripts/converters/__init__.py` | 4 (new) | new file | +0 LOC (empty) |
| `scripts/converters/md_to_toml.py` | 4 (new) | new file | +80 LOC |
| `scripts/agents_cli/__init__.py` | 7 (new) | new file | +0 |
| `scripts/agents_cli/main.py` | 7 (new) | new file | +100 LOC |
| `scripts/agents_cli/install.py` | 7 (new) | new file | +120 LOC |
| `scripts/agents_cli/list.py` | 7 (new) | new file | +50 LOC |
| `scripts/agents_cli/marketplace.py` | 7 (new) | new file | +60 LOC |
| `scripts/agents_cli/constructs/*.py` | 7 (new ×6) | 6 new files | +300 LOC total |
| `scripts/agents_cli/utils/*.py` | 7 (new ×2) | 2 new files | +80 LOC total |
| `install.sh` | 7 (new) | new file | +40 LOC |
| `install.ps1` | 7 (new) | new file | +30 LOC |
| `tests/test_marketplace.py` | 0, 1, 2, 3, 4, 5, 6 | ~60 LOC modified | +90 LOC, -40 LOC (net +50) |
| `tests/test_agents_cli.py` | 7 (new) | new file | +200 LOC |
| `tests/test_md_to_toml.py` | 4 (new) | new file | +60 LOC (or fold into test_marketplace.py) |
| `.github/workflows/compat-agent.yml` | 8 | ~80 LOC added (3 new jobs) | +80 LOC |
| `.github/workflows/compat-hook.yml` | 8 | ~90 LOC added (3 jobs) | +90 LOC |
| `.github/workflows/compat-command.yml` | 8 | ~30 LOC added (1 job) | +30 LOC |
| `.github/workflows/compat-mcp.yml` | 8 | ~30 LOC added (1 job) | +30 LOC |
| `.github/workflows/compat-agents-cli.yml` | 8 (new) | new file | +60 LOC |
| `docs/PLATFORMS.md` | 9 | ~40 LOC modified | net 0 |
| `docs/ARCHITECTURE.md` | 9 | ~15 LOC modified | net 0 |
| `docs/RULE_FORMAT.md` | 9 | -1 LOC | -1 |
| `docs/CONSTRUCT_TYPES.md` | 9 | ~5 LOC added (footnote) | +5 |
| `rules/*/README.md` (22 files) | 9 | ~2 LOC modified each (search/replace) | -44 LOC net |
| `README.md` | 9 | ~25 LOC added | +25 |
| `CHANGELOG.md` | 9 | ~25 LOC added | +25 |
| **Existing files modified** | | | **~12 files** |
| **New files created** | | | **~22 files** |
| **Net LOC (excluding generated output)** | | | **~+1,300 LOC** |

Generated tree deltas (NOT committed by hand — produced by `uv run scripts/generate_manifest.py`):
- DELETES: `.codex/skills/<27>/`, `.devin/skills/<27>/` (entire trees, ~108 generated files)
- ADDS: `.agents/rules/<22>.md` (22), `.cursor/agents/<1>.md` (1), `.gemini/agents/<1>.md` (1), `.gemini/hooks/hooks.json` (1), `.codex/agents/<1>.toml` (1), `.windsurf/hooks.json` (1), `.agents/plugins/marketplace.json` (1), per-plugin `.cursor-plugin/plugin.json` for ~28 newly-supported plugins, per-plugin `.codex-plugin/plugin.json` for the agent plugin

---

## Test plan

### New tests to add

| Test class / file | Assertions |
|---|---|
| `TestAgentsRulesMirror` (in test_marketplace.py) | 22 subTest asserts that `.agents/rules/<name>.md` exists per rule source |
| `TestCursorAgentsMirror` | 1 subTest assert that `.cursor/agents/<n>.md` exists per agent source |
| `TestGeminiAgentsMirror` | 1 subTest assert that `.gemini/agents/<n>.md` exists per agent source |
| `TestGeminiHooksMirror` | 1 assert that `.gemini/hooks/hooks.json` exists; assert it parses as valid JSON with `hooks` key |
| `TestCodexAgentsMirror` | `test_codex_agents_toml_exists` (subTest per agent source); `test_codex_agents_toml_valid` (TOML parse + required keys: `name`, `description`, `developer_instructions`); `test_codex_agents_toml_roundtrip` (assert known input → known output for notebook-reviewer) |
| `TestWindsurfHooksMirror` | 1 assert that `.windsurf/hooks.json` exists + valid JSON |
| `TestAgentsPluginsMarketplace` | `test_agents_plugins_marketplace_exists`; `test_byte_identical_to_claude_plugin_marketplace` |
| `TestMdToTomlConverter` (could live in tests/test_md_to_toml.py or fold in) | `test_frontmatter_extracted`; `test_body_preserved_as_developer_instructions`; `test_tools_csv_parsed_to_list`; `test_missing_frontmatter_raises_valueerror`; `test_round_trip_known_agent` |
| `tests/test_agents_cli.py` | `TestArgParse`, `TestConstructDispatch`, `TestPaths`, `TestInstallSkillProjectScope`, `TestInstallRuleAllSpray`, `TestAgentsOnlyFlag`, `TestUninstall`, `TestList` (8 methods) |
| `test_codex_no_mirror_directory` (replaces `test_codex_skills_mirror`) | assert `PLATFORMS["codex"].mirror_directory` is not None BUT no skill subtree under it (or assert path equals `.codex/` and only `agents/` subdir present after generation) |
| `test_devin_no_mirror_directory` (replaces `test_devin_skills_mirror`) | assert `PLATFORMS["devin"].mirror_directory is None` |

### Existing tests to modify

| Test | Change | Why |
|---|---|---|
| `test_codex_skills_mirror` (lines 211-227) | DELETE | Mirror retired (D-1) |
| `test_devin_skills_mirror` (lines 273-286) | DELETE | Mirror retired (D-1) |
| `TestMirrorHygiene.MIRROR_DIRS_TO_CHECK` (line 867) | Drop `.codex`, `.devin` | Dirs gone |
| `test_codex_plugin_json_emitted_for_supported_constructs` (lines 609-632) | NO CODE CHANGE — auto-picks-up new construct types | Parameterized over `supports` |
| `test_cursor_plugin_json_emitted_for_supported_constructs` (lines 650-673) | NO CODE CHANGE | Parameterized |
| `test_cursor_marketplace_lists_cursor_supported_plugins` (lines 783-799) | NO CODE CHANGE | Parameterized |

### Expected final test count

Today: 52 (per CHANGELOG `2026-05-24 — Phase 5 cross-platform native install compliance` entry).

After refactor:
- Drop: 2 (codex/devin skill mirror tests).
- Add: ~20 (per the table above).
- Net: 52 + 20 - 2 = **70**.

### Drift-check expectations

The first `uv run scripts/generate_manifest.py` after the refactor will produce a large diff:
- Removes: ~108 files under `.codex/skills/` and `.devin/skills/`.
- Adds: ~55 files (`.agents/rules/<22>` + `.cursor/agents/<1>` + `.gemini/agents/<1>` + `.gemini/hooks/hooks.json` + `.codex/agents/<1>.toml` + `.windsurf/hooks.json` + `.agents/plugins/marketplace.json` + new per-plugin manifests).

Net file-count delta on disk: roughly **-55 files** (removals outweigh additions).

After regeneration the implementer must `git add -A` (because the generator writes/removes files, but it can't unstage what git already tracked) and the next `--check` invocation should exit 0.

---

## CI assertion changes

### Workflows to modify

See Unit 8 — adding cursor/gemini/codex/windsurf jobs to `compat-agent.yml`, `compat-hook.yml`, `compat-command.yml`, `compat-mcp.yml`.

### New CI assertions (if any)

- For sub-agent install: assert `.cursor/agents/<n>.md`, `.gemini/agents/<n>.md`, `.codex/agents/<n>.toml` present + parse.
- For hook install: assert `.cursor-plugin/plugin.json` for `hook-example` includes `"hooks"` field; assert `.gemini/hooks/hooks.json` + `.windsurf/hooks.json` present + parse.
- For command install: assert `.cursor-plugin/plugin.json` for `command-example` includes `"commands"` field.
- For MCP install: assert `.cursor-plugin/plugin.json` for `mcp-example` includes `"mcpServers"` field.
- For `agents` CLI: `compat-agents-cli.yml` end-to-end install/uninstall round-trip.

---

## Documentation updates (bundled in refactor PR per D-8)

The implementer should consult [[RECOMMENDATION]] §"Doc updates required" table for the full list; Unit 9 enumerates each file. Key bullets:

- `docs/PLATFORMS.md` — Cursor / Codex / Gemini / Windsurf / Devin sections + at-a-glance + per-platform manifest paths table; line 519 Windsurf user-scope correction.
- `docs/ARCHITECTURE.md` — seven-platform table; Phase 5.5 row.
- `docs/RULE_FORMAT.md` — drop stale `.devin/rules/` claim at line 117.
- `docs/CONSTRUCT_TYPES.md` — small per-platform support footnote.
- `rules/*/README.md` (22 files) — drop `.devin/rules/` references.
- `README.md` — `agents` CLI install section.
- `CHANGELOG.md` — new dated entry below.

---

## CHANGELOG entry (proposed exact text)

```markdown
## 2026-05-XX — Platform feature routing refactor

Surveyed every platform's native capabilities (Cursor 2.4 sub-agents, Codex sub-agents TOML, Gemini hooks/agents, Windsurf hooks) and discovered the generator was under-emitting against documented APIs. This refactor (a) retires two dead skill mirrors, (b) expands per-platform `supports` sets to cover sub-agents on Cursor + Gemini + Codex and hooks on Cursor + Gemini + Windsurf and commands/MCP on Cursor, (c) adds a forward-looking `.agents/rules/` mirror and `.agents/plugins/marketplace.json` (Codex canonical path), and (d) introduces an `agents` CLI shim for Class B platforms.

### Retired (breaking — no migration helper per D-7)

- `.codex/skills/` mirror tree (27 directories) — Codex installs plugins via `_generated/<plugin>/.codex-plugin/plugin.json`, not the repo-root skill mirror (verified hermetic act run Q-A1 PASS).
- `.devin/skills/` mirror tree (27 directories) — Devin enumerates `.agents/skills/` natively (verified hermetic act run Q-B1: 27 skills enumerated post-retirement).
- Migration: nothing required for users — content remains available at `.agents/skills/` and via per-plugin manifests.

### Added — per-platform emission

- **Cursor sub-agents** at `.cursor/agents/<name>.md` (`CursorPlatform.supports += {AgentConstruct}`); per-plugin `.cursor-plugin/plugin.json` now includes `agents`, `commands`, `hooks`, `mcpServers` fields for agent/command/hook/MCP plugins (per `cursor.com/docs/reference/plugins`, 2026-05-25).
- **Gemini sub-agents** at `.gemini/agents/<name>.md` (`GeminiPlatform.supports += {AgentConstruct}`) and **Gemini hooks** at `.gemini/hooks/hooks.json` (`+= {HookConstruct}`) per `geminicli.com/docs/extensions/reference/` (2026-05-25).
- **Codex sub-agents** at `.codex/agents/<name>.toml` (`CodexPlatform.supports += {AgentConstruct}`) per `developers.openai.com/codex/subagents/` (2026-05-25). Source format stays Claude-style markdown with YAML frontmatter (D-16); conversion happens at emit time via `scripts/converters/md_to_toml.py`.
- **Windsurf hooks** at `.windsurf/hooks.json` (`WindsurfPlatform.supports += {HookConstruct}`) per `docs.windsurf.com/windsurf/cascade/hooks` (2026-05-25).
- **`.agents/rules/<name>.md`** forward-looking convergence (`AgentsPlatform.supports += {RuleConstruct}`) — no platform reads it today (verified Q-R1/Q-R2) but Cursor 2.7+ and Windsurf 2.0 are credible adopters.

### Added — generator infrastructure

- **Phase 5.5**: emit `.agents/plugins/marketplace.json` (byte-identical copy of `.claude-plugin/marketplace.json`) — Codex's canonical marketplace path per `developers.openai.com/codex/plugins/build` (2026-05-25). Both paths remain valid; we now serve both.
- **`scripts/converters/md_to_toml.py`** — Claude-md → Codex-TOML translator for sub-agent emission.

### Added — `agents` CLI shim (`scripts/agents_cli/`)

- New CLI providing Claude-equivalent install UX for Class B platforms (Windsurf, Devin, Cursor CLI). Subcommands: `install`, `uninstall`, `list`, `list --available`, `upgrade`, `upgrade --all`, `info`, `marketplace add|list|remove`, `--version`, `--help`.
- `--scope project|user` semantics: project = `./.agents/<construct>/` + per-platform paths; user = `~/.agents/<construct>/` only (per D-6).
- `--agents-only` strict mode skips per-platform spray (D-13 Option C).
- Content source: `git clone` (per D-4).
- Install location: `~/.local/bin/agents` (POSIX) / `$env:LOCALAPPDATA\agents\bin\agents.ps1` (Windows) (per D-17).
- One-liner installers at repo root: `install.sh` (POSIX) and `install.ps1` (Windows).

### Documentation

- `docs/PLATFORMS.md`, `docs/ARCHITECTURE.md`, `docs/CONSTRUCT_TYPES.md`, `docs/RULE_FORMAT.md` aligned with new per-platform support matrix.
- `docs/RULE_FORMAT.md:117` removed stale `.devin/rules/` claim (the generator never emitted that path).
- `rules/*/README.md` (22 files) — dropped `.devin/rules/` references.
- `README.md` — added `agents` CLI install section.
- Research dossier: `docs/research/platform-feature-routing/` (RECOMMENDATION.md, IMPLEMENTATION_PLAN.md, hermetic act logs for Q-A1 / Q-B1).

### Tests

- `tests/test_marketplace.py` extended (52 → ~62 tests post-refactor across new TestAgentsRulesMirror, TestCursorAgentsMirror, TestGeminiAgentsMirror, TestGeminiHooksMirror, TestCodexAgentsMirror, TestWindsurfHooksMirror, TestAgentsPluginsMarketplace classes; 2 tests retired with their mirrors).
- `tests/test_agents_cli.py` (new, ~8 tests) — CLI argparse, dispatch, install/uninstall round-trip.
- `tests/test_md_to_toml.py` (new or folded in, ~5 tests) — converter correctness + roundtrip.

### CI

- Extended `compat-agent.yml`, `compat-hook.yml`, `compat-command.yml`, `compat-mcp.yml` with cursor / gemini / windsurf / codex assertion jobs.
- New `compat-agents-cli.yml` — install.sh → `agents install skill-example --scope project` round-trip on ubuntu-latest.
```

---

## CLI shim implementation detail

### Module layout

```
scripts/agents_cli/
  __init__.py
  main.py                  # entry point + argparse
  install.py               # install/uninstall/upgrade orchestration
  list.py                  # list/info logic
  marketplace.py           # marketplace add/list/remove
  constructs/
    __init__.py            # PREFIX_TO_HANDLER dict
    skill.py
    rule.py
    agent.py
    hook.py
    mcp.py
    command.py
  utils/
    __init__.py
    git_ops.py             # git clone + ref resolve (subprocess wrappers)
    paths.py               # scope-to-path resolution per platform + per construct
```

### Installer scripts

See Unit 7 for full `install.sh` + `install.ps1` sketches. Both follow the same pattern:
1. Resolve install target (`~/.local/bin/agents` POSIX, `$env:LOCALAPPDATA\agents\bin\agents.ps1` Windows).
2. `git clone --depth 1` the marketplace.
3. Copy `scripts/agents_cli/` into a stable library path (`~/.local/share/agents/` or `$env:LOCALAPPDATA\agents\lib\`).
4. Write a 3-line wrapper that sets `PYTHONPATH` and execs `python3 -m agents_cli.main "$@"`.
5. Optionally exec the rest of the user's command-line args (so the curl-piped one-liner can install + immediately use).

### Per-construct install logic

See [Unit 7](#unit-7-agents-cli-shim--scriptsagents_cli--repo-root-installers) tables for the per-construct destination matrix under D-13 Option C and the `--agents-only` override.

### Error handling

| Error | Behavior |
|---|---|
| `--scope` not in {project, user} | argparse rejects; exit 2 |
| Plugin name unknown | Print "Plugin '<name>' not found. Try `agents list --available`." → exit 1 |
| Write permission denied | Catch `OSError`; print path + suggest `--scope user` → exit 1 |
| Git clone failed | Surface git's stderr; suggest `--ref` or network check → exit 1 |
| Unknown construct prefix | Print known prefixes → exit 1 |
| TOML conversion error (agent install on Codex target) | Catch ValueError; print which agent failed; **continue install for other targets** (per-target failure tolerance) |

---

## Codex markdown-to-TOML converter (per D-16)

Full sketch of `scripts/converters/md_to_toml.py`:

```python
# sketch — scripts/converters/md_to_toml.py
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
md_to_toml.py — convert Claude-style agent markdown (YAML frontmatter + body)
to Codex sub-agent TOML per developers.openai.com/codex/subagents/ (2026-05-25).

Input format (Claude/Cursor/Gemini canonical, per agents/example/agents/notebook-reviewer.md):
    ---
    name: notebook-reviewer
    description: Reviews a lab notebook entry...
    tools: Read, Grep, Glob
    ---

    You are a peer reviewer for laboratory notebook entries...

Output format (Codex):
    name = "notebook-reviewer"
    description = "Reviews a lab notebook entry..."
    tools = ["Read", "Grep", "Glob"]
    developer_instructions = '''
    You are a peer reviewer for laboratory notebook entries...
    '''
"""

from __future__ import annotations

__all__ = ["claude_agent_md_to_codex_toml"]


def _parse_frontmatter_and_body(text: str) -> tuple[dict, str]:
    """Split a markdown doc with YAML frontmatter into (frontmatter_dict, body_str).

    Reuses the same frontmatter parsing semantics as utils._frontmatter — supports
    simple scalar values + a comma-separated 'tools' list. Raises ValueError if
    frontmatter is malformed (missing closing '---' delimiter).
    """
    if not text.startswith("---\n"):
        raise ValueError("Agent markdown must start with '---' YAML frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("Agent markdown frontmatter missing closing '---'")
    fm_text = text[4:end]
    body = text[end + len("\n---"):].lstrip("\n")
    fm: dict = {}
    for raw in fm_text.splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        if ":" not in raw:
            continue
        key, _, val = raw.partition(":")
        fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm, body


def _toml_escape_basic_string(s: str) -> str:
    """Escape a TOML basic string (double-quoted, single-line)."""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def _toml_multiline_literal(s: str) -> str:
    """Emit a TOML multi-line literal string (triple-single-quoted).

    Literal strings have no escapes — the only forbidden sequence is ''' itself.
    If the body contains ''' we fall back to triple-double-quoted basic string.
    """
    if "'''" not in s:
        # Strip trailing newline so the closing ''' lands on its own line
        return "'''\n" + s.rstrip("\n") + "\n'''"
    # Fallback: triple-double-quoted basic string with escapes
    escaped = s.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    return '"""\n' + escaped.rstrip("\n") + '\n"""'


def claude_agent_md_to_codex_toml(text: str) -> str:
    """Convert one Claude-style agent .md (frontmatter + body) to Codex TOML.

    Required Codex fields per the docs:
        - name             (required)
        - description      (required)
        - developer_instructions  (required; the agent's system prompt)

    Optional fields (passed through when present in frontmatter):
        - tools (comma-separated list in source; emitted as TOML array)
        - model (string)

    Raises ValueError if a required field is missing.
    """
    fm, body = _parse_frontmatter_and_body(text)

    if "name" not in fm:
        raise ValueError("Agent frontmatter missing required 'name' field")
    if "description" not in fm:
        raise ValueError("Agent frontmatter missing required 'description' field")

    lines: list[str] = []
    lines.append(f'name = "{_toml_escape_basic_string(fm["name"])}"')
    lines.append(f'description = "{_toml_escape_basic_string(fm["description"])}"')

    # Optional tools[] from comma-separated string
    if "tools" in fm and fm["tools"]:
        tools = [t.strip() for t in fm["tools"].split(",") if t.strip()]
        if tools:
            quoted = ", ".join(f'"{_toml_escape_basic_string(t)}"' for t in tools)
            lines.append(f"tools = [{quoted}]")

    # Optional model passthrough
    if "model" in fm and fm["model"]:
        lines.append(f'model = "{_toml_escape_basic_string(fm["model"])}"')

    # Required: developer_instructions (the body)
    lines.append("developer_instructions = " + _toml_multiline_literal(body))

    return "\n".join(lines) + "\n"
```

**Proposed converter tests** (`tests/test_md_to_toml.py` or folded into `test_marketplace.py`):

```python
# sketch — tests/test_md_to_toml.py
import tomllib
import unittest
from pathlib import Path

# Make the converter importable (mirrors test_marketplace.py sys.path tactic)
import sys
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from converters.md_to_toml import claude_agent_md_to_codex_toml


SAMPLE = """---
name: notebook-reviewer
description: Reviews a lab notebook entry as a skeptical peer reviewer.
tools: Read, Grep, Glob
---

You are a peer reviewer for laboratory notebook entries.

Apply skeptical eye.
"""


class TestMdToTomlConverter(unittest.TestCase):
    def test_required_fields_emitted(self):
        out = claude_agent_md_to_codex_toml(SAMPLE)
        data = tomllib.loads(out)
        self.assertEqual(data["name"], "notebook-reviewer")
        self.assertTrue(data["description"].startswith("Reviews"))
        self.assertIn("peer reviewer", data["developer_instructions"])

    def test_tools_parsed_as_array(self):
        out = claude_agent_md_to_codex_toml(SAMPLE)
        data = tomllib.loads(out)
        self.assertEqual(data["tools"], ["Read", "Grep", "Glob"])

    def test_missing_frontmatter_raises(self):
        with self.assertRaises(ValueError):
            claude_agent_md_to_codex_toml("no frontmatter here")

    def test_missing_required_name_raises(self):
        bad = "---\ndescription: x\n---\nbody"
        with self.assertRaises(ValueError):
            claude_agent_md_to_codex_toml(bad)

    def test_round_trip_on_real_example(self):
        src = (REPO_ROOT / "agents" / "example" / "agents" / "notebook-reviewer.md").read_text(encoding="utf-8")
        out = claude_agent_md_to_codex_toml(src)
        data = tomllib.loads(out)  # round-trips through stdlib TOML reader
        self.assertEqual(data["name"], "notebook-reviewer")


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

---

## Generator phase change details

### Phase 1.5 supports-gate expansion

Phase 1.5 (`scripts/generate_manifest.py:133-153`) iterates each `(plugin, platform)` pair and emits `_generated/<plugin>/.<platform>-plugin/plugin.json` where `type(construct) in platform.supports`. After the refactor:

| Platform | supports gains | New per-plugin manifests emitted |
|---|---|---|
| Cursor | Agent, Command, Hook, MCP | `_generated/agent-example/.cursor-plugin/plugin.json` + `command-example` + `hook-example` + `mcp-example` (4 new; with extended `build_plugin_json` populating the right field per type) |
| Gemini | Agent, Hook | `{}` returned (Gemini doesn't emit per-plugin manifests — `build_plugin_json` returns empty); no Phase 1.5 output. The new supports values are needed for the Phase 3 emit gate, not Phase 1.5. |
| Codex | Agent | `{}` returned for Agent in `build_plugin_json` (no plugin manifest schema field for sub-agents); the new supports value drives Phase 3 mirror emission only. |
| Windsurf | Hook | `{}` returned (Windsurf has no plugin manifest); supports drives Phase 3 only. |
| Agents | Rule | `{}` returned (Agents hosts content only); supports drives Phase 3 only. |

### Phase 3 mirror emission expansion

Phase 3 (`scripts/generate_manifest.py:182-196`) wipes each `platform.mirror_directory` and then calls `platform.emit(construct, name)` for every supported construct instance. After the refactor:

- `AgentsPlatform.emit` (Unit 1) → adds RuleConstruct branch writing `.agents/rules/<name>.md`.
- `CursorPlatform.emit` (Unit 2) → adds AgentConstruct branch writing `.cursor/agents/<name>.md`.
- `GeminiPlatform.emit` (Unit 3) → adds AgentConstruct and HookConstruct branches.
- `CodexPlatform.emit` (Unit 4) → adds AgentConstruct branch with md→TOML conversion.
- `WindsurfPlatform.emit` (Unit 5) → adds HookConstruct branch.

The Phase 3 loop body itself does not change — only the emit method bodies grow.

### New Phase 5.5

See Unit 6. Trivial 3-line `shutil.copy2` after Phase 5 closes.

---

## PR strategy

### Branch

Already on `refactor/platform-feature-routing` (verified per repo state at start of session — the current branch in the git status pre-task message).

### Commit grouping

Recommended: **10 commits**, one per Unit (0-8) + Unit 9 (docs/CHANGELOG) as the last commit. This gives a clean reviewer pass-by-pass:

1. `refactor(platforms): retire .codex/skills/ and .devin/skills/ mirrors` (Unit 0)
2. `feat(agents): emit .agents/rules/<name>.md for forward-looking convergence` (Unit 1)
3. `feat(cursor): emit sub-agents + commands + hooks + MCP per Cursor 2.4 schema` (Unit 2)
4. `feat(gemini): emit sub-agents + hooks under .gemini/ extension root` (Unit 3)
5. `feat(codex): emit Codex sub-agents at .codex/agents/<n>.toml` (Unit 4)
6. `feat(windsurf): emit .windsurf/hooks.json from HookConstruct` (Unit 5)
7. `feat(generator): add Phase 5.5 emitting .agents/plugins/marketplace.json` (Unit 6)
8. `feat(cli): add `agents` CLI shim for cross-platform marketplace install` (Unit 7)
9. `ci: extend compat workflows for new platform emissions + add agents-cli` (Unit 8)
10. `docs: align platform/construct refs with refactor; CHANGELOG entry` (Unit 9)

Each commit must include the regenerated `_generated/` + mirror trees + new `.agents/plugins/marketplace.json` + test additions for that unit. The implementer should run `uv run scripts/generate_manifest.py` after each Python change and `uv run scripts/generate_manifest.py --check` before each commit.

### PR body template

```markdown
## Summary

Refactors the generator to (a) retire two redundant skill mirrors, (b) emit
sub-agents to Cursor + Gemini + Codex, (c) emit hooks to Cursor + Gemini +
Windsurf, (d) emit commands + MCP to Cursor, (e) add a forward-looking
.agents/rules/ + .agents/plugins/marketplace.json layer, and (f) introduce an
`agents` CLI shim for Class B platforms.

See docs/research/platform-feature-routing/RECOMMENDATION.md and
IMPLEMENTATION_PLAN.md for the full research + plan.

## Locked decisions

D-1 through D-17 (see RECOMMENDATION.md).

## Test plan

- [x] `uv run tests/test_marketplace.py` — 70 passing (52 → 70, +20/-2)
- [x] `uv run tests/test_agents_cli.py` — 8 passing (new file)
- [x] `uv run tests/test_md_to_toml.py` — 5 passing (new file)
- [x] `uv run scripts/generate_manifest.py --check` — exits 0
- [x] `bash install.sh` smoke test in fresh container
- [x] `compat-*.yml` workflows all green
- [x] `compat-agents-cli.yml` (new) green

🤖 Generated with Claude Code (planning agent)
```

### Mergeability gates (human review checkpoints before merge)

1. **Diff size sanity** — net +1,300 LOC source + ~22 new files + ~10 commits. If the diff explodes past that, the implementer is gold-plating or has a bug.
2. **Drift check passes** — `uv run scripts/generate_manifest.py --check` exits 0 on the final commit.
3. **CI all green** — every `compat-*.yml` job passes (including new ones).
4. **Manual smoke** — `bash install.sh && agents install skill-example --scope project && ls .agents/skills/example/SKILL.md`.
5. **Round-2 act runs** still reproduce — the Q-A1 and Q-B1 workflow logs cited in [[RECOMMENDATION]] should still PASS against the post-refactor branch.

---

## Risk register

| # | Risk | Mitigation |
|---|---|---|
| 1 | Codex md→TOML converter mishandles edge cases (escaped quotes in body, `tools:` value containing comma in a description, frontmatter with multi-line values) | Round-trip test on the real `agents/example/agents/notebook-reviewer.md` is the canary. Add explicit tests for triple-quote-in-body and multi-line frontmatter (deferred — no source files use those today). |
| 2 | `--agents-only` flag default behaviour misinterpreted by users (might think it's the default) | Surface in `--help` text + README clearly. Default is "spray to all per-platform paths" per D-13 Option C. |
| 3 | `install.sh` PYTHONPATH wiring breaks on systems where `python3` doesn't exist (e.g. some Linux distros where only `python` is on PATH) | Probe for `python3` → `python` → fail with a clear "Install Python 3.11+ first" message. |
| 4 | Hook merge semantics (multiple hook plugins → `.windsurf/hooks.json` / `.gemini/hooks/hooks.json` overwrite) — single plugin today so latent | TODO comment in emit branches; track as a follow-up issue. Acceptable for v1. |
| 5 | `_check_drift` snapshot doesn't include `.agents/plugins/` (introduced in Unit 6) — would mask Phase 5.5 drift | Unit 6 explicitly adds it to `_check_drift`'s `root_generated` list. |
| 6 | `git rm -r .codex/ .devin/` (Unit 0) is destructive — easy to commit accidentally if someone runs it before reading the plan | Step is in commit message; included in PR body's test plan checklist. |
| 7 | Cursor's plugin manifest schema for `agents`/`commands`/`hooks` fields not fully documented; we infer the pointer string from `cursor.com/docs/reference/plugins` | The fields appear in the published reference; if Cursor rejects an emitted manifest, the implementer adjusts the pointer value (e.g. drop the trailing slash) and re-runs `compat-*.yml`. Cheap fix. |
| 8 | CI `compat-agents-cli.yml` may not have `git` configured in the ubuntu-latest image for the install.sh clone | ubuntu-latest ships git; verify in the job. If a forked PR + `AGENTS_REF=$GITHUB_HEAD_REF` doesn't authenticate, the install.sh falls back to `main` — assertions still cover the CLI surface. |
| 9 | Phase 5.5 `shutil.copy2` doesn't preserve POSIX mode bits identically on Windows runners | The byte-identical test (Unit 6) catches content drift; perms don't matter for a JSON file. |

---

## Open questions to surface to user during implementation (if any)

The plan locks 17 decisions and the implementer should not need to ask for further direction. Two genuine residual open questions:

1. **Hook merge format** when a second hook plugin lands (today only `hook-example` exists). Should the generator merge into a single `.windsurf/hooks.json` / `.gemini/hooks/hooks.json` by concatenating `hooks` arrays, or fail-fast on collision? **Recommended default: merge concatenate; user can override later.** Not blocking — current single-plugin-today means this isn't exercised.
2. **`agents` CLI bootstrap dependency on Python** — `install.sh` assumes Python 3.11+ is installed (used by `python3 -m agents_cli.main`). Acceptable for the marketplace's target audience (developers) but warrants a one-line callout in the install.sh failure path. **Recommended: probe Python at install time, print clear failure message if missing.** Implementer decides messaging.

Neither blocks implementation. If the user has strong opinions on either, surface them when the implementer hits the relevant unit.

---

## Cross-references

- [[RECOMMENDATION]] — full research dossier (round 1 + round 2). All D-decisions and U-items cited here trace back to that document.
- [[../../ARCHITECTURE]] — generator architecture; the seven-platform table at lines 111-119 is what changes per Unit 9.
- [[../../PLATFORMS]] — per-platform reference; per-platform sections all touched in Unit 9.
- [[../../CONSTRUCT_TYPES]] — construct reference table (small footnote in Unit 9).
- [[../../RULE_FORMAT]] — line 117 stale `.devin/rules/` claim removed in Unit 9.
- `scripts/platforms.py` — primary mutation target (Units 0-5).
- `scripts/generate_manifest.py` — Phase 5.5 added (Unit 6) + Unit 0 comment updates.
- `scripts/constructs.py` — **not modified** by this refactor (the construct protocol is stable; only platform `supports` gates change).
- `scripts/utils.py` — **not modified** (helpers are reused; new converter lives at `scripts/converters/md_to_toml.py` per the new module layout).
- `tests/test_marketplace.py` — extended per [Test plan](#test-plan).
