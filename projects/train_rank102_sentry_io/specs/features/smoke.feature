Feature: Sentry.io Website - Smoke Tests

  @smoke
  Scenario: Verify key elements are present on the homepage
    Given User navigates to the Sentry.io homepage
    Then User should be able to identify at least 5 buttons
    And User should be able to identify at least 2 links
    And User should be able to identify at least 2 menu bars
