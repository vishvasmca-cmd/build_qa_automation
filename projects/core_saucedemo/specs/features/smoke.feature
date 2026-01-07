Feature: Smoke Tests for core_saucedemo

  As a user,
  I want to perform basic actions on the Saucedemo website
  So that I can verify the core functionality is working

  @smoke
  Scenario: Login, sort products, and add to cart
    Given I am on the login page
    When I log in with username "standard_user" and password "secret_sauce"
    And I sort products by "Price (low to high)"
