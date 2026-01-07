Feature: core_saucedemo Smoke Tests

  @smoke
  Scenario: User Login and Sort Products by Price
    Given User is on the Saucedemo login page
    When User logs in with valid credentials
    Then User should be redirected to the inventory page
    When User sorts products by price (low to high)
    Then Products should be sorted correctly

  @smoke
  Scenario: Add a product to the cart
    Given User is on the inventory page
    When User adds the cheapest product to the cart
    Then The product should be added to the cart
