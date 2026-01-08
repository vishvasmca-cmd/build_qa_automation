Feature: Login Page Verification
  As a user
  I want to verify the login page elements and functionality
  So that I can ensure the application is accessible and ready for use

  @smoke
  Scenario: Verify Login Page Loads Successfully
    Given I navigate to the OrangeHRM login page
    Then the login page should load successfully
