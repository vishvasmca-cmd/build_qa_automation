Feature: Smoke Tests for core_saucedemo

  Scenario: User Login and Sort Products by Price
    Given User is on the login page
    When User enters valid username "standard_user"
    And User enters valid password "secret_sauce"
    And User clicks on the login button
    Then User should be logged in and redirected to the inventory page
    When User sorts products by price "Price (low to high)"
    Then Products should be sorted by price from low to high

