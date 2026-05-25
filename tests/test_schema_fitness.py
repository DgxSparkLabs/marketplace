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

from constructs import CONSTRUCTS, AgentConstruct, HookConstruct, SkillConstruct
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
CURSOR_SKILL_PLUGIN_SCHEMA = {
    "type": "object",
    "required": ["name", "version", "description", "skills"],
    "properties": {
        "name": {"type": "string"},
        "version": {"type": "string"},
        "description": {"type": "string"},
        # ``skills`` may be a string-pointer or an array per the Cursor
        # reference; we emit the string form.
        "skills": {"type": "string"},
    },
    "additionalProperties": True,  # Cursor allows other optional pointers
}


# Gemini AgentConstruct frontmatter (parsed from .gemini/agents/<n>.md).
# Source: geminicli.com/docs/core/subagents/ (fetched 2026-05-25)
# +     : docs/research/qa-bug-fixes-2026-05/RESEARCH.md (Bug 2)
GEMINI_AGENT_FRONTMATTER_SCHEMA = {
    "type": "object",
    "required": ["name", "description"],
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        # The bug: ``tools`` MUST be an array, not a comma-separated string.
        "tools": {"type": "array", "items": {"type": "string"}},
        "model": {"type": "string"},
        "kind": {"type": "string", "enum": ["local", "remote"]},
    },
    "additionalProperties": True,
}


# Windsurf HookConstruct file.
# Source: docs.windsurf.com/windsurf/cascade/hooks (fetched 2026-05-25)
# +     : docs/research/qa-bug-fixes-2026-05/RESEARCH.md (sanity #5)
_WINDSURF_HOOK_ENTRY_SCHEMA = {
    "type": "object",
    "properties": {
        "command": {"type": "string"},
        "powershell": {"type": "string"},
        "show_output": {"type": "boolean"},
        "working_directory": {"type": "string"},
    },
    "additionalProperties": False,
}

WINDSURF_HOOKS_SCHEMA = {
    "type": "object",
    "required": ["hooks"],
    "properties": {
        "hooks": {
            "type": "object",
            # Only snake_case event keys per Windsurf docs. Top-level
            # PascalCase Claude event names (UserPromptSubmit, etc.) get
            # rejected by patternProperties + additionalProperties=False.
            "patternProperties": {
                "^[a-z][a-z_]*$": {
                    "type": "array",
                    "items": _WINDSURF_HOOK_ENTRY_SCHEMA,
                },
            },
            "additionalProperties": False,
        },
    },
}


# Cursor HookConstruct file.
# Source: cursor.com/docs/agent/hooks (fetched 2026-05-25)
# +     : docs/research/qa-bug-fixes-2026-05/RESEARCH.md (Q1, empirical
#         verification round)
_CURSOR_HOOK_ENTRY_SCHEMA = {
    "type": "object",
    "required": ["command"],
    "properties": {
        "command": {"type": "string"},
        "matcher": {"type": "string"},
        "timeout": {"type": "number"},
        "loop_limit": {"type": "number"},
        "failClosed": {"type": "boolean"},
    },
    "additionalProperties": False,
}

CURSOR_HOOKS_SCHEMA = {
    "type": "object",
    "required": ["version", "hooks"],
    "properties": {
        # Cursor's parser silently ignores the file without `version: 1`
        # (verified against community plugins ralph-loop + continual-learning).
        "version": {"type": "number"},
        "hooks": {
            "type": "object",
            # Only camelCase event keys per Cursor docs. Top-level
            # PascalCase Claude event names (UserPromptSubmit, ...) get
            # rejected by patternProperties + additionalProperties=False.
            "patternProperties": {
                "^[a-z][a-zA-Z]*$": {
                    "type": "array",
                    "items": _CURSOR_HOOK_ENTRY_SCHEMA,
                },
            },
            "additionalProperties": False,
        },
    },
    "additionalProperties": False,
}


# Gemini HookConstruct file.
# Source: geminicli.com/docs/hooks/reference/ (fetched 2026-05-25) plus
# the working sandipchitale/hooklog extension (logs/hooklog-hooks.json).
# +     : docs/research/qa-bug-fixes-2026-05/RESEARCH.md (Q2)
#
# Gemini's hook-file shape is structurally identical to Claude's
# (`hooks.<event>[].hooks[].{type, command}` — nested twice). Only the
# event-name vocabulary differs: Gemini uses its own PascalCase set
# (BeforeModel, AfterModel, BeforeTool, ...). The schema below enforces
# the vocabulary via an enum of valid Gemini event names.

_GEMINI_INNER_HOOK_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "command": {"type": "string"},
        "name": {"type": "string"},
    },
    "additionalProperties": True,  # other inner fields documented per-plugin
}

_GEMINI_OUTER_HOOK_SCHEMA = {
    "type": "object",
    "properties": {
        "matcher": {"type": "string"},
        "hooks": {"type": "array", "items": _GEMINI_INNER_HOOK_SCHEMA},
    },
    "additionalProperties": True,
}

# Gemini events per the docs + hooklog working extension. Keep the
# allowlist here so a Claude leak (e.g. UserPromptSubmit) trips the
# enum check rather than silently passing.
GEMINI_HOOK_EVENT_NAMES = (
    "SessionStart", "SessionEnd",
    "BeforeModel", "AfterModel",
    "BeforeAgent", "AfterAgent",
    "BeforeTool", "AfterTool", "BeforeToolSelection",
    "PreCompress", "Notification",
)

GEMINI_HOOKS_SCHEMA = {
    "type": "object",
    "required": ["hooks"],
    "properties": {
        "description": {"type": "string"},
        "hooks": {
            "type": "object",
            # The patternProperties regex matches any PascalCase name —
            # the test_no_claude_event_names_anywhere test below catches
            # specific Claude leaks (UserPromptSubmit etc.) with a
            # human-readable message naming the leaked event.
            "patternProperties": {
                "^[A-Z][a-zA-Z]+$": {
                    "type": "array",
                    "items": _GEMINI_OUTER_HOOK_SCHEMA,
                },
            },
            "additionalProperties": False,
        },
    },
    "additionalProperties": True,
}


# ─── helpers for fixture lookup ──────────────────────────────────────────────

def _gemini_agent_frontmatter(md_path: Path) -> dict:
    """Parse the YAML-ish frontmatter from a Gemini sub-agent .md.

    Mirrors converters/md_to_gemini_md._parse_frontmatter_and_body but
    handles the YAML *array* shape used by Gemini (``tools:`` followed
    by ``  - <tool>`` lines). Returns a dict with simple-scalar +
    string-array values. No third-party YAML dep — sufficient for our
    sub-agent frontmatter shape.
    """
    text = md_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{md_path}: missing frontmatter opener")
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError(f"{md_path}: frontmatter unterminated")
    fm_text = text[4:end]
    fm: dict = {}
    current_array_key: str | None = None
    for raw in fm_text.splitlines():
        if not raw.strip():
            current_array_key = None
            continue
        # YAML array continuation line: ``  - <value>``
        if current_array_key is not None and raw.startswith("  - "):
            fm[current_array_key].append(raw[len("  - "):].strip())
            continue
        current_array_key = None
        if raw.startswith(" "):
            continue
        if ":" not in raw:
            continue
        key, _, val = raw.partition(":")
        key = key.strip()
        val = val.strip()
        if val == "":
            # Header for a YAML array on subsequent lines.
            fm[key] = []
            current_array_key = key
        else:
            fm[key] = val.strip('"').strip("'")
    return fm


# ─── tests ────────────────────────────────────────────────────────────────────

class TestCursorSkillManifestSchema(unittest.TestCase):
    """Every emitted Cursor SkillConstruct plugin.json must satisfy
    CURSOR_SKILL_PLUGIN_SCHEMA."""

    def test_cursor_skill_plugin_json_schema_fitness(self):
        skill = next(c for c in CONSTRUCTS.values() if isinstance(c, SkillConstruct))
        names = scan_source_dir(skill.source_directory)
        self.assertGreater(len(names), 0, "no skill sources found")
        for name in names:
            plugin_name = f"skill-{name}"
            path = REPO_ROOT / "_generated" / plugin_name / ".cursor-plugin" / "plugin.json"
            with self.subTest(plugin=plugin_name):
                data = json.loads(path.read_text(encoding="utf-8"))
                errors = validate_schema(data, CURSOR_SKILL_PLUGIN_SCHEMA)
                self.assertEqual(
                    errors, [],
                    f"{plugin_name}: schema violations:\n  " + "\n  ".join(errors),
                )


class TestGeminiAgentFrontmatterSchema(unittest.TestCase):
    """Every emitted Gemini sub-agent .md frontmatter must satisfy
    GEMINI_AGENT_FRONTMATTER_SCHEMA."""

    def test_gemini_agent_frontmatter_schema_fitness(self):
        agent = next(c for c in CONSTRUCTS.values() if isinstance(c, AgentConstruct))
        agents_dir = REPO_ROOT / ".gemini" / "agents"
        if not agents_dir.exists():
            self.skipTest(".gemini/agents/ does not exist")
        files = sorted(agents_dir.glob("*.md"))
        self.assertGreater(len(files), 0, ".gemini/agents/ is empty")
        # Sanity: every source agent has an emitted counterpart
        emitted = {p.name for p in files}
        for name in scan_source_dir(agent.source_directory):
            src_agents = agent.source_directory / name / "agents"
            if not src_agents.exists():
                continue
            for src_md in src_agents.glob("*.md"):
                with self.subTest(source=src_md.name):
                    self.assertIn(
                        src_md.name, emitted,
                        f"source agents/{name}/agents/{src_md.name} not "
                        f"emitted to .gemini/agents/",
                    )
        for md_path in files:
            with self.subTest(agent=md_path.name):
                fm = _gemini_agent_frontmatter(md_path)
                errors = validate_schema(fm, GEMINI_AGENT_FRONTMATTER_SCHEMA)
                self.assertEqual(
                    errors, [],
                    f"{md_path.name}: frontmatter schema violations:\n  "
                    + "\n  ".join(errors),
                )


class TestWindsurfHooksSchema(unittest.TestCase):
    """Emitted .windsurf/hooks.json must satisfy WINDSURF_HOOKS_SCHEMA."""

    def test_windsurf_hooks_schema_fitness(self):
        path = REPO_ROOT / ".windsurf" / "hooks.json"
        if not path.exists():
            self.skipTest(".windsurf/hooks.json does not exist")
        data = json.loads(path.read_text(encoding="utf-8"))
        errors = validate_schema(data, WINDSURF_HOOKS_SCHEMA)
        self.assertEqual(
            errors, [],
            ".windsurf/hooks.json schema violations:\n  " + "\n  ".join(errors),
        )

    def test_no_claude_event_names_anywhere(self):
        """Negative check: no Claude PascalCase event name may appear as a key.

        Backstop for ``additionalProperties: False`` above (so test failures
        name the exact key that leaked, not a generic "additional property").
        """
        path = REPO_ROOT / ".windsurf" / "hooks.json"
        if not path.exists():
            self.skipTest(".windsurf/hooks.json does not exist")
        data = json.loads(path.read_text(encoding="utf-8"))
        claude_events = {
            "UserPromptSubmit", "PreToolUse", "PostToolUse",
            "Notification", "Stop", "SubagentStop",
            "SessionStart", "SessionEnd", "PreCompact",
        }
        leaked = set((data.get("hooks") or {}).keys()) & claude_events
        self.assertFalse(
            leaked,
            f"Claude event names leaked into .windsurf/hooks.json: {leaked}",
        )


class TestCursorHooksSchema(unittest.TestCase):
    """Emitted .cursor/hooks.json must satisfy CURSOR_HOOKS_SCHEMA."""

    def test_cursor_hooks_schema_fitness(self):
        path = REPO_ROOT / ".cursor" / "hooks.json"
        if not path.exists():
            self.skipTest(".cursor/hooks.json does not exist")
        data = json.loads(path.read_text(encoding="utf-8"))
        errors = validate_schema(data, CURSOR_HOOKS_SCHEMA)
        self.assertEqual(
            errors, [],
            ".cursor/hooks.json schema violations:\n  " + "\n  ".join(errors),
        )

    def test_cursor_hooks_has_version_field(self):
        """Cursor's parser silently ignores hooks.json without `version: 1`.

        Verified against three working community plugins:
          - cursor/plugins/continual-learning  (logs/cl-hooks.json)
          - cursor/plugins/ralph-loop          (logs/ralph-hooks.json)
          - prisma/cursor-plugin               (logs/prisma-root-hooks.json)
        """
        path = REPO_ROOT / ".cursor" / "hooks.json"
        if not path.exists():
            self.skipTest(".cursor/hooks.json does not exist")
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(
            data.get("version"), 1,
            ".cursor/hooks.json missing required `version: 1` top-level field "
            "(Cursor's parser ignores the file otherwise — see "
            "docs/research/qa-bug-fixes-2026-05/RESEARCH.md Q1).",
        )

    def test_no_claude_event_names_in_cursor_hooks(self):
        """Negative check: no Claude PascalCase event name may appear as a key.

        Backstop for ``additionalProperties: False`` (so test failures name
        the exact key that leaked, not a generic "additional property").
        """
        path = REPO_ROOT / ".cursor" / "hooks.json"
        if not path.exists():
            self.skipTest(".cursor/hooks.json does not exist")
        data = json.loads(path.read_text(encoding="utf-8"))
        claude_events = {
            "UserPromptSubmit", "PreToolUse", "PostToolUse",
            "Notification", "Stop", "SubagentStop",
            "SessionStart", "SessionEnd", "PreCompact",
        }
        leaked = set((data.get("hooks") or {}).keys()) & claude_events
        self.assertFalse(
            leaked,
            f"Claude event names leaked into .cursor/hooks.json: {leaked}",
        )


class TestGeminiHooksSchema(unittest.TestCase):
    """Emitted .gemini/hooks/hooks.json must satisfy GEMINI_HOOKS_SCHEMA."""

    def test_gemini_hooks_schema_fitness(self):
        path = REPO_ROOT / ".gemini" / "hooks" / "hooks.json"
        if not path.exists():
            self.skipTest(".gemini/hooks/hooks.json does not exist")
        data = json.loads(path.read_text(encoding="utf-8"))
        errors = validate_schema(data, GEMINI_HOOKS_SCHEMA)
        self.assertEqual(
            errors, [],
            ".gemini/hooks/hooks.json schema violations:\n  "
            + "\n  ".join(errors),
        )

    def test_gemini_event_names_are_in_documented_vocabulary(self):
        """Every event key must be a documented Gemini event name.

        Gemini's vocabulary is small + closed (per
        geminicli.com/docs/hooks/reference/ + the hooklog working
        extension). Any unknown PascalCase key (e.g. a Claude
        `UserPromptSubmit` leak) is a bug.
        """
        path = REPO_ROOT / ".gemini" / "hooks" / "hooks.json"
        if not path.exists():
            self.skipTest(".gemini/hooks/hooks.json does not exist")
        data = json.loads(path.read_text(encoding="utf-8"))
        keys = set((data.get("hooks") or {}).keys())
        unknown = keys - set(GEMINI_HOOK_EVENT_NAMES)
        self.assertFalse(
            unknown,
            f"Unknown event names in .gemini/hooks/hooks.json: {unknown} "
            f"(documented Gemini events: {GEMINI_HOOK_EVENT_NAMES})",
        )

    def test_no_claude_event_names_in_gemini_hooks(self):
        """Negative check: no Claude PascalCase event name leaks through.

        Some Claude names (SessionStart, SessionEnd, Notification, PreCompact)
        DO appear in Gemini's vocabulary verbatim — those are allowed. But
        the Claude-only names (UserPromptSubmit, PreToolUse, PostToolUse,
        Stop, SubagentStop) must not leak.
        """
        path = REPO_ROOT / ".gemini" / "hooks" / "hooks.json"
        if not path.exists():
            self.skipTest(".gemini/hooks/hooks.json does not exist")
        data = json.loads(path.read_text(encoding="utf-8"))
        claude_only_events = {
            "UserPromptSubmit", "PreToolUse", "PostToolUse",
            "Stop", "SubagentStop",
        }
        leaked = set((data.get("hooks") or {}).keys()) & claude_only_events
        self.assertFalse(
            leaked,
            f"Claude-only event names leaked into .gemini/hooks/hooks.json: "
            f"{leaked}",
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
