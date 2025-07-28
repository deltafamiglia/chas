# Node Setup

This guide covers setting up CHaS worker nodes with the node agent. For detailed information about the node agent architecture and API, see the [Node Agent Specification](node-agent-specification.md).

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
- CHaS node agent (container management service)
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
systemctl status chas-node-agent

# Test node agent API
curl http://localhost:9090/health

# Check node registration
curl $CHAS_API_URL/nodes
```

## Troubleshooting

- **Permission errors**: Use sudo
- **Service failures**: Check logs with `journalctl -u containerd` or `journalctl -u chas-node-agent`
- **Node agent issues**: Check status with `systemctl status chas-node-agent`
- **Container logs**: Use the node agent API: `curl http://localhost:9090/containers/{container_id}/logs`
- **API connectivity**: Verify `CHAS_API_URL` is accessible and node is registered