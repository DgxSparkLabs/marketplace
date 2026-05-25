#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
event_name_mapping.py — shared Claude→{Cursor, Gemini, Windsurf} hook
event-name translation tables.

Why this exists
---------------
Three platforms (Cursor, Gemini, Windsurf) all consume Claude-shape
hooks.json content but each uses a *different* event-name vocabulary:

    Claude            Cursor              Gemini         Windsurf
    UserPromptSubmit  beforeSubmitPrompt  BeforeModel    pre_user_prompt
    PreToolUse        preToolUse          BeforeTool     (split into 4 sub-events)
    PostToolUse       postToolUse         AfterTool      (split into 4 sub-events)
    Stop              stop                —              —
    SessionStart      sessionStart        SessionStart   —
    SessionEnd        sessionEnd          SessionEnd     —
    Notification      —                   Notification   —
    PreCompact        preCompact          PreCompress    —
    SubagentStop      subagentStop        —              —

Per D-16 the canonical hook source format stays Claude-shape. Each
converter (``hooks_to_windsurf``, ``hooks_to_cursor``, ``hooks_to_gemini``)
imports its lookup table from this module so the mapping for any given
Claude event lives in exactly one place — adding a new event means
editing one table here, not three converters.

Conservative principle
----------------------
If a Claude event has no clean semantic 1:1 analog on the target
platform we leave it OUT of the table (or set the value to ``None``)
rather than guessing. ``map_event(event, platform)`` returns ``None``
in that case and each converter handles the ``None`` by dropping the
entry. Per the QA round of 2026-05-25
(``docs/research/qa-bug-fixes-2026-05/RESEARCH.md``) the cost of a
*wrong* mapping ("hook never fires, but file looks valid") is much
worse than the cost of a *missing* mapping ("hook missing on
platform X — surfaced as a gap in TEST_YOURSELF.md").

Sources (all fetched 2026-05-25):
  - Cursor:   cursor.com/docs/agent/hooks
  - Gemini:   geminicli.com/docs/hooks/reference/ + working-extension
              probe (logs/hooklog-hooks.json)
  - Windsurf: docs.windsurf.com/windsurf/cascade/hooks
"""

from __future__ import annotations

__all__ = [
    "CLAUDE_TO_CURSOR_EVENTS",
    "CLAUDE_TO_GEMINI_EVENTS",
    "CLAUDE_TO_WINDSURF_EVENTS",
    "CURSOR_EVENTS",
    "GEMINI_EVENTS",
    "WINDSURF_EVENTS",
    "map_event",
]


# ─── per-platform documented event vocabularies ──────────────────────────────

# Cursor — flat camelCase per cursor.com/docs/agent/hooks (2026-05-25).
CURSOR_EVENTS: frozenset[str] = frozenset({
    "sessionStart",
    "sessionEnd",
    "preToolUse",
    "postToolUse",
    "postToolUseFailure",
    "subagentStart",
    "subagentStop",
    "beforeShellExecution",
    "afterShellExecution",
    "beforeMCPExecution",
    "afterMCPExecution",
    "beforeReadFile",
    "afterFileEdit",
    "beforeSubmitPrompt",
    "preCompact",
    "stop",
    "afterAgentResponse",
    "afterAgentThought",
    "beforeTabFileRead",
    "afterTabFileEdit",
    "workspaceOpen",
})

# Gemini — PascalCase per geminicli.com/docs/hooks/reference/ +
# working hooklog extension (logs/hooklog-hooks.json), 2026-05-25.
GEMINI_EVENTS: frozenset[str] = frozenset({
    "SessionStart",
    "SessionEnd",
    "BeforeModel",
    "AfterModel",
    "BeforeAgent",
    "AfterAgent",
    "BeforeTool",
    "AfterTool",
    "BeforeToolSelection",
    "PreCompress",
    "Notification",
})

# Windsurf — snake_case per docs.windsurf.com/windsurf/cascade/hooks
# (2026-05-25). 12 events; the four "tool" sub-events disambiguate
# Claude's PreToolUse/PostToolUse (read_code/write_code/run_command/
# mcp_tool_use), so we don't map PreToolUse/PostToolUse directly.
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


# ─── Claude → platform mappings ──────────────────────────────────────────────

# Claude → Cursor. Per docs/research/qa-bug-fixes-2026-05/RESEARCH.md
# "Empirical verification round 2026-05-25" Q1.
CLAUDE_TO_CURSOR_EVENTS: dict[str, str] = {
    "UserPromptSubmit": "beforeSubmitPrompt",
    "PreToolUse":       "preToolUse",
    "PostToolUse":      "postToolUse",
    "Stop":             "stop",
    "SessionStart":     "sessionStart",
    "SessionEnd":       "sessionEnd",
    "SubagentStop":     "subagentStop",
    "PreCompact":       "preCompact",
    # Claude "Notification" has no clean Cursor analog; drop on conversion.
}

# Claude → Gemini. Per docs/research/qa-bug-fixes-2026-05/RESEARCH.md Q2.
# UserPromptSubmit maps to BeforeModel — Gemini fires BeforeModel before
# each model call which encompasses the prompt-submit moment.
CLAUDE_TO_GEMINI_EVENTS: dict[str, str] = {
    "UserPromptSubmit": "BeforeModel",
    "PreToolUse":       "BeforeTool",
    "PostToolUse":      "AfterTool",
    "SessionStart":     "SessionStart",
    "SessionEnd":       "SessionEnd",
    "Notification":     "Notification",
    "PreCompact":       "PreCompress",
    # Claude "Stop" / "SubagentStop" have no Gemini analog; drop on conversion.
}

# Claude → Windsurf. Per docs/research/qa-bug-fixes-2026-05/RESEARCH.md
# sanity-check #5. Windsurf splits "tool" into four sub-events so we cannot
# safely map Claude's generic PreToolUse/PostToolUse without losing info;
# drop those rather than guess. When a Claude hook author wants Windsurf
# coverage for tool events they should declare per-event entries in the
# source hooks.json (mirroring the Windsurf shape) and the table can be
# expanded.
CLAUDE_TO_WINDSURF_EVENTS: dict[str, str] = {
    "UserPromptSubmit": "pre_user_prompt",
    # Claude "Stop" / "SessionStart" / "SessionEnd" / "Notification" /
    # "PreCompact" have no Windsurf analog; drop on conversion.
}


_TABLES: dict[str, dict[str, str]] = {
    "cursor":   CLAUDE_TO_CURSOR_EVENTS,
    "gemini":   CLAUDE_TO_GEMINI_EVENTS,
    "windsurf": CLAUDE_TO_WINDSURF_EVENTS,
}


def map_event(event: str, platform: str) -> str | None:
    """Return the mapped event name for ``platform``, or ``None`` if the
    Claude event has no analog on the target.

    ``platform`` must be one of ``"cursor"``, ``"gemini"``, ``"windsurf"``.
    ``None`` means "drop this entry"; callers must handle it.
    """
    try:
        table = _TABLES[platform]
    except KeyError as exc:
        raise ValueError(
            f"unknown platform {platform!r}; expected one of {sorted(_TABLES)}"
        ) from exc
    return table.get(event)
