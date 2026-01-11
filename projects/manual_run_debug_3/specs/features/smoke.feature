Feature: Login Functionality
  As a user
  I want to be able to log in to the Saucedemo website
  So that I can access the inventory page

  @smoke
  Scenario: Successful Login with Valid Credentials
    Given I am on the Saucedemo login page
    When I enter the username "standard_user"
    And I enter the password "secret_sauce"
    Then I should be logged in and redirected to the inventory page
