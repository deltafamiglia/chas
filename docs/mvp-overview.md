# CHaS MVP Overview

## Architecture

CHaS is a simple container hosting system with these components:

1. **Nodes** - Machines running containerd/node-agent
2. **API Server** - FastAPI service for container management
3. **Scheduler** - Selects optimal nodes for deployment
4. **Ingress** - Load balancer and traffic router
5. **Client** - CLI and programmatic interfaces

### Infrastructure Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CHaS Infrastructure                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐                                                            │
│  │   Ingress   │ ◄──── Load Balancer & Service Discovery                    │
│  │ Router/LB   │                                                            │
│  └──────┬──────┘                                                            │
│         │ Internal API                                                      │
│         ▼                                                                   │
│  ┌─────────────┐      ┌─────────────┐                                       │
│  │ API Server  │◄────►│  Scheduler  │ ◄──── Control Plane                   │
│  │   FastAPI   │      │ Node Select │                                       │
│  └──────┬──────┘      └─────────────┘                                       │
│         │ Container Management                                              │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         Node Cluster                                │    │
│  │                                                                     │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │    │
│  │  │   Node 1    │  │   Node 2    │  │   Node 3    │  │   Node N   │  │    │
│  │  │             │  │             │  │             │  │            │  │    │
│  │  │ containerd  │  │ containerd  │  │ containerd  │  │ containerd │  │    │
│  │  │ node-agent  │  │ node-agent  │  │ node-agent  │  │ node-agent │  │    │
│  │  │             │  │             │  │             │  │            │  │    │
│  │  │ [Container] │  │ [Container] │  │ [Container] │  │ [Container]│  │    │
│  │  │ [Container] │  │ [Container] │  │             │  │            │  │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘  │    │
│  │                                                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

Network Connections:
• Client ←→ Ingress: HTTP/HTTPS requests
• API Server ←→ Ingress: Configuration of routing  
• API Server ←→ Scheduler: Resource allocation requests
• API Server ←→ Nodes: Container deployment & management
• Nodes ←→ Ingress: Service registration & health checks
• Ingress ←→ Containers: Load balanced traffic routing
```

## Deployment Flow

1. Client sends request to API server via ingress
2. Scheduler selects optimal node based on resources
3. API server deploys container on selected node
4. Ingress registers container for load balancing
5. Client receives deployment status and port info

## Key Features

- Multi-node container deployment
- Automatic resource-based scheduling
- Load balancing and service discovery
- API-driven container management via node agents
- Self-hosting capability
- Interactive API documentation

## MVP Limitations

- No persistent storage or health monitoring
- No advanced scheduling or auto-scaling
- No network policies or security isolation
- No container migration or multi-region support

## Future Enhancements

- Health monitoring and auto-healing
- Advanced scheduling policies
- Persistent storage management
- Web UI and enhanced observability