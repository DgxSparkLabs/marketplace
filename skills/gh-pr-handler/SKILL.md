---
name: gh-pr-handler
description: |
  Comprehensive guide for working with GitHub pull requests using the gh CLI. Use this skill whenever you need to interact with PRs - reading PR data (comments, reviews, status checks, files changed), creating or updating PRs, managing reviews (approving, requesting changes, commenting), checking CI status, viewing diffs, or any other PR-related operations. Also use when you see GitHub URLs, PR numbers, need to handle enterprise GitHub instances (like eos2git.cec.lab.emc.com), or when troubleshooting gh CLI commands that aren't working as expected. This skill covers both github.com and enterprise GitHub instances and teaches the correct patterns to avoid common mistakes like using wrong repository paths or forgetting hostname flags.
---

# GitHub PR Handler

This skill teaches you how to correctly use the `gh` CLI to work with GitHub pull requests across both github.com and enterprise GitHub instances.

## Core Principles

### 1. Auto-Detection vs. Explicit Specification

The `gh` CLI has two modes of operation:

**High-level commands** (`gh pr view`, `gh pr create`, etc.) automatically detect the GitHub instance from your git remotes when you're in a repository directory. Use these whenever possible - they're simpler and less error-prone.

**Low-level API commands** (`gh api`) default to github.com unless you explicitly specify `--hostname`. Use these only when the high-level commands don't expose the data you need.

### 2. Repository Context

When you're in a git repository directory, `gh` automatically knows:
- Which GitHub instance to use (github.com vs. enterprise)
- The repository owner and name
- The current branch

When you're NOT in a repo directory, or need to work with a different repo, use `-R OWNER/REPO` or `--repo [HOST/]OWNER/REPO`.

### 3. Getting the Correct Repository Path

Never guess the repository owner and name. Always verify:

```bash
# Get the correct owner/repo path
gh repo view --json nameWithOwner,url
```

This returns:
```json
{
  "nameWithOwner": "vxflexos/agentic_root_cause_analyzer",
  "url": "https://eos2git.cec.lab.emc.com/vxflexos/agentic_root_cause_analyzer"
}
```

Use `nameWithOwner` for API calls and the hostname from `url` for `--hostname` flags.

## Common Operations

### Reading PR Data

#### View PR Overview

```bash
# View current branch's PR
gh pr view

# View specific PR (auto-detects host from git remote)
gh pr view 243

# Get JSON output with specific fields
gh pr view 243 --json title,number,state,author,reviews,statusCheckRollup

# View PR from a different repo
gh pr view 243 --repo owner/repo
```

Available JSON fields: `additions`, `assignees`, `author`, `autoMergeRequest`, `baseRefName`, `baseRefOid`, `body`, `changedFiles`, `closed`, `closedAt`, `closingIssuesReferences`, `comments`, `commits`, `createdAt`, `deletions`, `files`, `fullDatabaseId`, `headRefName`, `headRefOid`, `headRepository`, `headRepositoryOwner`, `id`, `isCrossRepository`, `isDraft`, `labels`, `latestReviews`, `maintainerCanModify`, `mergeCommit`, `mergeStateStatus`, `mergeable`, `mergedAt`, `mergedBy`, `milestone`, `number`, `potentialMergeCommit`, `projectCards`, `projectItems`, `reactionGroups`, `reviewDecision`, `reviewRequests`, `reviews`, `state`, `statusCheckRollup`, `title`, `updatedAt`, `url`

#### Get Inline Review Comments

**Important**: Inline review comments are NOT in `gh pr view --json reviews` (the body field is empty for inline comments). You must use the API:

```bash
# First, get the correct repo path and hostname
REPO_INFO=$(gh repo view --json nameWithOwner,url)
OWNER_REPO=$(echo "$REPO_INFO" | jq -r '.nameWithOwner')
HOST=$(echo "$REPO_INFO" | jq -r '.url' | sed 's|https://||' | cut -d'/' -f1)

# Then get inline comments
gh api "repos/$OWNER_REPO/pulls/243/comments" --hostname "$HOST" \
  --jq '.[] | select(.user.login == "reviewer-name") | {path, line, body}'
```

For github.com, you can omit `--hostname`:
```bash
gh api repos/owner/repo/pulls/243/comments \
  --jq '.[] | select(.user.login == "reviewer-name") | {path, line, body}'
```

#### Check CI Status

```bash
# View all status checks
gh pr view 243 --json statusCheckRollup

# Filter for failed checks
gh pr view 243 --json statusCheckRollup \
  --jq '.statusCheckRollup[] | select(.conclusion != "SUCCESS") | {name, conclusion, status}'

# Check specific workflow
gh pr checks 243
```

#### View Changed Files

```bash
# List changed files
gh pr view 243 --json files --jq '.files[].path'

# View the diff
gh pr diff 243

# View diff for specific file
gh pr diff 243 -- path/to/file.py
```

#### Get PR Comments (not inline review comments)

```bash
# View all comments
gh pr view 243 --comments

# Get comments as JSON
gh pr view 243 --json comments \
  --jq '.comments[] | {author: .author.login, body, createdAt}'
```

### Creating PRs

#### Basic PR Creation

```bash
# Create PR with title and body
gh pr create --title "feat: add new feature" --body "Description here"

# Create PR using commit messages (autofill)
gh pr create --fill

# Create draft PR
gh pr create --draft --title "WIP: feature" --body "Not ready yet"

# Create PR with multi-line body using heredoc
gh pr create --title "fix: bug fix" --body "$(cat <<'EOF'
## Summary
Fixed the bug

## Test Plan
- Tested locally
- All tests pass
EOF
)"
```

#### PR Creation with Reviewers and Labels

```bash
# Request reviews
gh pr create --title "..." --body "..." \
  --reviewer username1,username2 \
  --reviewer org/team-name

# Add labels
gh pr create --title "..." --body "..." \
  --label bug,priority-high

# Assign to someone
gh pr create --title "..." --body "..." \
  --assignee username
```

#### Target Different Base Branch

```bash
# Create PR targeting specific branch
gh pr create --base develop --title "..." --body "..."

# Create PR from specific head branch
gh pr create --head feature-branch --title "..." --body "..."
```

### Updating PRs

#### Edit PR Metadata

```bash
# Update title
gh pr edit 243 --title "new title"

# Update body
gh pr edit 243 --body "new description"

# Add reviewers
gh pr edit 243 --add-reviewer username

# Add labels
gh pr edit 243 --add-label bug

# Mark as ready for review (convert from draft)
gh pr ready 243
```

#### Add Comments

```bash
# Add a comment to the PR
gh pr comment 243 --body "Thanks for the review!"

# Add comment with multi-line text
gh pr comment 243 --body "$(cat <<'EOF'
Multiple
lines
here
EOF
)"
```

### Reviewing PRs

#### Submit Reviews

```bash
# Approve PR
gh pr review 243 --approve

# Request changes
gh pr review 243 --request-changes --body "Please fix X"

# Leave a comment (not approval or request changes)
gh pr review 243 --comment --body "Looks good overall"
```

**Note**: The `gh pr review` command submits a review at the PR level, not inline comments on specific lines. For inline comments, you need to use the web interface or the API (which is more complex).

### Merging and Closing

#### Merge PR

```bash
# Merge with default strategy
gh pr merge 243

# Merge with specific strategy
gh pr merge 243 --merge      # Create merge commit
gh pr merge 243 --squash     # Squash and merge
gh pr merge 243 --rebase     # Rebase and merge

# Auto-merge when checks pass
gh pr merge 243 --auto --squash

# Delete branch after merge
gh pr merge 243 --delete-branch
```

#### Close Without Merging

```bash
gh pr close 243

# Reopen
gh pr reopen 243
```

### Checking Out PRs Locally

```bash
# Check out a PR branch
gh pr checkout 243

# This creates a local branch and switches to it
# Useful for testing changes locally
```

## Enterprise GitHub Instances

### How Auto-Detection Works

When you're in a repository directory:

1. `gh` reads your git remotes (`.git/config`)
2. Extracts the hostname from the remote URL
3. Uses that hostname for all operations

Example git remote:
```
[remote "origin"]
    url = https://eos2git.cec.lab.emc.com/vxflexos/repo.git
```

`gh` automatically uses `eos2git.cec.lab.emc.com` as the hostname.

### When You Need --hostname

Use `--hostname` only when:
1. Using `gh api` (low-level API calls)
2. Not in a repository directory
3. Working with a different instance than your current repo

```bash
# API call to enterprise instance
gh api repos/owner/repo/pulls/243 --hostname eos2git.cec.lab.emc.com

# High-level command (no --hostname needed if you're in the repo)
gh pr view 243
```

### Authentication

Check your authentication status:

```bash
gh auth status
```

This shows all GitHub instances you're authenticated with:
```
github.com
  ✓ Logged in to github.com account username
  
eos2git.cec.lab.emc.com
  ✓ Logged in to eos2git.cec.lab.emc.com account username
```

If not authenticated, log in:
```bash
# For github.com
gh auth login

# For enterprise instance
gh auth login --hostname eos2git.cec.lab.emc.com
```

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Using Wrong Repository Path

**Wrong**:
```bash
gh api repos/eos2git/jarvis/pulls/243/comments
```

**Why it's wrong**: `eos2git` is the hostname, not the owner. The owner is the organization/user that owns the repo.

**Right**:
```bash
# First get the correct path
gh repo view --json nameWithOwner
# Returns: {"nameWithOwner": "vxflexos/agentic_root_cause_analyzer"}

# Then use it
gh api repos/vxflexos/agentic_root_cause_analyzer/pulls/243/comments --hostname eos2git.cec.lab.emc.com
```

### Pitfall 2: Forgetting --hostname for API Calls

**Wrong**:
```bash
# This goes to github.com, not your enterprise instance
gh api repos/owner/repo/pulls/243/comments
```

**Right**:
```bash
# Extract hostname from repo URL
HOST=$(gh repo view --json url --jq '.url' | sed 's|https://||' | cut -d'/' -f1)

# Use it in API call
gh api repos/owner/repo/pulls/243/comments --hostname "$HOST"
```

**Better**: Use high-level commands when possible - they auto-detect:
```bash
# This automatically uses the correct hostname
gh pr view 243 --json reviews
```

### Pitfall 3: Looking for Inline Comments in Wrong Place

**Wrong**:
```bash
# This returns empty bodies for inline comments
gh pr view 243 --json reviews
```

**Right**:
```bash
# Use the API to get inline review comments
gh api repos/owner/repo/pulls/243/comments --hostname HOST
```

### Pitfall 4: Not Checking Current Directory

If `gh` commands fail with "not found" or "no pull request found":

1. Check if you're in a git repository: `git status`
2. Check which repo you're in: `gh repo view`
3. Either `cd` to the correct repo or use `-R owner/repo`

## Output Formats

### JSON Output

Use `--json` with `--jq` for programmatic parsing:

```bash
# Get specific fields
gh pr view 243 --json title,state,author

# Filter and transform with jq
gh pr view 243 --json statusCheckRollup \
  --jq '.statusCheckRollup[] | select(.conclusion == "FAILURE")'

# Extract nested data
gh pr view 243 --json reviews \
  --jq '.reviews[] | {author: .author.login, state}'
```

### Human-Readable Output

Default output is formatted for humans:

```bash
# Pretty-printed PR view
gh pr view 243

# List PRs in a table
gh pr list

# Show status checks
gh pr checks 243
```

## Workflow Patterns

### Pattern 1: Check PR Before Merging

```bash
# 1. View PR details
gh pr view 243

# 2. Check CI status
gh pr checks 243

# 3. Review changed files
gh pr diff 243

# 4. If all good, merge
gh pr merge 243 --squash --delete-branch
```

### Pattern 2: Address Review Feedback

```bash
# 1. Get review comments
gh api repos/$(gh repo view --json nameWithOwner --jq '.nameWithOwner')/pulls/243/comments \
  --hostname $(gh repo view --json url --jq '.url' | sed 's|https://||' | cut -d'/' -f1) \
  --jq '.[] | {path, line, body}'

# 2. Make changes locally
# ... edit files ...

# 3. Push changes
git add .
git commit -m "fix: address review feedback"
git push

# 4. Add comment to PR
gh pr comment 243 --body "Fixed the issues you mentioned"
```

### Pattern 3: Create PR with Full Context

```bash
# 1. Create PR with detailed description
gh pr create --title "feat(api): add new endpoint" --body "$(cat <<'EOF'
## Summary
Added new /api/users endpoint

## Changes
- Created new UserController
- Added tests
- Updated API docs

## Test Plan
- Unit tests pass
- Integration tests pass
- Manually tested with curl

Fixes #123
EOF
)" --draft

# 2. Request reviews
gh pr edit --add-reviewer teammate1,teammate2

# 3. When ready, mark as ready for review
gh pr ready
```

### Pattern 4: Monitor CI Status

```bash
# Check status periodically
while true; do
  STATUS=$(gh pr view 243 --json statusCheckRollup \
    --jq '[.statusCheckRollup[] | select(.conclusion != "SUCCESS")] | length')
  
  if [ "$STATUS" -eq 0 ]; then
    echo "All checks passed!"
    break
  else
    echo "Waiting for checks... ($STATUS failing)"
    sleep 30
  fi
done
```

## Error Handling

### Common Errors and Solutions

**Error**: `HTTP 404: Not Found`
- **Cause**: Wrong repository path or PR doesn't exist
- **Solution**: Verify with `gh repo view` and `gh pr list`

**Error**: `authentication required`
- **Cause**: Not logged in to the GitHub instance
- **Solution**: Run `gh auth status` and `gh auth login` if needed

**Error**: `pull request not found`
- **Cause**: Not in a repository directory or wrong repo
- **Solution**: `cd` to repo or use `-R owner/repo`

**Error**: `GraphQL: Could not resolve to a PullRequest`
- **Cause**: Using wrong hostname (e.g., github.com instead of enterprise)
- **Solution**: Use `--hostname` for API calls or ensure you're in the correct repo directory

## Quick Reference

### Most Common Commands

```bash
# View PR
gh pr view 243

# Create PR
gh pr create --title "..." --body "..."

# Get inline review comments
gh api repos/OWNER/REPO/pulls/243/comments --hostname HOST

# Check CI status
gh pr view 243 --json statusCheckRollup

# Approve PR
gh pr review 243 --approve

# Merge PR
gh pr merge 243 --squash

# Get repo info (for API calls)
gh repo view --json nameWithOwner,url
```

### When to Use What

| Task | Command Type | Example |
|------|-------------|---------|
| View PR overview | High-level | `gh pr view 243` |
| Get inline comments | API | `gh api repos/OWNER/REPO/pulls/243/comments` |
| Create PR | High-level | `gh pr create` |
| Check CI status | High-level | `gh pr checks 243` |
| Approve/review | High-level | `gh pr review 243 --approve` |
| Get specific JSON fields | High-level with --json | `gh pr view 243 --json statusCheckRollup` |
| Complex API queries | API | `gh api ...` |

## Summary

Remember these key points:

1. **Use high-level commands** (`gh pr view`, `gh pr create`) whenever possible - they auto-detect the GitHub instance
2. **Get the correct repo path** with `gh repo view --json nameWithOwner` before making API calls
3. **Use `--hostname` for API calls** to enterprise instances
4. **Inline review comments** require `gh api repos/OWNER/REPO/pulls/NUMBER/comments`, not `gh pr view --json reviews`
5. **Check your context** - are you in the right repo directory?
6. **Verify authentication** with `gh auth status` if commands fail

The `gh` CLI is powerful and handles most of the complexity for you when you use the right commands. When in doubt, start with high-level commands and only drop to `gh api` when you need data that isn't exposed through the standard commands.
