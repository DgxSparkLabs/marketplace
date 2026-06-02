# lsp-example-multi

Reference plugin for the **multi-LSP layout**: one plugin ships two Language Server
configurations (`markdown`, `python`) in one `lsp-config.json`. Unlike the single
counterpart (which points at an externally-installed `marksman`), **these two servers are
bundled and self-contained** — they run `example_lsp.py`, a dependency-free stdlib language
server shipped inside the plugin. No language toolchain to install, nothing to download:
install the plugin and it works (only `uv` is required on PATH).

## What it does — a real (minimal) language server

`example_lsp.py` answers the questions an editor actually asks a language server — it is not
a formatter. The Python side parses with the stdlib `ast` module; the Markdown side parses
headings and links.

| Capability (LSP method) | Python | Markdown |
|---|---|---|
| **diagnostics** (`publishDiagnostics`) | syntax errors + undefined names | links pointing at non-existent headings |
| **document symbols** (`documentSymbol`) | functions & classes | heading outline |
| **go-to-definition** (`definition`) | name → its `def`/assignment | `[..](#h)` link → that heading |
| **hover** (`hover`) | function signature / kind | heading level + slug |
| **references** (`references`) | every use of a name | — |

## How Claude Code uses it

Claude Code **auto-feeds** `publishDiagnostics` to the model after each edit, and reaches
the navigation features (symbols / definition / hover / references) through its **LSP
tool** when the model asks ("go to the definition of X", "list the symbols"). It never
requests `textDocument/formatting`, so the server reports problems as diagnostics rather
than rewriting files. (See `docs/TEST_YOURSELF.md` cell 4.8.7 and `PITFALLS.md`.)

Two facts that trip people up (both documented in `PITFALLS.md`):

- **Reading a file does not attach the LSP** — only an Edit/Write sends `textDocument/didOpen`
  (anthropics/claude-code#16804). Ask Claude to *edit* the file, not just read it.
- **Claude sends incremental `didChange`** (a range + the edited fragment, not the whole
  file), so the server keeps the document buffer and applies each change — see
  `apply_change()`. A handler that assumed "full document every change" silently published
  zero diagnostics after the first edit.

## Observability — two ways to watch it work

This example runs with `--always-error` and input logging on, so you can *see* it working
through two independent channels (handy when learning what an LSP does, or debugging your own):

1. **It always emits a diagnostic.** Every file the server analyzes gets a guaranteed marker —
   `example-lsp marker — file analyzed (always-on; event #N)` — on top of any real findings. So
   in Claude you see `⎿ Found N new diagnostic issue` on **every** edit, even a clean file. (Real
   findings like `undefined name 'x'` still appear alongside the marker.)
2. **It logs every message it receives.** The server appends each LSP message it gets
   (`initialize`, `didOpen`, incremental `didChange`, …) to a file you can tail:
   ```bash
   tail -f "${TMPDIR:-/tmp}/example_lsp.log"     # or set EXAMPLE_LSP_LOG=/path to choose
   ```
   You watch the client talk to the server in real time — including the incremental `didChange`
   `range`s that a naive server gets wrong.

Both are example-only conveniences. To make this behave like a production LSP (markers off),
remove `--always-error` from `lsp-config.json`; logging is harmless and can stay.

## File walkthrough

```
src/lsp-servers/example-multi/
├── .claude-plugin/plugin.json    ← lspServers → ./lsp-config.json
├── lsp-config.json               ← markdown + python entries; command: uv run ${CLAUDE_PLUGIN_ROOT}/example_lsp.py
├── example_lsp.py                ← the bundled stdio language server (stdlib only)
└── README.md
```

`${CLAUDE_PLUGIN_ROOT}` expands to the installed plugin directory, so the config locates the
bundled script wherever the plugin lands. `--no-project` keeps `uv` from latching onto the
user's current project environment.

## Try it (the observable QA loop)

```bash
# 1. uv must be on the PATH of the shell that launches claude:
which uv || curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. install the plugin (auto-enables on CLI >= 2.1.157):
claude plugin install lsp-example-multi@dgxsparklabs-marketplace --scope project

# 3. make a file with a real bug:
printf 'def add(a, b):\n    return a + b\n\nprint(undefined_var)\n' > calc.py

# 4. launch claude --debug, then EDIT the file (a Read will NOT trigger the LSP):
claude --debug
```

In a second shell, watch for the diagnostic **event** (not the `pending` counter, which
almost always polls as 0 even on success):

```bash
tail -f ~/.claude/debug/<session>.txt | grep --line-buffered -iE 'lsp server|publishdiagnostics|received diagnostics'
```

In the `claude` session, type this prompt **exactly** (verbatim — explicit so the model just
makes the edit instead of asking what to add):

> Use the Edit tool to append the comment line # lsp test as the last line of calc.py. Do not ask questions, just make the edit.

Accept the edit (press Enter). Expect `Starting LSP server instance: …:python` → `Received
notification 'textDocument/publishDiagnostics'` → `Received diagnostics … 1 diagnostic(s)`.
Diagnostics attach to the model's NEXT turn, so type exactly:

> List verbatim the language-server diagnostics shown to you for calc.py, with line numbers.

The model surfaces `undefined name 'undefined_var' (example-lsp)` on the `print(undefined_var)`
line. For the navigation features, type exactly `Use the LSP to list the symbols defined in
calc.py.` or `Use the LSP go-to-definition to tell me which line the function add is defined
on.`

## When to choose multi over single

- **multi** (this): ship several servers in one plugin — here, two bundled, self-contained
  language servers for a polyglot, install-free demo.
- **single** (`src/lsp-servers/example-single/`): one server, pointed at an externally
  installed binary (`marksman`) — the reference for wiring a real production LSP.

## Related

- Adding your own LSP plugin: `docs/ADDING_A_CONSTRUCT.md`
- Verification walkthrough: `docs/TEST_YOURSELF.md` cell 4.8.7
