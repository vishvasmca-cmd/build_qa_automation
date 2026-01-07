Feature: Product Search and Checkout
  As a user
  I want to search for a product and proceed to checkout
  So that I can purchase the product

  @smoke
<<<<<<< Updated upstream
  Scenario: Search for a dress and proceed to checkout
    Given I am on the products page
    When I search for "Dress"
    And I add the first product to the cart
    And I continue shopping
    And I go to the cart page
    Then I proceed to checkout
=======
  Scenario: Search for a dress and add it to the cart
    Given I am on the products page
    When I search for "Dress"
    And I add the first dress to the cart
    Then I continue shopping
>>>>>>> Stashed changes
