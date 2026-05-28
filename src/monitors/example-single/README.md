# monitor-example

Reference plugin for the **monitor** construct type. Copy this directory to scaffold your own.

## What it does

Registers a background monitor named `disk-usage` that runs `df -h .` at session start. The monitor output becomes available as context Claude can query.

Install:
```
/plugin install monitor-example@dgxsparklabs-marketplace
```

> Monitors are an experimental construct in Claude Code. The plugin.json field is `experimental.monitors`, reflecting that the API may change.

## File-by-file walkthrough

```
monitor-example/
├── .claude-plugin/plugin.json         ← manifest with "experimental.monitors": "./monitors/monitors.json"
├── monitors/
│   └── monitors.json                  ← monitor definitions
└── README.md
```

### `monitors/monitors.json`

Each monitor declares:

- `command` and `args` — what to run
- `intervalSeconds` — how often
- `description` — context surfaced to Claude when the monitor's output is queried

## When to use a monitor

Monitors are right when you need periodic observation of a system (disk, network, process, queue) without having Claude poll. The monitor process runs separately and surfaces data on demand.

For one-shot inspection, a skill or command is simpler.

## To make your own monitor from this template

1. `cp -r monitors/example monitors/my-monitor`
2. Edit `.claude-plugin/plugin.json` and `monitors/monitors.json`.
3. Pick a sensible interval — too frequent wastes resources, too rare misses events.
4. `uv run scripts/generate_manifest.py` and commit.

See `docs/ADDING_A_MONITOR.md` for the full schema. Monitors are experimental; the field naming may change as the API stabilizes.
