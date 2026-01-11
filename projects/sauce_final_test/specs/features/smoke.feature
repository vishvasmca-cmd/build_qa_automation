Feature: Login and Verify Product Price
  As a user, I want to log in and verify the first product price is visible.

  @smoke
  Scenario: Successful login and product price verification
    Given I am on the Saucedemo login page
    When I enter username "standard_user"
    And I enter password "secret_sauce"
    And I click the login button
    Then I should be logged in and see the inventory page
    And I should see the price of the first product
