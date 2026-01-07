Feature: ParaBank Smoke Tests
  As a user of ParaBank
  I want to perform basic actions
  So that I can verify the core functionality

  @smoke
  Scenario: Verify ParaBank Home Page Load
    Given I navigate to the ParaBank home page
    Then I should see the ParaBank logo
    And I should see the "Register" link

  @smoke
  Scenario: Attempt to navigate to Account History and return to Home
    Given I am on the ParaBank home page
    When I click on the "Account History" link
    Then I should be redirected back to the ParaBank home page
