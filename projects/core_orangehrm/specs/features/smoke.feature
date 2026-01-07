Feature: Login and Password Reset
  As a user
  I want to be able to log in and reset my password
  So that I can access the system

  @smoke
  Scenario: Verify Login Page Elements and Forgot Password Link
    Given I am on the OrangeHRM login page
    Then I should see the login page elements
    When I click on the "Forgot your password?" link
    Then I should be redirected to the password reset page

  @smoke
  Scenario: Reset Password
    Given I am on the password reset page
    When I enter a username
    And I click the "Reset Password" button
    Then I should see a password reset confirmation message

  @smoke
  Scenario: Verify Social Media Icons on Login Page
    Given I am on the OrangeHRM login page
    Then I should see the social media icons
