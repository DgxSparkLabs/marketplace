# Setting up a bore server

[bore](https://github.com/ekzhang/bore) is a simple TCP tunnel tool. You run a **server** on a machine with a reachable IP (a VPS, a LAN gateway, a home server with port forwarding), and then **clients** connect to it to expose their local ports.

This guide walks through installing bore and running it as a systemd service.

## Prerequisites

- A machine with a public or LAN-reachable IP address
- SSH access with sudo
- Linux with systemd (Ubuntu, Debian, Fedora, Arch, etc.)

## 1. Install bore

```bash
ARCH=$(uname -m)
case "$ARCH" in
  x86_64)  BORE_ARCH="x86_64-unknown-linux-musl" ;;
  aarch64) BORE_ARCH="aarch64-unknown-linux-musl" ;;
  *)       echo "Unsupported architecture: $ARCH"; exit 1 ;;
esac

VERSION="0.6.0"
curl -L "https://github.com/ekzhang/bore/releases/download/v${VERSION}/bore-v${VERSION}-${BORE_ARCH}.tar.gz" \
  | sudo tar xz -C /usr/local/bin bore
chmod +x /usr/local/bin/bore
bore --version
```

## 2. Create a dedicated user

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
ExecStart=/usr/local/bin/bore server --min-port 1024
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

### Optional: require a shared secret

bore reads the `BORE_SECRET` environment variable automatically. Store it in a root-only file:

```bash
echo 'BORE_SECRET=your-random-secret-here' | sudo tee /etc/bore-server.env
sudo chmod 600 /etc/bore-server.env
```

Then add this line to the `[Service]` section:

```ini
EnvironmentFile=/etc/bore-server.env
```

Clients must pass `--secret` with the same value (or set `BORE_SECRET` in their environment).

## 4. Start and enable

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now bore-server
sudo systemctl status bore-server
```

Verify it's listening:

```bash
ss -tlnp | grep 7835
```

## 5. Open firewall ports

bore needs two port ranges:

| Port | Purpose |
|------|---------|
| 7835 | Control port (clients connect here) |
| 1024-65535 | Tunnel ports (one per active tunnel) |

**UFW:**
```bash
sudo ufw allow 7835/tcp
sudo ufw allow 1024:65535/tcp
```

**firewalld:**
```bash
sudo firewall-cmd --permanent --add-port=7835/tcp
sudo firewall-cmd --permanent --add-port=1024-65535/tcp
sudo firewall-cmd --reload
```

To narrow the tunnel range, set `--min-port` / `--max-port` in `ExecStart` and only open that range.

## 6. Test from a client

```bash
# On the client machine
python3 -m http.server 8080 &
bore local 8080 --to YOUR_SERVER_IP
# Output: listening at YOUR_SERVER_IP:XXXXX

# From any other machine
curl http://YOUR_SERVER_IP:XXXXX
```

Or using the expose-port skill:

```bash
expose-port start 8080 --bore YOUR_SERVER_IP
```

## Logs

```bash
sudo journalctl -u bore-server -f            # follow live
sudo journalctl -u bore-server --since today  # today's logs
```

## Updating bore

```bash
VERSION="0.6.1"  # check https://github.com/ekzhang/bore/releases
ARCH=$(uname -m)
case "$ARCH" in
  x86_64)  BORE_ARCH="x86_64-unknown-linux-musl" ;;
  aarch64) BORE_ARCH="aarch64-unknown-linux-musl" ;;
esac
curl -L "https://github.com/ekzhang/bore/releases/download/v${VERSION}/bore-v${VERSION}-${BORE_ARCH}.tar.gz" \
  | sudo tar xz -C /usr/local/bin bore
sudo systemctl restart bore-server
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Connection refused` on 7835 | Check firewall, verify `ss -tlnp \| grep 7835` |
| Client connects but tunnel port unreachable | Open the tunnel port range in firewall |
| `authentication failed` | Client and server secrets don't match |
| bore crashes on startup | `journalctl -u bore-server -e` |

## Network topology examples

```
# VPS as public relay
[Your machine] --bore--> [VPS with public IP] <-- [Anyone on internet]

# LAN gateway
[Machine A] --bore--> [Machine B: 192.168.1.1] <-- [Machine C: 192.168.1.50]

# Home server with router port forwarding
[Dev machine] --bore--> [Home server] <--port forward-- [Router] <-- [Internet]
                         (bore on 7835)                  (forward 7835 + tunnel range)
```
