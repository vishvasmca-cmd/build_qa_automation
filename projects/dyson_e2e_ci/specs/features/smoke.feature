Feature: Product Purchase Flow
  As a customer
  I want to be able to search for a product, add it to the cart, and proceed to checkout
  So that I can purchase the desired product

  @smoke
  Scenario: Search, Add to Cart, and Checkout
    Given I am on the Dyson India homepage
    When I close the subscription popup
    And I search for "Dyson V15 Detect"
    And I click on the first product result
    Then the "Add to cart" button should be visible
    When I click the "Add to cart" button
    Then I should be able to navigate to the checkout page
