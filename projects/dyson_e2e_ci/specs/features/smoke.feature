Feature: E-commerce Flow
  As a user
  I want to be able to search for a product, add it to the cart, and proceed to checkout
  So that I can purchase the desired product

  @smoke
  Scenario: Purchase a product
    Given I am on the Dyson India homepage
    When I close the subscription popup
    And I search for "Dyson V15 Detect"
    And I click on the first product result
    Then I should see the "Add to cart" button
    When I click on the "Add to cart" button
    And I click on the "Continue to basket" button
    Then I should reach the checkout page
