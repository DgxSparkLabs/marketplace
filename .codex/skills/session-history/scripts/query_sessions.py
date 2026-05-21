# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Query the Devin CLI session history database.

Supports listing sessions, searching messages, reading full conversations,
and summarizing session activity.

The database is at ~/.local/share/devin/cli/sessions.db
"""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

DEFAULT_DB = Path.home() / ".local" / "share" / "devin" / "cli" / "sessions.db"


def get_db(db_path: str | None) -> sqlite3.Connection:
    path = Path(db_path) if db_path else DEFAULT_DB
    if not path.exists():
        print(f"Error: database not found at {path}", file=sys.stderr)
        print("Expected Devin CLI sessions database.", file=sys.stderr)
        sys.exit(1)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    return conn


def cmd_list(args):
    """List sessions, most recent first."""
    conn = get_db(args.db)
    limit = args.limit or 20
    rows = conn.execute(
        """
        SELECT id, title, model,
               datetime(created_at, 'unixepoch') as created,
               datetime(last_activity_at, 'unixepoch') as last_active,
               (SELECT count(*) FROM message_nodes m
                WHERE m.session_id = s.id
                  AND json_extract(m.chat_message, '$.role') IN ('user','assistant')) as msg_count
        FROM sessions s
        ORDER BY last_activity_at DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()

    if args.json_output:
        print(json.dumps([dict(r) for r in rows], indent=2))
        return

    for r in rows:
        title = r["title"] or "(untitled)"
        print(f"[{r['last_active']}] {title}")
        print(f"  id: {r['id']}")
        print(f"  model: {r['model']}  msgs: {r['msg_count']}")
        print()


def cmd_search(args):
    """Full-text search across all user and assistant messages."""
    conn = get_db(args.db)
    query = args.query
    limit = args.limit or 30
    role_filter = args.role

    sql = """
        SELECT m.session_id, s.title,
               json_extract(m.chat_message, '$.role') as role,
               json_extract(m.chat_message, '$.content') as content,
               datetime(m.created_at, 'unixepoch') as ts
        FROM message_nodes m
        JOIN sessions s ON s.id = m.session_id
        WHERE json_extract(m.chat_message, '$.role') IN ('user', 'assistant')
          AND json_extract(m.chat_message, '$.content') LIKE ?
    """
    params: list = [f"%{query}%"]

    if role_filter:
        sql += " AND json_extract(m.chat_message, '$.role') = ?"
        params.append(role_filter)

    sql += " ORDER BY m.created_at DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(sql, params).fetchall()

    if args.json_output:
        print(json.dumps([dict(r) for r in rows], indent=2))
        return

    if not rows:
        print(f"No results for '{query}'.")
        return

    print(f"Found {len(rows)} match(es) for '{query}':\n")
    for r in rows:
        title = r["title"] or "(untitled)"
        content = r["content"] or ""
        # Show a snippet around the match
        lower = content.lower()
        idx = lower.find(query.lower())
        start = max(0, idx - 80)
        end = min(len(content), idx + len(query) + 80)
        snippet = content[start:end].replace("\n", " ")
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."

        print(f"[{r['ts']}] ({r['role']}) in: {title}")
        print(f"  {snippet}")
        print()


def cmd_read(args):
    """Read the full conversation for a session."""
    conn = get_db(args.db)
    session_id = args.session_id

    # Resolve partial IDs
    if len(session_id) < 36:
        rows = conn.execute(
            "SELECT id FROM sessions WHERE id LIKE ?", (f"{session_id}%",)
        ).fetchall()
        if len(rows) == 0:
            print(f"No session found matching '{session_id}'.", file=sys.stderr)
            sys.exit(1)
        if len(rows) > 1:
            print(f"Ambiguous ID '{session_id}' matches {len(rows)} sessions:", file=sys.stderr)
            for r in rows:
                print(f"  {r['id']}", file=sys.stderr)
            sys.exit(1)
        session_id = rows[0]["id"]

    session = conn.execute(
        """SELECT title, model, datetime(created_at, 'unixepoch') as created,
                  datetime(last_activity_at, 'unixepoch') as last_active
           FROM sessions WHERE id = ?""",
        (session_id,),
    ).fetchone()

    if not session:
        print(f"Session {session_id} not found.", file=sys.stderr)
        sys.exit(1)

    messages = conn.execute(
        """
        SELECT json_extract(chat_message, '$.role') as role,
               json_extract(chat_message, '$.content') as content,
               datetime(created_at, 'unixepoch') as ts
        FROM message_nodes
        WHERE session_id = ?
          AND json_extract(chat_message, '$.role') IN ('user', 'assistant')
        ORDER BY node_id
        """,
        (session_id,),
    ).fetchall()

    if args.json_output:
        out = {
            "session": dict(session),
            "messages": [dict(m) for m in messages],
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    title = session["title"] or "(untitled)"
    print(f"# {title}")
    print(f"Model: {session['model']}  Created: {session['created']}")
    print(f"Messages: {len(messages)}")
    print("=" * 60)
    print()

    max_len = args.max_length or 2000
    for m in messages:
        role = m["role"].upper()
        content = m["content"] or ""
        if len(content) > max_len:
            content = content[:max_len] + f"\n... [truncated, {len(content)} chars total]"
        print(f"--- {role} [{m['ts']}] ---")
        print(content)
        print()


def cmd_stats(args):
    """Show summary statistics about the session database."""
    conn = get_db(args.db)

    total_sessions = conn.execute("SELECT count(*) as c FROM sessions").fetchone()["c"]
    total_messages = conn.execute("SELECT count(*) as c FROM message_nodes").fetchone()["c"]
    total_prompts = conn.execute("SELECT count(*) as c FROM prompt_history").fetchone()["c"]

    role_counts = conn.execute(
        """SELECT json_extract(chat_message, '$.role') as role, count(*) as c
           FROM message_nodes GROUP BY role ORDER BY c DESC"""
    ).fetchall()

    models = conn.execute(
        """SELECT model, count(*) as c FROM sessions GROUP BY model ORDER BY c DESC"""
    ).fetchall()

    first = conn.execute(
        "SELECT datetime(min(created_at), 'unixepoch') as d FROM sessions"
    ).fetchone()["d"]
    last = conn.execute(
        "SELECT datetime(max(last_activity_at), 'unixepoch') as d FROM sessions"
    ).fetchone()["d"]

    if args.json_output:
        print(json.dumps({
            "total_sessions": total_sessions,
            "total_messages": total_messages,
            "total_prompts": total_prompts,
            "role_counts": {r["role"]: r["c"] for r in role_counts},
            "models": {r["model"]: r["c"] for r in models},
            "first_session": first,
            "last_activity": last,
        }, indent=2))
        return

    print(f"Sessions:  {total_sessions}")
    print(f"Messages:  {total_messages}")
    print(f"Prompts:   {total_prompts}")
    print(f"First:     {first}")
    print(f"Last:      {last}")
    print()
    print("Messages by role:")
    for r in role_counts:
        print(f"  {r['role']:12s} {r['c']:>6d}")
    print()
    print("Sessions by model:")
    for r in models:
        print(f"  {r['model']:40s} {r['c']:>4d}")


def cmd_prompts(args):
    """List recent user prompts (the raw input history)."""
    conn = get_db(args.db)
    limit = args.limit or 30

    sql = "SELECT content, datetime(timestamp, 'unixepoch') as ts FROM prompt_history"
    params: list = []

    if args.query:
        sql += " WHERE content LIKE ?"
        params.append(f"%{args.query}%")

    sql += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(sql, params).fetchall()

    if args.json_output:
        print(json.dumps([dict(r) for r in rows], indent=2))
        return

    for r in rows:
        content = r["content"].replace("\n", " ")
        if len(content) > 120:
            content = content[:120] + "..."
        print(f"[{r['ts']}] {content}")


def main():
    parser = argparse.ArgumentParser(
        description="Query Devin CLI session history.",
    )
    parser.add_argument("--db", help=f"Path to sessions database (default: {DEFAULT_DB})")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Output as JSON")

    sub = parser.add_subparsers(dest="command", required=True)

    # list
    p_list = sub.add_parser("list", help="List recent sessions")
    p_list.add_argument("-n", "--limit", type=int, help="Number of sessions (default: 20)")
    p_list.set_defaults(func=cmd_list)

    # search
    p_search = sub.add_parser("search", help="Search across all messages")
    p_search.add_argument("query", help="Text to search for")
    p_search.add_argument("-n", "--limit", type=int, help="Max results (default: 30)")
    p_search.add_argument("--role", choices=["user", "assistant"], help="Filter by role")
    p_search.set_defaults(func=cmd_search)

    # read
    p_read = sub.add_parser("read", help="Read a full conversation")
    p_read.add_argument("session_id", help="Session ID (or unique prefix)")
    p_read.add_argument("--max-length", type=int, help="Max chars per message (default: 2000)")
    p_read.set_defaults(func=cmd_read)

    # stats
    p_stats = sub.add_parser("stats", help="Show database statistics")
    p_stats.set_defaults(func=cmd_stats)

    # prompts
    p_prompts = sub.add_parser("prompts", help="List recent user prompts")
    p_prompts.add_argument("query", nargs="?", help="Optional search filter")
    p_prompts.add_argument("-n", "--limit", type=int, help="Max results (default: 30)")
    p_prompts.set_defaults(func=cmd_prompts)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
