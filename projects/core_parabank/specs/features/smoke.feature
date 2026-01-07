Feature: ParaBank Smoke Tests
  As a user, I want to perform basic actions on the ParaBank website to ensure core functionalities are working.

  @smoke
  Scenario: Verify successful navigation to the About Us page
    Given I am on the ParaBank home page
    When I click on the "About Us" link
    Then I should be navigated to the "About Us" page

  @smoke
  Scenario: Verify navigation to Account History page
    Given I am on the ParaBank home page
    When I click on the "Account History" link
    Then I should be navigated to the Account History page
