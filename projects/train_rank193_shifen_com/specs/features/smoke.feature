Feature: Landing Page Element Identification
  As a user,
  I want to verify the presence of key elements on the landing page
  So that I can ensure the basic functionality of the website is working.

  @smoke
  Scenario: Verify presence of buttons, links, and menu bars
    Given I navigate to "https://www.example.com"
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
