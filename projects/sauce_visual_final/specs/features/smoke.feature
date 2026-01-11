Feature: Login and Product Price Check
  As a user,
  I want to be able to log in and see the product price,
  So that I can verify the core functionality of the website.

  @smoke
  Scenario: Successful Login and Product Price Verification
    Given I am on the login page
    When I enter valid username "standard_user"
    And I enter valid password "secret_sauce"
    And I click the login button
    Then I should be logged in and see the inventory page
    And I should see the price of the first product
