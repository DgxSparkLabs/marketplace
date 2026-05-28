# hook-example-precompact

Single-event reference plugin demonstrating the `PreCompact` hook in isolation.

## Behavior

Before Claude compacts conversation history, a sentinel line is appended to `/tmp/hook-fired-precompact.log`.

## Verification

```
tail /tmp/hook-fired-precompact.log
```

## Related

- All-events counterpart: `src/hooks/example-multi/`
- Other per-event references: `src/hooks/example-<other-event>/`
