Feature: Yahoo Finance Smoke Tests
  As a user,
  I want to verify the core functionalities of Yahoo Finance
  So that I can ensure the application is working as expected.

  @smoke
  Scenario: Verify Yahoo Finance Homepage
    Given I navigate to the Yahoo Finance homepage
    Then I should see the Yahoo Finance logo
    And I should see the Market Summary banner

  @smoke
  Scenario: Search for AAPL and verify quote page
    Given I am on the Yahoo Finance homepage
    When I search for AAPL
    Then I should see the Apple Inc. quote page

  @smoke
  Scenario: Verify AAPL quote price
    Given I am on the Apple Inc. quote page
    Then I should see the current price of AAPL

  @smoke
  Scenario: Navigate to AAPL Historical Data
    Given I am on the Apple Inc. quote page
    When I click on the Historical Data tab
    Then I should be on the AAPL Historical Data page
