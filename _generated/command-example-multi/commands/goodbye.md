---
description: Prints a formatted lab-notebook closing footer with a UTC timestamp.
---

First print this debug line exactly — it surfaces the raw arguments this command received (empty if none): `[command:goodbye] args=[$ARGUMENTS]`

Then print a markdown block in this exact shape, substituting the current UTC timestamp for `<TIMESTAMP>`:

```
---
**Session closed at <TIMESTAMP>**

Next checkpoint: (set one)
```

Get the timestamp by running `date -u +%FT%TZ` once. Then print the block to the user. Do not perform any other action.
