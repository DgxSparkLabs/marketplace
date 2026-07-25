#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
test_schema_fitness.py — validate per-platform emission against reference schemas.

Why this exists
---------------
Our drift check (``scripts/generate_manifest.py --check``) confirms that
*regenerated* output equals *committed* output byte-for-byte. It does
not confirm either side matches the *platform's actual schema*. The
three QA bugs of 2026-05-25 (Cursor skill popup mangled; Gemini
sub-agent not discovered; Windsurf hooks loaded but never fired) all
passed the drift check because both sides were wrong relative to
Cursor / Gemini / Windsurf's documented loader contracts.

Schema fitness closes the loop:

    drift check       == "is this what we *committed*?"
    schema fitness    == "is this what the *platform* expects?"

Each test parses an emitted file and validates it against a small
reference schema captured here (sourced directly from each platform's
docs, dates noted at the schema definitions). The schemas are
deliberately tight on required-fields and event-name allowlists — the
goal is to catch the same class of bug (a "field-name drift" that the
byte-diff check is blind to) before it ships.

Initial coverage (the three constructs implicated by the 2026-05-25 QA):
    - Cursor SkillConstruct      → .cursor-plugin/plugin.json
    - Gemini AgentConstruct      → .gemini/agents/<n>.md frontmatter
    - Windsurf HookConstruct     → .windsurf/hooks.json
    - Cursor HookConstruct       → .cursor/hooks.json
    - Gemini HookConstruct       → .gemini/hooks/hooks.json

Expand schemas as new per-platform emissions land. Each new emission
category we add (Codex agents, Cursor commands, ...) gets a schema
test added here.

No third-party deps (the repo convention — see scripts/utils.py:22).
A tiny in-file validator (~30 lines) covers the JSON Schema subset we
use: type, required, properties, patternProperties, additionalProperties,
items, enum. If validation needs grow beyond that, swap in jsonschema
via PEP 723 inline metadata.
"""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from constructs import (
    CONSTRUCTS,
    AgentConstruct,
    HookConstruct,
    LSPConstruct,
    MonitorConstruct,
    SkillConstruct,
)
from utils import scan_source_dir


# ─── tiny in-file schema validator ────────────────────────────────────────────

_TYPE_MAP = {
    "object": dict,
    "array": list,
    "string": str,
    "boolean": bool,
    "integer": int,
    "number": (int, float),
    "null": type(None),
}


def validate_schema(data: object, schema: dict, path: str = "$") -> list[str]:
    """Return a list of human-readable error messages; empty list = valid.

    Supports the JSON Schema draft-07 subset: type, enum, required,
    properties, patternProperties, additionalProperties, items. Enough for
    the per-platform reference schemas in this file.
    """
    errors: list[str] = []

    expected_type = schema.get("type")
    if expected_type is not None:
        py_type = _TYPE_MAP.get(expected_type)
        if py_type is None:
            errors.append(f"{path}: unsupported schema type {expected_type!r}")
            return errors
        # JSON Schema treats bool as not-an-integer
        if expected_type in ("integer", "number") and isinstance(data, bool):
            errors.append(f"{path}: expected {expected_type}, got bool")
            return errors
        if not isinstance(data, py_type):
            errors.append(
                f"{path}: expected {expected_type}, got {type(data).__name__}"
            )
            return errors

    if "enum" in schema and data not in schema["enum"]:
        errors.append(f"{path}: value {data!r} not in enum {schema['enum']}")

    if expected_type == "object" and isinstance(data, dict):
        for key in schema.get("required", []):
            if key not in data:
                errors.append(f"{path}: missing required property '{key}'")
        properties = schema.get("properties", {})
        pattern_properties = schema.get("patternProperties", {})
        additional = schema.get("additionalProperties", True)
        for key, value in data.items():
            child_path = f"{path}.{key}"
            matched = False
            if key in properties:
                errors.extend(validate_schema(value, properties[key], child_path))
                matched = True
            for pattern, sub_schema in pattern_properties.items():
                if re.search(pattern, key):
                    errors.extend(validate_schema(value, sub_schema, child_path))
                    matched = True
            if not matched:
                if additional is False:
                    errors.append(f"{path}: additional property '{key}' not allowed")
                elif isinstance(additional, dict):
                    errors.extend(validate_schema(value, additional, child_path))

    if expected_type == "array" and isinstance(data, list) and "items" in schema:
        for i, item in enumerate(data):
            errors.extend(validate_schema(item, schema["items"], f"{path}[{i}]"))

    return errors


# ─── reference schemas ───────────────────────────────────────────────────────

# Cursor SkillConstruct per-plugin manifest.
# Source: cursor.com/docs/reference/plugins (fetched 2026-05-25)
# +     : docs/research/qa-bug-fixes-2026-05/RESEARCH.md (Bug 3)
_LSP_SERVER_ENTRY_SCHEMA = {
    "type": "object",
    "required": ["command", "extensionToLanguage"],
    "properties": {
        "command": {"type": "string"},
        "args": {"type": "array", "items": {"type": "string"}},
        "extensionToLanguage": {
            "type": "object",
            "patternProperties": {
                r"^\.[a-zA-Z0-9]+$": {"type": "string"},
            },
            "additionalProperties": False,
        },
    },
    "additionalProperties": True,
}

CLAUDE_LSP_CONFIG_SCHEMA = {
    "type": "object",
    # Language-id keys (no ``lspServers`` wrapper, no invented field names).
    # The lowercase pattern is loose so future identifiers like "typescript"
    # or "rust" all pass.
    "patternProperties": {
        r"^[a-z][a-zA-Z0-9_-]*$": _LSP_SERVER_ENTRY_SCHEMA,
    },
    "additionalProperties": False,
}


# Claude Monitors standalone config file.
# Source: code.claude.com/docs/en/plugins-reference#monitors (fetched
# 2026-05-26). Top-level value is a JSON ARRAY of monitor objects with
# required fields name / command / description (and optional ``when``).
# The previous object-with-named-keys shape failed Claude's validator
# with ``expected: array, code: invalid_type`` at the document root.
# +     : docs/research/claude-qa-2026-05-26/RESEARCH.md (F3)
_MONITOR_ENTRY_SCHEMA = {
    "type": "object",
    "required": ["name", "command", "description"],
    "properties": {
        "name": {"type": "string"},
        "command": {"type": "string"},
        "description": {"type": "string"},
        "when": {"type": "string"},
    },
    "additionalProperties": True,
}

CLAUDE_MONITORS_SCHEMA = {
    "type": "array",
    "items": _MONITOR_ENTRY_SCHEMA,
}


# Claude Hooks standalone file.
# Source: code.claude.com/docs/en/plugins-reference#hooks (fetched
# 2026-05-26). The canonical shape is::
#
#   {"hooks": {"<Event>": [{"matcher"?: "...", "hooks": [{"type": "command",
#    "command": "..."}]}]}}
#
# Event keys are PascalCase Claude event names; each entry's inner hook
# must declare a 'type' (command|http|mcp_tool|prompt|agent) and the
# type-specific payload field (here 'command' for command hooks).
# +     : docs/research/claude-qa-2026-05-26/RESEARCH.md (F5)
_CLAUDE_HOOK_LEAF_SCHEMA = {
    "type": "object",
    "required": ["type", "command"],
    "properties": {
        "type": {
            "type": "string",
            "enum": ["command", "http", "mcp_tool", "prompt", "agent"],
        },
        "command": {"type": "string"},
    },
    "additionalProperties": True,
}

_CLAUDE_HOOK_OUTER_SCHEMA = {
    "type": "object",
    "required": ["hooks"],
    "properties": {
        "matcher": {"type": "string"},
        "hooks": {"type": "array", "items": _CLAUDE_HOOK_LEAF_SCHEMA},
    },
    "additionalProperties": True,
}

CLAUDE_HOOKS_FILE_SCHEMA = {
    "type": "object",
    "required": ["hooks"],
    "properties": {
        "description": {"type": "string"},
        "hooks": {
            "type": "object",
            "patternProperties": {
                "^[A-Z][a-zA-Z]+$": {
                    "type": "array",
                    "items": _CLAUDE_HOOK_OUTER_SCHEMA,
                },
            },
            "additionalProperties": False,
        },
    },
    "additionalProperties": True,
}


# The hook-example MUST demonstrate every event in this list so an
# operator can verify firing across session lifecycle, per-turn, and
# tool lifecycle. Subset per docs/research/claude-qa-2026-05-26/RESEARCH.md
# F5 recommended coverage table — categorical breadth without
# exhaustive listing of all 29 documented events.
CLAUDE_REQUIRED_HOOK_EVENTS = (
    "SessionStart",
    "UserPromptSubmit",
    "PreToolUse",
    "PostToolUse",
    "Stop",
    "SessionEnd",
)


# ─── helpers for fixture lookup ──────────────────────────────────────────────

# ─── tests ────────────────────────────────────────────────────────────────────

class TestClaudeLSPConfigSchema(unittest.TestCase):
    """Claude LSP standalone config file must satisfy CLAUDE_LSP_CONFIG_SCHEMA.

    The source ``lsp-servers/<n>/lsp-config.json`` is copied verbatim into
    ``_generated/lsp-<n>/lsp-config.json``; both must match the spec.
    """

    def test_lsp_config_file_schema_fitness(self):
        lsp = next(c for c in CONSTRUCTS.values() if isinstance(c, LSPConstruct))
        names = scan_source_dir(lsp.source_directory)
        self.assertGreater(len(names), 0, "no LSP sources found")
        for name in names:
            for fixture in (
                lsp.source_directory / name / "lsp-config.json",
                REPO_ROOT / "_generated" / f"lsp-{name}" / "lsp-config.json",
            ):
                with self.subTest(fixture=str(fixture.relative_to(REPO_ROOT))):
                    if not fixture.exists():
                        self.skipTest(f"{fixture} not present")
                    data = json.loads(fixture.read_text(encoding="utf-8"))
                    errors = validate_schema(data, CLAUDE_LSP_CONFIG_SCHEMA)
                    self.assertEqual(
                        errors, [],
                        f"{fixture.relative_to(REPO_ROOT)}: schema violations:\n  "
                        + "\n  ".join(errors),
                    )

    def test_lsp_config_no_lspservers_wrapper(self):
        """Negative check: the standalone file must NOT wrap entries under
        an outer ``lspServers`` key (that's the inline-in-plugin.json shape).
        Catches the exact bug from F2 with a human-readable message."""
        lsp = next(c for c in CONSTRUCTS.values() if isinstance(c, LSPConstruct))
        for name in scan_source_dir(lsp.source_directory):
            fixture = lsp.source_directory / name / "lsp-config.json"
            with self.subTest(name=name):
                data = json.loads(fixture.read_text(encoding="utf-8"))
                self.assertNotIn(
                    "lspServers", data,
                    f"{fixture.relative_to(REPO_ROOT)} wraps entries under "
                    "'lspServers' — Claude's standalone lsp-config.json takes "
                    "language IDs as top-level keys (see "
                    "docs/research/claude-qa-2026-05-26/RESEARCH.md F2)",
                )


class TestClaudeMonitorsSchema(unittest.TestCase):
    """Claude monitors.json must be a top-level JSON array per
    code.claude.com/docs/en/plugins-reference#monitors (fetched 2026-05-26)."""

    def test_monitors_file_is_array(self):
        monitor = next(c for c in CONSTRUCTS.values() if isinstance(c, MonitorConstruct))
        for name in scan_source_dir(monitor.source_directory):
            for fixture in (
                monitor.source_directory / name / "monitors" / "monitors.json",
                REPO_ROOT / "_generated" / f"monitor-{name}" / "monitors" / "monitors.json",
            ):
                with self.subTest(fixture=str(fixture.relative_to(REPO_ROOT))):
                    if not fixture.exists():
                        self.skipTest(f"{fixture} not present")
                    data = json.loads(fixture.read_text(encoding="utf-8"))
                    self.assertIsInstance(
                        data, list,
                        f"{fixture.relative_to(REPO_ROOT)} top-level value must "
                        "be a JSON array (see docs/research/claude-qa-2026-05-26/"
                        "RESEARCH.md F3)",
                    )

    def test_monitors_file_schema_fitness(self):
        monitor = next(c for c in CONSTRUCTS.values() if isinstance(c, MonitorConstruct))
        for name in scan_source_dir(monitor.source_directory):
            fixture = monitor.source_directory / name / "monitors" / "monitors.json"
            with self.subTest(name=name):
                if not fixture.exists():
                    self.skipTest(f"{fixture} not present")
                data = json.loads(fixture.read_text(encoding="utf-8"))
                errors = validate_schema(data, CLAUDE_MONITORS_SCHEMA)
                self.assertEqual(
                    errors, [],
                    f"{fixture.relative_to(REPO_ROOT)}: schema violations:\n  "
                    + "\n  ".join(errors),
                )


class TestClaudeHooksFileSchema(unittest.TestCase):
    """Claude hooks.json must satisfy CLAUDE_HOOKS_FILE_SCHEMA and the
    reference example must enumerate every required Claude hook event per
    docs/research/claude-qa-2026-05-26/RESEARCH.md F5."""

    def test_hooks_file_schema_fitness(self):
        hook = next(c for c in CONSTRUCTS.values() if isinstance(c, HookConstruct))
        for name in scan_source_dir(hook.source_directory):
            fixture = hook.source_directory / name / "hooks" / "hooks.json"
            with self.subTest(name=name):
                if not fixture.exists():
                    self.skipTest(f"{fixture} not present")
                data = json.loads(fixture.read_text(encoding="utf-8"))
                errors = validate_schema(data, CLAUDE_HOOKS_FILE_SCHEMA)
                self.assertEqual(
                    errors, [],
                    f"{fixture.relative_to(REPO_ROOT)}: schema violations:\n  "
                    + "\n  ".join(errors),
                )

    def test_hook_example_covers_required_events(self):
        """The reference example MUST demonstrate every event in
        CLAUDE_REQUIRED_HOOK_EVENTS so operators can verify firing for each
        major hook type (session lifecycle, per-turn, tool lifecycle)."""
        hook = next(c for c in CONSTRUCTS.values() if isinstance(c, HookConstruct))
        fixture = hook.source_directory / "example" / "hooks" / "hooks.json"
        if not fixture.exists():
            self.skipTest(f"{fixture} not present")
        data = json.loads(fixture.read_text(encoding="utf-8"))
        present = set((data.get("hooks") or {}).keys())
        missing = set(CLAUDE_REQUIRED_HOOK_EVENTS) - present
        self.assertFalse(
            missing,
            f"hook-example missing required Claude events {missing}; "
            "see docs/research/claude-qa-2026-05-26/RESEARCH.md F5 for the "
            "documented Claude hook type list",
        )


class TestValidatorSelfCheck(unittest.TestCase):
    """Smoke tests for the inline validate_schema helper.

    The validator is small enough to self-check. If these fail, every
    schema-fitness assertion above is suspect.
    """

    def test_missing_required(self):
        errors = validate_schema(
            {"name": "x"},
            {"type": "object", "required": ["name", "version"]},
        )
        self.assertTrue(any("version" in e for e in errors))

    def test_wrong_type(self):
        errors = validate_schema(
            "hello",
            {"type": "object", "required": ["x"]},
        )
        self.assertTrue(any("expected object" in e for e in errors))

    def test_additional_properties_false_rejects(self):
        errors = validate_schema(
            {"a": 1, "b": 2},
            {
                "type": "object",
                "properties": {"a": {"type": "integer"}},
                "additionalProperties": False,
            },
        )
        self.assertTrue(any("'b'" in e for e in errors))

    def test_pattern_properties_match(self):
        errors = validate_schema(
            {"pre_user_prompt": []},
            {
                "type": "object",
                "patternProperties": {"^[a-z_]+$": {"type": "array"}},
                "additionalProperties": False,
            },
        )
        self.assertEqual(errors, [])

    def test_pattern_properties_reject_pascal_case(self):
        errors = validate_schema(
            {"UserPromptSubmit": []},
            {
                "type": "object",
                "patternProperties": {"^[a-z_]+$": {"type": "array"}},
                "additionalProperties": False,
            },
        )
        self.assertTrue(any("UserPromptSubmit" in e for e in errors))


if __name__ == "__main__":
    unittest.main(verbosity=2)
