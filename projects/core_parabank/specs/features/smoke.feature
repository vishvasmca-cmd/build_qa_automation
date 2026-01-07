Feature: ParaBank Smoke Tests

  @smoke
  Scenario: Verify Login Page and Attempt Account History Navigation
    Given User is on the ParaBank login page
    When User clicks on the Account History link
    Then User should be redirected back to the home page
