# agent-example-multi

Reference plugin demonstrating the **multi-agent layout**: one plugin ships three sub-agents (`notebook-reviewer`, `summarizer`, `validator`) under a single `agents/` subdir.

## Slash forms (after install + enable)

Sub-agents are dispatched via the `/agents` picker:

- `dgxsparklabs-agent-example-multi:notebook-reviewer` — skeptical peer review
- `dgxsparklabs-agent-example-multi:summarizer` — TL;DR condenser
- `dgxsparklabs-agent-example-multi:validator` — fast-pass code check

## When to choose multi over single

Pick multi when you have multiple thematically related sub-agents (e.g., a code-review pipeline of distinct personas). Pick single (`src/agents/example-single/`) when you have exactly one sub-agent.

## File walkthrough

```
src/agents/example-multi/
├── .claude-plugin/plugin.json
├── agents/
│   ├── notebook-reviewer.md   ← one .md per sub-agent; frontmatter sets name/description/tools
│   ├── summarizer.md
│   └── validator.md
└── README.md
```

## Related

- Single counterpart: `src/agents/example-single/`
- Adding your own agent plugin: `docs/ADDING_A_CONSTRUCT.md`
