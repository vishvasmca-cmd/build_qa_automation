Feature: DuckDuckGo Search Functionality
  As a user,
  I want to be able to search on DuckDuckGo
  So that I can find information quickly and easily.

  @smoke
  Scenario: Search for 'Universal Gravity' and verify results are displayed
    Given I am on the DuckDuckGo homepage
    When I search for "Universal Gravity"
    Then I should see search results for "Universal Gravity"
