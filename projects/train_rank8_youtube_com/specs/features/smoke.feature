Feature: YouTube Homepage - Element Identification
  As a user,
  I want to verify the presence of key elements on the YouTube homepage
  So that I can ensure the basic structure and functionality are intact.

  @smoke
  Scenario: Identify buttons and links on the homepage
    Given I am on the YouTube homepage
    Then I should be able to identify at least 5 buttons
    And I should be able to identify at least 2 links
    And I should be able to identify at least 2 menu bars
