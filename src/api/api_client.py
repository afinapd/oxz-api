import logging
import requests
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class APIClient:
    """Client for interacting with the DemoQA BookStore API"""
    
    # API endpoints
    ACCOUNT_BASE = "/Account/v1"
    BOOKSTORE_BASE = "/BookStore/v1"
    
    def __init__(self):
        """Initialize API client"""
        self.base_url = "https://demoqa.com"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.token = None
        self.last_request_body = None

    def _log_request(self, method: str, url: str, headers: Dict, json: Optional[Dict] = None) -> None:
        """Log request details"""
        logger.info(f"{method} {url}")
        logger.debug(f"Headers: {headers}")
        if json:
            logger.debug(f"Body: {json}")

    def _log_response(self, response: requests.Response) -> None:
        """Log response details"""
        logger.info(f"Response: {response.status_code}")
        logger.debug(f"Response body: {response.text}")

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with logging"""
        url = f"{self.base_url}{endpoint}"
        
        # Add token to headers if available
        if self.token:
            self.headers['Authorization'] = f'Bearer {self.token}'
        
        # Log request
        self._log_request(method, url, self.headers, kwargs.get('json'))
        
        # Make request
        response = requests.request(method, url, headers=self.headers, **kwargs)
        
        # Store request body for testing
        if kwargs.get('json'):
            self.last_request_body = kwargs['json']
        
        # Log response
        self._log_response(response)
        
        return response

    def set_token(self, token: Optional[str]) -> None:
        """Set or clear authentication token"""
        self.token = token
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
        elif "Authorization" in self.headers:
            del self.headers["Authorization"]

    # HTTP methods
    def get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """Send GET request"""
        return self._make_request('GET', endpoint, params=params)

    def post(self, endpoint: str, json: Optional[Dict] = None) -> requests.Response:
        """Send POST request"""
        return self._make_request('POST', endpoint, json=json)

    def delete(self, endpoint: str, json: Optional[Dict] = None) -> requests.Response:
        """Send DELETE request"""
        return self._make_request('DELETE', endpoint, json=json)

    # Authentication endpoints
    def create_user(self, username: str, password: str) -> requests.Response:
        """Create a new user"""
        payload = {
            "userName": username,
            "password": password
        }
        return self.post(f"{self.ACCOUNT_BASE}/User", json=payload)

    def get_user(self, user_id: str) -> requests.Response:
        """Get user account details"""
        return self.get(f"{self.ACCOUNT_BASE}/User/{user_id}")

    def delete_user(self, user_id: str) -> requests.Response:
        """Delete user account"""
        return self.delete(f"{self.ACCOUNT_BASE}/User/{user_id}")

    def login(self, username: str, password: str) -> requests.Response:
        """Login user and get token"""
        payload = {
            "userName": username,
            "password": password
        }
        return self.post(f"{self.ACCOUNT_BASE}/Login", json=payload)

    def generate_token(self, username: str, password: str) -> requests.Response:
        """Generate authentication token"""
        payload = {
            "userName": username,
            "password": password
        }
        return self.post(f"{self.ACCOUNT_BASE}/GenerateToken", json=payload)

    # Book endpoints
    def get_books(self) -> requests.Response:
        """Get all books"""
        return self.get(f"{self.BOOKSTORE_BASE}/Books")

    def get_book(self, isbn: str) -> requests.Response:
        """Get book by ISBN"""
        return self.get(f"{self.BOOKSTORE_BASE}/Book", params={"ISBN": isbn})

    def add_book(self, user_id: str, isbn: str) -> requests.Response:
        """Add book to user's collection"""
        payload = {
            "userId": user_id,
            "collectionOfIsbns": [{"isbn": isbn}]
        }
        return self.post(f"{self.BOOKSTORE_BASE}/Books", json=payload)

    def delete_book(self, user_id: str, isbn: str) -> requests.Response:
        """Delete book from user's collection"""
        return self.delete(
            f"{self.BOOKSTORE_BASE}/Books?UserId={user_id}",
            json={"isbn": isbn}
        )

    def get_user_books(self, user_id: str) -> requests.Response:
        """Get user's book collection"""
        return self.get(f"{self.ACCOUNT_BASE}/User/{user_id}/Books")

    def delete_book_from_store(self, isbn: str, user_id: str) -> requests.Response:
        """Delete book from bookstore"""
        return self.delete(
            f"{self.BOOKSTORE_BASE}/Book",
            json={"isbn": isbn, "userId": user_id}
        )
