from typing import Dict, Any

from src.container.container_operations import ContainerOperations


class Container:
    """High-level container object"""
    def __init__(self, id: str, client: ContainerOperations):
        self.id = id
        self._client = client

async def start(self) -> None:
    """Start the container"""
    await self._client.start_container(self.id)

async def stop(self, timeout: int = 10) -> None:
    """Stop the container"""
    await self._client.stop_container(self.id, timeout)


async def delete(self, force: bool = False) -> None:
    """Delete the container"""
    await self._client.delete_container(self.id, force)


async def status(self) -> Dict[str, Any]:
    """Get container status"""
    return await self._client.get_container_status(self.id)
