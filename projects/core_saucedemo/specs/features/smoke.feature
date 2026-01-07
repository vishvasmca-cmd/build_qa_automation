Feature: E-commerce Smoke Tests

  Scenario: User Login and Product Sorting @smoke
    Given User is on the login page
    When User logs in with valid credentials
    Then User should be logged in successfully
    When User sorts products by price (low to high)
    Then Products should be sorted by price (low to high)

  Scenario: Add item to cart and view cart summary @smoke
    Given User is logged in
    When User adds an item to the cart
    Then The item should be added to the cart
    When User views the cart summary
    Then Cart summary should be displayed correctly

  Scenario: Complete a purchase @smoke
    Given User has items in the cart
    When User completes the checkout process
    Then The purchase should be completed successfully
