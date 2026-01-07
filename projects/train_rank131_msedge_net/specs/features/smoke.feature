Feature: Element Verification on Google Homepage
  As a user,
  I want to verify the presence of specific elements on the Google homepage
  So that I can ensure the basic structure and navigation are working correctly.

  @smoke
  Scenario: Verify presence of buttons and links
    Given I navigate to "https://www.google.com"
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
