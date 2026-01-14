Feature: Dyson E-commerce Smoke Tests

  @smoke
  Scenario: Search, Add to Cart, and Checkout
    Given User navigates to the Dyson India website
    When User closes the subscription popup
    And User searches for "Dyson V15 Detect"
    And User clicks on the first product result
    Then User should see the "Add to Cart" button
    When User clicks on "Add to Cart"
    Then The cart drawer should open
    When User clicks on "Checkout"
    Then User should be redirected to the Checkout page
