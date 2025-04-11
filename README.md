# DemoQA API Testing

This project contains automated test cases for the DemoQA BookStore API using Python with Behave BDD framework and requests library.

## Features Tested

1. **Account**
   - Generate auth token
   - Login with valid credentials
   - Get user account details
   - Create new user account
   - Delete user account

2. **Bookstore**
   - Get all books
   - Get a specific book by ISBN
   - Add books to user collection
   - Delete books from user collection
   - Delete book from user collection

## Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

## Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Unix/macOS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env` file:
```
TEST_USERNAME=your_username
TEST_PASSWORD=your_password
TEST_USER_ID=your_user_id
```

## Project Structure

```
oxz-api/
├── features/
│   ├── steps/              # Step Definitions
│   │   ├── account_steps.py
│   │   ├── bookstore_steps.py
│   │   └── common_steps.py
│   ├── src/
│   │   └── api/           # API Client
│   │       └── api_client.py
│   ├── bookstore.feature
│   └── environment.py
├── requirements.txt
└── README.md
```

## Running Tests

Run all tests:
```bash
behave -f pretty features/
```

Run specific feature:
```bash
behave -f pretty features/bookstore.feature
```

Run tests with tags:
```bash
behave -f pretty --tags=@GET_Books features/
```

## Test Reports

Test results are displayed in the console with the following information:
- Number of features passed/failed
- Number of scenarios passed/failed
- Number of steps passed/failed/undefined
- Total execution time
- Detailed logs for API requests and responses

## API Client

The project uses a custom APIClient class that:
- Handles authentication and token management
- Provides methods for all BookStore API operations
- Includes request/response logging
- Maintains session state
- Implements proper error handling