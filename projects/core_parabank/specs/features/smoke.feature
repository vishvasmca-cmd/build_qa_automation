Feature: ParaBank Smoke Tests
  As a user
  I want to perform basic functionalities
  So that I can ensure the core features are working

  @smoke
  Scenario: Verify ParaBank Home Page Navigation
    Given I am on the ParaBank home page
    Then I should see the "ParaBank" title

  @smoke
  Scenario: Attempt to navigate to Account History and return to home page
    Given I am on the ParaBank home page
    When I click on "Account History" link
    Then I should be navigated back to the ParaBank home page
