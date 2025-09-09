"""
Base service class for API integrations
"""

import requests
from config import Config


class BaseAPIService:
    """Base class for API services with common functionality"""
    
    def __init__(self):
        self.timeout = Config.REQUEST_TIMEOUT
    
    def safe_request(self, url: str) -> dict:
        """
        Make a safe HTTP request with error handling
        
        Args:
            url (str): URL to request
            
        Returns:
            dict: JSON response or empty dict on error
        """
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return {}
    
    def validate_api_key(self, api_key: str, service_name: str) -> bool:
        """
        Validate if API key is present
        
        Args:
            api_key (str): API key to validate
            service_name (str): Name of the service for error messages
            
        Returns:
            bool: True if API key is valid
        """
        if not api_key:
            print(f"Warning: {service_name} API key is missing")
            return False
        return True
