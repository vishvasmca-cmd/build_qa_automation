Feature: E-commerce Smoke Tests

  @smoke
  Scenario: User login, sort products by price, add to cart
    Given User is on the login page
    When User enters valid username "standard_user"
    And User enters valid password "secret_sauce"
    And User clicks the login button
    Then User should be logged in and redirected to the inventory page
    When User clicks on the sort dropdown
    And User selects "Price (low to high)" from the sort options
    Then Products should be sorted by price (low to high)
