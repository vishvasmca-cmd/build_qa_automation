Feature: ParaBank Smoke Tests

  @smoke
  Scenario: Verify successful navigation to the home page
    Given I am on the ParaBank home page
    Then I should see the "ParaBank" title

  @smoke
  Scenario: Check Account History link
    Given I am on the ParaBank home page
    When I click on the "Account History" link
    Then I should be on the "ParaBank Services" page

  @smoke
  Scenario: Navigate to About Us page
    Given I am on the ParaBank home page
    When I click on the "About Us" link
    Then I should be on the "ParaBank About Us" page
