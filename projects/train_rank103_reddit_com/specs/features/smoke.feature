Feature: Reddit Homepage - Smoke Tests

  Scenario: Verify presence of buttons and links on the homepage
    @smoke
    Given I am on the Reddit homepage
    Then I should see at least 5 buttons
    And I should see at least 2 links
