Feature: E-commerce Smoke Tests
  As a user
  I want to perform basic e-commerce operations
  So that I can verify the core functionalities of the website

  @smoke
  Scenario: Search for a product and add it to the cart
    Given I am on the products page
    When I search for "Dress"
    And I add the first product to the cart
    And I continue shopping
    Then I should see the product in the cart

  @smoke
  Scenario: Navigate to cart and proceed to checkout
    Given I have a product in the cart
    When I navigate to the cart page
    And I proceed to checkout
    Then I should be prompted to register or login
