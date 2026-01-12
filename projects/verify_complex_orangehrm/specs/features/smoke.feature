Feature: OrangeHRM Smoke Tests

  @smoke
  Scenario: Login and Add Employee
    Given I am on the OrangeHRM login page
    When I enter username "Admin"
    And I enter password "admin123"
    And I click the login button
    And I click the PIM menu
    And I click the Add Employee button
    And I enter First Name "Resilience"
    And I enter Last Name "Agent"
    And I click the Save button
    Then I should see the Personal Details page for the new employee
