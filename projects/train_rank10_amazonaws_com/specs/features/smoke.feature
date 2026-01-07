Feature: Website Element Identification
  As a user,
  I want to verify the presence of key elements on the website,
  So that I can ensure the website is functioning correctly.

  @smoke
  Scenario: Verify website homepage loads successfully and identifies key elements
    Given I navigate to "https://www.google.com"
    Then I should see at least 2 links
    Then I should see at least 5 buttons
    Then I should see at least 2 menu bars
