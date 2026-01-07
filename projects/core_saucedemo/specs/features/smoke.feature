Feature: E-commerce Smoke Tests

  Scenario: Successful Login and Sort Products
    @smoke
    Given User is on the login page
    When User logs in with valid credentials
    Then User should be redirected to the inventory page
    When User sorts products by price (low to high)
    Then Products should be sorted by price in ascending order
