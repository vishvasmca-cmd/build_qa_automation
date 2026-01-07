Feature: Website Element Identification
  As a user,
  I want to verify the presence of key UI elements
  So that I can ensure the website's basic structure is intact.

  @smoke
  Scenario: Verify presence of buttons and links
    Given I am on the "https://workers.cloudflare.com/" page
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
