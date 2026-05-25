## Revert on Failure

Use git as a safety net. Commit known-good state, experiment, measure, revert if no improvement.

- **Commit before experimenting.** Never experiment on a dirty working tree.
- **Define "better" before changing code.** If you cannot state the metric, you are not ready to change code.
- **Measure after every change.** Do not batch speculative changes — test each one individually.
- **Keep what improves, revert what doesn't.** `git checkout -- .` or `git reset --hard` back to last good state.
- **Never push through.** 3 failed attempts at the same approach = abandon it, try a different angle.

```
1. git commit   (baseline)
2. Make one change
3. Run the check
4. Improved? -> git commit    |    Same or worse? -> git reset --hard HEAD
5. Go to 2
```
