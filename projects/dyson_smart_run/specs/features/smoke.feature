Feature: Dyson India - Smoke Tests

  Scenario: Search for a product
    @smoke
    Given User navigates to the Dyson India homepage
    When User closes the initial popup if it appears
    And User clicks on the search icon
    Then User should be able to access the search functionality
