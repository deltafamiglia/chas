import json
import subprocess

from src.container.container import Container
from src.container.container_operations import ContainerOperations
from src.models import ContainerStatus
from src.models.utils import container_state_from_string, container_health_from_string


class Nerd(ContainerOperations):

    def __init__(self):
        pass

    async def get_all_containers(self) -> list[Container]:
        try:
            result = subprocess.run(
                ["nerdctl", "ps", "-q"],
                capture_output=True,
                text=True,
                check=True,
            )
            # TODO: Check command return 1 container_id on each line
            # and NOTHING else
            container_ids = result.stdout.splitlines()

            return [Container(id, self) for id in container_ids]
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Error getting containers: {e}")
            return []

    async def get_container_info(self, container_id: str) -> ContainerStatus | None:
        try:
            result = subprocess.run(
                ["nerdctl", "inspect", container_id],
                capture_output=True,
                text=True,
                check=True,
            )
            inspect_data = json.loads(result.stdout)[0]

            host_config = inspect_data.get("HostConfig",{})
            cpu_quota = host_config.get("CpuQuota", 0)
            cpu_period = host_config.get("CpuPeriod", 0)
            cpu_limit = cpu_quota / cpu_period if cpu_period else 0

            status = container_state_from_string(inspect_data.get("State", {}).get("Status", ''))
            health = container_health_from_string(inspect_data.get("State", {}).get("Health", {}).get("Status", ''))

            # Parse port bindings to extract just the host port
            port_bindings = host_config.get("PortBindings", {})
            ports = {}
            for container_port, bindings in port_bindings.items():
                if bindings and len(bindings) > 0:
                    # Extract the container port number without the protocol
                    container_port_num = container_port.split('/')[0]
                    # Get the host port
                    host_port = bindings[0].get("HostPort")
                    if host_port:
                        ports[container_port_num] = int(host_port)
            
            container_status = ContainerStatus(
                service_id="",
                container_id=container_id,
                container_name=inspect_data.get("Name", ''),
                status=status,
                health=health,
                ports=ports,
                cpu_usage=cpu_limit,
                memory_mb=host_config.get("Memory", 0)
            )

            return container_status
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Error getting containers: {e}")
