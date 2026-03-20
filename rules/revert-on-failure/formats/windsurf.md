---
trigger: always_on
description: "Commit before experimenting, measure after, keep improvements, revert failures -- never accumulate broken state"
---

## Revert on Failure

When making speculative changes, use git as a safety net. Commit a known-good state, experiment, measure, and revert if the change does not improve things.

- **Commit before experimenting.** Always have a clean commit to revert to. Never experiment on a dirty working tree.
- **Define "better" before changing code.** Know your success metric (test passes, performance improves, error disappears) before making the change. If you cannot state the metric, you are not ready to change code.
- **Measure after every change.** Run the relevant check immediately. Do not batch multiple speculative changes -- test each one individually.
- **Keep what improves, revert what doesn't.** If the metric improved, commit and advance. If it didn't, `git checkout -- .` or `git reset --hard` back to the last good state. Do not accumulate failed experiments in the working tree.
- **If a change crashes, use judgment.** Trivial fix (typo, missing import)? Fix and re-run. Fundamentally broken idea? Revert immediately and move on.
- **Never push through.** If you have tried the same approach 3 times without improvement, abandon it and try a different angle.

> *"If val_bpb improved (lower), you 'advance' the branch, keeping the git commit. If val_bpb is equal or worse, you git reset back to where you started."*
> -- [karpathy/autoresearch](https://github.com/karpathy/autoresearch/blob/master/program.md)

### The Loop

```
1. git commit   (baseline / known-good state)
2. Make one change
3. Run the check (test, build, benchmark)
4. Improved? -> git commit (new baseline)
   Same or worse? -> git reset --hard HEAD
5. Go to 2
```

### Examples

| Scenario | Action |
|----------|--------|
| Refactoring a function, tests still pass after change | **Commit** -- new baseline |
| Trying a different algorithm, tests fail | **Revert** -- go back to working state |
| Build breaks due to missing import you just introduced | **Fix the typo and re-run** -- trivial crash |
| Third attempt at an optimization yields no gain | **Abandon the approach** -- try something else |
