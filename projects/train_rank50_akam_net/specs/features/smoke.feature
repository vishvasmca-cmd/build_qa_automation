Feature: Homepage Element Identification
  As a user,
  I want to verify the presence of key elements on the homepage,
  So that I can ensure the website is functioning correctly.

  @smoke
  Scenario: Launch website and identify elements
    Given I navigate to "https://www.example.com"
    Then I should see at least 1 link
