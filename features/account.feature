Feature: BookStore Account API Testing
    As an API user
    I want to manage my account
    So that I can access the BookStore features

    @POST_GenerateToken
    Scenario: Generate auth token
        When I send a request to generate token
        Then the response status code should be 200
        And the response should contain "token"

    @POST_Login
    Scenario: Login with valid credentials
        When I send a request to login
        Then the response status code should be 200
        And the response should contain "userId"
        And the response should contain "username"
        And the response should contain "password"
        And the response should contain "token"
        And the response should contain "expires"
        And the response should contain "created_date"
        And the response should contain "isActive"
        And the response should be a valid JSON

    @GET_Account
    Scenario: Get user account details
        Given I login with username "afinapd" password "Afina12345!"
        When I send a request to get account details
        Then the response status code should be 200
        And the response should contain "userId"
        And the response should contain "username"
        And the response should contain "books"

    @POST_User
    Scenario: Create new user account
        When I send a request to create user with username "NewUser124" password "Test@User123!"
        Then the response status code should be 201
        And the response should contain "userID"
        And the response should contain "books"
        
    @DELETE_User
    Scenario: Delete user account
        Given I login with username "NewUser124" password "Test@User123!"
        When I send a request to delete my account
        Then the response status code should be 204
