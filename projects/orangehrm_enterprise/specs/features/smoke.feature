Feature: OrangeHRM Smoke Tests
  As a QA Engineer
  I want to perform smoke tests on OrangeHRM
  So that I can ensure the core functionalities are working as expected

  @smoke
  Scenario: Login, Add Employee, and Create System User
    Given I am on the OrangeHRM login page
    When I log in with valid credentials
    And I navigate to the PIM module
    And I add a new employee with first name "FirstNameTest" and last name "LastNameTest"
    And I save the employee information
    And I navigate to the Admin module
    And I navigate to the User Management page
    And I add a system user for the new employee
    Then the system user should be created successfully
