#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
hooks_to_gemini.py — convert Claude-style hooks.json to Gemini-CLI's
hooks shape per geminicli.com/docs/hooks/reference/ (fetched 2026-05-25).

Per D-16 the canonical hook source format stays Claude-shape (one
source of truth, used directly by Claude). The Gemini-CLI hooks
schema is **structurally identical** to Claude's
(``{event: [{matcher, hooks: [{type, command}]}]}``) — only the
event-name vocabulary differs. Empirical verification round
2026-05-25 confirmed this against the ``sandipchitale/hooklog``
working Gemini extension (logs/hooklog-hooks.json).

So this converter is much simpler than ``hooks_to_cursor`` /
``hooks_to_windsurf``: it ONLY renames event keys; the nested
``{event: [{matcher, hooks: [{type, command}]}]}`` shape is kept
verbatim.

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

Output format (Gemini — same nested shape, PascalCase from Gemini's
vocabulary):

    {
      "description": "...",
      "hooks": {
        "BeforeModel": [
          {
            "hooks": [
              {"type": "command", "command": "..."}
            ]
          }
        ]
      }
    }

Claude events without a clean Gemini analog (Stop, SubagentStop) are
dropped on conversion. The mapping table lives in
converters.event_name_mapping.CLAUDE_TO_GEMINI_EVENTS so all
platforms' tables stay in one place.

Gemini's gemini-extension.json does NOT declare a hooks pointer —
discovery is by directory convention (``hooks/hooks.json`` inside
the extension root). Our extension root is ``.gemini/`` so the
emitted file lands at ``.gemini/hooks/hooks.json``; no manifest
update needed.
"""

from __future__ import annotations

import json

from converters.event_name_mapping import CLAUDE_TO_GEMINI_EVENTS, GEMINI_EVENTS

__all__ = [
    "claude_hooks_to_gemini_hooks",
    "CLAUDE_TO_GEMINI_EVENTS",
    "GEMINI_EVENTS",
]


def claude_hooks_to_gemini_hooks(text: str) -> str:
    """Convert one Claude hooks.json string to Gemini hooks.json string.

    - Renames event keys per CLAUDE_TO_GEMINI_EVENTS (drops unmapped events).
    - Keeps the nested ``hooks.<event>[].hooks[]`` shape unchanged
      (Gemini matches Claude's structural shape — only vocabulary differs).
    - Preserves the optional top-level ``description`` field (the
      working hooklog extension includes one).
    """
    data = json.loads(text)
    src_hooks = data.get("hooks", {}) or {}

    out_hooks: dict[str, list[dict]] = {}
    for claude_event, entries in src_hooks.items():
        gemini_event = CLAUDE_TO_GEMINI_EVENTS.get(claude_event)
        if gemini_event is None:
            # No Gemini analog (or ambiguous); skip with no surprise.
            continue
        # Pass entries through verbatim — same nested shape.
        out_hooks[gemini_event] = list(entries or [])

    out: dict = {}
    if "description" in data:
        out["description"] = data["description"]
    out["hooks"] = out_hooks

    return json.dumps(out, indent=2) + "\n"
