Feature: Criteo Homepage - UI Element Presence
  As a user
  I want to verify the presence of key UI elements on the Criteo homepage
  So that I can ensure the basic structure and content are loading correctly

  @smoke
  Scenario: Verify the presence of 5 buttons
    Given I am on the Criteo homepage
    Then I should see at least 5 buttons

  @smoke
  Scenario: Verify the presence of 2 links
    Given I am on the Criteo homepage
    Then I should see at least 2 links
