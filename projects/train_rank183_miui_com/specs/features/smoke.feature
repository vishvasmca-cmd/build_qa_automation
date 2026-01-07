Feature: MIUI Website - Smoke Tests

  @smoke
  Scenario: Verify presence of links and buttons on the homepage
    Given User navigates to the MIUI homepage
    Then User should be able to identify at least 2 links
    And User should be able to identify at least 5 buttons
