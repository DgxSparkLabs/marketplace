# Releasing

Releases are optional for a skills marketplace — users always install from `main`. Tag a release when you want a citable version or GitHub Release notes.

## Checklist

1. **Set the version.** Edit `version` in `src/MARKETPLACE.toml` (semver). It propagates into every generated `plugin.json` and marketplace entry.
2. **Push a PR.** On a same-repo branch, `regen-bot` regenerates and commits the manifests for you; running `uv run scripts/generate_manifest.py` locally is optional.
3. **Verify.** `uv run scripts/tasks.py verify` — source validation, drift-clean, the test suites (`test_marketplace`, `test_tooling`), `claude plugin validate ./`.
4. **Record.** Add release notes to [`CHANGELOG.md`](CHANGELOG.md).
5. **Ship.** Merge, then tag:
   ```bash
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```
6. **(Optional)** Create a GitHub Release from the tag, pasting the CHANGELOG section.

## Dependency hygiene

Dependabot ([`.github/dependabot.yml`](.github/dependabot.yml)) opens weekly PRs bumping the GitHub Actions versions used by CI. Review and merge them like any other PR (the full CI suite gates them).
