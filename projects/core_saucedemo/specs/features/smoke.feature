Feature: E-commerce Smoke Tests

  Scenario: User Login with valid credentials @smoke
    Given I am on the login page
    When I fill the username field with "standard_user"
    And I fill the password field with "secret_sauce"
    And I click the login button
    Then I should be logged in and redirected to the inventory page

  Scenario: Sort products by price low to high @smoke
    Given I am on the inventory page
    When I click the sort dropdown
    Then products should be sorted by price low to high
