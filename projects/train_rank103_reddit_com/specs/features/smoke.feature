Feature: Reddit Homepage UI Elements
  As a user
  I want to see key UI elements on the Reddit homepage
  So that I can easily navigate and interact with the site

  @smoke
  Scenario: Verify presence of buttons and links
    Given I am on the Reddit homepage
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
