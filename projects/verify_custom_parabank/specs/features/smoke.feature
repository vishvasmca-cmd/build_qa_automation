Feature: Account Access - Smoke Tests
  As a user, I want to be able to register, login and view my account overview so that I can manage my finances.

  @smoke
  Scenario: Register a new user, login, and check account overview
    Given I am on the ParaBank home page
    When I click the 'Register' link
    And I fill the registration form with valid data
    And I click the 'Register' button
    Then I should be able to access the account overview page
