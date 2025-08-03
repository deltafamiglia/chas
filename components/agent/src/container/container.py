from src.container.container_operations import ContainerOperations
from src.models import ContainerStatus, HealthStatus


class Container:
    """High-level container object"""
    def __init__(self, cid: str, client: ContainerOperations):
        self.cid = cid
        self._client = client


    async def start(self) -> None:
        """Start the container"""
        await self._client.start_container(self.cid)

    async def stop(self, timeout: int = 10) -> None:
        """Stop the container"""
        await self._client.stop_container(self.cid, timeout)


    async def delete(self, force: bool = False) -> None:
        """Delete the container"""
        await self._client.delete_container(self.cid, force)


    async def status(self) -> HealthStatus:
        """Get container status"""
        return await self._client.get_container_status(self.cid)


    async def info(self) -> ContainerStatus:
        """Get container info"""
        return await self._client.get_container_info(self.cid)

