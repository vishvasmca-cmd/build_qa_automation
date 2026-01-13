Feature: Shopping Cart
  As a user
  I want to be able to log in and add items to my cart
  So that I can purchase items from the store

  @smoke
  Scenario: Login and Add Item to Cart
    Given I am on the login page
    When I log in with username "standard_user" and password "secret_sauce"
    Then I should be logged in successfully
    When I add "Sauce Labs Backpack" to the cart
    Then the item should be added to the cart
