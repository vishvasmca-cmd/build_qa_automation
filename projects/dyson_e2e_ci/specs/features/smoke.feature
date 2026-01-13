Feature: Smoke Test - Dyson India E-commerce

  @smoke
  Scenario: Search, Add to Cart, and Checkout
    Given User navigates to the Dyson India homepage
    When User closes the 'Subscribe' popup
    And User searches for 'Dyson V15 Detect'
    And User clicks on the first product result
    Then User should see the 'Add to Cart' button
    When User clicks 'Add to Cart'
    Then The cart drawer should open
    And User clicks 'Checkout'
    Then User should be redirected to the Checkout page
