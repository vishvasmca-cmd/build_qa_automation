Feature: Purchase flow
  As a user
  I want to purchase items from the store
  So that I can verify the core functionality

  @smoke
  Scenario: Complete purchase flow
    Given I am on the login page
    When I log in with username "standard_user" and password "secret_sauce"
    And I add "Sauce Labs Backpack" to the cart
    And I add "Sauce Labs Bike Light" to the cart
    Then I should be able to checkout successfully
