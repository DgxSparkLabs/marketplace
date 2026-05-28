# hook-example-subagentstop

Single-event reference plugin demonstrating the `SubagentStop` hook in isolation.

## Behavior

When a sub-agent's turn ends, a sentinel line is appended to `/tmp/hook-fired-subagentstop.log`.

## Verification

```
tail /tmp/hook-fired-subagentstop.log
```

## Related

- All-events counterpart: `src/hooks/example-multi/`
- Other per-event references: `src/hooks/example-<other-event>/`
