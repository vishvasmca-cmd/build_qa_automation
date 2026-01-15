Feature: Google Finance - Smoke Tests

  Scenario: Verify Homepage Load and Market Indices Display @smoke
    Given User navigates to the Google Finance homepage
    Then The Google Finance logo should be visible
    And The 'Compare Markets' section should display major indices
    And Each index card should show a numeric price and percentage change

  Scenario: Verify Search Functionality with Autosuggest @smoke
    Given User is on the Google Finance homepage
    When User clicks on the search bar
    And User types 'TES' in the search bar
    Then Tesla (TSLA) should appear in the dropdown suggestions

  Scenario: Verify Stock Detail Page Loads @smoke
    Given User searches for 'TSLA'
    When User selects Tesla (TSLA) from the search suggestions
    Then The browser should redirect to the Tesla (TSLA) detail page
    And The main stock price should be displayed
    And The 'Day's Change' should be visible

  Scenario: Verify Chart Interaction @smoke
    Given User is on the Tesla (TSLA) detail page
    When User clicks the '1D' button on the chart
    Then The graph line should appear
