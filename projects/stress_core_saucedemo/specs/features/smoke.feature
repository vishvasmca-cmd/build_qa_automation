Feature: E-commerce Smoke Tests

  @smoke
  Scenario: User Login and Sort Products
    Given User is on the login page
    When User logs in with valid credentials
    Then User should be redirected to the inventory page

  @smoke
  Scenario: Sort products by price low to high
    Given User is logged in on the inventory page
    When User sorts products by price low to high
    Then Products should be sorted by price low to high
