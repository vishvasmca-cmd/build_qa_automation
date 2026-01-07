Feature: Password Reset Functionality
  As a user, I want to be able to reset my password so I can regain access to my account.

  @smoke
  Scenario: Initiate password reset
    Given I am on the OrangeHRM login page
    When I click the "Forgot your password?" link
    And I fill in the username field with "testuser"
    And I click the "Reset Password" button
    Then I should be able to navigate back to the login page
