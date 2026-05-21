---
description: "Write documentation for humans — TL;DR readme, hand-holding guides, consistent terminology"
alwaysApply: true
---
## Readable Docs

Write documentation for humans who don't already understand the system.

- **README.md is a TL;DR.** What this project is, how to install/run it, and links to detailed docs. One screen of text. Not a tutorial, not a reference manual.
- **Detailed guides live in `docs/`.** One topic per file, named for what it explains (`getting-started.md`, `deployment.md`), not for who wrote it or when.
- **Hand-hold the reader.** Guides should walk a newcomer through step by step — prerequisites, exact commands, expected output, what to do if something goes wrong. Assume zero prior context.
- **Document every recurring operation.** If a task is done more than once (adding a feature, registering a resource, deploying), write a step-by-step runbook. The test: can someone who has never done it complete the task by following the doc alone?
- **Terms and style are consistent.** Define domain-specific concepts once. Use the same words everywhere — don't alternate between synonyms. Formatting, headings, and command syntax should be uniform across all docs.
- **Docs track code.** When behavior changes, update the relevant doc in the same commit. A doc that describes yesterday's behavior is worse than no doc.
- **No orphans.** Every doc is reachable from README.md or another doc. If it has no inbound link, it won't be found. Mirror code structure — if the code has modules, docs explain each one.
