Feature: E-commerce Smoke Tests

  @smoke
  Scenario: Search for a product and proceed to checkout
    Given I am on the products page
    When I search for "Dress"
    And I add the first product to the cart
    And I proceed to checkout from the cart page
    Then I should be on the checkout page
