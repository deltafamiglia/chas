# Ingress

## Overview

The ingress component provides hostname-based routing and load balancing for deployed containers.

## Features

- **Hostname Routing**: Each deployment gets a unique hostname
- **Load Balancing**: Distributes traffic across multiple container instances
- **Health Checking**: Monitors container health and removes unhealthy instances
- **Service Discovery**: Automatically discovers and routes to new containers

## Load Balancing Strategies

- **Round Robin**: Distributes requests evenly across backends
- **Least Connections**: Routes to backend with fewest active connections
- **IP Hash**: Routes same client IP to same backend

## Configuration

Ingress is configured automatically when containers are deployed with exposed ports. No manual configuration required for basic usage.

## Usage

Deploy a container and it will automatically be available via ingress:

```bash
curl -X POST http://localhost:8080/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "image": "nginx:latest",
    "name": "web-server",
    "exposed_ports": [{"container": 80, "protocol": "tcp"}]
  }'
```

The container will be accessible via its assigned hostname and load-balanced automatically.