Feature: Login Page Functionality
  As a user, I want to verify the login page elements and the 'Forgot your password?' link.

  @smoke
  Scenario: Verify elements and navigate to the password reset page
    Given I am on the OrangeHRM login page
    When I click the "Forgot your password?" link
    Then I should be on the password reset page

  @smoke
  Scenario: Reset password flow
    Given I am on the OrangeHRM password reset page
    When I fill the username field with "Admin"
    And I click the "Reset Password" button
    Then I should be navigated back to the login page by clicking on the OrangeHRM, Inc link

  @smoke
  Scenario: Verify login page elements
    Given I am on the OrangeHRM login page
    Then I should see the username field
    And I should see the password field
    And I should see the login button
    And I should see the "Forgot your password?" link
