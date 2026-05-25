#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
md_to_gemini_md.py — convert Claude-style agent markdown (YAML frontmatter
+ body) to Gemini sub-agent markdown shape per
geminicli.com/docs/core/subagents/ (2026-05-25).

Per D-16 the canonical agent source format stays Claude-style markdown
(one source of truth, used directly by Claude / Cursor). Gemini's
sub-agent loader requires the ``tools`` frontmatter as a YAML *array*
rather than the Claude-style comma-separated scalar. The mismatch
caused ``/agents`` discovery to silently skip our notebook-reviewer
sub-agent (QA 2026-05-25, docs/research/qa-bug-fixes-2026-05/RESEARCH.md
Bug 2). We convert at emit time rather than maintaining a parallel
source tree.

Input format (Claude/Cursor canonical):

    ---
    name: notebook-reviewer
    description: Reviews a lab notebook entry...
    tools: Read, Grep, Glob
    ---

    You are a peer reviewer for laboratory notebook entries...

Output format (Gemini sub-agent):

    ---
    name: notebook-reviewer
    description: Reviews a lab notebook entry...
    tools:
      - Read
      - Grep
      - Glob
    ---

    You are a peer reviewer for laboratory notebook entries...

Required Gemini frontmatter fields per the docs: name, description.
Optional pass-throughs: tools (array), model, kind, temperature,
max_turns, timeout_mins.

No third-party deps (the repo convention — see scripts/utils.py:22).
Re-uses the same simple-scalar frontmatter parser as md_to_toml.
"""

from __future__ import annotations

__all__ = ["claude_agent_md_to_gemini_md"]

# Pass-through optional frontmatter fields documented at
# geminicli.com/docs/core/subagents/ (2026-05-25). Anything else is
# dropped on conversion (the canonical Claude source remains intact).
_PASSTHROUGH_KEYS = ("model", "kind", "temperature", "max_turns", "timeout_mins")


def _parse_frontmatter_and_body(text: str) -> tuple[dict, str]:
    """Split a markdown doc with YAML frontmatter into (frontmatter_dict, body_str).

    Mirrors the same simple-scalar parsing semantics as utils._frontmatter
    and md_to_toml._parse_frontmatter_and_body (no list/nested-object
    support — sufficient for our agent frontmatter). Raises ValueError if
    frontmatter is malformed.
    """
    if not text.startswith("---\n"):
        raise ValueError("Agent markdown must start with '---' YAML frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("Agent markdown frontmatter missing closing '---'")
    fm_text = text[4:end]
    body = text[end + len("\n---"):].lstrip("\n")
    fm: dict = {}
    for raw in fm_text.splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        if ":" not in raw:
            continue
        key, _, val = raw.partition(":")
        fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm, body


def claude_agent_md_to_gemini_md(text: str) -> str:
    """Convert one Claude-style agent .md to Gemini sub-agent .md.

    Required Gemini fields per geminicli.com/docs/core/subagents/:
        - name         (slug — lowercase, numbers, hyphens, underscores)
        - description  (visible to main agent for routing)

    Optional fields (passed through when present in frontmatter):
        - tools (comma-separated string in source; emitted as YAML array)
        - model, kind, temperature, max_turns, timeout_mins (verbatim scalars)

    Raises ValueError if a required frontmatter field is missing.
    """
    fm, body = _parse_frontmatter_and_body(text)

    if "name" not in fm:
        raise ValueError("Agent frontmatter missing required 'name' field")
    if "description" not in fm:
        raise ValueError("Agent frontmatter missing required 'description' field")

    lines: list[str] = ["---", f"name: {fm['name']}", f"description: {fm['description']}"]

    if fm.get("tools"):
        tools = [t.strip() for t in fm["tools"].split(",") if t.strip()]
        if tools:
            lines.append("tools:")
            for t in tools:
                lines.append(f"  - {t}")

    for key in _PASSTHROUGH_KEYS:
        if fm.get(key):
            lines.append(f"{key}: {fm[key]}")

    lines.append("---")
    lines.append("")
    lines.append(body)
    # Use LF endings + trailing newline so write_text(..., newline="") on
    # Windows produces the same bytes as on Linux/macOS.
    return "\n".join(lines)
