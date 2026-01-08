Feature: OrangeHRM Smoke Tests

  Scenario: Successful Login, Add Employee, and Create System User
    @smoke
    Given I am on the OrangeHRM login page
    When I log in with valid credentials
    And I navigate to the PIM module
    And I add a new employee with first name "FirstNameTest" and last name "LastNameTest"
    And I navigate to the Admin module
    And I create a system user for the new employee
    Then the system user should be created successfully
