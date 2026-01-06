Feature: User Signup
  As a user
  I want to sign up for an account
  So that I can access the application's features

  @smoke
  Scenario: Navigate to the signup page
    Given I am on the home page
    When I click the "Sign up" button
    Then I should be on the signup page
