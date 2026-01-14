Feature: Product Search and Checkout
  As a user
  I want to be able to search for a product and proceed to checkout
  So that I can purchase the product

  @smoke
  Scenario: Search for a product and add it to the cart
    Given I am on the Dyson India homepage
    When I search for "Dyson V15 Detect"
    And I click on the first product result
    Then I should see the "Add to Cart" button
    When I click on the "Add to Cart" button
    Then I should see the cart drawer opens
    When I click on the "Checkout" button
    Then I should be redirected to the checkout page
