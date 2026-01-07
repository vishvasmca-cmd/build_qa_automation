Feature: OrangeHRM Login and Password Reset
  As a user, I want to be able to access the login page, reset my password, and view social media icons.

  @smoke
  Scenario: Verify Login Page Elements and Forgot Password Functionality
    Given I am on the OrangeHRM login page
    When I click on the "Forgot your password?" link
    Then I should be on the password reset page

  @smoke
  Scenario: Reset Password Flow
    Given I am on the password reset page
    When I fill the username field with "testuser"
    And I click the "Reset Password" button
    Then I should be on the password reset confirmation page

  @smoke
  Scenario: Navigate back to Login Page from Password Reset Confirmation
    Given I am on the password reset confirmation page
    When I click the "OrangeHRM, Inc" link
    Then I should be redirected to the OrangeHRM login page

  @smoke
  Scenario: Verify Social Media Icons on Login Page
    Given I am on the OrangeHRM login page
    Then I should see social media icons
