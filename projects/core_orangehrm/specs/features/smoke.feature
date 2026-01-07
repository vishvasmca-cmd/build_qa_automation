Feature: Login Page Verification
  As a user
  I want to verify the login page elements and functionality
  So that I can ensure the application is working as expected

  @smoke
  Scenario: Verify Login Page Elements and Functionality
    Given I am on the login page
    Then I should see the login page elements
    When I click on the "Forgot your password?" link
    Then I should be redirected to the password reset page
    And I fill the username field with "Admin"
    And I click the "Reset Password" button
    Then I should be redirected to the password reset confirmation page
    When I navigate back to the login page
    Then I should see the social media icons
    When I click on the first social media icon
    Then I should be redirected to the corresponding social media page
