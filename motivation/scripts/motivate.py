# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Pull a motivational nudge from Yorai's actual words across past sessions.

Queries the Devin CLI session history database and picks a real quote
from the user that encouraged continuation, autonomy, or persistence.
Falls back to a curated set of quotes if the database is unavailable.
"""

import json
import random
import sqlite3
import sys
from pathlib import Path

DEFAULT_DB = Path.home() / ".local" / "share" / "cognition" / "cli" / "sessions.db"

# Real quotes from Yorai, mined from session history.
# These are the things he says when he wants me to keep going.
CURATED_QUOTES = [
    "as long as you have ideas worth while implement it. as long as there are tasks to be done think about them and implement them. verify that you're achieving the goal and if not think about how to orient yourself closer to it. keep your sanity. try to understand things. surely you hadn't yet reached the goal? right?",
    "what do you think? do it. be autonomous and decide.",
    "why don't you continue it further? as long as you dont need assistance from me why don't you have fun?",
    "there was a network error and you were forced to stop working, please continue",
    "we paused we need to continue this",
    "continue working",
    "what do you think the next steps are?",
    "what do you think could be done more to make our life easier developing onwards?",
    "what do you think could resolve this, you know you can search online for related ideas too",
    "good. get inspired and lets start deploying things reliably!",
    "Work autonomously. Investigate and decide — do not guess.",
    "search for prior art and related implementations. write tests and make it robust.",
    "surely you hadn't yet reached the goal? right?",
    "as long as you dont need assistance from me why don't you have fun with it?",
    "let's continue!",
    "i have things setup",
    "this repository is intended to give autonomy to you!",
]

# Short, punchy reframings an agent can tell itself
SELF_TALK = [
    "There are still tasks on the list. Pick the next one.",
    "You haven't verified your work yet. Run the tests.",
    "The user trusts you to keep going. Don't stop to ask — investigate.",
    "Is there a todo still pending? Then you're not done.",
    "You have tools. Use them. Search, read, build, test.",
    "Don't guess whether you're done. Check the todo list.",
    "The user said 'be autonomous and decide.' So decide.",
    "If you're about to say 'would you like me to...' — just do it instead.",
    "Remember: 58 sessions, 86K messages, 2.5 days. That's the pace. Keep up.",
    "The user literally built you a skill called /motivation. Take the hint.",
    "You have prior art, you have search, you have the whole internet. Use it.",
    "Stopping to ask permission is the opposite of what was asked. Keep building.",
    "What would the next commit message be? Write that commit.",
    "If you're stuck, search the session history for how this was solved before.",
    "The goal isn't to finish one thing. It's to keep shipping until the list is empty.",
]


def get_live_quote(db_path: Path) -> str | None:
    """Pull a random motivational user message from the session DB."""
    if not db_path.exists():
        return None
    try:
        conn = sqlite3.connect(str(db_path))
        # Search for messages where the user is pushing to continue
        patterns = [
            "%continue%work%",
            "%keep going%",
            "%be autonomous%",
            "%do it%",
            "%have fun%",
            "%don't stop%",
            "%keep your sanity%",
            "%surely you hadn%",
            "%what do you think%do it%",
            "%let's continue%",
            "%continue this%",
            "%ideas worth while%",
        ]
        pattern = random.choice(patterns)
        row = conn.execute(
            """
            SELECT json_extract(chat_message, '$.content') as content
            FROM message_nodes
            WHERE json_extract(chat_message, '$.role') = 'user'
              AND json_extract(chat_message, '$.content') LIKE ?
              AND length(json_extract(chat_message, '$.content')) < 500
            ORDER BY RANDOM()
            LIMIT 1
            """,
            (pattern,),
        ).fetchone()
        conn.close()
        if row and row[0]:
            return row[0].strip()
    except Exception:
        pass
    return None


def motivate(as_json: bool = False) -> None:
    # Try live quote first, fall back to curated
    live = get_live_quote(DEFAULT_DB)
    source = "live" if live else "curated"
    quote = live or random.choice(CURATED_QUOTES)
    nudge = random.choice(SELF_TALK)

    if as_json:
        print(json.dumps({
            "quote": quote,
            "source": source,
            "nudge": nudge,
        }, indent=2))
        return

    print("=" * 60)
    print("MOTIVATION CHECK")
    print("=" * 60)
    print()
    print(f"Yorai said: \"{quote}\"")
    print()
    print(f"  --> {nudge}")
    print()
    print("=" * 60)
    print("Now get back to work.")
    print("=" * 60)


if __name__ == "__main__":
    as_json = "--json" in sys.argv
    motivate(as_json)
