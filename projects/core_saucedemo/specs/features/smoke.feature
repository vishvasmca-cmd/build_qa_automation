Feature: E-commerce Smoke Tests

  Scenario: Successful Login and Product Sorting
    Given User is on the login page
    When User enters valid username "standard_user"
    And User enters valid password "secret_sauce"
    And User clicks the login button
    Then User should be logged in and redirected to the inventory page
    When User sorts products by "Price (low to high)"
    Then Products should be sorted by price from low to high

  @smoke
  Scenario: Login with standard user and sort products by price
    Given User is on the login page
    When User enters username "standard_user"
    And User enters password "secret_sauce"
    And User clicks login
    Then User is redirected to inventory page
    When User sorts products by price low to high
    Then Products are sorted correctly
