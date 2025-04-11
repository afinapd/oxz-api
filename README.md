# DemoQA BookStore API Test Automation

This project contains API automation tests for the DemoQA BookStore API using Python with Behave (Cucumber).

## Project Structure

```
├── features/
│   ├── bookstore.feature    # Test scenarios in Gherkin
│   ├── environment.py       # Test environment setup
│   └── steps/
│       └── bookstore_steps.py  # Step definitions
├── src/
│   └── api/
│       └── api_client.py    # API client implementation
├── .env.example            # Environment variables template
└── requirements.txt        # Project dependencies
```

## Setup

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
```

4. Edit `.env` with your credentials:
```
TEST_USERNAME=your_username
TEST_PASSWORD=your_password
TEST_USER_ID=your_user_id
```

## Running Tests

### Run all tests:
```bash
behave
```

### Run non-authenticated tests only:
```bash
behave --tags=-auth
```

### Run specific feature:
```bash
behave features/bookstore.feature
```

### Run with detailed output:
```bash
behave -v
```

## Test Scenarios

1. Get all books
2. Get specific book details
3. Search for non-existent book
4. Add book to collection (authenticated)
5. Delete book from collection (authenticated)
6. View user's book collection (authenticated)