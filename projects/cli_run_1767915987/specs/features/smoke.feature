Feature: ParaBank Smoke Tests

  @smoke
  Scenario: Successful User Registration
    Given I am on the ParaBank home page
    When I click the "Register" link
    And I fill in the registration form with valid data
    Then I should be redirected to the "Open New Account" page

  @smoke
  Scenario: Successful User Login
    Given I am on the ParaBank home page
    When I enter valid username and password
    And I click the "Log In" button
    Then I should be logged in successfully
