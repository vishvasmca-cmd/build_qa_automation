Feature: OrangeHRM - Employee Management

  @smoke
  Scenario: Login and Add New Employee
    Given I am on the OrangeHRM login page
    When I log in with username "Admin" and password "admin123"
    Then I should be logged in successfully
    When I navigate to the PIM module
    And I click on 'Add Employee'
    And I enter First Name 'Resilience' and Last Name 'Agent'
    And I click 'Save'
    Then I should see the Personal Details page for the new employee
