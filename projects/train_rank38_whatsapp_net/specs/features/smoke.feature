Feature: Homepage UI Elements Verification
  As a user
  I want to verify the presence of key UI elements on the homepage
  So that I can ensure the basic structure of the website is intact

  @smoke
  Scenario: Verify the presence of buttons, links, and menu bars
    Given I am on the whatsapp.net homepage
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
