Feature: Google Homepage - Element Presence
  As a user,
  I want to verify the presence of key elements on the Google homepage
  So that I can ensure the basic functionality is available.

  @smoke
  Scenario: Verify the presence of links on the Google homepage
    Given I navigate to "https://www.google.com"
    Then I should see the "About" link
