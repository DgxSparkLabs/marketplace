# hook-example-sessionend

Single-event reference plugin demonstrating the `SessionEnd` hook in isolation.

## Behavior

When a Claude session terminates, a sentinel line is appended to `/tmp/hook-fired-sessionend.log`.

## Verification

```
tail /tmp/hook-fired-sessionend.log
```

## Related

- All-events counterpart: `src/hooks/example-multi/`
- Other per-event references: `src/hooks/example-<other-event>/`
