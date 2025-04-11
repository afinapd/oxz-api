import logging
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from src.api.api_client import APIClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def before_all(context):
    """Initialize test environment and logging"""
    # Load environment variables
    load_dotenv()
    
    # Initialize API client
    context.api = APIClient()
    context.base_url = "https://demoqa.com"
    
    # Initialize test data dictionary
    if not hasattr(context, 'test_data'):
        context.test_data = {}
    
    # Store test data
    context.test_data.update({
        "username": os.getenv("TEST_USERNAME", "testuser"),
        "password": os.getenv("TEST_PASSWORD", "Test@123"),
        "user_id": "",
        "isbn": ""
    })
    
    # Log test session start
    logging.info(f"Starting test session at {datetime.now()}")

def before_scenario(context, scenario):
    """Reset scenario-specific data before each scenario"""
    # Reset response and error state
    context.response = None
    context.error = None
    
    # Reset API client token
    context.api.set_token(None)
    
    # Reset test data except credentials
    credentials = {
        "username": context.test_data.get("username"),
        "password": context.test_data.get("password")
    }
    context.test_data = {
        "username": credentials["username"],
        "password": credentials["password"],
        "user_id": "",
        "isbn": ""
    }
    
    # Log scenario start
    logging.info(f"\nStarting scenario: {scenario.name}")

def after_scenario(context, scenario):
    """Cleanup after each scenario"""
    try:
        # Log scenario result
        if scenario.status == "failed":
            logging.error(f"Scenario failed: {scenario.name}")
            if context.error:
                logging.error(f"Error: {context.error}")
            if hasattr(context, 'response') and context.response:
                logging.error(f"Last response: {context.response.text}")
        else:
            logging.info(f"Scenario passed: {scenario.name}")
        
        # Cleanup: Remove test user if created during scenario
        if "POST_User" in scenario.tags and context.test_data.get("user_id"):
            try:
                context.api.delete_user(context.test_data["user_id"])
                logging.info(f"Cleaned up test user {context.test_data['user_id']}")
            except Exception as e:
                logging.warning(f"Failed to cleanup test user: {e}")
        
        # Cleanup: Remove test books if added during scenario
        if "POST_Books" in scenario.tags and context.test_data.get("user_id"):
            try:
                response = context.api.get_user_books(context.test_data["user_id"])
                if response.status_code == 200:
                    books = response.json().get("books", [])
                    for book in books:
                        context.api.delete_book(
                            context.test_data["user_id"],
                            book["isbn"]
                        )
                    if books:
                        logging.info(f"Cleaned up {len(books)} books from collection")
            except Exception as e:
                logging.warning(f"Failed to cleanup books: {e}")
    except Exception as e:
        logging.error(f"Error in cleanup: {e}")
    finally:
        # Reset scenario-specific data
        context.response = None
        context.error = None
        context.api.set_token(None)
        
        # Reset test data except credentials
        credentials = {
            "username": context.test_data.get("username"),
            "password": context.test_data.get("password")
        }
        context.test_data = {
            "username": credentials["username"],
            "password": credentials["password"],
            "user_id": "",
            "isbn": ""
        }

def before_feature(context, feature):
    """Setup before each feature"""
    logging.info(f"\nStarting feature: {feature.name}")

def after_feature(context, feature):
    """Cleanup after each feature"""
    logging.info(f"Completed feature: {feature.name}")

def after_all(context):
    """Cleanup after all tests"""
    logging.info(f"\nCompleted test session at {datetime.now()}\n")
