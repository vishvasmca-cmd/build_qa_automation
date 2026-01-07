Feature: Product Search and Add to Cart
  As a user
  I want to be able to search for a product and add it to my cart
  So that I can purchase the product

  @smoke
  Scenario: Search for a product and add it to the cart
    Given I am on the home page
    When I search for "Dress"
    Then I should see search results for "Dress"
    When I add the first product to the cart
    Then I should see the product in my cart
