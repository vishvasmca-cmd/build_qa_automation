Feature: Product Search and Checkout
  As a user
  I want to search for a product, add it to the cart, and proceed to checkout
  So that I can purchase the product

  @smoke
  Scenario: Search for a product and proceed to checkout
    Given I am on the Dyson India homepage
    When I close the subscription popup
    And I search for "Dyson V15 Detect"
    And I click on the first product result
    Then I should see the "Add to cart" button
    When I click the "Add to cart" button
    And I click the "Continue to basket" button
    And I click the "Continue to checkout" button
    Then I should be on the checkout page
