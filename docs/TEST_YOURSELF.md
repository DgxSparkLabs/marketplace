---
date: 2026-05-25
purpose: hands-on QA verification of all 6 supported platforms + the `agents` CLI, per construct × per platform
audience: operator-qa
status: live
---

# Test Yourself — Platform QA Walkthrough

A step-by-step verification guide for an operator to confirm the DgxSparkLabs marketplace works end-to-end on each of the six supported platforms plus the cross-platform `agents` CLI. Each section is independent — work through all of them, or pick the platforms you actually use.

This is a hand-holding document. If something below looks obvious, that's intentional — the goal is that someone who has never touched these tools can follow it without guessing.

**Round-2 expansion (2026-05-25)**: this revision was expanded from "a handful of exemplary cells" to **a full construct × platform grid**. Every construct type that a platform supports is exercised by a hands-on test. The 🐛 / ✅ callouts from the 2026-05-25 QA pass are preserved.

---

## How to use this guide

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

## Master verification matrix

This matrix is the index. Each cell tells you what to expect in the per-platform sections below.

- **TEST** — the platform emits and consumes this construct; QA covers it with a hands-on test in this doc.
- **TEST¹/TEST²/etc.** — TEST with a footnote (caveat, known bug, or pending QA).
- **N/A** — the platform doesn't support this construct (per its `supports` set in `scripts/platforms.py` and the per-platform "What constructs it supports" tables in `docs/PLATFORMS.md`).
- **CLAUDE-ONLY** — for lsp / monitor / output-style / theme, only Claude consumes these constructs; other platforms have no concept and no test path.

|                 | Claude  | Codex   | Gemini  | Cursor IDE | Cursor CLI | Windsurf | Devin   | `agents` CLI |
|---              |---      |---      |---      |---         |---         |---       |---      |---           |
| skill           | TEST    | TEST    | TEST    | TEST¹      | TEST²      | TEST     | TEST    | TEST         |
| rule            | TEST³   | N/A⁴    | N/A⁵    | TEST       | TEST²      | TEST     | TEST⁶   | TEST         |
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
3. Claude rules require a manual `bash <cache>/activate.sh` post-install step (per `docs/PLATFORMS.md` Claude "Known gaps" section, upstream issue `anthropics/claude-code#21163`).
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

## Prerequisites (one-time host setup)

### Docker Desktop (required for hermetic path)

```powershell
# Windows
winget install Docker.DockerDesktop
# Then launch Docker Desktop from Start Menu and let it finish first-run setup
docker --version
docker run --rm hello-world      # should print "Hello from Docker!"
```

If you'd rather skip Docker and test natively for everything, that's fine — just use Setup option B in each section.

### Node.js 18+ (required for Claude / Codex / Gemini CLIs)

```powershell
winget install OpenJS.NodeJS.LTS
node --version       # expected: v18.x or higher
npm --version
```

### WSL or Git Bash (only needed for Devin native install)

If you don't already have WSL:

```powershell
wsl --install
# Reboot when prompted
```

Otherwise, Git Bash from `git-scm.com` works for Devin's installer too.

### Docker hermetic-session primer

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

### Three install sources: choose remote-main, remote-branch, or local-clone

This doc was originally written assuming "install from `DgxSparkLabs/marketplace` on default branch." That works fine for smoke-testing a released marketplace, but it is **useless for pre-merge PR verification** — `main` doesn't yet have the fixes the PR introduces. To make this guide usable for testing PRs (the canonical example throughout this doc is PR #5 = `fix/platform-emission-bugs`), every per-platform section now documents THREE install sources where the platform supports them.

| Mode | What it tests | When to use |
|---|---|---|
| Remote `main` | The state of `main` on GitHub | Smoke-test of released marketplace |
| Remote branch ref | A specific branch on GitHub (e.g., `fix/platform-emission-bugs`) | Pre-merge PR verification — needs the platform's `--ref` flag |
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

**Canonical example branch throughout this doc**: `fix/platform-emission-bugs` (PR #5). Where you see that branch ref below, substitute your PR's branch when testing a different change.

**Docker setup pattern when testing a PR branch**: every per-platform Docker setup below has been updated to clone the PR branch into `/workspace/marketplace` inside the container, so the install commands further down can point at the local clone OR the remote branch. To test against `main` instead, omit `--branch fix/platform-emission-bugs` from the `git clone` call (or use `--branch main`).

### Repository state

Make sure you're on a recent `main` of `DgxSparkLabs/marketplace`:

```powershell
cd C:\Users\devic\source\marketplace
git fetch origin
git checkout main
git pull
git log --oneline -1        # expected: a86cb86 or newer
```

### Example plugins used as canonical test items

Throughout the per-construct tests below, these plugin names are used as the standard examples — they all exist in `_generated/` after the generator runs:

| Construct | Plugin name | Source dir |
|---|---|---|
| skill | `skill-example` | `skills/example/` |
| rule | `rule-example` | `rules/example/` |
| agent (sub-agent) | `agent-example` | `agents/example/` |
| command | `command-example` | `commands/example/` |
| hook | `hook-example` | `hooks/example/` |
| mcp | `mcp-example` | `mcp-servers/example/` |
| lsp | `lsp-example` | `lsp-servers/example/` |
| monitor | `monitor-example` | `monitors/example/` |
| output-style | `output-style-example` | `output-styles/example/` |
| theme | `theme-example` | `themes/example/` |

---

## Platform 1: Claude Code

**What we're verifying**: marketplace registration + per-construct install for **all 10 construct types** Claude supports (`ClaudeCodePlatform.supports` is the full set per `docs/PLATFORMS.md` Claude "What constructs it supports"). Nothing newly emitted for Claude in this refactor — this is the regression-check platform.

### Setup option A: Docker (hermetic)

```powershell
docker run -it --name qa-claude node:20 bash
```

Inside the container (`node:20` has `git` pre-installed):
```bash
# Install Claude CLI
npm install -g @anthropic-ai/claude-code
claude --version

# Clone the branch you want to test. For PR #5 verification, use the PR branch:
git clone --branch fix/platform-emission-bugs https://github.com/DgxSparkLabs/marketplace.git /workspace/marketplace
cd /workspace/marketplace

# (To test against main instead: replace --branch fix/platform-emission-bugs with --branch main, or omit --branch.)
```

### Setup option B: Native

```powershell
npm install -g @anthropic-ai/claude-code
claude --version
```

### Auth

Marketplace registration, listing, and install are auth-free (verified by `act`-based CI). `claude auth login` is only required if you actually use Claude for chat — not for the QA flow here.

### Marketplace registration

Use the `claude` CLI directly — these commands are scriptable and work in headless containers (the equivalent `/plugin ...` slash commands require the interactive Claude session UI).

- [ ] Step 1: Register the marketplace. Pick ONE of:
  - **Remote `main`** (smoke test only — NOT for PR #5 verification because `main` doesn't have the fixes yet):
    ```bash
    claude plugin marketplace add DgxSparkLabs/marketplace
    ```
  - **Remote PR branch** (Claude's `plugin marketplace add` has **no documented `--ref` flag** per `docs/PLATFORMS.md` Claude "Known gaps" — use the local-clone path below for PR verification):
    ```bash
    # Not supported. Clone the branch locally and use the local-clone form.
    ```
  - **Local clone** (recommended for PR #5 verification — tests exactly the bytes at `/workspace/marketplace`):
    ```bash
    claude plugin marketplace add /workspace/marketplace
    ```
  - **Expected (for remote-main and local-clone)**: "Successfully added marketplace 'dgxsparklabs-marketplace'" (or similar).
- [ ] Step 2: `claude plugin marketplace list`
  - **Expected**: `dgxsparklabs-marketplace` appears in the registered marketplaces list
- [ ] Step 3: `claude plugin list --json --available | head -50`
  - **Expected**: JSON output enumerating every plugin in the marketplace (81+ entries)

### Per-construct verification

Each test installs ONE plugin of the construct type, then invokes it. Per-construct cleanup is folded into the master cleanup block at the end.

#### Skill — `skill-example`
- [ ] **Install**: `claude plugin install skill-example@dgxsparklabs-marketplace --scope project`
- [ ] **Hands-on invocation**: in a `claude` session, type `/example` (or the actual command name) and observe the skill prompts you for the notification payload.
- [ ] **Expected**: the skill appears in the slash-command dropdown with its correct description; invocation executes the skill body.
- [ ] **Diagnostic (only if hands-on fails)**: `claude plugin details skill-example` should show the skill metadata, and `~/.claude/plugins/cache/dgxsparklabs-marketplace/skill-example/<version>/` should be populated.

#### Rule — `rule-example`
- [ ] **Install**: `claude plugin install rule-example@dgxsparklabs-marketplace --scope project`
- [ ] **Activate** (Claude has no native rule install slot yet, per `docs/PLATFORMS.md` Claude "Known gaps"): `bash ~/.claude/plugins/cache/dgxsparklabs-marketplace/rule-example/<version>/activate.sh`
- [ ] **Hands-on invocation**: start a `claude` session in the project and ask "what rules are currently active?" or attempt an action the rule should constrain.
- [ ] **Expected**: Claude's response reflects the rule's guidance (e.g., the example rule should make Claude qualify its plans with explicit example framing). Note: the slot is "manual activation" so a missed activation step is a likely failure mode — flag if `activate.sh` doesn't exist.

#### Sub-agent — `agent-example`
- [ ] **Install**: `claude plugin install agent-example@dgxsparklabs-marketplace --scope project`
- [ ] **Hands-on invocation**: in a `claude` session, dispatch the sub-agent with `/notebook-reviewer <input>` (or whatever the agent's slash name is per `agent-example/agents/notebook-reviewer.md` frontmatter).
- [ ] **Expected**: Claude spawns the sub-agent context and the sub-agent responds in role (skeptical peer reviewer of a lab notebook entry).
- [ ] **Diagnostic**: `claude plugin details agent-example` should list `notebook-reviewer` as a component.

#### Command — `command-example`
- [ ] **Install**: `claude plugin install command-example@dgxsparklabs-marketplace --scope project`
- [ ] **Hands-on invocation**: in a `claude` session, type the command's slash form (per `commands/example/commands/<name>.md` frontmatter, typically `/example-command`).
- [ ] **Expected**: command appears in the slash-command dropdown; invocation runs the command body.
- [ ] **Diagnostic**: `claude plugin details command-example | grep -F <command-slash-name>` matches.

#### Hook — `hook-example`
- [ ] **Install**: `claude plugin install hook-example@dgxsparklabs-marketplace --scope project`
- [ ] **Hands-on invocation**: trigger the hook's bound event (e.g., the `UserPromptSubmit` hook fires when you submit any prompt to Claude — submit any prompt and watch for the hook's observable side effect).
- [ ] **Expected**: hook executes (e.g., writes to a log file, prints to stderr, or otherwise reveals it ran). The exact observable depends on `hooks/example/hooks/hooks.json`.
- [ ] **Diagnostic**: `claude plugin details hook-example | grep -F UserPromptSubmit` matches the registered event.

#### MCP server — `mcp-example`
- [ ] **Install**: `claude plugin install mcp-example@dgxsparklabs-marketplace --scope project`
- [ ] **Hands-on invocation**: in a `claude` session, list available tools (Claude exposes MCP server tools as standard tools) — ask "what tools do you have?" or use one of the MCP-exposed tools.
- [ ] **Expected**: the MCP server's tools appear in Claude's tool surface.
- [ ] **Diagnostic**: `claude plugin details mcp-example | grep -iF mcp` matches.

#### LSP server — `lsp-example`
- [ ] **Install**: `claude plugin install lsp-example@dgxsparklabs-marketplace --scope project`
- [ ] **Hands-on invocation**: open a file in a language the LSP handles and observe Claude offering LSP-backed completions / diagnostics.
- [ ] **Expected**: LSP-backed features (hover, go-to-def, diagnostics) work for that language inside Claude.
- [ ] **Verification method UNKNOWN** if `lsp-example`'s LSP isn't actually configured for a real language — file is illustrative only. See follow-up.

#### Monitor — `monitor-example`
- [ ] **Install**: `claude plugin install monitor-example@dgxsparklabs-marketplace --scope project`
- [ ] **Hands-on invocation**: trigger the monitor's bound condition (e.g., file change, build failure) per `monitors/example/`.
- [ ] **Expected**: monitor fires its configured action.
- [ ] **Diagnostic**: `claude plugin list | grep -F monitor-example` confirms install.

#### Output style — `output-style-example`
- [ ] **Install**: `claude plugin install output-style-example@dgxsparklabs-marketplace --scope project`
- [ ] **Hands-on invocation**: in a `claude` session, switch to the new output style (per `output-styles/example/`'s slash command name, e.g. `/output-style example`) and ask Claude any question.
- [ ] **Expected**: Claude's reply format reflects the style's settings (formatting, verbosity, etc.).
- [ ] **Diagnostic**: `claude plugin details output-style-example` lists the style.

#### Theme — `theme-example`
- [ ] **Install**: `claude plugin install theme-example@dgxsparklabs-marketplace --scope project`
- [ ] **Hands-on invocation**: switch Claude's theme to the new one (per `themes/example/`'s slash command, e.g. `/theme example`) and observe terminal output color/styling change.
- [ ] **Expected**: terminal output uses the new theme's colors.
- [ ] **Diagnostic**: `claude plugin list | grep -F theme-example` confirms install.

### Specifically for THIS refactor

No Claude-side changes in 2026-05-25 refactor. If any of the above fails on `main` post-merge, that's a regression worth flagging. The lsp/monitor/output-style/theme cells are "thin coverage" historically — first hands-on QA in this revision. Bugs found there are more likely "longstanding" than "this-refactor regression."

### Cleanup

```bash
claude plugin uninstall skill-example --scope project
claude plugin uninstall rule-example --scope project
claude plugin uninstall agent-example --scope project
claude plugin uninstall command-example --scope project
claude plugin uninstall hook-example --scope project
claude plugin uninstall mcp-example --scope project
claude plugin uninstall lsp-example --scope project
claude plugin uninstall monitor-example --scope project
claude plugin uninstall output-style-example --scope project
claude plugin uninstall theme-example --scope project
claude plugin prune --scope project -y
claude plugin marketplace remove dgxsparklabs-marketplace
```

If hermetic (option A):
```powershell
docker rm -f qa-claude
```

---

## Platform 2: Codex

**What we're verifying**: marketplace registration + per-construct install for the four constructs Codex supports per `CodexPlatform.supports` and `docs/PLATFORMS.md` Codex "What constructs it supports": **skill, mcp, hook, sub-agent**. Codex also reads rule context from `AGENTS.md` and the Cursor/Windsurf rule mirrors. **New in 2026-05-25**: sub-agent emission as `.codex/agents/<name>.toml` (markdown→TOML converter) AND Phase 5.5 emits `.agents/plugins/marketplace.json` as Codex's canonical marketplace path.

### Setup option A: Docker (hermetic)

```powershell
docker run -it --name qa-codex node:20 bash
```

Inside the container (`node:20` has `git` pre-installed):
```bash
# Install Codex CLI
npm install -g @openai/codex
codex --version

# Clone the PR branch for testing PR #5:
git clone --branch fix/platform-emission-bugs https://github.com/DgxSparkLabs/marketplace.git /workspace/marketplace
cd /workspace/marketplace

# (To test against main instead: --branch main or omit --branch.)
```

### Setup option B: Native

```powershell
npm install -g @openai/codex
codex --version
```

### Auth

```bash
codex auth login         # OpenAI account; opens browser
```

Marketplace registration and `codex plugin list` are auth-free; `codex plugin add` typically requires auth.

### Marketplace registration

- [ ] Step 1: Register the marketplace. Pick ONE of:
  - **Remote `main`** (smoke test only — NOT for PR #5 verification; pre-fix `main` will trigger the C2 failure mode per `docs/PLATFORMS.md` Codex "Known gaps"):
    ```bash
    codex plugin marketplace add DgxSparkLabs/marketplace
    ```
  - **Remote PR branch** (recommended remote path — `--ref` is verified working per `docs/PLATFORMS.md` Codex "From GitHub (specific branch)" and `docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification.md` C3):
    ```bash
    codex plugin marketplace add DgxSparkLabs/marketplace --ref fix/platform-emission-bugs
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

### Per-construct verification

#### Skill — `skill-example`
- [ ] **Install**: `codex plugin add skill-example@dgxsparklabs-marketplace`
- [ ] **Hands-on invocation**: open a Codex session and ask it to use the skill:
  ```bash
  codex
  > use the example skill to send a test notification
  ```
- [ ] **Expected**: Codex recognizes the skill and invokes it (or describes how it would). Codex surfaces skills via the per-plugin `.codex-plugin/plugin.json` pointing at `./skills/`.
- [ ] **Diagnostic (only if hands-on fails)**: `codex plugin list | grep -F "skill-example"` shows STATUS = `installed`.

#### Sub-agent — `agent-example`
- [ ] **Install**: `codex plugin add agent-example@dgxsparklabs-marketplace`
  - **Expected**: install command succeeds.
- [ ] **Hands-on invocation** — open a Codex session and ask:
  ```bash
  codex
  > what subagents do we have available?
  ```
- [ ] **Expected**: `notebook-reviewer` (our sub-agent from `agent-example`) appears in the list alongside Codex's built-ins (`default`, `explorer`, `worker`).
- [ ] **🐛 KNOWN BUG (2026-05-25 QA)**: Codex does NOT currently surface our sub-agent. It lists only its three built-ins. The `.codex/agents/notebook-reviewer.toml` file emission is on disk (verified via `codex plugin list` ROOT path), but Codex's subagent loader isn't picking it up. Likely cause: TOML schema mismatch between what our `scripts/converters/md_to_toml.py` produces and what Codex expects. Needs investigation before this refactor's Codex sub-agent emission can claim "working." See "Known issues surfaced by QA" below.

#### Hook — `hook-example`
- [ ] **Install**: `codex plugin add hook-example@dgxsparklabs-marketplace`
- [ ] **Hands-on invocation**: trigger the hook's bound event inside a `codex` session (whichever event the hook subscribes to in `hooks/example/hooks/hooks.json`).
- [ ] **Expected**: hook fires its configured action. The per-plugin manifest emits `"hooks": "./hooks/hooks.json"` per `CodexPlatform.build_plugin_json`.
- [ ] **Verification method UNKNOWN** for Codex hook enumeration — Codex has no `codex hooks list` command captured in our docs. Hook firing is the only observable. See follow-up.

#### MCP server — `mcp-example`
- [ ] **Install**: `codex plugin add mcp-example@dgxsparklabs-marketplace`
- [ ] **Hands-on invocation**: in a `codex` session, list MCP tools or invoke one of the example MCP's tools.
  ```bash
  codex mcp list
  ```
- [ ] **Expected**: `mcp-example` (or its server name) appears in the MCP server list, OR Codex exposes the MCP's tools in-session.
- [ ] **Note**: Codex also accepts manually-added MCP servers via `codex mcp add` — verify our plugin-installed MCP is enumerated separately from any test MCPs added by hand.

#### Rule (no native install, file-discovery only) — `rule-example`
- [ ] **Setup**: this is N/A as a Codex-native install path. Codex reads rules from `AGENTS.md`, `.cursor/rules/*.md`, `.windsurf/rules/*.md` natively. Verify by opening Codex inside the workspace you cloned in setup:
  ```bash
  cd /workspace/marketplace   # already on fix/platform-emission-bugs from setup
  codex
  > what rules currently apply to your behavior?
  ```
- [ ] **Expected**: Codex describes rules from `.cursor/rules/` and `.windsurf/rules/` as active context (the rule mirrors are present after `uv run scripts/generate_manifest.py`).
- [ ] **Verification method UNKNOWN** — Codex has no documented "list active rules" command; this is qualitative. See follow-up.

### Specifically for THIS refactor

The whole `.codex/agents/<name>.toml` path is new. If the hands-on sub-agent test shows `notebook-reviewer` is invisible to Codex, that confirms the known bug above. If it DOES surface (i.e., the bug got fixed), update this doc.

Phase 5.5's `.agents/plugins/marketplace.json` is also new — Step 2 of marketplace registration is the verification (the ROOT path).

### Cleanup

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

## Platform 3: Gemini

**What we're verifying**: extension install from GitHub URL, plus per-construct verification for the three constructs Gemini supports per `GeminiPlatform.supports` and `docs/PLATFORMS.md` Gemini "What constructs it supports": **skill, sub-agent, hook**. **New in 2026-05-25**: sub-agent emission at `.gemini/agents/<name>.md` AND hook emission at `.gemini/hooks/hooks.json`.

### Setup option A: Docker (hermetic)

```powershell
docker run -it --name qa-gemini node:20 bash
```

Inside the container (`node:20` has `git` pre-installed):
```bash
# Install Gemini CLI
npm install -g @google/gemini-cli
gemini --version

# Clone the PR branch for testing PR #5:
git clone --branch fix/platform-emission-bugs https://github.com/DgxSparkLabs/marketplace.git /workspace/marketplace
cd /workspace/marketplace

# (To test against main instead: --branch main or omit --branch.)
```

### Setup option B: Native

```powershell
npm install -g @google/gemini-cli
gemini --version
```

### Auth

```bash
gemini auth login        # Google OAuth; needs browser
```

### Extension install

- [ ] Step 1: Install the marketplace extension. Pick ONE of:
  - **Remote `main`** (smoke test only — NOT for PR #5 verification, since `main` doesn't yet have the Gemini hook/sub-agent fixes):
    ```bash
    echo "y" | gemini extensions install https://github.com/DgxSparkLabs/marketplace --consent
    ```
  - **Remote PR branch** (recommended remote path — `--ref` is verified working per `docs/PLATFORMS.md` Gemini "From GitHub (specific branch)"; CI uses this same pattern via `compat-extension.yml`):
    ```bash
    echo "y" | gemini extensions install https://github.com/DgxSparkLabs/marketplace --ref fix/platform-emission-bugs --consent
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

### Per-construct verification

#### Skill — `skill-example`
- [ ] **Install**: covered by the extension install above (Gemini installs all skills as part of the extension).
- [ ] **Hands-on invocation**: in a `gemini` session, ask Gemini to invoke the skill:
  ```bash
  gemini
  > use the example skill to send a test
  ```
- [ ] **Expected**: Gemini recognizes the skill and executes it (or asks for needed params).
- [ ] **Diagnostic**: `gemini skills list --all 2>&1 | grep -F example` matches.

#### Sub-agent — `agent-example`
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

#### Hook — `hook-example`
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

### Specifically for THIS refactor

Sub-agent and hook emission to Gemini is new. The `/agents` hands-on test (NOT just file existence) is the only way to verify the platform actually loads what we ship. The file-existence check is diagnostic — useful only if the hands-on test fails. The hook hands-on test is currently bottlenecked by no hooks-list command — flag this as a verification-gap to research.

### Cleanup

```bash
gemini extensions uninstall DgxSparkLabs__marketplace
# (name shown by `gemini extensions list 2>&1` is the canonical form)
```

If hermetic:
```powershell
docker rm -f qa-gemini
```

---

## Platform 4: Cursor (IDE + CLI)

Cursor has two distinct surfaces — the **IDE** (GUI, in-editor `/add-plugin`) and the **CLI** (binary name is `agent`, no plugin install commands). Per the locked D-9 decision and `docs/PLATFORMS.md` Cursor "Discovery commands" + "Known gaps", both surfaces share the same `CursorPlatform` emission (`.cursor/rules/`, `.cursor/agents/`, per-plugin `.cursor-plugin/plugin.json`). The IDE installs via UI gesture; the CLI consumes from filesystem only.

**What we're verifying**: per-construct install on the IDE side for **rule, skill, sub-agent, command, hook, MCP** (`CursorPlatform.supports`), plus filesystem-discovery verification on the CLI side (populated either by Dashboard import, a `/add-plugin` in the IDE, or — on the CLI — by the `agents` cross-platform CLI).

### Cursor IDE

**Docker is NOT applicable** — Cursor IDE is a GUI, not headless.

Native install:
- Download installer from `cursor.com/download`
- Run the Windows installer, complete first-run setup
- Sign in via the app's UI

#### Marketplace registration paths

**Three install sources are possible for Cursor IDE**, varying by surface (in-editor `/add-plugin` vs Dashboard team-marketplace import) and source (remote main / remote branch / local clone). For PR #5 verification, **the local-clone path is the most reliable** because it tests the exact bytes of the PR (the hook + skill-manifest fixes in this PR write to `.cursor/*.json` and `.cursor/rules/`, both of which Cursor IDE picks up from a locally-opened workspace).

- [ ] **Path A — In-editor `/add-plugin` (remote)**:
  - Open any test repo in Cursor (a scratch dir is fine)
  - **Remote `main`**: in Cursor's chat panel, run `/add-plugin <plugin-name>@https://github.com/DgxSparkLabs/marketplace` — see per-construct tests below.
  - **Remote PR branch (UNTESTED)**: the form `/add-plugin <plugin-name>@https://github.com/DgxSparkLabs/marketplace?ref=fix/platform-emission-bugs` MAY work but is not documented in Cursor's published docs and not verified in this repo's evidence. If you can confirm or refute it, please report — see the open-questions section at the bottom of this doc.
  - **❗ Do NOT use the naked-URL form** (`/add-plugin https://github.com/DgxSparkLabs/marketplace`). It sends Cursor's chat agent into a research spiral — it goes off investigating the repo instead of installing. The `<plugin-name>@<url>` form goes straight to the install UI without involving the chat agent.

- [ ] **Path B — Dashboard team-marketplace import** (admin path; verify once):
  - Visit `cursor.com/dashboard` → Settings → Plugins → Import
  - **Remote `main`**: paste `https://github.com/DgxSparkLabs/marketplace` and save
  - **Remote PR branch**: the Dashboard UI exposes a branch selector — pick `fix/platform-emission-bugs` (per `docs/PLATFORMS.md` Cursor "From GitHub (specific branch)": "Branch selection happens in the dashboard").
  - **Expected**: marketplace appears in the team marketplace list, all Cursor-supported plugins enumerated.

- [ ] **Path C — Local clone** (recommended for PR #5 verification):
  - On the host (Cursor IDE is GUI, so Docker doesn't apply), clone the PR branch:
    ```powershell
    git clone --branch fix/platform-emission-bugs https://github.com/DgxSparkLabs/marketplace.git C:\Users\devic\source\marketplace-pr5
    ```
  - Open `C:\Users\devic\source\marketplace-pr5` in Cursor (File → Open Folder).
  - Cursor picks up `.cursor/rules/*.md`, `.cursor/agents/*.md`, `.cursor/hooks.json`, `.cursor/mcp.json`, and per-plugin `.cursor-plugin/plugin.json` files from the opened workspace. This is the path that exercises THIS PR's hook + skill-manifest fixes most directly — no marketplace registration needed; Cursor reads workspace files natively.

#### Per-construct verification (IDE)

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

### Cursor CLI (`agent` binary)

**What we're verifying**: Cursor CLI (the `agent` binary) consumes from filesystem only — there's no `agent plugin install`, no marketplace registration command (per `docs/PLATFORMS.md` Cursor "Known gaps"). Populate `.agents/` and `.cursor/` paths via the cross-platform `agents` CLI, then verify the Cursor CLI sees them.

Because the CLI reads only workspace files, **"branch selection" reduces to "which branch you cloned."** There is no remote-main vs remote-branch distinction for the CLI — clone the branch you want to test and open it.

#### Setup

```bash
# macOS/Linux/WSL
curl https://cursor.com/install -fsS | bash

# Windows PowerShell
irm 'https://cursor.com/install?win32=true' | iex

# Verify
agent --version    # expected: e.g., 2026.05.20-2b5dd59

# For PR #5 verification, clone the PR branch and cd into it:
git clone --branch fix/platform-emission-bugs https://github.com/DgxSparkLabs/marketplace.git /workspace/marketplace
cd /workspace/marketplace
```

#### Per-construct verification (CLI)

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

### Specifically for THIS refactor

Cursor IDE gained FOUR new construct types this refactor (sub-agents, commands, hooks, MCP). Sub-agent has a positive confirmation; the other three have UNKNOWN verification methods because Cursor's enumeration surface for these isn't documented.

The Cursor CLI per-construct tests are a forward-looking shape — the CLI's verification methods aren't fully mapped yet. UNKNOWN cells should fuel the next research round.

### Cleanup

Uninstall each plugin via Cursor IDE's UI:
- Settings → Plugins → click each → Remove
- Remove the marketplace from Settings → Plugins → Import list

For the CLI scratch project:
```bash
cd .. && rm -rf scratch-cursor-cli
```

---

## Platform 5: Windsurf

**What we're verifying**: rule + hook discovery, plus skill auto-discovery from `.agents/skills/`. Per `WindsurfPlatform.supports` and `docs/PLATFORMS.md` Windsurf "What constructs it supports": **rule, hook**, and skills via the `.agents/skills/` cross-platform path. **New in 2026-05-25**: hook emission at `.windsurf/hooks.json`.

### Setup

**Docker NOT applicable** — Windsurf is GUI-only, no CLI exists.

Native install:
- Download from `codeium.com/windsurf` → run the Windows installer
- Sign in via the app's UI (Codeium account)

### Populating the workspace

Windsurf reads from the filesystem only — no install command, no marketplace registration. "Branch selection" reduces to "which branch you cloned." Either:

1. **Clone the PR branch** (recommended for PR #5 verification — this is what tests THIS PR's hook fixes at `.windsurf/hooks.json`):
   ```bash
   git clone --branch fix/platform-emission-bugs https://github.com/DgxSparkLabs/marketplace.git C:\Users\devic\source\marketplace-pr5
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

### Per-construct verification

#### Skill — `skill-example` (read via `.agents/skills/`)
- [ ] **Hands-on invocation**: in Windsurf, open Cascade and type `@skill-example`.
- [ ] **Expected**: Cascade recognizes the `@skill-X` syntax and uses the skill — auto-discovered from `.agents/skills/example/SKILL.md` per `docs/PLATFORMS.md` Windsurf "Discovery paths".
- [ ] **Alternative hands-on**: ask Cascade "list the skills you have available" — `example` should appear.

#### Rule — `rule-example`
- [ ] **Hands-on invocation**: ask Cascade for an action the rule should affect (e.g., a refactor where example reasoning would change the recommendation).
- [ ] **Expected**: Cascade's reply reflects the rule's framing. Rule discovered from `.windsurf/rules/example.md` (with the required `trigger:` frontmatter — `always_on` for `example` per the source `rule.md`).
- [ ] **Diagnostic**: confirm `.windsurf/rules/example.md` exists in the workspace.

#### Hook — `hook-example`
- [ ] **Hands-on invocation**: trigger the hook's bound Cascade event (per `hooks/example/hooks/hooks.json`'s event subscription).
- [ ] **Expected**: hook fires its configured action.
- [ ] **🛑 Verification method UNKNOWN**: Windsurf has no CLI to enumerate registered hooks. Per `docs/PLATFORMS.md` Windsurf "Known gaps", verification today is qualitative — observe the side effect or check Cascade behavior. See follow-up.
- [ ] **Diagnostic**: `.windsurf/hooks.json` present at the workspace root (Windsurf-specific path — no `hooks/` subdir, unlike Gemini).

### Specifically for THIS refactor

Hook emission to `.windsurf/hooks.json` is new in 2026-05-25. With no Windsurf CLI for introspection, the only verification path is "trigger the event and observe behavior change" — which depends on the example hook being interactive enough to observe. This is a known coverage gap, not a bug in the emission itself.

### Cleanup

Nothing to uninstall on the platform side — Windsurf reads from the repo's filesystem. Close the project to "uninstall." If you used a scratch dir:
```bash
cd .. && rm -rf scratch-windsurf
```

---

## Platform 6: Devin

**What we're verifying**: skill discovery from `.agents/skills/`, rule discovery from `.windsurf/rules/` + `.cursor/rules/` (per `DevinPlatform.supports = {SkillConstruct}` and `docs/PLATFORMS.md` Devin "What constructs it supports" + "Discovery paths"), and MCP CLI surface. **New in 2026-05-25**: `.devin/skills/` mirror retired (now uses `.agents/skills/`).

### Setup option A: Docker (hermetic)

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
git clone --branch fix/platform-emission-bugs https://github.com/DgxSparkLabs/marketplace.git /workspace/marketplace
cd /workspace/marketplace

# (To test against main instead: --branch main or omit --branch.)
```

### Setup option B: Native (WSL or Git Bash)

```bash
# Inside WSL or Git Bash:
curl -fsSL https://cli.devin.ai/install.sh | bash || true
devin --version
```

### Auth

```bash
devin auth login         # Codeium/Windsurf login; opens browser
```

(Discovery commands are auth-free; `auth login` is only needed for actual Devin agent sessions.)

### Populating the workspace

For Docker setup: already done above by the `git clone --branch` step. Just confirm you're in the clone:
```bash
cd /workspace/marketplace && pwd
```

For native setup (WSL/Git Bash), clone the branch you want to test:
```bash
git clone --branch fix/platform-emission-bugs https://github.com/DgxSparkLabs/marketplace.git ~/marketplace-pr5 && cd ~/marketplace-pr5
# Or: omit --branch fix/platform-emission-bugs to clone main for a smoke test.
```

### Per-construct verification

#### Skill — `skill-example` (read via `.agents/skills/`)
- [ ] **Hands-on invocation**: `devin skills list`
- [ ] **Expected**: lists 27 skills from `.agents/skills/` (since `.devin/skills/` was retired this round). `example` is one of them. Output format per `docs/PLATFORMS.md` Devin "Discovery commands": `/<slash-command> [triggers] (path) - description`.
- [ ] **Hands-on (dispatching the skill)**: in a `devin` session, ask Devin to use the skill.
- [ ] **Diagnostic**: `devin skills paths` should mention `.agents/skills/` AND `~/.agents/skills/` (user scope) — `.devin/skills/` should be ABSENT (the legacy mirror was retired per D-1).
- [ ] **Hands-on (show)**: `devin skills show example` — prints the skill body.

#### Rule — `rule-example` (read via `.windsurf/rules/`, `.cursor/rules/`)
- [ ] **Hands-on invocation**: `devin rules list`
- [ ] **Expected**: rules listed with provider tags (`Cursor`, `Windsurf`, `Standard`) per `docs/PLATFORMS.md` Devin "Discovery commands". `example` appears tagged with both `Cursor` and `Windsurf` (it's mirrored to both `.cursor/rules/example.md` and `.windsurf/rules/example.md`).
- [ ] **Diagnostic**: `devin rules paths` lists `.windsurf/rules/*.md`, `.cursorrules`, `.cursor/rules/*.md`.
- [ ] **Hands-on (show)**: `devin rules show example` — prints the rule body.

#### MCP — Devin-managed (no marketplace-emitted Devin MCP config)
- [ ] **Hands-on invocation**: `devin mcp list`
- [ ] **Expected**: empty-state `No MCP servers configured` (or any MCPs you've manually added). The marketplace does not emit a Devin-native MCP config today; this test is "Devin's MCP surface still works alongside our marketplace clone."
- [ ] **Optional**: `devin mcp add example-fetch -- uvx mcp-server-fetch && devin mcp list | grep -i example-fetch`
- [ ] **Expected**: manual add + grep both succeed.

### Specifically for THIS refactor

The `.devin/skills/` mirror was retired. If `devin skills list` returns ZERO skills, the `.agents/skills/` fallback isn't working as expected (regression). Also confirm `.devin/skills/` is ABSENT in the workspace tree (`ls -la .devin/` should show no `skills/` subdir).

### Cleanup

If hermetic:
```powershell
docker rm -f qa-devin
```

If native:
- `devin auth logout` if you want to clear creds
- Delete the scratch clone

---

## Platform 7: `agents` CLI (the new cross-platform shim)

**What we're verifying**: the new `agents` CLI installs cleanly, has the documented subcommand surface, respects `--scope project|user`, and the `--agents-only` flag actually restricts emission to `.agents/`. Per construct, the CLI should emit to `.agents/<construct>/<name>/` (project) or `~/.agents/<construct>/<name>/` (user).

### Setup option A: Docker (hermetic)

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
curl -fsSL https://raw.githubusercontent.com/DgxSparkLabs/marketplace/fix/platform-emission-bugs/install.sh | bash

# Path 3 — Remote PR branch via AGENTS_REF env var (install.sh from main, but clones the marketplace from the branch — see install.sh: `REF="${AGENTS_REF:-main}"`):
AGENTS_REF=fix/platform-emission-bugs curl -fsSL https://raw.githubusercontent.com/DgxSparkLabs/marketplace/main/install.sh | bash

# Path 4 — Local clone (most reliable — tests exactly the bytes at /workspace/marketplace):
git clone --branch fix/platform-emission-bugs https://github.com/DgxSparkLabs/marketplace.git /workspace/marketplace
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

### Setup option B: Native (Windows PowerShell)

```powershell
# Path 1 — Remote main:
irm https://raw.githubusercontent.com/DgxSparkLabs/marketplace/main/install.ps1 | iex

# Path 2 — Remote PR branch via AGENTS_REF env var:
$env:AGENTS_REF = 'fix/platform-emission-bugs'
irm https://raw.githubusercontent.com/DgxSparkLabs/marketplace/main/install.ps1 | iex

# Path 3 — Local clone (most reliable):
git clone --branch fix/platform-emission-bugs https://github.com/DgxSparkLabs/marketplace.git C:\Users\devic\source\marketplace-pr5
Set-Location C:\Users\devic\source\marketplace-pr5
powershell -ExecutionPolicy Bypass -File .\install.ps1

agents --version
```

**Expected**: a version string (e.g., `agents 0.1.0`). If `agents` is not recognized: the wrapper's install path (`$env:LOCALAPPDATA\agents\bin\agents.ps1` on Windows, `~/.local/bin/agents` on POSIX) didn't get added to `$PATH`. That's a real UX bug — flag it.

### Auth

None. The `agents` CLI clones the marketplace via git; no platform auth required.

### CLI surface verification

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

### Per-construct install verification

For every supported construct, install and verify the on-disk landing path. The matrix's TEST¹² cells live here — construct types for which `agents` is the emit surface but no platform reads `.agents/<type>/` natively (yet) are still tested for correct emission.

#### Skill — `skill-example`
- [ ] **Project install**: `agents install skill-example --scope project`
- [ ] **Verify path**:
  ```bash
  test -d .agents/skills/example && echo "agents YES"   # expected: agents YES
  test -f .agents/skills/example/SKILL.md && echo "skill YES"   # expected: skill YES
  ```
- [ ] **Hands-on (Cursor CLI or Windsurf consumes)**: the SKILL.md at `.agents/skills/example/` is what Cursor CLI and Windsurf read — see those platforms' per-construct sections for the consumption test.
- [ ] **Per-platform spray** (default): `ls .cursor/skills/example/ 2>/dev/null` may also exist if the CLI sprays to per-platform paths; verify it matches the expected default scope.

#### Rule — `rule-example`
- [ ] **Project install (strict `.agents/` only)**: `agents install rule-example --scope project --agents-only`
- [ ] **Verify**:
  ```bash
  test -f .agents/rules/example.md && echo "agents YES"   # expected: agents YES
  test -f .cursor/rules/example.md && echo "cursor YES"   # expected: NOTHING (no output) — --agents-only blocks per-platform spray
  test -f .windsurf/rules/example.md && echo "windsurf YES"   # expected: NOTHING
  ```
- [ ] **Hands-on**: the `.agents/rules/example.md` is forward-looking per `docs/PLATFORMS.md` "Per-platform manifest paths" + `docs/ARCHITECTURE.md` AgentsPlatform notes — no platform reads it natively today, but emission must be correct.

#### Sub-agent — `agent-example`
- [ ] **Project install**: `agents install agent-example --scope project`
- [ ] **Verify**:
  ```bash
  test -d .agents/agents/agent-example && echo "agents YES"   # expected: agents YES (if CLI emits to .agents/agents/)
  ```
- [ ] **Note**: per `docs/research/platform-feature-routing/RECOMMENDATION.md` adoption matrix, `.agents/agents/` is UNVERIFIED across all platforms — no platform reads it natively today. The CLI test is "emission lands at the right path." Consumption is via per-platform mirrors (`.cursor/agents/`, `.codex/agents/`, `.gemini/agents/`).
- [ ] **Per-platform spray**: `ls .cursor/agents/notebook-reviewer.md` should exist (default-scope spray), and that file IS consumed by Cursor IDE.

#### Command — `command-example`
- [ ] **Project install**: `agents install command-example --scope project`
- [ ] **Verify**:
  ```bash
  test -d .agents/commands/command-example && echo "agents YES"   # expected: agents YES
  ```
- [ ] **Note**: only Cursor (manifest-only) and Claude consume commands today. The `.agents/commands/` emission is forward-looking.

#### Hook — `hook-example`
- [ ] **Project install**: `agents install hook-example --scope project`
- [ ] **Verify**:
  ```bash
  test -d .agents/hooks/hook-example && echo "agents YES"   # expected: agents YES
  ```
- [ ] **Per-platform spray**: `.cursor/hooks.json`, `.windsurf/hooks.json`, `.gemini/hooks/hooks.json` may also exist depending on what the CLI sprays under default scope.

#### MCP — `mcp-example`
- [ ] **Project install**: `agents install mcp-example --scope project`
- [ ] **Verify**:
  ```bash
  test -d .agents/mcp-servers/mcp-example && echo "agents YES"   # expected: agents YES
  ```
- [ ] **Per-platform spray**: `.cursor/mcp.json` should also exist; Claude's plugin install handles the MCP wiring via the per-plugin manifest.

#### LSP — `lsp-example` (forward-looking)
- [ ] **Project install**: `agents install lsp-example --scope project`
- [ ] **Verify**:
  ```bash
  test -d .agents/lsp-servers/lsp-example && echo "agents YES"   # expected: agents YES
  ```
- [ ] **Note**: only Claude consumes LSP today. The `.agents/lsp-servers/` emission is forward-looking.

#### Monitor — `monitor-example` (forward-looking)
- [ ] **Project install**: `agents install monitor-example --scope project`
- [ ] **Verify**:
  ```bash
  test -d .agents/monitors/monitor-example && echo "agents YES"
  ```
- [ ] **Note**: Claude-only consumer.

#### Output style — `output-style-example` (forward-looking)
- [ ] **Project install**: `agents install output-style-example --scope project`
- [ ] **Verify**:
  ```bash
  test -d .agents/output-styles/output-style-example && echo "agents YES"
  ```
- [ ] **Note**: Claude-only consumer.

#### Theme — `theme-example` (forward-looking)
- [ ] **Project install**: `agents install theme-example --scope project`
- [ ] **Verify**:
  ```bash
  test -d .agents/themes/theme-example && echo "agents YES"
  ```
- [ ] **Note**: Claude-only consumer.

### Scope and flag verification

#### `--scope user` (writes to `~/.agents/` only per D-6)
- [ ] **Install**: `agents install rule-example --scope user`
- [ ] **Verify**:
  ```bash
  test -f "$HOME/.agents/rules/example.md" && echo "user YES"     # expected: user YES
  test -f "./.agents/rules/example.md" && echo "project YES"      # expected: NOTHING (user scope writes ONLY to ~/.agents/)
  ```

#### `--scope user` + `--agents-only` for sub-agent
- [ ] **Install**: `agents install agent-example --scope user --agents-only`
- [ ] **Verify**:
  ```bash
  test -d "$HOME/.agents/agents/agent-example" && echo "user YES"     # expected: user YES
  test -d "./.agents/agents/agent-example" && echo "project YES"      # expected: NOTHING
  test -f "$HOME/.cursor/agents/notebook-reviewer.md" && echo "user cursor YES"   # expected: NOTHING (--agents-only)
  ```

#### `agents list` (installed, not available)
- [ ] **Hands-on**: `agents list`
- [ ] **Expected**: shows all the installs from the per-construct tests above; distinguishes project vs user scope clearly.

#### `agents uninstall` cleans both per-platform AND `.agents/` paths
- [ ] **Uninstall**: `agents uninstall skill-example --scope project`
- [ ] **Verify**:
  ```bash
  test -d .agents/skills/example && echo "still there"     # expected: NOTHING
  test -d .cursor/skills/example && echo "still there"     # expected: NOTHING
  ```

### Specifically for THIS refactor

The CLI is brand new. Watch for:
- PATH not updated after install → UX bug
- Unclear error messages on bad input → polish issue
- Default scope (project) not surprising → matches D-13 Option C
- `--agents-only` actually skips per-platform paths → tests D-13 strict mode
- Constructs the CLI doesn't yet support (if any) → flag as scope gap

### Cleanup

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

## Master teardown

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

**Note on in-container clones**: if you used the `git clone --branch fix/platform-emission-bugs ... /workspace/marketplace` step inside the containers, those clones live entirely inside each container's writable layer. `docker rm -f` removes the container AND its writable layer in one shot — no separate cleanup step needed for the clones. (Confirm with `docker ps -a` after teardown — nothing labelled `qa-*` should remain, and the clones go with them.)

Native platforms (Cursor IDE / Windsurf IDE / native CLI installs) — uninstall via their respective uninstall flows or simply leave installed if you use them day-to-day. If you made native local clones (e.g., `C:\Users\devic\source\marketplace-pr5` for Cursor IDE or Windsurf), delete those directories when you're done:

```powershell
Remove-Item -Recurse -Force C:\Users\devic\source\marketplace-pr5
```

---

## Reporting findings

When you're done (or if something breaks mid-flow), capture:

1. **Which platform(s)** you tested and via which path (hermetic / native)
2. **Which cells in the matrix passed** as expected — useful to confirm what works
3. **Which cells failed** — and what you saw vs what was expected
4. **Which cells were UNKNOWN-method** — operator's notes on how they tried to verify, even if the method wasn't documented. These notes feed the next research round.
5. **Anything that felt wrong even if it "worked"** — confusing output, unclear errors, ambiguous flags, missing help text

A short report is fine — even a one-line summary per platform like "Cursor: agent + command + hook + MCP all visible in UI ✓; Gemini hook not auto-discovered ✗" is genuinely useful. With the expanded matrix, the per-cell granularity makes it easier to report a partial pass ("8/10 Claude cells PASS, lsp and monitor UNKNOWN-method").

If you'd prefer, file findings as GitHub issues against `DgxSparkLabs/marketplace` (one per finding so they can be triaged independently).

---

## Quick reference table

Assumes `/workspace/marketplace` is the clone path (Docker setups in each platform's section produce this). For the local-install column, "clone first" means the `git clone --branch fix/platform-emission-bugs ... /workspace/marketplace` step has already run.

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
| Codex | `codex plugin marketplace add DgxSparkLabs/marketplace --ref fix/platform-emission-bugs` |
| Gemini | `echo "y" \| gemini extensions install https://github.com/DgxSparkLabs/marketplace --ref fix/platform-emission-bugs --consent` |
| Cursor IDE | Dashboard branch picker (UI); `/add-plugin <name>@<url>?ref=<branch>` form untested |
| Cursor CLI | n/a — clone the branch and open |
| Windsurf | n/a — clone the branch and open |
| Devin | n/a — clone the branch and open |
| `agents` CLI | `AGENTS_REF=fix/platform-emission-bugs curl -fsSL https://raw.githubusercontent.com/DgxSparkLabs/marketplace/main/install.sh \| bash` |

---

*Maintain this doc alongside platform changes. If a platform's install method changes or a new emission lands, update the relevant section and the master matrix. The doc is canonical only if it stays accurate.*

---

## Known issues surfaced by QA (2026-05-25)

Discovered during the first hands-on QA pass of this doc. All three are real and reproducible.

### 🐛 Codex sub-agents not discovered

- **Symptom**: `codex plugin add agent-example@dgxsparklabs-marketplace` reports success; `codex plugin marketplace list` shows our marketplace; but `codex` interactive session lists only built-in subagents (`default`, `explorer`, `worker`) — not our `notebook-reviewer`.
- **State on disk**: `.codex/agents/notebook-reviewer.toml` emission exists per `scripts/converters/md_to_toml.py` (verified by `codex plugin list` ROOT column pointing at the canonical `.agents/plugins/marketplace.json`).
- **Hypothesis**: TOML schema produced by our converter doesn't match what Codex's subagent loader expects. Compare a working Codex-native subagent TOML (if available in Codex docs) against what we emit.
- **Scope to investigate**: `scripts/converters/md_to_toml.py` + Codex sub-agent docs at `developers.openai.com/codex/subagents/` (compare field names).

### 🐛 Gemini sub-agents not discovered

- **Symptom**: `gemini extensions install` succeeds; `gemini extensions list 2>&1` and `gemini skills list --all 2>&1` both show our content correctly (all 27 skills enumerated); but `/agents` in an interactive `gemini` session shows only built-ins (`codebase_investigator`, `cli_help`, `generalist`) — not our `notebook-reviewer`.
- **State on disk**: `~/.gemini/extensions/dgxsparklabs-marketplace/agents/notebook-reviewer.md` exists with valid frontmatter.
- **Hypothesis**: Either the file location inside the extension is wrong (Gemini may expect `agents/<name>/agent.md` not `agents/<name>.md`), or the frontmatter is missing a required field, or Gemini's agent loader is gated on a `gemini-extension.json` declaration we don't emit.
- **Scope to investigate**: `GeminiPlatform.emit` in `scripts/platforms.py` + Gemini extension reference docs at `geminicli.com/docs/extensions/reference/` (specifically the sub-agents section).

### 🐛 Cursor skill popup mangled metadata

- **Symptom**: After `/add-plugin skill-example@<url>` succeeds, typing `/example` (the skill's invocation name) in Cursor shows a popup with mangled fields — version string, commit SHA, and the description duplicated, instead of a clean description-only popup. (Originally observed during 2026-05-25 QA with `skill-telegram-notify` / `/telegram`; symptom reproduces with the example fixture.)
- **State on disk**: `.cursor/settings.json` is populated correctly with the plugin entry. The actual install path works.
- **Hypothesis**: Our `.cursor-plugin/plugin.json` for skills populates fields that Cursor's display layer renders in unexpected slots. Compare against a working Cursor-native skill plugin's manifest.
- **Scope to investigate**: `CursorPlatform.build_plugin_json` for SkillConstruct in `scripts/platforms.py` + Cursor plugin manifest reference at `cursor.com/docs/reference/plugins`.

### ✅ Cursor sub-agent (positive finding)

- **Symptom**: `/add-plugin agent-example@<url>` then `/notebook-reviewer` in Cursor → clean popup with correct description. Sub-agent invocation works as designed.
- **Implication**: Cursor's sub-agent format DOES match what we emit (`.cursor/agents/<name>.md` with YAML frontmatter). The Codex and Gemini bugs above are NOT a "we shipped a uniformly broken format" issue — Cursor accepts it. The other two platforms have format-or-discovery mismatches specific to each.

### Documentation/process improvements adopted in this doc revision

- **Claude verification uses `claude plugin ...` CLI form** (not `/plugin ...` slash commands), because the slash commands require the interactive Claude UI; the CLI is scriptable and works in headless containers.
- **Codex verification uses `codex plugin marketplace list`** (not `cat ~/.codex/config.toml | grep`), because the list command is the source of truth for what Codex actually registered.
- **Codex Step 4's clone+cat was deleted** as hollow verification (it inspected a file without invoking Codex — proved nothing about Codex's recognition of the path).
- **Hands-on subagent invocation** added for both Codex and Gemini (`codex` then ask for available subagents; `gemini` then `/agents`) because file-existence checks miss the discovery-loading bugs above.
- **Cursor `/add-plugin` uses `<name>@<url>` form** (not naked URL) because the naked URL triggers Cursor's chat agent into research-spiral mode instead of going to the install UI.
- **Round-2 (2026-05-25)**: per-construct grid expansion. Every cell in the master matrix has either a hands-on test, a documented N/A justification, or an UNKNOWN-method flag for follow-up research.

---

## Discrepancies and unknowns flagged during doc expansion

Surfaced while building the per-construct grid from `docs/PLATFORMS.md` + `docs/ARCHITECTURE.md` + `scripts/platforms.py`. Not for resolution in this doc — these are follow-up items.

### Discrepancies between source documents

- **`docs/PLATFORMS.md` Codex "What constructs it supports" table** lists `mcp: yes` with note "manifest emits `mcpServers`", but `docs/ARCHITECTURE.md` "The seven platform classes" row for `CodexPlatform` only lists "skill, mcp, hook, agent". Both agree on MCP, but PLATFORMS.md's note "no per-plugin MCP install command" suggests the consumption pattern is qualitatively different from skill — the matrix marks MCP as TEST but the operator should expect `codex mcp list` to be the only enumeration surface for Codex MCP, distinct from how skills are listed via `codex plugin list`.
- **`docs/PLATFORMS.md` Cursor "What constructs it supports"** marks command/hook/mcp as "manifest-only" (auto-discovered, no Phase 3 mirror) per `CursorPlatform.emit`. The CursorPlatform code at `scripts/platforms.py:283-308` confirms this — Command/Hook have no mirror branch. But `docs/PLATFORMS.md` doesn't document an enumeration surface for these inside Cursor, leaving the verification method UNKNOWN. Flag for follow-up.
- **Devin `supports` discrepancy**: `DevinPlatform.supports = {SkillConstruct}` per `scripts/platforms.py:386`, but `docs/PLATFORMS.md` Devin "What constructs it supports" lists rule and mcp as `yes (via Cursor/Windsurf mirrors)` and `yes` (CLI-managed). The `supports` set is "what gets a per-plugin Devin manifest emitted" — not "what Devin reads." The matrix treats this with footnote 6 (rule) and 16 (mcp); the operator should be aware these are read-via-other-mirrors, not Devin-native plugin install.

### Unknown verification methods (gaps for the next research round)

These are cells in the matrix marked TEST but where no clean hands-on verification command is documented for the platform:

- **Claude lsp / monitor / output-style / theme** — example plugins exist, but `lsp-example` etc. may not configure a real language/event, making the "Expected" observation unreliable. Hands-on test is best-effort; full coverage may require richer example plugins.
- **Codex hook enumeration** — no `codex hooks list` command captured in our docs. Hook firing is the only observable.
- **Codex rule activation surface** — no documented "list active rules" command. Rule presence is verified via filesystem; rule effect is qualitative.
- **Gemini hook enumeration** — no `gemini hooks list` command. File presence + JSON validity is the minimum signal.
- **Cursor IDE command / hook enumeration** — Cursor has no documented "list registered commands/hooks" surface for plugin-installed constructs.
- **Cursor CLI agent / command / hook dispatch** — `agent --help` (per `logs/CU3.txt`) lists `mcp`, `models`, `generate-rule`, but no plugin-construct subcommand.
- **Windsurf hook trigger** — no CLI for introspection; verification is "observe Cascade-triggered side effect."
- **`agents` CLI per-platform spray default behavior** — the per-construct project-scope tests assume the CLI's default mode sprays to `.cursor/`, `.windsurf/`, etc. alongside `.agents/`. The exact spray policy per construct type isn't fully documented; verify empirically.
- **Cursor `/add-plugin` with `?ref=<branch>` query parameter** — undocumented in Cursor's published docs; not verified in this repo's evidence. If you try `/add-plugin <name>@https://github.com/DgxSparkLabs/marketplace?ref=fix/platform-emission-bugs` in Cursor and observe whether it installs from the branch or silently falls back to default, report your finding. The Dashboard team-marketplace import flow has a separate branch-selector UI per `docs/PLATFORMS.md` Cursor "From GitHub (specific branch)" — that path is the verified one.

These gaps suggest the next research pass should focus on:
1. Per-platform enumeration commands for each construct type (especially Cursor command/hook/MCP listing, Codex hooks listing, Gemini hooks listing).
2. The `agents` CLI's default spray policy per construct type.
3. Whether `lsp-example`, `monitor-example`, `output-style-example`, `theme-example` example plugins are configured for observable end-to-end testing or are illustrative-only.
