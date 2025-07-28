# API Client

## CLI Tool

Install and configure the command-line client:

```bash
# Install CLI
wget https://github.com/your-org/chas-cli/releases/latest/download/chas-cli-linux-amd64
chmod +x chas-cli-linux-amd64
sudo mv chas-cli-linux-amd64 /usr/local/bin/chas-cli

# Configure API endpoint
export CHAS_API_URL=http://localhost:8080
```

## Basic Usage

```bash
# Deploy a container
chas-cli deploy --image nginx:latest --name web-server

# List nodes
chas-cli nodes list

# Register a node
chas-cli nodes register --node-id $(hostname)-node
```

## HTTP Client

Use any HTTP client to interact with the API:

```bash
# Deploy container with curl
curl -X POST http://localhost:8080/deploy \
  -H "Content-Type: application/json" \
  -d '{"image": "nginx:latest", "name": "web-server"}'
```

## Client Libraries

Client libraries are available for:
- Python
- JavaScript/Node.js
- Go

See the `/docs` endpoint for detailed API documentation.