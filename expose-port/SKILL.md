---
name: expose-port
description: Expose a local port to a public HTTPS URL so the user can access it
argument-hint: "<port>"
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
  - model
---

# Expose Port

Expose a local port to a public HTTPS URL using localhost.run. No signup, no install — just SSH.

This is the equivalent of VSCode's automatic port forwarding for remote sessions.

## When to use this

Use this skill whenever:
- You start a dev server, preview server, or any HTTP service and the user needs to access it
- The user asks to see, preview, or test something you're running
- You're running on a remote machine and need to give the user a URL they can open in their browser

## Step 1: Start the service

Start whatever service needs to be accessible. For example:
```
python3 -m http.server 8080 --directory /path/to/site &
```

## Step 2: Expose the port

```
bash expose-port/scripts/expose-port.sh start PORT
```

Replace PORT with the port number the service is listening on.

The script will print a public HTTPS URL like `https://abc123.lhr.life` — give this URL to the user.

## Step 3: Tell the user

Present the URL clearly and tell them what it points to. For example:
> Your dev server is accessible at: https://abc123.lhr.life

## Management

```
bash expose-port/scripts/expose-port.sh list          # Show active tunnels with URLs
bash expose-port/scripts/expose-port.sh stop PID      # Stop a specific tunnel
bash expose-port/scripts/expose-port.sh stop all      # Stop all tunnels
bash expose-port/scripts/expose-port.sh status PORT   # Check if a port is listening
```

## Notes

- URLs are temporary — they change each time you start a new tunnel.
- The tunnel stays alive as long as the SSH connection is open.
- Free tier has no bandwidth or time limits but URLs are random hashes.
- Only works for HTTP/HTTPS services (not raw TCP).
- The tunnel adds TLS termination automatically — the public URL is always HTTPS even if the local service is HTTP.

User arguments: $ARGUMENTS
