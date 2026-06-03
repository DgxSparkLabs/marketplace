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
| `Dockerfile` | Containerized stub — see "Docker workflow" below. Composes with the `qa-claude` Setup option B container via `--network container:claude-stub`. |

## Quick start

Both stubs are self-bootstrapping PEP 723 scripts. `uv` reads the inline metadata header, fetches Flask into an ephemeral environment, and runs the stub — no `pip install`, no apt package, no virtualenv to activate.

```bash
# 1. Start the stub (first run downloads Flask; subsequent runs are instant).
uv run tests/fixtures/claude-stub/stub.py &
sleep 1

# 2. Point Claude at the stub.
export ANTHROPIC_BASE_URL=http://127.0.0.1:8088
export ANTHROPIC_AUTH_TOKEN=stub          # any non-empty value works
export API_TIMEOUT_MS=20000               # fail fast on stub bugs

# 3. Run any normal Claude command.
echo "hello stub" | claude --print
```

The shebang line `#!/usr/bin/env -S uv run --quiet` also lets you execute the file directly (`./tests/fixtures/claude-stub/stub.py`) on any host with `uv` on PATH.

## Env vars

Both scripts honor:

| Var | Default | Purpose |
|---|---|---|
| `STUB_HOST` | `127.0.0.1` | Use `0.0.0.0` inside a container if accessed from the host. |
| `STUB_PORT` | `8088` (stub) / `8089` (dumper) | Bind port. |
| `STUB_LOG` | `/tmp/stub-server.log` | Access log; truncated on each start. |
| `STUB_BODIES_LOG` | `/tmp/stub-bodies.log` | Dumper-only: full request bodies. |

## Docker workflow — for use alongside the `qa-claude` Setup option B

If you want the captured request bodies on your host filesystem (so you can `grep` them outside the container), or if you're orchestrating multiple containers, run the stub as its own Docker image. The composition is two `docker run` calls — one for the stub, one for the qa-claude container that joins the stub's network namespace so `localhost:8089` inside qa-claude reaches the stub natively.

> **Key design point.** The stub container does NOT need host port forwarding for the primary workflow. qa-claude joins the stub's network namespace via `--network container:claude-stub` and reaches the stub at `127.0.0.1:8089` directly via the shared loopback interface. The bind-mounted log dir is how the operator observes captured bodies from the host. Host port forwarding (`-p 8089:8089`) is OPTIONAL and only needed if you also want to `curl` the stub from the host shell.

### Step 1 — build the stub image (once)

```bash
docker build -t claude-stub tests/fixtures/claude-stub/
```

`uv` is already in the base image; the first build also fetches Flask via PEP 723 into the image's package cache. Subsequent rebuilds reuse it.

### Step 2 — run the stub with the log dir bind-mounted (no host port needed)

POSIX:

```bash
mkdir -p .stub-logs

docker run --rm -d \
  --name claude-stub \
  -v "$PWD/.stub-logs:/var/log/stub" \
  claude-stub
```

PowerShell:

```powershell
New-Item -ItemType Directory -Force .stub-logs | Out-Null

docker run --rm -d `
  --name claude-stub `
  -v "${PWD}/.stub-logs:/var/log/stub" `
  claude-stub
```

Logs land at `./.stub-logs/stub-server.log` (access) and `./.stub-logs/stub-bodies.log` (captured request bodies). `.stub-logs/` is gitignored.

To run the plain stub (port 8088, no body capture) instead of the dumper, override `CMD`:

```bash
docker run --rm -d --name claude-stub \
  -v "$PWD/.stub-logs:/var/log/stub" \
  claude-stub uv run /stub/stub.py
```

### Step 3 — compose with qa-claude (Setup option B)

Start the stub first (Step 2). Then start qa-claude with `--network container:claude-stub` so it shares the stub's network namespace — `127.0.0.1:8089` inside qa-claude is the stub. **qa-claude cannot have its own `-p` mappings when sharing a network namespace.**

POSIX:

```bash
docker run --rm -it \
  --name qa-claude \
  --network container:claude-stub \
  -v "$PWD:/workspace/marketplace" \
  -w /workspace/marketplace \
  -e ANTHROPIC_BASE_URL=http://127.0.0.1:8089 \
  -e ANTHROPIC_AUTH_TOKEN=stub \
  node:20 bash
```

PowerShell:

```powershell
docker run --rm -it `
  --name qa-claude `
  --network container:claude-stub `
  -v "${PWD}:/workspace/marketplace" `
  -w /workspace/marketplace `
  -e ANTHROPIC_BASE_URL=http://127.0.0.1:8089 `
  -e ANTHROPIC_AUTH_TOKEN=stub `
  node:20 bash
```

Inside qa-claude:

```bash
# One-time install
npm install -g @anthropic-ai/claude-code
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Run any claude command — request bodies stream to .stub-logs/stub-bodies.log on host
echo "hello stub" | claude --print
```

### Step 4 — observe captured bodies from the host

```bash
# Live tail
tail -f .stub-logs/stub-bodies.log

# Grep for a specific slash form (post-2026-05-28 unique-per-plugin shape)
grep -F '/dgxsparklabs-skill-example-single:hello' .stub-logs/stub-bodies.log
# Or the multi-skill plugin's slash form:
grep -F '/dgxsparklabs-skill-example:notebook' .stub-logs/stub-bodies.log

# Truncate between probes
: > .stub-logs/stub-bodies.log
```

### Step 5 — teardown

```bash
docker stop claude-stub                    # auto-removed because of --rm
# qa-claude exits when you `exit` the shell, also --rm
```

### Optional — expose the stub to the host (for `curl` debugging)

Only needed if you want to hit the stub from a process running directly on your host (not inside any container). Add `-p 8089:8089` to the Step 2 stub command:

```bash
docker run --rm -d --name claude-stub \
  -p 8089:8089 \
  -v "$PWD/.stub-logs:/var/log/stub" \
  claude-stub
```

Then from host: `curl http://127.0.0.1:8089/v1/models`.

> **Gotcha — Docker Desktop on Windows + Cursor IDE port conflict.** Cursor IDE has been observed binding `127.0.0.1:8089` on some Windows setups, which collides with the Docker Desktop port proxy. Symptom: `curl: (52) Empty reply from server` from host even though the stub Flask is serving correctly inside the container. Diagnose with `netstat -ano | findstr 8089` (PowerShell) or `netstat -ano | grep 8089` (Git Bash) — if you see two listeners (one `0.0.0.0:8089` from `com.docker.backend` and one `127.0.0.1:8089` from `Cursor.exe`), Cursor is intercepting connections. Workaround: use `-p 18089:8089` and `curl http://127.0.0.1:18089/...`, OR don't expose the port at all (the primary workflow above doesn't need it).

### Why share the network namespace instead of using `--link` or a user-defined network

`--network container:<name>` is the simplest pattern that keeps the stub's `127.0.0.1:8089` directly addressable from inside qa-claude. A user-defined bridge network would require Claude to address the stub as `http://claude-stub:8089` instead — works, but the `127.0.0.1:8089` form matches the operator's existing dev-container experience and the prior research's hermetic setup, so it's the lower-friction path. The shared-netns pattern also bypasses host port forwarding entirely, which sidesteps the Cursor-IDE port-conflict class.

## Origin

Empirical feasibility research at
`docs/research/claude-headless-qa/RESEARCH.md` confirmed that Claude
Code accepts any `ANTHROPIC_BASE_URL` with no remote validation, and
the stub recipe was developed there before being lifted into this
canonical fixture location. The CI workflow at
`.github/workflows/compat-headless-claude.yml` consumes these scripts
directly via `uv run` (no Docker image needed for CI).

The Docker workflow on this page was added 2026-05-27 after the
operator noted that running the body dumper from inside the operator's
session (instead of an embedded process) makes the captured-body log
easier to inspect and standardizes the multi-container workflow.
