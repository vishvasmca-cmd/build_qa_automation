Feature: Kaspersky Website - Smoke Tests

  Scenario: Verify Scrolling to the Bottom of the Homepage
    @smoke
    Given User navigates to the Kaspersky homepage
    When User scrolls to the bottom of the page
    Then User should be able to view the bottom section of the page
