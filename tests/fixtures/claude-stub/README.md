# Claude headless QA stub

A ~90-line Flask server that pretends to be the Anthropic Messages API.
It lets `claude` run without an Anthropic account, which makes
`F5` (hook firing), `F7` (slash command resolution), and `F9`
(output-style application) observable in a hermetic container or in
CI — no auth, no real LLM, no flakiness.

`F4` (theme visual distinctness) still needs a human eye, because it's
a TTY paint operation with no observable in the request stream.

## Files

| File | Purpose |
|---|---|
| `stub.py` | Returns Anthropic-shape responses on port `8088` (`STUB_PORT` overrides). Use for F5 and F7 — hook sentinels + access log are enough. |
| `stub_body_dumper.py` | Same wire behavior on port `8089`, but additionally writes every request body to `/tmp/stub-bodies.log` (`STUB_BODIES_LOG` overrides). Use for F9 (need to grep the captured `system[]` array). |

## Quick start

```bash
# 1. Install the prereqs.
pip install flask

# 2. Run the stub.
python3 tests/fixtures/claude-stub/stub.py &
sleep 1

# 3. Point Claude at the stub.
export ANTHROPIC_BASE_URL=http://127.0.0.1:8088
export ANTHROPIC_AUTH_TOKEN=stub          # any non-empty value works
export API_TIMEOUT_MS=20000               # fail fast on stub bugs

# 4. Run any normal Claude command.
echo "hello stub" | claude --print
```

## Env vars

Both scripts honor:

| Var | Default | Purpose |
|---|---|---|
| `STUB_HOST` | `127.0.0.1` | Use `0.0.0.0` inside a container if accessed from the host. |
| `STUB_PORT` | `8088` (stub) / `8089` (dumper) | Bind port. |
| `STUB_LOG` | `/tmp/stub-server.log` | Access log; truncated on each start. |
| `STUB_BODIES_LOG` | `/tmp/stub-bodies.log` | Dumper-only: full request bodies. |

## Origin

Empirical feasibility research at
`docs/research/claude-headless-qa/RESEARCH.md` confirmed that Claude
Code accepts any `ANTHROPIC_BASE_URL` with no remote validation, and
the stub recipe was developed there before being lifted into this
canonical fixture location. The CI workflow at
`.github/workflows/compat-headless-claude.yml` consumes these scripts
directly.
