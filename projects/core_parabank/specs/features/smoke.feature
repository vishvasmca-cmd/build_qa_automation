Feature: ParaBank Smoke Tests
  As a user
  I want to perform basic checks on the ParaBank application
  So that I can ensure the core functionalities are working

  @smoke
  Scenario: Verify Login Page and Account History Link
    Given I am on the ParaBank login page
    When I click on the 'Account History' link
    Then I should be navigated to the Account History page
