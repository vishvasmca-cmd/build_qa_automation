<<<<<<< Updated upstream
Feature: Product Search and Checkout
  As a user
  I want to search for a product and proceed to checkout
  So that I can purchase the product

  @smoke
  Scenario: Search for 'Dress', add to cart, and proceed to checkout
    Given I navigate to the Products page
    When I search for 'Dress'
    And I add the first dress to the cart
    And I continue shopping
=======
Feature: E-commerce Smoke Tests
  As a user
  I want to perform basic e-commerce operations
  So that I can verify the core functionalities are working

  @smoke
  Scenario: Browse products, search, add to cart, and checkout
    Given I am on the products page
    When I search for "Dress"
    And I add the first dress to the cart
>>>>>>> Stashed changes
    And I go to the cart
    Then I proceed to checkout
