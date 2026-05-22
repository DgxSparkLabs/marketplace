# Windsurf CLI — Empirical Findings

**CI Run ID**: 26260259166 (run 1)  
**Date Verified**: 2026-05-22  
**Result**: NO CLI EXISTS for headless/terminal use

## Summary

Windsurf has no standalone CLI binary. It is a GUI IDE (VS Code fork). No headless agent or terminal CLI is available via any package manager, download, or install script.

## Evidence from CI

| Check | Result |
|-------|--------|
| `npm show windsurf` | Found — but it's an unrelated package (`windsurf@0.0.1`) by `colinedge`, NOT Codeium |
| `npm show @windsurf/cli` | 404 Not Found |
| `npm show @codeium/windsurf` | 404 Not Found |
| `npm show windsurf-cli` | 404 Not Found |
| `npm show @codeium/cli` | 404 Not Found |
| `pip show windsurf` | WARNING: Package(s) not found |
| `pip index versions windsurf` | `windsurf (0.0.1)` — same unrelated PyPI stub |
| GitHub API: `codeium-ai/windsurf/releases` | 404 Not Found |
| `windsurf --version` | Exit 127 (command not found) |
| `windsurf --help` | Exit 127 (command not found) |
| `codeium --version` | Exit 127 (command not found) |
| `snap info windsurf` | `error: no snap found for "windsurf"` |
| `apt-cache show windsurf` | `E: No packages found` |

## The misleading npm package

`windsurf@0.0.1` on npm is maintained by `colinedge/colinmcd94` and has nothing to do with Codeium/Windsurf IDE. It's a terminal cursor-hiding utility. Published "over a year ago."

## What IS available for Windsurf (config, not CLI)

Windsurf's agent behavior is configured via **editor rules files** read by the Windsurf IDE:
- `.windsurf/rules/*.md` — project-level always-on rules
- (Confirmed by `devin rules paths` which shows Windsurf reads these paths)

There is NO programmatic CLI to verify, list, or inspect these files from outside the IDE.

## Conclusion for marketplace validation

Windsurf cannot be validated via CLI. The only validation possible is **file existence checks**:
- Check `.windsurf/rules/<name>.md` exists
- Validate YAML frontmatter and content structure manually

No auth-free CLI commands exist because no CLI exists.
