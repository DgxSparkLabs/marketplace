# Skills Marketplace

A curated collection of reusable agent skills and rules. Each item is a self-contained directory that can be installed into any compatible AI agent tool.

**Skills** are invoked on demand (`/skill-name`). **Rules** are always-on and activate automatically every session.

## Catalog

### Rules

| Rule | Description |
|------|-------------|
| [autonomous-persistence](./rules/autonomous-persistence/) | Never ask permission to continue -- keep working autonomously until done or explicitly stopped |
| [blast-radius](./rules/blast-radius/) | Scope changes by blast radius — prefer small atomic edits over large risky rewrites |
| [code-hygiene](./rules/code-hygiene/) | Enforce DRY, single-responsibility, centralized definitions, and human-readable naming |
| [continuous-improvement](./rules/continuous-improvement/) | Structured seven-phase workflow for finding, planning, and implementing codebase improvements |
| [document-lifecycle](./rules/document-lifecycle/) | Three-tier documentation: rules, reference, history — no sprawl |
| [document-progress](./rules/document-progress/) | Write progress to disk using todo lists and HANDOFF.md so nothing is lost between sessions |
| [improve-the-process](./rules/improve-the-process/) | Fix friction structurally — every session should improve the workflow |
| [no-ai-credit](./rules/no-ai-credit/) | Prevent AI agents from adding self-attribution to any output |
| [output-discipline](./rules/output-discipline/) | Redirect verbose output to files and extract only what you need -- never flood context |
| [pitfalls-discipline](./rules/pitfalls-discipline/) | Read PITFALLS.md before complex work, write to it after fixing bugs |
| [prior-art](./rules/prior-art/) | Search for existing solutions before building custom code |
| [python-uv](./rules/python-uv/) | Use uv for all Python operations — never pip, venv, conda, or poetry |
| [readable-docs](./rules/readable-docs/) | Write documentation for humans — TL;DR readme, hand-holding guides, consistent terminology |
| [revert-on-failure](./rules/revert-on-failure/) | Commit before experimenting, measure after, keep improvements, revert failures |
| [session-resilience](./rules/session-resilience/) | Write state to disk continuously — you don't have memory, these files do |
| [simplicity-bar](./rules/simplicity-bar/) | Weigh complexity cost against improvement magnitude -- simpler is better, deletion is a win |
| [stay-motivated](./rules/stay-motivated/) | Completeness checklist — verify done conditions before stopping |
| [task-formation](./rules/task-formation/) | Decompose requests into goals with intent, then into actionable session-sized tasks |
| [telegram-on-complete](./rules/telegram-on-complete/) | Send a Telegram notification after completing any task |
| [verification-ladder](./rules/verification-ladder/) | Five-layer automated testing: compile, unit, integration, perf, e2e |
| [verify-your-work](./rules/verify-your-work/) | Require agents to test and verify their work before declaring tasks complete |

### Skills

| Skill | Description |
|-------|-------------|
| [act-runner](./skills/act-runner/) | Run GitHub Actions workflows locally with act and podman |
| [check](./skills/check/) | Mid-session course correction — stop, review rules, and realign |
| [code-health-audit](./skills/code-health-audit/) | Audit codebase for DRY violations, oversized files, and scattered definitions |
| [duckduckgo-search](./skills/duckduckgo-search/) | Search DuckDuckGo and return results as structured text |
| [expose-port](./skills/expose-port/) | Expose a local port via HTTPS (localhost.run) or TCP (bore) |
| [gemini-chat](./skills/gemini-chat/) | Interactive multi-turn chat with Google Gemini |
| [github-repo-setup](./skills/github-repo-setup/) | Create a GitHub repo with CI, branch protection, and naming rules |
| [github-search](./skills/github-search/) | Search GitHub for repositories, prior art, and implementation inspiration |
| [google-drive-reader](./skills/google-drive-reader/) | Read Google Docs from personal Drive, extract URLs and conclusions |
| [motivation](./skills/motivation/) | Completeness checker — report what's actually unfinished before stopping |
| [pitfall-check](./skills/pitfall-check/) | Search PITFALLS.md and git log for known issues before starting work |
| [project-bootstrap](./skills/project-bootstrap/) | Initialize project docs — AGENTS.md, HANDOFF.md, CHANGELOG.md, PITFALLS.md |
| [recall-rules](./skills/recall-rules/) | Re-read global rules and thinking framework to realign mid-session |
| [send-email](./skills/send-email/) | Send an email to someone using the Resend API |
| [session-history](./skills/session-history/) | Query past Devin CLI conversations from the local session database |
| [session-wrapup](./skills/session-wrapup/) | End-of-session audit — check docs, commits, and readiness for the next agent |
| [skill-analytics](./skills/skill-analytics/) | Analyze skill usage patterns and generate an interactive HTML dashboard |
| [skill-creator](./skills/skill-creator/) | Create, test, and iteratively improve agent skills with evals |
| [ssh-tunnel](./skills/ssh-tunnel/) | Set up SSH port forwarding tunnels (local, remote, SOCKS proxy) |
| [structured-handoff](./skills/structured-handoff/) | Generate structured task files for autonomous agent sessions |
| [sync-rules](./skills/sync-rules/) | Sync rules from global AI agent configs into the workspace |
| [telegram-notify](./skills/telegram-notify/) | Send a Telegram notification with a task summary |
| [textual-tui-guide](./skills/textual-tui-guide/) | Build rich terminal UIs with Python Textual — layouts, widgets, modals, styling |
| [web-scraper](./skills/web-scraper/) | Fetch a web page and extract its main content as clean readable text |
| [youtube-search](./skills/youtube-search/) | Search YouTube for technical videos, tutorials, and talks on a topic |
| [youtube-wisdom](./skills/youtube-wisdom/) | Extract key knowledge from a YouTube video transcript |

## Install

```bash
# In a Claude Code session:
/plugin marketplace add DgxSparkLabs/marketplace

# Install an individual skill:
/plugin install skill-telegram-notify@marketplace

# Install a domain bundle (auto-installs all member skills):
/plugin install skills-communication@marketplace

# Install an individual rule (then activate to symlink into .claude/rules/):
/plugin install rule-blast-radius@marketplace
bash ~/.claude/plugins/cache/DgxSparkLabs/marketplace/rule-blast-radius/activate.sh

# Install a rule bundle (auto-installs all rules in the bundle):
/plugin install rules-quality@marketplace
# Then activate each rule's symlink, or use the repo-root helper:
bash <(curl -fsSL https://raw.githubusercontent.com/DgxSparkLabs/marketplace/main/activate-installed-rules.sh)
```

For users on **Devin, Cursor, Windsurf, Codex CLI, or Gemini CLI** — clone the repo and point your tool at the appropriate auto-generated mirror directory:

```
.devin/skills/      .devin/rules/
.cursor/rules/      .windsurf/rules/
.codex/skills/      .gemini/skills/
```

The mirrors are regenerated by `uv run scripts/generate_manifest.py` whenever the source skills/rules change.

## Repository Structure

```
marketplace/
├── MARKETPLACE.toml        # Single source for repo identity (owner, version, license)
├── catalog.toml            # Construct types + skill/rule domain tagging
├── .claude-plugin/
│   └── marketplace.json    # Generated root manifest (71 plugin entries)
├── skills/                 # Source skill content (one directory per skill)
├── rules/                  # Source rule content (one directory per rule)
├── examples/               # 10 example-* reference plugins (one per construct type)
├── _generated/             # Generated plugin wrappers + bundles (run scripts/generate_manifest.py)
├── .codex/ .gemini/ .cursor/ .windsurf/ .devin/   # Cross-platform mirrors
├── scripts/
│   └── generate_manifest.py
├── docs/
│   ├── ONBOARDING.md
│   ├── SKILL_FORMAT.md
│   ├── RULE_FORMAT.md
│   ├── GOAL_PLUGIN_COMPLIANCE.md
│   ├── PLAN_PLUGIN_COMPLIANCE.md
│   ├── INVESTIGATION_PLUGIN_DEPENDENCIES.md
│   └── IMPLEMENTING_AGENT_PROMPT.md
├── tests/                  # Automated tests
└── activate-installed-rules.sh  # One-shot helper for symlinking installed rule plugins
```

## Documentation

| Document | Audience | Purpose |
|----------|----------|---------|
| [AGENTS.md](./AGENTS.md) | AI agents | Instructions for creating skills and rules autonomously |
| [docs/ONBOARDING.md](./docs/ONBOARDING.md) | AI agents | Quick-start orientation for new agents (3-minute read) |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Humans | Contribution guide with quality checklist |
| [docs/SKILL_FORMAT.md](./docs/SKILL_FORMAT.md) | Both | Complete SKILL.md format specification |
| [docs/RULE_FORMAT.md](./docs/RULE_FORMAT.md) | Both | Rule format specification for all supported tools |
| [_template/](./_template/) | Both | Copy-and-modify starter for new skills |
| [research/](./research/) | Both | Market intelligence: 200+ sources, knowledge base, methodology |

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on adding new skills and rules.

## License

MIT
