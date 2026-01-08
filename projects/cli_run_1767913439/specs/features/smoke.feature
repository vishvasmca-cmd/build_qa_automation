Feature: ParaBank Smoke Tests

  Scenario: User Registration
    @smoke
    Given I am on the ParaBank home page
    When I click on the "Register" link
    And I fill in the registration form with valid data
    And I click the "Register" button
    Then I should be registered successfully

  Scenario: User Login
    @smoke
    Given I am on the ParaBank home page
    When I enter valid username and password
    And I click the "Log In" button
    Then I should be logged in successfully
