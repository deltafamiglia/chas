import json
import requests
from src.models import RegisterRequest, RegisterResponse

class Client:

    def __init__(self, api_url: str = None):
        self.api_url = api_url or "http://localhost:8000/api/v1"

    def register_agent(self, request: RegisterRequest) -> RegisterResponse:
        """
        Register an agent with the API server.
        
        Args:
            request: RegisterRequest object containing agent information
            
        Returns:
            RegisterResponse object with the server's response
            
        Raises:
            requests.exceptions.HTTPError: If the server returns an error response
            requests.exceptions.RequestException: If there's a network error
            json.JSONDecodeError: If the response is not valid JSON
        """
        # Prepare request data
        data = request.model_dump()
        
        # Set headers
        headers = {"Content-Type": "application/json"}
        
        try:
            # Send request and get response
            response = requests.post(
                f"{self.api_url}/agents",
                json=data,
                headers=headers
            )
            
            # Raise an exception for 4XX/5XX responses
            response.raise_for_status()
            
            # Parse response JSON
            response_data = response.json()
                
            # Convert response to RegisterResponse object
            return RegisterResponse(**response_data)
        except requests.exceptions.HTTPError as e:
            # Try to parse error response if possible
            if e.response.headers.get('Content-Type') == 'application/json':
                error_data = e.response.json()
                return RegisterResponse(
                    success=False,
                    message=error_data.get('message', f"HTTP Error: {e.response.status_code}"),
                    poll_interval=30
                )
            # Otherwise, re-raise the exception
            raise

    def unregister_agent(self):
        pass

    def sync_agent(self):
        pass

