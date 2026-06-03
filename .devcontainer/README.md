# .devcontainer/

A pre-baked development + QA environment for this repo. Opening the marketplace in VS Code (or any tool that implements the [Dev Containers spec](https://containers.dev/)) builds a container with every CLI and library needed to walk through `docs/TEST_YOURSELF.md` and develop against the generator + tests.

## What you get

| Tool | Purpose | Source |
|---|---|---|
| `claude` | The Claude Code CLI — needed for every Claude QA cell | [official Anthropic feature](https://github.com/anthropics/devcontainer-features/tree/main/src/claude-code) |
| `node` 20 | Required by `claude`; also matches CI base image | [dev container feature](https://github.com/devcontainers/features/tree/main/src/node) |
| `python` 3.12 | Base interpreter; deps come from PEP 723 inline metadata via `uv run` | python feature |
| `uv` | Canonical Python tool per `AGENTS.md` — runs every PEP 723 script in `scripts/`, `tests/`, and `tests/fixtures/claude-stub/`. Flask for the hermetic stub is declared in the stub's own PEP 723 header. | `astral.sh/uv/install.sh` in `post-create.sh` |
| `git` + `gh` | Branch ops + PR review | dev container features |

VS Code extensions that auto-install: Python + Pylance, Even Better TOML, YAML, GitHub Actions, GitHub PR. The Claude Code VS Code extension is added automatically by the official feature.

Forwarded ports: **8088** (the F5 sentinel stub) and **8089** (the F7/F9 body-dumper stub). Both are silent on auto-forward — they appear in the Ports panel but VS Code does not pop a notification.

## Persistence

Claude's auth + settings live at `~/.claude` inside the container. The config is mounted as a named docker volume `claude-code-config-${devcontainerId}` so rebuilds keep your sign-in. Per-project isolation: the `${devcontainerId}` variable scopes the volume to *this* repo's container, so opening another marketplace clone won't share state.

## Open the container

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
2. Open this repo in VS Code.
3. When prompted, click **Reopen in Container**. Or run `Dev Containers: Reopen in Container` from the Command Palette.
4. First build pulls features and runs `post-create.sh` — a few minutes. Subsequent reopens are fast.
5. Open a terminal inside VS Code (`` Ctrl+` ``). Run `claude` to sign in.

## Operator QA flow

After the container is up:

```bash
# 1. Confirm everything is wired (this prints at end of post-create.sh; re-run anytime)
bash .devcontainer/post-create.sh

# 2. Optional — start the hermetic stub for F5/F7/F9 verification
uv run tests/fixtures/claude-stub/stub.py &
export ANTHROPIC_BASE_URL=http://127.0.0.1:8088
export ANTHROPIC_AUTH_TOKEN=stub

# 3. Walk through the Claude section of docs/TEST_YOURSELF.md
```

## Why not Codex / Gemini / Cursor / Windsurf / Devin CLIs

Scope is the Claude QA arc + marketplace dev. Adding the other 5 platform CLIs would balloon the image and most of them prefer their own native install paths anyway. When the next platform's QA cycle starts, either:

- add an opt-in feature flag to this devcontainer, or
- create a sibling `.devcontainer/<platform>/` config with that CLI

Both patterns are first-class in the dev containers spec.

## References

- [containers.dev — devcontainer.json schema](https://containers.dev/implementors/json_schema/)
- [code.claude.com — dev containers guide](https://code.claude.com/docs/en/devcontainer)
- [anthropics/devcontainer-features — claude-code](https://github.com/anthropics/devcontainer-features/tree/main/src/claude-code)
- [Reference Anthropic devcontainer](https://github.com/anthropics/claude-code/tree/main/.devcontainer) (firewall + persistent volumes + Zsh)
