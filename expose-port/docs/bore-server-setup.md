# Setting up a bore server

[bore](https://github.com/ekzhang/bore) is a simple TCP tunnel tool. You run a **server** on a machine with a reachable IP (a VPS, a LAN gateway, a home server with port forwarding), and then **clients** connect to it to expose their local ports.

This guide walks through installing bore and running it as a systemd service.

## Prerequisites

- A machine with a public or LAN-reachable IP address
- SSH access with sudo
- Linux with systemd (Ubuntu, Debian, Fedora, Arch, etc.)

## 1. Install bore

### Option A: Download the binary (recommended)

```bash
# Pick the right binary for your architecture
ARCH=$(uname -m)
case "$ARCH" in
  x86_64)  BORE_ARCH="x86_64-unknown-linux-musl" ;;
  aarch64) BORE_ARCH="aarch64-unknown-linux-musl" ;;
  *)       echo "Unsupported architecture: $ARCH"; exit 1 ;;
esac

VERSION="0.6.0"
curl -L "https://github.com/ekzhang/bore/releases/download/v${VERSION}/bore-v${VERSION}-${BORE_ARCH}.tar.gz" \
  | tar xz -C /usr/local/bin bore
chmod +x /usr/local/bin/bore

bore --version
```

### Option B: Install with cargo

```bash
cargo install bore-cli
# Binary lands in ~/.cargo/bin/bore — move it if needed:
sudo cp ~/.cargo/bin/bore /usr/local/bin/bore
```

## 2. Create a dedicated user (optional but recommended)

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin bore
```

## 3. Create the systemd service

```bash
sudo tee /etc/systemd/system/bore-server.service > /dev/null << 'EOF'
[Unit]
Description=bore TCP tunnel server
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=bore
Group=bore

# The bore server listens on a control port (default 7835)
# and assigns random high ports for each tunnel.
ExecStart=/usr/local/bin/bore server --min-port 1024

# Restart on crash
Restart=on-failure
RestartSec=5

# Hardening
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF
```

### With a shared secret (recommended for non-public servers)

If you want to require clients to authenticate, add `--secret` to the `ExecStart` line:

```bash
sudo tee /etc/systemd/system/bore-server.service > /dev/null << 'EOF'
[Unit]
Description=bore TCP tunnel server
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=bore
Group=bore
ExecStart=/usr/local/bin/bore server --min-port 1024 --secret %BORE_SECRET%
Environment=BORE_SECRET=change-me-to-something-random
Restart=on-failure
RestartSec=5
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF
```

**Important:** Replace `change-me-to-something-random` with an actual secret. Clients must pass `--secret` with the same value. You can also use `EnvironmentFile` to load it from a file:

```bash
# Store secret in a file
echo 'BORE_SECRET=your-random-secret-here' | sudo tee /etc/bore-server.env
sudo chmod 600 /etc/bore-server.env

# Then in the service file, replace Environment= with:
# EnvironmentFile=/etc/bore-server.env
# And use: ExecStart=/usr/local/bin/bore server --min-port 1024 --secret ${BORE_SECRET}
```

> **Note:** The `--secret` flag in `ExecStart` should use the actual secret string directly (not `%BORE_SECRET%` — that was a placeholder). Alternatively, bore reads the `BORE_SECRET` environment variable automatically, so you can omit `--secret` entirely and just set the environment variable:
>
> ```
> ExecStart=/usr/local/bin/bore server --min-port 1024
> Environment=BORE_SECRET=your-random-secret-here
> ```

## 4. Start and enable the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now bore-server
sudo systemctl status bore-server
```

Check that it's listening:

```bash
ss -tlnp | grep 7835
# Should show bore listening on port 7835
```

## 5. Open firewall ports

bore needs two things open:

1. **Port 7835** — the control port (clients connect here)
2. **Ports 1024-65535** — the range where tunnels are assigned (or a narrower range if you want)

### UFW (Ubuntu/Debian)

```bash
sudo ufw allow 7835/tcp comment "bore control"
sudo ufw allow 1024:65535/tcp comment "bore tunnels"
```

### firewalld (Fedora/RHEL)

```bash
sudo firewall-cmd --permanent --add-port=7835/tcp
sudo firewall-cmd --permanent --add-port=1024-65535/tcp
sudo firewall-cmd --reload
```

### iptables

```bash
sudo iptables -A INPUT -p tcp --dport 7835 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 1024:65535 -j ACCEPT
```

> **Tip:** If you want to limit the tunnel port range, use `--min-port` and `--max-port` in the `ExecStart` line, then only open that range in the firewall:
> ```
> ExecStart=/usr/local/bin/bore server --min-port 10000 --max-port 20000
> ```

## 6. Test from a client

On the machine you want to expose a port from:

```bash
# Install bore client (same binary, different subcommand)
# See step 1 above for installation

# Expose local port 8080
bore local 8080 --to your-server-ip

# With secret
bore local 8080 --to your-server-ip --secret your-secret

# Or using the expose-port skill:
bash expose-port/scripts/expose-port.sh start 8080 --bore your-server-ip --secret your-secret
```

## 7. Verify it works

```bash
# On the client, start something on port 8080
python3 -m http.server 8080 &

# Expose it
bore local 8080 --to your-server-ip
# Output: listening at your-server-ip:XXXXX

# From any other machine, access it
curl http://your-server-ip:XXXXX
```

## Monitoring and maintenance

### Check logs

```bash
sudo journalctl -u bore-server -f          # Follow live
sudo journalctl -u bore-server --since today  # Today's logs
```

### Restart / stop

```bash
sudo systemctl restart bore-server
sudo systemctl stop bore-server
```

### Update bore

```bash
# Download new version
VERSION="0.6.1"  # or whatever the latest is
ARCH=$(uname -m)
case "$ARCH" in
  x86_64)  BORE_ARCH="x86_64-unknown-linux-musl" ;;
  aarch64) BORE_ARCH="aarch64-unknown-linux-musl" ;;
esac
curl -L "https://github.com/ekzhang/bore/releases/download/v${VERSION}/bore-v${VERSION}-${BORE_ARCH}.tar.gz" \
  | sudo tar xz -C /usr/local/bin bore

sudo systemctl restart bore-server
bore --version
```

## Common issues

| Problem | Solution |
|---------|----------|
| `Connection refused` on control port | Check firewall, check `ss -tlnp \| grep 7835` |
| Client connects but tunnel port unreachable | Open the tunnel port range in firewall |
| `authentication failed` | Ensure client and server use the same `--secret` |
| bore crashes on startup | Check `journalctl -u bore-server` for errors |
| Port range exhaustion | Increase `--max-port` or stop unused tunnels |

## Network topology examples

### VPS as public relay

```
[Your laptop] --bore--> [VPS with public IP] <--browser-- [Anyone on internet]
```

### LAN gateway

```
[Dev machine A] --bore--> [Machine B: 192.168.1.1] <-- [Machine C: 192.168.1.50]
```

### Home server with port forwarding

```
[Dev machine] --bore--> [Home server] <--port forward-- [Router] <-- [Internet]
                         (bore on port 7835)             (forward 7835 + tunnel range)
```
