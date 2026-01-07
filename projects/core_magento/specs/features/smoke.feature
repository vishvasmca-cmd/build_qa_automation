Feature: E-commerce Smoke Tests

  Scenario: Navigate to the Home Page
    Given User navigates to the home page
    Then The home page should load successfully

  @smoke
  Scenario: Search for a product
    Given User is on the home page
    When User searches for "Watch"
    Then Search results page should be displayed
