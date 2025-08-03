import psutil


def get_cpu_cores() -> int:
    return psutil.cpu_count(logical=False)

def get_free_cpu_cores() -> int:
    cores = get_cpu_cores()
    # get allocated cpu cores from containerd


    return cores - psutil.cpu_percent(interval=1) / 100 * cores


def get_total_memory_gb() -> float:
    return psutil.virtual_memory().total / 1024**3

def get_free_memory_gb() -> float:
    return psutil.virtual_memory().available / 1024**3

