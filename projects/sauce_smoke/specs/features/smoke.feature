Feature: Smoke Test - sauce_smoke E-commerce

  This suite verifies the core functionalities of the sauce_smoke application.

  @smoke
  Scenario: User Login and Add Item to Cart
    Given I am on the login page
    When I log in with username "standard_user" and password "secret_sauce"
    Then I should be logged in and see the inventory page
    When I add "Sauce Labs Backpack" to the cart
    Then The cart badge should display "1"