Feature: ParaBank Smoke Tests

  @smoke
  Scenario: Verify successful login
    Given User is on the ParaBank login page
    When User enters valid username and password
    And User clicks the login button
    Then User should be logged in successfully

  @smoke
  Scenario: Perform internal fund transfer
    Given User is logged in
    When User initiates an internal fund transfer from checking to savings
    Then The fund transfer should be successful

  @smoke
  Scenario: View recent transactions
    Given User is logged in
    When User navigates to the account history page
    Then User should be able to view recent transactions
