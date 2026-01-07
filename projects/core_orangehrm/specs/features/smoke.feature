Feature: Login Page Verification and Password Reset
  As a user, I want to be able to reset my password if I forget it and see social media icons on the login page.

  @smoke
  Scenario: Reset password flow and verify social media icons
    Given I am on the OrangeHRM login page
    When I click the "Forgot your password?" link
    And I fill the username field with "Admin"
    And I click the "Reset Password" button
    And I navigate back to the login page
    Then I should see the social media icons
