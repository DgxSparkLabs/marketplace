# Investigation — Plugin Dependency Auto-Install

**Status:** ✅ RESOLVED — verified empirically on 2026-05-22. See **Result** section at the bottom.

**Outcome (TL;DR):** Plugin dependencies **DO auto-install**. The planned dependency-only domain bundle architecture works. No fallback needed for tasks #3-#5. The Option 2 fallback design remains documented below as reference material for future readers.

**Owner:** Whoever picks up task #13.

**Blocks:** All domain-bundle work (tasks #3, #4, #5). The chosen architecture below depends on the answer.

---

## The Question

When a user runs `/plugin install skills-communication@dgxsparklabs-marketplace`, and the `skills-communication` plugin declares `"dependencies": ["skill-send-email", "skill-telegram-notify"]` in its `plugin.json`, **does Claude Code automatically install those dependency plugins?**

Sources we already have:

- The official plugins-reference docs list `dependencies` as a valid field with the form `["helper-plugin", { "name": "vault", "version": "~2.1.0" }]`, described as "Other plugins this plugin requires."
- The docs do **not** explicitly say "will be auto-installed."
- The SchemaStore manifest confirms the field exists but does not describe install-time behavior.
- Our prior research did not find a concrete example of an auto-installed dependency in any real plugin marketplace.

The unknown: whether Claude Code resolves and installs declared dependencies, or simply warns when they are missing.

---

## Why It Matters

The marketplace ships **domain bundle plugins** (`skills-communication`, `rules-quality`, etc.) whose entire purpose is to install a curated set of individual plugins in one command. Two architectures are possible:

| Architecture | Bundle contains | Works if deps DON'T auto-install? |
|--------------|----------------|----------------------------------|
| Dependency-only (preferred) | Just `plugin.json` with a `dependencies` array | No — user sees "missing deps" with no clear next step |
| Inlined content | Physical copies of all member content | Yes — but duplicates content and breaks the "one source of truth" goal |
| Shell-script-shipped | `plugin.json` + `install-deps.sh` that calls `claude plugin install <each>` | Yes — but adds a manual second step like rules-activate.sh |

The dependency-only architecture is the cleanest by a wide margin. We commit to it only if Claude Code resolves deps.

---

## Verification Plan

A 30-minute experiment, no real marketplace touched.

### Step 1: Build two minimal test plugins in a scratch directory

```
test-plugin-A/
├── .claude-plugin/plugin.json
└── SKILL.md

test-plugin-B/
├── .claude-plugin/plugin.json
└── (no other content — bundle plugin)
```

**`test-plugin-A/.claude-plugin/plugin.json`:**
```json
{
  "name": "test-plugin-A",
  "version": "0.0.1",
  "description": "Test individual plugin"
}
```

**`test-plugin-A/SKILL.md`** — minimal SKILL with frontmatter and one line of body, just to confirm install worked.

**`test-plugin-B/.claude-plugin/plugin.json`:**
```json
{
  "name": "test-plugin-B",
  "version": "0.0.1",
  "description": "Test bundle plugin",
  "dependencies": ["test-plugin-A"]
}
```

### Step 2: Wrap them in a test marketplace

Create a throwaway repo `dep-test-marketplace` with `.claude-plugin/marketplace.json` listing both plugins. Push to GitHub.

### Step 3: Run the install and observe

In a fresh Claude Code project:

```bash
/plugin marketplace add <your-github>/dep-test-marketplace
/plugin install test-plugin-B@dep-test-marketplace
```

Then check:

```bash
# Does test-plugin-A also exist in the cache?
ls ~/.claude/plugins/cache/<your-github>/dep-test-marketplace/
```

**Three possible outcomes:**

| Outcome | Cache contains | What it means |
|---------|---------------|---------------|
| ✅ Auto-install works | Both `test-plugin-A` and `test-plugin-B` | Dependency-only bundle architecture is viable. Proceed as planned. |
| ⚠️ Warning, no install | Only `test-plugin-B`, console shows a warning about missing dep | Bundle plugins need fallback design. Pick Option 2 or 3 below. |
| ❌ Field ignored | Only `test-plugin-B`, no warning at all | `dependencies` is decorative. Pick Option 2 or 3 below. |

### Step 4: Document the result

Append a "Result" section to this file with the date, outcome, and any observed Claude Code version/build details. Update `PITFALLS.md` if the outcome was surprising.

---

## Decision Matrix

### Outcome A: Dependencies auto-install ✅

**Proceed with the planned architecture:**
- Each domain bundle = ~10-line `plugin.json` with a `dependencies` array
- Bundles are auto-generated from `catalog.toml` tagging
- Zero content duplication
- `/plugin install skills-communication@dgxsparklabs-marketplace` installs every dependent skill

No further changes needed. Cancel the fallback design work.

### Outcome B or C: Dependencies don't auto-install ⚠️❌

Pick one of three fallback designs:

#### Option 1: Inlined bundles (reject)

Each bundle physically contains copies of all its member plugin content. Pros: works without dep resolution. Cons: defeats the "single source of truth" goal, doubles content size, makes updates require regenerating bundles, breaks individual-vs-bundle install equivalence (installing the bundle gives you something different from installing the members individually). **Do not pick.**

#### Option 2: Bundle ships `install-deps.sh` (likely best fallback)

Each bundle has:
- `plugin.json` (with `dependencies` declared anyway, for future when Anthropic adds the feature)
- `install-deps.sh` — a shell script that runs `claude plugin install <dep>` for each dependency

User flow:
```bash
/plugin install skills-communication@dgxsparklabs-marketplace
bash ~/.claude/plugins/cache/dgxsparklabs-marketplace/skills-communication/install-deps.sh
```

Pros: preserves bundle UX, parallels the rules-activate.sh pattern we're already shipping. Cons: extra manual step.

This is the closest analog to the existing rules architecture and keeps everything inside the `/plugin` mental model.

#### Option 3: Drop bundle plugins entirely

Remove `skills-*` and `rules-*` bundle plugins from the marketplace. Replace with `BUNDLES.md` documentation that lists the install commands:

> **Communication bundle:**
> ```
> /plugin install skill-send-email@dgxsparklabs-marketplace
> /plugin install skill-telegram-notify@dgxsparklabs-marketplace
> ```

Pros: simplest, no bundle plugin maintenance. Cons: loses one-command bundle install, more typing, less discoverable.

**Choose Option 2 unless dep auto-install is added by Anthropic in a near-term release**, in which case revisit and migrate from Option 2 to the planned dependency-only architecture (the `dependencies` field will already be declared).

---

## When to Run This Investigation

**Trigger:** Immediately after `feat/claude-plugin-compliance` is pushed to GitHub for the first time.

**Why early:** Tasks #3, #4, and #5 all assume the dependency-only design. Running this experiment first prevents building work that has to be redone.

**Time budget:** 30 minutes for the experiment, 15 minutes to document the result and update the design if needed.

**Update this file with the result** when complete, then mark task #13 as completed.

---

## Result

**Date:** 2026-05-22
**Verified by:** Claude (during execution of `feat/claude-plugin-compliance`)
**Claude Code version:** as installed via `claude` CLI on this machine
**Outcome:** ✅ **Dependencies auto-install**

### Experiment summary

Built two minimal test plugins per the plan above:

- `test-plugin-a` — content-only plugin with a minimal SKILL.md
- `test-plugin-b` — bundle-style plugin with `"dependencies": ["test-plugin-a"]` and no other content

Bundled them in a local `dep-test-marketplace` and registered it via:

```bash
claude plugin marketplace add ./_dep-test/dep-test-marketplace
```

Installed ONLY the bundle plugin (project scope to avoid leaking into user state):

```bash
claude plugin install test-plugin-b@dep-test-marketplace --scope project
```

### What happened

Install output (verbatim):

> Successfully installed plugin: test-plugin-b@dep-test-marketplace (scope: project) **(+ 1 dependency: test-plugin-a)**

Subsequent `claude plugin list` confirmed both plugins installed and enabled.

### Bonus findings

Several useful behaviors discovered during cleanup that inform our plan:

| Behavior | Detail |
|---------|--------|
| Auto-installed deps are tracked separately from user-installed | They're called "auto-installed dependencies" in CLI output |
| Uninstalling the bundle does NOT auto-remove its deps | Deps become "orphaned" / "no longer needed" but persist until prune |
| `claude plugin prune --scope <scope> -y` removes orphans | The `-y` is needed in non-TTY mode (e.g., scripted execution) |
| Removing a marketplace marks all its plugins as orphaned | Files written to cache with `.orphaned_at` marker; final cleanup is deferred |
| Cache path is `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/` | Versioned subdirectories — multiple installed versions coexist |
| Plugin names must be kebab-case for Claude.ai marketplace sync | Mixed-case names load locally but fail Claude.ai sync; `claude plugin validate` warns |
| `homepage` and `repository` fields in marketplace.json are tolerated | `claude plugin validate` flags them as "Unknown field. Claude Code ignores it at load time." — keep them anyway for documentation, no harm |
| Local-path marketplaces work | `claude plugin marketplace add <local-dir>` succeeds — no GitHub push needed for testing |

### Implications for the marketplace design

1. **Domain bundles work as planned.** `skills-communication`, `rules-quality`, etc. can be dep-only plugins. No `install-deps.sh` script needed.
2. **Update behavior is correct.** When a user bumps their installed bundle version and a new dep was added, the new dep should auto-install too. (Not separately verified; document this for the implementing agent of task #3.)
3. **Pruning is the user's responsibility.** If a user uninstalls a bundle, they must run `claude plugin prune` to remove orphaned deps. Worth mentioning in the contributor tutorials.
4. **Validate during CI.** `claude plugin validate <path>` should run against every plugin in CI as part of task #6. Catches kebab-case violations and unknown fields before they ship.

### Conclusion

The bundle architecture documented in `PLAN_PLUGIN_COMPLIANCE.md` is approved as-is. Proceed with tasks #3-#5 using dependency-only domain bundles. The Option 2 fallback design (bundles ship `install-deps.sh`) is no longer needed but remains documented above as reference.

---

## References

- [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference) — `dependencies` field listed but install behavior was unspecified
- [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) — confirms marketplace.json structure
- [SchemaStore Claude Code Plugin Manifest](https://www.schemastore.org/claude-code-plugin-manifest.json) — canonical schema
- `claude plugin --help`, `claude plugin install --help`, `claude plugin marketplace --help` — most authoritative source we found during this work
- `docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md` — this file
- Task #13 in the project task list
