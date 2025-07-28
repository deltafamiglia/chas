# Examples

## Basic Container Deployment

Deploy a simple web server:

```bash
curl -X POST http://localhost:8080/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "image": "nginx:latest",
    "name": "web-server",
    "exposed_ports": [{"container": 80, "protocol": "tcp"}]
  }'
```

## Self-Hosting Example

Deploy the CHaS API itself as a container:

```bash
# Build API image
docker build -t chas-api:latest .

# Deploy API as container
curl -X POST http://localhost:8080/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "image": "chas-api:latest",
    "name": "chas-api-container",
    "exposed_ports": [{"container": 8080, "protocol": "tcp"}]
  }'
```

## Multi-Container Application

Deploy a web app with database:

```bash
# Deploy database
curl -X POST http://localhost:8080/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "image": "postgres:13",
    "name": "app-db",
    "environment": {"POSTGRES_PASSWORD": "secret"}
  }'

# Deploy web app
curl -X POST http://localhost:8080/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "image": "myapp:latest",
    "name": "web-app",
    "exposed_ports": [{"container": 3000, "protocol": "tcp"}],
    "environment": {"DATABASE_URL": "postgres://app-db:5432/myapp"}
  }'
```

## Using the CLI

```bash
# Deploy with CLI
chas-cli deploy --image nginx:latest --name web-server --expose 80:tcp

# List deployments
chas-cli containers list

# Check node status
chas-cli nodes list
```