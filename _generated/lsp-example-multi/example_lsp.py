#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# ///
"""example_lsp — a minimal but REAL language server for Python and Markdown (stdlib only).

Unlike a formatter, this answers the questions an editor actually asks a language server,
so you can see what "LSP" means in practice:

  - publishDiagnostics : real problems
        Python   → syntax errors + undefined names (parsed with the `ast` module)
        Markdown → links pointing at headings that don't exist
  - documentSymbol     : the outline (Python: functions/classes; Markdown: headings)
  - definition         : jump to where a name is defined; in Markdown, from a [..](#h) link
                         to that heading
  - hover              : what is this symbol (function signature; heading level/slug)
  - references         : every use of a name (Python)

Claude Code feeds diagnostics to the model automatically after each edit, and reaches the
rest through its LSP tool ("go to the definition of X", "list the symbols", "find
references to Y"). Speaks LSP over stdio (JSON-RPC, Content-Length framing). No deps.

Usage:  example_lsp.py --lang {python,markdown}
"""
import sys
import json
import re
import ast
import argparse
import builtins
import os
import tempfile

WARNING, INFO = 2, 3
# LSP SymbolKind
SK_CLASS, SK_FUNCTION, SK_VARIABLE, SK_STRING = 5, 12, 13, 15


# ---------- LSP transport ----------
def read_message():
    headers = {}
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        line = line.decode("ascii").rstrip("\r\n")
        if line == "":
            break
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()
    n = int(headers.get("content-length", 0))
    return json.loads(sys.stdin.buffer.read(n).decode("utf-8"))


def write_message(msg):
    data = json.dumps(msg).encode("utf-8")
    sys.stdout.buffer.write(b"Content-Length: %d\r\n\r\n" % len(data))
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()


def rng(l0, c0, l1, c1):
    return {"start": {"line": l0, "character": c0}, "end": {"line": l1, "character": c1}}


# ---------- Python model (real analysis via ast) ----------
class PyModel:
    def __init__(self, text):
        self.lines = text.split("\n")
        self.syntax_error = None
        self.defs = {}        # name -> (line0, col0)  definition position
        self.detail = {}      # name -> hover detail string
        self.symbols = []     # DocumentSymbol[]
        self.uses = []        # (name, line0, col0, end0, is_load)
        self._build(text)

    def _name_col(self, line0, keyword):
        m = re.search(r"\b" + keyword + r"\s+(\w+)", self.lines[line0]) if 0 <= line0 < len(self.lines) else None
        return m.start(1) if m else 0

    def _build(self, text):
        try:
            tree = ast.parse(text)
        except SyntaxError as e:
            ln = (e.lineno or 1) - 1
            col = max((e.offset or 1) - 1, 0)
            self.syntax_error = (ln, col, "syntax error: " + (e.msg or ""))
            return
        defined = set(dir(builtins)) | {"self", "cls", "__name__", "__file__", "__doc__"}
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                kw = "def"
                col = self._name_col(node.lineno - 1, kw)
                args = [a.arg for a in node.args.args]
                self.defs[node.name] = (node.lineno - 1, col)
                self.detail[node.name] = "def %s(%s)" % (node.name, ", ".join(args))
                self.symbols.append(self._sym(node, node.name, SK_FUNCTION, col))
                defined.add(node.name)
                for a in node.args.args:
                    defined.add(a.arg)
            elif isinstance(node, ast.ClassDef):
                col = self._name_col(node.lineno - 1, "class")
                self.defs[node.name] = (node.lineno - 1, col)
                self.detail[node.name] = "class %s" % node.name
                self.symbols.append(self._sym(node, node.name, SK_CLASS, col))
                defined.add(node.name)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                for a in node.names:
                    nm = (a.asname or a.name).split(".")[0]
                    defined.add(nm)
                    self.defs.setdefault(nm, (node.lineno - 1, node.col_offset))
                    self.detail.setdefault(nm, "import %s" % nm)
            elif isinstance(node, ast.Name):
                end = node.col_offset + len(node.id)
                self.uses.append((node.id, node.lineno - 1, node.col_offset, end,
                                  isinstance(node.ctx, ast.Load)))
                if isinstance(node.ctx, (ast.Store,)):
                    defined.add(node.id)
                    self.defs.setdefault(node.id, (node.lineno - 1, node.col_offset))
                    self.detail.setdefault(node.id, "variable %s" % node.id)
        self._defined = defined

    def _sym(self, node, name, kind, namecol):
        l0 = node.lineno - 1
        end_l = getattr(node, "end_lineno", node.lineno) - 1
        end_c = getattr(node, "end_col_offset", namecol + len(name))
        return {"name": name, "kind": kind,
                "range": rng(l0, 0, end_l, end_c),
                "selectionRange": rng(l0, namecol, l0, namecol + len(name))}

    def diagnostics(self):
        if self.syntax_error:
            ln, col, msg = self.syntax_error
            return [{"range": rng(ln, col, ln, col + 1), "severity": WARNING,
                     "source": "example-lsp", "message": msg}]
        out = []
        for name, l0, c0, e0, is_load in self.uses:
            if is_load and name not in self._defined:
                out.append({"range": rng(l0, c0, l0, e0), "severity": WARNING,
                            "source": "example-lsp", "message": "undefined name '%s'" % name})
        return out

    def _name_at(self, line0, char):
        for name, l0, c0, e0, _ in self.uses:
            if l0 == line0 and c0 <= char < e0:
                return name
        for name, (l0, c0) in self.defs.items():
            if l0 == line0 and c0 <= char < c0 + len(name):
                return name
        return None

    def definition(self, uri, line0, char):
        name = self._name_at(line0, char)
        if name and name in self.defs:
            l0, c0 = self.defs[name]
            return {"uri": uri, "range": rng(l0, c0, l0, c0 + len(name))}
        return None

    def references(self, uri, line0, char):
        name = self._name_at(line0, char)
        if not name:
            return []
        out = []
        if name in self.defs:
            l0, c0 = self.defs[name]
            out.append({"uri": uri, "range": rng(l0, c0, l0, c0 + len(name))})
        for n, l0, c0, e0, _ in self.uses:
            if n == name:
                out.append({"uri": uri, "range": rng(l0, c0, l0, e0)})
        return out

    def hover(self, line0, char):
        name = self._name_at(line0, char)
        if name and name in self.detail:
            return "```python\n%s\n```" % self.detail[name]
        if name and name in dir(builtins):
            return "`%s` — Python builtin" % name
        return None


# ---------- Markdown model ----------
def md_slug(text):
    return re.sub(r"[^\w\s-]", "", text.lower()).strip().replace(" ", "-")


class MdModel:
    def __init__(self, text):
        self.lines = text.split("\n")
        self.headings = []   # (level, text, line0, slug)
        self.links = []      # (target, line0, c0, e0)
        for i, line in enumerate(self.lines):
            m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
            if m:
                self.headings.append((len(m.group(1)), m.group(2), i, md_slug(m.group(2))))
            for lm in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", line):
                self.links.append((lm.group(1), i, lm.start(), lm.end()))
        self.slugs = {h[3] for h in self.headings}

    def diagnostics(self):
        out = []
        for target, l0, c0, e0 in self.links:
            if target.startswith("#") and md_slug(target[1:]) not in self.slugs:
                out.append({"range": rng(l0, c0, l0, e0), "severity": WARNING,
                            "source": "example-lsp",
                            "message": "broken link: no heading '%s' in this file" % target})
        return out

    def symbols(self):
        return [{"name": "H%d %s" % (lvl, txt), "kind": SK_STRING,
                 "range": rng(l0, 0, l0, len(self.lines[l0])),
                 "selectionRange": rng(l0, 0, l0, len(self.lines[l0]))}
                for (lvl, txt, l0, slug) in self.headings]

    def _link_at(self, line0, char):
        for target, l0, c0, e0 in self.links:
            if l0 == line0 and c0 <= char < e0:
                return target
        return None

    def definition(self, uri, line0, char):
        target = self._link_at(line0, char)
        if target and target.startswith("#"):
            want = md_slug(target[1:])
            for lvl, txt, l0, slug in self.headings:
                if slug == want:
                    return {"uri": uri, "range": rng(l0, 0, l0, len(self.lines[l0]))}
        return None

    def hover(self, line0, char):
        for lvl, txt, l0, slug in self.headings:
            if l0 == line0:
                return "Heading level %d — link as `#%s`" % (lvl, slug)
        target = self._link_at(line0, char)
        if target:
            return "Link target: `%s`" % target
        return None


def model_for(lang, text):
    return PyModel(text) if lang == "python" else MdModel(text)


def apply_change(text, change):
    """Apply one LSP contentChange to the buffer. Full-sync changes have no 'range'
    (the whole document); incremental changes splice change['text'] over [start,end)."""
    if "range" not in change:
        return change["text"]
    lines = text.split("\n")
    def offset(p):
        return sum(len(lines[i]) + 1 for i in range(p["line"])) + p["character"]
    s = offset(change["range"]["start"])
    e = offset(change["range"]["end"])
    return text[:s] + change["text"] + text[e:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="python", choices=["python", "markdown"])
    ap.add_argument("--always-error", action="store_true",
                    help="emit one guaranteed marker diagnostic per file (observability)")
    ap.add_argument("--log", default=os.environ.get("EXAMPLE_LSP_LOG"),
                    help="append every received LSP message to this file (default: <tmp>/example_lsp.log)")
    args = ap.parse_args()
    lang = args.lang

    # Observability channel 1: log every message the client sends us to a file you can tail.
    log_path = args.log or os.path.join(tempfile.gettempdir(), "example_lsp.log")
    logf = open(log_path, "a", encoding="utf-8", buffering=1)
    logf.write("\n=== example_lsp started (lang=%s, always_error=%s, pid=%d) ===\n"
               % (lang, args.always_error, os.getpid()))
    seq = [0]

    def log_input(m):
        seq[0] += 1
        method = m.get("method", "(response)")
        payload = json.dumps(m.get("params", m.get("result", "")))
        if len(payload) > 300:
            payload = payload[:300] + "…(%d chars total)" % len(payload)
        logf.write("[%04d] %-32s %s\n" % (seq[0], method, payload))

    docs = {}
    texts = {}

    def publish(uri):
        # Observability channel 2: with --always-error, every file gets a guaranteed marker
        # diagnostic, so `Found N diagnostic issue` appears on EVERY edit regardless of content.
        diags = list(docs[uri].diagnostics())
        if args.always_error:
            diags.insert(0, {"range": rng(0, 0, 0, 1), "severity": WARNING, "source": "example-lsp",
                             "message": "example-lsp marker — file analyzed (always-on; event #%d)" % seq[0]})
        write_message({"jsonrpc": "2.0", "method": "textDocument/publishDiagnostics",
                       "params": {"uri": uri, "diagnostics": diags}})

    while True:
        msg = read_message()
        if msg is None:
            break
        log_input(msg)
        method = msg.get("method")
        mid = msg.get("id")

        if method == "initialize":
            write_message({"jsonrpc": "2.0", "id": mid, "result": {
                "capabilities": {
                    "textDocumentSync": {"openClose": True, "change": 2},
                    "documentSymbolProvider": True,
                    "definitionProvider": True,
                    "hoverProvider": True,
                    "referencesProvider": True,
                },
                "serverInfo": {"name": "example-lsp", "version": "1.0.0"},
            }})
        elif method == "shutdown":
            write_message({"jsonrpc": "2.0", "id": mid, "result": None})
        elif method == "exit":
            break
        elif method == "textDocument/didOpen":
            d = msg["params"]["textDocument"]
            texts[d["uri"]] = d["text"]
            docs[d["uri"]] = model_for(lang, d["text"])
            publish(d["uri"])
        elif method == "textDocument/didChange":
            uri = msg["params"]["textDocument"]["uri"]
            t = texts.get(uri, "")
            for ch in msg["params"]["contentChanges"]:
                t = apply_change(t, ch)
            texts[uri] = t
            docs[uri] = model_for(lang, t)
            publish(uri)
        elif method in ("textDocument/documentSymbol", "textDocument/definition",
                        "textDocument/hover", "textDocument/references"):
            params = msg["params"]
            uri = params["textDocument"]["uri"]
            m = docs.get(uri) or model_for(lang, "")
            if method == "textDocument/documentSymbol":
                result = m.symbols() if callable(getattr(m, "symbols", None)) else m.symbols
            else:
                pos = params["position"]
                line0, char = pos["line"], pos["character"]
                if method == "textDocument/definition":
                    result = m.definition(uri, line0, char)
                elif method == "textDocument/references":
                    result = m.references(uri, line0, char) if hasattr(m, "references") else []
                else:  # hover
                    h = m.hover(line0, char)
                    result = {"contents": {"kind": "markdown", "value": h}} if h else None
            write_message({"jsonrpc": "2.0", "id": mid, "result": result})
        # other notifications ignored


if __name__ == "__main__":
    main()
