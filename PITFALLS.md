# Pitfalls

## Confirm summary misrepresents scope when multiple platforms selected

- **Symptom:** Selecting Devin + Windsurf with all rules in global scope showed everything in "Workspace" section, nothing in "Global."
- **Cause:** `has_forced_ws` is True if ANY platform lacks global rules. The summary code treated this as "all items are workspace," but actual install correctly handles per-platform forcing.
- **Fix:** Show items in user-chosen scope (global), add a note naming which platforms redirect to workspace. Commit `404b181`.

## Banner K identical to R

- **Symptom:** The letter K in both SKILLS and MARKET banner text looked like R.
- **Cause:** K top row used `╦═╗` (closed top, same as R) instead of `╦ ╦` (open top).
- **Fix:** Changed K top glyph from `\u2566\u2550\u2557` to `\u2566 \u2566`. Commit `404b181`.

## Installed marker only checks primary platform

- **Symptom:** Rules showed as "not installed" even when installed on other platforms.
- **Cause:** `is_rule_installed` / `is_skill_installed` only checked the first detected platform's global paths. If Devin was primary, `global.rules = None` meant all rules showed as uninstalled.
- **Fix:** Added `_is_rule_installed_any()` / `_is_skill_installed_any()` that check across all detected platforms. Commit `404b181`.

## IndexError crash when catalog.toml missing

- **Symptom:** `list(PLATFORMS.keys())[0]` crashes if PLATFORMS is empty.
- **Cause:** `_load_catalog()` returns `{}` when catalog.toml is absent, making PLATFORMS empty.
- **Fix:** Guard with error message before indexing. Commit `d6f254a`.

## install_rule exists check after open(a)

- **Symptom:** Confusing logic: `target.exists()` checked after `open(target, "a")` which always creates the file.
- **Cause:** The append-mode open creates the file, making the exists check always True.
- **Fix:** Capture `needs_separator` before opening. Commit `d6f254a`.
