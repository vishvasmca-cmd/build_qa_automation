Feature: Product Search and Add to Cart
  As a user,
  I want to search for a product and add it to my cart,
  So that I can purchase the product.

  @smoke
  Scenario: Search for 'Dress' and add to cart
    Given I navigate to the Products page
    When I search for 'Dress'
    And I add the first dress to the cart
    Then I should be able to continue shopping
