# GitHub Support Request — Allow `@openai/codex` and `@google/gemini-cli` in Actions

This document is a copy-pasteable support ticket for GitHub Support, asking that the npm packages `@openai/codex` and `@google/gemini-cli` be permitted in this organization's GitHub Actions runners. Both packages are first-party CLI tools from OpenAI and Google respectively; both are MIT/Apache-2.0 licensed. They're currently blocked at what appears to be an organization-or-repository-level policy.

## How to file

1. Go to [GitHub Support contact form](https://support.github.com/contact).
2. Select category: **Account & profile** → **Other** (or **Actions and packages** if visible).
3. Subject: `Request: allow @openai/codex and @google/gemini-cli in Actions runners for DgxSparkLabs org`
4. Paste the body below.

## The request body (copy-paste)

```
Hello GitHub Support,

We're the DgxSparkLabs organization (https://github.com/DgxSparkLabs).

We've observed that GitHub Actions workflows referencing the npm packages
`@openai/codex` and `@google/gemini-cli` fail at the runner-startup phase
with a 0-second exit and no useful diagnostic. We've reproduced this
across 12+ workflow variants on our `DgxSparkLabs/marketplace` repository
during May 2026 (CI run logs available at
https://github.com/DgxSparkLabs/marketplace/actions?query=branch%3Aexp%2Fcli-empirical-discovery).

Both packages are:

- First-party, published by their respective vendors:
  - `@openai/codex` is published by OpenAI under Apache-2.0
    (https://www.npmjs.com/package/@openai/codex)
  - `@google/gemini-cli` is published by Google under Apache-2.0
    (https://www.npmjs.com/package/@google/gemini-cli)
- Legitimate CLI tools used in AI-agent workflows
- Verified by their respective publishers on npm
- Used in our planned multi-platform CI/CD validation of an open-source
  AI agent skills marketplace

Our use case: we ship a Claude Code plugin marketplace and want to verify
in CI that our generated artifacts (skill directories, MCP server configs,
rule files) are correctly detected by each platform's CLI. This requires
running auth-free inspection commands like `codex mcp list`, `codex plugin
marketplace add <local-path>`, `gemini skills list`, `gemini extensions
list`, and `gemini mcp list`. We do not invoke any AI inference in CI; we
only run local-state inspection commands. No API keys are used.

Request: please confirm whether these packages are blocked, and if so,
whether they can be added to our organization's allowlist. If the block
is at the GitHub Actions runner level (not configurable per org), please
advise the correct mechanism for an org admin to permit these packages.

Reference data:
- npm package metadata: @openai/codex@0.133.0 (latest as of 2026-05-22),
  @google/gemini-cli@0.42.0
- Verified locally outside CI: both packages install cleanly via `npm
  install -g`, expose auth-free subcommands, and have no malicious
  behavior observed
- Empirical CI evidence: the runs in the link above show 0-second
  failures across multiple variants (direct install, install via
  `npx`, install with version pinning, etc.) — strongly suggesting a
  policy block rather than a transient infrastructure issue

Thank you,
DgxSparkLabs
```

## What the response might be

| Possible response | Our follow-up |
|------------------|---------------|
| "These are allowed; check your workflow config" | Reproduce the failure with a minimal test workflow, file a ticket with that minimal case |
| "These are blocked by [policy X]; you can opt in via [setting Y]" | Apply the setting; flip Codex/Gemini compat workflows from advisory to required (per the promotion path in `PLATFORM_VALIDATION_CICD_PLAN.md` decision #8) |
| "These are blocked at the npm-publisher level; we can't override per-org" | Update the plan to permanently rely on local-dev fallback scripts; document this finding |
| (no response within 1 week) | Follow up with the support ticket ID + ask for status |

## What happens to the validation plan independent of the support response

The plan in `PLATFORM_VALIDATION_CICD_PLAN.md` already handles both outcomes:

- **If whitelist is granted:** `compat-codex.yml` and `compat-gemini.yml` (and the Codex/Gemini matrix rows in shared workflows) flip from advisory to required after one green CI run on `main`.
- **If whitelist is denied or indefinitely delayed:** `scripts/validate-codex-local.sh` and `scripts/validate-gemini-local.sh` are the primary verification path. CI workflows for those platforms remain disabled. Local-dev script invocation is required before opening PRs that change Codex/Gemini-relevant content.

The implementation can proceed before the support response arrives.

## After-the-fact tracking

When the request is filed, capture:

- Support ticket number: `_____________`
- Date filed: `_____________`
- Date of GitHub response: `_____________`
- Outcome: `_____________`

Update this document with the final outcome so future maintainers know what was attempted.
