# hook-example-userpromptsubmit

Single-event reference plugin demonstrating the `UserPromptSubmit` hook in isolation.

## Behavior

Every user prompt triggers two side effects:

1. A line `[Lab Notebook context: timestamp=...]` is prepended to the prompt (Claude sees it; the user doesn't).
2. A sentinel line is appended to `/tmp/hook-fired-userpromptsubmit.log`.

## Verification

```
tail /tmp/hook-fired-userpromptsubmit.log
```

## Related

- All-events counterpart: `src/hooks/example-multi/`
- Other per-event references: `src/hooks/example-<other-event>/`
