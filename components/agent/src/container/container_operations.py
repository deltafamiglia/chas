from abc import ABC, abstractmethod
from typing import Protocol, Optional, Dict, Any, List

from src.models import ContainerStatus, HealthStatus


class ContainerOperations(Protocol):
    """Protocol defining container operations"""

    async def start_container(self, cid: str) -> None:
        ...

    async def stop_container(self, cid: str, timeout: int) -> None:
        ...

    async def delete_container(self, cid: str, force: bool) -> None:
        ...

    async def get_container_status(self, cid: str) -> HealthStatus:
        ...

    async def get_container_info(self, cid: str) -> ContainerStatus | None:
        ...

    async def get_all_containers(self):
        ...
