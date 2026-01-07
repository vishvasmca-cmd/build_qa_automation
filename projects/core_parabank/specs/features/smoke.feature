Feature: ParaBank Smoke Tests

  @smoke
  Scenario: Verify successful navigation to the home page
    Given User navigates to the ParaBank home page
    Then The ParaBank home page should be displayed

  @smoke
  Scenario: Attempt to access account history
    Given User is on the ParaBank home page
    When User clicks on the 'Account History' link
    Then User should be redirected to the home page

  @smoke
  Scenario: Verify navigation to the home page after a 404 error
    Given User encounters a 404 error page
    When User navigates to the ParaBank home page
    Then The ParaBank home page should be displayed
