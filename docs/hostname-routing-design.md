# Hostname Routing Design

## Overview

CHaS automatically assigns unique hostnames to deployed containers for easy access and routing.

## Hostname Generation

Hostnames are generated using the pattern:
```
{container-name}.{environment}.{domain}
```

Examples:
- `web-server.prod.chas.local`
- `api-service.staging.chas.local`

## Features

- **Automatic Assignment**: Hostnames generated automatically during deployment
- **Environment Separation**: Different environments get different subdomains
- **DNS Integration**: Hostnames resolve to container endpoints
- **Load Balancing**: Multiple containers with same hostname are load-balanced

## Usage

Specify environment during deployment:

```bash
curl -X POST http://localhost:8080/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "image": "nginx:latest",
    "name": "web-server",
    "environment_label": "prod",
    "exposed_ports": [{"container": 80, "protocol": "tcp"}]
  }'
```

The container will be accessible at `web-server.prod.chas.local`.