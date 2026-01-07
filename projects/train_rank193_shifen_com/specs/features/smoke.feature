Feature: Basic UI Element Identification
  As a user,
  I want to verify the presence of key UI elements
  So that I can ensure the basic structure of the website is intact.

  @smoke
  Scenario: Verify website loads and identifies UI elements
    Given I navigate to "https://www.google.com"
    Then I should be able to identify links on the page
    And I should be able to scroll the page
