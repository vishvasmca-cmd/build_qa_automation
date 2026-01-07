Feature: Mail.ru Homepage - Element Presence
  As a user,
  I want to verify the presence of key elements on the Mail.ru homepage
  So that I can ensure the basic structure and navigation are functional.

  @smoke
  Scenario: Verify presence of buttons and links on homepage
    Given I am on the Mail.ru homepage
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
