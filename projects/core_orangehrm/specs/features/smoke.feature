Feature: Login Page Verification and Password Reset
  As a user, I want to be able to access the login page, use the "Forgot your password?" link, and see social media icons.

  @smoke
  Scenario: Verify Login Page Elements and Forgot Password Link
    Given I am on the OrangeHRM login page
    When I click on the "Forgot your password?" link
    Then I should be redirected to the password reset page

  @smoke
  Scenario: Reset Password Request
    Given I am on the OrangeHRM password reset page
    When I enter a username "testuser"
    And I click the "Reset Password" button
    Then I should see a confirmation message indicating that the password reset process has been initiated

  @smoke
  Scenario: Verify Social Media Icons on Login Page
    Given I am on the OrangeHRM login page
    Then I should see the social media icons (LinkedIn, Facebook, Twitter, YouTube)
