Feature: Login and View Financial Table
  As a user, I want to log in to the application and view the financial table.

  @smoke
  Scenario: Successful login and display of financial table
    Given I am on the login page
    When I enter username "test"
    And I enter password "password"
    And I click the Sign in button
    Then I should be logged in and see the financial table