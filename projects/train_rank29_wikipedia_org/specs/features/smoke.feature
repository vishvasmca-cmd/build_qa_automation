Feature: Wikipedia Homepage - Smoke Tests
  As a user,
  I want to verify the presence of key elements on the Wikipedia homepage
  So that I can ensure the basic functionality is working.

  @smoke
  Scenario: Verify the presence of buttons, links, and menu bars
    Given I am on the Wikipedia homepage
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
