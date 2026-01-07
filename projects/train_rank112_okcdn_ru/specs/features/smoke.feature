Feature: Google Homepage Smoke Tests
  As a user
  I want to verify the basic functionality of the Google homepage

  @smoke
  Scenario: Verify Google.com is accessible
    Given I navigate to "https://www.google.com"
    Then the page should load successfully

  @smoke
  Scenario: Verify buttons and links can be identified on the Google homepage
    Given I am on the "https://www.google.com" page
    Then I should be able to identify buttons and links