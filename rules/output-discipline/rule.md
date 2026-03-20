## Output Discipline

Do not flood your context with raw command output. Redirect to files and extract only what you need.

- **Redirect verbose commands to files.** Use `command > output.log 2>&1` for anything that produces more than a screenful. Never pipe long output into your context window.
- **Extract with targeted reads.** Use `grep`, `tail`, `head`, or specific line reads to pull out the information you need. Do not read entire log files when one line answers the question.
- **Never use `tee` for long-running commands.** It floods your context with the same output you saved to disk. Redirect, then read selectively.
- **Diagnose failures from the end.** If a command fails, `tail -n 50 output.log` gets you the stack trace. Do not read from the top.
- **Delete temporary output files when done.** Log files are diagnostic tools, not artifacts. Clean up after yourself.

> *"Run the experiment: `uv run train.py > run.log 2>&1` (redirect everything -- do NOT use tee or let output flood your context). Read out the results: `grep '^val_bpb:\|^peak_vram_mb:' run.log`"*
> -- [karpathy/autoresearch](https://github.com/karpathy/autoresearch/blob/master/program.md)

### Examples

| Task | Wrong | Right |
|------|-------|-------|
| Run tests | `pytest` (500 lines flood context) | `pytest > test.log 2>&1 && tail -n 20 test.log` |
| Check a metric | Read entire 10,000-line log | `grep "^accuracy:" run.log` |
| Debug a crash | `cat output.log` | `tail -n 50 output.log` |
| Build a project | `make` (scrolling build output) | `make > build.log 2>&1 && echo "exit: $?"` |
