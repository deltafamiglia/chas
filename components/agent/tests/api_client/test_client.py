from unittest.mock import patch, MagicMock
import json
import requests
from src.api_client.client import Client
from src.models import RegisterRequest, RegisterResponse, AgentCapabilities

def test_client_init_defaults():
    # Test with default api_url
    client = Client()
    assert client.api_url == "http://localhost:8000/api/v1"

def test_client_init_custom_url():
    # Test with custom api_url
    custom_url = "https://example.com/api"
    client_with_custom_url = Client(api_url=custom_url)
    assert client_with_custom_url.api_url == custom_url

@patch('requests.post')
def test_client_register(mock_post):
    # POST /api/v1/agents/
    # Request: RegisterRequest
    # Response: RegisterResponse
    
    # Setup mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    
    # Setup the response data
    response_data = {
        "success": True,
        "message": "Agent registered successfully",
        "poll_interval": 45
    }
    
    # Configure the json method to return the response data
    mock_response.json.return_value = response_data
    
    # Configure the post method to return the mock response
    mock_post.return_value = mock_response
    
    # Create test data
    capabilities = AgentCapabilities(
        cpu_cores=4,
        memory_gb=8.0,
        docker_networks=["bridge", "host"]
    )
    request = RegisterRequest(
        agent_id="test-agent-001",
        hostname="test-host",
        capabilities=capabilities
    )
    
    # Create client and call register_agent
    client = Client()
    response = client.register_agent(request)
    
    # Verify the request was created correctly
    mock_post.assert_called_once_with(
        f"{client.api_url}/agents",
        json=request.model_dump(),
        headers={"Content-Type": "application/json"}
    )
    
    # Verify response
    assert isinstance(response, RegisterResponse)
    assert response.success is True
    assert response.message == "Agent registered successfully"
    assert response.poll_interval == 45

@patch('requests.post')
def test_client_register_error(mock_post):
    # Test error handling when the API returns an error
    
    # Create a mock response for the error
    mock_response = MagicMock()
    mock_response.status_code = 409  # Conflict
    mock_response.headers = {"Content-Type": "application/json"}
    
    # Setup the error data
    error_data = {
        "success": False,
        "message": "Agent ID already exists"
    }
    
    # Configure the json method to return the error data
    mock_response.json.return_value = error_data
    
    # Create a requests.exceptions.HTTPError
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "409 Client Error: Conflict",
        response=mock_response
    )
    
    # Configure post to return the mock response
    mock_post.return_value = mock_response
    
    # Create test data
    capabilities = AgentCapabilities(
        cpu_cores=4,
        memory_gb=8.0
    )
    request = RegisterRequest(
        agent_id="existing-agent-id",
        hostname="test-host",
        capabilities=capabilities
    )
    
    # Create client and call register_agent
    client = Client()
    response = client.register_agent(request)
    
    # Verify the request was created correctly
    mock_post.assert_called_once_with(
        f"{client.api_url}/agents",
        json=request.model_dump(),
        headers={"Content-Type": "application/json"}
    )
    
    # Verify response contains error information
    assert isinstance(response, RegisterResponse)
    assert response.success is False
    assert response.message == "Agent ID already exists"
    assert response.poll_interval == 30

def test_client_unregister():
    pass

def test_client_sync():
    pass
