# Adding a Monitor

> **Experimental construct.** The plugin.json field is `experimental.monitors`, reflecting that the API may change.

Monitors are background processes that run on an interval and surface output to Claude on demand. Use them for periodic observation (disk, network, process, queue health).

For the file structure, read [`monitors/example-monitor/README.md`](../monitors/example-monitor/README.md).

## Workflow

1. **Copy the example**:
   ```bash
   cp -r monitors/example-monitor monitors/my-monitor
   ```

2. **Edit**:
   - `monitors/my-monitor/.claude-plugin/plugin.json` — set `name` to `monitor-my-monitor`.
   - `monitors/my-monitor/monitors/monitors.json` — declare your monitor under the `monitors` object. Each entry has `command`, `args`, `intervalSeconds`, and `description`.

3. **Pick a sensible interval**. Too frequent wastes resources; too rare misses events. Default to minutes, not seconds.

4. **Regenerate and validate**:
   ```bash
   uv run scripts/generate_manifest.py
   uv run tests/test_marketplace.py
   claude plugin validate monitors/my-monitor
   ```

5. **Commit**.

## Install path after merge

```
/plugin install monitor-my-monitor@dgxsparklabs-marketplace
```

The monitor starts running in the background once the plugin is enabled. Track Claude Code release notes for changes to the monitor API.

## Related docs

- [`CONSTRUCT_TYPES.md`](./CONSTRUCT_TYPES.md)
- [`monitors/example-monitor/README.md`](../monitors/example-monitor/README.md)
