Feature: core_saucedemo Smoke Tests

<<<<<<< Updated upstream
  @smoke
  Scenario: User Login and Sort Products by Price
    Given User is on the Saucedemo login page
    When User logs in with valid credentials
    Then User should be redirected to the inventory page
    When User sorts products by price (low to high)
    Then Products should be sorted correctly

  @smoke
  Scenario: Add a product to the cart
    Given User is on the inventory page
    When User adds the cheapest product to the cart
    Then The product should be added to the cart
=======
  Scenario: User Login, Sort Products, and Add to Cart
    @smoke
    Given User is on the login page
    When User enters valid username "standard_user"
    And User enters valid password "secret_sauce"
    And User clicks on the login button
    Then User should be logged in and redirected to the inventory page
    When User sorts products by price (low to high)
    And User adds the lowest price item to the cart
    Then The item should be added to the cart
>>>>>>> Stashed changes
