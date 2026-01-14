Feature: Product Search and Checkout Flow
  As a user
  I want to be able to search for a product, add it to the cart, and proceed to checkout
  So that I can purchase the desired product

  @smoke
  Scenario: Search for a product and proceed to checkout
    Given I am on the Dyson India website
    When I close the 'Subscribe' popup
    And I search for "Dyson V15 Detect"
    And I click on the first product result
    Then I should see the 'Add to Cart' button
    When I click 'Add to Cart'
    Then the cart drawer should open
    When I click 'Checkout'
    Then I should be on the checkout page
