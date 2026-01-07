Feature: Product Search and Checkout
  As a user
  I want to search for a product and proceed to checkout
  So that I can purchase the product

  @smoke
  Scenario: Search for a product and proceed to checkout
    Given I navigate to the Products page
    When I search for "Dress"
    And I add the first product to the cart
    And I proceed to checkout
    Then I should be on the checkout page
