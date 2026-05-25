# example-rule

A working reference plugin demonstrating the **rule** construct type. Copy this directory and modify to scaffold your own rule plugin.

## What it does

Ships an always-on behavioral rule. The rule gets emitted to per-platform mirrors that Cursor / Codex / Gemini / Windsurf consume directly. For Claude Code, the rule is installed into the memory subsystem at `.claude/rules/` (rules are not a Claude plugin component as of 2026-05-26).

## Install

### Claude Code (filesystem only — not a plugin)

Per `code.claude.com/docs/en/plugins-reference#plugin-components-reference` (fetched 2026-05-26), rules are not a Claude plugin component. Install into Claude's memory subsystem at `.claude/rules/` directly:

```bash
# Project scope (live updates if symlinked)
mkdir -p .claude/rules
ln -s "$(pwd)/rules/example/rule.md" .claude/rules/example.md

# Or copy for portability:
cp rules/example/rule.md .claude/rules/example.md

# User scope (every project on this machine)
mkdir -p ~/.claude/rules
cp rules/example/rule.md ~/.claude/rules/example.md
```

See `docs/USER_GUIDE.md` Claude section for the full operator workflow and the rationale.

### Cursor / Codex / Gemini / Windsurf (still a plugin)

For these platforms `rule-example` IS a plugin — install via the platform's native marketplace surface (`codex plugin add rule-example@dgxsparklabs-marketplace`, Cursor `/add-plugin rule-example@<url>`, etc.). See `docs/USER_GUIDE.md` per-platform sections.

After install, Cursor reads `.cursor/rules/example.md`, Windsurf reads `.windsurf/rules/example.md`, and Codex/Gemini read the file through their per-plugin manifest pointers.

## File-by-file walkthrough

```
example/
├── rule.md           ← the actual rule body (single source of truth)
├── formats/          ← per-platform format variants (if any) — auto-generated where missing
└── README.md         ← human-facing tutorial (you are here)
```

The generator emits `_generated/rule-example/rules/example.md` (for Cursor/Codex/Gemini per-plugin manifests) and mirrors the rule into `.cursor/rules/example.md`, `.windsurf/rules/example.md`, and `.agents/rules/example.md` (forward-looking convergence) on every `uv run scripts/generate_manifest.py` run.

## To make your own rule from this template

1. Copy this directory: `cp -r rules/example rules/my-rule`
2. Rename `my-rule` to whatever you want (kebab-case).
3. Edit `rule.md` with your behavioral guideline. Keep it short, imperative, focused on one behavior.
4. Edit `README.md` to describe your rule (used as the per-plugin description in Cursor/Codex manifests).
5. Add your rule name to a domain in `catalog.toml` if you want a domain bundle to include it.
6. Run `uv run scripts/generate_manifest.py` to refresh manifests.
7. Run `uv run tests/test_marketplace.py` and `uv run tests/test_schema_fitness.py`.
8. Commit.

## Related

- Full rule format reference: `docs/RULE_FORMAT.md`
- User-facing install workflow: `docs/USER_GUIDE.md`
- Per-platform technical reference: `docs/PLATFORMS.md` (Claude rule discovery section)
- Other example plugins: `<construct>/example/`
- Real rules shipped by this marketplace: `rules/`
