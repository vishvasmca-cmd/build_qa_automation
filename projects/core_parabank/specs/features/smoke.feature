Feature: ParaBank Smoke Tests

  @smoke
  Scenario: Verify ParaBank Home Page and Navigation
    Given User navigates to the ParaBank home page
    Then The ParaBank home page should be displayed

  @smoke
  Scenario: Check Account History Link
    Given User is on the ParaBank home page
    When User clicks on the Account History link
    Then User should be redirected to the Account History page

  @smoke
  Scenario: Navigate to About Us Page
    Given User is on the ParaBank home page
    When User navigates to the About Us page
    Then The About Us page should be displayed
