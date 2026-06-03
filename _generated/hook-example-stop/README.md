# hook-example-stop

Single-event reference plugin demonstrating the `Stop` hook in isolation.

## Behavior

At the end of every assistant turn, a sentinel line is appended to `/tmp/hook-fired-stop.log`.

## Verification

```
tail /tmp/hook-fired-stop.log
```

## Related

- All-events counterpart: `src/hooks/example-multi/`
- Other per-event references: `src/hooks/example-<other-event>/`
