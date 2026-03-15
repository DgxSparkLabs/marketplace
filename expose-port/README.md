# expose-port

Expose a local port to a reachable address. Two backends:

- **localhost.run** — free, no signup, public HTTPS URL via SSH. HTTP only.
- **bore** — self-hosted TCP tunnel, any protocol (HTTP, SSH, databases, FTP, anything).

## Quick start

```bash
# Run interactive setup (installs bore, configures server)
bash expose-port/setup.sh

# Expose a port
bash expose-port/scripts/expose-port.sh start 8080
```

## Usage

Invoke as a skill:

```
/expose-port 8080
/expose-port 5432 --bore myserver.com
```

Or run the script directly:

```bash
# Start a dev server
python3 -m http.server 8080 &

# Expose via localhost.run (public HTTPS)
bash expose-port/scripts/expose-port.sh start 8080
# Output: Exposed port 8080 at: https://abc123.lhr.life

# Expose via bore (any TCP, self-hosted)
bash expose-port/scripts/expose-port.sh start 8080 --bore myserver.com
# Output: Exposed port 8080 at: myserver.com:54321

# List active tunnels
bash expose-port/scripts/expose-port.sh list

# Stop all tunnels
bash expose-port/scripts/expose-port.sh stop all
```

## Commands

| Command | Description |
|---------|-------------|
| `start PORT` | Expose port (uses localhost.run or bore if configured) |
| `start PORT --bore SERVER` | Expose via bore to a specific server |
| `start PORT --bore SERVER --secret SECRET` | Expose via bore with authentication |
| `start PORT --bore SERVER --bore-port PORT` | Request a specific remote port |
| `list` | Show active tunnels with URLs/addresses |
| `stop PID\|all` | Stop tunnel(s) |
| `status PORT` | Check if something is listening on a port |

## Backends

### localhost.run (default)

Creates an SSH reverse tunnel to [localhost.run](https://localhost.run), which gives you a public HTTPS URL pointing to your local port. No account, no API key, no binary to install.

**Requirements:** OpenSSH client, internet connection.

### bore

Connects to a self-hosted [bore](https://github.com/ekzhang/bore) server to create a TCP tunnel. Works with any protocol — not just HTTP.

**Requirements:** `bore` CLI binary ([install guide](https://github.com/ekzhang/bore#installation)), a bore server running somewhere reachable.

## Configuration

### Environment variables (preferred)

Set in `~/.auth/bore` and source it from your bashrc:

```bash
# ~/.auth/bore
export BORE_SERVER="myserver.com"
export BORE_SECRET="my-secret"
```

```bash
# ~/.bashrc (add this line)
[ -f ~/.auth/bore ] && source ~/.auth/bore
```

With these set, `start PORT` automatically uses bore — no flags needed.

### Config file (fallback)

`~/.config/expose-port/config` is sourced as a fallback for non-login shells:

```bash
BORE_SERVER="myserver.com"
BORE_SECRET="my-secret"
```

**Priority:** CLI flags > environment variables > config file.

## Setting up a bore server

See [docs/bore-server-setup.md](docs/bore-server-setup.md) for a step-by-step guide to running bore as a systemd service on a VPS or LAN gateway.

## As an Agent Skill

Copy this directory into your agent's skills directory:

```bash
# Global (available everywhere)
cp -r expose-port/ ~/.config/cognition/skills/expose-port/
# or: cp -r expose-port/ ~/.windsurf/skills/expose-port/

# Project-specific
cp -r expose-port/ /path/to/project/.cognition/skills/expose-port/
```

Then invoke with `/expose-port` in a session.
