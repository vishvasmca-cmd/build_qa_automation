Feature: Website Navigation and Element Identification
  As a user,
  I want to navigate to the website and identify key elements,
  So that I can verify the basic functionality of the website.

  @smoke
  Scenario: Navigate to the website
    Given I navigate to "https://www.example.com"
    Then the page should load successfully

  @smoke
  Scenario: Attempt to navigate to the website again
    Given I navigate to "https://www.example.com"
    Then the page should load successfully

  @smoke
  Scenario: Attempt to navigate to the website a third time
    Given I navigate to "https://www.example.com"
    Then the page should load successfully