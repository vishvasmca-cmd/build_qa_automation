Feature: E-commerce Smoke Tests - core_saucedemo

  Scenario: User Login, Sort Products, Add to Cart, and Begin Checkout
    @smoke
    Given User is on the Saucedemo login page
    When User logs in with username "standard_user" and password "secret_sauce"
    Then User should be logged in and redirected to the inventory page
    When User sorts products by "Price (low to high)"
    Then Products should be sorted by price from low to high
