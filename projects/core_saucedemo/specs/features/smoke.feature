Feature: Smoke Tests for core_saucedemo

  @smoke
  Scenario: User Login and Add Item to Cart
    Given I am on the login page
    When I enter valid username "standard_user"
    And I enter valid password "secret_sauce"
    And I click the login button
    Then I should be logged in and see the inventory page
    When I sort products by "Price (low to high)"
    And I add the lowest price item to the cart
    Then The item should be added to the cart
