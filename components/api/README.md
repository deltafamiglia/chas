# API Endpoints Schema
"""
POST /api/v1/agents/
Request: RegisterRequest
Response: RegisterResponse

POST /api/v1/agents/{agent_id}/sync
Request: SyncRequest  
Response: SyncResponse

GET /api/v1/agents/{agent_id}/status
Response: AgentStatus

DELETE /api/v1/agents/{agent_id}
Response: {"success": bool, "message": str}
"""

# Example Usage for Testing

```python
from typing import List, Dict, Any
from pydantic import BaseModel, Field

# Sync Response (API -> Agent)
class SyncResponse(BaseModel):
    success: bool
    desired_containers: List[ContainerConfig]
    poll_interval: int = 30
    global_config: Dict[str, Any] = Field(default_factory=dict)  # Global settings
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    
example_register_request = RegisterRequest(
    agent_id="agent-001",
    hostname="docker-host-01",
    capabilities=AgentCapabilities(
        cpu_cores=8,
        memory_gb=32.0,
        available_ports="8000-8100,9000-9100",
        docker_networks=["bridge", "host"],
        nerdctl_version="1.7.0"
    )
)

example_sync_request = SyncRequest(
    agent_id="agent-001",
    timestamp=datetime.utcnow(),
    resources=AgentResources(
        cpu_used=2.4,
        memory_used_gb=8.2,
        available_ports="8010-8100,9000-9100",
        running_containers=3
    ),
    containers=[
        ContainerStatus(
            service_id="web-app-v1",
            container_id="abc123",
            container_name="web-app-v1-abc123",
            status=ContainerState.RUNNING,
            health=HealthStatus.HEALTHY,
            ports={"80": 8080, "443": 8443},
            cpu_usage=0.3,
            memory_mb=256,
            started_at=datetime.utcnow()
        )
    ]
)

example_sync_response = SyncResponse(
    success=True,
    desired_containers=[
        ContainerConfig(
            service_id="web-app-v1",
            state=ContainerState.RUNNING,
            image="nginx",
            tag="1.24",
            ports={"80": 0, "443": 0},  # Auto-assign ports
            environment={"ENV": "production", "LOG_LEVEL": "info"},
            resources={"memory": "512m", "cpus": "0.5"},
            volumes=["/var/log/nginx:/var/log/nginx:rw"],
            labels={"app": "web", "version": "v1"}
        ),
        ContainerConfig(
            service_id="api-v2",
            state=ContainerState.RUNNING,
            image="myapp/api",
            tag="v2.1.0",
            ports={"3000": 0},
            environment={"DATABASE_URL": "postgresql://..."},
            resources={"memory": "1g", "cpus": "1.0"},
            restart_policy="always"
        )
    ],
    poll_interval=15
)
```
