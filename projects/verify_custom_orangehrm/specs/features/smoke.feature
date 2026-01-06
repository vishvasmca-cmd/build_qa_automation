Feature: OrangeHRM Login Page
  As a user
  I want to access the OrangeHRM login page
  So that I can log in to the application

  @smoke
  Scenario: Verify OrangeHRM login page loads successfully
    Given I navigate to the OrangeHRM login page
    Then I should see the OrangeHRM login page