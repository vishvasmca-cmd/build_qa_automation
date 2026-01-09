Feature: OrangeHRM Enterprise Smoke Tests

  Scenario: User Login
    Given User is on the login page
    When User enters valid username and password
    And User clicks on the login button
    Then User should be logged in successfully

  @smoke
  Scenario: Add New Employee
    Given User is logged in
    When User navigates to the PIM module
    And User clicks on the Add button
    And User fills in the first name and last name
    And User clicks on the Save button
    Then Employee should be added successfully

  @smoke
  Scenario: Create System User
    Given User is logged in
    When User navigates to the Admin module
    And User navigates to User Management -> Users
    And User clicks on the Add button
    And User fills in the required user details
    And User clicks on the Save button
    Then System User should be created successfully
