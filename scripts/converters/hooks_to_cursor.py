#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
hooks_to_cursor.py — convert Claude-style hooks.json to Cursor's flat
hooks schema per cursor.com/docs/agent/hooks (fetched 2026-05-25).

Per D-16 the canonical hook source format stays Claude-shape (one
source of truth, used directly by Claude). Cursor's hook parser uses:
  - a top-level ``version`` key (REQUIRED — empirically the file is
    silently ignored without it; verified by inspecting Cursor's own
    plugins ``continual-learning`` and ``ralph-loop`` —
    docs/research/qa-bug-fixes-2026-05/logs/cl-hooks.json + ralph-hooks.json)
  - camelCase event names (``beforeSubmitPrompt``, ``stop``,
    ``preToolUse``, ...) — see CLAUDE_TO_CURSOR_EVENTS in
    converters.event_name_mapping
  - a flat per-entry shape ``{command, matcher?, timeout?, loop_limit?}``
    rather than Claude's doubly-nested
    ``hooks.<event>[].hooks[].command``

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

Output format (Cursor — flat shape, camelCase events, version-tagged):

    {
      "version": 1,
      "hooks": {
        "beforeSubmitPrompt": [
          {"command": "..."}
        ]
      }
    }

Claude events without a clean Cursor analog are dropped on conversion
(the canonical Claude source remains intact for Claude). The mapping
table lives in converters.event_name_mapping.CLAUDE_TO_CURSOR_EVENTS
so all platforms' tables stay in one place.
"""

from __future__ import annotations

import json

from converters.event_name_mapping import CLAUDE_TO_CURSOR_EVENTS, CURSOR_EVENTS

__all__ = [
    "claude_hooks_to_cursor_hooks",
    "CLAUDE_TO_CURSOR_EVENTS",
    "CURSOR_EVENTS",
]


# Top-level Cursor hooks-file schema version. Per cursor.com/docs/agent/hooks
# (2026-05-25), every working community example sets ``"version": 1``.
_CURSOR_HOOKS_VERSION = 1

# Per-entry pass-through fields. ``type`` is dropped (Cursor's parser
# does not document a ``type`` key; the presence of ``command`` is
# sufficient). ``matcher``, ``timeout``, ``loop_limit``, ``failClosed``
# are documented optional fields per the same doc.
_PASSTHROUGH_FIELDS = (
    "command",
    "matcher",
    "timeout",
    "loop_limit",
    "failClosed",
)


def _convert_inner_entry(entry: dict) -> dict | None:
    """Convert one Claude inner-hook dict to one Cursor hook entry.

    Returns None if the entry has no ``command`` field (Cursor requires
    at least a command — there's no PowerShell or shell-only alternative
    documented).
    """
    out: dict = {}
    for key in _PASSTHROUGH_FIELDS:
        if key in entry:
            out[key] = entry[key]
    if "command" not in out:
        return None
    return out


def claude_hooks_to_cursor_hooks(text: str) -> str:
    """Convert one Claude hooks.json string to Cursor hooks.json string.

    - Adds top-level ``"version": 1`` (REQUIRED by Cursor's parser).
    - Renames event keys per CLAUDE_TO_CURSOR_EVENTS (drops unmapped events).
    - Flattens the doubly-nested ``hooks.<event>[].hooks[]`` structure into
      Cursor's single-level ``hooks.<event>[]`` shape.
    - Drops the ``description`` and other top-level fields not in Cursor's
      documented schema.
    """
    data = json.loads(text)
    src_hooks = data.get("hooks", {}) or {}

    out_hooks: dict[str, list[dict]] = {}
    for claude_event, entries in src_hooks.items():
        cursor_event = CLAUDE_TO_CURSOR_EVENTS.get(claude_event)
        if cursor_event is None:
            # No Cursor analog (or ambiguous); skip with no surprise.
            continue
        cursor_entries: list[dict] = []
        for outer in entries or []:
            inner_list = outer.get("hooks") or []
            for inner in inner_list:
                conv = _convert_inner_entry(inner)
                if conv is not None:
                    cursor_entries.append(conv)
        if cursor_entries:
            out_hooks[cursor_event] = cursor_entries

    return json.dumps(
        {"version": _CURSOR_HOOKS_VERSION, "hooks": out_hooks},
        indent=2,
    ) + "\n"
