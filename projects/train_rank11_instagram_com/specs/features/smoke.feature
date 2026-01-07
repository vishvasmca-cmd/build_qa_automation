Feature: Instagram Login Page - Smoke Tests
  As a user, I want to see the key elements on the Instagram login page
  So that I can start using the application

  @smoke
  Scenario: Verify presence of key elements on the login page
    Given I am on the Instagram login page
    Then I should see the "Log in" button
    And I should see the "Sign up" link
    And I should see the "Forgot password?" link
    And I should see the "Log in with Facebook" button
