---
description: Minimal liveness check. Prints "pong" plus the current UTC time.
---

Run `date -u +%FT%TZ` to capture a UTC timestamp. Then print one line:

```
pong @ <UTC timestamp>
```

That is the entire command. Do not perform any other action.
