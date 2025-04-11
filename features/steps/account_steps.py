from behave import given, when, then
from assertpy import assert_that

@when('I send a request to generate token')
def step_generate_token(context):
    context.response = context.api.generate_token(
        context.test_data['username'],
        context.test_data['password']
    )

@when('I send a request to login')
def step_login(context):
    context.response = context.api.login(
        context.test_data['username'],
        context.test_data['password']
    )

@when('I send a request to create user with username "{username}" password "{password}"')
def step_create_user(context, username, password):
    # Store credentials in test_data
    context.test_data['username'] = username
    context.test_data['password'] = password

    context.response = context.api.create_user(
        username=username,
        password=password
    )

@when('I send a request to get my account')
def step_get_account(context):
    context.response = context.api.get_user(context.test_data['user_id'])

@when('I send a request to get account details')
def step_get_account_details(context):
    context.response = context.api.get_user(context.test_data['user_id'])

@when('I send a request to delete my account')
def step_delete_account(context):
    context.response = context.api.delete_user(context.test_data['user_id'])

@given('I login with username "{username}" password "{password}"')
def step_login_with_credentials(context, username, password):
    # Store credentials in test_data
    context.test_data['username'] = username
    context.test_data['password'] = password

    # Wait for 2 seconds before login
    import time
    time.sleep(2)

    # Generate token first
    response = context.api.generate_token(username, password)
    data = response.json()
    token = data.get('token')
    assert_that(token).is_not_none()
    context.api.set_token(token)

    # Wait for 2 seconds after token generation
    time.sleep(2)

    # Login to get user ID
    response = context.api.login(username, password)
    data = response.json()
    context.test_data['user_id'] = data['userId']

@given('I am an authenticated user')
def step_authenticate_user(context):
    # Generate token
    response = context.api.login(
        context.test_data['username'],
        context.test_data['password']
    )
    data = response.json()
    token = data.get('token')
    assert_that(token).is_not_none()
    context.api.set_token(token)
    
    # Store user ID
    context.test_data['user_id'] = data['userId']


