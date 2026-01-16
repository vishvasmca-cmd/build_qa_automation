Feature: Wikipedia Search
  As a user
  I want to search for information on Wikipedia
  So that I can find the information I need

  @smoke
  Scenario: Search for 'Antigravity' and verify the heading contains 'Anti-gravity'
    Given I am on the Wikipedia Main Page
    When I search for "Antigravity"
    Then the heading should contain "Anti-gravity"