# hook-example-pretooluse

Single-event reference plugin demonstrating the `PreToolUse` hook in isolation, scoped to `Write|Edit` tool calls.

## Behavior

Before any `Write` or `Edit` tool call, a sentinel line is appended to `/tmp/hook-fired-pretooluse.log` with the tool name.

## Verification

```
tail /tmp/hook-fired-pretooluse.log
```

## Note on matchers

The `matcher` field is a regex on tool names. To fire on any tool, drop the matcher entirely.

## Related

- All-events counterpart: `src/hooks/example-multi/`
- Other per-event references: `src/hooks/example-<other-event>/`
