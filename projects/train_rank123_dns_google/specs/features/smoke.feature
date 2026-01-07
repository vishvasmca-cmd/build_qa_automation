Feature: DNS.google - Smoke Tests

  @smoke
  Scenario: Verify presence of key elements on the homepage
    Given User navigates to the DNS.google homepage
    Then User should see the 'Get Started with Google Public DNS' link
    And User should see the 'Resolve' button

  @smoke
  Scenario: Verify scrolling functionality
    Given User navigates to the DNS.google homepage
    When User scrolls down the page
    Then User should still see the 'Get Started with Google Public DNS' link
