Feature: E-commerce Smoke Tests

  As a user,
  I want to perform basic actions on the e-commerce platform,
  So that I can verify the core functionalities are working as expected.

  @smoke
  Scenario: Login, sort products, and add to cart
    Given I am on the Saucedemo login page
    When I log in with username "standard_user" and password "secret_sauce"
    Then I should be redirected to the inventory page
    When I sort the products by "Price (low to high)"
    Then the products should be sorted by price from low to high
