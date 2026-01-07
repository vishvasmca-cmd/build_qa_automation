Feature: Website Element Identification
  As a user,
  I want to verify the presence of key elements on the website
  So that I can ensure the website is functioning correctly.

  @smoke
  Scenario: Launch website and attempt to identify elements
    Given I navigate to "google.com"
    Then the page should load without errors
