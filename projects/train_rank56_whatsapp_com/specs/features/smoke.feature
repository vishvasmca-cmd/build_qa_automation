Feature: WhatsApp Homepage - Element Presence
  As a user,
  I want to verify the presence of key elements on the WhatsApp homepage
  So that I can ensure the website is functioning correctly.

  @smoke
  Scenario: Verify the presence of buttons and links
    Given I am on the WhatsApp homepage
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
