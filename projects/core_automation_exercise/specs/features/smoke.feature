Feature: E-commerce Smoke Tests

  @smoke
  Scenario: Browse Products, Search, Add to Cart, and Checkout
    Given User navigates to the Products page
    When User searches for "Dress"
    And User adds the first displayed product to the cart
    And User navigates to the cart
    And User proceeds to checkout
    Then User should be redirected to the login page
