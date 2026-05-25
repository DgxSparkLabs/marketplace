#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
hooks_to_windsurf.py — convert Claude-style hooks.json to Windsurf
Cascade hooks shape per docs.windsurf.com/windsurf/cascade/hooks
(fetched 2026-05-25).

Per D-16 the canonical hook source format stays Claude-shape (one
source of truth, used directly by Claude). Windsurf's parser uses
different event names AND a flatter per-entry shape. The mismatch
caused our .windsurf/hooks.json entries to load but never fire
(docs/research/qa-bug-fixes-2026-05/RESEARCH.md sanity-check #5,
QA 2026-05-25). We convert at emit time.

Input format (Claude — see hooks/example/hooks/hooks.json):

    {
      "description": "...",
      "hooks": {
        "UserPromptSubmit": [
          {
            "hooks": [
              {"type": "command", "command": "..."}
            ]
          }
        ]
      }
    }

Output format (Windsurf — flat shape, snake_case event names):

    {
      "hooks": {
        "pre_user_prompt": [
          {"command": "..."}
        ]
      }
    }

Event-name mapping (Claude → Windsurf):
    UserPromptSubmit → pre_user_prompt

Claude events without a clean Windsurf 1:1 equivalent are dropped on
conversion with a noted reason (the canonical Claude source remains
intact for Claude/other platforms). Adding more mappings here is the
right place to evolve coverage as Windsurf adds events.
"""

from __future__ import annotations

import json

__all__ = [
    "claude_hooks_to_windsurf_hooks",
    "CLAUDE_TO_WINDSURF_EVENTS",
]

# Per docs.windsurf.com/windsurf/cascade/hooks (2026-05-25): 12 supported
# Windsurf events.
WINDSURF_EVENTS: frozenset[str] = frozenset({
    "pre_read_code",
    "post_read_code",
    "pre_write_code",
    "post_write_code",
    "pre_run_command",
    "post_run_command",
    "pre_mcp_tool_use",
    "post_mcp_tool_use",
    "pre_user_prompt",
    "post_cascade_response",
    "post_cascade_response_with_transcript",
    "post_setup_worktree",
})

# Claude → Windsurf event-name mapping.
#
# Only entries with a clean semantic 1:1 match are listed. Claude events
# without a Windsurf analog (Stop, SubagentStop, SessionStart, SessionEnd,
# Notification, PreCompact) are dropped on conversion. PreToolUse and
# PostToolUse are not mapped because Windsurf splits "tool" into four
# sub-events (read_code, write_code, run_command, mcp_tool_use); our
# Claude source does not disambiguate which sub-event applies, so we
# would emit incorrect events. When a Claude hook author wants Windsurf
# coverage for tool events they should declare per-event entries in the
# source hooks.json (mirroring the Windsurf shape) and the table can be
# expanded.
CLAUDE_TO_WINDSURF_EVENTS: dict[str, str] = {
    "UserPromptSubmit": "pre_user_prompt",
}

# Pass-through field names from Claude inner-hook entries to Windsurf
# entries. ``type`` is dropped on conversion (Windsurf inferred type
# from presence of ``command``/``powershell``).
_PASSTHROUGH_FIELDS = (
    "command",
    "powershell",
    "show_output",
    "working_directory",
)


def _convert_inner_entry(entry: dict) -> dict | None:
    """Convert one Claude inner-hook dict ({"type": "command", "command": ...})
    to one Windsurf hook entry ({"command": ...}). Returns None if the entry
    has no executable field (command or powershell)."""
    out: dict = {}
    for key in _PASSTHROUGH_FIELDS:
        if key in entry:
            out[key] = entry[key]
    if "command" not in out and "powershell" not in out:
        return None
    return out


def claude_hooks_to_windsurf_hooks(text: str) -> str:
    """Convert one Claude hooks.json string to Windsurf hooks.json string.

    - Renames event keys per CLAUDE_TO_WINDSURF_EVENTS (drops unmapped events).
    - Flattens the doubly-nested ``hooks.<event>[].hooks[]`` structure into
      Windsurf's single-level ``hooks.<event>[]`` shape.
    - Drops the ``description`` and other top-level fields not in Windsurf's
      documented schema.
    """
    data = json.loads(text)
    src_hooks = data.get("hooks", {}) or {}

    out_hooks: dict[str, list[dict]] = {}
    for claude_event, entries in src_hooks.items():
        ws_event = CLAUDE_TO_WINDSURF_EVENTS.get(claude_event)
        if ws_event is None:
            # No Windsurf analog (or ambiguous); skip with no surprise.
            continue
        ws_entries: list[dict] = out_hooks.setdefault(ws_event, [])
        for outer in entries or []:
            inner_list = outer.get("hooks") or []
            for inner in inner_list:
                conv = _convert_inner_entry(inner)
                if conv is not None:
                    ws_entries.append(conv)
            # Clean up empty event keys that ended up with no entries
            # (e.g. a Claude entry that had only unknown inner fields).
            if not ws_entries:
                out_hooks.pop(ws_event, None)

    return json.dumps({"hooks": out_hooks}, indent=2) + "\n"
