Feature: User Registration
  As a user
  I want to register on the ParaBank website
  So that I can use the banking services

  @smoke
  Scenario: Successful user registration
    Given I am on the registration page
    When I fill in the registration form with valid data
      | firstName | lastName | address | city | state | zipCode | phone | ssn | username | password |
      | test      | test     | test    | test | test  | 12345   | 12345 | 123 | test     | test     |
    And I click the register button
    Then I should be registered successfully

