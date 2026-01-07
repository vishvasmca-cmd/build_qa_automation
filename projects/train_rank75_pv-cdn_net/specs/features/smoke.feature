Feature: Website Element Identification
  As a user,
  I want to verify the presence of key UI elements on the website,
  So that I can ensure the basic structure and navigation are functional.

  @smoke
  Scenario: Launch website and identify UI elements
    Given I navigate to "https://www.google.com"
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
