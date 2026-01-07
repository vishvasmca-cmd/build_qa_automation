Feature: Login Page and Password Reset
  As a user
  I want to be able to access the login page and reset my password if needed
  So that I can access the application

  @smoke
  Scenario: Verify Login Page Elements and Forgot Password Link
    Given I am on the OrangeHRM login page
    Then I should see the login page elements
    When I click on the "Forgot your password?" link
    Then I should be on the password reset page
    When I enter a valid username
    And I click the "Reset Password" button
    Then I should see a password reset confirmation message
    When I click on the OrangeHRM, Inc link
    Then I should be redirected to the login page
