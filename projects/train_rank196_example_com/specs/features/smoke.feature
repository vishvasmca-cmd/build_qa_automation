Feature: Basic Website Navigation and Element Identification
  As a user,
  I want to navigate the website and identify key elements,
  So that I can ensure the website is functioning correctly.

  @smoke
  Scenario: Navigate to the website and identify elements
    Given I navigate to "https://www.example.com"
    Then I should be able to see the "Learn more" link
    And I should be able to scroll the page
