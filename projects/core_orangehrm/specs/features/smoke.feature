Feature: Login Page Verification
  As a user
  I want to verify the login page elements and functionalities
  So that I can ensure the application is working as expected

  @smoke
  Scenario: Verify Login Page Elements and Forgot Password Link
    Given I am on the OrangeHRM login page
    Then I should see the username and password fields
    And I should see the 'Forgot Your Password?' link
    When I click on the 'Forgot Your Password?' link
    Then I should be redirected to the password reset page

  @smoke
  Scenario: Verify Social Media Icons on Login Page
    Given I am on the OrangeHRM login page
    Then I should see the social media icons
