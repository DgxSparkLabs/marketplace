"""Per-construct install handlers.

The ``PREFIX_TO_HANDLER`` dict maps a plugin's construct prefix (resolved
from the plugin's name — e.g. ``skill-example`` → ``skill``) to the
handler module that knows how to install / uninstall that construct
across the per-platform path matrix (D-13 Option C).
"""

from __future__ import annotations

from . import agent, command, hook, mcp, rule, skill

# Order matters only for `agents list --available --type` filtering UX.
PREFIX_TO_HANDLER: dict[str, object] = {
    "skill":        skill,
    "rule":         rule,
    "agent":        agent,
    "hook":         hook,
    "mcp":          mcp,
    "command":      command,
    # Claude-only constructs — handled by the generic claude_only handler
    # at call time (see install.py). We list the prefixes so unknown-prefix
    # detection still works.
    "lsp":          None,
    "monitor":      None,
    "output-style": None,
    "theme":        None,
    "bundle":       None,
}


def split_plugin_name(plugin_name: str) -> tuple[str, str]:
    """Split ``skill-example`` into ``("skill", "example")``.

    Handles multi-word prefixes (``output-style-X`` → ``("output-style", "X")``).
    Raises ValueError if no known prefix matches.
    """
    # Longest-prefix-first match so output-style beats output.
    for prefix in sorted(PREFIX_TO_HANDLER, key=len, reverse=True):
        if plugin_name.startswith(f"{prefix}-"):
            return prefix, plugin_name[len(prefix) + 1:]
    raise ValueError(
        f"Unknown plugin prefix in '{plugin_name}'. "
        f"Known prefixes: {sorted(PREFIX_TO_HANDLER)}"
    )
