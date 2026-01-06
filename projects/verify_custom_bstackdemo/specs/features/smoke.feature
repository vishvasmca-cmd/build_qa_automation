Feature: Add to cart functionality

  @smoke
  Scenario: Add a product to the cart
    Given I am on the bstackdemo homepage
    When I click the 'Add to cart' button for the first product
    Then the product should be added to the cart
