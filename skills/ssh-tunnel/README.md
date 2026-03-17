# ssh-tunnel

Set up and manage SSH port-forwarding tunnels from the command line. Supports local forwarding, remote forwarding, and SOCKS proxies.

## Usage

Invoke as a skill:

```
/ssh-tunnel local 8080 localhost 80 user@server
```

Or run the script directly:

```bash
bash ssh-tunnel/scripts/ssh-tunnel.sh local  8080 localhost 80 user@server
bash ssh-tunnel/scripts/ssh-tunnel.sh remote 8080 localhost 3000 user@server
bash ssh-tunnel/scripts/ssh-tunnel.sh socks  1080 user@server
bash ssh-tunnel/scripts/ssh-tunnel.sh list
bash ssh-tunnel/scripts/ssh-tunnel.sh stop all
```

## Commands

| Command | Description |
|---------|-------------|
| `local LP RHOST RPORT DEST` | Forward local port to remote host via SSH |
| `remote RP LHOST LPORT DEST` | Expose local service on remote server |
| `socks LP DEST` | SOCKS5 proxy through SSH |
| `list` | Show active tunnels |
| `stop PID\|all` | Stop tunnel(s) |
| `check PORT` | Test if a local port responds |

## Quick reference

| I want to... | Mode | Example |
|--------------|------|---------|
| Access remote DB locally | `local` | `local 5432 db.internal 5432 user@bastion` |
| Show my local app to a server | `remote` | `remote 8080 localhost 3000 user@server` |
| Browse as if on remote network | `socks` | `socks 1080 user@server` |

## Requirements

- OpenSSH client (`ssh`)
- Key-based or agent-based SSH auth (the script uses `BatchMode=yes`)

## As an Agent Skill

Copy this directory into your agent's skills directory:

```bash
# Global (available everywhere)
cp -r ssh-tunnel/ ~/.config/cognition/skills/ssh-tunnel/
# or: cp -r ssh-tunnel/ ~/.windsurf/skills/ssh-tunnel/

# Project-specific
cp -r ssh-tunnel/ /path/to/project/.cognition/skills/ssh-tunnel/
```

Then invoke with `/ssh-tunnel` in a session.
