# Scheduler

## Overview

The scheduler automatically selects the best node for container deployment based on available resources.

## Scheduling Strategy

The scheduler uses a simple resource-based approach:

1. **Resource Check**: Evaluates CPU and memory availability on all nodes
2. **Node Selection**: Chooses the node with the most available resources
3. **Deployment**: Deploys the container on the selected node

## Scheduling Criteria

- **CPU Usage**: Prefers nodes with lower CPU utilization
- **Memory Usage**: Prefers nodes with more available memory
- **Node Health**: Only considers healthy, online nodes
- **Resource Requirements**: Ensures node can meet container resource needs

## Usage

Scheduling happens automatically when deploying containers:

```bash
curl -X POST http://localhost:8080/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "image": "nginx:latest",
    "name": "web-server",
    "resources": {
      "cpu": "0.5",
      "memory": "512m"
    }
  }'
```

The scheduler will automatically select the best available node for deployment.

## Future Enhancements

- Node affinity and anti-affinity rules
- Custom scheduling policies
- Resource prediction and planning