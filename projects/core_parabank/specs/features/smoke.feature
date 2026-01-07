Feature: ParaBank Smoke Tests

  @smoke
  Scenario: Navigate to About Us and Back Home
    Given I am on the ParaBank home page
    When I click the "About Us" link
    Then I should be on the "About Us" page
    When I click the "Home" link
    Then I should be on the ParaBank home page

  @smoke
  Scenario: Navigate to Account History
    Given I am on the ParaBank home page
    When I click the "Account History" link
    Then I should be on the "Account History" page or an error page
