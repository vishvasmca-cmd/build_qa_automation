Feature: ParaBank Smoke Tests

  As a user
  I want to perform basic operations on ParaBank
  So that I can verify the core functionality is working

  @smoke
  Scenario: Register a new user
    Given I am on the ParaBank home page
    When I click the "Register" link
    And I fill in the registration form with valid data
    | firstName | lastName | address.street | address.city | address.state | address.zipCode | phone | ssn | username | password |
    | John      | Doe      | 123 Main St    | Anycity      | Anystate      | 12345           | 555-1212 | 123-45-6789 | testuser | password |
    Then I should be registered successfully

  @smoke
  Scenario: Log in with valid credentials
    Given I am on the ParaBank home page
    When I enter valid username and password
    And I click the "Log In" button
    Then I should be logged in successfully
