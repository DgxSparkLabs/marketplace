---
description: "Search for existing solutions before building custom code"
alwaysApply: true
---

## Prior Art

Before building anything non-trivial, search for existing solutions first.

1. **In the codebase** — check for existing utilities, helpers, patterns.
2. **In dependencies** — check package.json/Cargo.toml/requirements.txt before adding anything new.
3. **On the web** — use `duckduckgo-search` skill for established packages and patterns.
4. **On GitHub** — use `github-search` skill for repos with stars, license, and freshness info.

**Evaluate:** maintenance status, adoption, scope fit, license, security.

**Always report** what you found: "Found X, reusing it" or "Searched for X, nothing suitable, building custom."
