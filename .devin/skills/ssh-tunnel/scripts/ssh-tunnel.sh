#!/usr/bin/env bash
set -euo pipefail

# ssh-tunnel: manage SSH port-forwarding tunnels
#
# Usage:
#   ssh-tunnel local  LOCAL_PORT REMOTE_HOST REMOTE_PORT SSH_DEST [SSH_OPTS...]
#   ssh-tunnel remote REMOTE_PORT LOCAL_HOST LOCAL_PORT  SSH_DEST [SSH_OPTS...]
#   ssh-tunnel socks  LOCAL_PORT                         SSH_DEST [SSH_OPTS...]
#   ssh-tunnel list
#   ssh-tunnel stop   PID|all
#   ssh-tunnel check  LOCAL_PORT

TUNNEL_DIR="${HOME}/.ssh/tunnels"
mkdir -p "$TUNNEL_DIR"

usage() {
    cat <<'EOF'
ssh-tunnel — manage SSH port-forwarding tunnels

Commands:
  local  LP RHOST RPORT DEST [SSH_OPTS]  Forward local LP to RHOST:RPORT via DEST
  remote RP LHOST LPORT DEST [SSH_OPTS]  Forward remote RP on DEST to LHOST:LPORT
  socks  LP DEST [SSH_OPTS]              SOCKS5 proxy on local LP via DEST
  list                                   Show active tunnels
  stop   PID|all                         Stop a tunnel (or all)
  check  PORT                            Test if a local port is responding

Examples:
  ssh-tunnel local  8080 localhost 80 user@server
  ssh-tunnel remote 8080 localhost 3000 user@server
  ssh-tunnel socks  1080 user@server
  ssh-tunnel local  5432 db.internal 5432 user@bastion -i ~/.ssh/key -p 2222
  ssh-tunnel list
  ssh-tunnel stop 12345
  ssh-tunnel stop all
  ssh-tunnel check 8080
EOF
    exit 1
}

_record_tunnel() {
    local pid=$1 mode=$2 spec=$3 dest=$4
    echo "${pid} ${mode} ${spec} ${dest} $(date -Iseconds)" > "${TUNNEL_DIR}/${pid}.tunnel"
}

_start_tunnel() {
    local mode=$1; shift
    local ssh_flag ssh_spec dest

    case "$mode" in
        local)
            [[ $# -lt 4 ]] && { echo "Error: local requires LOCAL_PORT REMOTE_HOST REMOTE_PORT SSH_DEST" >&2; exit 1; }
            local lport=$1 rhost=$2 rport=$3; shift 3
            dest=$1; shift
            ssh_flag="-L"
            ssh_spec="${lport}:${rhost}:${rport}"
            ;;
        remote)
            [[ $# -lt 4 ]] && { echo "Error: remote requires REMOTE_PORT LOCAL_HOST LOCAL_PORT SSH_DEST" >&2; exit 1; }
            local rport=$1 lhost=$2 lport=$3; shift 3
            dest=$1; shift
            ssh_flag="-R"
            ssh_spec="${rport}:${lhost}:${lport}"
            ;;
        socks)
            [[ $# -lt 2 ]] && { echo "Error: socks requires LOCAL_PORT SSH_DEST" >&2; exit 1; }
            local lport=$1; shift
            dest=$1; shift
            ssh_flag="-D"
            ssh_spec="${lport}"
            ;;
        *) usage ;;
    esac

    # Start the tunnel in background
    ssh -o StrictHostKeyChecking=accept-new \
        -o ServerAliveInterval=60 \
        -o ServerAliveCountMax=3 \
        -o ExitOnForwardFailure=yes \
        -o BatchMode=yes \
        ${ssh_flag} "${ssh_spec}" \
        -N -f \
        "$@" \
        "${dest}" 2>&1

    # Find the PID of the backgrounded ssh process
    local pid
    pid=$(pgrep -n -f "ssh.*${ssh_flag} ${ssh_spec}.*${dest}" 2>/dev/null || true)

    if [[ -z "$pid" ]]; then
        echo "Error: tunnel failed to start" >&2
        exit 1
    fi

    _record_tunnel "$pid" "$mode" "$ssh_spec" "$dest"

    echo "Tunnel started: ${mode} ${ssh_spec} via ${dest} (pid ${pid})"

    # For local/socks, test the port after a short delay
    if [[ "$mode" == "local" || "$mode" == "socks" ]]; then
        local test_port="${ssh_spec%%:*}"
        sleep 0.5
        if ss -tlnp 2>/dev/null | grep -q ":${test_port} " || \
           netstat -tlnp 2>/dev/null | grep -q ":${test_port} "; then
            echo "Port ${test_port} is listening"
        else
            echo "Warning: port ${test_port} not yet listening (tunnel may still be connecting)"
        fi
    fi
}

_list_tunnels() {
    local found=0
    shopt -s nullglob
    for f in "${TUNNEL_DIR}"/*.tunnel; do
        [[ -f "$f" ]] || continue
        read -r pid mode spec dest started < "$f"
        if kill -0 "$pid" 2>/dev/null; then
            printf "  pid=%-8s mode=%-8s spec=%-25s dest=%-30s started=%s\n" \
                "$pid" "$mode" "$spec" "$dest" "$started"
            found=1
        else
            rm -f "$f"
        fi
    done
    if [[ $found -eq 0 ]]; then
        echo "No active tunnels"
    fi
}

_stop_tunnel() {
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

_check_port() {
    local port=$1
    if curl -s --connect-timeout 2 "http://localhost:${port}/" > /dev/null 2>&1; then
        echo "Port ${port}: HTTP responding"
    elif (echo > /dev/tcp/localhost/${port}) 2>/dev/null; then
        echo "Port ${port}: TCP open (not HTTP)"
    else
        echo "Port ${port}: not responding"
    fi
}

# --- main ---

[[ $# -lt 1 ]] && usage

cmd=$1; shift

case "$cmd" in
    local|remote|socks) _start_tunnel "$cmd" "$@" ;;
    list|ls)            _list_tunnels ;;
    stop|kill)          [[ $# -lt 1 ]] && { echo "Error: stop requires PID or 'all'" >&2; exit 1; }; _stop_tunnel "$1" ;;
    check|test)         [[ $# -lt 1 ]] && { echo "Error: check requires PORT" >&2; exit 1; }; _check_port "$1" ;;
    -h|--help|help)     usage ;;
    *)                  echo "Unknown command: $cmd" >&2; usage ;;
esac
