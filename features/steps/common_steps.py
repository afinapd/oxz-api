from behave import then
from assertpy import assert_that

@then('the response should contain "{field}"')
def step_verify_response_field(context, field):
    data = context.response.json()
    assert_that(data).contains_key(field)
    
    # Store userId for later use
    if field == 'userId':
        context.test_data['user_id'] = data[field]
    
    # Additional validations based on field type
    if field == 'token':
        assert_that(data[field]).is_not_empty()
    elif field in ['expires', 'created_date']:
        assert_that(data[field]).matches(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z')
    elif field == 'isActive':
        assert_that(data[field]).is_instance_of(bool)

@then('the response should be a valid JSON')
def step_verify_valid_json(context):
    try:
        context.response.json()
    except ValueError:
        raise AssertionError('Response is not a valid JSON')

@then('the response status code should be {status_code:d}')
def step_check_status_code(context, status_code):
    assert_that(context.response.status_code).is_equal_to(status_code)
