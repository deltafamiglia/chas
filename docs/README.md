# CHaS Container Hosting System

Simple API-driven container hosting using containerd and nerdctl.

## Documentation

- **[MVP Overview](mvp-overview.md)** - System architecture and core concepts
- **[Node Setup](node-setup.md)** - Setting up container runtime nodes  
- **[API Specification](api-specification.md)** - REST API documentation
- **[API Client](api-client.md)** - Client tools and libraries
- **[Examples](examples.md)** - Usage examples and tutorials

## Quick Start

1. **Set up a node**: `sudo ./setup-node.sh`
2. **Start API server**: `uvicorn main:app --host 0.0.0.0 --port 8080`
3. **Deploy container**:
   ```bash
   curl -X POST http://localhost:8080/deploy \
     -H "Content-Type: application/json" \
     -d '{"image": "nginx:latest", "name": "web-server"}'
   ```

## Components

- **Node**: containerd + nerdctl runtime
- **API Server**: FastAPI service for container management  
- **Client**: CLI and libraries for API interaction

## Features

- Simple container deployment via REST API
- Docker-compatible interface (nerdctl)
- Automatic port allocation
- Self-hosting capability

---

**Next Steps**: Read the [MVP Overview](mvp-overview.md) then follow [Node Setup](node-setup.md).