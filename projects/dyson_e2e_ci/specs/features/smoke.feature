Feature: Dyson E-commerce Smoke Tests

  Scenario: Search for a product and initiate checkout @smoke
    Given User is on the Dyson India homepage
    When User closes the subscription popup
    And User clicks on the search icon
    And User closes the search popup
