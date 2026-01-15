Feature: Google Finance - Smoke Tests
  As a user,
  I want to verify the core functionality of Google Finance
  So that I can ensure the application is working as expected

  @smoke
  Scenario: Verify Homepage Load and Basic Elements
    Given I navigate to the Google Finance homepage
    Then I should see the 'Google Finance' logo
    And I should see the 'Compare Markets' section with major indices

  @smoke
  Scenario: Search for a Stock and Verify Navigation
    Given I am on the Google Finance homepage
    When I search for 'TES'
    Then Tesla (TSLA) should appear in the search suggestions
    When I click on the Tesla suggestion
    Then I should be redirected to the Tesla stock detail page
