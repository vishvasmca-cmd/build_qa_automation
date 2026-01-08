Feature: Product Search and Checkout
  As a user
  I want to search for a product and proceed to checkout
  So that I can purchase the product

  @smoke
  Scenario: Search for a dress and proceed to checkout
    Given I am on the products page
    When I search for "Dress"
    And I add a dress to the cart
    And I continue shopping
    And I go to the cart
    Then I proceed to checkout
