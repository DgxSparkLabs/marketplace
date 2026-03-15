---
trigger: always_on
description: "Search for existing solutions before building custom code — don't reinvent the wheel"
---

## Prior Art

Before building anything non-trivial, ALWAYS search for existing solutions first. The default assumption is that someone has already solved this problem — your job is to prove otherwise before writing custom code.

### When to search

Search for prior art whenever you are about to:

- Write a new utility, helper, or abstraction (string manipulation, date parsing, retry logic, etc.)
- Implement a pattern you haven't seen in this codebase before (auth flow, pagination, caching, rate limiting, etc.)
- Solve a problem that feels general rather than specific to this project
- Add a new dependency or integration (API client, file format parser, protocol handler, etc.)
- Build a CLI tool, script, or automation that others likely need too
- Fix a bug that seems like it would affect many users of a library or framework

Do NOT search when the task is clearly project-specific (renaming a variable, fixing a typo, adjusting business logic unique to this project).

### What to search for

1. **In the codebase first** — search the project for existing utilities, helpers, or patterns that already solve the problem. Check shared/utils directories, existing dependencies, and internal libraries.
2. **In the project's dependencies** — the library you need may already be installed. Check package.json, Cargo.toml, requirements.txt, go.mod, etc. before adding anything new.
3. **On the web** — search for established libraries, packages, or well-known approaches using the `duckduckgo-search` skill. Look for:
   - Popular, maintained packages on npm/PyPI/crates.io/etc.
   - Stack Overflow answers with high vote counts
   - Official documentation or guides from the framework/language
   - Blog posts or articles describing battle-tested approaches
4. **On GitHub** — search for repositories with the `github-search` skill. It returns stars, license, language, and last-updated info to help you triage. Explore the top repos by reading their READMEs, browsing source code, and checking issues for known gotchas.
5. **On YouTube** — search with the `youtube-search` skill when the topic benefits from visual or step-by-step explanation, architecture walkthroughs, or conference talks from library authors.
6. **In documentation** — check if the framework or language has a built-in way to do what you need. Many problems are solved by standard library functions that are easy to overlook.

### How to evaluate what you find

Not all existing solutions are worth using. Evaluate:

- **Maintenance status** — is it actively maintained? When was the last commit/release? Are issues being addressed?
- **Adoption** — how many downloads/stars/dependents? A widely-used package is more battle-tested.
- **Scope fit** — does it solve your exact problem, or would you pull in a large dependency for one small feature? Prefer lightweight, focused packages.
- **License compatibility** — is the license compatible with the project?
- **Quality** — does the code look well-written? Does it have tests? Does it handle edge cases?
- **Security** — any known vulnerabilities? Check advisories.

### Decision framework

After searching, you will be in one of these situations:

1. **Exact match exists in the codebase** — use it. Do not duplicate.
2. **A well-maintained library solves it** — prefer using it over writing custom code, unless the dependency cost is disproportionate to the problem.
3. **Partial solutions exist** — adapt or extend what exists rather than starting from scratch. Mention what you found and why you built on it.
4. **Nothing suitable exists** — build it, but document that you searched and explain why existing options were insufficient.

### What to tell the user

ALWAYS briefly report what you found, even if you end up building custom code:

- "Found X in the codebase at path/to/file — reusing it."
- "The project already depends on library Y which has this built in — using Y.method()."
- "Searched for Z — found libraries A and B but neither handles [specific requirement]. Building a focused solution."
- "This is a common pattern — using the well-established approach from [source]."

NEVER silently write custom code for a problem that has a well-known, battle-tested solution. The user deserves to know you checked.
