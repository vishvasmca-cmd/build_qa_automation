Feature: Dyson Website Smoke Tests

  @smoke
  Scenario: Search for a product and verify PDP elements
    Given User navigates to the Dyson India website
    When User closes the 'Subscribe' popup if it appears
    And User clicks on the search icon
    And User clicks on the search icon again to enable input
    And User searches for "Dyson V15 Detect"
    Then User should see the 'Add to Cart' button on the product details page
