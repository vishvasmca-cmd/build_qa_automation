Feature: Smoke Tests for core_saucedemo

  As a user,
  I want to perform basic actions on the Saucedemo website
  To ensure the core functionalities are working as expected.

  @smoke
  Scenario: Successful Login and Sort Products by Price
    Given I am on the Saucedemo login page
    When I enter valid username "standard_user"
    And I enter valid password "secret_sauce"
    And I click the login button
    Then I should be logged in and redirected to the inventory page
    When I sort the products by "Price (low to high)"
    Then the products should be sorted by price from low to high
