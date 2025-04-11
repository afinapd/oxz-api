from behave import given, when, then
from assertpy import assert_that

@then('each book in collection should contain "{field}"')
def step_verify_collection_book_field(context, field):
    books = context.response.json()['books']
    if not books:  # Collection might be empty, which is valid
        return
        
    for book in books:
        assert_that(book).contains_key(field)
        # Additional validations based on field type
        if field == 'pages':
            assert_that(book[field]).is_instance_of(int)
        elif field == 'publish_date':
            assert_that(book[field]).matches(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z')
        elif field in ['isbn', 'title', 'subTitle', 'author', 'publisher', 'description', 'website']:
            assert_that(book[field]).is_instance_of(str)
            assert_that(book[field]).is_not_empty()

@when('I send a request to get all books')
def step_get_all_books(context):
    context.response = context.api.get_books()



@then('each book should contain "{field}"')
def step_verify_book_field(context, field):
    books = context.response.json()['books']
    assert_that(books).is_not_empty()
    
    for book in books:
        assert_that(book).contains_key(field)
        # Additional validations based on field type
        if field == 'pages':
            assert_that(book[field]).is_instance_of(int)
        elif field == 'publish_date':
            assert_that(book[field]).matches(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z')
        elif field in ['isbn', 'title', 'subTitle', 'author', 'publisher', 'description', 'website']:
            assert_that(book[field]).is_instance_of(str)
            assert_that(book[field]).is_not_empty()

@given('there are books available in the store')
def step_verify_books_available(context):
    response = context.api.get_books()
    books = response.json()['books']
    assert_that(books).is_not_empty()
    # Store first book's ISBN for later use
    context.test_data['isbn'] = books[0]['isbn']

@when('I send a request to get book with ISBN "{isbn}"')
def step_get_book_by_isbn(context, isbn):
    context.response = context.api.get_book(isbn)



@when('I send a request to add book with isbn "{isbn}" to my collection')
@given('I send a request to add book with isbn "{isbn}" to my collection')
def step_add_book_to_collection(context, isbn):
    context.test_data['isbn'] = isbn
    context.response = context.api.add_book(
        user_id=context.test_data['user_id'],
        isbn=isbn
    )



@given('I have a valid book ISBN')
def step_get_valid_isbn(context):
    response = context.api.get_books()
    books = response.json()['books']
    assert_that(books).is_not_empty()
    context.test_data['isbn'] = books[0]['isbn']



@then('the book should appear in my collection')
def step_verify_book_added(context):
    response = context.api.get_user_books(context.test_data['user_id'])
    books = response.json()['books']
    assert_that(books).extracting('isbn').contains(context.test_data['isbn'])

@given('I have a book in my collection')
def step_ensure_book_in_collection(context):
    # First get a valid ISBN if we don't have one
    if not context.test_data['isbn']:
        step_get_valid_isbn(context)
    
    # Add book to collection
    response = context.api.add_book(
        context.test_data['user_id'],
        context.test_data['isbn']
    )
    assert_that(response.status_code).is_between(200, 201)

@given('I remove book with isbn "{isbn}" from my collection if exists')
def step_remove_book_if_exists(context, isbn):
    # Make sure we're authenticated
    if not context.api.token:
        # Generate token first
        response = context.api.generate_token(context.test_data['username'], context.test_data['password'])
        data = response.json()
        token = data.get('token')
        assert_that(token).is_not_none()
        context.api.set_token(token)

    # Get user books first
    response = context.api.get_user(context.test_data['user_id'])
    if response.status_code == 200:
        books = response.json().get('books', [])
        if any(book['isbn'] == isbn for book in books):
            # Book exists, delete it
            context.response = context.api.delete_book(
                user_id=context.test_data['user_id'],
                isbn=isbn
            )
            # Wait for deletion to complete
            assert_that(context.response.status_code).is_equal_to(204)

@when('I remove book with isbn "{isbn}" from my collection')
def step_remove_book(context, isbn):
    context.test_data['isbn'] = isbn
    context.response = context.api.delete_book(
        context.test_data['user_id'],
        isbn
    )

@when('I remove books from my collection')
def step_remove_books(context):
    # Make sure we're authenticated
    if not context.api.token:
        # Generate token first
        response = context.api.generate_token(context.test_data['username'], context.test_data['password'])
        data = response.json()
        token = data.get('token')
        assert_that(token).is_not_none()
        context.api.set_token(token)

    # Get user books first
    response = context.api.get_user(context.test_data['user_id'])
    if response.status_code == 200:
        books = response.json().get('books', [])
        for book in books:
            # Delete each book
            context.response = context.api.delete_book(
                user_id=context.test_data['user_id'],
                isbn=book['isbn']
            )

@then('the book should not be in my collection')
def step_verify_book_removed(context):
    response = context.api.get_user(context.test_data['user_id'])
    if response.status_code != 200:
        raise AssertionError(f"Failed to get user books: {response.status_code}")
    try:
        books = response.json()['books']
        for book in books:
            if book['isbn'] == context.test_data['isbn']:
                raise AssertionError(f"Book {context.test_data['isbn']} still exists in collection")
    except (ValueError, KeyError) as e:
        if response.text:
            raise AssertionError(f"Failed to parse response: {str(e)}. Response: {response.text}")
        else:
            raise AssertionError(f"Failed to parse response: {str(e)}. Empty response.")

@when('I send a request to delete book with isbn "{isbn}" from store')
def step_delete_book_from_store(context, isbn):
    context.test_data['isbn'] = isbn
    context.response = context.api.delete_book_from_store(
        isbn=isbn,
        user_id=context.test_data['user_id']
    )

@then('the request should contain only isbn "{isbn}"')
def step_verify_request_body_isbn(context, isbn):
    expected_body = {'isbn': isbn}
    actual_body = context.api.last_request_body
    assert_that(actual_body).is_equal_to(expected_body)

@then('the request should contain isbn "{isbn}" and userId "{user_id}"')
def step_verify_request_body(context, isbn, user_id):
    expected_body = {
        'isbn': isbn,
        'userId': user_id
    }
    # Get the actual request body from the last API call
    actual_body = context.api.last_request_body
    assert_that(actual_body).is_equal_to(expected_body)


