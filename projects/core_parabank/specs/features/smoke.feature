Feature: ParaBank Smoke Tests
  As a user of ParaBank
  I want to perform basic actions
  So that I can verify the core functionality

  @smoke
  Scenario: Navigate to About Us and Back Home
    Given I am on the ParaBank home page
    When I click on the "About Us" link
    Then I should be on the "About Us" page
    When I click on the "Home" link
    Then I should be on the ParaBank home page

  @smoke
  Scenario: Navigate to Account History
    Given I am on the ParaBank home page
    When I click on the "Account History" link
    Then I should be on the Account History page
