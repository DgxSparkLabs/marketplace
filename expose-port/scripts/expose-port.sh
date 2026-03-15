#!/usr/bin/env bash
set -euo pipefail

# expose-port: expose a local port to a public URL via localhost.run
#
# Usage:
#   expose-port start PORT
#   expose-port list
#   expose-port stop  PID|all
#   expose-port status PORT

TUNNEL_DIR="${HOME}/.local/share/expose-port"
mkdir -p "$TUNNEL_DIR"

usage() {
    cat <<'EOF'
expose-port — expose a local port to a public HTTPS URL

Uses localhost.run (free, no signup, SSH-based).

Commands:
  start  PORT           Expose PORT and print the public URL
  list                  Show active tunnels
  stop   PID|all        Stop a tunnel (or all)
  status PORT           Check if a port is listening locally

Examples:
  expose-port start 8080     # Get a public URL for localhost:8080
  expose-port start 3000     # Get a public URL for localhost:3000
  expose-port list            # Show active tunnels with URLs
  expose-port stop all        # Stop all tunnels
EOF
    exit 1
}

_record_tunnel() {
    local pid=$1 port=$2 url=$3
    echo "${pid} ${port} ${url} $(date -Iseconds)" > "${TUNNEL_DIR}/${pid}.tunnel"
}

_start() {
    local port=$1

    # Verify something is listening on the port
    if ! ss -tlnp 2>/dev/null | grep -q ":${port} "; then
        echo "Warning: nothing is listening on port ${port}" >&2
        echo "The tunnel will start but won't serve anything until a service binds to that port." >&2
    fi

    # Create a temp file to capture the tunnel output
    local logfile
    logfile=$(mktemp "${TUNNEL_DIR}/tunnel-XXXXXX.log")

    # Start the tunnel in background
    ssh -o StrictHostKeyChecking=accept-new \
        -o ServerAliveInterval=60 \
        -o ServerAliveCountMax=3 \
        -o ExitOnForwardFailure=yes \
        -o LogLevel=ERROR \
        -T -R "80:localhost:${port}" \
        nokey@localhost.run > "$logfile" 2>&1 &

    local tunnel_pid=$!

    # Wait for the URL to appear (up to 15 seconds)
    local url=""
    local waited=0
    while [[ $waited -lt 15 ]]; do
        sleep 1
        waited=$((waited + 1))

        # Check if process died
        if ! kill -0 "$tunnel_pid" 2>/dev/null; then
            echo "Error: tunnel process died" >&2
            cat "$logfile" >&2
            rm -f "$logfile"
            exit 1
        fi

        # Look for the URL in output
        url=$(grep -oE 'https://[a-z0-9]+\.lhr\.life' "$logfile" 2>/dev/null | head -1 || true)
        if [[ -n "$url" ]]; then
            break
        fi
    done

    rm -f "$logfile"

    if [[ -z "$url" ]]; then
        echo "Error: timed out waiting for public URL" >&2
        kill "$tunnel_pid" 2>/dev/null
        exit 1
    fi

    _record_tunnel "$tunnel_pid" "$port" "$url"

    echo "Exposed port ${port} at: ${url}"
    echo "Tunnel PID: ${tunnel_pid}"
    echo ""
    echo "Share this URL — it points to localhost:${port} on this machine."
}

_list() {
    local found=0
    shopt -s nullglob
    for f in "${TUNNEL_DIR}"/*.tunnel; do
        [[ -f "$f" ]] || continue
        read -r pid port url started < "$f"
        if kill -0 "$pid" 2>/dev/null; then
            printf "  pid=%-8s port=%-6s url=%-45s started=%s\n" \
                "$pid" "$port" "$url" "$started"
            found=1
        else
            rm -f "$f"
        fi
    done
    if [[ $found -eq 0 ]]; then
        echo "No active tunnels"
    fi
}

_stop() {
    local target=$1
    if [[ "$target" == "all" ]]; then
        local count=0
        shopt -s nullglob
        for f in "${TUNNEL_DIR}"/*.tunnel; do
            [[ -f "$f" ]] || continue
            read -r pid _ < "$f"
            if kill "$pid" 2>/dev/null; then
                echo "Stopped tunnel pid ${pid}"
                count=$((count + 1))
            fi
            rm -f "$f"
        done
        echo "Stopped ${count} tunnel(s)"
    else
        if kill "$target" 2>/dev/null; then
            echo "Stopped tunnel pid ${target}"
            rm -f "${TUNNEL_DIR}/${target}.tunnel"
        else
            echo "Error: no tunnel with pid ${target}" >&2
            exit 1
        fi
    fi
}

_status() {
    local port=$1
    if ss -tlnp 2>/dev/null | grep -q ":${port} "; then
        local proc
        proc=$(ss -tlnp 2>/dev/null | grep ":${port} " | grep -oP 'users:\(\("\K[^"]+' | head -1 || echo "unknown")
        echo "Port ${port}: listening (process: ${proc})"
    else
        echo "Port ${port}: nothing listening"
    fi
}

# --- main ---

[[ $# -lt 1 ]] && usage

cmd=$1; shift

case "$cmd" in
    start|expose)    [[ $# -lt 1 ]] && { echo "Error: start requires PORT" >&2; exit 1; }; _start "$1" ;;
    list|ls)         _list ;;
    stop|kill)       [[ $# -lt 1 ]] && { echo "Error: stop requires PID or 'all'" >&2; exit 1; }; _stop "$1" ;;
    status|check)    [[ $# -lt 1 ]] && { echo "Error: status requires PORT" >&2; exit 1; }; _status "$1" ;;
    -h|--help|help)  usage ;;
    *)               echo "Unknown command: $cmd" >&2; usage ;;
esac
