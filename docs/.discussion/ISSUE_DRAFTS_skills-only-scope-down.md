# Issue drafts — skills-only, Claude-only template marketplace scope-down

> Status: FILED 2026-07-25 on DgxSparkLabs/marketplace. Letter → issue map:
> A=#18 (umbrella) · J=#19 (naming/UX) · B=#20 C=#21 D=#22 E=#23 F=#24 G=#25 H=#26 I=#27
> (constructs) · K=#28 L=#29 M=#30 N=#31 O=#32 (former platforms) · P=#33 Q=#34 R=#35 S=#36
> (new platforms). The 13 `type:/area:/status:` labels exist in the repo. GitHub is now the
> source of truth; this file is the historical draft.
>
> Doc links verified 2026-07-25 against https://code.claude.com/docs/en/plugins-reference.
> No issue for output-styles: deprecated upstream (styles migrated to skills), not returning.

## Label taxonomy (created before any issue is filed)

Three orthogonal prefixes; every issue gets exactly one `type:`, at least one `area:`, and
`status:` labels as applicable. Filterable and self-explanatory by design
(e.g. `label:type:feature label:area:platform` = "all future platform expansions").

| Label | Meaning |
|---|---|
| `type:feature` | adds capability that doesn't exist today |
| `type:refactor` | restructures without changing user-facing behavior promises |
| `type:investigation` | produces knowledge/standards, not code |
| `type:fix` | corrects a defect |
| `type:docs` | documentation only |
| `area:construct` | a plugin construct type (skills, hooks, …) |
| `area:platform` | a target agent platform (Claude, Codex, …) |
| `area:naming-ux` | naming standards + user-interaction surfaces |
| `area:ci` | pipelines, automation, the generator |
| `status:someday` | deliberately deferred; part of the documented future, not the present |
| `status:blocked-upstream` | cannot proceed until an upstream platform change lands |
| `status:upstream-experimental` | depends on a feature its platform marks experimental |
| `breaking-change` | removes or changes something users may depend on |

---

## Issue A (umbrella) — Scope down: skills-only, Claude-only template marketplace

**Labels:** `type:refactor`, `area:construct`, `area:platform`, `breaking-change`

### Why

The marketplace currently ships ten construct types compiled for six platforms (Claude Code,
Codex, Gemini CLI, Cursor, Windsurf, Devin). It works — v1.0.0 is published and CI proves
registration → enumeration → install end-to-end — but the maintenance surface (7 platform
classes, 10 construct classes, ~10 compat workflows, 6 generated mirrors, an installer CLI)
is too large for a solo maintainer, and the breadth obscures the actual value:

**a fork-and-forget template for hosting your own Claude Code skill marketplace.**

That value is provable with one construct on one platform. So we shrink to exactly that,
and govern re-expansion — along BOTH axes, constructs and platforms — through the child
issues below. Shrinking is deliberate deferral, not abandonment: every removed capability
has a `status:someday` issue describing what it is and what bringing it back requires.

### The contract this repo exists to provide

```
contributor forks this repo
 └▶ drops a folder into src/skills/<their-skill>/     ← the ONLY thing they touch
     └▶ git commit + push to their fork's main
         └▶ GitHub Actions (in THEIR fork) fires
             └▶ validates skill structure (frontmatter, naming)
                 └▶ regenerates _generated/ + .claude-plugin/marketplace.json
                     └▶ auto-commits the generated output back to main
                         └▶ user: claude plugin marketplace add <their-fork>
                             └▶ /plugin install <their-skill>
```

Contributors need git only — no Python, no generator knowledge. CI owns packaging,
manifests, paths, and names.

### Design values (bind every current and future change)

1. **Naming and user interaction are first-class.** What a user types
   (`claude plugin marketplace add <owner>/<repo>`, `/plugin install <skill>@<marketplace>`),
   what appears in listings, what a forker must rename versus what renames itself — these
   surfaces are the product. No expansion lands without the naming/UX investigation of #J
   applied to it. No confusion or double meaning anywhere.
2. **One source of truth.** Contributors touch `src/skills/` only; everything else is
   generated, and CI is the only writer of generated output.
3. **Feature-level governance.** Re-expansion issues describe what a capability does and
   what reviving it requires — never implementation mechanics, because the codebase will
   have changed by revival time.

### Scope of the shrink

- **Platform:** Claude Code only. The `.codex/`, `.gemini/`, `.cursor/`, `.windsurf/`,
  `.devin/`, `.agents/` mirrors, `gemini-extension.json`, `.cursor-plugin/`, their compat
  workflows, and the `agents` installer CLI are removed.
- **Construct:** skills only. All other construct types are removed (sources, generator
  classes, wrappers, workflows, tests, docs). Catalog bundles are removed — every skill is
  individually installable; curation is the forker's README's job.
- Everything removed stays recoverable via git history. Nothing is archived in-tree.

### Checklist

- [ ] PR 1 — Claude-only: remove non-Claude platforms, mirrors, compat CI, `agents` CLI
- [ ] PR 2 — skills-only: remove non-skill constructs and catalog bundles
- [ ] PR 3 — CI inversion: auto-regenerate + auto-commit on push; contributors never run the generator
- [ ] PR 4 — template polish: README/docs rewritten for the forker audience
- [ ] End-to-end proof: a fresh fork + one committed skill installs via `claude plugin marketplace add <fork>`
- Cross-cutting: #J naming & user-interaction standards (investigation; gates all expansions)
- Construct re-expansion: #B commands · #C agents · #D hooks · #E MCP servers · #F LSP servers · #G rules · #H themes · #I monitors
- Platform re-expansion (formerly supported): #K Codex · #L Gemini CLI · #M Cursor · #N Windsurf · #O Devin
- Platform expansion (new, never supported): #P GitHub Copilot CLI · #Q xAI Grok Build · #R Hermes Agent · #S Google Antigravity
  (further platforms follow the same issue template — one issue per platform, `type:feature area:platform status:someday`)

---

## Issue J — Naming & user-interaction standards (cross-cutting investigation)

**Labels:** `type:investigation`, `area:naming-ux`

**Why:** The user-visible surfaces of this marketplace ARE the product: what someone types,
what they see listed, and what a forker must change to make the template theirs. Today these
conventions are implicit (kebab-case, `./`-prefixed source paths, scoped command names).
This issue makes them an explicit, enforced standard — and every re-expansion issue
(constructs #B–#I, platforms #K–#O) is gated on applying it.

**Questions to investigate and settle:**

1. **Install-command surface.** Exactly what does a user type at each step
   (`claude plugin marketplace add <owner>/<repo>`, `/plugin install <name>@<marketplace>`)?
   Which parts derive from repo identity, which from `MARKETPLACE.toml`, which from the
   skill folder name? Document the full name-resolution chain.
2. **Scoped-name surface.** How installed skills surface in-session
   (`<plugin>:<skill>` scoping, typeahead appearance, collision behavior between plugins
   and with built-ins).
3. **Fork identity.** When someone forks: what renames automatically (repo slug in install
   commands), what they MUST edit (marketplace name/owner metadata), what they may not
   touch. Deliverable: a "make it yours" checklist in the README measured in minutes.
4. **Naming rules.** Casing, allowed characters, length, reserved words, uniqueness — as
   validation the CI runs on every contributed skill, not prose.
5. **Future-surface rule.** Any revived construct or platform must answer 1–4 for its own
   surfaces before it lands (e.g. what `/plugin install` means on Codex; how a revived
   command avoids shadowing a skill).

**Deliverables:** a naming-standard section in the docs, CI validation rules implementing
it, and the README "make it yours" checklist. Feature-level here; the mechanics live in the
PRs that implement them.

---

## Construct re-expansion issues (#B–#I)

Common to all eight: **Labels** `type:feature`, `area:construct`, `status:someday` (plus
noted extras). **Status:** removed in the skills-only scope-down (#A). May return.
**Vision fit:** identical contract to skills — commit a folder, CI packages,
`/plugin install`. **Gate:** the #J naming/UX standard applied to this construct's surfaces
before revival. **Deliberately omitted:** implementation mechanics — see #A's
feature-level-governance rule.

### Issue B — Re-expansion candidate: slash commands

**What it is:** User-invoked prompts: a markdown file becomes a `/name` command the user
types to run a predefined prompt with arguments. In plugins they live in a `commands/`
directory (or alongside skills) and are auto-discovered on install, surfacing as
`/plugin-name:command-name`.
**Official docs:** https://code.claude.com/docs/en/plugins-reference (Skills/commands
section) · https://code.claude.com/docs/en/skills
**How it fit here:** shipped as `src/commands/<name>/` sources compiled into plugins.
**Naming/UX note:** commands share the `/` namespace with skills and built-ins — collision
and shadowing rules are the #J question to answer first.
**Revival criteria:** demand for user-invoked (rather than model-invoked) prompts in forks;
the skills pipeline stable enough to generalize. Lowest-cost revival (closest sibling to
skills).

### Issue C — Re-expansion candidate: agents (subagents)

**What it is:** Specialized subagents — markdown files with frontmatter (`name`,
`description`, `model`, `tools`, …) in an `agents/` directory. Once the plugin is enabled
they appear in the @-mention typeahead under a scoped name (`my-plugin:code-reviewer`) and
Claude can invoke them automatically when a task matches.
**Official docs:** https://code.claude.com/docs/en/sub-agents ·
https://code.claude.com/docs/en/plugins-reference (Agents section)
**How it fit here:** shipped as `src/agents/<name>/` sources compiled into plugins.
**Naming/UX note:** scoped-name visibility in the typeahead is a #J surface.
**Revival criteria:** demand for shareable subagents in marketplace forks.

### Issue D — Re-expansion candidate: hooks

**What it is:** Event handlers that fire automatically on Claude Code events (tool calls,
prompts, session lifecycle). Shipped as `hooks/hooks.json` (or inline in `plugin.json`);
handler types include shell commands and MCP tool calls — how a plugin enforces policy or
automates reactions without the model having to remember.
**Official docs:** https://code.claude.com/docs/en/hooks ·
https://code.claude.com/docs/en/plugins-reference (Hooks section)
**How it fit here:** shipped as `src/hooks/<name>/` sources compiled into plugins.
**Revival criteria:** demand for shareable event automation. Hooks execute arbitrary shell
commands — revival must also settle a review/trust stance for forks.

### Issue E — Re-expansion candidate: MCP servers

**What it is:** Bundled Model Context Protocol servers (`.mcp.json` in the plugin root or
inline in `plugin.json`) connecting Claude Code to external tools and services. Bundled
servers' tools surface under scoped names (`mcp__plugin_<plugin>_<server>__<tool>`).
**Official docs:** https://code.claude.com/docs/en/mcp (incl. "Plugin-provided MCP
servers") · https://code.claude.com/docs/en/plugins-reference (MCP section)
**How it fit here:** shipped as `src/mcp-servers/<name>/` sources compiled into plugins.
**Naming/UX note:** the long scoped tool names are exactly the kind of user-visible surface
#J standardizes.
**Revival criteria:** demand for shareable tool-server configs in marketplace forks.

### Issue F — Re-expansion candidate: LSP servers

**What it is:** Language Server Protocol integrations (`.lsp.json` in the plugin root or
inline in `plugin.json`), giving Claude language-aware capabilities (diagnostics,
navigation) for the languages the server covers.
**Official docs:** https://code.claude.com/docs/en/plugins-reference (LSP servers section —
no dedicated page as of 2026-07)
**How it fit here:** shipped as `src/lsp-servers/<name>/` sources compiled into plugins.
**Revival criteria:** demand for shareable language tooling configs in marketplace forks.

### Issue G — Re-expansion candidate: rules

**Extra labels:** `status:blocked-upstream`
**What it is:** Always-on memory/policy files — standing instructions Claude reads from
`.claude/rules/` via its memory subsystem on every session, unlike skills which load on
demand.
**Official docs:** rules are **not a Claude Code plugin component** — no plugin schema
exists for them. Feature request open upstream: anthropics/claude-code#21163.
**How it fit here:** the one construct that never fit the plugin pipeline: Claude users
copied `src/rules/<name>/rule.md` into `.claude/rules/` by hand (with an activation helper
script), while other platforms got generated mirrors. That asymmetry was a standing source
of confusion — exactly what the scope-down eliminates.
**Revival criteria:** anthropics/claude-code#21163 (or equivalent) lands, making rules a
native plugin component. Do not revive before then — the copy-in workaround is the
confusion this repo is shedding.

### Issue H — Re-expansion candidate: themes

**Extra labels:** `status:upstream-experimental`
**What it is:** Color themes — JSON files in `themes/` with a base preset plus sparse
color-token overrides — appearing in `/theme` alongside built-in presets as
`custom:<plugin-name>:<slug>`. Plugin themes are read-only (Ctrl+E copies one locally).
An **experimental** plugin component.
**Official docs:** https://code.claude.com/docs/en/plugins-reference (Themes section)
**How it fit here:** shipped as `src/themes/<name>/` sources compiled into plugins.
**Revival criteria:** the themes component graduates from experimental, plus demand.

### Issue I — Re-expansion candidate: monitors

**Extra labels:** `status:upstream-experimental`
**What it is:** Background monitors — configured watchers (`monitors.json` /
`experimental.monitors` in `plugin.json`) that stream events into the session, in the
spirit of the Monitor tool. An **experimental** component, skipped on hosts without the
Monitor tool.
**Official docs:** https://code.claude.com/docs/en/plugins-reference (Monitors section) ·
https://code.claude.com/docs/en/tools-reference#monitor-tool
**How it fit here:** shipped as `src/monitors/<name>/` sources compiled into plugins.
**Revival criteria:** the monitors component graduates from experimental, plus demand.

---

## Platform re-expansion issues (#K–#O)

Common to all five: **Labels** `type:feature`, `area:platform`, `status:someday`.
**Status:** support removed in the Claude-only scope-down (#A). May return.
**Vision fit:** the same fork→commit→CI→install contract, extended so one committed skill
also becomes installable on this platform via its native mechanism — CI still owns all
packaging; the contributor still touches only `src/skills/`.
**Gate:** the #J naming/UX investigation applied to this platform's install commands,
listing surfaces, and name-resolution chain before revival.
**Deliberately omitted:** implementation mechanics (the old mirror/generator code will be
stale by revival time — recover concepts, not code, from git history).
**Template note:** a platform not listed here (new CLI agents appear constantly) gets a new
issue in exactly this shape.

### Issue K — Platform re-expansion: OpenAI Codex CLI

**What it is:** OpenAI's terminal coding agent. Previously supported end-to-end: it has a
native plugin system (`codex plugin marketplace add <owner>/<repo>`, `codex plugin
install`) that this repo's generated `.codex/` mirror and per-plugin manifests satisfied,
verified by compat CI (registration → enumeration → install).
**Revival criteria:** demand from forks; Codex's plugin surface stable; #J answered for
Codex's command shapes.

### Issue L — Platform re-expansion: Gemini CLI

**What it is:** Google's terminal coding agent. Previously supported via its extensions
mechanism (`gemini extensions install <github-url> --consent`), satisfied by the generated
root `gemini-extension.json` + `.gemini/` mirror, verified by compat CI. Known quirk from
prior support (kept as knowledge, not mechanics): remote skill install with `--path`
failed validation while local install worked.
**Revival criteria:** demand from forks; #J answered for Gemini's install/consent flow.

### Issue M — Platform re-expansion: Cursor (agent CLI + IDE)

**What it is:** Cursor's IDE and its `agent` CLI. Previously supported via the
`.cursor-plugin/marketplace.json` team-marketplace manifest (Dashboard import of the GitHub
URL; IDE `/add-plugin`) and a generated `.cursor/` mirror. Install was GUI-only — the
`agent` CLI had no plugin commands (it did expose `--plugin-dir` for runtime injection).
**Revival criteria:** Cursor ships a CLI install path (removes the GUI-only friction), or
fork demand justifies the GUI flow; #J answered for Cursor's surfaces.

### Issue N — Platform re-expansion: Windsurf

**What it is:** The Windsurf IDE (Cascade agent). Previously supported via auto-discovery:
Cascade reads `.windsurf/rules/` and `.agents/skills/` from a cloned repo — no install
command at all (clone + open). No headless CLI exists, so compat CI could not exercise it
end-to-end.
**Revival criteria:** Windsurf ships a CLI/headless surface CI can verify, plus demand;
#J answered for its discovery-based (command-less) UX.

### Issue O — Platform re-expansion: Devin

**What it is:** Cognition's Devin agent and CLI. Previously supported via `.agents/skills/`
auto-discovery (`devin skills list` enumerates after clone). Known quirk from prior
support: the installer exits 1 in non-TTY environments (CI worked around it).
**Revival criteria:** demand from forks; Devin's skill discovery stable; #J answered for
its surfaces.

---

## New-platform expansion issues (#P–#S)

Common to all four: **Labels** `type:feature`, `area:platform`, `status:someday`.
**Status:** never supported here; candidate for future expansion.
**Vision fit:** the fork→commit→CI→install contract extended so a committed skill also
becomes installable on this platform via whatever native mechanism it offers.
**Gate:** unlike the formerly-supported platforms, these need a *discovery investigation
first* — does the platform have a plugin/skill/marketplace distribution surface at all,
and what shape is it? — then the #J naming/UX standard applied to it.
**Deliberately omitted:** implementation mechanics, per #A.

### Issue P — Platform expansion: GitHub Copilot CLI

**What it is:** GitHub's terminal coding agent (`copilot`), the agentic CLI sibling of the
Copilot IDE product family.
**Investigation first:** what distribution surface exists (Copilot extensions? skills
directories? MCP config?) and whether a GitHub-repo marketplace maps onto it.

### Issue Q — Platform expansion: xAI Grok Build

**What it is:** xAI's terminal coding agent (`grok`), launched May 2026 — full-screen TUI
with subagent parallelism, plan mode, and headless mode, installed via `x.ai/cli`.
**Reference:** https://docs.x.ai/build/overview · https://x.ai/news/grok-build-cli
**Investigation first:** whether Grok Build exposes a plugin/skill install surface a forked
repo can serve.

### Issue R — Platform expansion: Hermes Agent (Nous Research)

**What it is:** Nous Research's open-source autonomous agent — a terminal TUI plus a
gateway reachable from Telegram/Discord/Slack/WhatsApp/Signal/Email, with persistent
memory and bundled skills (it can even orchestrate other coding agents).
**Reference:** https://github.com/nousresearch/hermes-agent ·
https://hermes-agent.nousresearch.com/docs/
**Investigation first:** how Hermes discovers/installs skills and plugins, and whether a
GitHub skill marketplace maps onto that mechanism.

### Issue S — Platform expansion: Google Antigravity

**What it is:** Google's agentic development platform (launched Nov 2025) — an agent-first
IDE/CLI family powered by Gemini, oriented around autonomous agents working across editor,
terminal, and browser.
**Investigation first:** what plugin/skill/extension surface Antigravity exposes (and how
it relates to Gemini CLI extensions, #L), then #J applied to it.
