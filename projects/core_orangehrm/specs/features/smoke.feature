Feature: Login Page Verification and Password Reset
  As a user,
  I want to verify the login page elements and the 'Forgot your password?' functionality
  So that I can ensure the core functionality is working as expected.

  @smoke
  Scenario: Verify Login Page Elements and Navigate to Forgot Password
    Given I am on the OrangeHRM login page
    Then I should see the username and password fields
    And I should see the 'Forgot your password?' link
    When I click on the 'Forgot your password?' link
    Then I should be redirected to the password reset page

  @smoke
  Scenario: Reset Password Flow
    Given I am on the password reset page
    When I fill in the username field with "testuser"
    And I click the 'Reset Password' button
    Then I should be redirected to the password reset confirmation page

  @smoke
  Scenario: Verify Social Media Icons on Login Page
    Given I am on the OrangeHRM login page
    When I scroll to the bottom of the page
    Then I should see the social media icons
    When I click on the first social media icon
    Then a new tab should open with the corresponding social media page
