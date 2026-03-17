# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Generate structured task files for autonomous agent sessions."""

import argparse
import os
from pathlib import Path


RULES_TEMPLATE = """\
# Rules

Coding conventions and architectural patterns for this work.

## Code Style

- <!-- e.g., Use 4-space indentation, max line length 100 -->

## Architecture Patterns

- <!-- e.g., Use factory patterns for object creation -->
- <!-- e.g., Prefer dependency injection over global state -->

## File Conventions

- <!-- e.g., Max file size: 300 lines -->
- <!-- e.g., One class per file -->

## Testing Requirements

- <!-- e.g., All new functions must have unit tests -->
- <!-- e.g., Minimum 80% coverage on changed files -->
"""

SCOPE_TEMPLATE = """\
# Scope

High-level overview of what we're trying to accomplish.

## Objective

{task}

## Context

<!-- Background information, motivation, and relevant history -->

## Success Criteria

- <!-- What does "done" look like? -->

## Constraints

- <!-- Time, technology, compatibility, or other constraints -->
"""

RESEARCH_TEMPLATE = """\
# Research

References and resources for this work.

## Files Involved

<!-- List all files that will be read or modified -->

| File | Purpose |
|------|---------|
| <!-- path/to/file --> | <!-- why it's relevant --> |

## Dependencies

<!-- Libraries, services, or internal modules this work depends on -->

## External References

<!-- Links to docs, issues, PRs, design docs, etc. -->
"""

TASK_TEMPLATE = """\
# Task {number:02d}: {title}

## Description

<!-- What needs to be done in this task -->

## Files to Modify

- <!-- path/to/file -->

## Acceptance Criteria

- [ ] <!-- Criterion 1 -->
- [ ] <!-- Criterion 2 -->

## Dependencies on Other Tasks

- <!-- e.g., Requires task-00 to be completed first, or "None" -->
"""


def create_structure(task: str, output_dir: str, num_tasks: int) -> None:
    base = Path(output_dir)
    tasks_dir = base / "tasks"

    os.makedirs(tasks_dir, exist_ok=True)

    # rules.md
    rules_path = base / "rules.md"
    rules_path.write_text(RULES_TEMPLATE)

    # scope.md
    scope_path = base / "scope.md"
    scope_path.write_text(SCOPE_TEMPLATE.format(task=task))

    # research.md
    research_path = base / "research.md"
    research_path.write_text(RESEARCH_TEMPLATE)

    # task files
    for i in range(num_tasks):
        task_path = tasks_dir / f"task-{i:02d}.md"
        task_path.write_text(TASK_TEMPLATE.format(number=i, title="TODO"))

    # Print summary
    print(f"Created handoff structure in {base}/")
    print()
    print("  Files:")
    print(f"    {rules_path}")
    print(f"    {scope_path}")
    print(f"    {research_path}")
    for i in range(num_tasks):
        print(f"    {tasks_dir / f'task-{i:02d}.md'}")
    print()
    print(f"  Total: {3 + num_tasks} files")
    print()
    print("Next steps:")
    print("  1. Fill in rules.md with your coding conventions")
    print("  2. Expand scope.md with context and success criteria")
    print("  3. Populate research.md with relevant file paths")
    print("  4. Detail each task file with descriptions and acceptance criteria")


def main():
    parser = argparse.ArgumentParser(
        description="Generate structured task files for autonomous agent sessions"
    )
    parser.add_argument(
        "--task",
        required=True,
        help="Description of what needs to be done",
    )
    parser.add_argument(
        "--dir",
        default=".tasks",
        help="Output directory (default: .tasks)",
    )
    parser.add_argument(
        "--num-tasks",
        type=int,
        default=5,
        help="Number of task files to generate (default: 5)",
    )
    args = parser.parse_args()

    if args.num_tasks < 1:
        parser.error("--num-tasks must be at least 1")

    create_structure(task=args.task, output_dir=args.dir, num_tasks=args.num_tasks)


if __name__ == "__main__":
    main()
