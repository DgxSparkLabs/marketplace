## Simplicity Bar

Every change has a complexity cost. Weigh it against the improvement.

- **Removing code that preserves results is always a win.** Fewer lines, same outcome = strictly better.
- **Marginal gains do not justify ugly complexity.** A 0.1% improvement from deleting code is worth it. A 0.1% improvement that adds 20 hacky lines is not.
- **Equal results + simpler code = keep.** A refactor with same behavior but less complexity is a positive outcome.
- **Complexity is a liability.** Every line must be read, maintained, and debugged. Earn each line.
