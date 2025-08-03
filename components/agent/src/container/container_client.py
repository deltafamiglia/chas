from typing import Optional, List, Dict

import asyncio

from src.container.container import Container
from src.container.container_operations import ContainerOperations


class ContainerdClient(ContainerOperations):
    """High-level client for containerd"""
