#!/usr/bin/env bash
set -euo pipefail

# expose-port: expose a local port via localhost.run (HTTP) or bore (TCP)
#
# Usage:
#   expose-port start PORT [--bore SERVER] [--bore-port RPORT] [--secret S]
#   expose-port list
#   expose-port stop  PID|all
#   expose-port status PORT

TUNNEL_DIR="${HOME}/.local/share/expose-port"
mkdir -p "$TUNNEL_DIR"

# Environment variables (BORE_SERVER, BORE_SECRET) are expected to be set
# in ~/.auth/bore and sourced by bashrc.  The config file below is a fallback.
CONF="${HOME}/.config/expose-port/config"
AUTH="${HOME}/.auth/bore"

_load_config() {
    # Defaults — environment variables (from ~/.auth/bore) take priority,
    # then config file, then empty.
    local env_server="${BORE_SERVER:-}"
    local env_secret="${BORE_SECRET:-}"

    BORE_SERVER=""
    BORE_SECRET=""
    BORE_PORT="0"

    # Source auth file if present (in case we're in a non-login shell)
    if [[ -f "$AUTH" ]]; then
        # shellcheck source=/dev/null
        source "$AUTH"
    fi

    # Source config file for any extra settings (BORE_PORT, etc.)
    if [[ -f "$CONF" ]]; then
        # shellcheck source=/dev/null
        source "$CONF"
    fi

    # Env vars that were already set before sourcing win
    [[ -n "$env_server" ]] && BORE_SERVER="$env_server" || true
    [[ -n "$env_secret" ]] && BORE_SECRET="$env_secret" || true
}

usage() {
    cat <<'EOF'
expose-port — expose a local port to a reachable URL

Backends:
  localhost.run   Free SSH-based, HTTPS only (default)
  bore            Self-hosted, any TCP protocol (FTP, SSH, DB, HTTP, ...)

Commands:
  start  PORT [options]   Expose PORT and print the reachable address
  list                    Show active tunnels
  stop   PID|all          Stop a tunnel (or all)
  status PORT             Check if a port is listening locally

Start options:
  --bore SERVER           Use bore backend, connect to SERVER (ip or hostname)
  --bore-port PORT        Request a specific remote port (default: auto)
  --secret SECRET         Bore authentication secret

Examples:
  expose-port start 8080                                   # HTTPS via localhost.run
  expose-port start 8080 --bore 192.168.2.100              # TCP via bore server
  expose-port start 5432 --bore bore.example.com --bore-port 15432
  expose-port start 21 --bore 10.0.0.1 --secret mysecret   # FTP via bore
  expose-port list
  expose-port stop all

Environment variables (preferred — set in ~/.auth/bore, sourced by bashrc):
    export BORE_SERVER="192.168.2.100"
    export BORE_SECRET="my-secret"

Config file (~/.config/expose-port/config — fallback):
    BORE_SERVER="192.168.2.100"
    BORE_SECRET="my-secret"

Priority: CLI flags > env vars > config file
EOF
    exit 1
}

_record_tunnel() {
    local pid=$1 port=$2 url=$3 backend=$4
    echo "${pid} ${port} ${url} ${backend} $(date -Iseconds)" > "${TUNNEL_DIR}/${pid}.tunnel"
}

# ---------------------------------------------------------------------------
# localhost.run backend (HTTP/HTTPS only)
# ---------------------------------------------------------------------------
_start_localhost_run() {
    local port=$1
    local logfile
    logfile=$(mktemp "${TUNNEL_DIR}/tunnel-XXXXXX.log")

    ssh -o StrictHostKeyChecking=accept-new \
        -o ServerAliveInterval=60 \
        -o ServerAliveCountMax=3 \
        -o ExitOnForwardFailure=yes \
        -o LogLevel=ERROR \
        -T -R "80:localhost:${port}" \
        nokey@localhost.run > "$logfile" 2>&1 &

    local tunnel_pid=$!
    local url="" waited=0
    while [[ $waited -lt 15 ]]; do
        sleep 1
        waited=$((waited + 1))
        if ! kill -0 "$tunnel_pid" 2>/dev/null; then
            echo "Error: tunnel process died" >&2
            cat "$logfile" >&2
            rm -f "$logfile"
            exit 1
        fi
        url=$(grep -oE 'https://[a-z0-9]+\.lhr\.life' "$logfile" 2>/dev/null | head -1 || true)
        [[ -n "$url" ]] && break
    done
    rm -f "$logfile"

    if [[ -z "$url" ]]; then
        echo "Error: timed out waiting for public URL" >&2
        kill "$tunnel_pid" 2>/dev/null
        exit 1
    fi

    _record_tunnel "$tunnel_pid" "$port" "$url" "localhost.run"
    echo "Exposed port ${port} at: ${url}"
    echo "Tunnel PID: ${tunnel_pid}"
    echo "Backend: localhost.run (HTTPS only)"
}

# ---------------------------------------------------------------------------
# bore backend (any TCP)
# ---------------------------------------------------------------------------
_start_bore() {
    local port=$1 server=$2 remote_port=$3 secret=$4

    if ! command -v bore &>/dev/null; then
        echo "Error: bore is not installed." >&2
        echo "Install: curl -sL https://github.com/ekzhang/bore/releases/latest/download/bore-v0.6.0-\$(uname -m)-unknown-linux-musl.tar.gz | tar xz -C ~/.local/bin/" >&2
        exit 1
    fi

    local logfile
    logfile=$(mktemp "${TUNNEL_DIR}/tunnel-XXXXXX.log")

    local bore_args=("local" "$port" "--to" "$server")
    [[ "$remote_port" != "0" ]] && bore_args+=("--port" "$remote_port")
    [[ -n "$secret" ]] && bore_args+=("--secret" "$secret")

    bore "${bore_args[@]}" > "$logfile" 2>&1 &
    local tunnel_pid=$!

    # Wait for bore to connect and report the listening address
    local remote_addr="" waited=0
    while [[ $waited -lt 10 ]]; do
        sleep 1
        waited=$((waited + 1))
        if ! kill -0 "$tunnel_pid" 2>/dev/null; then
            echo "Error: bore process died" >&2
            cat "$logfile" >&2
            rm -f "$logfile"
            exit 1
        fi
        # bore logs: "listening at SERVER:PORT"
        remote_addr=$(grep -oP 'listening at \K\S+' "$logfile" 2>/dev/null | head -1 || true)
        [[ -n "$remote_addr" ]] && break
    done
    rm -f "$logfile"

    if [[ -z "$remote_addr" ]]; then
        echo "Error: timed out waiting for bore to connect" >&2
        kill "$tunnel_pid" 2>/dev/null
        exit 1
    fi

    _record_tunnel "$tunnel_pid" "$port" "$remote_addr" "bore"
    echo "Exposed port ${port} at: ${remote_addr}"
    echo "Tunnel PID: ${tunnel_pid}"
    echo "Backend: bore (TCP — works with any protocol)"
}

# ---------------------------------------------------------------------------
# Shared commands: list, stop, status
# ---------------------------------------------------------------------------
_list() {
    local found=0
    shopt -s nullglob
    for f in "${TUNNEL_DIR}"/*.tunnel; do
        [[ -f "$f" ]] || continue
        read -r pid port url backend started < "$f"
        if kill -0 "$pid" 2>/dev/null; then
            printf "  pid=%-8s port=%-6s %-10s url=%-45s started=%s\n" \
                "$pid" "$port" "[${backend}]" "$url" "$started"
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

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
[[ $# -lt 1 ]] && usage
cmd=$1; shift

case "$cmd" in
    start|expose)
        [[ $# -lt 1 ]] && { echo "Error: start requires PORT" >&2; exit 1; }
        local_port=$1; shift

        _load_config

        # Parse options
        bore_server="${BORE_SERVER}"
        bore_port="${BORE_PORT}"
        bore_secret="${BORE_SECRET}"

        while [[ $# -gt 0 ]]; do
            case "$1" in
                --bore)       bore_server="$2"; shift 2 ;;
                --bore-port)  bore_port="$2"; shift 2 ;;
                --secret)     bore_secret="$2"; shift 2 ;;
                *)            echo "Unknown option: $1" >&2; exit 1 ;;
            esac
        done

        # Verify something is listening
        if ! ss -tlnp 2>/dev/null | grep -q ":${local_port} "; then
            echo "Warning: nothing is listening on port ${local_port}" >&2
        fi

        if [[ -n "$bore_server" ]]; then
            _start_bore "$local_port" "$bore_server" "$bore_port" "$bore_secret"
        else
            _start_localhost_run "$local_port"
        fi
        ;;
    list|ls)        _list ;;
    stop|kill)      [[ $# -lt 1 ]] && { echo "Error: stop requires PID or 'all'" >&2; exit 1; }; _stop "$1" ;;
    status|check)   [[ $# -lt 1 ]] && { echo "Error: status requires PORT" >&2; exit 1; }; _status "$1" ;;
    -h|--help|help) usage ;;
    *)              echo "Unknown command: $cmd" >&2; usage ;;
esac
