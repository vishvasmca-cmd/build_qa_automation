Feature: Smoke Tests - Dyson E-commerce

  @smoke
  Scenario: Add product to cart and proceed to checkout
    Given I am on the Dyson India homepage
    When I handle the initial popup
    And I search for "Dyson V15 Detect" and select the first product
    Then I should see the "Add to Cart" button
    When I click "Add to Cart"
    Then the cart drawer should open
    When I click "Checkout"
    Then I should be on the Checkout page
