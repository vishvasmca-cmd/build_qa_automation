Feature: OrangeHRM Login and Password Reset

  @smoke
  Scenario: Verify Login Page Elements and Forgot Password Link
    Given User navigates to the OrangeHRM login page
    Then User should see the username field
    And User should see the password field
    And User should see the login button
    And User should see the 'Forgot your password?' link

  @smoke
  Scenario: Reset Password Request
    Given User is on the OrangeHRM login page
    When User clicks on the 'Forgot your password?' link
    Then User should be redirected to the password reset page
    When User enters a valid username
    And User clicks the 'Reset Password' button
    Then User should see a password reset confirmation message

  @smoke
  Scenario: Verify Social Media Icons on Login Page
    Given User is on the OrangeHRM login page
    Then User should see social media icons
