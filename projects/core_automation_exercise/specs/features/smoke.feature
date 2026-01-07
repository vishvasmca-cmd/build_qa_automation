Feature: E-commerce Smoke Tests

  @smoke
  Scenario: Browse Products and Add to Cart
    Given I navigate to the products page
    When I search for "Dress"
    And I add the first product to the cart
    And I continue shopping
    And I add the second product to the cart
    And I navigate to the cart
    Then I should see the selected products in the cart

  @smoke
  Scenario: Proceed to Checkout
    Given I am on the cart page
    When I proceed to checkout
    Then I should be redirected to the login page
