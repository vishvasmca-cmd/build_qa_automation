Feature: SauceDemo Order Placement
  As a user,
  I want to be able to place an order successfully
  So that I can purchase items from the store.

  @smoke
  Scenario: Successful order placement
    Given I am on the SauceDemo login page
    When I log in with username "standard_user" and password "secret_sauce"
    And I add "Sauce Labs Backpack", "Sauce Labs Bike Light", and "Sauce Labs Bolt T-Shirt" to the cart
    And I proceed to checkout
    And I fill in the checkout information with "First", "Last", and "11111" as zip code
    And I finalize the order
    Then I should see the "Thank you for your order!" confirmation message
