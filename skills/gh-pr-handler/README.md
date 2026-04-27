# GitHub PR Handler

A comprehensive skill for working with GitHub pull requests using the `gh` CLI.

## What it does

This skill teaches agents how to correctly use the GitHub CLI (`gh`) to:
- Read PR data (comments, reviews, status checks, files changed)
- Create and update PRs
- Manage reviews (approve, request changes, comment)
- Check CI status
- View diffs
- Handle both github.com and enterprise GitHub instances

## Key features

- **Auto-detection**: Teaches when to use high-level commands (which auto-detect GitHub instance) vs. low-level API calls
- **Enterprise GitHub support**: Covers proper hostname handling for enterprise instances
- **Common pitfalls**: Explicitly addresses mistakes like using wrong repo paths or forgetting `--hostname` flags
- **Inline review comments**: Shows the correct way to retrieve inline review comments (which aren't in `gh pr view --json reviews`)

## When to use

Use this skill whenever you need to interact with GitHub PRs via the command line, especially when:
- Working with enterprise GitHub instances
- Retrieving inline review comments
- Checking CI status programmatically
- Creating PRs with specific formatting
- Troubleshooting `gh` CLI commands that aren't working

## Installation

```bash
ln -s ~/sandbox/marketplace/skills/gh-pr-handler ~/.config/devin/skills/gh-pr-handler
```
