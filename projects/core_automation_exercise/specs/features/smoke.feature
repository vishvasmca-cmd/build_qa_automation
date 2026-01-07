Feature: E-commerce Smoke Tests

  @smoke
  Scenario: Browse Products and Add to Cart
    Given User navigates to the products page
    When User searches for "Dress"
    And User adds a dress to the cart
    And User continues shopping
    And User adds another dress to the cart
