# Claude Code Skill Marketplace — fork-ready template

A **template marketplace for Claude Code skills**. Fork it, drop skill folders into `src/skills/`, push — CI packages and publishes them, and anyone can install your skills with two `claude` commands. You never run the generator; the only thing you touch is `src/skills/`.

```
you fork this repo
 └▶ drop a folder into src/skills/<your-skill>/      ← the ONLY thing you touch
     └▶ git commit + push to your fork's main
         └▶ GitHub Actions (in your fork) validates → regenerates → commits
             └▶ users: claude plugin marketplace add <you>/<your-repo>
                 └▶ /plugin install <your-skill>
```

Governance and history: umbrella issue [#18](https://github.com/DgxSparkLabs/marketplace/issues/18) (the skills-only, Claude-only scope-down) and [#19](https://github.com/DgxSparkLabs/marketplace/issues/19) (the naming standard CI enforces). Other construct types and other agent platforms are deliberately deferred with tracked re-expansion issues — see #18's index.

## Install skills from this marketplace

```bash
claude plugin marketplace add DgxSparkLabs/marketplace
claude plugin install skill-example-multi@dgxsparklabs-marketplace --scope project
claude plugin enable  skill-example-multi@dgxsparklabs-marketplace
```

Install and enable are separate steps — skipping enable yields `Plugin not found in any editable settings scope.` Browse what's installable with `claude plugin list --available | grep dgxsparklabs`. The authoritative plugin list is generated at [`docs/INVENTORY.md`](docs/INVENTORY.md).

Skills invoke as `/<brand>-skill-<plugin>:<component>` (e.g. `/dgxsparklabs-skill-example-multi:notebook`) or via the flat shortcut (`/notebook`) when unambiguous.

## Make it yours (forking checklist, ~5 minutes)

1. **Fork** this repo on GitHub.
2. **Enable Actions** in your fork (Actions tab → enable — one click; forks start with workflows off).
3. **Edit `src/MARKETPLACE.toml`**: set `name` (must be kebab-case and end in `-marketplace` — e.g. `acme-marketplace`; CI enforces this, and the part before `-marketplace` becomes the brand prefix on every skill), plus `owner` and the repo URL.
4. **Push to main.** CI regenerates every manifest with your identity — nothing else needs renaming; install commands, plugin names, and slash namespaces all derive from that one file plus your repo slug.
5. Tell users: `claude plugin marketplace add <you>/<your-fork>`.

What you may NOT hand-edit: `_generated/`, `.claude-plugin/`, `docs/INVENTORY.md` — CI owns them and will overwrite (drift is also a CI failure on PRs).

## Add a skill

```bash
uv run scripts/new_construct.py skill my-skill     # scaffold from the example (optional)
# — or just create src/skills/my-skill/SKILL.md by hand —
git add src/skills/my-skill && git commit && git push
```

A skill folder is either **solo** (`src/skills/<plugin>/SKILL.md`) or **multi** (`src/skills/<plugin>/skills/<a>/SKILL.md`, one subfolder per skill — folder name must equal the SKILL.md frontmatter `name:`). Format details: [`docs/SKILL_FORMAT.md`](docs/SKILL_FORMAT.md); the full naming rules CI enforces: issue #19 and `scripts/validate_source.py`.

Working locally and want the full gate before pushing? `uv run scripts/tasks.py verify` runs source validation → drift check → test suites → `claude plugin validate`.

## Repo map

- `src/MARKETPLACE.toml` — your marketplace identity (the one file a forker edits)
- `src/skills/<plugin>/` — skill sources (the only contributor surface)
- `_generated/`, `.claude-plugin/` — CI-generated install artifacts; never hand-edit
- `scripts/` — generator + validators + task runner; `tests/` — the suites
- `docs/` — [`RESUME_HERE.md`](docs/RESUME_HERE.md) (orientation) · [`ARCHITECTURE.md`](docs/ARCHITECTURE.md) (how generation works) · [`CONTRIBUTING.md`](docs/CONTRIBUTING.md)
