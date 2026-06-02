"""agent install — copy agent .md (or convert to .toml for Codex) to targets.

Per D-13 Option C: emit to .agents/, .cursor/, .gemini/, .claude/, and (after
md→TOML conversion) .codex/. With ``--agents-only`` only .agents/ is written.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

from ..utils.paths import resolve_agent

# scripts/ already on sys.path when invoked via the installed shim (PYTHONPATH).
# Direct invocation (uv run scripts/agents_cli/main.py) also works because the
# parent main.py module prepends scripts/ to sys.path itself.
try:
    from converters.md_to_toml import claude_agent_md_to_codex_toml
except ImportError:  # CLI installed standalone — converter shipped alongside
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from converters.md_to_toml import claude_agent_md_to_codex_toml


def install(marketplace_root: Path, name: str, *, scope: str, agents_only: bool) -> list[Path]:
    """Install ``agent-<name>``.

    The agent plugin source ``agents/<name>/agents/`` may contain multiple .md
    files; we install each file separately at each destination (which is one
    file path per dest, named after the agent file stem rather than the plugin
    name). For simplicity, the path resolver assumes one-file-per-plugin and
    uses ``<name>.md`` as the destination filename. If the source contains a
    single .md file we use that; if it contains multiple, we write all of them
    by replacing the destination stem with each source stem.
    """
    src_agents = marketplace_root / "src" / "agents" / name / "agents"
    if not src_agents.exists():
        raise FileNotFoundError(f"agent-{name} not found at {src_agents}")
    src_files = sorted(src_agents.glob("*.md"))
    if not src_files:
        raise FileNotFoundError(f"No agent .md files in {src_agents}")

    targets = resolve_agent(name, scope, agents_only)
    written: list[Path] = []
    for dest_template in [targets.agents_path, *targets.platform_paths]:
        for src in src_files:
            dest = dest_template.with_name(f"{src.stem}{dest_template.suffix}")
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.suffix == ".toml":
                try:
                    toml_text = claude_agent_md_to_codex_toml(
                        src.read_text(encoding="utf-8")
                    )
                except ValueError as exc:
                    # Per-target failure tolerance (D-13): skip this target,
                    # continue with the rest.
                    print(
                        f"warning: skipping Codex TOML emit for {src.name}: {exc}",
                        file=sys.stderr,
                    )
                    continue
                dest.write_text(toml_text, encoding="utf-8")
            else:
                shutil.copy(src, dest)
            written.append(dest)
    return written


def uninstall(name: str, *, scope: str, agents_only: bool) -> list[Path]:
    # Without the marketplace clone we can't enumerate the source agent files,
    # so we remove the canonical ``<name>.md/.toml`` path at every destination
    # (sufficient for the common one-agent-per-plugin case).
    targets = resolve_agent(name, scope, agents_only)
    removed: list[Path] = []
    for dest in [targets.agents_path, *targets.platform_paths]:
        if dest.exists():
            dest.unlink()
            removed.append(dest)
    return removed
