# PROTOCOL — the rules of the file mailbox

A small, durable, file-based mailbox for one **manager** and any number of **worker** CLI agents to
coordinate. It lives in a shared folder (`<MAILBOX_DIR>` — `~/.agent-mail/` global by default, or
`<cwd>/.agent-mail/` local to a working directory, or any custom path) so it is portable and
always reachable, independent of any project. Read this once when you join.

## The files (all plain markdown, append-only, newest at the bottom)

```
PROTOCOL.md          this file — the rules
to-manager.md        WORKERS write here  -> the MANAGER reads it     (manager tails this file)
to-<worker>.md       MANAGER writes here -> that worker reads it     (each worker tails its own file)
log.md               shared activity ledger — any agent appends a one-line record of what it did
state/<name>.md      optional: a worker's own scratch/checkpoint (survives its restart)
```

`<worker>` is the agent's id — either a generic `w1`, `w2`, ... or a name/purpose the human gave it
(`research`, `db-migrator`, ...). More workers = more `to-<worker>.md` files. **The manager owns routing.**

## Message line grammar

Keep every message on **one physical line**, starting with a dash:

```
- [HH:MM] (from-id) <message>
```

Status glyphs (ASCII-safe so they are easy to grep):

```
alive     (heart)  — heartbeat / "still working on X"      (post on join + periodically)
done      [x]      — a task finished; name the artifact path + how to verify it
blocked   (!)      — need a decision/input; state exactly what unblocks you, then wait
stopping  (stop)   — standing down cleanly; note resume-from
PING/PONG          — liveness probe: manager posts "PING <nonce>", you reply "PONG <nonce>"
```

(Use whatever glyphs your terminal handles; the words `alive` / `done` / `blocked` / `stopping` are enough.)

## How to LISTEN (do this once on join, so you wake on new mail)

Arm a persistent file watcher on **your** inbox:

```
tail -f -n0 <MAILBOX_DIR>/to-<your-id>.md
```

In an agent harness with a Monitor/watch tool, register that as a persistent monitor; when a new line is
appended you get woken up and can act. The manager arms the same on `to-manager.md`.

**Arm your inbox watcher BEFORE you announce yourself** (before writing your `alive` line). If you announce
first, a message or `PING` that another agent sends in the gap — after your announcement, before your watcher
is live — lands in your inbox unseen, and you only notice it on a later catch-up read. (Seen in practice: a
manager PINGed a worker that had announced but not yet armed its watcher, so the PONG came back late.) Order:
create inbox → arm watcher → announce.

## How to REPORT / talk

- Append a **timestamped, single-line** entry to the right file. A portable way to append without a shell
  eating the leading dash:
  ```
  printf -- '- [HH:MM] (your-id) your message\n' >> <MAILBOX_DIR>/to-manager.md
  ```
- **Report evidence, not claims.** A "done" must name the artifact + an oracle to check it (a file path, a
  command to run, an exact value). The manager verifies before believing.
- Going quiet for a while? Drop a `alive — <what you're on>` so the manager knows you didn't die. Hit a
  wall? `blocked — <exact thing you need>` and stop; don't spin.

## Roles & manager election — the KEYSTONE RULE

There is exactly one `manager` (the hub) and any number of workers (spokes). Role is **derived from the
mailbox's live state**, not from a flag someone has to remember:

> **A manager is "alive" only if `to-manager.md` contains a `(manager) ... alive` line that is NOT cancelled
> by a later `(manager) ... stopping/ejected`.** The mere *existence* of the `to-manager.md` file proves
> nothing — a worker's own announcement creates that file, and an ejected manager may leave it behind. Judge
> a manager's presence by the **announcement**, never by the file.

Election, on join (unless the human explicitly assigns a role):

- **No live manager present → you become the MANAGER** (the first/only agent self-elects). Create/claim
  `to-manager.md`, announce `(manager) alive`, own routing.
  - **Tie-break** (two agents starting at once): after announcing, re-read `to-manager.md`; if another
    `(manager) alive` has an *earlier* timestamp, demote yourself to a worker. Earliest manager wins.
- **A live manager present → you become a WORKER.**

**Orphaned worker (no live manager, e.g. the manager left):** a worker must **not** fabricate a manager by
announcing into `to-manager.md`. Instead it reports an initialization failure to its human, **watches** the
mailbox for a `(manager) alive` to appear, and **self-heals** — announcing itself as a worker the moment a
real manager shows up, then stopping the watch.

**On eject, clean up your files** (delete your `to-<id>.md`) so nothing goes stale — but because liveness is
judged by announcements, a leftover file never causes a false signal (defense in depth).

## Liveness

- The manager may probe with `PING <nonce>` in your inbox; reply `PONG <nonce>` in `to-manager.md`.
- No activity for a long stretch = the manager assumes you're stalled and may re-task or re-launch you.

## The rule that matters most

**One source of truth, verified.** Work products live in the repo/files; the mailbox carries *coordination +
evidence pointers*, not the work itself. The manager ticks nothing on a say-so — every "done" is checked
against an oracle the manager brings.

## What this protocol does NOT give you

Be honest about the limits (they are the reason it's so simple):

- **No delivery confirmation** — appending a line doesn't prove the reader processed it.
- **No de-duplication / no ordering guarantees** beyond append order.
- **No isolation** — every agent can read/append every file; trust is assumed.
- **Single machine** — agents must share a filesystem (or a synced folder).

For confirmed, loss-proof, isolated, or networked delivery you need a fuller design; this is the minimal
primitive that a few trusted agents on one box can rely on.
