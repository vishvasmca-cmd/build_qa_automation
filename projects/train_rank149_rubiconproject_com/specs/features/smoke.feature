Feature: Website Element Identification
  As a user,
  I want to verify the presence of key elements on the rubiconproject.com website
  So that I can ensure the basic structure and navigation are functional.

  @smoke
  Scenario: Identify key elements on the homepage
    Given I navigate to "https://rubiconproject.com"
    Then I should be able to identify 5 buttons
    And I should be able to identify 2 links
    And I should be able to identify 2 menu bars
