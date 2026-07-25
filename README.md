# DgxSparkLabs Marketplace

A Claude Code plugin marketplace. Operator-authored source content lives under `src/`; the generator (`scripts/`) emits the Claude-native manifests (`.claude-plugin/marketplace.json` + per-plugin `plugin.json`) and the generated plugin wrappers under `_generated/`.

> **Scope-down in progress ([#18](https://github.com/DgxSparkLabs/marketplace/issues/18)).** This repo is being reduced to a **skills-only, Claude-Code-only template marketplace** that you can fork to host your own skills: contributors drop a folder into `src/skills/`, CI handles packaging and publishing, users install with `claude plugin` commands. Support for other platforms (Codex, Gemini, Cursor, Windsurf, Devin — formerly shipped here) and other construct types was deliberately deferred, not abandoned — each has a tracked re-expansion issue (see [#18](https://github.com/DgxSparkLabs/marketplace/issues/18) for the full index). This README is interim; the full fork-and-use guide lands with the template polish PR.

## Install (Claude Code)

Register the marketplace and install. The `bundle-examples` plugin auto-installs every reference example:

```bash
claude plugin marketplace add DgxSparkLabs/marketplace
claude plugin install bundle-examples@dgxsparklabs-marketplace --scope project
```

Or install one at a time. Install + enable are SEPARATE steps:

```bash
claude plugin install skill-example-multi@dgxsparklabs-marketplace --scope project
claude plugin enable  skill-example-multi@dgxsparklabs-marketplace
```

If you skip enable, Claude says `Plugin not found in any editable settings scope.`

Browse what's installable:

```bash
claude plugin list --available | grep dgxsparklabs
```

Invoke: every plugin's slash form follows `/dgxsparklabs-<construct>-<plugin>:<component>` (skills also resolve via the flat shortcut, e.g. `/notebook`). For the authoritative, generated plugin inventory see [`docs/INVENTORY.md`](docs/INVENTORY.md).

## Contributing

```bash
uv run scripts/new_construct.py skill <name>   # scaffold from the example
# edit the copied files
uv run scripts/tasks.py verify                 # drift check + test suites + claude plugin validate
git add . && git commit                        # open a PR
```

See [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) and [`docs/ADDING_A_CONSTRUCT.md`](docs/ADDING_A_CONSTRUCT.md).

## Repo map

- `src/` — operator-authored sources (the only thing contributors touch)
- `_generated/`, `.claude-plugin/`, `docs/INVENTORY.md` — generated; never hand-edit
- `scripts/` — generator + task runner (`uv run scripts/tasks.py verify`)
- `docs/` — [`RESUME_HERE.md`](docs/RESUME_HERE.md) (orientation), [`ARCHITECTURE.md`](docs/ARCHITECTURE.md), [`USER_GUIDE.md`](docs/USER_GUIDE.md)
