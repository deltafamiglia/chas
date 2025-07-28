# Node Setup

## Prerequisites

- Linux system (Ubuntu 20.04+ or CentOS 8+)
- Root/sudo access
- Internet connectivity

## Quick Setup

Run the automated setup script:

```bash
# Download and run setup
curl -fsSL https://raw.githubusercontent.com/your-repo/chas/main/scripts/node-setup.sh | sudo bash

# Or run locally
sudo ./scripts/node-setup.sh
```

This installs:
- containerd (container runtime)
- nerdctl (Docker-compatible CLI)
- Python dependencies for node agent

## Node Registration

Register the node with the CHaS API server:

```bash
export CHAS_API_URL="http://your-chas-api-server:8080"
export NODE_ID="$(hostname)-node"
./scripts/register-node.sh
```

## Verification

Verify the installation:

```bash
# Check services
systemctl status containerd

# Test container execution
nerdctl run --rm alpine echo "Hello from CHaS node!"
```

## Troubleshooting

- **Permission errors**: Use sudo
- **Service failures**: Check logs with `journalctl -u containerd`
- **Container logs**: Use `nerdctl logs <container-name>`