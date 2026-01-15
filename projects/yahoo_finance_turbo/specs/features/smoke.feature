Feature: Yahoo Finance Smoke Tests

  @smoke
  Scenario: Verify Yahoo Finance Homepage
    Given User navigates to the Yahoo Finance homepage
    Then User should see the Yahoo Finance logo
    And User should see the Market Summary banner

  @smoke
  Scenario: Navigate to News and Markets pages
    Given User is on the Yahoo Finance homepage
    When User clicks the 'News' link
    Then User should be navigated to the 'News' page
    When User clicks the 'Markets' link
    Then User should be navigated to the 'Markets' page

  @smoke
  Scenario: Search for AAPL and verify Apple Inc. page
    Given User is on the Yahoo Finance homepage
    When User searches for 'AAPL'
    Then User should be navigated to the Apple Inc. page

  @smoke
  Scenario: Verify AAPL price display
    Given User is on the Apple Inc. page
    Then User should see the current price of AAPL
