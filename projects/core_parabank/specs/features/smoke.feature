Feature: ParaBank Smoke Tests
  As a user of ParaBank
  I want to perform basic actions
  So that I can verify the core functionalities

  @smoke
  Scenario: Verify ParaBank Home Page
    Given I navigate to the ParaBank home page
    Then I should see the ParaBank login form

  @smoke
  Scenario: Attempt to navigate to Account History and return to Home
    Given I am on the ParaBank home page
    When I click on the "Account History" link
    Then I should be redirected to the ParaBank Web Service Definition page
    When I navigate back to the ParaBank home page
    Then I should see the ParaBank login form
