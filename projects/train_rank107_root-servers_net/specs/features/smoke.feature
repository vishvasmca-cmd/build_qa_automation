Feature: Website Element Identification
  As a user,
  I want to verify the presence of key elements on the website
  So that I can ensure the website is functioning correctly.

  @smoke
  Scenario: Navigate to a website and identify elements
    Given I navigate to "google.com"
    Then I should be able to identify buttons, links, and menu bars
