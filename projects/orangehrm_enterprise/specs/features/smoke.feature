Feature: OrangeHRM Smoke Tests

  Scenario: Login to OrangeHRM and Add Employee and Create User
    @smoke
    Given I am on the OrangeHRM login page
    When I log in with valid credentials
    Then I should be logged in successfully
    When I navigate to the PIM module and add a new employee "FirstNameTest" "LastNameTest"
    Then the new employee should be added successfully
    When I navigate to the Admin module and create a system user for the new employee
    Then the system user should be created successfully
