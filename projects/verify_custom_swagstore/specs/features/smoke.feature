Feature: Login Functionality
  As a user
  I want to be able to log in to the application
  So that I can access the application's features

  @smoke
  Scenario: Successful login with valid credentials
    Given I am on the login page "https://www.saucedemo.com/v1/"
    When I enter username "standard_user" and password "secret_sauce"
    Then I should be logged in successfully
