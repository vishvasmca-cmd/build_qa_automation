Feature: SoundCloud Smoke Tests

  @smoke
  Scenario: Launch SoundCloud and find elements
    Given User navigates to the SoundCloud homepage
    Then User should see the "Sign in" button
    Then User should be able to scroll the page
    Then User should see the "Create a SoundCloud account" button
