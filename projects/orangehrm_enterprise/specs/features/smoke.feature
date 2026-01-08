Feature: OrangeHRM Smoke Tests

  @smoke
  Scenario: User can successfully log in, add an employee, and create a system user
    Given User is on the OrangeHRM login page
    When User enters valid username and password
    And User clicks on the login button
    Then User should be logged in successfully

    When User navigates to the PIM module
    And User clicks on the Add button to add a new employee
    And User fills in the first name as "FirstNameTest"
    And User fills in the last name as "LastNameTest"
    And User clicks the Save button
    Then The employee should be added successfully

    When User navigates to the Admin module
    And User navigates to the User Management page
    And User clicks on the Users page
    And User clicks on the Add button to add a new system user
    And User clicks the Save button
    Then The system user should be created successfully
