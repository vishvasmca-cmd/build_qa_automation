Feature: Homepage UI Elements
  As a user,
  I want to see the basic UI elements on the homepage,
  So that I can navigate and interact with the website.

  @smoke
  Scenario: Verify website navigation and identify UI elements
    Given I navigate to "https://www.example.com"
    Then I should be able to see buttons, links, and menu bars
