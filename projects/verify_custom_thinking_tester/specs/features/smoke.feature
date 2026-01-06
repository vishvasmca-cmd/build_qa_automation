Feature: User Registration
  As a user
  I want to be able to register for a new account
  So that I can access the application

  @smoke
  Scenario: Successful user registration
    Given I am on the signup page
    When I fill in the registration form with valid data
      | firstName | lastName | email               | password   |
      | John      | Test     | test@example.com | password   |
    And I click the submit button
    Then I should be redirected to the contact list page
