Feature: OrangeHRM Enterprise - Smoke Tests

  Scenario: Create a new employee and system user
    @smoke
    Given User is on the OrangeHRM login page
    When User logs in with valid credentials
    And User navigates to the PIM module
    And User adds a new employee with first name "FirstNameTest" and last name "LastNameTest"
    And User saves the new employee
    And User navigates to the Admin module
    And User navigates to the User Management page
    And User adds a new system user for the created employee
    Then User should be able to see the new user created successfully
