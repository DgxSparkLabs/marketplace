# agent-example

Reference plugin for the **agent** (sub-agent) construct type. Copy this directory to scaffold your own.

## What it does

Ships an agent named `notebook-reviewer` with a skeptical-peer-reviewer system prompt. The user can invoke it via Claude Code's agent picker (`--agent notebook-reviewer` or via `/agents`) when they want a critical review of a notebook entry.

Install:
```
/plugin install agent-example@dgxsparklabs-marketplace
```

## File-by-file walkthrough

```
agent-example/
├── .claude-plugin/plugin.json    ← minimal manifest (no "agents" field needed)
├── agents/
│   └── notebook-reviewer.md      ← agent definition (filename = agent name)
└── README.md
```

**Auto-discovery:** Claude Code automatically picks up any `agents/*.md` files in the plugin root — you do NOT need to declare an `agents` field in `plugin.json`. (You can add `"agents": ["./custom/path"]` to override the default location, but for the standard `agents/` directory, omit the field entirely.)

The `agents/<name>.md` file uses YAML frontmatter for metadata (name, description, optionally `tools` to restrict which tools the agent can use) and a markdown body that becomes the agent's system prompt.

## Agent vs skill vs command

- **Agent**: persistent persona with its own system prompt and scoped tool access. Invoked when you want Claude to "be" something else for a task.
- **Skill**: domain expertise loaded on demand. Doesn't change Claude's persona.
- **Command**: one-shot prompt for a deterministic task.

## To make your own agent from this template

1. `cp -r agents/example agents/my-agent`
2. Rename, edit `.claude-plugin/plugin.json` and the `agents/*.md` file.
3. `uv run scripts/generate_manifest.py` and commit.

See `docs/ADDING_AN_AGENT.md` for full conventions.
