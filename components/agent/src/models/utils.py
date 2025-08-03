from src.models import HealthStatus, ContainerState


def container_state_from_string(status: str) -> ContainerState:
    """
    Convert a string representation to a ContainerStatus object.
    
    Args:
        status: String representation of container status
        
    Returns:
        ContainerStatus object with the status field set to the appropriate ContainerState
    """
    try:
        container_state = ContainerState(status.lower())
        return container_state
    except ValueError:
        # If the string doesn't match any ContainerState value
        raise ValueError(f"Invalid container status: {status}. Valid values are: {[s.value for s in ContainerState]}")

def container_state_to_string(status: ContainerState) -> str:
    """
    Convert a ContainerStatus object to its string representation.
    
    Args:
        status: ContainerStatus object
        
    Returns:
        String representation of the container status
    """
    return status.value

def container_health_from_string(status: str) -> HealthStatus:
    """
    Convert a string representation to a HealthStatus enum value.
    
    Args:
        status: String representation of health status
        
    Returns:
        HealthStatus enum value
    """
    try:
        return HealthStatus(status.lower())
    except ValueError:
        # If the string doesn't match any HealthStatus value
        raise ValueError(f"Invalid health status: {status}. Valid values are: {[s.value for s in HealthStatus]}")
