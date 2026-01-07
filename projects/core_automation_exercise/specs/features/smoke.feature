Feature: Product Search and Checkout
  As a user
  I want to search for a product and proceed to checkout
  So that I can purchase the product

  @smoke
  Scenario: Search for a dress and proceed to checkout
    Given I am on the Products page
    When I search for "Dress"
    And I add the first dress to the cart
    And I go to the cart
    Then I should be able to proceed to checkout
