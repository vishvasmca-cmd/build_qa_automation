Feature: Login and Product Price Verification
  As a user, I want to log in and verify the first product price is visible.

  @smoke
  Scenario: Successful login and price verification
    Given I am on the Saucedemo login page
    When I enter "standard_user" as the username
    And I enter "secret_sauce" as the password
    And I click the login button
    Then I should be logged in and see the product inventory
    And the price of the first product should be visible
