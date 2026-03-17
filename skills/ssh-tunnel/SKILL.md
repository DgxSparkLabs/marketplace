---
name: ssh-tunnel
description: Set up SSH port forwarding tunnels (local, remote, SOCKS proxy)
argument-hint: "<mode> <args...>"
allowed-tools:
  - exec
  - read
permissions:
  allow:
    - Exec(bash)
    - Exec(ssh)
    - Exec(curl)
    - Exec(ss)
triggers:
  - user
---

# SSH Tunnel

Set up and manage SSH port-forwarding tunnels.

## The script

```
bash ssh-tunnel/scripts/ssh-tunnel.sh <command> <args...>
```

## Tunnel types

### Local forwarding (`-L`)

Makes a remote service accessible on a local port. Traffic flows: **your machine -> SSH server -> target**.

```
bash ssh-tunnel/scripts/ssh-tunnel.sh local LOCAL_PORT REMOTE_HOST REMOTE_PORT SSH_DEST [SSH_OPTS...]
```

Use when: you want to access a database, web app, or service that's only reachable from the SSH server's network.

Example — access a Postgres database behind a bastion:
```
bash ssh-tunnel/scripts/ssh-tunnel.sh local 5432 db.internal 5432 user@bastion
# Now connect to localhost:5432 as if it were db.internal:5432
```

### Remote forwarding (`-R`)

Makes a local service accessible from the remote server. Traffic flows: **remote server -> SSH tunnel -> your machine**.

```
bash ssh-tunnel/scripts/ssh-tunnel.sh remote REMOTE_PORT LOCAL_HOST LOCAL_PORT SSH_DEST [SSH_OPTS...]
```

Use when: you want to expose a local dev server to a remote machine (e.g., show a coworker your local app, or let a CI server reach your machine).

Example — expose local dev server on the remote host:
```
bash ssh-tunnel/scripts/ssh-tunnel.sh remote 8080 localhost 3000 user@server
# On the server, localhost:8080 now reaches your local port 3000
```

### SOCKS proxy (`-D`)

Creates a local SOCKS5 proxy that routes all traffic through the SSH server.

```
bash ssh-tunnel/scripts/ssh-tunnel.sh socks LOCAL_PORT SSH_DEST [SSH_OPTS...]
```

Use when: you want to browse the web or make requests as if you were on the remote server's network.

Example:
```
bash ssh-tunnel/scripts/ssh-tunnel.sh socks 1080 user@server
# Configure browser/app to use SOCKS5 proxy at localhost:1080
# Or: curl --socks5-hostname localhost:1080 http://internal-site.example.com
```

## Management

```
bash ssh-tunnel/scripts/ssh-tunnel.sh list          # Show active tunnels
bash ssh-tunnel/scripts/ssh-tunnel.sh stop PID      # Stop a specific tunnel
bash ssh-tunnel/scripts/ssh-tunnel.sh stop all      # Stop all tunnels
bash ssh-tunnel/scripts/ssh-tunnel.sh check PORT    # Test if a port is responding
```

## Extra SSH options

Pass additional SSH flags after the destination:

```
bash ssh-tunnel/scripts/ssh-tunnel.sh local 8080 localhost 80 user@server -i ~/.ssh/mykey -p 2222
```

Common options:
- `-i KEY` — use a specific SSH key
- `-p PORT` — connect to SSH on a non-standard port
- `-J JUMP` — use a jump/bastion host

## When the user asks for help

- If they say "forward a port" or "tunnel" without specifying a type, ask which service they want to reach and from where. Then pick local vs remote.
- If they want to "access something on a remote network", that's **local** forwarding.
- If they want to "expose a local service", that's **remote** forwarding.
- If they want to "proxy traffic" or "browse as if on another network", that's **SOCKS**.
- Always verify the tunnel works with `check` after starting it.

User arguments: $ARGUMENTS
