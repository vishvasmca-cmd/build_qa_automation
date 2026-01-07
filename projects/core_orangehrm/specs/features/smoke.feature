Feature: Login Page Verification
  As a user, I want to verify the login page elements and functionalities.

  @smoke
  Scenario: Verify login page elements and 'Forgot your password?' link
    Given I am on the OrangeHRM login page
    When I click the 'Forgot your password?' link
    Then I should be redirected to the password reset page
    And I navigate back to the login page

  @smoke
  Scenario: Verify social media icons on the login page
    Given I am on the OrangeHRM login page
    Then I should see social media icons
    When I click on the first social media icon
    Then a new tab should open with the corresponding social media page
