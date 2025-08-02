import grpc
from containerd.services.namespaces.v1 import namespace_pb2_grpc, namespace_pb2
from containerd.services.containers.v1 import containers_pb2, containers_pb2_grpc
from containerd.services.tasks.v1 import tasks_pb2, tasks_pb2_grpc
from containerd.types.task import task_pb2

from typing import Dict, Any

from src.container.container_operations import ContainerOperations


class Container:
    """High-level container object"""
    def __init__(self, id: str, client: ContainerOperations):
        self.id = id
        self._client = client

def get_containers(self) -> list:
    with grpc.insecure_channel(self.containerd_address) as channel:
        containersv1 = containers_pb2_grpc.ContainersStub(channel)
        containers = containersv1.List().containers
        for container in containers:
            print('container ID:', container.id)
        return containers

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


def get_container_cpu_allocation(self, container_id: str) -> float:
    # Connect to containerd using the well-known containerd.sock and location.
    # Please note that this does not really connect yet, but just jots down the
    # grpc server address and the connect will only happen later when the first
    # service is to be called.
    with grpc.insecure_channel(self.containerd_address) as channel:
        # These are the containerd APIs we're going to use below.
        namespacev1 = namespace_pb2_grpc.NamespacesStub(channel)
        containersv1 = containers_pb2_grpc.ContainersStub(channel)
        tasksv1 = tasks_pb2_grpc.TasksStub(channel)

        # First, discover all available containerd namespaces.
        try:
            namespaces = namespacev1.List(namespace_pb2.ListNamespacesRequest()).namespaces
        except grpc.RpcError as e:
            print('ERROR: cannot connect: {}'.format(e))
            return 0.0
        # Now look for containers and their corresponding tasks in each of the
        # containerd namespaces...
        for namespace in namespaces:
            print('⬚ namespace:', namespace.name)
            print('  ⤏ namespace labels ({}):'.format(len(namespace.labels)))
            for label in namespace.labels:
                print('      "{n}": "{v}"'.format(n=label, v=namespace.labels[label]))

            # The containerd API is slightly "peculiar" in that the list of containers
            # lacks such useful information such as PID and container status. Instead,
            # these nuggets of wisdom are to be gleamed from the tasks lists. Both the
            # list of containers as well as the list of tasks are related by their IDs.
            # That is, the task ID is the same as the container ID. However, there
            # doesn't need to be a task for a container, so be careful. According to
            # https://github.com/containerd/containerd/blob/master/design/architecture.md,
            # the list of containers is considered as metadata (as are images), while
            # tasks are directly associated with the runtime(s).
            tasks = tasksv1.List(tasks_pb2.ListPidsRequest(),
                                 metadata=(('containerd-namespace', namespace.name),)).tasks
            taskidx = dict()
            for task in tasks:
                taskidx[task.id] = task

            # We also need the list of containers, and not only the list of tasks, as we
            # need metadata: in particular, the labels of a container. While Docker is
            # giving us not much but a "com.docker/engine.bundle.path", Kubernetes
            # labels all the important metadata, such as pod namespace and name,
            # container name, et cetera. And cri-containerd throws in a kind to indicate
            # Kubernetes' pause sandboxes. Only Docker isn't keen of labeling.
            containers = containersv1.List(containers_pb2.ListContainersRequest(),
                                           metadata=(('containerd-namespace', namespace.name),)).containers
            for container in containers:
                print('  ▩ container:', container.id)
                if container.id in taskidx:
                    t = taskidx[container.id]
                    print('    ▷ PID:', t.pid, '⚐ status:', task_pb2.Status.Name(t.status))
                print('    ⚙ runtime:', container.runtime.name)
                print('    ◷ created:', container.created_at.ToDatetime(), '◷ updated:',
                      container.updated_at.ToDatetime())
                # print('    extensions:', container.extensions)
                # print('    spec:', container.spec)
                print(f"Task CPU Allocation: {container.cpu}")
            print()
            return container.cpu
