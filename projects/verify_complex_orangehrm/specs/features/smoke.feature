Feature: OrangeHRM - Smoke Tests

  Scenario: User Login
    @smoke
    Given I am on the OrangeHRM login page
    When I enter username "Admin"
    And I enter password "admin123"
    Then I should be logged in successfully

  Scenario: Add Employee
    @smoke
    Given I am logged in as an administrator
    When I navigate to the 'PIM' section
    And I click 'Add Employee'
    And I enter First Name 'Resilience'
    And I enter Last Name 'Agent'
    And I click 'Save'
    Then I should see the Personal Details page for the new employee
