Feature: Product Search and Checkout
  As a user,
  I want to search for a product, add it to the cart, and proceed to checkout.

  @smoke
  Scenario: Search for a dress and proceed to checkout
    Given I am on the products page
    When I search for "Dress"
    And I add the first dress to the cart
    And I go to the cart
    Then I proceed to checkout