from container.container import Container
from container.container_operations import ContainerOperations


class Nerd(ContainerOperations):

    def __init__(self):
        pass

    async def get_all_containers(self) -> list[Container]:
        return []

    async def get_container_info(self, container_id: str):
        pass
