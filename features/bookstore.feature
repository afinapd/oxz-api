Feature: BookStore API Testing
    As an API user
    I want to interact with the BookStore API
    So that I can manage books in my collection

    @GET_Books
    Scenario: Get all books
        When I send a request to get all books
        Then the response status code should be 200
        And the response should contain "books"
        And each book should contain "isbn"
        And each book should contain "title"
        And each book should contain "subTitle"
        And each book should contain "author"
        And each book should contain "publish_date"
        And each book should contain "publisher"
        And each book should contain "pages"
        And each book should contain "description"
        And each book should contain "website"

    @GET_Books_isbn
    Scenario: Get a specific book by ISBN
        When I send a request to get book with ISBN "9781449325862"
        Then the response status code should be 200
        And the response should contain "isbn"
        And the response should contain "title"
        And the response should contain "subTitle"
        And the response should contain "author"
        And the response should contain "publish_date"
        And the response should contain "publisher"
        And the response should contain "pages"
        And the response should contain "description"
        And the response should contain "website"

    @POST_Books
    Scenario: Add books to user collection
        Given I login with username "afinapd" password "Afina12345!"
        When I remove books from my collection
        When I send a request to add book with isbn "9781449325862" to my collection
        Then the response status code should be 201
        And the response should contain "books"
        And each book in collection should contain "isbn"

    @DELETE_Books
    Scenario: Delete books from user collection
        Given I login with username "afinapd" password "Afina12345!"
        And I send a request to add book with isbn "9781449325862" to my collection
        When I remove books from my collection
        Then the response status code should be 204
        And the request should contain only isbn "9781449325862"

    @DELETE_Book
    Scenario: Delete book from user collection
        Given I login with username "afinapd" password "Afina12345!"
        When I send a request to add book with isbn "9781449325862" to my collection
        When I send a request to delete book with isbn "9781449325862" from store
        Then the response status code should be 204
        And the request should contain isbn "9781449325862" and userId "30e4bb09-77df-4ac7-9b11-abf64ab0f24c"