Feature: Basic Website Functionality
  As a user,
  I want to verify the basic elements of the website are present
  So that I can ensure the website is functioning correctly.

  @smoke
  Scenario: Verify website loads and identifies basic elements
    Given I navigate to "https://www.example.com"
    Then I should be able to find at least 1 link

