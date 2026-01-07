Feature: E-commerce Smoke Tests - core_saucedemo

  @smoke
  Scenario: User Login and Product Sorting
    Given User is on the login page
    When User logs in with valid credentials
    Then User should be logged in successfully
    When User sorts products by price (low to high)
    Then Products should be sorted correctly
