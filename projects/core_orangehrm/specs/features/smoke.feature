Feature: Login Page Verification and Password Reset

  As a user
  I want to access the login page and initiate the password reset process
  So that I can verify the core functionality is working

  @smoke
  Scenario: Verify Login Page and Initiate Password Reset
    Given I am on the OrangeHRM login page
    When I click on the "Forgot your password?" link
    Then I should be redirected to the password reset page
    When I fill the username field with "testuser"
    And I click the "Reset Password" button
    Then I should see a message indicating that a reset password link has been sent
