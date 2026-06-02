---
description: Minimal liveness check. Prints "pong" plus the current UTC time.
---

Run `date -u +%FT%TZ` to capture a UTC timestamp. First print this debug line exactly — it surfaces the raw arguments this command received (empty if none): `[command:ping] args=[$ARGUMENTS]`

Then print one line:

```
pong @ <UTC timestamp>
```

That is the entire command. Do not perform any other action.
