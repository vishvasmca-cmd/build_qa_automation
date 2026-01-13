Feature: Employee Management - Smoke Tests
  As an administrator
  I want to be able to add a new employee
  So that I can manage employee information

  @smoke
  Scenario: Add a new employee successfully
    Given I am on the OrangeHRM login page
    When I log in with username "Admin" and password "admin123"
    And I navigate to the PIM module
    And I click on the Add button
    And I enter First Name "Resilience" and Last Name "Agent"
    And I click Save
    Then I should be on the Personal Details page for the new employee
