Feature: Dyson E-commerce Smoke Tests

  Scenario: Search for a product and add it to the cart
    Given User is on the Dyson India homepage
    When User closes the subscription popup
    And User searches for "Dyson V15 Detect"
    And User clicks on the first product result
    Then User should see the "Add to cart" button
    When User clicks the "Add to cart" button
    Then The cart drawer should open
    And User clicks on the "Checkout" button
    Then User should be redirected to the checkout page
