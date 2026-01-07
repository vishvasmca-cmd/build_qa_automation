Feature: Website Element Identification
  As a user,
  I want to navigate to a website and identify key elements
  So that I can verify the basic structure of the website

  @smoke
  Scenario: Navigate to a website and identify elements
    Given I navigate to "https://google.com/"
    Then I should be able to identify at least 5 buttons
    And I should be able to identify at least 2 links
    And I should be able to identify at least 2 menu bars
