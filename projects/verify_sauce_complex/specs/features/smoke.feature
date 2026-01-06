Feature: E-commerce Smoke Tests

  Scenario: Successful Login, Add Items to Cart, and Complete Checkout
    Given I am on the login page
    When I enter username "standard_user"
    And I enter password "secret_sauce"
    And I click the login button
    Then I should be logged in and redirected to the inventory page
    When I add "Sauce Labs Backpack" to the cart
    And I add "Sauce Labs Bike Light" to the cart
    And I go to the cart page
    And I click on checkout
    And I enter first name "John"
    And I enter last name "Doe"
    And I enter zip code "12345"
    And I click continue
    And I click finish
    Then I should see the order completion message
