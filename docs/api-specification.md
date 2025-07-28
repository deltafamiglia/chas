# API Specification

## Overview

REST API for container deployment and management using FastAPI.

- **Base URL**: `http://localhost:8080`
- **Content-Type**: `application/json`
- **Documentation**: Available at `/docs`

## Core Endpoints

### POST /deploy
Deploy a container:
```bash
curl -X POST http://localhost:8080/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "image": "nginx:latest",
    "name": "web-server",
    "exposed_ports": [{"container": 80, "protocol": "tcp"}]
  }'
```

### GET /nodes
List all nodes:
```bash
curl http://localhost:8080/nodes
```

### POST /nodes/register
Register a new node:
```bash
curl -X POST http://localhost:8080/nodes/register \
  -H "Content-Type: application/json" \
  -d '{
    "node_id": "node-1",
    "hostname": "worker-1",
    "ip_address": "192.168.1.10"
  }'
```

## Additional Options

For detailed field descriptions and response formats, see the interactive documentation at `/docs`.