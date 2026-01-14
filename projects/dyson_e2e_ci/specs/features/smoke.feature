Feature: Product Search and Checkout
  As a user, I want to be able to search for a product, add it to the cart, and proceed to checkout.

  @smoke
  Scenario: Search for Dyson V15 Detect and proceed to checkout
    Given I am on the Dyson India homepage
    When I search for "Dyson V15 Detect"
    And I click on the first product result
    Then I should see the "Add to Cart" button
    When I click on "Add to Cart"
    Then I should see the cart drawer open
    When I click on "Checkout"
    Then I should be on the Checkout page
