# hook-example-sessionstart

Single-event reference plugin demonstrating the `SessionStart` hook in isolation.

## Behavior

When a Claude session begins, a sentinel line is appended to `/tmp/hook-fired-sessionstart.log`.

## Verification

```
tail /tmp/hook-fired-sessionstart.log
```

## Related

- All-events counterpart: `src/hooks/example-multi/`
- Other per-event references: `src/hooks/example-<other-event>/`
