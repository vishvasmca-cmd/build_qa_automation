Feature: User Registration
  As a new user
  I want to register on the ParaBank website
  So that I can access banking services

  Scenario: Successful user registration
    Given I am on the ParaBank home page
    When I click the "Register" link
    And I fill in the registration form with valid data:
      | firstName   | lastName | address       | city      | state | zipCode | phoneNumber | ssn         | username   | password    | confirm     |
      | John        | Doe      | 123 Main Street | New York  | NY    | 10001   | 555-1234    | 123-45-6789 | Test@1234 | Test@1234 |
    And I click the "Register" button
    Then I should be redirected to the home page

  Scenario: Open new account
    Given I am on the ParaBank home page
    When I click the "Open New Account" link
    And I select an account type
    And I click the "Open New Account" button
    Then I should be redirected to the accounts overview page

  Scenario: Transfer funds
    Given I am on the ParaBank home page
    When I click the "Transfer Funds" link
    And I enter the amount to transfer as "10"
    And I click the "Transfer" button
    Then the transfer should be successful

  Scenario: Bill Payment
    Given I am on the ParaBank home page
    When I click the "Bill Pay" link
    And I fill in the bill payment form with valid data:
      | payeeName     | address       | city      | state | zipCode | phoneNumber | accountNumber | verifyAccount | amount |
      | John Doe      | 123 Main Street | New York  | NY    | 10001   | 555-1234    | 12345         | 12345         | 100    |
    And I click the "Send Payment" button
    Then the bill payment should be successful and I should be redirected to the home page

  Scenario: Navigate to About Us page and back to Home
    Given I am on the ParaBank home page
    When I click the "About Us" link
    And I click the "Home" link
    Then I should be redirected to the home page