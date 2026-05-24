#!/usr/bin/env bash
set -euo pipefail

# Run GitHub Actions workflows locally using act + podman.
#
# Usage:
#   act-runner.sh run [workflow] [act-flags...]   Run a workflow
#   act-runner.sh dry-run [workflow]              Dry-run (no containers)
#   act-runner.sh list [workflow]                 List jobs in a workflow
#   act-runner.sh setup                           Install act, verify podman
#
# The script auto-installs act if missing and auto-detects the podman socket.

ACT_IMAGE="catthehacker/ubuntu:act-latest"
ACT_CACHE_DIR="${HOME}/.cache/act-runner"

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

die() { echo "Error: $*" >&2; exit 1; }

# --------------------------------------------------------------------------- #
# Locate or install act
# --------------------------------------------------------------------------- #

ensure_act() {
    if command -v act &>/dev/null; then
        ACT="act"
        return
    fi

    # Check common install locations
    for p in /tmp/act "${ACT_CACHE_DIR}/act" "${HOME}/.local/bin/act"; do
        if [[ -x "$p" ]]; then
            ACT="$p"
            return
        fi
    done

    echo "act not found — installing to ${ACT_CACHE_DIR}/act ..."
    mkdir -p "$ACT_CACHE_DIR"

    local arch
    arch=$(uname -m)
    local os
    os=$(uname -s)

    local arch_suffix
    case "$arch" in
        x86_64)  arch_suffix="x86_64" ;;
        aarch64) arch_suffix="arm64" ;;
        arm64)   arch_suffix="arm64" ;;
        *)       die "Unsupported architecture: $arch" ;;
    esac

    local os_suffix
    case "$os" in
        Linux)  os_suffix="Linux" ;;
        Darwin) os_suffix="Darwin" ;;
        *)      die "Unsupported OS: $os" ;;
    esac

    local url="https://github.com/nektos/act/releases/latest/download/act_${os_suffix}_${arch_suffix}.tar.gz"
    curl -fsSL "$url" | tar xz -C "$ACT_CACHE_DIR" act \
        || die "Failed to download act from $url"
    ACT="${ACT_CACHE_DIR}/act"
    echo "Installed $($ACT --version)"
}

# --------------------------------------------------------------------------- #
# Locate podman socket
# --------------------------------------------------------------------------- #

ensure_podman_socket() {
    command -v podman &>/dev/null || die \
        "podman is not installed. Install it with:\n  Debian/Ubuntu: sudo apt install podman\n  macOS: brew install podman"

    local user_socket="/run/user/$(id -u)/podman/podman.sock"
    local system_socket="/run/podman/podman.sock"

    # macOS podman machine socket
    local machine_socket="${HOME}/.local/share/containers/podman/machine/podman.sock"

    if [[ -S "$user_socket" ]]; then
        PODMAN_SOCKET="$user_socket"
    elif [[ -S "$system_socket" ]]; then
        PODMAN_SOCKET="$system_socket"
    elif [[ -S "$machine_socket" ]]; then
        PODMAN_SOCKET="$machine_socket"
    else
        echo "No podman socket found — starting podman system service ..."
        podman system service --time=0 &
        sleep 2
        if [[ -S "$user_socket" ]]; then
            PODMAN_SOCKET="$user_socket"
        else
            die "Could not find or start a podman socket.\nTry: systemctl --user start podman.socket"
        fi
    fi
}

# --------------------------------------------------------------------------- #
# Ensure actrc exists
# --------------------------------------------------------------------------- #

ensure_actrc() {
    local actrc="${HOME}/.config/act/actrc"
    if [[ ! -f "$actrc" ]]; then
        mkdir -p "$(dirname "$actrc")"
        echo "-P ubuntu-latest=${ACT_IMAGE}" > "$actrc"
        echo "Created $actrc with default image mapping"
    fi
}

# --------------------------------------------------------------------------- #
# Resolve workflow path
# --------------------------------------------------------------------------- #

resolve_workflow() {
    local arg="${1:-}"

    # Explicit path given
    if [[ -n "$arg" && -f "$arg" ]]; then
        echo "$arg"
        return
    fi

    # Check standard location
    local workflow_dir=".github/workflows"
    if [[ -n "$arg" && -f "${workflow_dir}/${arg}" ]]; then
        echo "${workflow_dir}/${arg}"
        return
    fi

    # Glob for yml/yaml
    if [[ -n "$arg" ]]; then
        # Could be a name without extension
        for ext in yml yaml; do
            if [[ -f "${workflow_dir}/${arg}.${ext}" ]]; then
                echo "${workflow_dir}/${arg}.${ext}"
                return
            fi
        done
        die "Workflow not found: $arg\nLooked in: ${workflow_dir}/"
    fi

    # No arg — use the workflow directory if it exists
    if [[ -d "$workflow_dir" ]]; then
        echo "$workflow_dir"
        return
    fi

    die "No .github/workflows/ directory found in the current project."
}

# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #

cmd_setup() {
    echo "=== act-runner setup ==="
    echo ""

    ensure_act
    echo "act:    $($ACT --version)"

    ensure_podman_socket
    echo "podman: $(podman --version)"
    echo "socket: ${PODMAN_SOCKET}"

    ensure_actrc

    echo ""
    echo "Ready. Run workflows with: act-runner.sh run"
}

cmd_list() {
    ensure_act
    ensure_podman_socket
    ensure_actrc

    local workflow
    workflow=$(resolve_workflow "${1:-}")
    shift 2>/dev/null || true

    echo "Jobs in ${workflow}:"
    echo ""

    DOCKER_HOST="unix://${PODMAN_SOCKET}" "$ACT" \
        --container-daemon-socket "$PODMAN_SOCKET" \
        -W "$workflow" \
        -l \
        "$@"
}

cmd_run() {
    ensure_act
    ensure_podman_socket
    ensure_actrc

    # First arg might be a workflow path, or an act flag
    local workflow_arg=""
    local -a extra_args=()

    if [[ $# -gt 0 && ! "$1" =~ ^- ]]; then
        workflow_arg="$1"
        shift
    fi
    extra_args=("$@")

    local workflow
    workflow=$(resolve_workflow "$workflow_arg")

    echo "Running ${workflow} via act + podman"
    echo "act:    $($ACT --version)"
    echo "socket: ${PODMAN_SOCKET}"
    echo ""

    DOCKER_HOST="unix://${PODMAN_SOCKET}" "$ACT" \
        --container-daemon-socket "$PODMAN_SOCKET" \
        -W "$workflow" \
        "${extra_args[@]+"${extra_args[@]}"}"
}

cmd_dry_run() {
    ensure_act
    ensure_podman_socket
    ensure_actrc

    local workflow_arg=""
    local -a extra_args=()

    if [[ $# -gt 0 && ! "$1" =~ ^- ]]; then
        workflow_arg="$1"
        shift
    fi
    extra_args=("$@")

    local workflow
    workflow=$(resolve_workflow "$workflow_arg")

    echo "Dry-running ${workflow} via act + podman"
    echo ""

    DOCKER_HOST="unix://${PODMAN_SOCKET}" "$ACT" \
        --container-daemon-socket "$PODMAN_SOCKET" \
        -W "$workflow" \
        -n \
        "${extra_args[@]+"${extra_args[@]}"}"
}

# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

usage() {
    cat <<'EOF'
Usage: act-runner.sh <command> [workflow] [options]

Commands:
  run [workflow] [flags...]   Run a workflow (default: all in .github/workflows/)
  dry-run [workflow]          Dry-run without containers
  list [workflow]             List jobs in a workflow
  setup                       Install act and verify podman

Examples:
  act-runner.sh run                              # run all workflows
  act-runner.sh run ci.yml                       # run a specific workflow
  act-runner.sh run ci.yml -j test               # run a specific job
  act-runner.sh run --secret GITHUB_TOKEN=ghp_x  # pass a secret
  act-runner.sh dry-run                          # validate workflows
  act-runner.sh list                             # show available jobs
  act-runner.sh setup                            # install act + verify podman

All extra flags are passed through to act.
EOF
}

COMMAND="${1:-run}"
shift 2>/dev/null || true

case "$COMMAND" in
    run)     cmd_run "$@" ;;
    dry-run) cmd_dry_run "$@" ;;
    list)    cmd_list "$@" ;;
    setup)   cmd_setup "$@" ;;
    -h|--help|help)
        usage
        exit 0
        ;;
    *)
        # If the first arg looks like a workflow path or act flag, treat it as "run"
        if [[ -f "$COMMAND" || "$COMMAND" =~ ^- || -f ".github/workflows/${COMMAND}" ]]; then
            cmd_run "$COMMAND" "$@"
        else
            echo "Unknown command: $COMMAND" >&2
            echo "" >&2
            usage >&2
            exit 1
        fi
        ;;
esac
