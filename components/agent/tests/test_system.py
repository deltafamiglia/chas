from unittest.mock import patch
from unittest.result import failfast

import psutil

from src.system import get_cpu_cores, get_total_memory_gb, get_free_memory_gb, get_free_cpu_cores


@patch("psutil.cpu_count", return_value=4)
def test_get_cpu_cores(mock_cpu_count: int):
    # report the number of cores on node
    cpu_cores = get_cpu_cores()
    assert cpu_cores == 4

def test_get_free_cpu_cores():
    # Uses psutil to get cpu usage and return available cpu cores
    available_cpu = get_free_cpu_cores()
    assert available_cpu == 0.5


@patch("psutil.virtual_memory")
def test_get_total_mem(mock_virtual_memory):
    mock_virtual_memory.return_value.total = 1024**3

    total_memory = get_total_memory_gb()

    assert total_memory == 1.0

@patch("psutil.virtual_memory")
def test_get_free_mem(mock_virtual_memory):
    mock_virtual_memory.return_value.available = 0.5 * 1024**3
    free_memory = get_free_memory_gb()
    assert free_memory == 0.5
