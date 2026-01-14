Feature: Dyson E-commerce Smoke Tests

  @smoke
  Scenario: Add a product to cart and navigate to checkout
    Given I am on the Dyson India homepage
    When I close the subscribe popup
    And I click the search icon
    And I search for "Dyson V15 Detect"
    And I click the first product result
    Then I should see the "Add to Cart" button
    When I click the "Add to Cart" button
    Then the cart drawer should open
    When I click "Checkout"
    Then I should be on the checkout page
