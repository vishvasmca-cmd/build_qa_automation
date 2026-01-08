Feature: Smoke Tests for core_parabank

  Scenario: Verify Login Page
    Given I am on the ParaBank login page
    Then I should see the username and password fields
    And I should see the login button
    @smoke

  Scenario: Check Find Transactions Link
    Given I am on the ParaBank login page
    Then I should see the "Find Transactions" link
    @smoke

  Scenario: Navigate to About Us Page
    Given I am on the ParaBank login page
    When I click the "About Us" link
    Then I should be on the "About Us" page
    @smoke