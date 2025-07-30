"""
API Schema for Docker Agent Management System
Compatible with nerdcli container management
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime, UTC
from enum import Enum


class ContainerState(str, Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    PAUSED = "paused"
    RESTARTING = "restarting"


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    STARTING = "starting"
    UNKNOWN = "unknown"


# Agent Registration
class AgentCapabilities(BaseModel):
    cpu_cores: int
    memory_gb: float
    docker_networks: List[str] = Field(default_factory=list)
    nerdctl_version: Optional[str] = None


class RegisterRequest(BaseModel):
    agent_id: str
    hostname: str
    capabilities: AgentCapabilities
    version: str = "1.0"


class RegisterResponse(BaseModel):
    success: bool
    message: str
    poll_interval: int = 30  # seconds


# Container Status Reporting
class ContainerStatus(BaseModel):
    service_id: str
    container_id: Optional[str] = None  # None if container doesn't exist
    container_name: Optional[str] = None
    status: ContainerState
    health: HealthStatus = HealthStatus.UNKNOWN
    ports: Dict[str, int] = Field(default_factory=dict)  # {"80": 8080, "443": 8443}
    cpu_usage: Optional[float] = None  # CPU usage percentage
    memory_mb: Optional[int] = None
    started_at: Optional[datetime] = None
    error_message: Optional[str] = None


class AgentResources(BaseModel):
    cpu_used: float  # Number of CPU cores in use
    memory_used_gb: float
    running_containers: int
    load_average: Optional[float] = None


# Sync Request (Agent -> API)
class SyncRequest(BaseModel):
    agent_id: str
    timestamp: datetime
    resources: AgentResources
    containers: List[ContainerStatus]
    nerdctl_events: Optional[List[Dict[str, Any]]] = Field(default_factory=list)


# Desired Container Configuration
class ContainerConfig(BaseModel):
    service_id: str
    state: ContainerState
    image: str
    tag: str = "latest"

    # Port mapping: container_port -> host_port (0 = auto-assign)
    ports: Dict[str, int] = Field(default_factory=dict)

    # Environment variables
    environment: Dict[str, str] = Field(default_factory=dict)

    # Resource limits (nerdctl format)
    resources: Dict[str, str] = Field(default_factory=dict)  # {"memory": "512m", "cpus": "0.5"}

    # Volume mounts
    volumes: List[str] = Field(default_factory=list)  # ["/host/path:/container/path:ro"]

    # Network settings
    networks: List[str] = Field(default_factory=list)

    # Health check
    health_check: Optional[Dict[str, Any]] = None

    # Restart policy
    restart_policy: str = "unless-stopped"

    # Labels for container metadata
    labels: Dict[str, str] = Field(default_factory=dict)

    # Command override
    command: Optional[List[str]] = None

    # Working directory
    workdir: Optional[str] = None


# Sync Response (API -> Agent)
class SyncResponse(BaseModel):
    success: bool
    desired_containers: List[ContainerConfig]
    poll_interval: int = 30
    global_config: Dict[str, Any] = Field(default_factory=dict)  # Global settings
    timestamp: datetime = Field(default_factory=datetime.now(UTC))
