Feature: OrangeHRM Smoke Tests

  @smoke
  Scenario: User Login
    Given User is on the OrangeHRM login page
    When User enters valid username "Admin" and password "admin123"
    And User clicks on the login button
    Then User should be redirected to the Dashboard page

  @smoke
  Scenario: Add New Employee
    Given User is logged in to OrangeHRM
    When User navigates to the PIM module
    And User clicks on the Add button
    And User fills in the first name as "FirstNameTest" and last name as "LastNameTest"
    And User clicks on the Save button
    Then A new employee should be added successfully

  @smoke
  Scenario: Create System User
    Given User is logged in to OrangeHRM
    When User navigates to the Admin module
    And User clicks on the User Management -> Users
    And User clicks on the Add button
    Then User should be able to create a new system user
