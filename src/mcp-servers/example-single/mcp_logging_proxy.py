#!/usr/bin/env python3
"""mcp_logging_proxy.py — a transparent stdio logging proxy for MCP servers.

Sits between the MCP client (Claude Code) and a real MCP server, forwarding the
newline-delimited JSON-RPC stream in BOTH directions while appending every
message to a log file. This is the MCP analog of the LSP input log
(`example_lsp.py`): a "debug example" so an author can see exactly what the
client sends (`->`) and what the server replies (`<-`) — invaluable when
building or debugging your own MCP server.

It is protocol-agnostic: it only forwards bytes line-by-line (MCP stdio messages
are newline-delimited JSON and must not contain embedded newlines), so it cannot
corrupt the exchange — the real server's behavior is unchanged.

Usage:
  mcp_logging_proxy.py [--log PATH] [--name LABEL] -- <server-cmd> [args...]

Everything after the literal `--` is the real server command, launched as a
subprocess. With no --log, writes to ${TMPDIR:-/tmp}/mcp_proxy_<name>.log
(or set MCP_LOG to choose a path). Tail it to watch the wire live:

  tail -f /tmp/mcp_proxy_fetch.log
"""
import argparse
import os
import sys
import subprocess
import threading
import tempfile


def main():
    argv = sys.argv[1:]
    # Split on the first literal "--": everything after it is the server command.
    if "--" in argv:
        i = argv.index("--")
        pre, server_cmd = argv[:i], argv[i + 1:]
    else:
        pre, server_cmd = argv, []

    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--log", default=os.environ.get("MCP_LOG"))
    ap.add_argument("--name", default="mcp")
    opts, _ = ap.parse_known_args(pre)

    if not server_cmd:
        sys.stderr.write("mcp_logging_proxy: no server command given after '--'\n")
        return 2

    log_path = opts.log or os.path.join(
        tempfile.gettempdir(), "mcp_proxy_%s.log" % opts.name
    )
    logf = open(log_path, "a", buffering=1, encoding="utf-8", errors="replace")

    def log(direction, data):
        text = data.decode("utf-8", "replace").rstrip("\n") if isinstance(data, bytes) else str(data)
        logf.write("[%s] %s %s\n" % (opts.name, direction, text))

    log("##", "proxy start -> %s" % " ".join(server_cmd))

    try:
        proc = subprocess.Popen(server_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    except FileNotFoundError as e:
        log("##", "failed to launch server: %r" % e)
        sys.stderr.write("mcp_logging_proxy: cannot launch %r: %s\n" % (server_cmd, e))
        return 127

    def pump(src, dst, direction):
        try:
            for line in iter(src.readline, b""):
                log(direction, line)
                dst.write(line)
                dst.flush()
        except Exception as e:  # noqa: BLE001 — log and shut the pipe down
            log("##", "pump error (%s): %r" % (direction, e))
        finally:
            try:
                dst.close()
            except Exception:
                pass

    # client stdin -> server stdin  : "->" (requests/notifications from Claude)
    t_in = threading.Thread(
        target=pump, args=(sys.stdin.buffer, proc.stdin, "->"), daemon=True
    )
    # server stdout -> client stdout: "<-" (responses/notifications from the server)
    t_out = threading.Thread(
        target=pump, args=(proc.stdout, sys.stdout.buffer, "<-"), daemon=True
    )
    t_in.start()
    t_out.start()

    rc = proc.wait()
    log("##", "server exited rc=%s" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
