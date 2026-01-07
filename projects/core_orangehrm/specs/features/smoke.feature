Feature: Login Page and Password Reset
  As a user, I want to verify the login page elements and the password reset functionality.

  @smoke
  Scenario: Verify login page elements and navigate to password reset
    Given I am on the OrangeHRM login page
    When I click on the "Forgot your password?" link
    Then I should be redirected to the password reset page

  @smoke
  Scenario: Request password reset with valid username
    Given I am on the OrangeHRM password reset page
    When I enter a valid username "Admin"
    And I click the "Reset Password" button
    Then I should see a confirmation message that a reset link has been sent

  @smoke
  Scenario: Verify social media icons are present on the login page
    Given I am on the OrangeHRM login page
    Then I should see social media icons
