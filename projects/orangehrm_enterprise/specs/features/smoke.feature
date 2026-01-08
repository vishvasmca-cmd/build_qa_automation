Feature: OrangeHRM Smoke Tests

  @smoke
  Scenario: Successfully add a new employee and create a system user
    Given User is on the OrangeHRM login page
    When User logs in with valid credentials
    And User navigates to the PIM module
    And User adds a new employee with first name "FirstNameTest" and last name "LastNameTest"
    And User navigates to the Admin module
    And User creates a system user for the new employee
    Then The new employee and system user should be created successfully
