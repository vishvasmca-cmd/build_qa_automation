Feature: Website Element Identification
  As a user,
  I want to verify the presence of key elements on the website,
  So that I can ensure the website is functioning correctly.

  @smoke
  Scenario: Verify website loads and identifies elements
    Given I navigate to "https://windows.net"
    Then I should see at least 5 buttons
    And I should see at least 2 links
    And I should see at least 2 menu bars
