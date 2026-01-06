Feature: Verify Saucedemo Website
  As a user
  I want to ensure the Saucedemo website is functioning correctly
  So that I can use its features

  @smoke
  Scenario: Verify successful page load
    Given I navigate to "https://www.saucedemo.com/"
    Then the page should load successfully
