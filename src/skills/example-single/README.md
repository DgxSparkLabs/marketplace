# skill-example-single

A working reference plugin demonstrating the **solo layout**: one plugin ships exactly one skill (`hello`) via a `SKILL.md` at the plugin root — no `skills/` subdir. Copy this directory to scaffold a one-off skill.

## What it does

After install, the plugin exposes one slash command:

```
/dgxsparklabs-skill-example-single:hello
```

The bare flat form `/hello` also resolves when unambiguous.

## Install

```
claude plugin install skill-example-single@dgxsparklabs-marketplace --scope project
```

(Install auto-enables on current CLIs. On a fork, the part after `@` is your `src/.metadata-MARKETPLACE.toml` `name`.)

## File-by-file walkthrough

```
skills/example-single/
├── .claude-plugin/
│   └── plugin.json   ← ONE optional key: "description" (the marketplace one-liner).
│                        Everything else (name, version, author) is generated —
│                        any extra key here fails validation (rule R6).
├── SKILL.md          ← the skill: frontmatter (name: hello, description: …) + prompt body
└── README.md         ← you are here
```

The generator detects "no `skills/` subdir + one root `SKILL.md`" and emits `skills: ["./"]` in the *generated* plugin manifest. The multi-skill counterpart lives at `skills/example-multi/`.

## Make your own

1. Copy this directory to `src/skills/<your-plugin>/` (kebab-case, ≤32 chars) — or run `uv run scripts/new_construct.py skill <your-plugin>`.
2. Edit `SKILL.md` (frontmatter `description:` is required) and, optionally, the one-line `description` in `.claude-plugin/plugin.json`.
3. Commit and push — CI regenerates and publishes everything.
4. Optional local gate first: `uv run scripts/tasks.py verify`.
