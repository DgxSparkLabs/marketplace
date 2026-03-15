# expose-port

Expose a local port to a public HTTPS URL. Like VSCode's automatic port forwarding, but for any remote session.

Uses [localhost.run](https://localhost.run) — free, no signup, just SSH.

## Usage

Invoke as a skill:

```
/expose-port 8080
```

Or run the script directly:

```bash
# Start a dev server
python3 -m http.server 8080 &

# Expose it
bash expose-port/scripts/expose-port.sh start 8080
# Output: Exposed port 8080 at: https://abc123.lhr.life

# List active tunnels
bash expose-port/scripts/expose-port.sh list

# Stop all tunnels
bash expose-port/scripts/expose-port.sh stop all
```

## Commands

| Command | Description |
|---------|-------------|
| `start PORT` | Expose port and print public URL |
| `list` | Show active tunnels with URLs |
| `stop PID\|all` | Stop tunnel(s) |
| `status PORT` | Check if something is listening on a port |

## How it works

The script creates an SSH reverse tunnel to `localhost.run`, which gives you a public HTTPS URL pointing to your local port. No account, no API key, no binary to install — it only needs `ssh`.

## Requirements

- OpenSSH client (`ssh`)
- An internet connection (for the SSH tunnel to localhost.run)
