Feature: Dyson India - Smoke Tests

  @smoke
  Scenario: Search for Dyson V15 Detect and verify 'Add to Cart' button
    Given User navigates to the Dyson India homepage
    When User closes the initial popup
    And User clicks on the search icon
    Then User should see the search input field
    #And User enters "Dyson V15 Detect" in the search input
    #And User presses Enter
    #Then User should see search results for "Dyson V15 Detect"
    #And User clicks on the "Dyson V15 Detect" product
    #Then User should see the "Add to Cart" button on the product page
