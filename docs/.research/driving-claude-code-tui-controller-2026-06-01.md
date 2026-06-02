# Driving Claude Code's interactive session from outside — experience report + a closed-loop controller design

> **Status:** design note for a FUTURE session that will implement it. Written 2026-06-01 by the
> session that lived through the problem. Assume the implementing session has **no memory** of any of
> this — everything needed is here.
>
> **One-line problem:** I drove an interactive `claude` TUI through `tmux send-keys`/`capture-pane`
> with fixed `sleep`s between actions. That is an **open-loop blind controller** — it acts on a guess,
> not on an observed "ready" signal — and it was flaky.
>
> **One-line answer:** We drive **interactive REPL CLIs** (NOT the Agent SDK). If a target CLI happens to
> offer a non-interactive structured mode (claude's `-p --output-format stream-json`, where the `result`
> event is a completion ack), prefer that — but it's an escape hatch, not our path. For the REPL itself,
> **close the loop**: replace `sleep` with an **observed idle signal**, and remove avoidable dialogs at
> launch. That is Chapter 5, our design.

---

## How to use this document

- **Chapter 1** — the situational setup (what we were doing and why a live session needed driving).
- **Chapter 2** — exactly what I did (verbatim commands). This is fact, observed.
- **Chapter 3** — the open-loop problem and every failure mode it caused.
- **Chapter 4** — the escape hatch: a structured/headless mode *if* a CLI has one. We do **NOT** use the Agent SDK.
- **Chapter 5** — **OUR primary design**: the closed-loop interactive-REPL controller. **Start here when implementing.**
- **Chapter 6** — verification channels (how to KNOW what happened).
- **Chapter 7** — the concrete next-session implementation plan + acceptance criteria.
- **Appendix** — command reference, sources, and "verify before trusting" open questions.

Confidence tags used below: **[fact]** = I observed it this session; **[doc]** = from official docs via
research; **[verify]** = plausible but confirm against current docs before relying on it.

---

## Chapter 0 — Reproducing the environment (bootstrap)

> The original `qa-claude` container pre-existed from the live session. This chapter is the **recipe to
> recreate an equivalent** so a cold session has something to drive. Steps tagged **[verify]** are
> standard/reconstructed, not copied from the original — confirm them.

**0.1 Container + repo + toolchain.** From the repo root on the host:
```bash
docker run -d --name qa-claude -v "$PWD:/workspace/marketplace" -w /workspace/marketplace node:20 sleep infinity
docker exec -it qa-claude bash      # then, inside:  [verify]
apt-get update && apt-get install -y tmux curl ca-certificates
curl -LsSf https://astral.sh/uv/install.sh | sh ; export PATH="$HOME/.local/bin:$PATH"
npm install -g @anthropic-ai/claude-code
claude --version          # MUST be >= 2.1.157 (older CLIs don't auto-enable plugins)
```

**0.2 Authenticate claude — REQUIRED; headless fails before the first `result` without it.** Either:
- **API key** (best for automation): `export ANTHROPIC_API_KEY=sk-ant-…`  **[verify: confirm headless honors it]**; or
- **OAuth** (what the original session used — a Claude Max login): run `claude` once and complete `/login`,
  or `claude setup-token`.

**0.3 Register the marketplace + install the LSP plugin** (the repo is a *Directory* source via the mount):
```bash
claude plugin marketplace add /workspace/marketplace
mkdir -p /root/test && cd /root/test
claude plugin install lsp-example-multi@dgxsparklabs-marketplace --scope project   # auto-enables on >=2.1.157
```
The server ships *inside* the plugin; its filename is whatever the installed `lsp-config.json` points at
(currently `example_lsp.py`). **Don't hardcode it** — resolve with
`find ~/.claude/plugins -name '*.py' -path '*lsp-example-multi*' | head -1`.

**0.4 Create the self-test fixture** (Chapter 7 asserts against this exact file, in `/root/test`):
```bash
printf 'def add(a, b):\n    return a + b\n\nprint(undefined_var)\n' > /root/test/calc.py
```

**0.5 Launch claude in tmux** (only needed for the Chapter-5 TUI path; the headless path doesn't use tmux):
```bash
tmux new-session -d -s 0 -x 120 -y 50      # pin width 120 — Chapter 5's regexes depend on stable wrapping
tmux send-keys -t 0:0.0 -l 'cd /root/test && claude --debug' ; tmux send-keys -t 0:0.0 Enter
```

**Prereqs checklist:** Docker; repo mounted at `/workspace/marketplace`; container has `tmux`+`uv`+`node`+
`claude >= 2.1.157`; claude **authenticated**; plugin installed; `/root/test/calc.py` present.

---

## Chapter 1 — Situational setup (the "where are we")

**Project.** A cross-platform AI-coding-agent **plugin marketplace** (`DgxSparkLabs/marketplace`).
Source of truth lives under `src/<construct>/`; a generator (`uv run scripts/generate_manifest.py`)
produces `_generated/` and the platform manifests. There is a hand-written operator QA manual,
`docs/TEST_YOURSELF.md`, with a cell per construct × platform.

**What led here.** We built a bundled **LSP server** plugin (`src/lsp-servers/example-multi/example_lsp.py`)
— a real, stdlib-only Language Server (Python via `ast`, Markdown) that does diagnostics + document
symbols + go-to-definition + hover + references. To prove it works *inside real Claude Code* (not just a
unit smoke test), we had to drive a live `claude` session, make it edit a file, and watch the LSP fire.
That live-driving is the subject of this doc. **[fact]**

**The topology I was working through.** Three boundaries between me and the thing I was steering:

```
me  = Claude Code on the Windows host (had: Bash tool [git-bash], Docker, the repo)
  │
  │  docker exec qa-claude <cmd>           (one-shot, non-interactive, crosses host→container)
  ▼
container "qa-claude"  (id 8976f5d2…, image node:20; repo bind-mounted at /workspace/marketplace)
  │
  │  tmux  (session 0, window 0, pane 0.0)
  ▼
interactive `claude` CLI  (cwd /root/test, launched as `claude --debug`)
  │
  ▼
example_lsp.py  (the LSP child process Claude forks lazily on a matching edit)
```

Key facts about that environment **[fact]**:
- The container had `uv`, `node`/`npm`, `claude` (CLI 2.1.x), and the repo bind-mounted (so my host edits
  were visible inside at `/workspace/marketplace`; the marketplace was registered as a *Directory* source).
- The `claude` process ran inside a **tmux** pane; I was on the host. I never attached interactively — I
  poked the pane and screenshotted it via `docker exec`.
- Claude Code writes a per-session debug log at `~/.claude/debug/<session-id>.txt` when launched with
  `--debug`. This turned out to be the **reliable** channel.

---

## Chapter 2 — What I actually did (the tmux control method) [fact]

Every action was a **separate, fire-and-forget `docker exec`** from the host Bash tool. No live terminal.

**Discover the target:**
```bash
docker ps --format '{{.Names}}\t{{.ID}}\t{{.Image}}'        # → qa-claude  8976f5d2  node:20
docker exec qa-claude tmux ls                               # → 0: 1 windows (attached)
docker exec qa-claude tmux list-panes -t 0 \
  -F '#{session_name}:#{window_index}.#{pane_index} cmd=#{pane_current_command} path=#{pane_current_path}'
#   → 0:0.0 cmd=claude path=/root/test     (this gave me the pane target "0:0.0")
```

**Send input** (`send-keys`, addressing pane `-t 0:0.0`):
```bash
# literal text into the input box (-l = literal; tmux won't parse it as key names):
docker exec qa-claude tmux send-keys -t 0:0.0 -l "Use the Edit tool to append # x to calc.py. Do not ask questions."
# submit — Enter WITHOUT -l so tmux treats it as the Enter key; sent as a SEPARATE call:
docker exec qa-claude tmux send-keys -t 0:0.0 Enter
# other keys, named, no -l:
docker exec qa-claude tmux send-keys -t 0:0.0 Down        # move selection in a dialog
docker exec qa-claude tmux send-keys -t 0:0.0 Escape      # dismiss a menu / ghost text
docker exec qa-claude tmux send-keys -t 0:0.0 C-u         # clear the input line
```

**Read output** (`capture-pane`, a snapshot of the *visible* screen only):
```bash
docker exec qa-claude tmux capture-pane -t 0:0.0 -p 2>&1 | tail -20
```

**The (bad) synchronization** — a fixed guess:
```bash
send-keys -l "<prompt>" ; send-keys Enter ; sleep 22 ; capture-pane -p | tail
```

**Reliable back-channel #1 — the debug log** (grep structured events instead of scraping the TUI):
```bash
docker exec qa-claude bash -lc '
  LOG=$(ls -t ~/.claude/debug/*.txt | head -1)
  grep -iE "starting lsp server|publishdiagnostics|received diagnostics|skipping empty" "$LOG" | tail
'
# This is where the ground-truth came from, e.g.:
#   Received diagnostics from plugin:…:python: 1 diagnostic(s) for file:///root/test/calc.py
#   Skipping empty diagnostics …                       ← this line exposed a real bug
```

**Reliable back-channel #2 — talk to the LSP directly** (cut out the model and the TUI entirely; speak
LSP JSON-RPC to the installed server over a heredoc):
```bash
docker exec qa-claude bash -lc '
  SRV=$(find ~/.claude/plugins -name example_lsp.py | head -1)
  uv run --no-project python - "$SRV" << "PYEOF"
import subprocess, json, sys
def frame(m):
    d=json.dumps(m).encode(); return b"Content-Length: %d\r\n\r\n"%len(d)+d   # LSP wire framing
# spawn SRV; send initialize + didOpen + an INCREMENTAL didChange; read publishDiagnostics
PYEOF
'
```
(The `<< "PYEOF"` quoted heredoc stops the host shell from expanding `$` inside the Python.)

**Restart trick** (because `/exit` and `/reload-plugins` sent via `send-keys` got submitted as *chat
messages* — the slash menu lost the race — the model just replied conversationally):
```bash
docker exec qa-claude bash -lc 'pkill -f "claude"'         # process dies → pane drops to bash
sleep 3
docker exec qa-claude tmux send-keys -t 0:0.0 -l "claude --debug"
docker exec qa-claude tmux send-keys -t 0:0.0 Enter
```

---

## Chapter 3 — The problem: open-loop blind control

The loop was `emit keystroke → sleep(fixed) → snapshot`, with **no signal that the previous action
landed or that the app is idle.** It's open-loop: I act on a timer, not on an observation. **[fact]**

Concrete failure modes I hit, all traceable to that missing "is it idle yet?" signal **[fact]**:

1. **Captured mid-think.** `sleep` too short → I scraped a spinner (`✻ Brewed for 6s`) and saw no answer.
2. **Dropped input.** Sent the next prompt while the model was still busy → the `Enter` was ignored.
3. **Ghost-text collisions.** Claude shows grey auto-suggestions in the input box; my typed text
   sometimes blended with them, so a prompt looked "typed" but didn't submit.
4. **Slash-commands became chat.** `/exit`, `/reload-plugins` via `send-keys` submitted as messages
   (Enter beat the slash menu) → the model answered them in prose instead of executing them.
5. **Popups inserted dead turns.** Permission dialogs, an "install pyright-lsp?" recommendation, and a
   session-feedback survey interrupted the flow. Worse: the LSP diagnostic attaches to the *turn after an
   edit*, and a popup consuming that turn made the diagnostic vanish before I could ask for it.
6. **Snapshot blindness.** `capture-pane -p` shows only the visible ~47 rows; long replies scrolled off,
   so I often saw truncated or stale state.

Net: many retries, and several "it's broken" conclusions that were actually *measurement* failures, not
system failures. (Twice the truth was the opposite of what the TUI suggested — a confident-but-wrong model
reply masked a dead server; later a `0 pending` counter masked a live one.)

---

## Chapter 4 — Escape hatch: a structured mode (if a CLI has one). We do NOT use the Agent SDK.

> **Scope.** We drive **interactive REPL CLIs** — that is the deliverable. We are **NOT** using the Claude
> Agent SDK. This chapter is a short, honest aside; **Chapter 5 is our actual design.**

**The principle:** if the app offers a non-interactive JSON/headless mode, scraping its TUI is the wrong
tool — a structured mode gives a real completion **ack** instead of a guessed `sleep`. Prefer it *when it
exists*. Our targets are interactive REPLs, so usually it doesn't — go build Chapter 5.

### 4.1 Claude's structured mode, for reference only (one-shot, NOT a REPL) **[doc]**
```bash
# single turn, structured result:
claude -p "append a comment to calc.py" --output-format json

# event stream (newline-delimited JSON); each line is an event object:
claude -p "append a comment to calc.py" \
  --output-format stream-json --verbose --include-partial-messages
```
The stream emits `{"type":"system","subtype":"init", "session_id":…}` first, then `assistant` /
`tool_use` / `tool_result` events, and finishes with the **completion ack**:
```json
{"type":"result","subtype":"success","session_id":"…","num_turns":2,"total_cost_usd":…,"result":"…"}
```
**Closing the loop = read stdout until you see `{"type":"result"}`** (subtype `success`, or an
`error_*` subtype on failure). No `sleep`, no scraping. `--verbose` is required to get the event stream on
`-p`. **If stdout closes BEFORE a `result` event** (process crash / non-zero exit), treat the run as
**failed** — don't block forever. Source: `code.claude.com/docs/en/headless.md`. **[doc]**

*(Multi-turn via the Agent SDK was here and is REMOVED — out of scope. If you ever need multi-turn over the
CLI escape hatch, `--resume <session_id>` from the init event works; but our path is the interactive REPL.)*

### 4.2 Removing permission dialogs & popups — do it at LAUNCH (the single biggest win) **[verify]**
Most of Chapter 3's flakiness was avoidable dialogs the controller then had to fight. Kill them when you
**launch** the interactive session — full details in **5.0**. In short: `claude --permission-mode
acceptEdits` removes the per-edit "1. Yes" prompt that every Chapter-2 edit had to answer; the
LSP-recommendation / session-survey / "what's new" popups are disabled via settings/env where possible
(**[verify]** exact keys) or handled in the controller (5.4). `acceptEdits` covers *edits only* — for
`Bash`/MCP add `--allowedTools` or use `--dangerously-skip-permissions` in a throwaway sandbox.

### 4.3 Features with NO non-interactive path — this is what the REPL controller is FOR **[doc]**
Genuinely TTY-only, no structured path: the **`/theme`** and **`/output-style`** interactive pickers, the
**`/agents`** interactive list, and the **slash-command menu** fuzzy picker. For these you either pass
config up front (settings/flags) or drive a real TUI (Chapter 5). Note: ordinary **LSP diagnostics are NOT
in this list** — they flow fine in a non-interactive edit; we proved that. The LSP *navigation tool*
(definition/hover) is model-invoked and works headlessly if the model calls it.

---

## Chapter 5 — OUR primary design: a closed-loop interactive-REPL controller (tmux)

This is the build. We drive interactive REPL CLIs, so this controller — not the escape hatch — is the
deliverable. Two moves turn a flaky open-loop driver reliable: **(5.0) remove the avoidable interruptions at
launch**, and **(5.2) replace `sleep` with an observed idle signal.**

### 5.0 Tame the REPL at launch (remove avoidable interruptions) **[verify]**
Half of Chapter 3 was self-inflicted — dialogs the controller then had to fight. Eliminate them at LAUNCH so
the happy path has none:
- **Permission dialog (the biggest one):** launch `claude --permission-mode acceptEdits` (auto-accept edits),
  or `--dangerously-skip-permissions` in a throwaway sandbox. Removes the per-edit "1. Yes" prompt that every
  Chapter-2 edit had to answer. **[verify: confirm the flag applies to the interactive REPL, not only `-p`]**
- **Popups (LSP-recommendation / session survey / "what's new"):** disable via `settings.json`/env where
  possible (**[verify]** the keys); otherwise dismiss in the controller via the expect-alternation (5.4).
  Whatever you kill at launch you don't have to detect.
- **Never send slash-commands via `send-keys`** — they race into the chat box and get sent as messages
  (Ch.3 #4). Use launch flags/settings, or restart the process, instead of `/reload-plugins` etc.

### 5.1 Better tmux primitives **[doc]**
- **Send:** text then Enter as **separate** calls (avoids the race + bracketed-paste swallowing Enter):
  `send-keys -l "text"` then `send-keys Enter`. Clear stale input first with `send-keys C-u`.
- **Capture cleanly:** `capture-pane -p -J` (`-J` rejoins wrapped lines; **omit `-e`** so tmux strips ANSI
  for you). Scrollback: `capture-pane -p -J -S -` (history) or `-S -200`.
- **Pin width** once (`resize-window -x 120`) so wrap points — and your regexes — are stable.
- **Stream instead of poll:** `pipe-pane -O 'cat >> /tmp/agent.stream'` tees raw pane output to a file
  (you handle ANSI on the consumer side).
- **Event-driven wake (best, but best-effort):** if the app rings the bell on turn-complete,
  `set-option -g monitor-bell on; set-hook -g alert-bell 'run-shell "tmux wait-for -S idle"'`, then the
  controller blocks on `tmux wait-for idle`. **Caveats:** (1) only works if Claude actually emits `\a` on
  completion — unconfirmed (verify-list #5); (2) signal-before-wait race — if the bell fires before the
  controller reaches `wait-for`, the wake is lost and you hang to timeout. Mitigate by creating a
  **per-turn unique channel before sending input** (not a global `idle`), and **always keep a polled
  `wait_idle()` fallback**. Don't ship bell-only.
- **Control mode** (`tmux -CC`) emits `%output`/`%begin`/`%end` as a parseable async feed — the robust
  substrate for a real driver (it's how iTerm2 drives tmux).

### 5.2 Idle detection — the core, best-to-worst **[doc]**
- **(c) App sentinel/marker** — match a stable ready-prompt the app prints. Best if it exists.
- **(a) Ready-regex poll** — `capture-pane` then test the **last non-empty line** against a prompt regex.
- **(b) Output-quiescence** — declare idle when the screen hash is unchanged for `quiet_ms`.
- **(d) Spinner exclusion** — strip spinner glyphs (`⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏`, `|/-\`) before hashing, else animation
  reads as perpetual activity and a prompt regex can match the spinner's line.

Reference idle loop (bash; combine a + b + d):
```bash
wait_idle() {  # target  ready_regex  quiet_ms  timeout_s    (GNU date %3N; BusyBox/macOS lack it)
  local t=$1 re=$2 quiet=${3:-700} to=${4:-120}
  local deadline=$(( $(date +%s) + to )) last="" since=$(date +%s%3N)
  while (( $(date +%s) < deadline )); do
    # Normalize EVERYTHING volatile so animation != activity: spinner glyphs, the elapsed-seconds
    # counter, token counts, the interrupt hint. (The '-' MUST stay last in the class, else it's a range.)
    local now; now=$(tmux capture-pane -p -J -t "$t" | sed -E \
      's/[⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏|/\\-]//g; s/[Bb]rewed for [0-9]+s//g; s/[0-9]+ tokens//g; s/esc to interrupt//g')
    # (a) ready prompt on the LAST NON-EMPTY line (capture-pane pads the screen with blank lines):
    if printf '%s' "$now" | grep -E '.' | tail -n1 | grep -qE "$re"; then return 0; fi
    # (b) quiescence: normalized screen unchanged for quiet_ms:
    if [[ "$now" == "$last" ]]; then (( $(date +%s%3N)-since >= quiet )) && return 0
    else last="$now"; since=$(date +%s%3N); fi
    sleep 0.1
  done
  return 1   # timed out — still busy (do NOT treat as idle)
}
```
> Two bugs this version fixes (found in review): the original tested `tail -n1` on a screen that
> `capture-pane` pads with blanks (so it tested an empty line — use **last non-empty**), and it only
> stripped spinner *glyphs* while Claude's status line also animates an elapsed-seconds counter / token
> count / "esc to interrupt" — any of which reset the quiescence timer forever, silently degrading the
> loop back to a fixed sleep. Normalize all of it before comparing.

### 5.3 Controller architecture (Python / libtmux preferred over shelling out) **[doc]**
```python
class Controller:                       # libtmux pane wrapper
    def send(self, text):
        self.pane.send_keys("\x15", enter=False)   # C-u clear (idempotent)
        self.pane.send_keys(text, enter=False)     # literal text
        self.pane.enter()                          # Enter separately
    def wait_idle(self, timeout=120, quiet=0.7): ...   # ready-marker, else quiescence+spinner-exclusion
    def expect(self, pattern, timeout=60): ...         # poll capture until pattern or timeout
    def read_new(self): ...   # back this on the `pipe-pane` stream, NOT capture-pane hashes — a hash
                              # tells you THAT the screen changed, not WHAT's new, and fast/scrolled
                              # output is lost between snapshots (Ch.3 #6). pipe-pane tees every byte.
```
Handle popups as an **expect-alternation**: after each `send`, branch on `{ready, dialog_A, dialog_B,
timeout}` and run a dismiss-handler before continuing (don't assume one turn = one prompt).

### 5.4 Gotchas to bake in **[doc][fact]**
text-then-Enter race; bracketed paste; ghost/auto-suggest text (match **last line only**, clear with
`C-u`/`Escape`); pin terminal width + always `-J`; multiple dialogs; idempotency (clear input before send,
re-establish "ready" on retry rather than blind re-send). Slash commands: **don't** send via `send-keys`
(they race into chat) — prefer flags/settings, or restart the process.

---

## Chapter 6 — Verification channels (how to KNOW what happened)

Never trust the model's prose or a transient UI counter. Rank of trust **[fact]**:
1. **`stream-json` `result`/`tool_use` events** (headless) — machine-readable source of truth. **[doc]**
2. **`~/.claude/debug/<id>.txt`** — `grep` for `Received diagnostics … N diagnostic(s)`,
   `Starting LSP server instance`, `Skipping empty diagnostics`. This caught a real bug. **[fact]**
3. **Direct protocol driver** (speak LSP JSON-RPC straight to the server) — isolates server-vs-client.
   The bug-revealing test: send `didOpen` **and an incremental `didChange`**, not `didOpen` alone. **[fact]**
4. **`capture-pane` / model reply** — lowest trust; use only to confirm UX, never as proof.

> War story that justifies the ranking: the LSP unit smoke test (which only sent `didOpen`) passed, but the
> live `--debug` log showed `Skipping empty diagnostics` — Claude sends **incremental** `didChange`
> (a range + the edited fragment, not the whole file), and the server was re-parsing the fragment. The fix
> was to maintain the document buffer and `apply_change()` each delta. Only the real-protocol channel
> exposed it. **[fact]**

---

## Chapter 7 — Next-session implementation plan

**Goal.** A small, reusable controller to drive **interactive REPL CLIs** (here: `claude`) for QA of this
marketplace — closed-loop, no Agent SDK.

**Build order:**
1. **`replctl/Controller` (Python, PRIMARY — Chapter 5).** The interactive-REPL driver (libtmux): launch the
   session with `--permission-mode acceptEdits` (5.0); `send()` = clear input → literal text → **separate**
   Enter; `wait_idle()` = ready-marker → quiescence with volatile-text normalization (NO fixed sleep);
   `expect(pattern)`; `read_new()` backed by `pipe-pane`; popup expect-alternation (5.4); pinned pane width.
2. **`headless_run()` (optional helper — Chapter 4 escape hatch; NO SDK).** Only for a target CLI that has a
   structured mode: spawn `claude -p --output-format stream-json --verbose`, parse stdout, return on the
   `{"type":"result"}` event (treat stdout-closing-first as failure). Not our main path.
3. **Verifiers (Chapter 6).** `debug_events(session_log, patterns)` grep helper; `lsp_probe(server_path,
   text, changes)` speaking LSP over stdio (Appendix 1) — the load-bearing case is an incremental `didChange`.

**Validate it against THIS repo (self-test):**
- Drive the REPL: launch `claude --debug --permission-mode acceptEdits` in tmux (Ch.0.5) against the
  `calc.py` fixture (Ch.0.4). Via the Controller: `send("Use the Edit tool to append # x as the last line of
  /root/test/calc.py. Do not ask questions, just do it.")`, `wait_idle()`, then
  `send("List the language-server diagnostics for calc.py.")`, `wait_idle()`.
- Assert via the debug log `Received diagnostics … 1 diagnostic(s)` AND via `lsp_probe` that `example_lsp`
  reports `undefined name 'undefined_var'` after an **incremental** `didChange`.
- This reproduces, deterministically and closed-loop, the exact flow that took dozens of flaky tmux pokes.

**Acceptance criteria:**
- [ ] Zero `sleep`-as-synchronization: turn-completion detected via an **observed idle signal** (ready-marker
      / quiescence); the optional headless helper uses the `result` event.
- [ ] No permission dialog is ever waited on — removed at launch via `--permission-mode acceptEdits`.
- [ ] The `Controller` detects idle without a fixed sleep AND survives a popup mid-flow (expect-alternation).
- [ ] A single self-test command edits `calc.py`, confirms the diagnostic via the debug log AND `lsp_probe`,
      and exits non-zero on any failure.
- [ ] All "verify before trusting" items in the Appendix are confirmed against current docs.

---

## Appendix

### Appendix 1 — Verbatim command reference (everything used this session) [fact]
```bash
# discover
docker ps --format '{{.Names}}\t{{.ID}}\t{{.Image}}'
docker exec qa-claude tmux ls
docker exec qa-claude tmux list-panes -t 0 -F '#{session_name}:#{window_index}.#{pane_index} cmd=#{pane_current_command} path=#{pane_current_path}'
# input
docker exec qa-claude tmux send-keys -t 0:0.0 -l "TEXT"
docker exec qa-claude tmux send-keys -t 0:0.0 Enter          # also: Down Escape C-u
# output (visible screen only)
docker exec qa-claude tmux capture-pane -t 0:0.0 -p | tail -20
# debug-log ground truth
docker exec qa-claude bash -lc 'LOG=$(ls -t ~/.claude/debug/*.txt|head -1); grep -iE "lsp|diagnostic|publishdiag" "$LOG" | tail'
# restart the session reliably
docker exec qa-claude bash -lc 'pkill -f "claude"'; sleep 3
docker exec qa-claude tmux send-keys -t 0:0.0 -l "claude --debug"; docker exec qa-claude tmux send-keys -t 0:0.0 Enter
# direct LSP probe (bypass model+TUI) — COMPLETE, runnable. The incremental didChange is the load-bearing part.
docker exec qa-claude bash -lc 'SRV=$(find ~/.claude/plugins -name "*.py" -path "*lsp-example-multi*"|head -1); uv run --no-project python - "$SRV" <<"PYEOF"
import subprocess, json, sys
srv=sys.argv[1]
def frame(m):
    d=json.dumps(m).encode(); return b"Content-Length: %d\r\n\r\n"%len(d)+d
def rd(f):
    h={}
    while True:
        l=f.readline()
        if not l: return None
        l=l.decode().rstrip("\r\n")
        if l=="": break
        k,v=l.split(":",1); h[k.strip().lower()]=v.strip()
    return json.loads(f.read(int(h["content-length"])))
p=subprocess.Popen(["uv","run","--no-project",srv,"--lang","python"],
                   stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
text="def add(a, b):\n    return a + b\n\nprint(undefined_var)\n"
p.stdin.write(frame({"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}))
p.stdin.write(frame({"jsonrpc":"2.0","method":"textDocument/didOpen","params":{"textDocument":{
    "uri":"file:///c","languageId":"python","version":1,"text":text}}}))
p.stdin.flush(); rd(p.stdout)                       # initialize result
print("didOpen:", [d["message"] for d in rd(p.stdout)["params"]["diagnostics"]])
# INCREMENTAL didChange (range + fragment, NOT the whole file) — this is what Claude actually sends:
p.stdin.write(frame({"jsonrpc":"2.0","method":"textDocument/didChange","params":{
    "textDocument":{"uri":"file:///c","version":2},
    "contentChanges":[{"range":{"start":{"line":4,"character":0},"end":{"line":4,"character":0}},"text":"# appended\n"}]}}))
p.stdin.flush()
print("incremental didChange:", [d["message"] for d in rd(p.stdout)["params"]["diagnostics"]])
# PASS = both lines show ["undefined name '"'"'undefined_var'"'"'"]
PYEOF'
```

### Appendix 2 — Sources
**Claude Code (CLI; headless escape hatch only — we do NOT use the Agent SDK):**
- Headless / print mode — https://code.claude.com/docs/en/headless.md
- Permission modes — https://code.claude.com/docs/en/permission-modes.md
- CLI reference / env vars — https://code.claude.com/docs/en/cli-reference.md , /env-vars.md

**tmux / terminal automation:**
- tmux(1) man — https://man7.org/linux/man-pages/man1/tmux.1.html (`send-keys -l`, `capture-pane -p/-J/-e/-S/-E`, `pipe-pane`, `wait-for`)
- tmux Control Mode — https://github.com/tmux/tmux/wiki/Control-Mode
- tmux hooks/notifications — https://deepwiki.com/tmux/tmux/7.2-hooks-and-notifications
- pexpect — https://pexpect.readthedocs.io/en/stable/overview.html , /api/pexpect.html
- libtmux — https://libtmux.git-pull.com/quickstart/ , /topics/pane_interaction.html , /api/panes.html

### Appendix 3 — "Verify before trusting" — open questions for the implementing session **[verify]**
1. Exact `--output-format stream-json` event schema in the *current* CLI (field names of the `result`
   event; whether `--verbose`/`--include-partial-messages` are required). Confirm via a live
   `claude -p … --output-format stream-json` run.
2. **The key lever:** whether `--permission-mode acceptEdits` (and the exact value set) suppresses the edit
   dialog in the **INTERACTIVE REPL**, not just `-p`. This is the single biggest reliability win (Ch.5 5.0).
3. Which TUI popups (LSP-recommendation, session survey, "what's new") can be disabled via `settings.json` /
   env for an automated interactive run — and the exact keys.
4. The env-var names for suppressing interrupts / faster startup (`--bare`, any `CLAUDE_CODE_*`) — names
   were reported by a research agent and are not yet eyeballed in docs.
5. Whether Claude rings the terminal **bell** on turn-complete (enables the `wait-for` event-driven wake);
   if not, default the tmux controller to quiescence+ready-marker.
6. **Auth:** how `claude -p` authenticates in the target container — `ANTHROPIC_API_KEY` env vs an OAuth
   login (`claude /login` / `setup-token`). A fresh box with no credentials fails before any `result`.
   (Bootstrapped in Chapter 0.2 but confirm the headless path honors your chosen method.)
7. **CLI floor:** `claude >= 2.1.157` for plugin auto-enable; older CLIs silently load no plugin.
```
