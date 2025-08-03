import asyncio
from unittest.mock import MagicMock

from src.container.container_operations import ContainerOperations
from src.container.container import Container
from src.container.nerd import Nerd


async def test_get_all_containers():
    # find all running containers
    nerd = MagicMock(spec=ContainerOperations)
    # given
    running_images = [
        Container("BEEF", nerd),
        Container("CHICKEN", nerd),
    ]
    nerd.get_all_containers.return_value = running_images
    # when
    containers = await nerd.get_all_containers()

    #then

    assert containers == running_images


def test_get_container_info():
    # Each container (inspect) has information we need
    # like image, status, cpu allocation/usage, memory allocation/usage,
    pass
