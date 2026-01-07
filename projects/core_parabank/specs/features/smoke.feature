Feature: ParaBank Smoke Tests
  As a user of ParaBank
  I want to perform basic actions
  So that I can verify the core functionality

  @smoke
<<<<<<< Updated upstream
  Scenario: Verify ParaBank Home Page Load
    Given I navigate to the ParaBank home page
    Then I should see the ParaBank logo
    And I should see the "Register" link

  @smoke
  Scenario: Attempt to navigate to Account History and return to Home
    Given I am on the ParaBank home page
    When I click on the "Account History" link
    Then I should be redirected back to the ParaBank home page
=======
  Scenario: Verify successful login
    Given I am on the ParaBank login page
    When I enter valid username and password
    And I click the login button
    Then I should be logged in successfully

  @smoke
  Scenario: Perform internal fund transfer
    Given I am logged in to ParaBank
    When I initiate an internal fund transfer from checking to savings
    Then the transfer should be successful

  @smoke
  Scenario: View recent transactions
    Given I am logged in to ParaBank
    When I navigate to the account history page
    Then I should be able to view my recent transactions
>>>>>>> Stashed changes
