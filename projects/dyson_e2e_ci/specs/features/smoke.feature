Feature: Dyson E-commerce Smoke Tests

  @smoke
  Scenario: Search, Add to Cart, and Checkout
    Given I am on the Dyson India homepage
    When I close the subscribe popup
    And I search for "Dyson V15 Detect"
    And I click the first product result
    Then I should see the "Add to Cart" button
    When I click "Add to Cart"
    Then the cart drawer should open
    When I click "Checkout"
    Then I should be on the checkout page
