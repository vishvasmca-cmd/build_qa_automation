Feature: Smoke Test - Core Functionality

  @smoke
  Scenario: User Login, Sort Products, and Add Item to Cart
    Given User is on the Swag Labs login page
    When User logs in with valid credentials "standard_user" and "secret_sauce"
    Then User should be redirected to the inventory page
    When User sorts products by price (low to high)
    And User adds the cheapest item "Sauce Labs Bike Light" to the cart
    Then The item should be added to the cart successfully
