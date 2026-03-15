# Skills Marketplace

A curated collection of reusable agent skills and rules. Each item is a self-contained directory that can be installed into any compatible AI agent tool.

**Skills** are invoked on demand (`/skill-name`). **Rules** are always-on and activate automatically every session.

## Catalog

### Rules

| Rule | Description |
|------|-------------|
| [continuous-improvement](./continuous-improvement/) | Structured seven-phase workflow for finding, planning, and implementing codebase improvements |
| [no-ai-credit](./no-ai-credit/) | Prevent AI agents from adding self-attribution to any output |
| [prior-art](./prior-art/) | Search for existing solutions before building custom code |
| [telegram-on-complete](./telegram-on-complete/) | Send a Telegram notification after completing any task |
| [verify-your-work](./verify-your-work/) | Require agents to test and verify their work before declaring tasks complete |

### Skills

| Skill | Description |
|-------|-------------|
| [duckduckgo-search](./duckduckgo-search/) | Search DuckDuckGo and return results as structured text |
| [expose-port](./expose-port/) | Expose a local port via HTTPS (localhost.run) or TCP (bore) |
| [github-search](./github-search/) | Search GitHub for repositories, prior art, and implementation inspiration |
| [google-drive-reader](./google-drive-reader/) | Read Google Docs from personal Drive, extract URLs and conclusions |
| [send-email](./send-email/) | Send an email to someone using the Resend API |
| [ssh-tunnel](./ssh-tunnel/) | Set up SSH port forwarding tunnels (local, remote, SOCKS proxy) |
| [telegram-notify](./telegram-notify/) | Send a Telegram notification with a task summary |
| [web-scraper](./web-scraper/) | Fetch a web page and extract its main content as clean readable text |
| [youtube-search](./youtube-search/) | Search YouTube for technical videos, tutorials, and talks on a topic |
| [youtube-wisdom](./youtube-wisdom/) | Extract key knowledge from a YouTube video transcript |

## Installing Rules

Rules activate automatically — no invocation needed. Each rule includes an install script and format-specific files for multiple agent tools.

```bash
git clone https://github.com/ForkYoraiLevi/marketplace.git /tmp/marketplace

# Install a rule into the current project (all agent formats)
/tmp/marketplace/<rule-name>/install.sh

# Install globally (all projects)
/tmp/marketplace/<rule-name>/install.sh --global

# Install for a specific tool only
/tmp/marketplace/<rule-name>/install.sh --format windsurf
```

Supported formats: `agents` (AGENTS.md), `windsurf`, `cursor`, `claude`, `all` (default).

## Installing Skills

Skills are invoked with `/<skill-name>` in an agent session. Copy the skill directory into your agent's skills directory:

```bash
git clone https://github.com/ForkYoraiLevi/marketplace.git /tmp/marketplace
cp -r /tmp/marketplace/<skill-name> ~/.<agent>/skills/<skill-name>
# e.g. ~/.config/cognition/skills/, ~/.windsurf/skills/, etc.
```

Or into a project:

```bash
mkdir -p <project>/.windsurf/skills   # or .cognition/skills
cp -r /tmp/marketplace/<skill-name> <project>/.windsurf/skills/<skill-name>
```

## Repository Structure

```
marketplace/
├── AGENTS.md               # Agent-facing instructions for contributing
├── README.md               # This file — catalog
├── CONTRIBUTING.md          # Contribution guide
├── docs/
│   ├── SKILL_FORMAT.md     # SKILL.md format reference
│   └── RULE_FORMAT.md      # Rule format reference
├── _template/              # Starter template for new skills
│   ├── SKILL.md
│   ├── README.md
│   └── scripts/
├── <rule-name>/            # Rule directories
│   ├── rule.md             # Rule content (AGENTS.md format)
│   ├── README.md           # Documentation
│   ├── install.sh          # Install script
│   └── formats/            # Tool-specific rule files
│       ├── windsurf.md
│       └── cursor.md
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
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Humans | Contribution guide with quality checklist |
| [docs/SKILL_FORMAT.md](./docs/SKILL_FORMAT.md) | Both | Complete SKILL.md format specification |
| [docs/RULE_FORMAT.md](./docs/RULE_FORMAT.md) | Both | Rule format specification for all supported tools |
| [_template/](./_template/) | Both | Copy-and-modify starter for new skills |

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on adding new skills and rules.

## License

MIT
