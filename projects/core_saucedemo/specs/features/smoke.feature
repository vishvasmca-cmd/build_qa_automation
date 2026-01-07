Feature: E-commerce Smoke Tests

  Scenario: User Login and Add Item to Cart
    @smoke
    Given User is on the login page
    When User logs in with valid credentials
    Then User should be logged in successfully
    When User sorts products by price (low to high)
    Then Products should be sorted by price
    When User adds the lowest-priced item to the cart
    Then The item should be added to the cart
