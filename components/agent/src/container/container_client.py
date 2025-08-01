from typing import Optional, List, Dict
import grpc
from containerd.services.containers.v1 import containers_pb2, containers_pb2_grpc
from containerd.services.tasks.v1 import tasks_pb2, tasks_pb2_grpc
from containerd.services.images.v1 import images_pb2, images_pb2_grpc
from containerd.services.snapshots.v1 import snapshots_pb2, snapshots_pb2_grpc
import asyncio

from src.container.container import Container
from src.container.container_operations import ContainerOperations


class ContainerdClient(ContainerOperations):
    """High-level client for containerd"""

    def __init__(
            self,
            address: str = "unix:///run/containerd/containerd.sock",
            namespace: str = "default"
    ):
        self.channel = grpc.insecure_channel(address)
        self.namespace = namespace

        # Initialize service stubs
        self.containers = containers_pb2_grpc.ContainersStub(self.channel)
        self.tasks = tasks_pb2_grpc.TasksStub(self.channel)
        self.images = images_pb2_grpc.ImagesStub(self.channel)
        self.snapshots = snapshots_pb2_grpc.SnapshotsStub(self.channel)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        """Close the client connection"""
        self.channel.close()

    async def pull_image(self, image_ref: str) -> str:
        """Pull an image from a registry

        Args:
            image_ref: Image reference (e.g. "docker.io/library/redis:latest")

        Returns:
            Image ID
        """
        request = images_pb2.PullRequest(
            image=image_ref,
            platform={"os": "linux", "architecture": "amd64"}
        )
        response = await self.images.Pull(request)
        return response.image.id

    async def create_container(
            self,
            cid: str,
            image: str,
            labels: Optional[Dict[str, str]] = None
    ) -> Container:
        """Create a new container

        Args:
            cid: Container ID
            image: Image reference
            labels: Container labels

        Returns:
            Container object
        """
        spec = {
            "image": image,
            "labels": labels or {}
        }

        request = containers_pb2.CreateContainerRequest(
            container={
                "id": cid,
                "image": image,
                "labels": labels or {},
                "runtime": {
                    "name": "io.containerd.runc.v2"
                }
            }
        )

        await self.containers.Create(request)
        return Container(cid, self)

    async def list_containers(self) -> List[Container]:
        """List all containers"""
        request = containers_pb2.ListContainersRequest()
        response = await self.containers.List(request)
        return [Container(c.id, self) for c in response.containers]

    async def get_container(self, cid: str) -> Optional[Container]:
        """Get container by ID"""
        try:
            request = containers_pb2.GetContainerRequest(id=cid)
            await self.containers.Get(request)
            return Container(cid, self)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return None
            raise

    # Internal methods used by Container class
    async def start_container(self, cid: str) -> None:
        task_request = tasks_pb2.CreateTaskRequest(
            container_id=cid
        )
        task = await self.tasks.Create(task_request)

        start_request = tasks_pb2.StartRequest(
            container_id=cid
        )
        await self.tasks.Start(start_request)

    async def stop_container(self, cid: str, timeout: int) -> None:
        request = tasks_pb2.KillRequest(
            container_id=cid,
            signal=15  # SIGTERM
        )
        await self.tasks.Kill(request)

        # Wait for graceful shutdown
        await asyncio.sleep(timeout)

        # Force kill if still running
        try:
            force_request = tasks_pb2.KillRequest(
                container_id=cid,
                signal=9  # SIGKILL
            )
            await self.tasks.Kill(force_request)
        except grpc.RpcError:
            pass

    async def delete_container(self, cid: str, force: bool) -> None:
        if force:
            try:
                await self.stop_container(cid, 0)
            except grpc.RpcError:
                pass

        request = containers_pb2.DeleteContainerRequest(id=cid)
        await self.containers.Delete(request)
