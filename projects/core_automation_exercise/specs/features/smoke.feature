Feature: E-commerce Smoke Tests

  @smoke
  Scenario: Browse Products, Search, Add to Cart, and Checkout
    Given User navigates to the products page
    When User searches for "Dress"
    And User adds the first dress to the cart
    Then User navigates to the cart page
