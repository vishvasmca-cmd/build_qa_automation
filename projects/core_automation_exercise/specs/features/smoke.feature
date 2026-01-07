Feature: Product Browsing and Checkout
  As a user
  I want to browse products, add to cart, and proceed to checkout
  So that I can purchase items easily

  @smoke
  Scenario: Browse products and add a dress to cart
    Given I am on the products page
    When I search for "Dress"
    And I add the first dress to the cart
    And I proceed to the cart
    Then I should be able to proceed to checkout
