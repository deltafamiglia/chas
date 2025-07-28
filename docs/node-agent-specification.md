# Node Agent Specification

## Overview

The CHaS Node Agent is a lightweight service that runs on each worker node to manage containers and communicate with the CHaS API server. It replaces the need for nerdctl by providing a dedicated agent for container lifecycle management, resource monitoring, and health reporting.

## Architecture

The Node Agent consists of:

1. **Container Manager** - Interfaces with containerd for container operations
2. **Resource Monitor** - Tracks CPU, memory, and system health
3. **API Server** - HTTP server for receiving deployment requests
4. **Health Reporter** - Periodic health checks and status updates
5. **Registration Client** - Handles node registration with CHaS API

## Core Functionality

### Container Management

The Node Agent manages container lifecycle operations:

- **Deploy**: Create and start containers from images
- **Stop**: Gracefully stop running containers
- **Remove**: Clean up stopped containers
- **List**: Enumerate running containers
- **Logs**: Retrieve container logs
- **Status**: Report container health and status

### Resource Monitoring

Continuous monitoring of node resources:

- **CPU Usage**: Current CPU utilization percentage
- **Memory Usage**: Available and used memory
- **Disk Space**: Available storage for containers
- **Network**: Network interface status
- **Container Count**: Number of running containers

### Health Reporting

Regular health status updates to the CHaS API server:

- **Node Status**: Online/offline, healthy/unhealthy
- **Resource Availability**: Current resource utilization
- **Container Status**: Status of all managed containers
- **System Metrics**: Load average, uptime, errors

## API Interface

### Inbound API (Node Agent Server)

The Node Agent exposes HTTP endpoints for the CHaS API server:

#### POST /containers/deploy
Deploy a new container:
```json
{
  "image": "nginx:latest",
  "name": "web-server-1",
  "exposed_ports": [{"container": 80, "protocol": "tcp"}],
  "resources": {
    "cpu": "0.5",
    "memory": "512m"
  },
  "environment": {
    "ENV_VAR": "value"
  }
}
```

#### GET /containers
List all containers on this node:
```json
{
  "containers": [
    {
      "id": "abc123",
      "name": "web-server-1",
      "image": "nginx:latest",
      "status": "running",
      "ports": [{"host": 8080, "container": 80}]
    }
  ]
}
```

#### DELETE /containers/{container_id}
Stop and remove a container.

#### GET /containers/{container_id}/logs
Retrieve container logs.

#### GET /health
Node health and resource status:
```json
{
  "status": "healthy",
  "resources": {
    "cpu_usage": 25.5,
    "memory_usage": 60.2,
    "disk_available": "50GB",
    "container_count": 3
  },
  "uptime": 86400
}
```

### Outbound API (CHaS API Client)

The Node Agent communicates with the CHaS API server:

#### POST /nodes/register
Register this node with the CHaS cluster:
```json
{
  "node_id": "node-worker-1",
  "hostname": "worker-1.local",
  "ip_address": "192.168.1.10",
  "port": 9090,
  "resources": {
    "cpu_cores": 4,
    "memory_total": "8GB",
    "disk_total": "100GB"
  }
}
```

#### PUT /nodes/{node_id}/health
Periodic health updates to the CHaS API server.

## Configuration

### Environment Variables

- `CHAS_API_URL`: CHaS API server URL (required)
- `NODE_ID`: Unique node identifier (default: hostname)
- `NODE_PORT`: Port for Node Agent API server (default: 9090)
- `CONTAINERD_SOCKET`: Path to containerd socket (default: /run/containerd/containerd.sock)
- `HEALTH_INTERVAL`: Health reporting interval in seconds (default: 30)
- `LOG_LEVEL`: Logging level (default: INFO)

### Configuration File

Optional YAML configuration file at `/etc/chas/node-agent.yaml`:

```yaml
api:
  chas_url: "http://chas-api:8080"
  port: 9090
  
node:
  id: "worker-1"
  hostname: "worker-1.local"
  
containerd:
  socket: "/run/containerd/containerd.sock"
  namespace: "chas"
  
monitoring:
  health_interval: 30
  metrics_enabled: true
  
logging:
  level: "INFO"
  file: "/var/log/chas-node-agent.log"
```

## Installation Requirements

### System Dependencies

- Linux system (Ubuntu 20.04+ or CentOS 8+)
- containerd runtime
- Python 3.8+ or Go 1.19+
- systemd for service management

### Network Requirements

- Outbound access to CHaS API server
- Inbound access on configured port (default: 9090)
- Access to container registry for image pulls

## Service Management

### Systemd Service

The Node Agent runs as a systemd service:

```ini
[Unit]
Description=CHaS Node Agent
After=containerd.service
Requires=containerd.service

[Service]
Type=simple
ExecStart=/usr/local/bin/chas-node-agent
Restart=always
RestartSec=10
User=root

[Install]
WantedBy=multi-user.target
```

### Service Commands

```bash
# Start the service
systemctl start chas-node-agent

# Enable auto-start
systemctl enable chas-node-agent

# Check status
systemctl status chas-node-agent

# View logs
journalctl -u chas-node-agent -f
```

## Security Considerations

- **Authentication**: Secure communication with CHaS API server
- **Authorization**: Validate deployment requests
- **Network Security**: Firewall rules for Node Agent port
- **Container Isolation**: Proper containerd namespace isolation
- **Resource Limits**: Enforce container resource constraints

## Monitoring and Observability

### Metrics

The Node Agent exposes metrics for monitoring:

- Container deployment success/failure rates
- Resource utilization trends
- API request latency
- Health check status
- Error rates and types

### Logging

Structured logging with configurable levels:

- Container lifecycle events
- API requests and responses
- Health status changes
- Error conditions and recovery

## Migration from nerdctl

### Replaced Functionality

The Node Agent replaces these nerdctl operations:

- `nerdctl run` → Container deployment via API
- `nerdctl ps` → Container listing via API
- `nerdctl logs` → Log retrieval via API
- `nerdctl stop/rm` → Container management via API

### Benefits

- **Centralized Management**: All operations through CHaS API
- **Resource Awareness**: Integrated resource monitoring
- **Health Monitoring**: Automatic health reporting
- **Service Integration**: Native systemd service
- **Security**: Controlled access through API authentication
- **Observability**: Built-in metrics and logging

## Future Enhancements

- **Container Migration**: Move containers between nodes
- **Volume Management**: Persistent storage support
- **Network Policies**: Advanced networking features
- **Auto-scaling**: Dynamic resource adjustment
- **Multi-tenancy**: Namespace and quota management