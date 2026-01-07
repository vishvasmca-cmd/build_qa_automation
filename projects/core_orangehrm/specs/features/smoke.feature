Feature: Login Page Verification

  @smoke
  Scenario: Verify Login Page Elements
    Given I am on the OrangeHRM login page
    Then I should see the username field
    And I should see the password field
    And I should see the login button

  @smoke
  Scenario: Verify 'Forgot Password' Link
    Given I am on the OrangeHRM login page
    When I click the 'Forgot your password?' link
    Then I should be redirected to the password reset page

  @smoke
  Scenario: Verify Social Media Icons
    Given I am on the OrangeHRM login page
    When I scroll to the bottom of the page
    Then I should see the social media icons
