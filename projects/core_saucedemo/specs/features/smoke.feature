Feature: E-commerce Smoke Tests

  @smoke
  Scenario: User Login and Product Sorting
    Given User is on the Saucedemo login page
    When User enters valid username "standard_user"
    And User enters valid password "secret_sauce"
    And User clicks the login button
    Then User should be logged in and redirected to the inventory page
    When User sorts products by price (low to high)
    Then Products should be sorted by price (low to high)

  @smoke
  Scenario: Add cheapest product to cart
    Given User is logged in on the inventory page
    When User adds the cheapest product to the cart
    Then The product should be added to the cart

  @smoke
  Scenario: Complete a purchase
    Given User has items in the cart
    When User proceeds to checkout
    And User enters shipping information
    And User completes the purchase
    Then User should see a confirmation message
