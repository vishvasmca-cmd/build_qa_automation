Feature: Product Search and Add to Cart
  As a user
  I want to be able to search for a product and add it to the cart
  So that I can purchase the product

  @smoke
  Scenario: Search for a product and add it to cart
    Given I am on the Dyson India homepage
    When I close the subscription popup
    And I search for "Dyson V15 Detect"
    And I click on the first product result
    Then I should see the "Add to Cart" button
    When I click on the "Add to Cart" button
    Then the cart drawer should open
    And I click on the "Checkout" button
    Then I should be redirected to the checkout page
