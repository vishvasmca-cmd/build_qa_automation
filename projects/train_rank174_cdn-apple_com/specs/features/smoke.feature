Feature: Website Navigation and Element Identification
  As a user,
  I want to navigate to a website and identify key elements,
  So that I can verify the website's basic structure and functionality.

  @smoke
  Scenario: Launch website and identify elements
    Given I navigate to "https://www.google.com"
    Then I should be able to identify elements on the page
