Feature: Login Page Verification
  As a user,
  I want to verify the login page elements and functionality
  So that I can ensure the application is working as expected.

  @smoke
  Scenario: Verify login page elements and navigate to forgot password page
    Given I am on the OrangeHRM login page
    When I click on the "Forgot your password?" link
    Then I should be redirected to the password reset page

  @smoke
  Scenario: Verify reset password functionality
    Given I am on the password reset page
    When I enter a username
    And I click the "Reset Password" button
    Then I should see a password reset confirmation message

  @smoke
  Scenario: Verify social media icons are visible on the login page
    Given I am on the OrangeHRM login page
    Then I should see social media icons
