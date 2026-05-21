# skill-creator

Create new skills, modify and improve existing skills, and measure skill performance with structured evals.

Originally from [Anthropic's official skills repository](https://github.com/anthropics/skills/tree/main/skills/skill-creator). Announced in [Improving skill-creator: Test, measure, and refine Agent Skills](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills) (March 2026).

## What it does

Guides the full skill authoring lifecycle:

1. **Capture intent** — interview the user to understand what the skill should do
2. **Write the SKILL.md** — draft the skill following best practices
3. **Create test cases** — generate realistic prompts that exercise the skill
4. **Run evaluations** — spawn subagents to test with-skill vs baseline
5. **Review results** — launch an interactive viewer for qualitative feedback
6. **Iterate** — improve the skill based on feedback, re-run, repeat
7. **Optimize triggering** — tune the description for reliable activation

## Key features

- **Eval framework** — write assertions, run benchmarks, track pass rates across iterations
- **Blind A/B comparison** — compare two skill versions without bias
- **Description optimizer** — automated loop to improve skill triggering accuracy
- **Multi-agent support** — parallel eval runs with independent contexts

## Usage

```
/skill-creator
```

Works in Claude Code, Claude.ai, and Cowork. Adapts behavior based on the environment (e.g., skips browser-based review in headless setups).

## Requirements

- Python 3.11+
- `claude` CLI (for description optimization)
- Subagent support recommended (for parallel evals)
