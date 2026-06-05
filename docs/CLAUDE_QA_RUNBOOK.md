---
date: 2026-06-02
purpose: self-contained setup + QA runbook for the Claude plugin platform, driven by an automated agent through tmux (interactive) and claude --print (non-interactive)
audience: agent-operator (drives the Claude TUI from the host via docker exec ... tmux send-keys)
scope: Claude Code ONLY — the other platforms + the agents CLI live in docs/TEST_YOURSELF.md
status: live
source: distilled from docs/TEST_YOURSELF.md Section 4 (verified live 2026-06-01/02, claude CLI 2.1.159); cross-checked against the live src/ tree, the hermetic stub, and the dev container on 2026-06-02
---

# Claude Plugin Platform — Setup and QA Runbook

A standalone, copy-pasteable runbook for an **automated agent** to set up the environment and QA every Claude construct, two ways:

- **Interactive (tmux)** — you drive the live Claude TUI from the host with `docker exec <container> tmux send-keys` and read it back with `capture-pane`. This is the **primary, authoritative** method.
- **Non-interactive (headless)** — `claude --print` against a local hermetic stub. No Anthropic account needed, CI-friendly. This is the **no-auth alternative**; it does not cover every construct (see the coverage matrix in part 4).

This runbook is self-contained — you should not need to open `docs/TEST_YOURSELF.md` to follow it. The shared one-time setup is part 1; the per-construct QA cells are part 2 (one section per construct, each covering `-single` and `-multi`); teardown is part 3; quick-reference cards are part 4.

---

## 0. Read this first — the five rules that prevent every common mistake

These come from a controlled cold-read test (several fresh agents, one construct each — all passed, but they hit the same snags). Internalize them before driving anything.

1. **Trust machine signals, not the model's prose.** A capable model (Opus 4.x) narrates a lot — it will recite injected monitor data, describe a type error it spotted by *reading* (with no language server running), and propose "Next:" steps, all before your construct fires. None of that is proof. The real signal is always a **file, a settings write, a namespaced task header, or a source-tagged diagnostic** — never a sentence Claude wrote.

2. **The grey "ghost-suggestion" text is not your input, and `C-u` does NOT clear it.** After most turns the input box shows dimmed grey text (an autocomplete hint from history). It never submits on its own and never concatenates with your next command. Don't fight it — your `send-keys -l '<text>'` overwrites the line and the hint vanishes. (most cold-read agents wasted calls pressing `C-u`/`Escape` at it.)

3. **`capture-pane | tail -n N` lies — widen with scrollback, and read files for file-based proofs.** A freshly split pane or a chatty turn pushes the block you want above the visible tail. Always `capture-pane -p -t <pane> -S -30 | tail -n 20`, and when the proof is a file (hook sentinels, mcp proxy log, lsp input log) read the **file** directly with `bash -lc 'cat <file>'`.

4. **Make sentinel/persistence proofs causal — establish a control first.** The container is not a clean slate between runs: a theme/output-style may already hold your target value, and `SessionStart`/`Stop` hooks fire at launch *before* you act. Reset first (`rm -f /tmp/hook-fired-*.log`; or set a *different* theme, confirm it, then set the target) so the before→after change is one you caused.

5. **TUI menus open on a default tab/row you must navigate from.** `/agents` opens on the **Running** tab (`No subagents are currently running`) — that is not failure; press `Left` once to reach **Agents**. In `/config` and `/theme` the highlight starts on the *currently active* item, so capture the `❯` row first and compute the delta — never hardcode "press Down N times".

Bonus: **the container clock can lag the host.** Match the *shape* of timestamped output (`<UTC-ISO> <event> fired`, `pong @ <ts>`), never the literal date.

---

## 1. One-time setup (shared — do this once, then jump to any construct)

### 1.1 Host prerequisites

```powershell
# Windows host (PowerShell)
winget install Docker.DockerDesktop      # then launch Docker Desktop once to finish first-run setup
docker --version
docker run --rm hello-world              # should print "Hello from Docker!"
winget install OpenJS.NodeJS.LTS         # only needed for the Native path (1.2-C)
```

`uv` (the Python runner for the generator and the hermetic stub) is installed *inside* the container in the steps below; you do not need it on the host.

### 1.2 Bring up the Claude environment — pick ONE

**A. Dev Container (recommended).** The repo ships `.devcontainer/` pre-wired with `claude`, Node 20, Python 3.12, `uv`, `git`, `gh`, and the Claude VS Code extension. Ports **8088** (sentinel stub) and **8089** (body-dumper stub) are forwarded. Claude's auth persists across rebuilds via a named docker volume scoped to this repo.

```text
1. Install Docker Desktop + the VS Code "Dev Containers" extension.
2. Open the repo in VS Code -> "Reopen in Container".
3. First build runs .devcontainer/post-create.sh (a few minutes) and prints what's installed.
4. Open a terminal inside VS Code (Ctrl+`). Run `claude` to sign in (only if you want a real model; the stub path needs no sign-in).
```

**B. Manual Docker (hermetic, bind-mount).** A one-off container with no VS Code. It bind-mounts your working tree, so whatever branch you have checked out on the host is what the container tests — no `git clone` step.

```powershell
# From the marketplace repo root on the host (PowerShell)
docker run --rm -it --name qa-claude `
  -v "${PWD}:/workspace/marketplace" `
  -w /workspace/marketplace `
  node:20 bash
```

```bash
# POSIX equivalent
docker run --rm -it --name qa-claude \
  -v "$PWD:/workspace/marketplace" \
  -w /workspace/marketplace \
  node:20 bash
```

Then, inside the container, install the two things `node:20` lacks:

```bash
# 1. Claude CLI
npm install -g @anthropic-ai/claude-code
claude --version

# 2. uv (needed by the mcp/lsp constructs and the hermetic stub)
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv --version
```

No separate Flask install — the stub uses PEP 723 inline metadata, so `uv run` fetches Flask on first invocation.

**C. Native.** `npm install -g @anthropic-ai/claude-code` on the host. Use only if you already work this way; the tmux-driving commands below assume a container named `qa-claude`.

### 1.3 The hermetic stub (required only for the non-interactive path)

The stub is a ~90-line Flask server that pretends to be the Anthropic Messages API, so `claude` runs with no account. Hooks fire before the API call, slash commands resolve client-side, and output-style content lands verbatim in the request body — all observable from sentinels + captured bodies. (A theme's color flip is a TTY paint with no request-stream observable, so it stays interactive-only.)

Two stub files, two jobs:

| File | Port | Use for |
|---|---|---|
| `tests/fixtures/claude-stub/stub.py` | `8088` | Hook firing + slash resolution — sentinel files + access log are enough |
| `tests/fixtures/claude-stub/stub_body_dumper.py` | `8089` | Output-style + slash-body capture — writes every request body to `/tmp/stub-bodies.log` for grepping |

**Simplest path — run the stub inside `qa-claude`:**

```bash
# Pick stub.py (sentinels) OR stub_body_dumper.py (captured bodies). Example uses stub.py:
uv run tests/fixtures/claude-stub/stub.py > /tmp/stub-server.log 2>&1 &
sleep 1                                          # wait for Flask to bind
export ANTHROPIC_BASE_URL=http://127.0.0.1:8088  # use :8089 for the body dumper
export ANTHROPIC_AUTH_TOKEN=stub                 # any non-empty value
export API_TIMEOUT_MS=20000                       # fail fast on stub bugs
```

Now any `claude --print` invocation routes through the stub. CI runs the same recipe in `.github/workflows/compat-headless-claude.yml`.

**Optional — dockerized stub with bind-mounted logs** (captured bodies land on the host so you can `grep`/`tail -f` them without exec'ing in). Two containers; `qa-claude` joins the stub's network namespace so `127.0.0.1:8089` inside it *is* the stub:

```bash
docker build -t claude-stub tests/fixtures/claude-stub/          # once
mkdir -p .stub-logs
docker run --rm -d --name claude-stub -v "$PWD/.stub-logs:/var/log/stub" claude-stub
# qa-claude MUST NOT have its own -p mappings when sharing a netns:
docker run --rm -it --name qa-claude --network container:claude-stub \
  -v "$PWD:/workspace/marketplace" -w /workspace/marketplace \
  -e ANTHROPIC_BASE_URL=http://127.0.0.1:8089 -e ANTHROPIC_AUTH_TOKEN=stub node:20 bash
# Captured bodies stream to ./.stub-logs/stub-bodies.log on the host.
```

> **Windows gotcha.** If you expose the stub with `-p 8089:8089` and `curl` from the host returns `curl: (52) Empty reply from server`, a host process (observed: Cursor IDE) is squatting `127.0.0.1:8089`. Diagnose with `netstat -ano | findstr 8089`; use `-p 18089:8089` instead, or just don't expose the port — the shared-netns workflow doesn't need it.

### 1.4 Register the marketplace, validate, and understand the install model

Use the `claude` CLI directly (scriptable, works headless). The `/plugin …` slash equivalents need the interactive UI.

```bash
# Register — pick ONE source:
claude plugin marketplace add DgxSparkLabs/marketplace     # remote main (released state)
claude plugin marketplace add /workspace/marketplace       # local clone (RECOMMENDED for in-flight changes)

claude plugin marketplace list                             # expect: dgxsparklabs-marketplace
```

**Non-interactive sanity gate (do this once, no stub needed):**

```bash
claude plugin validate ./
# Expect: exit 0, "Validation passed", the full set of plugins, no rule-* plugins, no description warning.
```

Enumerate just this marketplace's plugins:

```bash
MARKETPLACE="dgxsparklabs-marketplace"
claude plugin list --json --available > /tmp/plugins.json 2>/tmp/claude.err
jq --arg mp "$MARKETPLACE" '[.. | objects | select(.marketplaceName? == $mp)]' /tmp/plugins.json
# Expect a JSON array of the full set of plugins: the -single/-multi pairs for each construct type,
#  the per-event and multi hook plugins, and bundle-examples. Rule individuals excluded.
#  A much shorter array means you are on a pre-cd7a7d8 checkout (see docs/INVENTORY.md for the authoritative set).
```

**Install model (CLI ≥ 2.1.157 — verify with `claude --version`):**

- `claude plugin install <name>@dgxsparklabs-marketplace --scope project` **auto-enables** the plugin (writes `"enabledPlugins": {…: true}` into `<project>/.claude/settings.json`). A separate `claude plugin enable …` afterward now *errors* with `already enabled` — treat that output as **PASS**, not failure.
- **Scope is cwd-relative.** `claude plugin list` shows `✔ enabled` only when run **from the project dir you installed in**. From elsewhere the same plugin reads `✘ disabled` — correct scope behavior, not a regression. This is the single most likely cause of "I installed it but list says disabled."

### 1.5 The docker + tmux driving primitives (the interactive harness)

Your tools run on the *host*; Claude runs *inside the container, inside tmux*. There are eight primitives — every later command is built from these. Replace `qa-claude` with the real container name from primitive 2.

```bash
# 1. Run a shell command INSIDE the container:
docker exec qa-claude bash -lc 'ls /workspace'

# 2. Find the container and the tmux session:
docker ps --format '{{.Names}}\t{{.Status}}'        # e.g. "qa-claude  Up 2 hours"
docker exec qa-claude tmux ls                        # e.g. "0: 1 windows (attached)" — session is NAMED "0"
docker exec qa-claude tmux new-session -d -s 0       # ONLY if "no server running"

# 3. Pane addressing is session:window.pane -> 0:0.0 = left pane, 0:0.1 = right pane (after a split).

# 4. Send keystrokes (THE most important rule): text with -l, then Enter as a SEPARATE call.
docker exec qa-claude tmux send-keys -t 0:0.0 -l 'some text'   # types verbatim, does NOT submit
docker exec qa-claude tmux send-keys -t 0:0.0 Enter           # a key NAME -> NO -l
#   Special keys are sent WITHOUT -l: Enter Up Down Escape Tab Space C-c C-u C-o
#   WARNING: putting text and Enter in one -l call types the literal word "Enter" and never submits.

# 5. Read a pane (-S -<n> includes scrollback):
docker exec qa-claude tmux capture-pane -p -t 0:0.0 -S -30 | tail -n 20

# 6. ALWAYS sleep before capturing: TUI boot ~15s; permission dialog ~6-9s after a tool prompt; a turn ~6-20s.
#    A follow-up won't submit while the model is busy (a "Brewed for Ns" spinner shows) — wait for the idle ❯.

# 7. Answer dialogs: Enter accepts the highlighted row (usually Yes/option 1); Down/Up move; Escape cancels.

# 8. Windows/Git-Bash hosts ONLY: prefix bare-slash commands with MSYS_NO_PATHCONV=1
#    (/mcp /theme /config /agents /compact /exit), or a bare /word is rewritten to a Windows path.
#    Namespaced slashes (/dgxsparklabs-...:hello) are immune (the ':' disables conversion).
```

### 1.6 Launch Claude in tmux and install the example plugins

```bash
# Create an ABSOLUTE scratch dir (a pane's cwd/$HOME can differ from a `docker exec bash -lc` shell):
docker exec qa-claude bash -lc 'mkdir -p /workspace/lsptest && cd /workspace/lsptest && pwd'

# Install every -multi plugin into project scope (install auto-enables):
docker exec qa-claude bash -lc 'cd /workspace/lsptest && for p in command skill agent hook mcp monitor output-style theme lsp; do claude plugin install ${p}-example-multi@dgxsparklabs-marketplace --scope project 2>&1 | tail -n1; done'
# -> one "✔ Successfully installed plugin: <p>-example-multi@dgxsparklabs-marketplace (scope: project)" per construct

# Confirm enabled:
docker exec qa-claude bash -lc 'cd /workspace/lsptest && claude plugin list 2>&1 | grep -E "@dgxsparklabs|Status:"'

# Launch Claude in the LEFT pane (absolute cd), then wait and read:
docker exec qa-claude tmux send-keys -t 0:0.0 -l 'cd /workspace/lsptest && claude'
docker exec qa-claude tmux send-keys -t 0:0.0 Enter
sleep 16
docker exec qa-claude tmux capture-pane -p -t 0:0.0 | tail -n 14
# If "Do you want to trust the files in this folder?" appears, press Enter (Yes is highlighted).
# Because monitors are installed, the model often narrates session-start monitor reports — that is itself proof the monitor fired.
```

The `-single` siblings install identically — swap `-multi` for `-single` (and for hooks, install one or more `hook-example-<event>` plugins). Each construct cell below gives the exact `-single` install name.

---

## 2. Per-construct QA

Run in this order (easiest first). Each cell has: **what it is · variants & install · interactive (tmux) test · non-interactive (headless) test · proof signal · gotchas · failure signals.** Drive the left pane `0:0.0` unless a second pane is called for.

### 2.1 command — a reusable slash prompt

A command is a stored prompt invoked by slash. It works in `--print` too. **Headless: YES.**

**Variants & install**

```bash
# multi (3 commands: hello, goodbye, ping):
docker exec qa-claude bash -lc 'cd /workspace/lsptest && claude plugin install command-example-multi@dgxsparklabs-marketplace --scope project'
# single (1 command: hello):
docker exec qa-claude bash -lc 'cd /workspace/lsptest && claude plugin install command-example-single@dgxsparklabs-marketplace --scope project'
```

**Interactive (tmux)**

```bash
MSYS_NO_PATHCONV=1 docker exec qa-claude tmux send-keys -t 0:0.0 -l '/dgxsparklabs-command-example-multi:hello'
docker exec qa-claude tmux send-keys -t 0:0.0 Enter
sleep 6
docker exec qa-claude tmux capture-pane -p -t 0:0.0 -S -16 | tail -n 10
```

Expect (the `[command:hello]` line is the debug echo of `$ARGUMENTS`, empty here):

```text
  Ran 1 shell command
● [command:hello] args=[]
  # Lab Notebook — 2026-06-01
  ## Entries
  - [ ] (add entries here)
```

Other invocations — `:ping extra-args` → `[command:ping] args=[extra-args]` then `pong @ <UTC>`; `:goodbye` → a closing footer. **single** uses `/dgxsparklabs-command-example-single:hello` (same output as multi's `:hello`). Typing `/dgxsparklabs-command-example-multi:` opens an autocomplete dropdown whose rows are tagged `(dgxsparklabs-command-example-multi)` — confirming the per-plugin (not shared) namespace.

**Non-interactive (headless)** — body-dumper stub on 8089:

```bash
docker exec qa-claude bash -lc 'cd /workspace/lsptest && export ANTHROPIC_BASE_URL=http://127.0.0.1:8089 ANTHROPIC_AUTH_TOKEN=stub && echo "/dgxsparklabs-command-example-multi:hello" | claude --print; grep -F "dgxsparklabs-command-example-multi:hello" /tmp/stub-bodies.log'
# PASS: the captured request body contains <command-name>/dgxsparklabs-command-example-multi:hello</command-name>,
#       proving Claude resolved the per-plugin namespace client-side.
```

**Proof signal** — the rendered block + `Ran 1 shell command` (interactive); the `<command-name>…</command-name>` body match (headless). **Not** the model saying it ran.

**Gotchas** — pressing Enter on a grey ghost-suggestion does nothing; type the command fresh. A back-compat `enable` may report `scope: user` even after `--scope project` — harmless.

**Failure signals** — (a) no `command-example-multi` in `/plugins` → install broken; (b) `Unknown command` → `src/` reorg didn't propagate or a command file was renamed; (c) wrong output shape → re-check `src/commands/example-multi/commands/hello.md`.

### 2.2 skill — a model-invoked capability (SKILL.md)

A skill is invoked by slash or auto-loaded when its `description` matches your task. **Headless: YES** (same client-side resolver as commands).

**Variants & install**

```bash
# multi (2 skills: notebook, status):
docker exec qa-claude bash -lc 'cd /workspace/lsptest && claude plugin install skill-example-multi@dgxsparklabs-marketplace --scope project'
# single (1 skill: hello):
docker exec qa-claude bash -lc 'cd /workspace/lsptest && claude plugin install skill-example-single@dgxsparklabs-marketplace --scope project'
```

**Interactive (tmux)** — pass a topic argument:

```bash
MSYS_NO_PATHCONV=1 docker exec qa-claude tmux send-keys -t 0:0.0 -l '/dgxsparklabs-skill-example-multi:notebook rookie-onboarding'
docker exec qa-claude tmux send-keys -t 0:0.0 Enter
sleep 7
docker exec qa-claude tmux capture-pane -p -t 0:0.0 -S -18 | tail -n 12
```

Expect the `$ARGUMENTS`-carrying debug line, then the block:

```text
● [skill:notebook] args=[rookie-onboarding]
  [Lab Notebook] Status update on "rookie-onboarding"
  - Time: 2026-06-01T20:22:45Z
  - Status: in-progress
  - Next checkpoint: …
```

`:status` runs `df -h .` + a UTC stamp. **single** uses `/dgxsparklabs-skill-example-single:hello`. **Display quirk:** the `/dgxsparklabs-skill-example-multi:` dropdown labels rows by **bare component name** (`/notebook`, `/status`), each tagged `(dgxsparklabs-skill-example-multi)` — but the resolving invocation is still the full namespaced form. There is no `Skill: notebook` banner; the proof is the `[Lab Notebook]`/`[Status]` block.

**Non-interactive (headless)** — same shape as command (slash in `--print`, grep the body for the resolved namespaced slash). Skills also auto-load by description, which you can't deterministically assert headlessly.

**Proof signal** — the rendered `[Lab Notebook]`/`[Status]` block (interactive); the namespaced slash in the captured body (headless).

**Gotchas** — the invocation echoes as a normal `❯` line then `Ran 1 shell command`; no skill-loaded announcement.

**Failure signals** — (a) no entry in `/plugins` → install broken; (b) `Unknown command` → `src/` reorg didn't propagate or `SKILL.md name:` changed; (c) slash resolves but body empty → frontmatter parse error.

### 2.3 sub-agent — a separate agent with its own context and tools

Dispatched in plain English or managed via the TUI `/agents` picker. **Headless: NO** (`/agents` is TUI-only; the command-namespacing headless check exercises the same resolver as indirect evidence).

**Variants & install**

```bash
# multi (3 agents: notebook-reviewer, summarizer, validator):
docker exec qa-claude bash -lc 'cd /workspace/lsptest && claude plugin install agent-example-multi@dgxsparklabs-marketplace --scope project'
# single (1 agent: notebook-reviewer):
docker exec qa-claude bash -lc 'cd /workspace/lsptest && claude plugin install agent-example-single@dgxsparklabs-marketplace --scope project'
```

**Interactive (tmux)** — first inspect the picker, then do a real dispatch:

```bash
# Picker (bare slash -> MSYS_NO_PATHCONV=1 on Windows):
MSYS_NO_PATHCONV=1 docker exec qa-claude tmux send-keys -t 0:0.0 -l '/agents'
docker exec qa-claude tmux send-keys -t 0:0.0 Enter ; sleep 3
docker exec qa-claude tmux send-keys -t 0:0.0 Left           # /agents OPENS on "Running" — press Left to reach "Agents"
docker exec qa-claude tmux capture-pane -p -t 0:0.0 -S -20 | tail -n 16
docker exec qa-claude tmux send-keys -t 0:0.0 Escape         # close the picker

# Real dispatch (the model-independent proof):
docker exec qa-claude bash -lc 'printf "# Demo\nA short note for the agent test.\n" > /workspace/lsptest/demo-note.md'
docker exec qa-claude tmux send-keys -t 0:0.0 -l 'Use the dgxsparklabs-agent-example-multi:summarizer subagent to summarize demo-note.md. Do not ask questions.'
docker exec qa-claude tmux send-keys -t 0:0.0 Enter ; sleep 14
docker exec qa-claude tmux capture-pane -p -t 0:0.0 -S -20 | tail -n 12
```

Expect the picker's **Plugin agents** group (`dgxsparklabs-agent-example-multi:notebook-reviewer · summarizer · validator`), then on dispatch:

```text
● dgxsparklabs-agent-example-multi:summarizer(Summarize demo-note.md)
  ⎿  Done (1 tool use · 3.4k tokens · 7s)
● Here's the summary of demo-note.md: …
```

**single** lists only `dgxsparklabs-agent-example-single:notebook-reviewer`.

**Proof signal** — the **namespaced task header** + the `Done (N tool use · … · Ns)` line. These always appear and prove the sub-agent ran in its own context. The agent's prompt also asks it to echo its task as `[agent-input]`, but that is model-compliance-dependent and **frequently skipped** — do not treat it as a pass criterion. (`C-o` toggles the whole transcript verbose; it is not a per-block expand.)

**Gotchas** — `/agents` opening on the empty **Running** tab is not failure (rule 5). Bare-slash MSYS mangling (rule 8).

**Failure signals** — (a) no entry in `/plugins` → install broken; (b) no **Plugin agents** group in the picker → loader broken or `name:` mismatch; (c) dispatch with no namespaced header / `Done` line → context not switching.

### 2.4 hook — a shell command bound to a lifecycle event

Hooks are passive (fire on events) and produce **no chat output** — the proof is sentinel files. The example reads the event's JSON payload from **stdin** and writes `/tmp/hook-fired-<event>.log` (marker line + full payload). **Headless: PARTIAL.**

**Variants & install** — the "single" axis here is the per-event hook plugins; "multi" wires all the events.

```bash
# multi (all events in one plugin):
docker exec qa-claude bash -lc 'cd /workspace/lsptest && claude plugin install hook-example-multi@dgxsparklabs-marketplace --scope project'
# per-event (install any of these 9; each fires its one event):
#   hook-example-{userpromptsubmit,sessionstart,pretooluse,posttooluse,stop,subagentstop,sessionend,notification,precompact}
docker exec qa-claude bash -lc 'cd /workspace/lsptest && claude plugin install hook-example-pretooluse@dgxsparklabs-marketplace --scope project'
```

**Interactive (tmux)** — the `rm` is the *control* (isolates this edit's events). One edit+approve fires six events (`UserPromptSubmit → PreToolUse → Notification → PostToolUse → Stop → SubagentStop`):

```bash
docker exec qa-claude bash -lc 'rm -f /tmp/hook-fired-*.log'        # control, not cleanup
docker exec qa-claude tmux send-keys -t 0:0.0 -l 'Use the Edit tool to append the line # hooktest as the last line of demo-note.md. Do not ask questions, just make the edit.'
docker exec qa-claude tmux send-keys -t 0:0.0 Enter ; sleep 8
docker exec qa-claude tmux capture-pane -p -t 0:0.0 -S -20 | tail -n 16   # the edit dialog is ~14 lines tall
docker exec qa-claude tmux send-keys -t 0:0.0 Enter ; sleep 6            # approve (option 1, Yes)
docker exec qa-claude bash -lc 'cat /tmp/hook-fired-pretooluse.log'      # read the FILE, not the pane
```

Expect a marker line + the full JSON payload — note the real `tool_name` (the whole point of the debug hook):

```text
2026-06-01T20:01:56Z preToolUse fired
{"session_id":"…","cwd":"/workspace/lsptest","hook_event_name":"PreToolUse","tool_name":"Edit","tool_input":{…},"tool_use_id":"toolu_…"}
```

To fire every event: restart `claude` (`SessionStart`) → the edit+approve above → `/compact` (`PreCompact`, re-fires `SessionStart`/`SubagentStop`) → `/exit` (`SessionEnd`). Then `docker exec qa-claude bash -lc 'ls /tmp/hook-fired-*.log'` shows one sentinel file per event. Use `/exit` (not Ctrl+C) to fire `SessionEnd` reliably.

**Non-interactive (headless)** — stub on 8088. Confirmed firing under `claude --print`: `SessionStart`, `UserPromptSubmit`, `Stop`, `SessionEnd`:

```bash
docker exec qa-claude bash -lc 'cd /workspace/lsptest && export ANTHROPIC_BASE_URL=http://127.0.0.1:8088 ANTHROPIC_AUTH_TOKEN=stub && rm -f /tmp/hook-fired-sessionstart.log && echo "say hello" | claude --print && test -s /tmp/hook-fired-sessionstart.log && echo PASS'
# Same recipe for hook-fired-{userpromptsubmit,stop,sessionend}.log.
```

`PreToolUse`/`PostToolUse` need Claude to return a `tool_use` block, which the default stub doesn't emit → **partial** (use the interactive edit). `Notification`/`PreCompact` are interactive-only.

**Proof signal** — the sentinel file's marker line + JSON payload. (`UserPromptSubmit` additionally injects `[Lab Notebook context: timestamp=…]` into the prompt via stdout.)

**Gotchas** — read the payload from **stdin** (`p="$(cat)"`), not `${CLAUDE_TOOL_NAME}` (unpopulated in 2.1.159 → logs `unknown`). Sentinels append across firings.

**Failure signals** — (a) sentinel missing for a triggered event → that hook didn't fire; (b) marker but no JSON → handler isn't reading stdin; (c) no `tool_name` in a pre/post payload → wrong matcher or malformed payload.

### 2.5 mcp — external tool servers (model-called)

Servers spawn at session start (behind a logging proxy that tees JSON-RPC to `/tmp/mcp_proxy_<server>.log`); tools are model-called. **Requires `uv` on PATH.** **Headless: PARTIAL** (tool names only appear once Claude returns a `tool_use` block).

**Variants & install**

```bash
docker exec qa-claude bash -lc 'which uv || curl -LsSf https://astral.sh/uv/install.sh | sh'
# multi (3 servers: fetch, filesystem, sequential-thinking):
docker exec qa-claude bash -lc 'cd /workspace/lsptest && claude plugin install mcp-example-multi@dgxsparklabs-marketplace --scope project'
# single (1 server, key: example):
docker exec qa-claude bash -lc 'cd /workspace/lsptest && claude plugin install mcp-example-single@dgxsparklabs-marketplace --scope project'
```

**Interactive (tmux)**

```bash
docker exec qa-claude bash -lc 'ls /tmp/mcp_proxy_*.log'    # proxy logs exist once servers spawned at session start
docker exec qa-claude tmux send-keys -t 0:0.0 -l 'Use the fetch MCP tool to retrieve https://example.com and show me just the page title. Do not ask questions.'
docker exec qa-claude tmux send-keys -t 0:0.0 Enter ; sleep 6
docker exec qa-claude tmux capture-pane -p -t 0:0.0 | tail -n 8     # expect a tool-permission dialog
docker exec qa-claude tmux send-keys -t 0:0.0 Enter                # approve
sleep 14   # COLD CACHE: first run downloads the server via uvx/npx (~34s). If no "Called plugin:…:fetch" yet, sleep 20 more.
docker exec qa-claude tmux capture-pane -p -t 0:0.0 -S -16 | tail -n 8
docker exec qa-claude bash -lc 'grep tools/call /tmp/mcp_proxy_fetch.log | tail -n1'   # the real proof
```

Expect `Called plugin:dgxsparklabs-mcp-example-multi:fetch` + `The page title is: Example Domain`, and the proxy line:

```text
[fetch] -> {"method":"tools/call","params":{"name":"fetch","arguments":{"url":"https://example.com"},…}}
```

`/mcp` (TUI, bare-slash → `MSYS_NO_PATHCONV=1`) lists all three servers; `fetch` (uvx) and `sequential-thinking` (npx) connect, **`filesystem` fails** (upstream `zod`/`ERR_MODULE_NOT_FOUND` npx-cache bug — not a config defect). **single** advertises one server, key `example`.

**Non-interactive (headless)** — **partial.** The tool name `mcp__dgxsparklabs-mcp-example-multi__fetch__fetch` (hook-matcher form) / `plugin:dgxsparklabs-mcp-example-multi:fetch` (CLI form) only appears once a real model returns a `tool_use` block; the default stub returns text only. Use the interactive call.

**Proof signal** — the `Called plugin:…:fetch` line + correct result, **and** the `tools/call` line in the proxy log.

**Gotchas** — first-run latency (re-check before judging failure); `filesystem` failing while siblings connect is the upstream bug.

**Failure signals** — (a) `✗ Failed to connect` on `uvx mcp-server-fetch` → `uv` not installed; (b) `/mcp` empty → config not loaded; (c) model says "no fetch tool" → reorg didn't propagate; (d) only `filesystem` fails → upstream `zod` bug.

### 2.6 monitor — a shell command run once at session start

Monitors run at session start and inject their stdout into the model's context (each line prefixed `[monitor:<name>]`). **Headless: NO** dedicated test.

**Variants & install**

```bash
# multi (3 monitors: disk-usage, memory-usage, git-status):
docker exec qa-claude bash -lc 'cd /workspace/lsptest && claude plugin install monitor-example-multi@dgxsparklabs-marketplace --scope project'
# single (1 monitor: disk-usage):
docker exec qa-claude bash -lc 'cd /workspace/lsptest && claude plugin install monitor-example-single@dgxsparklabs-marketplace --scope project'
```

**Interactive (tmux)** — probe the injected context, and **forbid tool use** (else the model just runs `df` itself and proves nothing):

```bash
docker exec qa-claude tmux send-keys -t 0:0.0 -l 'Without running any tool or command, quote verbatim any session-start monitor or observation context you were given. If you received none, say exactly: NO MONITOR CONTEXT.'
docker exec qa-claude tmux send-keys -t 0:0.0 Enter ; sleep 8
docker exec qa-claude tmux capture-pane -p -t 0:0.0 -S -20 | tail -n 16
```

Expect all three recited, each prefixed:

```text
[monitor:disk-usage]
overlay        1007G   12G  944G   2% /
[monitor:memory-usage]
…
[monitor:git-status]
not a git repo
```

**single** recites only `[monitor:disk-usage]`.

**Non-interactive (headless)** — no clean path. A fresh `claude --print` fires `SessionStart`, but reliably surfacing the injected monitor context requires the model to recite it. Treat monitor as interactive-only.

**Proof signal** — the `[monitor:<name>]`-prefixed recital (must forbid tool use). Note: a capable model often *spontaneously narrates* this context at boot — that's the model reading its context, which itself half-proves the monitor fired.

**Gotchas** — no chat banner and no `/plugin` Monitors tab needed; `plugin.json` carries no `monitors` key (auto-discovered from `monitors/monitors.json`).

**Failure signals** — (a) no entry in `/plugins` → install broken; (b) recital returns `NO MONITOR CONTEXT` → loader didn't run or `monitors.json` schema mismatch; (c) a monitor missing → rename/reorg didn't propagate.

### 2.7 output-style — a system-prompt voice preset

Set via `/config` → **Output style** — there is **no `/output-style` command** in CLI 2.1.159. Persists namespaced to **project** `.claude/settings.local.json`. **Headless: YES** (via `--append-system-prompt` + body capture).

**Variants & install**

```bash
# multi (3 styles: Lab Notebook Voice, Concise Engineer, Tutoring):
docker exec qa-claude bash -lc 'cd /workspace/lsptest && claude plugin install output-style-example-multi@dgxsparklabs-marketplace --scope project'
# single (1 style: Lab Notebook Voice):
docker exec qa-claude bash -lc 'cd /workspace/lsptest && claude plugin install output-style-example-single@dgxsparklabs-marketplace --scope project'
```

**Interactive (tmux)** — drive the config panel (bare-slash → `MSYS_NO_PATHCONV=1`):

```bash
MSYS_NO_PATHCONV=1 docker exec qa-claude tmux send-keys -t 0:0.0 -l '/config'
docker exec qa-claude tmux send-keys -t 0:0.0 Enter ; sleep 3
docker exec qa-claude tmux send-keys -t 0:0.0 -l 'output style' ; sleep 1   # filter to the row
docker exec qa-claude tmux send-keys -t 0:0.0 Enter ; sleep 1               # select the row
docker exec qa-claude tmux send-keys -t 0:0.0 Space ; sleep 1               # open the style list
docker exec qa-claude tmux capture-pane -p -t 0:0.0 | tail -n 16
# Navigate with Down (compute N from the captured ❯ row), Enter to confirm (the WRITE lands here),
# then Escape Escape to leave /config (Esc does NOT revert the write).
docker exec qa-claude bash -lc 'cat /workspace/lsptest/.claude/settings.local.json'
```

Expect the three plugin styles listed as `dgxsparklabs-output-style-example-multi:{Lab Notebook Voice,Concise Engineer,Tutoring}`, and after selection:

```json
{"outputStyle":"dgxsparklabs-output-style-example-multi:Lab Notebook Voice"}
```

**single** offers only `…:Lab Notebook Voice`.

**Non-interactive (headless)** — body-dumper on 8089; inject the style file and confirm it reaches the request's `system[]` array:

```bash
docker exec qa-claude bash -lc 'cd /workspace/lsptest && export ANTHROPIC_BASE_URL=http://127.0.0.1:8089 ANTHROPIC_AUTH_TOKEN=stub && rm -f /tmp/stub-bodies.log && claude --print --append-system-prompt "$(cat src/output-styles/example-multi/output-styles/lab-notebook-voice.md)" "explain F9" && grep -F "Lab Notebook Voice" /tmp/stub-bodies.log && grep -F "Next:" /tmp/stub-bodies.log'
# PASS: both greps match — the style content reached system[] verbatim (would be applied behind a real model).
```

**Proof signal** — the namespaced `outputStyle` write in `settings.local.json` (interactive); the `system[]` body match (headless). Behavior change shows only on a *substantive* prompt (a trivial "2+2" won't reveal the voice).

**Gotchas** — the persisted value is **namespaced** (not bare `"Lab Notebook Voice"`); `settings.local.json` was seen reset to `{}` on a later unrelated restart, so capture the write *immediately* after selection. A `/config` fired mid-turn is queued as literal text → `Unknown command`.

**Failure signals** — (a) no entry in `/plugins` → install broken; (b) styles absent from the `/config` list → frontmatter `name:` not exposed; (c) selection made but no `outputStyle` in settings → persistence broken.

### 2.8 theme — a terminal color palette

`/theme` **is** a real slash command (unlike output-style). Persists to **user** `~/.claude/settings.json`. **Headless: NO** — visual/TTY only (`/theme` errors under `--print`).

**Variants & install**

```bash
# multi (3 themes: Lab Notebook, Nord, Solarized Dark):
docker exec qa-claude bash -lc 'cd /workspace/lsptest && claude plugin install theme-example-multi@dgxsparklabs-marketplace --scope project'
# single (1 theme: Lab Notebook):
docker exec qa-claude bash -lc 'cd /workspace/lsptest && claude plugin install theme-example-single@dgxsparklabs-marketplace --scope project'
```

**Interactive (tmux)** — establish a causal control first (rule 4):

```bash
MSYS_NO_PATHCONV=1 docker exec qa-claude tmux send-keys -t 0:0.0 -l '/theme'
docker exec qa-claude tmux send-keys -t 0:0.0 Enter ; sleep 2
docker exec qa-claude tmux capture-pane -p -t 0:0.0 | tail -n 16   # items 8-10: Lab Notebook / Nord / Solarized Dark
# CONTROL: first select "2. Dark mode", confirm settings reads "dark", THEN re-open /theme and pick the plugin theme.
# The highlight starts on the ACTIVE theme — capture the ❯ row and compute N; do not hardcode Down count.
docker exec qa-claude bash -lc 'grep -i theme ~/.claude/settings.json'
```

Expect items `8. Lab Notebook / 9. Nord / 10. Solarized Dark (from dgxsparklabs-theme-example-multi)`, a `⎿ Using custom theme "Lab Notebook"` confirmation, and the **user**-scope write:

```json
"theme": "custom:dgxsparklabs-theme-example-multi:lab-notebook"
```

Note the id is `custom:<plugin-name>:<theme-file-stem>` — the JSON filename stem (`lab-notebook`), not the human `name:` ("Lab Notebook"). **single** offers only `Lab Notebook`.

**Non-interactive (headless)** — none. The color flip has no request-stream observable; `/theme` returns `isn't available in this environment` under `--print`.

**Proof signal** — the confirmation line + the `custom:dgxsparklabs-theme-example-multi:*` write in **user** settings. The literal color flip doesn't survive `capture-pane -p` (strips ANSI) — use `capture-pane -e` if you must assert on color codes, or a human eye.

**Gotchas** — theme persists to **user** scope (not the project `settings.local.json` where output-style lands); bare-slash MSYS mangling; wait for an idle `❯` (a queued `/theme` returns `unknown`).

**Failure signals** — (a) no entry in `/plugins` → install broken; (b) the three themes absent from the picker → JSON `name`/loader mismatch; (c) selection made but no `custom:…` theme in user settings → persistence broken.

### 2.9 lsp — a language server feeding diagnostics and navigation

There is **no LSP tab** in Claude Code 2.1. The server is forked **lazily on the first matching edit** (not a Read), using the **PATH of the shell that launched `claude`**. Two observability channels: the in-chat `(example-lsp)` diagnostic, and the server's own input log. **Headless: NO** via Claude (needs edit + TTY); the server *is* stdio-smoke-testable directly.

**Variants & install** — the two variants differ fundamentally:

```bash
# multi (bundled, self-contained: markdown + python via example_lsp.py; only uv needed):
docker exec qa-claude bash -lc 'cd /workspace/lsptest && which uv || curl -LsSf https://astral.sh/uv/install.sh | sh; claude plugin install lsp-example-multi@dgxsparklabs-marketplace --scope project'
# single (points at EXTERNAL marksman — install the binary separately on the launch shell's PATH):
docker exec qa-claude bash -lc 'cd /workspace/lsptest && claude plugin install lsp-example-single@dgxsparklabs-marketplace --scope project'
```

**Interactive (tmux)** — two panes: left = Claude, right = the server's input log. (Diagnostics attach one turn *late*, so send a second prompt to surface them.)

```bash
docker exec qa-claude tmux split-window -h -t 0:0                                    # right pane = 0:0.1
docker exec qa-claude tmux send-keys -t 0:0.1 -l 'tail -n0 -F /tmp/example_lsp.log'  # -F waits for the file to appear
docker exec qa-claude tmux send-keys -t 0:0.1 Enter
docker exec qa-claude bash -lc "printf 'def add(a, b):\n    return a + b\n\nprint(undefined_var)\n' > /workspace/lsptest/calc.py"
# Launch claude in 0:0.0 if not already running (1.6). Then edit (NOT read) the file:
docker exec qa-claude tmux send-keys -t 0:0.0 -l 'Use the Edit tool to append the comment line # lsp test as the last line of calc.py. Do not ask questions, just make the edit.'
docker exec qa-claude tmux send-keys -t 0:0.0 Enter ; sleep 9
docker exec qa-claude tmux capture-pane -p -t 0:0.0 | tail -n 8                       # the edit dialog
docker exec qa-claude tmux send-keys -t 0:0.0 Enter ; sleep 8                        # accept the edit
docker exec qa-claude tmux send-keys -t 0:0.0 -l 'List verbatim the language-server diagnostics shown to you for calc.py, with line numbers.'
docker exec qa-claude tmux send-keys -t 0:0.0 Enter ; sleep 22                       # diagnostic attaches to THIS turn
docker exec qa-claude tmux capture-pane -p -t 0:0.0 -S -16 | tail -n 12              # LEFT: the (example-lsp) diagnostics
docker exec qa-claude tmux capture-pane -p -t 0:0.1 | tail -n 8                      # RIGHT: [0001] initialize … [0003] didOpen
```

Expect (the `--always-error` marker guarantees ≥1 diagnostic on *every* edit, even a clean file):

```text
⚠ [Line 1:1] example-lsp marker — file analyzed (always-on; event #N) (example-lsp)
⚠ undefined name 'undefined_var' (example-lsp)
```

and on the right, live wire traffic: `initialize → initialized → textDocument/didOpen → didChange → didSave`. **multi** is self-contained; **single** needs `marksman` on PATH (else no `Starting LSP server instance` line). Navigation: ask "Use the LSP to list the symbols defined in calc.py" / "…go-to-definition for add" → the model calls its LSP tool.

**Non-interactive (headless)** — none via Claude (a Read won't attach; `--debug` exits immediately in many headless containers). To isolate server-vs-client, drive `src/lsp-servers/example-multi/example_lsp.py` directly over stdio with `initialize → didOpen → didChange` (test **both** a full-sync change — `contentChanges:[{"text":"<whole doc>"}]`, no `range` — and an incremental one).

**Proof signal** — the `(example-lsp)` source tag in chat **and** the wire traffic in `/tmp/example_lsp.log`. Watch `Received diagnostics … N diagnostic(s)`, **not** the `Checking registry - N pending` counter (it polls `0` even on success). A capable model describing the bug from its own reading is **not** proof.

**Gotchas** — a Read won't trigger it (Edit/Write only); use plain `claude`, not `--debug`; `tail -F` (capital F) for the not-yet-existing log; the diagnostic lands one turn late.

**Failure signals** — no `Starting LSP server instance: …:python` after an edit → (a) `uv`/`marksman` not on the launch shell's PATH; (b) `/plugin` → Errors tab shows a spawn error; (c) stale install → uninstall, reinstall, `/reload-plugins`. If it starts but logs `0 diagnostic(s)`, drive the server over stdio to isolate (it must maintain its document buffer for both sync modes — `apply_change()` does).

---

## 3. Teardown

**Per-session reset** (close the session + extra pane + scratch/log files; keeps plugins installed):

```bash
MSYS_NO_PATHCONV=1 docker exec qa-claude tmux send-keys -t 0:0.0 -l '/exit'
docker exec qa-claude tmux send-keys -t 0:0.0 Enter
docker exec qa-claude tmux kill-pane -t 0:0.1     # close the right pane (ignore error if unused)
docker exec qa-claude bash -lc 'rm -rf /workspace/lsptest /tmp/hook-fired-*.log /tmp/mcp_proxy_*.log /tmp/example_lsp.log'
```

**Full uninstall** (removes every plugin installed from this marketplace, whatever set you exercised):

```bash
docker exec qa-claude bash -lc 'cd /workspace/lsptest 2>/dev/null; for p in $(claude plugin list 2>/dev/null | grep -oE "[a-z-]+@dgxsparklabs-marketplace" | cut -d@ -f1 | sort -u); do claude plugin uninstall "$p" --scope project; done; claude plugin marketplace remove dgxsparklabs-marketplace'
```

**Container removal** (Setup option B / dockerized stub):

```powershell
docker rm -f qa-claude
docker stop claude-stub   # only if you ran the dockerized stub
```

---

## 4. Quick reference

### 4.1 Install-name and slash-string card

Install pattern for every row: `claude plugin install <install-name>@dgxsparklabs-marketplace --scope project` (auto-enables). Slash namespace = `dgxsparklabs-<install-name>`.

| Construct · variant | Install name | Invoke | Headless |
|---|---|---|---|
| command · single | `command-example-single` | `/dgxsparklabs-command-example-single:hello` | YES |
| command · multi | `command-example-multi` | `…-command-example-multi:hello` · `:goodbye` · `:ping` | YES |
| skill · single | `skill-example-single` | `/dgxsparklabs-skill-example-single:hello` | YES |
| skill · multi | `skill-example-multi` | `…-skill-example-multi:notebook [topic]` · `:status` | YES |
| agent · single | `agent-example-single` | `/agents` → `…-agent-example-single:notebook-reviewer` | NO |
| agent · multi | `agent-example-multi` | `/agents` → `…:notebook-reviewer` · `:summarizer` · `:validator` | NO |
| hook · per-event | `hook-example-<event>` | passive (one event) | PARTIAL |
| hook · multi | `hook-example-multi` | passive (all events) | PARTIAL |
| mcp · single | `mcp-example-single` | model-called; server key `example` | PARTIAL |
| mcp · multi | `mcp-example-multi` | model-called; keys `fetch` · `filesystem` · `sequential-thinking` | PARTIAL |
| monitor · single | `monitor-example-single` | passive — `disk-usage` at session start | NO |
| monitor · multi | `monitor-example-multi` | passive — `disk-usage` · `memory-usage` · `git-status` | NO |
| output-style · single | `output-style-example-single` | `/config` → Output style → `…:Lab Notebook Voice` | YES |
| output-style · multi | `output-style-example-multi` | `/config` → Output style → `…:{Lab Notebook Voice,Concise Engineer,Tutoring}` | YES |
| theme · single | `theme-example-single` | `/theme` → `Lab Notebook` | NO |
| theme · multi | `theme-example-multi` | `/theme` → `Lab Notebook` · `Nord` · `Solarized Dark` | NO |
| lsp · single | `lsp-example-single` | passive — external `marksman` (`.md`) | NO |
| lsp · multi | `lsp-example-multi` | passive — bundled `example_lsp.py` (`.md`, `.py`) | NO |

The component after the `:` is the construct's own internal name: skill/agent/output-style frontmatter `name:`, command filename stem, MCP server key.

### 4.2 Headless coverage — what the non-interactive path can and cannot prove

| Verdict | Constructs | Why |
|---|---|---|
| **YES** | command, skill, output-style | Slash resolves client-side / style lands in `system[]` — observable in the captured request body, no model needed |
| **PARTIAL** | hook, mcp | Hooks: `SessionStart`/`UserPromptSubmit`/`Stop`/`SessionEnd` fire under `--print`; `PreToolUse`/`PostToolUse`/`Notification`/`PreCompact` need a `tool_use` block the stub doesn't emit. MCP: tool names need a `tool_use` block |
| **NO** | sub-agent, monitor, theme, lsp | `/agents` is TUI-only; monitor recital needs the model; theme is a TTY paint; LSP needs an edit + TTY (smoke-test the server over stdio instead) |

### 4.3 Failure-signal index (fast triage)

| Symptom | Likely cause |
|---|---|
| `claude plugin list` says `✘ disabled` right after install | You're not in the project dir you installed in — scope is cwd-relative (1.4) |
| `Unknown command` on a namespaced slash | `src/` reorg didn't propagate, or a `name:`/filename changed → regenerate |
| Blank `capture-pane` after a command that ran | Block scrolled past the tail → re-capture with `-S -40` (rule 3) |
| `/agents` shows `No subagents are currently running` | The Running tab — press `Left` to reach Agents (rule 5) |
| Bare slash becomes `C:/Program Files/Git/…` | Windows MSYS path conversion — prefix `MSYS_NO_PATHCONV=1` (primitive 8) |
| Hook sentinel has a marker but no JSON | Handler reads `${CLAUDE_TOOL_NAME}` env instead of stdin (`p="$(cat)"`) |
| MCP `filesystem` fails while siblings connect | Upstream `zod`/`ERR_MODULE_NOT_FOUND` npx-cache bug, not your config |
| LSP `0 diagnostic(s)` / `Skipping empty diagnostics` | Server didn't run (check `uv`/PATH + `/plugin` Errors), OR you Read instead of Edit |
| Theme/output-style "passes" without your action | No causal control — set a different value first (rule 4) |
| Timestamps don't match the host | Container clock skew — match the output *shape*, not the literal date |

---

*Source of truth for the full multi-platform grid (Codex, Gemini, Cursor, Windsurf, Devin, agents CLI) and the live captures behind these cells: `docs/TEST_YOURSELF.md` Section 4. Where this runbook and that doc disagree, that doc's Section 4 is authoritative — it carries the dated live captures.*
