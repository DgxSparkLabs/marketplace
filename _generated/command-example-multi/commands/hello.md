---
description: Prints a formatted lab-notebook header for today's UTC date.
---

Print a markdown block in this exact shape, substituting today's UTC date for `<DATE>`:

```
# Lab Notebook — <DATE>

## Entries

- [ ] (add entries here)
```

Get the date by running `date -u +%F` once. Then print the block to the user. Do not perform any other action.
