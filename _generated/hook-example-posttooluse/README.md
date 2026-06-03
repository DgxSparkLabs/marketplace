# hook-example-posttooluse

Single-event reference plugin demonstrating the `PostToolUse` hook in isolation, scoped to `Write|Edit` tool calls.

## Behavior

After any `Write` or `Edit` tool call completes, a sentinel line is appended to `/tmp/hook-fired-posttooluse.log` with the tool name.

## Verification

```
tail /tmp/hook-fired-posttooluse.log
```

## Related

- All-events counterpart: `src/hooks/example-multi/`
- Other per-event references: `src/hooks/example-<other-event>/`
