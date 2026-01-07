Feature: ParaBank Smoke Tests

  @smoke
  Scenario: Verify ParaBank Home Page Loads
    Given I navigate to the ParaBank home page
    Then I should see the ParaBank logo
    And I should see the "Register" link
    And I should see the "Forgot login info" link

  @smoke
  Scenario: Check Account History Link
    Given I am on the ParaBank home page
    When I click on the "Account History" link
    Then I should be redirected to the account history page

  @smoke
  Scenario: Navigate to About Us Page
    Given I am on the ParaBank home page
    When I click on the "About Us" link
    Then I should be redirected to the about us page
