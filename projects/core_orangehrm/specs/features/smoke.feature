Feature: Login Page Verification and Password Reset
  As a user, I want to verify the login page elements and the password reset functionality.

  @smoke
  Scenario: Verify access to the login page and navigation to password reset
    Given I am on the OrangeHRM login page
    When I click the "Forgot your password?" link
    Then I should be navigated to the password reset page

  @smoke
  Scenario: Reset password request
    Given I am on the OrangeHRM password reset page
    When I enter a username
    And I click the "Reset Password" button
    Then I should be navigated back to the login page
