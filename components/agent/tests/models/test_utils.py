import unittest
from src.models import HealthStatus, ContainerState
from src.models.utils import (
    container_state_from_string,
    container_state_to_string,
    container_health_from_string
)


class TestModelUtils(unittest.TestCase):
    def test_container_status_from_string_valid(self):
        """Test converting valid strings to ContainerState enum values"""
        # Test all valid container states
        for state in ContainerState:
            status = container_state_from_string(state.value)
            self.assertIsInstance(status, ContainerState)
            self.assertEqual(status, state)
            
        # Test with uppercase
        status = container_state_from_string("RUNNING")
        self.assertEqual(status, ContainerState.RUNNING)
        
    def test_container_status_from_string_invalid(self):
        """Test converting invalid strings to ContainerState enum values"""
        with self.assertRaises(ValueError):
            container_state_from_string("invalid_status")
            
    def test_container_status_to_string(self):
        """Test converting ContainerState enum values to strings"""
        for state in ContainerState:
            status_str = container_state_to_string(state)
            self.assertEqual(status_str, state.value)
            
    def test_health_status_from_string_valid(self):
        """Test converting valid strings to HealthStatus enum values"""
        # Test all valid health statuses
        for health in HealthStatus:
            status = container_health_from_string(health.value)
            self.assertEqual(status, health)
            
        # Test with uppercase
        status = container_health_from_string("HEALTHY")
        self.assertEqual(status, HealthStatus.HEALTHY)
        
    def test_health_status_from_string_invalid(self):
        """Test converting invalid strings to HealthStatus enum values"""
        with self.assertRaises(ValueError):
            container_health_from_string("invalid_health")


if __name__ == "__main__":
    unittest.main()