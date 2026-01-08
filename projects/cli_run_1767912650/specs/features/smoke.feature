Feature: ParaBank Smoke Tests

  @smoke
  Scenario: User Registration
    Given I am on the ParaBank registration page
    When I fill the registration form with valid data
    Then I should be registered successfully

  @smoke
  Scenario: User Login
    Given I am on the ParaBank login page
    When I enter valid username and password
    Then I should be logged in successfully
