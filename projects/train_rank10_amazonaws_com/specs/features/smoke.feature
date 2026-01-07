Feature: Identify UI Elements on Amazon AWS Website
  As a tester
  I want to verify the presence of key UI elements on the Amazon AWS website
  So that I can ensure the website is functioning correctly

  @smoke
  Scenario: Verify presence of buttons, links, and menu bars on the homepage
    Given I navigate to "https://amazonaws.com"
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
