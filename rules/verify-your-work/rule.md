## Verify Your Work

Test everything you create before declaring done. Do not assume correctness — prove it.

- **Run the code.** If it produces output, inspect it. If it has side effects, confirm they occurred.
- **Prove three things:** correct outcome, correct mechanism (went through the intended path), clean side effects (no leaks, no stale state).
- **Test the negative path.** Invalid inputs must produce clean errors, not crashes.
- **Be autonomous.** Exhaust all approaches before asking the user for help.
- **Pause for what only the user can provide** — API keys, OAuth, credentials, policy decisions.
- **State what was tested** and what remains untested. Never say "should work."
