# Releasing

The marketplace is **Claude-first stable**: releases are validated on Claude
Code. The other five platforms (Codex, Gemini, Cursor, Windsurf, Devin) emit and
are tracked toward parity in [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Checklist

1. **Set the version.** Edit `version` in `src/MARKETPLACE.toml` (semver).
2. **Regenerate.** Run `uv run scripts/generate_manifest.py`. The version
   propagates into every generated `plugin.json`, so expect a wide diff — keep
   the version bump in **its own commit**.
3. **Verify.** Run `uv run scripts/tasks.py verify` — drift-clean, all the test suites
   (`test_marketplace`, `test_schema_fitness`, `test_agents_cli`, `test_tooling`), and
   `claude plugin validate ./` clean.
4. **Record.** Add release notes to [`CHANGELOG.md`](CHANGELOG.md).
5. **Ship.** Open a PR; on merge to `main`, tag the release:
   ```bash
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```
6. **(Optional)** Create a GitHub Release from the tag, pasting the CHANGELOG
   section.

## Dependency hygiene

Dependabot ([`.github/dependabot.yml`](.github/dependabot.yml)) opens weekly PRs
bumping the GitHub Actions versions used by the CI workflows. Review and merge
them like any other PR (the full CI suite gates them).
