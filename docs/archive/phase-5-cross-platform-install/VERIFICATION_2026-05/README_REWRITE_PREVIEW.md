# README Rewrite Preview (Phase 2 input)

**Status**: Draft for Phase 2 of [[../PLAN_CROSS_PLATFORM_INSTALL_FIX]]. Not yet applied to README.md.
**Date**: 2026-05-24
**Purpose**: Map every current install instruction in README.md to its verified-working replacement, sourced from [[empirical_act_verification]] log evidence. This becomes the spec for the Phase 2 README rewrite.

**Convention**: Each block shows what's in `README.md` **today** vs. what will replace it **post-Phase-1-merge**. Pre-merge install commands (those that need `--ref feat/claude-plugin-compliance` until PR #1 lands) are flagged explicitly.

---

## Section: Quick Start → Claude Code (lines 23-33)

### Today
```bash
/plugin marketplace add DgxSparkLabs/marketplace
/plugin install bundle-skill-all@dgxsparklabs-marketplace
/plugin install skill-telegram-notify@dgxsparklabs-marketplace
/plugin install bundle-quality-rules@dgxsparklabs-marketplace
```

### Verified post-Phase 1 (CL1/CL2/CL3 PASS)
Identical to today. Claude install chain works end-to-end per [[empirical_act_verification|CL1]] (`claude plugin marketplace add ./`), [[empirical_act_verification|CL2]] (`claude plugin install skill-example@dgxsparklabs-marketplace --scope project`), [[empirical_act_verification|CL3]] (`claude plugin list` shows it). No copy changes needed; can add an inline note that install + list both work end-to-end.

---

## Section: Quick Start → Codex (lines 35-42)

### Today
```bash
codex plugin marketplace add ./
# Codex registers it as dgxsparklabs-marketplace in ~/.codex/config.toml
# Individual plugin install follows the same pattern as Claude Code
```
**Problem**: Comment claims "individual plugin install follows the same pattern" — but C5 PROVED that `codex plugin add skill-example@dgxsparklabs-marketplace` fails today with `missing or invalid plugin.json`. Statement is false.

### Verified post-Phase 1 (assuming `.codex-plugin/plugin.json` emission lands, gated on supports)
```bash
# Register the marketplace (pre-PR-#1-merge: requires --ref pointing at the feature branch)
codex plugin marketplace add DgxSparkLabs/marketplace --ref feat/claude-plugin-compliance
# After PR #1 merges to main, --ref becomes optional:
#   codex plugin marketplace add DgxSparkLabs/marketplace

# Browse what's available
codex plugin list

# Install a specific plugin
codex plugin add skill-telegram-notify@dgxsparklabs-marketplace
```

Citations: [[empirical_act_verification|C3]] (PASS — `--ref` shortform), [[empirical_act_verification|C4]] (PASS — enumeration after implementer's Phase 1.5 generator addition keeps this working), [[empirical_act_verification|C5]] (currently FAIL; expected PASS post-implementation).

**Pre-merge footnote**: Add an explicit note in the README explaining that until PR #1 lands on main, Codex users must use `--ref feat/claude-plugin-compliance`. After merge, drop the note in a follow-up commit.

---

## Section: Quick Start → Gemini (lines 44-53)

### Today
```bash
echo "y" | gemini skills install ./_generated/skill-telegram-notify
gemini extensions validate ./.gemini/
echo "y" | gemini extensions install ./.gemini/ --consent
```
**Problem**: All three commands require a local clone first. User has no native GitHub-URL install path documented.

### Verified post-Phase 1 (assuming root-level `gemini-extension.json` emission lands)
```bash
# Install the whole marketplace as a Gemini extension directly from GitHub (no clone required)
gemini extensions install https://github.com/DgxSparkLabs/marketplace --ref feat/claude-plugin-compliance --consent
# Post-PR-#1-merge: --ref becomes optional.

# Verify the extension is registered (note: list output goes to stderr — pipe with 2>&1)
gemini extensions list 2>&1

# List discovered skills (project + user + built-in)
gemini skills list --all 2>&1

# Or, from a local clone (still works — same as today):
echo "y" | gemini extensions install ./.gemini/ --consent
```

Citations: [[empirical_act_verification|G1]] (PASS — local path baseline), [[empirical_act_verification|G2]] (currently FAIL; expected PASS post-implementation), [[empirical_act_verification|G3]] (currently FAIL with `--ref`; expected PASS post-implementation), [[empirical_act_verification|G5]] (PASS — extensions list grep), [[empirical_act_verification|G6]] (PASS — skills list grep).

**Gemini specifically gets the biggest improvement**: today's README forces a clone; post-fix, one-command install from GitHub works.

---

## Section: Quick Start → Cursor (lines 55-62)

### Today
```bash
git clone https://github.com/DgxSparkLabs/marketplace
# Open the cloned directory in Cursor IDE
```
**Problem**: Implies no CLI exists (FALSE — `agent` binary exists per [[cursor|CU1]]). Doesn't mention the plugin marketplace (cursor.com/marketplace launched Feb 2026). Doesn't mention team-marketplace import.

### Verified post-Phase 1
Two install paths now make sense to document:

```bash
# Path 1: Cursor team marketplace (Cursor 2.6+, admin Dashboard import)
#   Dashboard → Settings → Plugins → Import → paste GitHub repo URL → save
#   This requires .cursor-plugin/marketplace.json at repo root (emitted by Phase 1)
#   See: https://cursor.com/docs/plugins

# Path 2: Clone + open (works for all Cursor versions; IDE auto-loads .cursor/rules/ and reads .agents/skills/)
git clone https://github.com/DgxSparkLabs/marketplace
# Open the cloned directory in Cursor IDE

# Bonus: Cursor CLI ('agent' binary, separate install) exists for interactive sessions but has NO plugin install commands.
# Install (macOS/Linux/WSL): curl https://cursor.com/install -fsS | bash
# Install (Windows PowerShell): irm 'https://cursor.com/install?win32=true' | iex
```

Citations: [[cursor|CU1]] (PASS — `agent --version`), [[cursor|CU2]] (PASS — install path), [[cursor|CU3]] (PASS — full help; no plugin commands). Cursor docs source: `cursor.com/docs/plugins`, `cursor.com/docs/cli/installation` (fetched 2026-05-24).

---

## Section: Quick Start → Windsurf (lines 64-71)

### Today
```bash
git clone https://github.com/DgxSparkLabs/marketplace
# Open the cloned directory in Windsurf IDE
```
**Problem**: Only mentions rules; doesn't mention that Windsurf reads `.windsurf/skills/<name>/SKILL.md` AND `.agents/skills/` natively (per `docs.windsurf.com/windsurf/cascade/skills`). 26 skills are invisible today.

### Verified post-Phase 1 (assuming `AgentsPlatform` lands `.agents/skills/`)
```bash
# Clone and open in Windsurf IDE
git clone https://github.com/DgxSparkLabs/marketplace
# Rules auto-load from .windsurf/rules/
# Skills auto-load from .agents/skills/ (per Windsurf Cascade docs)
# Invoke any skill via @skill-name in Cascade chat
```

Citations: [[cursor#Section 3a Does Cursor read .agents/skills/<name>/SKILL.md natively?|Windsurf+Cursor share `.agents/skills/`]] (research agent's WebFetch on `docs.windsurf.com/windsurf/cascade/skills`, fetched 2026-05-24).

**No new CLI exists** for Windsurf (confirmed by [[../EMPIRICAL_CLI_FINDINGS/windsurf|May 22 empirical]] and unchanged in May 2026 docs). Clone-and-open remains the only install path; the upgrade is that skills now actually work.

---

## Section: Quick Start → Devin (lines 73-82)

### Today
```bash
git clone https://github.com/DgxSparkLabs/marketplace
devin skills list
devin rules list
```

### Verified post-Phase 1
Same commands work; can add a note that skills come from BOTH `.devin/skills/` and `.agents/skills/` per [[../EMPIRICAL_CLI_FINDINGS/devin|devin skills paths]] — useful if a future cleanup retires `.devin/skills/` in favor of `.agents/skills/` alone.

Optional addition: `npx skills add DgxSparkLabs/marketplace -a devin` as a no-clone alternative (per research agent's note; unverified live, would need another act run).

---

## Per-Platform Details section (lines 158-330)

The same rewrite pattern applies to the longer-form Per-Platform Details. Each platform's "Install + use" block needs the same updates as its Quick Start counterpart, plus deeper detail on:

- **Codex**: document the `.codex-plugin/plugin.json` per-plugin manifest that Phase 1 adds; explain that this is what makes `codex plugin add` work
- **Gemini**: explain both install paths (GitHub URL and local), note the stderr-goes-to-stdout quirk for `extensions list` / `mcp list`, note that the root-level `gemini-extension.json` is byte-identical to `.gemini/gemini-extension.json` and exists solely for GitHub-URL install
- **Cursor**: distinguish (a) IDE GUI plugin marketplace at `cursor.com/marketplace`, (b) team-marketplace GitHub import via Dashboard, (c) `agent` CLI (no plugin install), (d) classic `.cursor/rules/` auto-load
- **Windsurf**: explain that `.windsurf/skills/` AND `.agents/skills/` both auto-discover; we emit `.agents/skills/` and skills work in Cascade via `@skill-name`
- **Devin**: explain that Devin reads `.devin/skills/` + `.agents/skills/` + `.cursor/rules/` + `.windsurf/rules/` — the broadest cross-platform coverage of any platform

---

## What this preview does NOT change

- The "Construct Types Available" table (lines 86-101) — unchanged; we updated the type-column links in a separate edit earlier today
- "Installation Patterns" section (lines 105-152) — bundle/catch-all install patterns are Claude-specific; they remain Claude-format
- "Repository Structure" (lines 334-368) — needs minor additions for `.agents/` and the root-level `gemini-extension.json` + `.cursor-plugin/marketplace.json` files Phase 1 adds
- "Contributing", "Deep Dives", "License" — unchanged

---

## Phase 2 execution checklist (for whoever does the README rewrite)

1. Confirm Phase 1 is merged on `feat/claude-plugin-compliance` (commits land; `.codex-plugin/plugin.json` files exist in `_generated/`; root-level `gemini-extension.json` exists; `.agents/skills/` populated)
2. Open `README.md`; for each section block above, replace the "Today" copy with the "Verified post-Phase 1" copy
3. Add the pre-merge footnotes for Codex `--ref` and Gemini `--ref` (drop both in a separate commit after PR #1 lands on main and the no-ref forms start working)
4. Update the Repository Structure tree to mention `.agents/`, root-level `gemini-extension.json`, root-level `.cursor-plugin/marketplace.json`
5. Update the Table of Contents anchors if any section headings changed
6. Run a final sanity check: every command in the README should appear in `empirical_act_verification.md` as VERIFIED-PASS OR be flagged as "in-IDE action sequence" (Cursor team marketplace, `/add-plugin`, etc.) where act-style verification doesn't apply

## Cross-references

- [[../PLAN_CROSS_PLATFORM_INSTALL_FIX]] — Phase 2 of which this is the input
- [[SUMMARY]] — ground truth verification synthesis
- [[empirical_act_verification]] — per-claim evidence
- [[cursor]] — Cursor IDE + CLI WebFetch research
