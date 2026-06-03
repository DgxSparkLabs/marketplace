# hook-example-notification

Single-event reference plugin demonstrating the `Notification` hook in isolation.

## Behavior

When Claude raises a notification (e.g. a tool-permission prompt), a sentinel line is appended to `/tmp/hook-fired-notification.log`.

## Verification

```
tail /tmp/hook-fired-notification.log
```

## Related

- All-events counterpart: `src/hooks/example-multi/`
- Other per-event references: `src/hooks/example-<other-event>/`
