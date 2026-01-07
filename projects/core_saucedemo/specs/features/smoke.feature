Feature: core_saucedemo Smoke Tests

  @smoke
  Scenario: User Login and Sort Products by Price
    Given User is on the login page
    When User logs in with valid credentials
    Then User should be redirected to the inventory page
    When User sorts products by price (low to high)
    Then Products should be sorted by price (low to high)

  @smoke
  Scenario: Add Lowest Price Item to Cart
    Given User is on the inventory page
    When User adds the lowest price item to the cart
    Then The item should be added to the cart
