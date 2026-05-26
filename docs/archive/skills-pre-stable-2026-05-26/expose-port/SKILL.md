---
name: expose-port
description: Expose a local port via HTTPS (localhost.run) or TCP (bore)
argument-hint: "<port> [--bore SERVER]"
allowed-tools:
  - exec
  - Bash
  - read
  - Read
permissions:
  allow:
    - Exec(bash)
    - Exec(ssh)
    - Exec(bore)
    - Exec(curl)
    - Exec(ss)
triggers:
  - user
  - model
---

# Expose Port

Expose a local port so the user (or other machines) can reach it. Two backends:

- **localhost.run** (default) — free, SSH-based, gives a public HTTPS URL. HTTP only.
- **bore** — self-hosted, any TCP protocol (FTP, SSH, databases, HTTP, anything).

## When to use this

- You start a dev server, preview, or any service and the user needs to access it
- The user asks to see, preview, or test something running on a port
- You need to expose a non-HTTP service (database, FTP, custom TCP)

## Expose via localhost.run (HTTPS, no setup)

```
bash $SKILL_DIR/scripts/expose-port.sh start PORT
```

Returns a URL like `https://abc123.lhr.life`. Only works for HTTP services.

## Expose via bore (any TCP protocol)

```
bash $SKILL_DIR/scripts/expose-port.sh start PORT --bore SERVER_IP
bash $SKILL_DIR/scripts/expose-port.sh start PORT --bore SERVER_IP --secret SECRET
bash $SKILL_DIR/scripts/expose-port.sh start PORT --bore SERVER_IP --bore-port 15432
```

Returns an address like `SERVER_IP:PORT` plus a clickable `http://SERVER_IP:PORT` URL. Works with any TCP protocol.

If `BORE_SERVER` is set (via `~/.auth/bore` or env), the `--bore` flag is not needed:
```
bash $SKILL_DIR/scripts/expose-port.sh start PORT
```

## Management

```
bash $SKILL_DIR/scripts/expose-port.sh list          # Show active tunnels
bash $SKILL_DIR/scripts/expose-port.sh stop PID      # Stop a tunnel
bash $SKILL_DIR/scripts/expose-port.sh stop all      # Stop all tunnels
bash $SKILL_DIR/scripts/expose-port.sh status PORT   # Check if port is listening
```

## Choosing a backend

| Need | Backend | Example |
|------|---------|---------|
| Share a web app with anyone on the internet | localhost.run | `start 3000` |
| Access a DB from another LAN machine | bore | `start 5432 --bore 192.168.1.1` |
| Expose FTP to the network | bore | `start 21 --bore 10.0.0.1` |
| SSH into this machine from another | bore | `start 22 --bore gateway.local` |

User arguments: $ARGUMENTS
