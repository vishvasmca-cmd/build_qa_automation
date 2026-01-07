Feature: Website Element Identification
  As a user,
  I want to verify the presence of key elements on the website
  So that I can ensure the website is functioning correctly.

  @smoke
  Scenario: Launch Website and Attempt to Identify Elements
    Given I navigate to "https://www.example.com"
    Then I should be able to see the website
