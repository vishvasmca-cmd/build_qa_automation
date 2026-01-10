Feature: Login Functionality
  As a user
  I want to be able to log in to the application
  So that I can access the application's features

  @smoke
  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter the username "standard_user"
    And I enter the password "secret_sauce"
    Then I should be logged in successfully
