# API Deployment

## Overview

Guide for deploying the CHaS API server itself.

## Deployment Options

### 1. Direct Installation

Install and run the API server directly on a host:

```bash
# Install dependencies
pip install fastapi uvicorn

# Start the API server
uvicorn main:app --host 0.0.0.0 --port 8080
```

### 2. Container Deployment

Deploy the API server as a container:

```bash
# Build API image
docker build -t chas-api:latest .

# Deploy via CHaS API (self-hosting)
curl -X POST http://localhost:8080/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "image": "chas-api:latest",
    "name": "chas-api-container",
    "exposed_ports": [{"container": 8080, "protocol": "tcp"}]
  }'
```

### 3. Systemd Service

Set up as a system service:

```bash
# Create systemd service file
sudo tee /etc/systemd/system/chas-api.service > /dev/null <<EOF
[Unit]
Description=CHaS API Server
After=network.target

[Service]
Type=simple
User=chas
WorkingDirectory=/opt/chas-api
ExecStart=/opt/chas-api/bin/uvicorn main:app --host 0.0.0.0 --port 8080
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl enable chas-api
sudo systemctl start chas-api
```

## Configuration

The API server can be configured via environment variables:

- `CHAS_API_PORT`: API server port (default: 8080)
- `CHAS_API_HOST`: API server host (default: 0.0.0.0)
- `LOG_LEVEL`: Logging level (default: info)