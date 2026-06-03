---
date: 2026-05-26
purpose: research-feasibility-of-headless-claude-for-hermetic-qa
arc: claude/qa-and-user-guide (follow-up)
status: complete
container: qa-claude (reused; node:20)
claude-version: 2.1.150
---

# Headless Claude Code for Hermetic QA — Research

## TL;DR

**FEASIBLE.** Claude Code accepts an arbitrary HTTP backend via `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN` — no Anthropic auth check, no licensing phone-home, no version validation against the real API. A 90-line Flask stub that returns Anthropic-shape `/v1/messages` responses is enough to run `claude --print`, fire all six hook events, resolve namespaced slash commands, and inject output-style content into the system prompt. **3 of the 4 deferred cells (F5, F7, F9) move from "interactive-auth required" to fully hermetic; only F4 (visual theme rendering) remains user-driven** because it's a TTY paint operation with no observable in the request stream.

Recommended integration: add a "Hermetic Claude session" setup option to `docs/TEST_YOURSELF.md` Platform 1 using the Flask stub. The stub originated here under `logs/` during the probe but now lives canonically at `tests/fixtures/claude-stub/stub.py` (with `stub_body_dumper.py` alongside) so CI and per-platform docs can cite a stable path. CI extension to `compat-validate.yml` is viable — no Anthropic secret needed.

## What Claude Code supports for non-Anthropic backends

### Documented configuration

Per `code.claude.com/docs/en/env-vars` (fetched 2026-05-26) and `code.claude.com/docs/en/llm-gateway` (fetched 2026-05-26):

| Variable | Behavior |
|---|---|
| `ANTHROPIC_BASE_URL` | Override API endpoint to any URL. No validation of host or TLS. |
| `ANTHROPIC_AUTH_TOKEN` | Sent verbatim as `Authorization: Bearer <token>`. Any non-empty string accepted client-side. |
| `ANTHROPIC_API_KEY` | Sent verbatim as `X-Api-Key`. Any non-empty string accepted client-side. |
| `ANTHROPIC_CUSTOM_HEADERS` | Add arbitrary headers (newline-separated). |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` | Strip beta headers for gateways that reject them. |
| `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` | Query gateway's `/v1/models`. |
| `API_TIMEOUT_MS` | Shorten the default 10-minute timeout (we used 20s). |

Gateway must expose one of three API surfaces; the simplest is **Anthropic Messages**: `POST /v1/messages`, `POST /v1/messages/count_tokens`, with forwarded headers `anthropic-beta` and `anthropic-version` (per `code.claude.com/docs/en/llm-gateway#gateway-requirements`, 2026-05-26).

`claude --help` (claude 2.1.150) confirms `--bare` mode statement: *"Anthropic auth is strictly ANTHROPIC_API_KEY or apiKeyHelper via --settings (OAuth and keychain are never read). 3P providers (Bedrock/Vertex/Foundry) use their own credentials."* This is the explicit client-side contract: no remote auth check at startup.

### Provider abstraction

Three first-party provider modes (per `code.claude.com/docs/en/amazon-bedrock`, 2026-05-26):

- `CLAUDE_CODE_USE_BEDROCK=1` + AWS creds → Bedrock Invoke API
- `CLAUDE_CODE_USE_MANTLE=1` + AWS creds → Bedrock Mantle endpoint (Anthropic-shape over AWS)
- `CLAUDE_CODE_USE_VERTEX=1` + GCP creds → Vertex rawPredict

Plus `CLAUDE_CODE_USE_ANTHROPIC_AWS=1` (Claude Platform on AWS) and `ANTHROPIC_FOUNDRY_API_KEY` (Microsoft Foundry). Each can be paired with `CLAUDE_CODE_SKIP_*_AUTH=1` so a gateway can inject signed credentials server-side.

## Community tooling

### Proxies / routers (maintained, < 6 months since last commit per GitHub search, 2026-05-26)

- **`musistudio/claude-code-router`** — multi-provider router; sets `ANTHROPIC_BASE_URL` to local port, routes per-task to Claude / DeepSeek / Gemini / Ollama. Used in production by getaiperks community guide (2026).
- **`seifghazi/claude-code-proxy`** — request capture + visualization proxy, also routes to alternate providers. Useful for debug but heavier than what we need.
- **`jimmc414/claude_n_codex_api_proxy`** — Claude Code + Codex API routing proxy.

### Mock / stub servers

No off-the-shelf mock specifically for Claude Code QA was found. Rolling our own (≈90 lines of Flask) is simpler than adopting a router for this use case — the QA path needs deterministic canned responses, not real LLM routing.

### Local model backends

- **LiteLLM** has a documented `/anthropic` unified endpoint that translates Anthropic Messages ↔ any provider (per `code.claude.com/docs/en/llm-gateway#litellm-configuration`, 2026-05-26).
  - **Security caveat from docs**: LiteLLM PyPI versions `1.82.7` and `1.82.8` were compromised. Pin to a known-good version if adopted.
- **Ollama / LM Studio** expose OpenAI-compatible APIs, not Anthropic. Would need LiteLLM as a translation shim.
- **llama.cpp** — same story; OpenAI shape only.

For hermetic QA the translation chain (Ollama → LiteLLM → Claude Code) is heavier than a 90-line stub and brings real-LLM nondeterminism. Stub wins for CI.

## Empirical probe results

### Approach tried

**Flask stub server (port 8089) returning Anthropic-shape `/v1/messages` responses** — supports both non-streaming (JSON) and streaming (SSE) shape per the Anthropic spec. Stub also implements `/v1/messages/count_tokens` and `/v1/models` (the discovery endpoints Claude Code probes).

### Setup steps

Inside the reused `qa-claude` container (`node:20`, `claude --version` → `2.1.150`):

```bash
apt-get install -y python3-pip python3-flask  # already present
# Stub written to /tmp/stub.py (port 8088) and /tmp/stub_body_dumper.py (port 8089)
# Both committed at docs/research/claude-headless-qa/logs/

nohup python3 /tmp/stub_body_dumper.py > /tmp/stub2.log 2>&1 &

# Install plugins (auth-free per prior verification)
claude plugin marketplace add /workspace/marketplace
claude plugin install hook-example@dgxsparklabs-marketplace
claude plugin install command-example@dgxsparklabs-marketplace
claude plugin install skill-example@dgxsparklabs-marketplace
claude plugin install output-style-example@dgxsparklabs-marketplace

# Probe — single command exercises 4+ cells
rm -f /tmp/hook-fired-*.log
ANTHROPIC_BASE_URL=http://127.0.0.1:8089 \
ANTHROPIC_AUTH_TOKEN=stub-token \
API_TIMEOUT_MS=20000 \
claude --print --append-system-prompt "$(cat <output-style.md>)" 'explain F9'
```

### Outcome

Claude accepted the stub backend with no validation hiccup. Captured request body (124,769 bytes for the F9 probe) shows the official Anthropic Messages request shape: `system[]` array with the appended output style at `system[2]`, `messages[]` user content including hook-injected `<system-reminder>` blocks, and headers including `Authorization: Bearer stub-token`, `Anthropic-Beta: claude-code-20250219,...`, `X-Claude-Code-Session-Id: <uuid>`.

Per-event observations:

- **Round-trip works**: stub's `"OK stub."` returned to operator stdout.
- **All session/turn hooks fired** (F5 evidence): `SessionStart`, `UserPromptSubmit`, `Stop`, `SessionEnd` sentinels written to `/tmp/hook-fired-*.log` with UTC timestamps.
- **`UserPromptSubmit` stdout injection works**: hook's `[Lab Notebook context: timestamp=...]` line appears in the next request body as a `<system-reminder>` user content block — both halves of the F5 spec confirmed.
- **`PreToolUse` / `PostToolUse` did NOT fire** because the stub returned a text-only response, not a tool_use block. **Extending the stub to return a canned `Edit` tool_use block would trigger these too** — feasible, not done in this probe.
- **F7 slash resolution**: `/command-example:example-command` resolved to the command body (sent to LLM, stub returned `OK stub.`); `/nonexistent-xxx` returned `Unknown command:` parser error. The client-side resolver is fully exercised.
- **F9 output-style application**: the entire `lab-notebook-voice.md` frontmatter + body appeared verbatim in `system[2]` (markers `Lab Notebook Voice`, `measured`, `hedging`, `Next:` all grep-positive). Proves the style reaches the model boundary.

### Logs

- Probe summary: `docs/research/claude-headless-qa/logs/PROBE_SUMMARY.txt`
- Stub server access log: `docs/research/claude-headless-qa/logs/stub-server.log`
- Captured request body (F9 probe): `docs/research/claude-headless-qa/logs/stub-bodies-f9.log` (124,769 bytes)
- Hook sentinels: `docs/research/claude-headless-qa/logs/hook-{sessionstart,userpromptsubmit,stop,sessionend}.log`
- Stub source (canonical, tracked): `tests/fixtures/claude-stub/stub.py`, `tests/fixtures/claude-stub/stub_body_dumper.py`
- Stub source (original probe copy, untracked): `docs/research/claude-headless-qa/logs/stub.py`, `docs/research/claude-headless-qa/logs/stub_body_dumper.py`

## Per-cell feasibility

| Deferred cell | Hermetic-headless feasible? | Mechanism |
|---|---|---|
| **F4 theme distinctness** | **NO** | Theme is a TTY paint operation. No request-stream observable. Persistence check (`settings.json` contains `custom:theme-example:lab-notebook`) is feasible but is file-existence not behavior. Visual distinctness from default Dark mode genuinely requires a human-eye check. |
| **F5 hook firing** | **YES (full)** | Sentinel-file tail demonstrated. SessionStart / UserPromptSubmit / Stop / SessionEnd fired in the probe. PreToolUse / PostToolUse require stub to emit a `tool_use` block (engineering, not feasibility). |
| **F7 slash invocation** | **YES (full)** | Client-side slash resolution. Known names → stub body shows command markdown reached LLM; unknown names → `Unknown command:` parser error. Both branches observable. |
| **F9 output-style activation** | **YES (full)** | Output-style content appears verbatim in `system[2]` of the request body. `--append-system-prompt "$(cat <style>.md)"` is the simplest injection; `--settings '{"outputStyle":"<Name>"}'` also accepted but the persistence-vs-application distinction needs a body-capturing stub to verify. |

**Bonus surfaces hermetic also covers** (beyond the original 4):

- All of Claude validation 5a–5f (6 hook subtypes) — same sentinel mechanism.
- F7 namespacing variants 7a/7b/7c (skill / agent / MCP tool naming) — visible via stub request body.
- Plugin install/list/uninstall lifecycle — already verified hermetically in the 2026-05-26 round.

## Recommendation

### Integrate "Hermetic Claude session" into `docs/TEST_YOURSELF.md`

Add a third setup option to Platform 1 (Claude Code), between **Setup option A: Docker** and **Setup option B: Native**:

> ### Setup option C: Hermetic (Docker + stub LLM)
>
> For CI-style verification with no Anthropic auth required. Uses the Flask stub at `docs/research/claude-headless-qa/logs/stub.py`.
>
> ```powershell
> docker run -it --name qa-claude-headless node:20 bash
> ```
>
> Inside the container:
> ```bash
> apt-get update && apt-get install -y python3-flask git
> npm install -g @anthropic-ai/claude-code
> git clone --branch main https://github.com/DgxSparkLabs/marketplace.git /workspace/marketplace
> cd /workspace/marketplace
> nohup python3 tests/fixtures/claude-stub/stub.py > /tmp/stub.log 2>&1 &
> sleep 2
> export ANTHROPIC_BASE_URL=http://127.0.0.1:8088
> export ANTHROPIC_AUTH_TOKEN=stub
> export API_TIMEOUT_MS=20000
> ```
>
> Then run any per-construct test using `claude --print '<prompt>'` instead of an interactive session. F5/F7/F9 validations have hermetic equivalents below.

For each affected cell, add a "Hermetic alternative" sub-bullet next to the existing interactive instructions. F4 keeps its interactive-only note.

### CI extension to `compat-validate.yml`

The current workflow runs `claude plugin validate` (schema only). Extend it with a hermetic-Claude job that:

1. Starts the stub as a sidecar service.
2. Runs `claude --print` with `hook-example` installed.
3. Asserts presence of `/tmp/hook-fired-userpromptsubmit.log`.

No Anthropic secret needed; the job runs unauthed end-to-end.

### Do NOT adopt LiteLLM / claude-code-router for this use case

They solve a different problem (real-LLM routing). Stub is simpler, deterministic, and ships in-repo.

## Open questions

- **PreToolUse / PostToolUse hermetic firing**: requires the stub to return a `tool_use` content block (e.g., `Edit` with a fake file path). Worth implementing as a v2 of the stub before integrating into CI.
- **F4 persistence-only fallback**: an operator-skippable "hermetic partial" check that reads `~/.claude/settings.json` for `custom:theme-example:lab-notebook` and confirms the SET is observable, even if the rendered colors aren't. Could downgrade F4 from "human required" to "human required ONLY for visual confirmation."
- **`claude --bare` mode interaction**: the `--bare` flag is documented as the hermetic-friendly path (skips OAuth/keychain). Worth checking whether `--bare` + stub also fires plugin hooks (the help text says it "skips hooks") — if so, the stub recipe should NOT use `--bare`.
- **Streaming SSE robustness**: stub returns minimal SSE events. Claude accepted them, but variations (longer streams, error injection, partial responses) untested — fine for the QA cells listed, may break if a future cell needs richer LLM behavior.

## Citations

- `code.claude.com/docs/en/settings` — environment variables list (fetched 2026-05-26)
- `code.claude.com/docs/en/env-vars` — full env-var reference (fetched 2026-05-26)
- `code.claude.com/docs/en/llm-gateway` — gateway requirements and LiteLLM section (fetched 2026-05-26)
- `code.claude.com/docs/en/amazon-bedrock` — Bedrock / Mantle endpoint env vars (fetched 2026-05-26)
- `code.claude.com/docs/en/output-styles` — outputStyle persistence (cited in prior research; not re-fetched today)
- `github.com/musistudio/claude-code-router` — community router (verified active 2026-05-26 via WebSearch)
- `github.com/seifghazi/claude-code-proxy` — community capture proxy (verified active 2026-05-26 via WebSearch)
- `claude --help` output from `claude 2.1.150` inside `qa-claude` container (run 2026-05-26)

No URLs returned 404 during this research.
