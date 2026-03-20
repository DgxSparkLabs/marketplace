---
trigger: always_on
description: "Weigh complexity cost against improvement magnitude -- simpler is better, deletion is a win"
---

## Simplicity Bar

Every change has a complexity cost. Weigh it against the improvement before keeping it.

- **Removing code that preserves results is always a win.** Fewer lines, same outcome = strictly better. Keep it unconditionally.
- **Marginal gains do not justify ugly complexity.** A 0.1% improvement that adds 20 lines of hacky code is not worth it. A 0.1% improvement from *deleting* code is definitely worth it.
- **Equal results + simpler code = keep.** If a refactor yields the same behavior with less complexity, that is a positive outcome, not a wash.
- **Before adding code, ask:** "Would I accept this in a code review if someone else wrote it?" If the answer is "only because it technically works," don't ship it.
- **Complexity is a liability.** Every line you add must be read, maintained, and debugged by the next agent. Earn each line.

> *"All else being equal, simpler is better. A small improvement that adds ugly complexity is not worth it. Conversely, removing something and getting equal or better results is a great outcome -- that's a simplification win."*
> -- [karpathy/autoresearch](https://github.com/karpathy/autoresearch/blob/master/program.md)

### Examples

| Change | Outcome | Verdict |
|--------|---------|---------|
| Add 30-line caching layer | 2% speedup | Weigh carefully -- is 2% worth 30 lines? |
| Delete unused abstraction | Same behavior | **Keep** -- simpler with no downside |
| Inline a helper used once | Same behavior, fewer indirections | **Keep** -- simplification win |
| Add retry logic with backoff | Fixes flaky failures | **Keep** -- complexity is justified by reliability |
| Add feature flag framework | Supports one toggle | **Reject** -- over-engineering for one use case |
