Feature: UI Element Identification
  As a user,
  I want to verify the presence of key UI elements
  So that I can ensure the basic structure of the website is correct.

  @smoke
  Scenario: Identify buttons and links on the homepage
    Given I navigate to "https://www.google.com"
    Then I should be able to identify buttons and links on the page
