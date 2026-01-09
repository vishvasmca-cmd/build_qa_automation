Feature: OrangeHRM Smoke Tests

  Scenario: Successful Login and Employee Onboarding
    @smoke
    Given I am on the OrangeHRM login page
    When I log in with username "Admin" and password "admin123"
    Then I should be logged in successfully

    When I navigate to the PIM module
    And I click the Add button
    And I fill in the employee's first name with "FirstNameTest"
    And I fill in the employee's last name with "LastNameTest"
    And I click the Save button
    Then the employee should be added successfully

    When I navigate to the Admin module
    And I navigate to the User Management page
    And I click the Add button to create a new user
    Then I should be able to create a new system user for the employee
