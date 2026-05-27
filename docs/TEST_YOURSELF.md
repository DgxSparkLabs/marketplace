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

**What we're verifying**: marketplace registration + per-construct install for the **9 construct types** Claude supports (`ClaudeCodePlatform.supports` per `docs/PLATFORMS.md` Claude "What constructs it supports" — `RuleConstruct` was removed 2026-05-26 because rules are not a Claude plugin component per `code.claude.com/docs/en/plugins-reference#plugin-components-reference`). This is also the verification surface for the 2026-05-26 Claude QA fixes (marketplace description, LSP / monitor / theme / hook example fixes, `uv` prereq doc, rule emission retirement) — see the validation list below.

### Setup option A: Dev Container (recommended)

The repo ships `.devcontainer/` with everything pre-wired — Claude CLI, Node 20, Python 3.12, `uv`, Flask (for the hermetic stub), `git`, `gh`, plus VS Code extensions. See `.devcontainer/README.md` for the full inventory.

```text
1. Install Docker Desktop + the VS Code "Dev Containers" extension.
2. Open the repo in VS Code -> "Reopen in Container" when prompted.
3. First build runs .devcontainer/post-create.sh and prints what's installed + next steps.
4. Open a terminal inside VS Code (Ctrl+`). Run `claude` to sign in.
```

Forwarded ports: 8088 (F5 sentinel stub) and 8089 (F7/F9 body-dumper stub). Claude config persists across rebuilds via a named docker volume scoped to this repo's container ID.

### Setup option B: Docker (manual, hermetic)

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

### Setup option C: Native

```powershell
npm install -g @anthropic-ai/claude-code
claude --version
```

### Auth

Marketplace registration, listing, and install are auth-free (verified by `act`-based CI). `claude auth login` is only required if you actually use Claude for chat — not for the QA flow here.

### Hermetic Claude session (no auth required)

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

### Marketplace registration

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
  **Expected**: JSON array of **10** plugins (9 Claude-supported individuals + 1 cross-construct catalog bundle `bundle-examples`; rule individuals are excluded per F8, and per-construct catch-all bundles were retired 2026-05-27). If you see more, you're testing a pre-PR-#10 state.

- [ ] Step 4 — **enable-after-install gotcha**: empirically (`docs/research/naming-conventions-2026-05-26/logs/06-enable-qualified.log:1-9`), `claude plugin install` lands plugins in the *disabled* scope on first install. After installing any plugin in the per-construct cells below, you MUST run `claude plugin enable <plugin>@dgxsparklabs-marketplace` before invoking. The bare `<plugin>` form (without `@dgxsparklabs-marketplace`) errors with `Plugin "<name>" not found in any editable settings scope. Use plugin@marketplace format.` This is the single most likely cause of "I installed it but nothing happens" — flag it up front.

### Claude construct reference card — exact strings to type and expect

This table is the cheat sheet for the per-construct cells below. Every row was verified empirically in a Docker Claude session on 2026-05-26 (logs at `docs/research/naming-conventions-2026-05-26/logs/`). The marketplace name and the plugin.json name now agree across all 10 example plugins (post-Scheme-B+ alignment); the slash prefix in practice is `<construct>-example`.

| Construct      | Type to install                                                                | After install, `/plugins` shows               | Type to invoke                                                | Expected behavior on invoke                              |
|---             |---                                                                             |---                                            |---                                                            |---                                                       |
| skill          | `claude plugin install skill-example@dgxsparklabs-marketplace --scope project` | `skill-example@dgxsparklabs-marketplace`       | `/skill-example:lab-notebook [topic]` (or bare `/lab-notebook`) | Skill body renders a lab-notebook-style status block for the topic. |
| rule           | N/A — not a Claude plugin component as of 2026-05-26                            | (no entry)                                    | rule applies passively (no slash)                              | See Claude validation 8.                                  |
| sub-agent      | `claude plugin install agent-example@dgxsparklabs-marketplace --scope project` | `agent-example@dgxsparklabs-marketplace`       | `/agents` then select `agent-example:notebook-reviewer`        | Sub-agent dispatched as a skeptical peer reviewer of a lab notebook entry. |
| command        | `claude plugin install command-example@dgxsparklabs-marketplace --scope project` | `command-example@dgxsparklabs-marketplace`   | `/command-example:hello`                                       | Prints a formatted lab-notebook header for today's UTC date. |
| hook           | `claude plugin install hook-example@dgxsparklabs-marketplace --scope project`  | `hook-example@dgxsparklabs-marketplace`        | (passive — fires on events)                                    | Writes per-event sentinel files to `/tmp/hook-<event>-fired.log` for six event types. See validations 5a–5f. |
| MCP server     | `claude plugin install mcp-example@dgxsparklabs-marketplace --scope project`   | `mcp-example@dgxsparklabs-marketplace`         | `mcp__mcp-example__example__fetch` (tool, model-called)        | Claude can fetch URLs via the wrapped `mcp-server-fetch`. Requires `uv` on PATH. |
| LSP server     | `claude plugin install lsp-example@dgxsparklabs-marketplace --scope project`   | `lsp-example@dgxsparklabs-marketplace`         | (auto-attaches by file extension)                              | LSP loaded if the example points at a real server binary (illustrative only by default). |
| monitor        | `claude plugin install monitor-example@dgxsparklabs-marketplace --scope project` | `monitor-example@dgxsparklabs-marketplace`   | (passive — runs `disk-usage` monitor at session start)         | `df -h .` output appended once per session.                |
| output style   | `claude plugin install output-style-example@dgxsparklabs-marketplace --scope project` | `output-style-example@dgxsparklabs-marketplace` | `/output-style Lab Notebook Voice`                       | Subsequent Claude replies use measured, citation-focused prose. Persisted to `.claude/settings.local.json` `"outputStyle"`. |
| theme          | `claude plugin install theme-example@dgxsparklabs-marketplace --scope project` | `theme-example@dgxsparklabs-marketplace`       | `/theme Lab Notebook`                                          | Terminal colors flip to the Lab Notebook palette (solarized-light-ish). F4 interactive cell. |

**Reading the slash columns**: the prefix is the marketplace/plugin name (they're aligned now), the suffix after `:` is the component's own name from inside the plugin. For skill, the SKILL.md `name:` is `lab-notebook` (post-Scheme-B+ rename — was `example-skill`); for sub-agent it's the frontmatter `name:` `notebook-reviewer`; for command it's the filename `hello.md`; for MCP it's the server key `example` from mcp-config.json; for output-style and theme it's the human-readable `name:` from the file's metadata, typed as the slash argument. The skill flat form `/lab-notebook` also resolves and bypasses the namespace.

**After-install enable step**: also flagged in setup Step 4. Every per-construct cell below has its own explicit `Enable` step. Skipping enable is the most common operator confusion.

**Interactive vs headless**: many Claude slash commands require an interactive TTY session and return `Unknown command` or `isn't available in this environment` when invoked via `claude --print` (headless). Cells below flag this per-construct. Specifically: `/mcp`, `/agents`, `/output-style <name>`, `/theme <name>` are all interactive-only — they can be exercised under `claude --print` only via the hermetic stub's request-body inspection, not via direct slash invocation. See `docs/research/naming-conventions-2026-05-26/logs/15-output-style-theme.log:2-7` for the empirical capture.

**Where do the names come from?** If you're staring at `/skill-example:lab-notebook` and wondering which file produced which segment: the plugin name (`skill-example`) is the construct prefix (`skill`, [`scripts/constructs.py:73`](../scripts/constructs.py)) + the source directory name (`example`, discovered via [`scripts/utils.py:33-41`](../scripts/utils.py) `scan_source_dir`); the marketplace suffix (`@dgxsparklabs-marketplace`) is [`MARKETPLACE.toml:12`](../MARKETPLACE.toml); the component name (`lab-notebook`) is the SKILL.md frontmatter `name:` field (operator-authored, e.g. `skills/example/SKILL.md` line 2). See [`ADDING_A_CONSTRUCT.md` § "Trace each fragment to its source"](./ADDING_A_CONSTRUCT.md#trace-each-fragment-to-its-source--claude-plugin-install-skill-notifydgxsparklabs-marketplace-byte-by-byte) for the full byte-by-byte breakdown of every fragment in `claude plugin install skill-notify@dgxsparklabs-marketplace`, including a diagram of which generator output file each fragment ends up in.

### Per-construct verification

Each test installs ONE plugin of the construct type, then invokes it. Per-construct cleanup is folded into the master cleanup block at the end.

#### Skill — `skill-example`

- [ ] **Install** (run in host shell or container shell):
  ```bash
  claude plugin install skill-example@dgxsparklabs-marketplace --scope project
  ```
- [ ] **Enable** (plugins land disabled on install per `docs/research/naming-conventions-2026-05-26/logs/06-enable-qualified.log`):
  ```bash
  claude plugin enable skill-example@dgxsparklabs-marketplace
  ```
- [ ] **Verify in `/plugins`**: row labeled `skill-example@dgxsparklabs-marketplace`, status `✔ enabled`.
- [ ] **Invoke** (canonical namespaced form; type in an interactive `claude` session):
  ```text
  /skill-example:lab-notebook weather
  ```
  Or the bare flat form (also resolves per `docs/research/naming-conventions-2026-05-26/logs/18-rename-proof.log:2-6`):
  ```text
  /lab-notebook weather
  ```
- [ ] **Expected visible output**: a markdown block formatted as a lab-notebook status entry — header with the topic, current UTC timestamp, and the skill's canned body text per `skills/example/SKILL.md`.
- [ ] **Slash-dropdown check**: typing `/skill-example` triggers autocomplete; you should see `/skill-example:lab-notebook` highlighted with the description from frontmatter: "Reference example. Echoes back a formatted lab-notebook-style status message…"
- [ ] **Failure signals**: (a) no `skill-example` entry in `/plugins` → install path broken; (b) `/skill-example:lab-notebook` returns "Unknown command" → namespacing broken or skill `name:` field changed; (c) slash resolves but body is empty → SKILL.md frontmatter parse error.
- [ ] **Diagnostic**:
  ```bash
  claude plugin details skill-example
  ls ~/.claude/plugins/cache/dgxsparklabs-marketplace/skill-example/
  ```
  `details` lists `lab-notebook` as a component; the cache dir is populated.

#### Rule — N/A for Claude (retired 2026-05-26)

- [ ] **No Claude plugin install path for rules.** Per `code.claude.com/docs/en/plugins-reference#plugin-components-reference` (fetched 2026-05-26), rules are not a Claude plugin component — they live in Claude's memory subsystem.
- [ ] **Manual install (filesystem)** — POSIX:
  ```bash
  mkdir -p .claude/rules
  cp rules/example/rule.md .claude/rules/example.md
  ```
  PowerShell:
  ```powershell
  New-Item -ItemType Directory -Force .claude/rules
  Copy-Item rules/example/rule.md .claude/rules/example.md
  ```
- [ ] **Verify**:
  ```bash
  diff rules/example/rule.md .claude/rules/example.md
  ```
- [ ] **Invoke**: rules are passive — no slash command. Start a `claude` session in the project; the rule's guidance becomes part of every system prompt.
- [ ] **Expected observable**: Claude's responses reflect the rule (e.g., the example rule's `When you are not sure, ask for confirmation` directive surfaces as cautious counterquestions in ambiguous cases).
- [ ] See Claude validation 8 below to confirm no `rule-*` plugins surface in Claude's marketplace listing post-deprecation.

#### Sub-agent — `agent-example`  *(invocation requires interactive Claude session — `/agents` is TUI-only)*

- [ ] **Install**:
  ```bash
  claude plugin install agent-example@dgxsparklabs-marketplace --scope project
  ```
- [ ] **Enable**:
  ```bash
  claude plugin enable agent-example@dgxsparklabs-marketplace
  ```
- [ ] **Verify in `/plugins`**: row labeled `agent-example@dgxsparklabs-marketplace`, status `✔ enabled`.
- [ ] **Invoke (interactive only)** — TTY picker, no headless equivalent per F7b. In a real `claude` session:
  ```text
  /agents
  ```
  Then select `agent-example:notebook-reviewer` from the picker.
- [ ] **Expected (per spec, not empirically captured in PR #10 research)**: `/agents` shows the entry `agent-example:notebook-reviewer` with description "Reviews a lab notebook entry as a skeptical peer reviewer…" After selection, the next user message routes to that sub-agent context, and the reply tone is critical-second-opinion not generic Claude. This is inferred from the namespacing convention; the Docker research did not exercise the TUI picker. Operator should verify and report deviations.
- [ ] **Failure signals**: (a) no `agent-example` entry in `/plugins` → install path broken; (b) `/agents` picker has no row matching → agent loader broken or frontmatter `name:` mismatch; (c) selection succeeds but response is generic Claude tone → sub-agent context not switching (regression of PR #5 fixes).
- [ ] **Diagnostic**:
  ```bash
  claude plugin details agent-example | grep -F notebook-reviewer
  ```

#### Command — `command-example`

- [ ] **Install**:
  ```bash
  claude plugin install command-example@dgxsparklabs-marketplace --scope project
  ```
- [ ] **Enable**:
  ```bash
  claude plugin enable command-example@dgxsparklabs-marketplace
  ```
- [ ] **Verify in `/plugins`**: row labeled `command-example@dgxsparklabs-marketplace`, status `✔ enabled`.
- [ ] **Invoke** (in any `claude` session — works in `--print` too):
  ```text
  /command-example:hello
  ```
- [ ] **Expected visible output**: Claude prints a markdown block in this shape (substituting today's UTC date for `<DATE>`):
  ```markdown
  ## <DATE> — Lab notebook entry

  ### Goal

  ### Observations

  ### Next steps
  ```
- [ ] **Slash-dropdown check**: typing `/command-example:` triggers autocomplete; you should see `/command-example:hello` with description "Reference example slash command. Prints a formatted lab-notebook header."
- [ ] **Failure signals**: (a) no `command-example` entry in `/plugins` → install broken; (b) `/command-example:hello` returns "Unknown command" → the rename from `example-command.md → hello.md` (PR #9) didn't propagate; (c) command runs but output is wrong shape → command file edited locally — re-check against `commands/example/commands/hello.md`.

#### Hook — `hook-example`

- [ ] **Install**:
  ```bash
  claude plugin install hook-example@dgxsparklabs-marketplace --scope project
  ```
- [ ] **Enable**:
  ```bash
  claude plugin enable hook-example@dgxsparklabs-marketplace
  ```
- [ ] **Verify in `/plugins`**: row labeled `hook-example@dgxsparklabs-marketplace`, status `✔ enabled`.
- [ ] **Invoke**: hooks are passive — they fire on Claude events. Per `hooks/example/hooks/hooks.json`, six events have hooks: `UserPromptSubmit`, `SessionStart`, `PreToolUse`, `PostToolUse`, `Stop`, `SessionEnd`. Trigger each by:
  - `UserPromptSubmit`: type any prompt and press Enter.
  - `SessionStart`: open a fresh `claude` session.
  - `PreToolUse` / `PostToolUse`: ask Claude to read a file — both fire on the `Read` tool call.
  - `Stop`: send the response that completes a turn.
  - `SessionEnd`: type `/exit` or press `Ctrl+D`.
- [ ] **Check sentinels** (run in a separate shell) — POSIX:
  ```bash
  ls /tmp/hook-*-fired.log
  ```
  PowerShell on Windows:
  ```powershell
  Get-ChildItem $env:TEMP\hook-*-fired.log
  ```
  Expect one file per event triggered.
- [ ] **Failure signals**: (a) sentinel file missing for a triggered event → that hook didn't fire; (b) sentinel exists but empty → hook ran but didn't write; (c) `UserPromptSubmit` hook silently injects context but operator sees no sentinel → may need to check `claude --debug` per F5 finding (operator-invisible by design).
- [ ] See Claude validations 5a–5f below for per-event hands-on cells.

#### MCP server — `mcp-example`  *(connection check and tool-call verification both require interactive Claude session)*

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
  claude plugin install mcp-example@dgxsparklabs-marketplace --scope project
  ```
- [ ] **Enable**:
  ```bash
  claude plugin enable mcp-example@dgxsparklabs-marketplace
  ```
- [ ] **Verify in `/plugins`**: row labeled `mcp-example@dgxsparklabs-marketplace`, status `✔ enabled`.
- [ ] **Verify in `/mcp` (interactive only)**: in a real `claude` session type:
  ```text
  /mcp
  ```
  Server `example` should appear with status `✓ Connected` (assuming `uv` present). If `uv` is missing, you'll see `plugin:mcp-example:example: uvx mcp-server-fetch - ✗ Failed to connect`. `/mcp` is a TUI command; it cannot be exercised under `claude --print`.
- [ ] **Exercise the tool (interactive)**: tools are model-called, not user-typed. Ask Claude:
  ```text
  fetch https://example.com and summarize the contents
  ```
  Watch the tool name in `claude --debug` output.
- [ ] **Expected tool name**: `mcp__mcp-example__example__fetch` (hook-matcher form) or `plugin:mcp-example:example` (CLI display form).
- [ ] **Failure signals**: (a) `/mcp` shows `✗ Failed to connect` with `uvx mcp-server-fetch` → `uv` not installed; (b) `/mcp` empty → server config not loaded — check `_generated/mcp-example/mcp-config.json` post-install; (c) tool invocation but model says "no fetch tool" → MCP namespace wrong (regression of the 2026-05-26 alignment).

#### LSP server — `lsp-example`

- [ ] **Install**:
  ```bash
  claude plugin install lsp-example@dgxsparklabs-marketplace --scope project
  ```
- [ ] **Enable**:
  ```bash
  claude plugin enable lsp-example@dgxsparklabs-marketplace
  ```
- [ ] **Verify in `/plugins`**: row labeled `lsp-example@dgxsparklabs-marketplace`, status `✔ enabled`.
- [ ] **Verify in `/plugin` LSP tab (if available)**: example LSP listed; `lsp-example` plugin contributing.
- [ ] **Invoke**: LSPs auto-attach by file extension per `lsp-config.json`'s `extensionToLanguage` map. Open a file matching one of the configured extensions in Claude.
- [ ] **Expected**: LSP-backed features (hover, go-to-definition, completion) work for that language.
- [ ] **Known limitation**: `lsp-example`'s config points at a placeholder server binary — the example is illustrative for the schema, not a working LSP. To verify end-to-end, copy the example to scaffold a real LSP plugin per `lsp-servers/example/README.md`. Reported as Verification gap.

#### Monitor — `monitor-example`

- [ ] **Install**:
  ```bash
  claude plugin install monitor-example@dgxsparklabs-marketplace --scope project
  ```
- [ ] **Enable**:
  ```bash
  claude plugin enable monitor-example@dgxsparklabs-marketplace
  ```
- [ ] **Verify in `/plugins`**: row labeled `monitor-example@dgxsparklabs-marketplace`, status `✔ enabled`.
- [ ] **Verify in `/plugin` Monitors tab (interactive)**: `disk-usage` monitor listed (renamed from `example-disk` on 2026-05-26 per Scheme B+).
- [ ] **Invoke**: monitors are passive — `disk-usage` runs `df -h .` once at session start per `monitors/example/monitors/monitors.json`. Start a fresh `claude` session.
- [ ] **Probe the monitor output** (interactive) — ask Claude:
  ```text
  what's our current disk usage?
  ```
- [ ] **Expected (per spec, not empirically captured)**: at session start, the model context receives the `df -h .` output as a monitor observation. Visible via `/plugin` Monitors tab or via the prompt above. The Docker research did not exercise the monitor at session start; this cell describes the expected behavior per the F3 fix and the monitors.json schema, but the operator is the first to verify end-to-end.
- [ ] **Failure signals**: (a) no `monitor-example` entry in `/plugins` → install broken; (b) Monitors tab empty → monitor loader broken or monitors.json schema mismatch (regression of F3); (c) monitor name shown as `example-disk` → rename didn't propagate post-regenerate.

#### Output style — `output-style-example`  *(invocation requires interactive Claude session — `/output-style` returns `Unknown command` in `--print`)*

- [ ] **Install**:
  ```bash
  claude plugin install output-style-example@dgxsparklabs-marketplace --scope project
  ```
- [ ] **Enable**:
  ```bash
  claude plugin enable output-style-example@dgxsparklabs-marketplace
  ```
- [ ] **Verify in `/plugins`**: row labeled `output-style-example@dgxsparklabs-marketplace`, status `✔ enabled`.
- [ ] **Invoke (interactive only)** — in a real `claude` session, type:
  ```text
  /output-style Lab Notebook Voice
  ```
  The argument is the human-readable `name:` from the output-style frontmatter — NOT the plugin name. The slash returns `Unknown command: /output-style` in `claude --print` mode (`docs/research/naming-conventions-2026-05-26/logs/15-output-style-theme.log:2-7`); hermetic verification uses request-body inspection instead — see Claude validation 9.
- [ ] **Refresh the session**:
  ```text
  /clear
  ```
- [ ] **Expected immediate confirmation**: Claude responds with a confirmation: "Output style set to: Lab Notebook Voice" (exact wording per Claude version).
- [ ] **Expected behavior change**: subsequent replies use measured, citation-focused prose with lab-notebook section markers (per `output-styles/example/output-styles/lab-notebook-voice.md` spec). Ask:
  ```text
  summarize what you just did
  ```
  Reply should have lab-notebook structure.
- [ ] **Verify persistence** — POSIX:
  ```bash
  cat .claude/settings.local.json
  ```
  PowerShell:
  ```powershell
  Get-Content .claude/settings.local.json
  ```
  Expect `"outputStyle": "Lab Notebook Voice"` (per `code.claude.com/docs/en/output-styles`, 2026-05-26).
- [ ] **Failure signals**: (a) no `output-style-example` entry in `/plugins` → install broken; (b) `/output-style Lab Notebook Voice` returns "Unknown output style" → frontmatter `name:` not exposed to Claude; (c) confirmation appears but settings.local.json unchanged → persistence broken.
- [ ] See Claude validation 9 below for hermetic verification.

#### Theme — `theme-example`  *(invocation requires interactive Claude session — `/theme` returns `isn't available in this environment` in `--print`)*

- [ ] **Install**:
  ```bash
  claude plugin install theme-example@dgxsparklabs-marketplace --scope project
  ```
- [ ] **Enable**:
  ```bash
  claude plugin enable theme-example@dgxsparklabs-marketplace
  ```
- [ ] **Verify in `/plugins`**: row labeled `theme-example@dgxsparklabs-marketplace`, status `✔ enabled`.
- [ ] **Invoke (interactive only)** — in a real `claude` session, type:
  ```text
  /theme Lab Notebook
  ```
  The argument is the `name` from `themes/example/themes/lab-notebook.json` — NOT the plugin name. The slash returns `isn't available in this environment` in `claude --print` mode (`docs/research/naming-conventions-2026-05-26/logs/15-output-style-theme.log:2-7`).
- [ ] **Expected visible output**: terminal colors flip to the Lab Notebook palette — solarized-light-ish: background `#fdf6e3`, foreground `#586e75`, Claude messages `#268bd2`, errors `#dc322f`. The change is immediate; no `/clear` needed.
- [ ] **Persistence check (format speculative)**:
  ```bash
  cat ~/.claude/settings.json | grep -i theme
  ```
  Should show some persisted theme reference (exact format unverified against PR #10 research; the schema may be `custom:theme-example:lab-notebook` per `code.claude.com/docs/en/plugins-reference#themes` but operator should confirm).
- [ ] **Failure signals**: (a) no `theme-example` entry in `/plugins` → install broken; (b) `/theme Lab Notebook` returns "Unknown theme" → theme JSON `name` field mismatch; (c) `/theme` succeeds but colors don't change → TTY paint issue (this is F4, the one cell that remains interactive-only — no hermetic verification possible).
- [ ] **F4 interactive cell**: this is the only Claude QA cell that cannot be verified hermetically — the stub doesn't drive TTY paint. Operator-eyes-on-screen required.

### Specifically for THIS refactor (cumulative Claude QA arcs through 2026-05-26)

Three landed arcs contributed Claude-side fixes that still need operator verification on every run:

- **Arc 1 (PR #6, 2026-05-26)**: 6 example-plugin bugs fixed (marketplace description, LSP/monitor/theme schemas, hook coverage, MCP uv prereq) + Claude rule emission retired. Findings F1–F9. Source research: `docs/archive/claude-qa-2026-05-26/RESEARCH.md`.
- **Arc 2 (PR #8, 2026-05-26)**: hermetic Claude stub at `tests/fixtures/claude-stub/` enables F5/F7/F9 to verify without auth; F4 (visual theme) still interactive-only. Source research: `docs/archive/claude-headless-qa-2026-05-26/RESEARCH.md`.
- **Arc 3 (PR #10, 2026-05-26)**: mcp-example name alignment + Scheme B+ across all 9 other example plugins + 2 component renames. Source research: `docs/research/naming-conventions-2026-05-26/RESEARCH.md`.

The validations below all remain live for every operator pass. Each is operator-runnable; "do X, observe Y" — no file-existence-only checks.

#### Claude validation 1 — marketplace description (F1)

- [ ] **Action** — from the marketplace repo root:
  ```bash
  claude plugin validate ./
  ```
  (or add `--strict` if your CLI version supports the flag)
- [ ] **Expected**: exit code 0; output contains `Validation passed`; the previously-seen `description: No marketplace description provided` warning is GONE.
- [ ] **CI gate**: `.github/workflows/compat-validate.yml` runs this on every PR and fails the build if ANY warning or error appears.

#### Claude validation 2 — lsp-example schema (F2)

- [ ] **Action**:
  ```bash
  claude plugin install lsp-example@dgxsparklabs-marketplace --scope project
  claude plugin enable lsp-example@dgxsparklabs-marketplace
  ```
  Then open or edit a `.md` file in a project with the plugin enabled.
- [ ] **Expected**: Claude surfaces `marksman` diagnostics (e.g., broken-link or heading warnings) inline; `/plugin` Errors tab shows no LSP errors. Pre-fix the `/plugin` Errors tab would show three validator errors complaining about `lspServers.command`, `lspServers.extensionToLanguage`, and `unrecognized_keys: ["example-markdown"]` (per F2 symptom block).

#### Claude validation 3 — monitor-example shape (F3)

- [ ] **Action**:
  ```bash
  claude plugin install monitor-example@dgxsparklabs-marketplace --scope project
  claude plugin enable monitor-example@dgxsparklabs-marketplace
  claude
  ```
  Watch the bottom-status / notification panel during the first 30 seconds.
- [ ] **Expected**: a notification appears with the `df -h .` disk usage summary, sourced from the `disk-usage` monitor (renamed from `example-disk` on 2026-05-26 per Scheme B+). Pre-fix `/plugin` Errors tab would show `Failed to load monitors ... expected array, received object`.

#### Claude validation 4 — theme-example distinctiveness (F4)

- [ ] **Action** — install + enable:
  ```bash
  claude plugin install theme-example@dgxsparklabs-marketplace --scope project
  claude plugin enable theme-example@dgxsparklabs-marketplace
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
  Should show `custom:theme-example:lab-notebook` per `code.claude.com/docs/en/plugins-reference#themes` (operator confirms exact format — see F4 caveat above).

#### Claude validation 5a — UserPromptSubmit hook firing (F5)

- [ ] **Hermetic verification** (run the stub session above first):
  ```bash
  rm -f /tmp/hook-fired-userpromptsubmit.log
  echo "test prompt" | claude --print
  test -s /tmp/hook-fired-userpromptsubmit.log && echo PASS
  ```
- [ ] **Expected (hermetic)**: exit 0; the sentinel file exists and contains a `<UTC-ISO-timestamp> userPromptSubmit fired` line.
- [ ] **Interactive**: with `hook-example` installed + enabled, submit any prompt in a `claude` session. In another terminal:
  ```bash
  tail /tmp/hook-fired-userpromptsubmit.log
  ```
- [ ] **Expected**: a new line in the form `<UTC-ISO-timestamp> userPromptSubmit fired` (the hook command writes the sentinel). The injected `[Lab Notebook context: timestamp=...]` line goes into Claude's prompt context — not visible at the operator terminal by design; `claude --debug` reveals it.

#### Claude validation 5b — SessionStart hook firing (F5)

- [ ] **Hermetic verification**:
  ```bash
  rm -f /tmp/hook-fired-sessionstart.log
  echo "x" | claude --print
  test -s /tmp/hook-fired-sessionstart.log && echo PASS
  ```
- [ ] **Expected (hermetic)**: exit 0; sentinel contains a `sessionStart fired` line. A fresh `claude --print` invocation is a fresh session, so SessionStart always fires.
- [ ] **Interactive**: restart `claude` in the project (exit + re-enter, or open a new session). In another terminal:
  ```bash
  tail /tmp/hook-fired-sessionstart.log
  ```
- [ ] **Expected**: a new line with the session-start timestamp.

#### Claude validation 5c — PreToolUse hook with matcher (F5)

- [ ] **Hermetic verification (partial)**: PreToolUse only fires when Claude returns a `tool_use` content block. The default `stub.py` returns text-only, so this hook does NOT fire under hermetic — extending the stub to emit a canned `Edit` tool_use block is future work. Use the interactive step for now.
- [ ] **Interactive** — ask Claude to edit any file, e.g.:
  ```text
  edit README.md and add a blank line at the bottom
  ```
  In another terminal:
  ```bash
  tail /tmp/hook-fired-pretooluse.log
  ```
- [ ] **Expected**: a line like `<UTC-ISO-timestamp> preToolUse Edit` (or `preToolUse Write`). The matcher `Write|Edit` in `hooks.json` gates which tool calls trigger this hook.

#### Claude validation 5d — PostToolUse hook firing (F5)

- [ ] **Hermetic verification (partial)**: same caveat as 5c — needs the stub to return a `tool_use` block. Use the interactive step.
- [ ] **Interactive**: same edit as 5c. After the tool call completes:
  ```bash
  tail /tmp/hook-fired-posttooluse.log
  ```
- [ ] **Expected**: mirror line right after the PreToolUse entry (`<ts> postToolUse Edit` or `postToolUse Write`).

#### Claude validation 5e — Stop hook firing (F5)

- [ ] **Hermetic verification**:
  ```bash
  rm -f /tmp/hook-fired-stop.log
  echo "x" | claude --print
  test -s /tmp/hook-fired-stop.log && echo PASS
  ```
- [ ] **Expected (hermetic)**: exit 0; sentinel contains a `stop fired` line. Stop fires at the end of every assistant turn, including the single stub turn.
- [ ] **Interactive**: ask Claude any question and wait for the response to complete. Then:
  ```bash
  tail /tmp/hook-fired-stop.log
  ```
- [ ] **Expected**: a new line per assistant turn.

#### Claude validation 5f — SessionEnd hook firing (F5)

- [ ] **Hermetic verification**:
  ```bash
  rm -f /tmp/hook-fired-sessionend.log
  echo "x" | claude --print
  test -s /tmp/hook-fired-sessionend.log && echo PASS
  ```
- [ ] **Expected (hermetic)**: exit 0; sentinel contains a `sessionEnd fired` line. `claude --print` always exits the session after one turn, so SessionEnd fires.
- [ ] **Interactive**: exit the Claude session (`/exit` or `Ctrl+D`). Then in a separate shell:
  ```bash
  tail /tmp/hook-fired-sessionend.log
  ```
- [ ] **Expected**: a final line with the session-end timestamp.

#### Claude validation 6 — mcp-example uv prerequisite (F6)

- [ ] **Action** — on a fresh host (no `uv` installed):
  ```bash
  claude plugin install mcp-example@dgxsparklabs-marketplace --scope project
  claude plugin enable mcp-example@dgxsparklabs-marketplace
  claude
  ```
  Then in the session, ask Claude to fetch a URL. Check `/plugin` Errors tab.
- [ ] **Pre-install-uv expected**: error in `/plugin` Errors tab — `plugin:mcp-example:example: uvx mcp-server-fetch - ✗ Failed to connect` (because `uvx` is not on PATH).
- [ ] **Then install uv** — POSIX:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
  PowerShell:
  ```powershell
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
  Restart the Claude session.
- [ ] **Post-install-uv expected**: `/plugin` shows `plugin:mcp-example:example: uvx mcp-server-fetch - ✓ Connected`. The fix is the README documenting this prereq (see `mcp-servers/example/README.md`).

#### Claude validation 7a — skill slash command namespacing (F7)

- [ ] **Hermetic verification** — with `command-example` installed + enabled and the body-dumper stub running on port 8089:
  ```bash
  export ANTHROPIC_BASE_URL=http://127.0.0.1:8089
  echo "/command-example:hello" | claude --print
  grep -F "/command-example:hello" /tmp/stub-bodies.log
  ```
- [ ] **Expected (hermetic)**: grep matches — the namespaced slash form reaches the request body, proving Claude resolved it client-side. (The skill-example body lives under the same namespacing convention.)
- [ ] **Interactive**: with `skill-example` installed, in a real `claude` session type:
  ```text
  /
  ```
  And read the autocomplete dropdown entry.
- [ ] **Expected**: the entry resolves to `/skill-example:lab-notebook` (the UI may show a shorter label, but the actual invocation is the namespaced form). Per `code.claude.com/docs/en/plugins` (2026-05-26): *"Plugin skills are always namespaced (like `/my-first-plugin:hello`) to prevent conflicts..."* The SKILL.md frontmatter `name:` was changed from `example-skill` to `lab-notebook` on 2026-05-26 per Scheme B+ to eliminate the doubled slash form.

#### Claude validation 7b — agent namespacing (F7)

- [ ] **Hermetic verification (partial)**: `/agents` is an interactive TUI command — there is no headless equivalent. The 7a hermetic check exercises the same client-side resolver code path, so a green 7a is strong evidence the namespacing infrastructure works for agents too. Use the interactive step for the agent-specific surface.
- [ ] **Interactive**: with `agent-example` installed + enabled, in a `claude` session type:
  ```text
  /agents
  ```
- [ ] **Expected**: the entry appears as `agent-example:notebook-reviewer` (no `/` prefix — the colon-namespaced form is what `/agents` displays).

#### Claude validation 7c — MCP tool namespacing (F7)

- [ ] **Hermetic verification (partial)**: same as 7b — `mcp__*` tool names only appear once Claude returns a `tool_use` block; the default stub doesn't. Future work to extend the stub. Use the interactive step.
- [ ] **Interactive**: with `mcp-example` installed + enabled, ask Claude:
  ```text
  fetch https://example.com
  ```
  Watch the tool name in `claude --debug` output.
- [ ] **Expected**: tool name appears as `mcp__mcp-example__example` (the hook-matcher form) or `plugin:mcp-example:example` (the CLI display form). Both are documented per `code.claude.com/docs/en/hooks` and `code.claude.com/docs/en/plugins-reference`.

#### Claude validation 8 — rule deprecation (F8)

- [ ] **Action**:
  ```bash
  claude plugin list --available --json | jq '.available | map(.name) | map(select(startswith("rule-"))) | length'
  ```
- [ ] **Expected**: `0` — no `rule-*` plugins are surfaced to Claude after the 2026-05-26 deprecation. Additionally, Claude-side bundle cascade: `bundle-quality-rules`, `bundle-workflow-rules`, `bundle-documentation-rules`, `bundle-environment-rules`, `bundle-notifications-rules`, and `bundle-rule-all` are also gone (their dependencies are no longer valid Claude plugins). They remain available to Cursor / Codex / Gemini / Windsurf.

#### Claude validation 9 — output style applied (F9)
- [ ] **Hermetic verification** (use `stub_body_dumper.py` on port 8089, `ANTHROPIC_BASE_URL=http://127.0.0.1:8089`): with `output-style-example` installed, the simplest injection path is `--append-system-prompt`:
  ```bash
  rm -f /tmp/stub-bodies.log
  claude --print --append-system-prompt "$(cat output-styles/example/output-styles/lab-notebook-voice.md)" "explain F9"
  grep -F "Lab Notebook Voice" /tmp/stub-bodies.log
  grep -F "Next:" /tmp/stub-bodies.log
  ```
- [ ] **Expected (hermetic)**: both greps match — the output-style content reaches the `system[]` array of the captured request body verbatim, which is the proof the style would be applied if a real model were behind the stub. The persistence-vs-application distinction (`/config` selection vs `--append-system-prompt` injection) can be tested separately by setting `outputStyle` in settings and re-running.
- [ ] **Action (interactive)**: with `output-style-example` installed, type `/config` in a `claude` session, navigate to **Output style**, pick "Lab Notebook Voice", and confirm.
- [ ] **Persistence check**: `cat .claude/settings.local.json | jq .outputStyle` returns `"Lab Notebook Voice"`.
- [ ] **Apply**: type `/clear` to force a fresh session that re-reads the system prompt.
- [ ] **Behavioral check**: ask Claude: *"Explain what the `_base_plugin_shape` function in `scripts/constructs.py` does."*
- [ ] **Expected response markers** (from the SKILL.md spec): plain factual sentences citing file paths and line numbers; no hedging language unless flagged as uncertainty; the response ends with one line tagged `Next:` proposing the immediate next checkable step. The `Next:` line is the cleanest binary signal — present means active, absent means not.
- [ ] **A/B compare**: in a separate clean session, set `outputStyle: "Default"`, ask the same question — observe no `Next:` line and more conversational tone.

### Cleanup

```bash
claude plugin uninstall skill-example --scope project
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
git clone --branch main https://github.com/DgxSparkLabs/marketplace.git /workspace/marketplace
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
  cd /workspace/marketplace   # already on main from setup
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
git clone --branch main https://github.com/DgxSparkLabs/marketplace.git /workspace/marketplace
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
git clone --branch main https://github.com/DgxSparkLabs/marketplace.git /workspace/marketplace
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
git clone --branch main https://github.com/DgxSparkLabs/marketplace.git /workspace/marketplace
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
git clone --branch main https://github.com/DgxSparkLabs/marketplace.git ~/marketplace-pr5 && cd ~/marketplace-pr5
# Or: omit --branch main to clone main for a smoke test.
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
- [ ] **Optional**: `devin mcp add example -- uvx mcp-server-fetch && devin mcp list | grep -i example`
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

### Setup option B: Native (Windows PowerShell)

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

**Note on in-container clones**: if you used the `git clone --branch main ... /workspace/marketplace` step inside the containers, those clones live entirely inside each container's writable layer. `docker rm -f` removes the container AND its writable layer in one shot — no separate cleanup step needed for the clones. (Confirm with `docker ps -a` after teardown — nothing labelled `qa-*` should remain, and the clones go with them.)

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
- **Cursor `/add-plugin` with `?ref=<branch>` query parameter** — undocumented in Cursor's published docs; not verified in this repo's evidence. If you try `/add-plugin <name>@https://github.com/DgxSparkLabs/marketplace?ref=main` in Cursor and observe whether it installs from the branch or silently falls back to default, report your finding. The Dashboard team-marketplace import flow has a separate branch-selector UI per `docs/PLATFORMS.md` Cursor "From GitHub (specific branch)" — that path is the verified one.

These gaps suggest the next research pass should focus on:
1. Per-platform enumeration commands for each construct type (especially Cursor command/hook/MCP listing, Codex hooks listing, Gemini hooks listing).
2. The `agents` CLI's default spray policy per construct type.
3. Whether `lsp-example`, `monitor-example`, `output-style-example`, `theme-example` example plugins are configured for observable end-to-end testing or are illustrative-only.
