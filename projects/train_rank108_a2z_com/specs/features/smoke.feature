Feature: Website Navigation and Element Identification
  As a user,
  I want to navigate to a website and identify key elements,
  So that I can verify the basic functionality of the website.

  @smoke
  Scenario: Navigate to a website
    Given I navigate to "google.com"
    Then the page should load successfully

  @smoke
  Scenario: Identify elements on the page
    Given I am on "google.com"
    Then I should be able to identify at least 5 buttons
    And I should be able to identify at least 2 links
    And I should be able to identify at least 2 menu bars
