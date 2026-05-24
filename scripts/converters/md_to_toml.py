#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
md_to_toml.py — convert Claude-style agent markdown (YAML frontmatter + body)
to Codex sub-agent TOML per developers.openai.com/codex/subagents/ (2026-05-25).

Per D-16: the canonical agent source format stays Claude-style markdown with
YAML frontmatter (one source of truth, used directly by Claude / Cursor /
Gemini). Codex sub-agents are TOML files with the same semantic content but
a different shape, so we convert at emit time rather than maintaining a
parallel source tree.

Input format (Claude/Cursor/Gemini canonical, per
agents/example/agents/notebook-reviewer.md):

    ---
    name: notebook-reviewer
    description: Reviews a lab notebook entry...
    tools: Read, Grep, Glob
    ---

    You are a peer reviewer for laboratory notebook entries...

Output format (Codex):

    name = "notebook-reviewer"
    description = "Reviews a lab notebook entry..."
    tools = ["Read", "Grep", "Glob"]
    developer_instructions = '''
    You are a peer reviewer for laboratory notebook entries...
    '''

Required Codex fields per the docs: name, description, developer_instructions.
Optional pass-throughs: tools (list), model (string).

No third-party deps (the repo convention — see scripts/utils.py:22). We
hand-roll a tiny TOML writer scoped to the keys we emit; tomllib (stdlib
3.11+) handles round-trip verification in tests.
"""

from __future__ import annotations

__all__ = ["claude_agent_md_to_codex_toml"]


def _parse_frontmatter_and_body(text: str) -> tuple[dict, str]:
    """Split a markdown doc with YAML frontmatter into (frontmatter_dict, body_str).

    Mirrors the same simple-scalar parsing semantics as utils._frontmatter
    (no list/nested-object support — sufficient for our agent frontmatter).
    Raises ValueError if frontmatter is malformed (missing opening or closing
    '---' delimiter).
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


def _toml_escape_basic_string(s: str) -> str:
    """Escape a TOML basic string (double-quoted, single-line)."""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def _toml_multiline_literal(s: str) -> str:
    """Emit a TOML multi-line literal string (triple-single-quoted).

    Literal strings have no escapes — the only forbidden sequence is ''' itself.
    If the body contains ''' we fall back to a triple-double-quoted basic
    string with the necessary escapes.
    """
    if "'''" not in s:
        # Strip trailing newline so the closing ''' lands on its own line.
        return "'''\n" + s.rstrip("\n") + "\n'''"
    # Fallback: triple-double-quoted basic string with escapes.
    escaped = s.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    return '"""\n' + escaped.rstrip("\n") + '\n"""'


def claude_agent_md_to_codex_toml(text: str) -> str:
    """Convert one Claude-style agent .md (frontmatter + body) to Codex TOML.

    Required Codex fields per developers.openai.com/codex/subagents/:
        - name                       (required)
        - description                (required)
        - developer_instructions     (required; the agent's system prompt = body)

    Optional fields (passed through when present in frontmatter):
        - tools  (comma-separated list in source; emitted as TOML array)
        - model  (string)

    Raises ValueError if a required frontmatter field is missing.
    """
    fm, body = _parse_frontmatter_and_body(text)

    if "name" not in fm:
        raise ValueError("Agent frontmatter missing required 'name' field")
    if "description" not in fm:
        raise ValueError("Agent frontmatter missing required 'description' field")

    lines: list[str] = []
    lines.append(f'name = "{_toml_escape_basic_string(fm["name"])}"')
    lines.append(f'description = "{_toml_escape_basic_string(fm["description"])}"')

    # Optional tools[] from comma-separated string.
    if "tools" in fm and fm["tools"]:
        tools = [t.strip() for t in fm["tools"].split(",") if t.strip()]
        if tools:
            quoted = ", ".join(f'"{_toml_escape_basic_string(t)}"' for t in tools)
            lines.append(f"tools = [{quoted}]")

    # Optional model passthrough.
    if "model" in fm and fm["model"]:
        lines.append(f'model = "{_toml_escape_basic_string(fm["model"])}"')

    # Required: developer_instructions (the body of the markdown file).
    lines.append("developer_instructions = " + _toml_multiline_literal(body))

    return "\n".join(lines) + "\n"
