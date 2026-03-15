# Progress

## Commit ce23061 — Remove claude format from install scripts
- Removed `install_claude()` function and all claude references from 8 install.sh
- Changed default FORMAT from "all" to "agents"
- Updated tests to match

## Commit f8fb906 — Trim rules 81%, deduplicate install scripts
- 8 rule.md files: 483 -> 93 lines. Each is now a focused checklist.
- 8 copy-pasted install.sh replaced with shared scripts/install-rule.sh + 3-line wrappers
- Format files regenerated from trimmed rules

## Commit 73e4e31 — Remove stale CLAUDE.md references, sync global rules
- 8 rule READMEs: removed claude install examples/sections/table rows
- docs/RULE_FORMAT.md, AGENTS.md, CONTRIBUTING.md: removed CLAUDE.md references
- Global ~/.config/cognition/AGENTS.md: replaced with clean concat of marketplace rules

## What's done
- Zero claude references remain in the marketplace
- Global rules match marketplace rules exactly
- 46 tests pass
- Install scripts default to agents format (no duplication possible)

## What's next
- Update README.md install instructions if needed
- Check if any other stale content exists
- Clean up .tasks/ files
