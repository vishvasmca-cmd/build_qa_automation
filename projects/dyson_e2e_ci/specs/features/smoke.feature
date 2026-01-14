Feature: Product Search and Add to Cart
  As a user
  I want to search for a product and add it to the cart
  So that I can purchase it

  @smoke
  Scenario: Search for Dyson V15 Detect and add to cart
    Given I am on the Dyson India homepage
    When I close the subscription popup
    And I search for "Dyson V15 Detect"
    And I click the first product result
    Then I should see the "Add to Cart" button
    When I click the "Add to Cart" button
    Then the cart drawer should open
    And I click the "Checkout" button
    Then I should be on the checkout page
