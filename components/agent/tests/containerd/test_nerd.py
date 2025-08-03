import json
import pytest
from unittest.mock import MagicMock, patch

from src.container.container import Container
from src.container.nerd import Nerd


@pytest.mark.asyncio
async def test_get_all_containers():
    # find all running containers
    nerd = Nerd()
    # given
    container_ids = ["BEEF", "CHICKEN"]
    image_names=f"{container_ids[0]}\n{container_ids[1]}"
    subprocess_result = MagicMock()
    subprocess_result.stdout = image_names

    # when
    with patch("src.container.nerd.subprocess.run", return_value=subprocess_result) as mock_run:
        containers = await nerd.get_all_containers()

    #then

    assert containers[0].cid == container_ids[0]
    assert containers[1].cid == container_ids[1]


@pytest.mark.asyncio
async def test_get_container_info():
    nerd = Nerd()
    
    # given
    container_id = "BEEF"
    mock_inspect_data = [{
        "Name": "test-container",
        "State": {
            "Status": "running",
            "Health": {
                "Status": "healthy"
            }
        },
        "HostConfig": {
            "PortBindings": {"80/tcp": [{"HostIp": "0.0.0.0", "HostPort": "8080"}]},
            "CpuQuota": 50000,
            "CpuPeriod": 100000,
            "Memory": 1000000000.0
        }
    }]
    
    subprocess_result = MagicMock()
    subprocess_result.stdout = json.dumps(mock_inspect_data)
    
    # when
    with patch("src.container.nerd.subprocess.run", return_value=subprocess_result) as mock_run:
        info = await nerd.get_container_info(container_id)
        
        # then
        mock_run.assert_called_once_with(
            ["nerdctl", "inspect", container_id],
            capture_output=True,
            text=True,
            check=True
        )
    
    assert info.container_id == "BEEF"
    assert info.status == "running"
    assert info.health == "healthy"
    assert info.ports == {"80": 8080}
    assert info.cpu_usage == 0.5
    assert info.memory_mb == 1000000000.0
