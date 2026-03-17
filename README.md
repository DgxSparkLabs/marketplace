# Skills Marketplace

A curated collection of reusable agent skills and rules. Each item is a self-contained directory that can be installed into any compatible AI agent tool.

**Skills** are invoked on demand (`/skill-name`). **Rules** are always-on and activate automatically every session.

## Catalog

### Rules

| Rule | Description |
|------|-------------|
| [blast-radius](./blast-radius/) | Scope changes by blast radius — prefer small atomic edits over large risky rewrites |
| [continuous-improvement](./continuous-improvement/) | Structured seven-phase workflow for finding, planning, and implementing codebase improvements |
| [document-lifecycle](./document-lifecycle/) | Three-tier documentation: rules, reference, history — no sprawl |
| [document-progress](./document-progress/) | Write progress to disk using todo lists and HANDOFF.md so nothing is lost between sessions |
| [no-ai-credit](./no-ai-credit/) | Prevent AI agents from adding self-attribution to any output |
| [prior-art](./prior-art/) | Search for existing solutions before building custom code |
| [python-uv](./python-uv/) | Use uv for all Python operations — never pip, venv, conda, or poetry |
| [stay-motivated](./stay-motivated/) | Prevent the agent from stopping prematurely — keep working until truly done |
| [task-formation](./task-formation/) | Concrete pass conditions, code references by name, session-sized tasks |
| [telegram-on-complete](./telegram-on-complete/) | Send a Telegram notification after completing any task |
| [verification-ladder](./verification-ladder/) | Five-layer automated testing: compile, unit, integration, perf, e2e |
| [verify-your-work](./verify-your-work/) | Require agents to test and verify their work before declaring tasks complete |

### Skills

| Skill | Description |
|-------|-------------|
| [act-runner](./act-runner/) | Run GitHub Actions workflows locally with act and podman |
| [duckduckgo-search](./duckduckgo-search/) | Search DuckDuckGo and return results as structured text |
| [expose-port](./expose-port/) | Expose a local port via HTTPS (localhost.run) or TCP (bore) |
| [gemini-chat](./gemini-chat/) | Interactive multi-turn chat with Google Gemini |
| [github-search](./github-search/) | Search GitHub for repositories, prior art, and implementation inspiration |
| [google-drive-reader](./google-drive-reader/) | Read Google Docs from personal Drive, extract URLs and conclusions |
| [motivation](./motivation/) | Encourage the agent to keep working instead of stopping prematurely |
| [send-email](./send-email/) | Send an email to someone using the Resend API |
| [session-history](./session-history/) | Query past Devin CLI conversations from the local session database |
| [ssh-tunnel](./ssh-tunnel/) | Set up SSH port forwarding tunnels (local, remote, SOCKS proxy) |
| [structured-handoff](./structured-handoff/) | Generate structured task files for autonomous agent sessions |
| [telegram-notify](./telegram-notify/) | Send a Telegram notification with a task summary |
| [web-scraper](./web-scraper/) | Fetch a web page and extract its main content as clean readable text |
| [youtube-search](./youtube-search/) | Search YouTube for technical videos, tutorials, and talks on a topic |
| [youtube-wisdom](./youtube-wisdom/) | Extract key knowledge from a YouTube video transcript |

## Interactive Installer

<p align="center">
  <img src="docs/installer-screenshot.svg" alt="Marketplace Installer TUI" width="700">
</p>

### One-liner install

```bash
curl -fsSL https://raw.githubusercontent.com/ForkYoraiLevi/marketplace/main/scripts/install.sh | bash
```

Installs `uv` if needed, clones the repo, and launches the interactive TUI. Pass arguments through:

```bash
curl -fsSL ... | bash -s -- --uninstall    # uninstall mode
curl -fsSL ... | bash -s -- --project      # project-level install
```

### From a local clone

The easiest way to install everything. Detects your agent platforms, shows checkboxes, installs your selections:

```bash
uv run install.py
```

Supports install and uninstall with a full TUI:

```bash
uv run install.py              # interactive install (global scope)
uv run install.py --uninstall  # interactive uninstall
uv run install.py --project    # install to project-level config
```

The installer handles MCP servers, rules, and skills across all detected platforms (Devin, Claude Code, Cursor, Windsurf). It shows what's already installed, skips duplicates, and uses the correct format for each platform.

## Manual Installation

### Rules

Rules activate automatically — no invocation needed. Each rule includes an install script and format-specific files for multiple agent tools.

```bash
# Install a rule into the current project (AGENTS.md only, the default)
<rule-name>/install.sh

# Install globally (all projects)
<rule-name>/install.sh --global

# Install for all tools at once (agents + windsurf + cursor)
<rule-name>/install.sh --format all
```

Supported formats: `agents` (AGENTS.md, default), `windsurf`, `cursor`, `all`.

### Skills

Skills are invoked with `/<skill-name>` in an agent session. Copy the skill directory into your agent's skills directory:

```bash
cp -r <skill-name> ~/.<agent>/skills/<skill-name>
# e.g. ~/.config/cognition/skills/, ~/.windsurf/skills/, etc.
```

## Repository Structure

```
marketplace/
├── AGENTS.md               # Agent-facing instructions for contributing
├── README.md               # This file — catalog
├── CONTRIBUTING.md          # Contribution guide
├── install.py              # Interactive TUI installer (uv run install.py)
├── docs/
│   ├── ONBOARDING.md       # Quick-start for new agents
│   ├── SKILL_FORMAT.md     # SKILL.md format reference
│   └── RULE_FORMAT.md      # Rule format reference
├── research/               # 200+ sources of market intelligence
│   ├── README.md           # Navigation index and reading order
│   ├── KNOWLEDGE_BASE.md   # Distilled insights by topic
│   ├── ANTI_PATTERNS.md    # Noise catalog and dead ends
│   └── METHODOLOGY.md      # How research was done
├── tests/                  # 104 automated tests
├── scripts/                # Repo-level install scripts
├── _template/              # Starter template for new skills
├── <rule-name>/            # Rule directories
│   ├── rule.md             # Rule content (AGENTS.md format)
│   ├── README.md           # Documentation
│   ├── install.sh          # Install script
│   └── formats/            # Tool-specific rule files
└── <skill-name>/           # Skill directories
    ├── SKILL.md
    ├── README.md
    ├── scripts/
    └── setup.sh            # Optional — prerequisite installer
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
