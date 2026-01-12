Feature: Product Search and Checkout Flow
  As a user
  I want to be able to search for a product, add it to the cart, and proceed to checkout
  So that I can purchase the product

  @smoke
  Scenario: Search for a product and initiate checkout
    Given I am on the Dyson India homepage
    When I close the subscription popup
    And I search for "Dyson V15 Detect"
    And I click on the first product result
    Then I should see the "Add to Cart" button
    When I click on the "Add to Cart" button
    Then I should see the cart drawer
    When I click on the "Checkout" button
    Then I should be on the checkout page
