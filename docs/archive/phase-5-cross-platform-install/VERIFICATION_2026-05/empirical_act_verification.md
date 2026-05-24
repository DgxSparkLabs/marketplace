# Empirical act-based Verification — May 2026

**Date**: 2026-05-24
**Method**: nektos/act 0.2.63 + Docker 29.1.5, image catthehacker/ubuntu:act-latest (Ubuntu 24.04 amd64)
**Branch under test**: feat/claude-plugin-compliance
**Researcher**: general-purpose subagent (Claude Sonnet 4.6)

---

## Per-claim verification table

| ID | Claim | Status | Log file | Key evidence | Reproducible command |
|----|-------|--------|----------|--------------|----------------------|
| C1 | `codex plugin marketplace add ./` local path registers | VERIFIED-PASS | logs/verify-codex-run.log:139-159 | `Added marketplace \`dgxsparklabs-marketplace\` from /mnt/c/.../marketplace. C1_EXIT=0` | `act workflow_dispatch -W docs/VERIFICATION_2026-05/workflows/verify-codex.yml -P ubuntu-latest=catthehacker/ubuntu:act-latest --pull=false` |
| C2 | `codex plugin marketplace add DgxSparkLabs/marketplace` (GitHub shortform, no ref) registers | VERIFIED-FAIL | logs/verify-codex-run.log:161-178 | `Error: invalid marketplace file …: marketplace root does not contain a supported manifest. C2_EXIT=1` | same as C1 |
| C3 | `codex plugin marketplace add DgxSparkLabs/marketplace --ref feat/claude-plugin-compliance` registers | VERIFIED-PASS | logs/verify-codex-run.log:179-198 | `Added marketplace \`dgxsparklabs-marketplace\` from https://github.com/DgxSparkLabs/marketplace.git#feat/claude-plugin-compliance. C3_EXIT=0` | same as C1 |
| C4 | After marketplace registration, `codex plugin list` enumerates our plugins | VERIFIED-PASS | logs/verify-codex-run.log:206-385 | `skill-example@dgxsparklabs-marketplace … not installed … C4_FOUND=YES` | same as C1 |
| C5 | `codex plugin add skill-example@dgxsparklabs-marketplace` succeeds | VERIFIED-FAIL | logs/verify-codex-run.log:386-400 | `Error: missing or invalid plugin.json. Caused by: missing or invalid plugin.json. C5_EXIT=1` | same as C1 |
| C6 | Where Codex looks for manifest after `add owner/repo` | VERIFIED | logs/verify-codex-run.log:401-470 + logs/C6_C7.txt | Repo root; no `.codex-plugin/` exists at root; only `.claude-plugin/marketplace.json`; error is `marketplace root does not contain a supported manifest` | same as C1 |
| C7 | Does Codex require `.codex-plugin/plugin.json` per plugin? | VERIFIED | logs/verify-codex-run.log:386-418 + logs/C6_C7.txt | Error: `missing or invalid plugin.json`; per-plugin dir only has `.claude-plugin/plugin.json`. Codex needs `plugin.json` at per-plugin root (exact path ambiguous from error). | same as C1 |
| G1 | `gemini extensions install ./.gemini/ --consent` local path succeeds | VERIFIED-PASS | logs/verify-gemini-run.log | `Extension "dgxsparklabs-marketplace" installed successfully and enabled. G1_EXIT=0. G1_ASSERT=PASS` | `act workflow_dispatch -W docs/VERIFICATION_2026-05/workflows/verify-gemini.yml -P ubuntu-latest=catthehacker/ubuntu:act-latest --pull=false` |
| G2 | `gemini extensions install https://github.com/DgxSparkLabs/marketplace --consent` succeeds | VERIFIED-FAIL | logs/verify-gemini-run.log + logs/G2.txt | `Configuration file not found at /tmp/gemini-extensionOunyeo/gemini-extension.json. G2_EXIT=1` | same as G1 |
| G3 | `gemini extensions install GitHub URL --ref feat/claude-plugin-compliance --consent` succeeds | VERIFIED-FAIL | logs/verify-gemini-run.log + logs/G3.txt | `Configuration file not found at /tmp/gemini-extensioncULULP/gemini-extension.json. G3_EXIT=1` | same as G1 |
| G4 | `gemini skills install GitHub URL --path _generated/skill-example --consent` succeeds | VERIFIED-FAIL | logs/verify-gemini-run.log + logs/G4.txt | `No valid skills found … Ensure a SKILL.md file exists with valid frontmatter. G4_EXIT=1` | same as G1 |
| G5 | After extension install, `gemini extensions list` shows dgxsparklabs entry | VERIFIED-PASS | logs/verify-gemini-run.log + logs/G5.txt | `G5_FOUND=YES` | same as G1 |
| G6 | After install, `gemini skills list --all` finds telegram-notify | VERIFIED-PASS | logs/verify-gemini-run.log + logs/G6.txt | `G6_EXIT=0. G6_FOUND=YES` | same as G1 |
| CU1 | `agent --version` succeeds after `curl https://cursor.com/install \| bash` | VERIFIED-PASS | logs/verify-cursor-run.log + logs/CU1.txt | `2026.05.20-2b5dd59. CU1_EXIT=0. CU1=PASS` | `act workflow_dispatch -W docs/VERIFICATION_2026-05/workflows/verify-cursor.yml -P ubuntu-latest=catthehacker/ubuntu:act-latest --pull=false` |
| CU2 | Capture install path of `agent` binary | VERIFIED-PASS | logs/verify-cursor-run.log + logs/CU2.txt | `which agent: /root/.local/bin/agent` → symlink to `~/.local/share/cursor-agent/versions/2026.05.20-2b5dd59/cursor-agent` | same as CU1 |
| CU3 | `agent --help` full output + plugin subcommands | VERIFIED-PASS | logs/verify-cursor-run.log + logs/CU3.txt | Full help captured; `--plugin-dir <path>` exists; NO `plugin install`/`plugin list` subcommand found | same as CU1 |
| CL1 | `claude plugin marketplace add ./` registers | VERIFIED-PASS | logs/verify-claude-run.log + logs/CL1.txt | `Successfully added marketplace: dgxsparklabs-marketplace (declared in user settings). CL1=PASS` | `act workflow_dispatch -W docs/VERIFICATION_2026-05/workflows/verify-claude.yml -P ubuntu-latest=catthehacker/ubuntu:act-latest --pull=false` |
| CL2 | `claude plugin install skill-example@dgxsparklabs-marketplace --scope project` succeeds | VERIFIED-PASS | logs/verify-claude-run.log + logs/CL2.txt | `Successfully installed plugin: skill-example@dgxsparklabs-marketplace (scope: project). CL2=PASS` | same as CL1 |
| CL3 | `claude plugin list` shows skill-example after CL2 | VERIFIED-PASS | logs/verify-claude-run.log + logs/CL3.txt | `skill-example@dgxsparklabs-marketplace … Status: ✔ enabled. CL3_FOUND=YES` | same as CL1 |

---

## Detailed findings per platform

### Codex

**CLI version installed**: codex-cli 0.133.0 (via `npm install -g @openai/codex@latest`)

**C1 — Local path (PASS)**

The baseline works. `codex plugin marketplace add ./` in the repo root adds `dgxsparklabs-marketplace` and writes to `~/.codex/config.toml`:

```
[marketplaces.dgxsparklabs-marketplace]
last_updated = "2026-05-24T02:39:01Z"
source_type = "local"
source = "/mnt/c/Users/devic/source/marketplace"
```

Codex reads `.claude-plugin/marketplace.json` as the marketplace manifest for local paths.

**C2 — GitHub shortform without --ref (FAIL)**

`codex plugin marketplace add DgxSparkLabs/marketplace` clones the default branch (main) to a staging directory and then fails:

```
Error: invalid marketplace file `/root/.codex/.tmp/marketplaces/.staging/marketplace-add-RcEj0t`:
  marketplace root does not contain a supported manifest
```

The default branch (main) does not have any recognized manifest at the repo root that Codex accepts for the no-ref path. The `.claude-plugin/marketplace.json` is present but is not recognized without the feature branch context.

**C3 — GitHub shortform with --ref (PASS)**

`codex plugin marketplace add DgxSparkLabs/marketplace --ref feat/claude-plugin-compliance` succeeds:

```
Added marketplace `dgxsparklabs-marketplace` from https://github.com/DgxSparkLabs/marketplace.git#feat/claude-plugin-compliance.
Installed marketplace root: /root/.codex/.tmp/marketplaces/dgxsparklabs-marketplace
```

The feature branch's `.claude-plugin/marketplace.json` is found and accepted by Codex.

**C4 — Plugin enumeration (PASS)**

After local-path marketplace registration, `codex plugin list` enumerates all 81 plugins from `.claude-plugin/marketplace.json`. The "silent fail" claim in the research brief is **refuted**. All plugins appear with status "not installed". The marketplace manifest path shown in the output:

```
Marketplace `dgxsparklabs-marketplace`
/mnt/c/Users/devic/source/marketplace/.claude-plugin/marketplace.json
```

**C5 — Plugin install (FAIL)**

`codex plugin add skill-example@dgxsparklabs-marketplace` fails after successful marketplace registration:

```
Error: missing or invalid plugin.json
Caused by:
    missing or invalid plugin.json
```

**C6 — Manifest resolution path for GitHub shortform**

Codex clones the GitHub repo to `/root/.codex/.tmp/marketplaces/.staging/marketplace-add-<random>/`. The full repo content is present in staging. The repo root does NOT have `.codex-plugin/` directory — only `.claude-plugin/marketplace.json`. Codex accepts `.claude-plugin/marketplace.json` as the marketplace-level manifest when present (confirmed by C1 and C3 passing).

**C7 — Per-plugin manifest requirement**

The `_generated/skill-example/` directory contains:
- `.claude-plugin/plugin.json` (Claude Code manifest, inside subdirectory)
- `SKILL.md`
- `README.md`

Codex's `plugin add` error is `missing or invalid plugin.json` — referencing `plugin.json` directly (not `.codex-plugin/plugin.json`). The exact expected path cannot be confirmed solely from error output, but what is confirmed is that `.claude-plugin/plugin.json` (inside a subdirectory) is NOT recognized. Our per-plugin directories lack a Codex-compatible manifest at whatever path Codex expects.

---

### Gemini

**CLI installed**: `@google/gemini-cli@latest` via npm. Install succeeded; `gemini --version` returned successfully.

**G1 — Local path (PASS)**

`echo "y" | gemini extensions install ./.gemini/ --consent` succeeds:

```
Extension "dgxsparklabs-marketplace" installed successfully and enabled.
G1_EXIT=0
```

**G2 — GitHub URL without ref (FAIL)**

`gemini extensions install https://github.com/DgxSparkLabs/marketplace --consent` clones the repo and then fails:

```
Configuration file not found at /tmp/gemini-extensionOunyeo/gemini-extension.json
```

Gemini expects `gemini-extension.json` at the **repo root** (`/tmp/gemini-extension*/gemini-extension.json`). Our repo stores it at `.gemini/gemini-extension.json`, which is a subdirectory. This is a layout mismatch.

**G3 — GitHub URL with --ref (FAIL)**

Same error with `--ref feat/claude-plugin-compliance`:

```
Configuration file not found at /tmp/gemini-extensioncULULP/gemini-extension.json
```

The `--ref` works (branch is cloned) but the manifest is still expected at the repo root, not `.gemini/`.

**G4 — GitHub URL with --path (FAIL, different reason)**

`gemini skills install https://github.com/DgxSparkLabs/marketplace --path _generated/skill-example --consent` clones correctly and navigates to the path, but then fails:

```
Searching for skills in /tmp/gemini-skill-SVtviM/_generated/skill-example...
No valid skills found in https://github.com/DgxSparkLabs/marketplace at path "_generated/skill-example".
Ensure a SKILL.md file exists with valid frontmatter.
```

The `--path` argument IS valid for `gemini skills install` (confirmed: directory is navigated). The failure is that Gemini's skill installer does not recognize our SKILL.md frontmatter format as valid for remote install. The local extension path works (G1) because `.gemini/` contains `gemini-extension.json` which passes validation.

Additional finding: `gemini extensions install --path` does NOT exist:
```
Unknown argument: path
gemini extensions install <source> [--auto-update] [--pre-release]
```

**G5 — extensions list (PASS)**

After local install: `gemini extensions list 2>&1 | grep -F "dgxsparklabs"` → `G5_FOUND=YES`.

**G6 — skills list (PASS)**

`gemini skills list --all 2>&1 | grep -iF "telegram-notify"` → `G6_FOUND=YES`. The `--all` flag is valid and skills from installed extensions are discoverable.

---

### Cursor CLI

**CU1 — agent --version (PASS)**

The open discrepancy from `cursor.md` is **fully resolved**. The install succeeds:

```
Cursor Agent Installer
Detecting system architecture... Detected linux/x64
Downloading Cursor Agent package...
  Download URL: https://downloads.cursor.com/lab/2026.05.20-2b5dd59/linux/x64/agent-cli-package.tar.gz
Package installed successfully
Symlink created
Installation Complete!
```

`agent --version` returns `2026.05.20-2b5dd59` (exit 0). The prior CI failure was due to `~/.local/bin` not being in `$PATH` at test time — the binary IS installed but PATH was not expanded.

**CU2 — Install path (PASS)**

```
which agent:        /root/.local/bin/agent
which cursor-agent: /root/.local/bin/cursor-agent
Real binary:        /root/.local/share/cursor-agent/versions/2026.05.20-2b5dd59/cursor-agent
Config:             ~/.cursor/cli-config.json
```

Both `agent` and `cursor-agent` are symlinks to the versioned real binary.

**CU3 — Help output and plugin subcommands (PASS / NO plugin commands)**

Full `agent --help` captured. Plugin-related findings:

- `--plugin-dir <path>` flag exists: loads a local plugin directory at runtime (not a persistent install).
- NO `plugin install`, `plugin list`, `marketplace`, or `add-plugin` subcommand exists.
- Commands: `install-shell-integration`, `uninstall-shell-integration`, `login`, `logout`, `mcp`, `worker`, `status|whoami`, `models`, `about`, `update`, `create-chat`, `generate-rule|rule`, `agent`, `ls`, `resume`, `help`.

The research agent's finding that "no plugin CLI subcommands exist" is confirmed by live binary output.

---

### Claude Code

**Claude version installed**: 2.1.150 (Claude Code)

**CL1 — Marketplace add (PASS)**

```
Adding marketplace…✔ Successfully added marketplace: dgxsparklabs-marketplace (declared in user settings)
CL1=PASS
```

Marketplace list confirms:
```
  ❯ dgxsparklabs-marketplace
    Source: Directory (/mnt/c/Users/devic/source/marketplace)
```

**CL2 — Plugin install (PASS)**

```
Installing plugin "skill-example@dgxsparklabs-marketplace"...
✔ Successfully installed plugin: skill-example@dgxsparklabs-marketplace (scope: project)
CL2=PASS
```

**CL3 — Plugin list (PASS)**

```
Installed plugins:
  ❯ skill-example@dgxsparklabs-marketplace
    Version: 1.0.0
    Scope: project
    Status: ✔ enabled
CL3_FOUND=YES
```

Plugin cache: `~/.claude/plugins/cache/dgxsparklabs-marketplace/skill-example/1.0.0/.claude-plugin/plugin.json`

---

## What I could not verify

1. **Exact Codex per-plugin manifest path** (C7): The error `missing or invalid plugin.json` identifies the problem but does not tell us whether Codex expects `plugin.json` at the per-plugin root, `.codex-plugin/plugin.json`, or another location. Inspecting Codex source code or a working Codex-compatible plugin repo would resolve this.

2. **G2/G3 root manifest fix**: Whether placing `gemini-extension.json` at the repo root (alongside `.gemini/gemini-extension.json`) would fix GitHub URL installs. This is the likely fix but was not tested in this verification run.

3. **G4 SKILL.md frontmatter format**: The exact frontmatter fields Gemini's skill installer requires for remote GitHub skill install. The local extension path works because the extension's `gemini-extension.json` validates differently from remote skill install.

4. **C2 with main branch fix**: Whether adding a `.codex-plugin/marketplace.json` or symlink at the repo root would fix the no-ref shortform install.

---

## Summary of corrections to the prior research

### Corrections to claims in the brief

| Original claim | Actual finding |
|----------------|----------------|
| "Codex enumeration silently fails for our plugins despite marketplace registration succeeding" | **WRONG.** Enumeration works correctly. `codex plugin list` shows all 81 plugins after local-path marketplace add (C4=PASS). The failure is only at the *install* step (C5). |
| "Codex supports `codex plugin marketplace add owner/repo` GitHub shortform" | **PARTIALLY WRONG.** Shortform works WITH `--ref` pointing to the feature branch (C3=PASS). Without `--ref`, it clones the default branch (main) which lacks the recognized manifest, causing failure (C2=FAIL). The shortform itself works; the issue is the default branch not having the right manifest at the root. |
| "Codex requires per-plugin `.codex-plugin/plugin.json`" | **UNCONFIRMED AS TO EXACT PATH** — but confirmed that `.claude-plugin/plugin.json` (inside subdirectory) does NOT satisfy Codex. The error says `missing or invalid plugin.json` without a path. |
| "Gemini supports `gemini extensions install https://github.com/...`" | **VERIFIED-FAIL.** Gemini clones the repo but expects `gemini-extension.json` at the repo root, not at `.gemini/gemini-extension.json`. This is a layout mismatch in our repo. |
| Prior CI tested `cursor --version` instead of `agent --version` (cursor.md open discrepancy) | **RESOLVED.** `agent --version` succeeds. The prior failure was PATH not including `~/.local/bin`, not a missing binary. Binary is at `~/.local/share/cursor-agent/versions/2026.05.20-2b5dd59/cursor-agent`. |

---

## Reproduce instructions

See `docs/VERIFICATION_2026-05/reproduce.sh` for the full command list.

Prerequisites:
- nektos/act 0.2.63+ installed and in PATH
- Docker Desktop running with `catthehacker/ubuntu:act-latest` image available
- Run from the repo root: `C:/Users/devic/source/marketplace`

```powershell
# Pull image once
docker pull catthehacker/ubuntu:act-latest

# Run all four verification workflows (sequentially to avoid Docker auth rate limiting)
act workflow_dispatch -W docs/VERIFICATION_2026-05/workflows/verify-codex.yml `
  -P ubuntu-latest=catthehacker/ubuntu:act-latest `
  --container-architecture linux/amd64 --pull=false `
  2>&1 | Tee-Object docs/VERIFICATION_2026-05/logs/verify-codex-run.log

act workflow_dispatch -W docs/VERIFICATION_2026-05/workflows/verify-gemini.yml `
  -P ubuntu-latest=catthehacker/ubuntu:act-latest `
  --container-architecture linux/amd64 --pull=false `
  2>&1 | Tee-Object docs/VERIFICATION_2026-05/logs/verify-gemini-run.log

act workflow_dispatch -W docs/VERIFICATION_2026-05/workflows/verify-cursor.yml `
  -P ubuntu-latest=catthehacker/ubuntu:act-latest `
  --container-architecture linux/amd64 --pull=false `
  2>&1 | Tee-Object docs/VERIFICATION_2026-05/logs/verify-cursor-run.log

act workflow_dispatch -W docs/VERIFICATION_2026-05/workflows/verify-claude.yml `
  -P ubuntu-latest=catthehacker/ubuntu:act-latest `
  --container-architecture linux/amd64 --pull=false `
  2>&1 | Tee-Object docs/VERIFICATION_2026-05/logs/verify-claude-run.log
```

Each log contains the full stdout+stderr of the act run. Per-claim snippets are in `logs/<ID>.txt`.
