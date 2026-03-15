# SKILL.md Format Reference

Complete specification for the `SKILL.md` file format used by agent skills.

## File Structure

A `SKILL.md` file has two parts:

1. **YAML frontmatter** — metadata between `---` delimiters (optional but recommended)
2. **Prompt body** — Markdown content that gets injected into the agent's context when the skill is invoked

```markdown
---
# YAML frontmatter (metadata)
name: my-skill
description: What this skill does
---

# Prompt body (Markdown)
Instructions for the agent go here.
```

---

## Frontmatter Fields

All fields are optional. Frontmatter itself is optional (the file can be just Markdown).

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | string | directory name | Display name of the skill. Used in UI and completions. |
| `description` | string | none | Short description shown in slash-command completions. Keep under 80 characters. |
| `argument-hint` | string | none | Hint shown after the command name, e.g. `[file]`, `[url] [format]`. |
| `model` | string | current model | Override the model used when this skill runs. Examples: `sonnet`, `opus`. |
| `allowed-tools` | list of strings | all tools | Restrict which tools the skill can use. If omitted, the skill can use all tools. |
| `permissions` | object | inherit session | Permission overrides for this skill (see Permissions section). |
| `triggers` | list of strings | `[user, model]` | How the skill can be invoked (see Triggers section). |

### `allowed-tools` values

Built-in tools:
- `read` — read files
- `edit` — edit files
- `grep` — search file contents with regex
- `glob` — find files by name pattern
- `exec` — execute shell commands

MCP tools use the naming convention `mcp__<server>__<tool>`:
```yaml
allowed-tools:
  - read
  - mcp__github__list_issues
  - mcp__github__create_issue
```

### `permissions` object

```yaml
permissions:
  allow:          # Auto-approved during skill execution
    - Read(src/**)
    - Exec(npm run test)
    - Write(output/**)
  deny:           # Blocked during skill execution
    - Write(/etc/**)
    - exec
  ask:            # Always prompt the user
    - Write(src/**)
```

Permission scopes use glob patterns:
- `Read(<glob>)` — file read access
- `Write(<glob>)` — file write access
- `Exec(<command-prefix>)` — shell command execution

Permissions are **additive** to the session's base permissions. A skill cannot grant permissions that are denied at a higher level (project or organization config).

### `triggers` values

| Value | Description |
|-------|-------------|
| `user` | User can invoke with `/skill-name` in the chat |
| `model` | Agent can invoke the skill autonomously when it deems relevant |

Default is both: `[user, model]`. Set `[user]` to prevent autonomous invocation.

---

## Prompt Body

The Markdown content after the frontmatter closing `---`. This is what the agent sees when the skill is invoked.

### Writing effective prompts

- Use imperative/verb-first instructions ("Run the test suite", "Check for errors")
- State prerequisites clearly (required env vars, tools, services)
- Provide exact commands the agent should run
- Describe how to handle errors and edge cases
- Include examples of expected output when helpful

### Dynamic content

Three substitution mechanisms are available in the prompt body:

#### 1. User arguments

When a user invokes `/my-skill arg1 arg2`, the arguments are available as:

| Variable | Value |
|----------|-------|
| `$1` | First positional argument (`arg1`) |
| `$2` | Second positional argument (`arg2`) |
| `$ARGUMENTS` | All arguments as a single string (`arg1 arg2`) |

Example:
```markdown
Explain the code in $1 in detail.

Full user input: $ARGUMENTS
```

#### 2. File inclusion

Include the contents of a file using `@` syntax. Paths are **relative to the config directory** (e.g., `.windsurf/`, `.cognition/`, or `~/.config/cognition/`), not relative to the skill directory.

```markdown
Check the code against our style guide:

@style-guide.md

Apply these rules to the current file.
```

To include a file from within the skill's own directory, use the `references/` subdirectory convention and reference from the config root:
```markdown
@skills/my-skill/references/guide.md
```

#### 3. Command output

Execute a shell command at invocation time and inject its stdout:

```markdown
Review these staged changes:

!`git diff --staged`

Provide feedback on code quality.
```

The command runs once when the skill is invoked. Its output is included verbatim in the prompt.

---

## Complete Examples

### Minimal skill (no frontmatter)

```markdown
Search the codebase for the given term and summarize what you find.

$ARGUMENTS
```

### Skill with all frontmatter fields

```yaml
---
name: deploy
description: Run the deployment checklist
argument-hint: "[environment]"
model: sonnet
allowed-tools:
  - read
  - exec
  - grep
permissions:
  allow:
    - Exec(npm run)
    - Exec(git)
  deny:
    - Write(/etc/**)
triggers:
  - user
---

Run the deployment checklist for the $1 environment:

1. Run tests: `npm run test`
2. Run linter: `npm run lint`
3. Check git status: `git status`
4. Build: `npm run build`
5. Show current branch and last commit

Report the status of each step. If anything fails, stop and explain the issue.
```

### Skill with a supporting script

```yaml
---
name: send-email
description: Send an email to someone using the Resend API
argument-hint: "[recipient] [subject]"
allowed-tools:
  - exec
  - read
permissions:
  allow:
    - Exec(uv run)
triggers:
  - user
  - model
---

# Send Email

Send an email using the Resend API via a self-contained Python script.

## Prerequisites

The `RESEND_API_KEY` environment variable must be set.

## Usage

uv run send-email/scripts/send_email.py --to "recipient@example.com" --subject "Subject" --body "Body"

## Instructions

Parse the user's request to extract recipient, subject, and body.
Then run the script with the appropriate arguments.

User arguments: $ARGUMENTS
```
