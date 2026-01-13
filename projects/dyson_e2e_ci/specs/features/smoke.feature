Feature: Dyson E-commerce Smoke Tests

  @smoke
  Scenario: Search for a product and add it to the cart
    Given User navigates to the Dyson India homepage
    When User closes the subscription popup
    And User searches for "Dyson V15 Detect"
    And User clicks on the first product result
    Then User should see the "Add to Cart" button
    When User clicks on the "Add to Cart" button
    Then The cart drawer should open
    When User clicks on the "Checkout" button
    Then User should be redirected to the Checkout page
