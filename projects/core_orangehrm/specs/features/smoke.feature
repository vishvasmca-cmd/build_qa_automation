Feature: Login Page and Password Reset
  As a user,
  I want to access the login page and initiate the password reset process,
  So that I can log in or recover my account.

  @smoke
  Scenario: Verify Login Page and Initiate Password Reset
    Given I am on the OrangeHRM login page
    When I click the "Forgot your password?" link
    And I fill the username field with "Admin"
    And I click the "Reset Password" button
    Then I navigate back to the login page by clicking the OrangeHRM link
