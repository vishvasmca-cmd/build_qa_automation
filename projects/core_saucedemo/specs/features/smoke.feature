Feature: E-commerce Smoke Tests

  @smoke
  Scenario: User Login and Product Sorting
    Given User is on the login page
    When User enters valid username "standard_user"
    And User enters valid password "secret_sauce"
    And User clicks the login button
    Then User should be logged in and redirected to the inventory page
    When User sorts products by "Price (low to high)"
    Then Products should be sorted by price from low to high
