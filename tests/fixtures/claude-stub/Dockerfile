# tests/fixtures/claude-stub/Dockerfile
#
# Standalone image that runs either of the two Anthropic-shape stubs
# (stub.py on 8088 for F5 sentinel observers, stub_body_dumper.py on 8089
# for F7/F9 request-body capture). Designed to run alongside the qa-claude
# `node:20` container so the operator's Claude session writes the entire
# request stream to a bind-mounted log file on the host.
#
# Composition pattern (from the repo root on the host):
#
#   mkdir -p .stub-logs
#
#   docker build -t claude-stub tests/fixtures/claude-stub/
#
#   # Stub container — note no `-p` port mapping needed for the primary
#   # workflow. qa-claude joins this container's network namespace below
#   # so 127.0.0.1:8089 inside qa-claude reaches Flask directly. Add
#   # `-p 8089:8089` only if you also want host-side curl access.
#   docker run --rm -d \
#     --name claude-stub \
#     -v "$PWD/.stub-logs:/var/log/stub" \
#     claude-stub
#
#   # Watch captured bodies live from the host:
#   tail -f .stub-logs/stub-bodies.log
#
#   # Compose with qa-claude sharing the stub's network namespace:
#   docker run --rm -it --name qa-claude \
#     --network container:claude-stub \
#     -v "$PWD:/workspace/marketplace" \
#     -w /workspace/marketplace \
#     -e ANTHROPIC_BASE_URL=http://127.0.0.1:8089 \
#     -e ANTHROPIC_AUTH_TOKEN=stub \
#     node:20 bash
#
# See tests/fixtures/claude-stub/README.md for the full operator workflow,
# including the Cursor-IDE port-conflict gotcha (a known Docker-Desktop +
# Cursor interaction that can break `-p` host port forwarding on Windows).

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /stub

# Copy both stub variants. Default CMD runs the body-dumper (most useful
# for QA); override on the docker run line to use the plain stub instead.
COPY stub.py stub_body_dumper.py ./

# Bind to 0.0.0.0 inside the container so `-p` mappings expose the port.
# 127.0.0.1 (the script default) is only reachable inside the same network namespace.
ENV STUB_HOST=0.0.0.0

# Write logs to a directory the operator bind-mounts to the host filesystem.
# Using /var/log/stub keeps it FHS-friendly and distinct from arbitrary /tmp paths.
ENV STUB_LOG=/var/log/stub/stub-server.log
ENV STUB_BODIES_LOG=/var/log/stub/stub-bodies.log

# Pre-create the dir so a bind mount of an empty host dir is harmless.
RUN mkdir -p /var/log/stub

# Both stubs listen on their script-default ports. EXPOSE is informational
# only — the `-p` mapping on the docker run line is what actually publishes
# the port to the host.
EXPOSE 8088 8089

# Default: run the body dumper on 8089. The stub uses PEP 723 inline
# metadata, so `uv run` fetches Flask on first invocation. Subsequent
# starts of the same image reuse the cached env.
#
# To run the plain stub instead (port 8088, no body capture, lighter):
#     docker run ... claude-stub uv run /stub/stub.py
CMD ["uv", "run", "/stub/stub_body_dumper.py"]
