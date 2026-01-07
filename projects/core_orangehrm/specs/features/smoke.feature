Feature: Login Page Verification
  As a user,
<<<<<<< Updated upstream
  I want to verify the login page elements and the 'Forgot your password?' functionality
  So that I can ensure the basic functionality of the login page is working.

  @smoke
  Scenario: Verify Login Page Elements and Navigate to Forgot Password
    Given I am on the OrangeHRM login page
    When I click on the 'Forgot your password?' link
    Then I should be on the password reset request page

  @smoke
  Scenario: Request Password Reset
    Given I am on the password reset request page
    When I fill the username field with "testuser"
    And I click the 'Reset Password' button
    Then I should see a confirmation message indicating that the reset link has been sent

  @smoke
  Scenario: Verify Social Media Icons on Login Page
    Given I am on the OrangeHRM login page
    When I scroll down to the bottom of the page
    Then I should see the social media icons
    And I click on the first social media icon
=======
  I want to verify the login page elements and functionality
  So that I can ensure the core functionality is working as expected.

  @smoke
  Scenario: Verify Login Page Elements and Forgot Password Link
    Given I am on the login page
    Then I should see the login page elements
    When I click on the "Forgot your password?" link
    Then I should be redirected to the password reset page

  @smoke
  Scenario: Verify Social Media Icons on Login Page
    Given I am on the login page
    Then I should see the social media icons
    When I click on the first social media icon
>>>>>>> Stashed changes
    Then I should be redirected to the corresponding social media page
