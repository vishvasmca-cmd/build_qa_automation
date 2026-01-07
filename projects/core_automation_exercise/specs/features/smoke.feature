Feature: Product Search and Add to Cart
  As a user
  I want to search for a product and add it to the cart
  So that I can purchase the product

  @smoke
  Scenario: Search for a dress and add it to the cart
    Given I am on the products page
    When I search for "Dress"
    And I add the first dress to the cart
    And I continue shopping
    And I add the second dress to the cart
