# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Bootstrap project documentation structure: AGENTS.md, HANDOFF.md, CHANGELOG.md, PITFALLS.md."""

import argparse
import os
import sys
from datetime import datetime, timezone


AGENTS_TEMPLATE = """\
# {name} — Agent Rules

Project-specific conventions. Global rules are inherited from `~/.config/devin/AGENTS.md`.

---

## Build & Test

<!-- Fill in after setting up the project -->

- **Build:** `TODO`
- **Test:** `TODO`
- **Lint:** `TODO`

---

## Conventions

<!-- Add project-specific patterns, naming conventions, architecture notes -->

"""

HANDOFF_TEMPLATE = """\
# {name} — Handoff

> Current state of the project. Updated in-place after every commit that changes behavior.

## Status

Project bootstrapped on {date}.

## How to Build

TODO

## How to Test

TODO

## What Works

TODO

## What's Next

TODO

## Known Issues

None yet.
"""

CHANGELOG_TEMPLATE = """\
# {name} — Changelog

## {date} — Project bootstrapped

Initial documentation structure created: AGENTS.md, HANDOFF.md, CHANGELOG.md, PITFALLS.md.
"""

PITFALLS_TEMPLATE = """\
# {name} — Pitfalls

Known issues, bugs encountered, and lessons learned. Each entry has:
- **Symptom:** what you observed
- **Cause:** root cause
- **Fix:** what resolved it
- **Commit:** reference (if applicable)

---

<!-- Add entries below as you encounter issues -->
"""


def main():
    parser = argparse.ArgumentParser(description="Bootstrap project documentation structure")
    parser.add_argument("--name", help="Project name (default: directory name)")
    parser.add_argument("--dir", default=".", help="Target directory (default: cwd)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be created")
    args = parser.parse_args()

    target_dir = os.path.abspath(args.dir)
    if not os.path.isdir(target_dir):
        print(f"Error: directory does not exist: {target_dir}", file=sys.stderr)
        sys.exit(1)

    name = args.name or os.path.basename(target_dir)
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    files = {
        "AGENTS.md": AGENTS_TEMPLATE.format(name=name),
        "HANDOFF.md": HANDOFF_TEMPLATE.format(name=name, date=date),
        "CHANGELOG.md": CHANGELOG_TEMPLATE.format(name=name, date=date),
        "PITFALLS.md": PITFALLS_TEMPLATE.format(name=name),
    }

    created = []
    skipped = []

    for filename, content in files.items():
        path = os.path.join(target_dir, filename)
        if os.path.exists(path) and not args.force:
            skipped.append(filename)
            continue
        if args.dry_run:
            created.append(filename)
            continue
        with open(path, "w") as f:
            f.write(content)
        created.append(filename)

    action = "Would create" if args.dry_run else "Created"
    if created:
        print(f"{action}: {', '.join(created)}")
    if skipped:
        print(f"Skipped (already exist): {', '.join(skipped)}")
    if not created and not skipped:
        print("Nothing to do.")


if __name__ == "__main__":
    main()
