Feature: Product Search and Add to Cart
  As a user
  I want to be able to search for a product and add it to my cart
  So that I can purchase the product

  @smoke
  Scenario: Search for a dress and add it to the cart
    Given I am on the home page
    When I navigate to the products page
    And I search for "Dress"
    And I add the first dress to the cart
    And I navigate to the cart page
    Then I should see the dress in my cart
