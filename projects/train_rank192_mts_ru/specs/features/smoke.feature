Feature: MTS.RU Homepage - UI Element Presence
  As a user
  I want to verify the presence of key UI elements on the MTS.RU homepage
  So that I can ensure the basic structure and navigation are functional

  @smoke
  Scenario: Verify presence of buttons and links
    Given I am on the MTS.RU homepage
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
