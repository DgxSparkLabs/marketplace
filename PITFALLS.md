# Pitfalls

## Confirm summary misrepresents scope when multiple platforms selected

- **Symptom:** Selecting Devin + Windsurf with all rules in global scope showed everything in "Workspace" section, nothing in "Global."
- **Cause:** `has_forced_ws` is True if ANY platform lacks global rules. The summary code treated this as "all items are workspace," but actual install correctly handles per-platform forcing.
- **Fix:** Show items in user-chosen scope (global), add a note naming which platforms redirect to workspace. Commit `404b181`.

## Banner K glyph doesn't read as K

- **Symptom:** The letter K in both SKILLS and MARKET banner text didn't look like K (first fix made it `╦ ╦` / `╠╩╗` / `╩ ╩` — two parallel verticals on top, reads as H).
- **Cause:** The banner uses the `calvin_s` pyfiglet font. The canonical K top row is `╦╔═` (vertical + upper diagonal arm), not `╦ ╦` (two parallel verticals).
- **Fix:** Changed K top row from `╦ ╦` to `╦╔═` in both SKILLS and MARKET lines. Commit `404b181`, then corrected again.

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

## telegram-notify skill leaks secrets via agent echo

- **Symptom:** SKILL.md told the agent to run `echo "$TELEGRAM_BOT_TOKEN" "$TELEGRAM_CHAT_ID"` to check config, printing raw secrets into the conversation context. Also, `setup.py` printed the full bot token in a URL during fallback.
- **Cause:** Env var validation was delegated to the agent (via shell echo) instead of to the script. The setup script interpolated the token into a user-facing URL.
- **Fix:** Added `--check` flag to `send_telegram.py` that validates env vars and tests the token against the API without revealing secret values. Updated SKILL.md to use `--check`. Masked the token in setup.py's fallback URL.
